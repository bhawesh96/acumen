# -*- coding: utf-8 -*-
import traceback, warnings
warnings.filterwarnings("ignore")
import requests

# from mysql.connector import MySQLConnection, Error

from flask import Flask, render_template, redirect, json, request, session, Markup
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'user2'
app.config['MYSQL_DATABASE_PASSWORD'] = 'passw'
app.config['MYSQL_DATABASE_DB'] = 'acumen'
app.config['MYSQL_DATABASE_HOST'] = '139.59.17.132'

mysql.init_app(app)

app.secret_key = '8bf9547569cd5a638931a8639cf9f86237931e92' 

@app.route('/home')
@app.route('/')
def main():
    # params = {'ques':'Who is the President of United States of America ?', 'quesImage': 'code.png'}
    params = {'ques':"Who is the president of America?", 'quesImage': False, 'story':"President is a mjor role and is given to one ho is highly responsible, smart and harworking but clubs make mistakes here"}
    return render_template('question.html', params = params)

@app.route('/login')
def showSignUp():
    return render_template('signin.html')

@app.route('/signup')
def showSignIn():
    return render_template('signup.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/signup',methods=['POST'])
def signUp():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _reg = request.form['inputRegno']
        _phone = request.form['inputPhone']
        # captcha_response = request.form['g-recaptcha-response']

        # validate the received values
        if _name and _email and _password and _reg and _phone:
            # All Good, let's call MySQL
            #validate captcha from api
            # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {'secret':captcha_secret_key ,'response':captcha_response})
            # is_success_captcha = r.json()['success']
            
            # if not is_success_captcha:
            #     return render_template("404.html",error = 'The captcha couldnt be verified')
            try:
                cursor.callproc('insert_player',(_name, _reg, _email, _phone, _password))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return render_template('signin.html')

                else:
                    return render_template('404.html', error="not unique")            
            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return render_template('404.html',error = "Enter all the values. Please :(")

    except Exception as e:
        return json.dumps({'errory':str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/login',methods=['POST'])
def validateLogin():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
       # captcha_response = request.form['g-recaptcha-response']

        # validate the received values
        if _email and _password:

            
            # All Good, let's call MySQL
            #validate captcha from api
            #r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {'secret':captcha_secret_key ,'response':captcha_response})
            #is_success_captcha = r.json()['success']
            
            #if not is_success_captcha:
            #    return render_template("404.html",error = 'The captcha couldnt be verified')
            try:
                data = cursor.callproc('validate_login',(_email, _password))
                data = cursor.fetchall()
                if len(data) > 0:
                    conn.commit()
                    session['user_id'] = str(data[0][0])
                    session['name'] = str(data[0][1])
                    session['email'] = str(data[0][3])
                    return redirect('/')
                else:
                    print 'not validated'
                    return render_template('404.html', error = "not validated")            
            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return render_template('404.html',error = "Enter all the values. Please :(")

    except Exception as e:
        return json.dumps({'errory':str(e)})
    finally:
        cursor.close()
        conn.close()

def updateScore():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM scores WHERE id = %s", (session['user_id']))
        data = cursor.fetchall()
        score = '0'
        money = '0'
        for player in data:
            score = float(session['point_wt']) + float(player[1])
            money = float(session['money_wt']) + float(player[2])
            session['correctly_answered'] = str(float(player[3])+1)
        cursor.execute("UPDATE scores SET points = %s, money = %s, correctly_answered = %s WHERE id = %s", (str(score), str(money), session['correctly_answered'], session['user_id']))
        conn.commit()
    except Exception as e:
        print str(e)
    return update()

def update():
    if(session.get('user_id')):
        conn = mysql.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE players SET curr_ques_id= %s WHERE id = %s", (session['curr_ques_id'], session['user_id']))
            conn.commit()
        except Exception as e:
            print str(e)
        return go_to_new_round

def getQuestion():
	if(session.get('user_id')):
		conn=mysql.connect()
		try:
		    cursor=conn.cursor()
		    cursor.execute("SELECT * FROM questions WHERE ques_id = %s", (session['curr_ques_id']))
		except Exception as e:
		    print str(e)
		data = cursor.fetchall()
		for value in data:
		    story = value[1]
		    ques = value[2]
		    session['curr_ans'] = value[3]
		    hint = value[4]
		params = {'story':story, 'ques':ques, 'ans':ans, 'hint':hint}
		conn.close()
		return params

@app.route('/question')
def question():
	if(session.get('user_id')):
		params = getQuestion()
		return render_template('question.html', params = params)
	else:
		return redirect('/singup')


@app.route('/question', methods=['POST'])
def validateAns():
	if(session.get('user_id')):
		_inputAns = str(request.form['answer']).lower().rstrip()
    	if(_inputAns == session['curr_ans']):
    		updateScore()

def updateHintScore():
	if(session.get('user_id')):
		conn = mysql.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE scores SET ")
            conn.commit()
        except Exception as e:
            print str(e)
     	return True

@app.route('/showHint', methods=['POST'])
def showHint():
	if(session.get('user_id')):
		updateHintScore()
		return redirect('/question')
	else:
		return redirect('/singup')
    

if __name__ == "__main__":
    app.run(debug=True,port=5006,use_evalex=False)
    # app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)
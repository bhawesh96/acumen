# -*- coding: utf-8 -*-
import traceback, warnings
warnings.filterwarnings("ignore")
import requests

# from mysql.connector import MySQLConnection, Error

from flask import Flask, render_template, redirect, json, request, session, Markup, flash
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'kodamr13_inquiz'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rtg8055'
app.config['MYSQL_DATABASE_DB'] = 'kodamr13_inquizitive'
app.config['MYSQL_DATABASE_HOST'] = '103.50.162.66'

mysql.init_app(app)

app.secret_key = '8bf9547569cd5a638931a8639cf9f86237931e92' 

@app.route('/')
@app.route('/home')
def main():
    if(session.get('user_id')):
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/login')
def showSignUp():
    if(session.get('user_id')):
        return redirect('/')
    else:
        return render_template('signin.html')

@app.route('/signup')
def showSignIn():
    if(session.get('user_id')):
        return redirect('/')
    else:
        return render_template('signup.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/instructions')
def instr():
    return render_template('instructions.html')

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
                cursor.callproc('insert_player_inquizitive',(_name, _reg, _email, _phone, _password))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return render_template('signin.html')

                else:
                    return render_template('404.html', error="not unique")            
            except Exception as e:
                return render_template('404.html', error = "Uh-huh! Some error. Please retry with valid fields")
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
                data = cursor.callproc('validate_login_inquizitive',(_email, _password))
                data = cursor.fetchall()
                if len(data) > 0:
                    conn.commit()
                    session['user_id'] = str(data[0][0])
                    session['name'] = str(data[0][1])
                    session['email'] = str(data[0][3])
                    session['curr_ques'] = str(data[0][6])
                    return redirect('/')
                else:
                    print 'not validated'
                    return render_template('signin.html', error="not validated")            
            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return render_template('404.html',error = "Enter all the values. Please :(")

    except Exception as e:
        return json.dumps({'errory':str(e)})
    finally:
        cursor.close()
        conn.close()

def updateScore(isAnswerCorrect):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM scores WHERE user_id = %s", (session['user_id']))
        data = cursor.fetchall()
        score = 0
        if(session['curr_difficulty'] == 1):
            points_to_be_added = 20
        elif(session['curr_difficulty'] == 2):
            points_to_be_added = 30
        elif(session['curr_difficulty'] == 3):
            points_to_be_added = 50

        if(not isAnswerCorrect):
            points_to_be_added = 0

        for player in data:
            score = int(player[1]) + points_to_be_added
            session['curr_score'] = score
        cursor.execute("UPDATE scores SET points = %s WHERE user_id = %s", (str(score), session['user_id']))
        conn.commit()
    except Exception as e:
        print str(e)
    return update()

def updateScoreRapid(isAnswerCorrect):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        
        if(isAnswerCorrect):
            session['correct_rapid'] +=1

        if(session['correct_rapid']==8):
            try:
                ins = "INSERT INTO winner_rapid values ("+ session['user_id']+",'" + session['curr_rapid_q'].split('_')[0] + "'"
                print(ins)
                cursor.execute("INSERT INTO winner_rapid values ("+ session['user_id']+",'" + session['curr_rapid_q'].split('_')[0] + "'")
            except Exception as e:
                print str(e)   ## to be commented in the end
                pass

    except Exception as e:
        print str(e)
    return updateRapid()

def updateRapid():
    if(session.get('user_id')):
        session['curr_rapid_q'] = session['curr_rapid_q'].split('_')[0]+ '_' + str(int(session['curr_rapid_q'].split('_')[1]) + 1)
    return True

def update():
    if(session.get('user_id')):
        session['curr_rapid'] = 0
        if(session['curr_ques'] == '1_20'):
            makeRapidZero()
            session['curr_rapid'] = 1
            session['correct_rapid'] = 0
            # session['curr_ques'] = str(int(session['curr_ques'].split('_')[0]) + 1) + '_0'
            session['curr_rapid_q'] = '1_1'
        elif(session['curr_ques'] == '2_20'):
            makeRapidZero()
            # session['curr_ques'] = str(int(session['curr_ques'].split('_')[0]) + 1) + '_0'
            session['curr_rapid'] = 2
            session['correct_rapid'] = 0
            session['curr_rapid_q'] = '2_1'
        elif(session['curr_ques'] == '3_20'):
            makeRapidZero()
            # session['curr_ques'] = str(int(session['curr_ques'].split('_')[0]) + 1) + '_0'
            session['curr_rapid'] = 3
            session['correct_rapid'] = 0
            session['curr_rapid_q'] = '3_1'
        elif(session['curr_ques'] == '4_20'):
            makeRapidZero()
            # session['curr_ques'] = str(int(session['curr_ques'].split('_')[0]) + 1) + '_0'
            session['curr_rapid'] = 4
            session['correct_rapid'] = 0
            session['curr_rapid_q'] = '4_1'
        session['curr_ques'] = session['curr_ques'].split('_')[0]+ '_' + str(int(session['curr_ques'].split('_')[1]) + 1)
        conn = mysql.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE players SET curr_ques = %s, curr_rapid = %s WHERE user_id = %s", (session['curr_ques'], session['curr_rapid'], session['user_id']))
            conn.commit()
        except Exception as e:
            print str(e)
        return True

def getRapidQuestion():
    if(session.get('user_id')):
        conn=mysql.connect()
        try:
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM rapid WHERE question_id = %s", (session['curr_rapid_q']))
        except Exception as e:
            print str(e)
        data = cursor.fetchall()
        for value in data:
            question = value[1]
            option1 = value[2]
            option2 = value[3]
            option3 = value[4]
            option4 = value[5]
            session['curr_ans'] = value[6]
        params = {'ques':question, 'option1':option1, 'option2':option2, 'option3':option3, 'option4':option4, 'ans':session['curr_ans']}
        conn.close()
        return params


def getQuestion():
    if(session.get('user_id')):
        conn=mysql.connect()
        try:
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM questions WHERE question_id = %s", (session['curr_ques']))
        except Exception as e:
            print str(e)
        data = cursor.fetchall()
        for value in data:
            question = value[1]
            option1 = value[2]
            option2 = value[3]
            option3 = value[4]
            option4 = value[5]
            quesImage = value[6]
            session['curr_difficulty'] = value[8]
            if(quesImage == 'False'):
                quesImage = False
            session['curr_ans'] = value[7]
        params = {'ques':question, 'option1':option1, 'option2':option2, 'option3':option3, 'option4':option4, 'difficulty':session['curr_difficulty'], 'quesImage':quesImage, 'ans':session['curr_ans']}
        conn.close()
        return params

@app.route('/newLevel')
def newLevel():
    if(session.get('user_id')):
        if(session['curr_ques'] == '1_1'):
            bg = "url('../static/image/level_1_storyline.jpg')"
            return render_template('newLevel1.html', bg=bg)
        elif(session['curr_ques'] == '2_1'):
            bg = "url('../static/image/level_2_storyline.jpg')"
            return render_template('newLevel2.html', bg=bg)
        elif(session['curr_ques'] == '3_1'):
            bg = "url('../static/image/level_3_storyline.jpg')"
            return render_template('newLevel3.html', bg=bg)
        elif(session['curr_ques'] == '4_1'):
            bg = "url('../static/image/level_4_storyline.jpg')"
            return render_template('newLevel4.html', bg=bg)
        else:
            return redirect('/question')

def makeRapidZero():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE players SET curr_rapid = 0 WHERE user_id = %s", (session['user_id']))
        conn.commit()
    except Exception as e:
        print str(e)

def rapidLevel():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT curr_rapid FROM players WHERE user_id = %s", (session['user_id']))
        data = cursor.fetchall()
        for player in data:
            curr_rapid = int(player[0])
        return curr_rapid
    except Exception as e:
        print str(e)
        return 0

def rapidFireEnd():
    if(session['curr_ques'] == '21'):
        session['curr_ques'] = str(int(session['curr_ques'].split('_')[0]) + 1) + '_1'
    conn = mysql.connect()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE players SET curr_ques = %s, curr_rapid = %s WHERE user_id = %s", (session['curr_ques'], session['curr_rapid'], session['user_id']))
        conn.commit()
    except Exception as e:
        print str(e)
    return True


@app.route('/rapidfire')
def rapidfire():
    if(session.get('user_id')):
        makeRapidZero()
        # if(rapidLevel() != 0):
        if('11' in session['curr_rapid_q']):
            # rapidFireEnd()
            return redirect('/question')
        params = getRapidQuestion()
        params['level'] = session['curr_rapid_q'].split('_')[0]
        params['question_number'] = session['curr_rapid_q'].split('_')[1]
        return render_template('rapid.html', params = params)
        # else:
            # return redirect('/question')
    else:
        return redirect('/login')

@app.route('/rapidfire', methods=['POST'])
def validateAnsx():
    if(session.get('user_id')):
        _inputAns = int(request.form['answer'])
        updateScoreRapid(_inputAns == int(session['curr_ans']))
        return redirect('/rapidfire')
    else:
        return redirect('/signup')

def fetchCurrentScore():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM scores WHERE user_id = %s", (session['user_id']))
        data = cursor.fetchall()
        for player in data:
            score = int(player[1])
            session['curr_score'] = score
    except Exception as e:
        print str(e)

@app.route('/question')
def question():
    if(session.get('user_id')):
        if(request.args.get('skipRapid') == 'True'):
            session['curr_ques'] = str(int(session['curr_ques'].split('_')[0]) + 1) + '_1'
            makeRapidZero()
            return redirect('/newLevel')
        if(session['curr_ques'] == '1_21'):
            fetchCurrentScore()
            return render_template('levelEnd1.html', score=session['curr_score'], showRapid=rapidLevel())
        elif(session['curr_ques'] == '2_21'):
            fetchCurrentScore()
            return render_template('levelEnd2.html', score=session['curr_score'], showRapid=rapidLevel())
        elif(session['curr_ques'] == '3_21'):
            fetchCurrentScore()
            return render_template('levelEnd3.html', score=session['curr_score'], showRapid=rapidLevel())
        elif(session['curr_ques'] == '4_21'):
            fetchCurrentScore()
            return render_template('levelEnd4.html', score=session['curr_score'], showRapid=rapidLevel())
        ## after 1_20 curr_ques is updated to 1_21 and curr_rapid (boolean to 1)##
        ## you have to redirct to /rapidfire and update the curr_rapid to zero!!!

        ## rapid fire round will be done (hopefully without errors) using all different and new variables
        ## so all other session variable values are the same 1_21(example)
        ## control will be redirected to /question once the rapidfire round completes properly!
        ## rest you have to do.
        params = getQuestion()
        params['level'] = session['curr_ques'].split('_')[0]
        if(params['level'] == '1'):
            bg = "url('../static/image/level_1_questions.jpg')"
        elif(params['level'] == '2'):
            bg = "url('../static/image/level_2_questions.jpg')"
        elif(params['level'] == '3'):
            bg = "url('../static/image/level_3_questions.jpg')"
        elif(params['level'] == '4'):
            bg = "url('../static/image/level_4_questions.jpg')"
        params['question_number'] = session['curr_ques'].split('_')[1]
        return render_template('questionfib.html', params = params, bg=bg)
    else:
        return redirect('/login')

@app.route('/question', methods=['POST'])
def validateAns():
    if(session.get('user_id')):
        _inputAns = int(request.form['answer'])
        updateScore(_inputAns == int(session['curr_ans']))
        return redirect('/question')
    else:
        return redirect('/signup')

@app.route('/admin')
def admin():
    return redirect('https://i0.kym-cdn.com/photos/images/original/000/232/114/e39.png', code=302)

if __name__ == "__main__":
    app.run(debug=True,port=10002,use_evalex=False)
    # app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)

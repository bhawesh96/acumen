import traceback, warnings
warnings.filterwarnings("ignore")
import requests

# from mysql.connector import MySQLConnection, Error

from flask import Flask, render_template, redirect, json, request, session
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

answers = {1: ['peat'], 2: ['7'], 3: ['Siemens'], 4: ['sn2'], 5: ['choke'], 6: ['graphite'], 7: ['Avogadro'], 8: ['helloworld'], 9: ['sodium hypochlorite'], 10: ['Subrahmanyan Chandrasekhar'], 11: ['20'], 12: ['1/4'], 13: ['0'], 14: ['Quantum Computing'], 15: ['increases'], 16: ['120'], 17: ['Petrache Poenaru'], 18: ['30'], 19: ['Kuiper'], 20: ['144'], 21: ['4'], 22: ['Coherence'], 23: ['710'], 24: ['9'], 25: ['30'], 26: ['180'], 27: ['Alpha centauri'], 28: ['nitrogen'], 29: ['dry powder'], 30: ['56'], 31: ['O'], 32: ['0.62'], 33: ['5'], 34: ['Humphry Davy'], 35: ['OH'], 36: ['Magnetic dip'], 37: ['decreases'], 38: ['West'], 39: ['6'], 40: ['45'], 41: ['0,1,2,0'], 42: ['30'], 43: ['Galileo Galilei '], 44: ['OS X'], 45: ['18'], 46: ['Audio Control'], 47: ['Poulsen'], 48: ['Encryption'], 49: ['429'], 50: ['Capillary Action'], 51: ['Spoofing'], 52: ["Faraday's Cage "]}

questions = {1: ['The only type of coal in which the deposit has some traces of the original plant material', False], 2: ['If a given triangle has a perimeter of 15, how many such triangles are possible if the sides are intergers?', False], 3: ['A derived unit in the SI system aplicable to three electrical quantities which is also the reciprocal of three other units', False], 4: ["Reaction mechanism which doesn't apply to tertiary alkly halides because of their size", False], 5: ['This electronic component serves a dual purpose in tubelights and gets its name from the action it performs on high frequency currents', False], 6: ["A contradictory element which is soft on the outside but commonly used as a reinforcing material for many devices. Doesn't conduct heat but electricity is another matter entirely", False], 7: ['"Three balloons have equal volume and hence the same number of molecules".This supports a famous law in chemistry. Who was the scientist after which it is named?', False], 8: ['9CODE', False], 9: ['You can find this compound in your bathroom and in pools. Wrongly believed that this could help you pass drug tests.', False], 10: ['Famous scientist who predicted a phenomenon for fast spinning stars years before which has now been observed by scientists.', False], 11: ['"Find the missing number. 11, 5, 14,10,17,20,   ,40"', False], 12: ['"There are two objects with masses m and 16m. they are moving with equal kinetic energy E. what is the ratio of their momentum?"', False], 13: ['14CODE', False], 14: ['"When asked to describe this new initiative, Bill Gates describe the physics as ""hieroglyphics"" and Satya Nadella couldn\'t describe this in a single sentence. Microsoft recently released a prgramming language for this invention. What is this?"', False], 15: ['If the mass of the earth decreased to half its original mass and the radius increased to twice its radius the acceleration due to gravity________ by 2.', False], 16: ['"5, 6, 10, 19, 35, 71, What is the next number in the series?"', False], 17: ['"A Romanian inventor, mathematician, physicist, engineer and politician among others. He is widely credited with patenting a writing instrument popular for its elegance, prestige and which is also a collector\'s item. Name this person"', False], 18: ['"Out of 5 consonants and 3 vowels, how many words of 3 consonants and 2 vowels can be formed?"', False], 19: ["This belt isn't an accessory, but a disc. The materials for this include methane,ammonia and water. It is named after a Dutch professor who was part of a plan to detonate a nuclear warhead on the moon.", False], 20: ["In how many different ways can the letters of the word 'EATING' be arranged in such a way that the vowels always come together?", False], 21: ['John was born on Feb 29th of 2012 which happened to be a Wednesday. If he lives to be 101 years old, how many birthdays would he celebrate on a Wednesday?', False], 22: ['The picture describes a physics phenomenon', 'work.jpg'], 23: ['What is the capacitance of the earth, viewed as an isolated conducting sphere of radius R=6370km? (in uF)', False], 24: ['', 'work.jpg'], 25: ['26CODE', False], 26: ["An accurate clock shows 8 o'clock in the morning. Through how may degrees will the hour hand rotate when the clock shows 2 o&#39;clock in the afternoon?", False], 27: ['Identify the three star system', False], 28: ['That crucial element of an incandescent light bulb without which the life of the tungsten filament would be considerably shortened.', False], 29: ['In a petroleum fires, since water is heavier than petrol, it causes the petrol to rise to the surface and continue burning. Name the alternative that extinguishes petroleum fires', False], 30: ['In a locality, there are ten houses in a row. On a particular night a thief planned to steal from three houses of the locality. In how many ways can he plan such that no two of them are next to each other?', False], 31: ['32CODE', False], 32: ['"An electrical generator consists of a rectangular loop of dimension 8.4 cm by 15.4 cm. It rotates in a uniform magnetic field of 0.126T at a frequency of 60 Hz about an axis perpendicular to the field direction. What is the maximum emf generated by the loop?"', False], 33: ['34CODE', False], 34: ['This product proved extremely useful in coal mines by providing a test fpr the presence of gases due to the varying intensity of its brightness. Name the inventor who is best known for isolating a few alkaline earth elements.', False], 35: ['FY, HA, KD,?', False], 36: ['Airplane compasses tend to align toward the north in the northern hemisphere and toward the south in the southern hemisphere. What is the error due to which comass navigation is almost impossible near the poles?', False], 37: ['The energy of dipole________ when rotated from unstable to stable equilibrium in a uniform magnetic field.', False], 38: ['A straight wire carrying current in vertically upward direction is placed in a uniform magnetic field directed towards north. The magnetic force acting on the wire is towards', False], 39: ['What is the number f folds for a paper to reach the moon assuming it to be of thickness 0.01mm?', False], 40: ['42CODE', False], 41: ['This unit is named after a scientist who shared the Nobel with two other eminent scientists working in the same field.', False], 42: ['44CODE', False], 43: ['A famous Danish footballer and a tape recorder are shown. The name of a scientist is the link between them', False], 44: ['Which one of the following remains constant while throwing a ball upward?', False], 45: ['These 2 scientists were credited with the invention of thermometer. But it was actually invented by ____', False], 46: ['The hybrid kernel developed by Carnegie Mellon University is used in which OS _____', False], 47: ['A bag contains 12 rerd marbles,5 yellow marbles and 15 green marbles. How many additional red marbles must be added to the 32 marbles already in the bag so that the probability of randamly drawing a red marble is 3/5?', False], 48: ['Which of the following software monitors and records computer transactions?', False], 49: ['Name the inventor.', False], 50: ['The scrambling of a code is called ______', False], 51: ['Look at this series: 8, 6, 9, 23, 87 , ... What number should come next?', False], 52: ['The necessary phenomena that allows drainage of tears.', False]} 

@app.route('/home')
@app.route('/')
def main():
    params = {'ques':'Who is the President of United States of America ?', 'quesImage': 'work.jpg'}
    return render_template('question.html', params = params)

@app.route('/login')
def showSignUp():
    return render_template('signin.html')

@app.route('/signup')
def showSignIn():
    return render_template('signup.html')

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


def getQuestion(ques):
	params = {'ques':questions[ques][0], 'quesImage':questions[ques][1]}
	return params

@app.route('/question')
def question():
	if(session.get('user_id')):
		params = getQuestion(session['curr_ques'])
		return render_template('question.html', params = params)


@app.route('/question', methods=['POST'])
def validateAns():
    _inputAns = str(request.form['answer']).lower().rstrip()
    if(ians == answers(int(session['quesNo']))):
    	updateScore()
    updateQuestion()
    return redirect('/question')

if __name__ == "__main__":
    app.run(debug=True,port=5006,use_evalex=False)
    # app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)
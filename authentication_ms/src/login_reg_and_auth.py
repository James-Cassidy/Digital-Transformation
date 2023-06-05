import random
from flask import Flask, Response, request
import jwt
import datetime
from functools import wraps
import requests
import json
import smtplib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#AWS ec2 instance public ip
dburl = url = "http://ec2-3-85-193-157.compute-1.amazonaws.com:3306/"
# dburl = url = "http://0.0.0.0:3306/"
app.config['SECRET_KEY'] = 'group6secretkey'

#save email and password to app config
app.config['EMAIL'] = 'mentalhealth2fa@gmail.com'
app.config['PASSWORD'] = 'vvmsunzojztbqlxh'

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    userID = -1

    if not auth or not auth.username or not auth.password:
        error=True
        text="Could not verify user. Username or password not provided."
        status = 500

        r = {
            "error": error,
            "string": text,
            "answer": userID
        }

    else:
        email = auth.username
        password = auth.password

        #send basic auth to auth service
        payload = {
            "email": email,
            "password": password
        }

        url = dburl+"login"

        res = requests.post(url, json=payload, auth=(email, password))
    

    if res.status_code != 200:
        response = Response(response=res, status=res.status_code, mimetype="application/json")

        response.headers["Content-Type"]="application/json"
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response

    resJSON = json.loads(res.json()['answer'])
    print(resJSON)
    print(resJSON['userID'])
    print(resJSON['email'])
    print(resJSON['userForename'])
    print(resJSON['userSurname'])
    print(resJSON['userTherapist'])

    tfatoken = genToken(resJSON['userID'], tfaFlag=True, email=resJSON['email'])

    status = 200

    a = {
        'tfaToken': tfatoken,
        'userForename': resJSON['userForename'],
        'userSurname': resJSON['userSurname'],
        'userTherapist': resJSON['userTherapist']
    }

    r = {
            "error": False,
            "string": "2FA token generated",
            "answer": a
        }

    reply = json.dumps(r)
    response = Response(response=reply, status=status, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

@app.route('/register', methods=['GET'])
def register():
    url = dburl+"insertUser"

    email = request.args.get('email')
    password = request.args.get('password')
    forename = request.args.get('forename')
    surname = request.args.get('surname')
    dob = request.args.get('dob')
    gender = request.args.get('gender')
    address1 = request.args.get('address1')
    city = request.args.get('city')
    country = request.args.get('country')
    postcode = request.args.get('postcode')

    if request.args.get('middle_names'):
        middle_names = request.args.get('middle_names')
    else:
        middle_names = ''
    if request.args.get('address2'):
        address2 = request.args.get('address2')
    else:
        address2 = ''
    if request.args.get('address3'):
        address3 = request.args.get('address3')
    else:
        address3 = ''

    res = requests.get(url, params={"email": email, "password": password, "forename": forename,
    "surname": surname, "dob": dob, "gender": gender, "address1": address1, "address2": address2,
    "address3": address3, "city": city, "country": country, "postcode": postcode, "middle_names": middle_names})

    if res.status_code != 200:
        response = Response(response=res, status=res.status_code, mimetype="application/json")

        response.headers["Content-Type"]="application/json"
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response
    
    else:
        #get asnwer from res
        userID = res.json()["answer"]
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        token = jwt.encode({'userID' : userID, 'exp' : expires}, app.config['SECRET_KEY'])

        # print(expires)
        status = 200

        r = {
                "error": False,
                "string": "User verified",
                "answer": token
            }

        reply = json.dumps(r)
        response = Response(response=reply, status=status, mimetype="application/json")

        response.headers["Content-Type"]="application/json"
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response


def requires_token(f):
    @wraps(f)
    def dec(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            status = 401
            r = {
                    "error": True,
                    "string": "Token not provided",
                    "answer": -1
                }

            reply = json.dumps(r)
            response = Response(response=reply, status=status, mimetype="application/json")

            response.headers["Content-Type"]="application/json"
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response

        tfaCode=''
        if 'tfacode' in request.args:
            tfaCode = request.args.get('tfacode')

        if tfaCode:
            try: 
                # print("token: " + str(token))
                tokenData = jwt.decode(token, app.config['SECRET_KEY']+tfaCode, algorithms=["HS256"])
                # print(tokenData)
                
                userID =tokenData['userID']

                # print(userID)

            except:
                status = 401
                r = {
                        "error": True,
                        "string": "TFA Token not valid! Please login again.",
                        "answer": -1
                    }

                reply = json.dumps(r)
                response = Response(response=reply, status=status, mimetype="application/json")

                response.headers["Content-Type"]="application/json"
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response

            return f(userID, *args, **kwargs)

        else:
            try: 
                # print("token: " + str(token))
                tokenData = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                # print(tokenData)
                
                userID =tokenData['userID']

                # print(userID)

            except:
                status = 401
                r = {
                        "error": True,
                        "string": "Token not valid! Please login again.",
                        "answer": -1
                    }

                reply = json.dumps(r)
                response = Response(response=reply, status=status, mimetype="application/json")

                response.headers["Content-Type"]="application/json"
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response

            return f(userID, *args, **kwargs)

    return dec

def genToken(userID, tfaFlag, email=''):
    if(tfaFlag):
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        tfaCode = random.randint(100000, 999999)
        print(tfaCode)
        token = jwt.encode({'userID' : userID, 'exp' : expires}, app.config["SECRET_KEY"]+str(tfaCode))

        #send email
        sendtfaEmail(email, tfaCode)
    else:
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        token = jwt.encode({'userID' : userID, 'exp' : expires}, app.config['SECRET_KEY'])
    return token


#retrieve data from database
@app.route('/2fa', methods=['GET'])
@requires_token
def tfaLogin(userID):
    token = genToken(userID, tfaFlag=False)

    status = 200

    r = {
            "error": False,
            "string": "User verified. Long term token generated",
            "answer": token
        }

    reply = json.dumps(r)
    response = Response(response=reply, status=status, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

#retrieve data from database
@app.route('/retrieveDataFromDB', methods=['GET'])
@requires_token
def retrieveData(userID):
    url = dburl+"retrieveDataFromDB"

    res = requests.get(url, params={"userID": userID,"dataType": request.args.get('dataType'),
        "timeType": request.args.get('timeType'), "timeInterval": request.args.get('timeInterval')})  

    response = Response(response=res, status=res.status_code, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

#retrieve data from database
@app.route('/saveMetricData', methods=['GET'])
@requires_token
def saveData(userID):
    url = dburl+"saveMetricData"

    res = requests.get(url, params={"userID": userID,"dataType": request.args.get('dataType'),
        "value": request.args.get('value'), "systolic": request.args.get('systolic'),
        "diastolic": request.args.get('diastolic')})

    response = Response(response=res, status=res.status_code, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

@app.route('/saveUserEmotions', methods=['GET'])
@requires_token
def saveUserEmotionalData(userID):
    url = dburl+"saveUserEmotions"

    res = requests.get(url, params={"userID": userID,"dataType": request.args.get('dataType'),
        "value": request.args.get('value'), "UserEmotions": request.args.get('userEmotions'),
        "diastolic": request.args.get('userThoughts')})

    response = Response(response=res, status=res.status_code, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

#set up mail server to send 2fa code email then shutdown
def sendtfaEmail(emailAddress, tfaCode):
    try:
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.starttls()
        mailServer.login(app.config['EMAIL'], app.config['PASSWORD'])

        msg = "Subject: 2FA Code\n\nYour 2FA code is: " + str(tfaCode)
        mailServer.sendmail(app.config['EMAIL'], emailAddress, msg)
        print("Email sent to: " + emailAddress, " with code: " + str(tfaCode))
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        mailServer.quit() 

    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3307, debug=True)
from flask import Flask
from flask import request
from flask import Response
import json
import pymysql
from passlib.hash import sha256_crypt

dbusername = "admin"
dbpassword = "Group6-password12345!"
dbhost = "group6-db-healthdata.csyjervhsgjs.us-east-1.rds.amazonaws.com"
dbport = "3306"
dbssl_ca='global-bundle.pem'

endPoints ={"saveToDB", "retrieveFromDB", "deleteFromDB"}

#ensures even if backend table name is changed, only need to change here not in frontend
sqlTableDict = {"HeartRate": "HeartRate", "BloodPressure": "BloodPressure", "Cortisol": "Cortisol"}

app = Flask(__name__)
    
#Will return answer to method requested as long as endpoint and method is allowed. Otherwise provides an error response of what went wrong.
#Saves data to and retrieves data from mysql database stored in aws rds
@app.route('/<path:methodCall>', methods=['GET'])
def mySQLRequestHandler(methodCall):
    if request.method == 'GET':

        #saves data to db if endpoint called and text param is provided
        if methodCall == "insertUser":
            email = request.args.get('email')
            password = sha256_crypt.encrypt(request.args.get('password'))
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
            
            insertedID = insertUser(
                email, password, forename, surname, dob,
                gender, address1, city, country, postcode, middle_names, address2, address3
            )
            
            if insertedID == -1:
                status = 500
                r = {
                "error": True,
                "string": "User email already exists",
                "answer": -1
                }

            else:
                status = 200
                r = {
                "error": False,
                "string": "Data saved successfully.",
                "answer": "1"
                }

            reply = json.dumps(r)
            response = Response(response=reply, status=status, mimetype="application/json")

            response.headers["Content-Type"]="application/json"
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response

        #UserID provided needs to be a positive integer and exist in db. Otherwise returns response of what went wrong.
        if methodCall == "saveMetricData" or methodCall == "retrieveDataFromDB":
            if request.args.get('userID'):
                userID = request.args.get('userID')

                if not userID.isdigit(): #ensures userID provided is a positive integer
                    status = 500
                    r = {
                    "error": True,
                    "string": "userID entered is not allowed. Need to provide a positive integer userID to search database.",
                    "answer": -1
                    }
                    response = Response(response=json.dumps(r), status=status, mimetype="application/json")

                    response.headers["Content-Type"]="application/json"
                    response.headers['Access-Control-Allow-Origin'] = "*"
                    return response

            else:
                status = 500
                r = {
                "error": True,
                "string": "UserID not provided.",
                "answer": -1
                }
                response = Response(response=json.dumps(r), status=status, mimetype="application/json")

                response.headers["Content-Type"]="application/json"
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response

        #saves data to db if endpoint called and value param is provided
        if methodCall == "saveMetricData":
            #default response
            status = 500
            r = {
            "error": True,
            "string": "Params empty or incorrect. Data not saved to database.",
            "answer": -1
            }

            if request.args.get('dataType'):
                dataType = request.args.get('dataType')
            else:
                reply = json.dumps(r)
                response = Response(response=reply, status=status, mimetype="application/json")

                response.headers["Content-Type"]="application/json"
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response
            
            if dataType == "HeartRate" or dataType == "Cortisol":
                print("Data type is: "+dataType)
                if request.args.get('value'):
                    print("Value is: "+request.args.get('value'))
                    insertedID = insertSingleMetricData(userID, dataType, request.args.get('value'))

                    status = 200
                    r = {
                    "error": False,
                    "string": "Data saved successfully.",
                    "answer": "1"
                    }

            elif dataType == "BloodPressure":
                print("Data type is: "+dataType)
                if request.args.get('systolic') and request.args.get('diastolic'):
                    insertedID = insertBloodPressureData(userID, dataType, request.args.get('systolic'), request.args.get('diastolic'))

                    status = 200
                    r = {
                    "error": False,
                    "string": "Data saved successfully.",
                    "answer": "1"
                    }                


            reply = json.dumps(r)
            response = Response(response=reply, status=status, mimetype="application/json")

            response.headers["Content-Type"]="application/json"
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response
        

        elif methodCall == "retrieveDataFromDB":
            if request.args.get('dataType') and request.args.get('timeType') and request.args.get('timeInterval'):
                dataType = request.args.get('dataType')
                timeType = request.args.get('timeType')
                timeInterval = request.args.get('timeInterval')
            else:
                status = 500
                r = {
                "error": True,
                "string": "Missing or incorrect params.",
                "answer": -1
                }
                response = Response(response=json.dumps(r), status=status, mimetype="application/json")

                response.headers["Content-Type"]="application/json"
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response
            
            dataRetrieved = retrieveData(userID, dataType, timeType, timeInterval)
            if dataRetrieved: #returns data from database if id exists
                status = 200
                r = {
                "error": False,
                "string": "Data retrieved successfully",
                "answer": str(dataRetrieved)
                }
            else:
                status = 500 #returns error status and message if id does not exist in db
                r = {
                "error": True,
                "string": "No data in database with id = "+str(userID),
                "answer": -1
                }

            reply = json.dumps(r)
            response = Response(response=reply, status=status, mimetype="application/json")

            response.headers["Content-Type"]="application/json"
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response
        
        if methodCall == "insertUserEmotion":
            #default response
            status = 500
            r = {
            "error": True,
            "string": "Params empty or incorrect. Data not saved to database.",
            "answer": -1
            }

            if request.args.get('dataType'):
                dataType = request.args.get('dataType')
            else:
                reply = json.dumps(r)
                response = Response(response=reply, status=status, mimetype="application/json")

                response.headers["Content-Type"]="application/json"
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response
            
            if dataType == "HeartRate" or dataType == "Cortisol":
                print("Data type is: "+dataType)
                if request.args.get('value'):
                    print("Value is: "+request.args.get('value'))
                    insertedID = insertSingleMetricData(userID, dataType, request.args.get('value'))

                    status = 200
                    r = {
                    "error": False,
                    "string": "Data saved successfully.",
                    "answer": "1"
                    }

            elif dataType == "BloodPressure":
                print("Data type is: "+dataType)
                if request.args.get('systolic') and request.args.get('diastolic'):
                    insertedID = insertBloodPressureData(userID, dataType, request.args.get('systolic'), request.args.get('diastolic'))

                    status = 200
                    r = {
                    "error": False,
                    "string": "Data saved successfully.",
                    "answer": "1"
                    }                


            reply = json.dumps(r)
            response = Response(response=reply, status=status, mimetype="application/json")

            response.headers["Content-Type"]="application/json"
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response

        else:
            count=0
            error=True
            text="Route endpoint not found."
            status = 404

            r = {
                "error": error,
                "string": text,
                "answer": count
            }

            reply = json.dumps(r)

            response = Response(response=reply, status=status, mimetype="application/json")

            response.headers["Content-Type"]="application/json"
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response

    else:
        status = 405
        r = {
            "error": True,
            "string": "Method not allowed.",
            "answer": -1
            }

        reply = json.dumps(r)
        response = Response(response=reply, status=status, mimetype="application/json")
        response.headers["Content-Type"]="application/json"
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response


#status 404 page not found error handling
@app.errorhandler(404)
def page_not_found(e):

    r = {
        "error": True,
        "string": "Page not found.",
        "answer": 0
    }

    reply = json.dumps(r)

    response = Response(response=reply, status=404, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

#status 405 method not allowed error handling
@app.errorhandler(405)
def method_not_allowed(e):
    status = 405
    r = {
        "error": True,
        "string": "Method not allowed.",
        "answer": -1
        }

    reply = json.dumps(r)
    response = Response(response=reply, status=status, mimetype="application/json")
    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response
    
#status 500 error handling
@app.errorhandler(500)
def page_error(e):

    r = {
        "error": True,
        "string": "An error has occurred.",
        "answer": 0
    }

    reply = json.dumps(r)

    response = Response(response=reply, status=500, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


#default response if no endpoint entered
@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    count=0
    error=True
    text="Route endpoint not found."
    status = 404

    r = {
        "error": error,
        "string": text,
        "answer": count
    }

    reply = json.dumps(r)

    response = Response(response=reply, status=status, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

#return connection to mysql database
def getConnection():
    con = pymysql.connect(host=dbhost, user=dbusername, password=dbpassword, ssl_ca=dbssl_ca)
    return con


#opens conection to aws database and saves text data provided.
#Returns id of newly saved data. id is unique and auto-incremented in database
def insertUser(
    email, password, forename, surname, dob, gender, address1,
    city, country, postcode, middle_names='', address2='', address3=''
    ):
    con = getConnection()

    #setup cursor to interact with database
    cursor=con.cursor()

    sql="USE HealthData"
    cursor.execute(sql)

    #check if user already exists
    cursor.execute("SELECT * FROM UserInformation WHERE email = %s", (email))
    if cursor.rowcount > 0:
        return -1

    cursor.execute("INSERT INTO UserInformation(email, password, forename, surname, dob, gender, address1,\
        city, country, postcode, middle_names, address2, address3) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (email, password, forename, surname, dob, gender, address1, city,
        country, postcode, middle_names, address2, address3))
    con.commit()
    insertedID = cursor.lastrowid

    cursor.close()
    con.close()
    return insertedID

#opens conection to aws database and saves text data provided.
def insertSingleMetricData(userID, dataType, value):
    con = getConnection()

    #setup cursor to interact with database
    cursor=con.cursor()

    sql="USE HealthData"
    cursor.execute(sql)

    cursor.execute("INSERT INTO "+sqlTableDict[dataType]+"(userID, timestamp, metric) VALUES(%s, now(), %s)", (userID, value))
    con.commit()
    insertedID = cursor.lastrowid

    cursor.close()
    con.close()
    return insertedID

#opens conection to aws database and saves text data provided.
def insertBloodPressureData(userID, dataType, systolic, diastolic):
    con = getConnection()

    #setup cursor to interact with database
    cursor=con.cursor()

    sql="USE HealthData"
    cursor.execute(sql)

    cursor.execute("INSERT INTO "+sqlTableDict[dataType]+"(userID, timestamp, systolic, diastolic) VALUES(%s, now(), %s, %s)",\
        (userID, systolic, diastolic))
    con.commit()
    insertedID = cursor.lastrowid

    cursor.close()
    con.close()
    return insertedID

def insertUserEmotions(userID, dataType, userEmotion , userThoughts):
    con = getConnection()

    #setup cursor to interact with database
    cursor=con.cursor()

    sql="USE HealthData"
    cursor.execute(sql)

    cursor.execute("INSERT INTO "+sqlTableDict[dataType]+"(userID, timestamp, userEmotion, userThoughts) VALUES(%s, now(), %s, %s)",\
        (userID, userEmotion, userThoughts))
    con.commit()
    insertedID = cursor.lastrowid

    cursor.close()
    con.close()
    return insertedID

#opens conection to aws database and retrieves data based on id provided.
def retrieveAllData(userID, dataType):    
    con = getConnection()

    #setup cusror to interact with database
    cursor=con.cursor()

    sql="USE HealthData"
    cursor.execute(sql)

    cursor.execute("SELECT * FROM " + sqlTableDict[dataType] + " WHERE userID =" + userID)
    dataRetrieved = cursor.fetchall()

    cursor.close()
    con.close()
    return dataRetrieved

#opens conection to aws database and retrieves data based on id provided.
def retrieveData(userID, dataType, timeType, timeValue):
    con = getConnection()

    #setup cusror to interact with database
    cursor=con.cursor()

    sql="USE HealthData"
    cursor.execute(sql)

    cursor.execute("SELECT * FROM " + sqlTableDict[dataType] + " WHERE userID =" + userID +
    " AND timestamp >= DATE_SUB(NOW(), INTERVAL " + timeValue + " " + timeType + ")")
    dataRetrieved = cursor.fetchall()

    cursor.close()
    con.close()
    return dataRetrieved



#opens conection to aws database and creates tables if they do not exist.
#TODO requires ssl certificate to connect to database. Uses TLSv1.2.
def createDatabase():
    con = getConnection()

    #setup cursor to interact with database
    cursor=con.cursor()

    #create database if none exists
    sql="CREATE DATABASE IF NOT EXISTS HealthData"
    print(cursor.execute(sql))
    print(cursor.connection.commit)


    sql="USE HealthData"
    print(cursor.execute(sql))

    #show all tables
    sql="SHOW TABLES"
    cursor.execute(sql)
    print(cursor.fetchall())

    # #drop table if exists SuperUser_Access
    # sql="DROP TABLE IF EXISTS Superuser_Access"
    # print("Superuser access",cursor.execute(sql))

    # # drop table if exists HeartRate
    # sql="DROP TABLE IF EXISTS HeartRate"
    # print("Heartrate",cursor.execute(sql))

    # # drop table if exists BloodPressure
    # sql="DROP TABLE IF EXISTS BloodPressure"
    # print("BloodPressure",cursor.execute(sql))

    # # drop table if exists Cortisol
    # sql="DROP TABLE IF EXISTS Cortisol"
    # print("Cortisol",cursor.execute(sql))
    
    # #drop table if exists UserInformation
    #sql="DROP TABLE IF EXISTS UserInput"
    #print(cursor.execute(sql))


    #create user information sql table
    sql = "\
    CREATE TABLE IF NOT EXISTS UserInformation (\
	userID INT NOT NULL AUTO_INCREMENT,\
	email VARCHAR(255) NOT NULL UNIQUE,\
	password VARCHAR(255) NOT NULL,\
	forename VARCHAR(255) NOT NULL,\
	middle_names VARCHAR(255),\
	surname VARCHAR(255) NOT NULL,\
	dob DATE NOT NULL,\
	gender VARCHAR(255) NOT NULL,\
    address1 VARCHAR(120) NOT NULL,\
    address2 VARCHAR(120),\
    address3 VARCHAR(120),\
    city VARCHAR(100) NOT NULL,\
    country CHAR(2) NOT NULL,\
    postcode VARCHAR(10) NOT NULL,\
    Therapist BIT NOT NULL DEFAULT 0,\
    PRIMARY KEY (userID)\
    );\
    "
    print(cursor.execute(sql))


    sql = "\
    CREATE TABLE IF NOT EXISTS Superuser_Access (\
	superuserID INT,\
	patientID INT,\
	role ENUM('therapist', 'gp', 'consultant', 'pt', 'nutritionist'),\
    PRIMARY KEY (superuserID,patientID),\
    CONSTRAINT FK_patientID FOREIGN KEY (patientID) REFERENCES UserInformation(userID),\
    CONSTRAINT FK_superuserID FOREIGN KEY (superuserID) REFERENCES UserInformation(userID)\
    );\
    "
    print(cursor.execute(sql))


    sql = "\
	CREATE TABLE IF NOT EXISTS HeartRate (\
	userID INT NOT NULL,\
	timestamp TIMESTAMP NOT NULL,\
	metric INT NOT NULL,\
    CONSTRAINT FK_heartRate FOREIGN KEY (userID) REFERENCES UserInformation(userID)\
    );\
    "
    print(cursor.execute(sql))

    sql = "\
    CREATE TABLE IF NOT EXISTS Cortisol (\
    userID INT NOT NULL,\
    timestamp TIMESTAMP NOT NULL,\
    metric INT NOT NULL,\
    CONSTRAINT FK_cortisol FOREIGN KEY (userID) REFERENCES UserInformation(userID)\
    );\
    "
    print(cursor.execute(sql))

    sql = "\
    CREATE TABLE IF NOT EXISTS BloodPressure (\
    userID INT NOT NULL,\
    timestamp TIMESTAMP NOT NULL,\
    systolic INT NOT NULL,\
    diastolic INT NOT NULL,\
    CONSTRAINT FK_bloodPressure FOREIGN KEY (userID) REFERENCES UserInformation(userID)\
    );\
    "
    print(cursor.execute(sql))

    sql = "\
    CREATE TABLE IF NOT EXISTS UserInput (\
    userID INT NOT NULL,\
    timestamp TIMESTAMP NOT NULL, \
    userEmotion VARCHAR(255) NOT NULL, \
    userThoughts VARCHAR(255) NOT NULL, \
    CONSTRAINT FK_userInput FOREIGN KEY (userID) REFERENCES UserInformation(userID)\
    );\
    "
    print(cursor.execute(sql))

    cursor.close()
    con.close()

#login endpoint
#returns user id if login is successful
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    userID = -1

    if not auth or not auth.username or not auth.password:
        error=True
        text="Could not verify user. Username or password not provided."
        status = 401

    else:
        email = auth.username

        #check if user exists
        dataRetrieved = checkLogin(email)

        if dataRetrieved == None:
            error=True
            text="Could not verify user. Username or password incorrect."
            status = 401
        
        else:
            if sha256_crypt.verify(auth.password, dataRetrieved[2]):
                error=False
                text="User verified"
                status = 200
                userID = dataRetrieved[0]
                userEmail = dataRetrieved[1]
                userForename = dataRetrieved[3]
                userSurname = dataRetrieved[5]
                userTherapist = dataRetrieved[14]

                if userTherapist == 1:
                    userTherapist = True
                else:
                    userTherapist = False

                print(userID, userEmail, userForename, userSurname, userTherapist)


    
    r = {
        "error": error,
        "string": text,
        #answer is json string of user id and email
        "answer": json.dumps({"userID": userID, "email": userEmail,
                                'userForename': userForename, 'userSurname': userSurname,
                                'userTherapist': userTherapist})
    }

    reply = json.dumps(r)

    response = Response(response=reply, status=status, mimetype="application/json")

    response.headers["Content-Type"]="application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

#check user login details
def checkLogin(email):
    con = getConnection()

    #setup cursor to interact with database
    cursor=con.cursor()

    sql="USE HealthData"
    cursor.execute(sql)

    cursor.execute("SELECT * FROM UserInformation WHERE email = %s", (email))
    dataRetrieved = cursor.fetchone()

    cursor.close()
    con.close()
    return dataRetrieved

if __name__ == '__main__':
    createDatabase()
    app.run(host='0.0.0.0',port=3306, debug=False)

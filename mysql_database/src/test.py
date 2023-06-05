from logging import log
import unittest
from awsdbapp import app
import json
        

class EndpointTest(unittest.TestCase):

    #check if returning correct response as json, with status code 404 when no endpoint provided
    def test_response_noendpointprovided(self):
        #check for 404 response 
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode,404)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"Route endpoint not found.\", \"answer\": 0}")

#check that wrong/unknown endpoint is handled correctly
#check if returning correct response as json, with status code 404 when wrong endpoint
    def test_response_wrongendpoint(self):
        #check for 404 response 
        tester = app.test_client(self)
        response = tester.get("/wrong/endpoint/")
        statuscode = response.status_code
        self.assertEqual(statuscode,404)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"Route endpoint not found.\", \"answer\": 0}")


#####Database saving tests######
    # check that correct end point is returning correct response as json, with status code 200
    def test_response_savingToDB_SingleMetric_Correct(self):
        # check for 200 response 
        tester = app.test_client(self)
        response = tester.get("/saveMetricData?userID=1&dataType=HeartRate&value=100")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
        self.assertEqual(response.content_type,"application/json")
        self.assertTrue(b"{\"error\": false, \"string\": \"Data saved successfully with ID =" in response.data)

    # check that correct end point is returning correct response as json, with status code 200
    def test_response_savingToDB_BloodPressureMetric_Correct(self):
        # check for 200 response 
        tester = app.test_client(self)
        response = tester.get("/saveMetricData?userID=1&dataType=BloodPressure&systolic=10&diastolic=5")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
        self.assertEqual(response.content_type,"application/json")
        self.assertTrue(b"{\"error\": false, \"string\": \"Data saved successfully with ID =" in response.data)

    #check if returning correct response as json, with status code 500 when params wrong
    def test_response_savingToDB_wrongparams(self):
        #check for 500 response 
        tester = app.test_client(self)
        response = tester.get("/saveMetricData?userID=1&dataType=wrong&value=wrong")
        statuscode = response.status_code
        self.assertEqual(statuscode,500)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"Params empty or incorrect. Data not saved to database.\", \"answer\": -1}")

    #check if returning correct response as json, with status code 500 when params not provided
    def test_response_savingToDB_noParams(self):
        #check for 500 response 
        tester = app.test_client(self)
        response = tester.get("/saveMetricData")
        statuscode = response.status_code
        self.assertEqual(statuscode,500)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"UserID not provided.\", \"answer\": -1}")

# # check that correct end point is returning correct response as json, with status code 200
#     def test_response_savingToDB_NewUser_Correct(self):
#         # check for 200 response 
#         tester = app.test_client(self)
#         response = tester.get("/insertUser?email=example@email.com&password=password&forename=Test&surname=User&dob=1990-01-01&gender=male&address1=1 Example Street&city=Example City&country=UK&postcode=BT00 000")
#         statuscode = response.status_code
#         self.assertEqual(statuscode,200)
#         self.assertEqual(response.content_type,"application/json")
#         self.assertTrue(b"{\"error\": false, \"string\": \"Data saved successfully with ID =" in response.data)



#####Database loading tests######
    # check that correct end point is returning correct response as json, with status code 200
    def test_response_retrieveFromDB_Correct(self):
        # check for 200 response 
        tester = app.test_client(self)
        response = tester.get("/retrieveDataFromDB?userID=1&dataType=HeartRate")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
        self.assertEqual(response.content_type,"application/json")
        self.assertTrue(b"{\"error\": false, \"string\":" in response.data)

    #check if returning correct response as json, with status code 500 when text param is empty
    def test_response_retrieveFromDB_noUserID(self):
        #check for 500 response 
        tester = app.test_client(self)
        response = tester.get("/retrieveDataFromDB?userID=&dataType=HeartRate")
        statuscode = response.status_code
        self.assertEqual(statuscode,500)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"UserID not provided.\", \"answer\": -1}")

    #check if returning correct response as json, with status code 500 when non-postive integer provided for id
    def test_response_retrieveFromDB_nonValidIDProvided(self):
        #check for 500 response 
        tester = app.test_client(self)
        response = tester.get("/retrieveDataFromDB?userID=abc&dataType=HeartRate")
        statuscode = response.status_code
        self.assertEqual(statuscode,500)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"userID entered is not allowed. Need to provide a positive integer userID to search database.\", \"answer\": -1}")

        #check if returning correct response as json, with status code 500 when non-postive integer provided for id
    def test_response_retrieveFromDB_negativeIntIDProvided(self):
        #check for 500 response 
        tester = app.test_client(self)
        response = tester.get("/retrieveDataFromDB?userID=-1&dataType=HeartRate")
        statuscode = response.status_code
        self.assertEqual(statuscode,500)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"userID entered is not allowed. Need to provide a positive integer userID to search database.\", \"answer\": -1}")
    

    #testing error handling for not expected methods. (Service only uses get requests for its actions)
    def test_response_POSTRequest(self):
        #check for 200 response 
        tester = app.test_client(self)

        dictToSend = {"testPost": "testPost"}
        #converts dictionary to json
        dictToSend = json.dumps(dictToSend)

        response = tester.post("/retrieveDataFromDB",data = dictToSend)
        
        statuscode = response.status_code
        self.assertEqual(statuscode,405)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"Method not allowed.\", \"answer\": -1}")

    #testing error handling for not expected methods. (Service only uses get requests for its actions)
    def test_response_DELETERequest(self):
        #check for 405 response 
        tester = app.test_client(self)

        response = tester.delete("/retrieveDataFromDB")
        
        statuscode = response.status_code
        self.assertEqual(statuscode,405)
        self.assertEqual(response.content_type,"application/json")
        self.assertEqual(response.data,b"{\"error\": true, \"string\": \"Method not allowed.\", \"answer\": -1}")


if __name__ == '__main__':
    unittest.main()

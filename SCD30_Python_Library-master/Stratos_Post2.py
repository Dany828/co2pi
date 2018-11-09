import requests
import json
import base64
import datetime
import time
from SCD30 import *
from os import system, name

#Gives Pi Time to boot
time.sleep(15)

#UAA Details
UAA_token = ''
app_URL = 'https://stratos-proxy.run.aws-usw02-pr.ice.predix.io/'
app_UAA_URL = 'https://aa15a2d0-bfc0-4ae7-b864-8f196004bdcb.predix-uaa.run.aws-usw02-pr.ice.predix.io/'
asset_Path = 'asset/pace'
timeseries_Path = 'ingest/timeseries'
SLAVE = 247

#Client Details
client_id = 'OG_PACE_INGEST'
client_password = 'Z[;eH+ZR6\,":`*$'


def getUAAToken():
    global UAA_token
    return UAA_token

def obtainNewUAAToken():
    while True:
        try:
            global UAA_token
            #UAA Authorisation
            UAA_authorization = 'Basic ' + base64.b64encode((client_id + ':' + client_password).encode('utf-8')).decode('utf-8')

            #Python Dictionaries for headers and parameters
            UAA_header =  {'Pragma': 'no-cache' ,'content-type': 'application/x-www-form-urlencoded','Cache-Control':'no-cache','authorization': UAA_authorization}
            UAA_params = {'client_id':client_id,'grant_type':'client_credentials'}
            UAA_issuer_id = app_UAA_URL + 'oauth/token'

            #Obtain access token
            r_UAA = requests.get(UAA_issuer_id,headers = UAA_header,params=UAA_params, timeout=5)
            UAA_token = r_UAA.json()['access_token']
            print('Token Obtained from Stratos')
            return

        except:
            print('Waiting for network connection...')
            time.sleep(1)

startTime = 0

def getStartTime_STR():
    global startTime_STR
    return startTime_STR

def setStartTime_STR(time):
    global startTime_STR
    startTime_STR = time
    return

def submitTimeSeriesData():
    stratosPost()
    
def timeSeriesPost(json_data):
    y = 0
    while True:
        try:
            #If running time > 11:58 then this needs changing to read token exp time.
            runningTime = time.time() - getStartTime_STR()
            if(runningTime > 43080): ## 43080 ~= 11:58:00.00. 
                setStartTime_STR(time.time())
                obtainNewUAAToken()
        
            #Get details
            timeseries_uri = app_URL + timeseries_Path
            UAA_header_2 = {'authorization': "Bearer " + getUAAToken(), 'content-type' : 'application/json'}

            #Post request and see if failure
            r = requests.post(timeseries_uri, headers=UAA_header_2, data=json_data, timeout=5)
            return

        except requests.ConnectionError:
            y += 1
            if y < 5:
                print('Stratos Waiting for network connection...')
                time.sleep(1)
            else:
                y = 0
                break #will continue to CP if it can't post the data
            
def stratosPost():

    s = Sensor()
    time.sleep(4)
    s.dataReady()
    s.readMeasurement()
    
    serialNumber = 100 
    sensorTemp = Tempvalueb
##    sensorHumid = humidity = hr.registers[1] / 10.0 
    timeTS = int(time.time()*1000)

    
    print("Formatting and Posting Time Series Data")

    dataStratos = {
        "messageId": str(timeTS),
        "body": [
                {
                "name": '06/11-Temp' ,
                "datapoints": [
                    [
                        timeTS,
                        sensorTemp
                        ]
                    ]
                },

##                {
##                "name": 'BHGE_DS_MC_LEIC_UKAS_HUMIDITY' ,
##                "datapoints": [
##                    [
##                        timeTS,
##                        sensorHumid
##                        ]
##                    ]
##                },
 
            ]
        }

    json_dataStratos = json.dumps(dataStratos)
    #print ("JSON: ", json_data)

    #Post json data to Predix
    timeSeriesPost(json_dataStratos)
    return

i=0    

def main():
    global i
    print("\nObtaining UAA Token")
    setStartTime_STR(time.time()) # New token start time for Stratos.
    obtainNewUAAToken() #12 hour exp. time
    assetTimer = time.time()
    print (assetTimer, time.time())

    while True:        
        print("\n\n************** Loop " + str(i) + " **************\n")
        submitTimeSeriesData()
        runningTime = time.time() - startTime
        print('Successfully Posted')
        time.sleep(6) # 5 second delay
        i += 1

main()




                

import json

import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time
import threading
import requests



global_broker_address =  "127.0.0.1"
global_broker_port = 1884
API_URL = "http://localhost:4000/data"


def on_message(client, userdata, message):

    if message.topic == 'dataService/storePosition':
        print ('Store new position')
        # get the new position coming from the autopilot controller
        positionStr = str(message.payload.decode("utf-8"))
        position = positionStr.split('*')
        # send the position to the API
        requests.post(API_URL, json={'lat': position[0], 'lon': position[1]})

    if message.topic == 'dataService/getStoredPositions':
        print ('get stored positions')
        # get the stored positions from the API
        r = requests.get(API_URL)
        #jsonData = r.json()
        # convert the request to string
        dataString = r.text
        # send answer to subscribed clients (by the moment, only dashboard)
        client.publish("dataServiceAnswer/storedPositions", dataString)


client = mqtt.Client("Data service")
client.on_message = on_message
client.connect(global_broker_address, global_broker_port)
client.loop_start()
print ('Waiting commnads')
# By the moment, the data service only can store positions (sent by the autopilot controller) and provide the stored positions
client.subscribe('dataService/storePosition')
client.subscribe('dataService/getStoredPositions')

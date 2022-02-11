import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import base64
import time
import threading



local_broker_address =  "127.0.0.1"
local_broker_port = 1883
sendingVideoStream = False

def SendVideoStream ():
    global sendingVideoStream
    cap = cv.VideoCapture(0)
    while sendingVideoStream:
        # Read Frame
        _, frame = cap.read()
        # Encoding the Frame
        _, buffer = cv.imencode('.jpg', frame)
        # Converting into encoded bytes
        jpg_as_text = base64.b64encode(buffer)
        # Publishig the Frame on the Topic home/server
        client.publish('cameraControllerAnswer/videoFrame', jpg_as_text)
    cap.release()




def on_message(client, userdata, message):
    global sendingVideoStream
    if message.topic == 'connectPlatform':
        print('Camera controller connected')
        client.subscribe('cameraControllerCommand/+')
    if message.topic == 'cameraControllerCommand/takePicture':
        print('Take picture')
        cap = cv.VideoCapture(0)  # video capture source camera (Here webcam of laptop)
        for n in range(10):
            # this loop is required to discard first frames
            ret, frame = cap.read()
            _, buffer = cv.imencode('.jpg', frame)
            # Converting into encoded bytes
            jpg_as_text = base64.b64encode(buffer)
            client.publish('cameraControllerAnswer/picture', jpg_as_text)

    if message.topic == 'cameraControllerCommand/startVideoStream':
        sendingVideoStream = True
        w = threading.Thread(target=SendVideoStream)
        w.start()

    if message.topic == 'cameraControllerCommand/stopVideoStream':
        sendingVideoStream = False




client = mqtt.Client("Camera controller")
client.on_message = on_message
client.connect(local_broker_address, local_broker_port)
client.loop_start()
print ('Waiting connection from DASH...')
client.subscribe('connectPlatform')

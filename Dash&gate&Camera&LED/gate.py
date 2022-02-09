import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time
import threading


global_broker_address =  "147.83.118.92"
global_broker_port = 1884
local_broker_address =  "147.83.118.92"
local_broker_port = 1883
sendingVideoStream = False

def on_local_message(client, userdata, message):
    if 'Answer' in message.topic:
        global_client.publish(message.topic, message.payload)


def on_global_message(client, userdata, message):
    global sendingVideoStream
    global local_client
    command = str(message.payload.decode("utf-8"))
    print (command)
    if message.topic == 'connectPlatform':
        # subscribe to commands from DASH
        global_client.subscribe('LEDsControllerCommand/+')
        global_client.subscribe('cameraControllerCommand/+')
        global_client.subscribe('autopilotControllerCommand/+')
        # connect to local broker
        local_client.on_message = on_local_message
        local_client.connect(local_broker_address, local_broker_port)
        local_client.loop_start()
        # Inform controllers
        local_client.publish("connectPlatform")
        # Subscribe to answers from controllers
        local_client.subscribe('LEDsControllerAnswer/+')
        local_client.subscribe('cameraControllerAnswer/+')
        local_client.subscribe('autopilotControllerAnswer/+')
        print ('Gate connected')
    if 'Command' in message.topic:
        local_client.publish(message.topic, message.payload)


global_client = mqtt.Client("Gate")
global_client.on_message = on_global_message
global_client.connect(global_broker_address, global_broker_port)

global_client.loop_start() # Inicio del bucle
local_client = mqtt.Client("Gate")
print ('Waiting connection from DASH...')
global_client.subscribe('connectPlatform')
#time.sleep(100) # Paramos el hilo para recibir mensajes.
#global_client.loop_stop() # Fin del bucle
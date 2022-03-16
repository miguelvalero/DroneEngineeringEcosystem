import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time
import threading



local_broker_address =  "127.0.0.1"
local_broker_port = 1883
LEDSequenceOn = False

def LEDSequence ():

    while LEDSequenceOn:
        print ('RED')
        time.sleep(1)
        print('GREEN')
        time.sleep(1)
        print('YELLOW')
        time.sleep(1)


def on_message(client, userdata, message):
    global LEDSequenceOn
    splited = message.topic.split('/')
    origin = splited[0]
    destination = splited[1]
    command = splited[2]

    if command == 'connectPlatform':
        print ('LEDs service connected by ' + origin)
        # aqui en realidad solo debería subscribirse a los comandos que llegan desde el dispositivo
        # que ordenó la conexión, pero esa información no la tiene porque el origen de este mensaje
        # es el gate. NO COSTARIA MUCHO RESOLVER ESTO. HAY QUE VER SI ES NECESARIO
        client.subscribe('+/LEDsService/#')

    if command == 'startLEDsSequence':
        print ('Start LED sequence')
        LEDSequenceOn = True
        w = threading.Thread(target=LEDSequence)
        w.start()

    if command == 'stopLEDsSequence':
        print('Stop LED sequence')
        LEDSequenceOn = False

    if command == 'LEDsSequenceForNSeconds':
        seconds = int (message.payload.decode("utf-8"))
        print ('LED sequence for ' + str(seconds) + 'seconds')
        LEDSequenceOn = True
        w = threading.Thread(target=LEDSequence)
        w.start()
        time.sleep (int (seconds))
        LEDSequenceOn = False


client = mqtt.Client("LEDs service")
client.on_message = on_message
client.connect(local_broker_address, local_broker_port)
client.loop_start()
print ('Waiting connection from DASH...')
client.subscribe('gate/LEDsService/connectPlatform')

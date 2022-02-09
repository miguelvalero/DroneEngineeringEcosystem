import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time
import threading



local_broker_address =  "147.83.118.92"
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

    if message.topic == 'connectPlatform':
        print ('LEDs controller connected')
        client.subscribe('LEDsControllerCommand/+')

    if message.topic == 'LEDsControllerCommand/startLEDsSequence':
        print ('Start LED sequence')
        LEDSequenceOn = True
        w = threading.Thread(target=LEDSequence)
        w.start()

    if message.topic == 'LEDsControllerCommand/stopLEDsSequence':
        print('Stop LED sequence')
        LEDSequenceOn = False

    if message.topic == 'LEDsControllerCommand/LEDsSequenceForNSeconds':
        seconds = int (message.payload.decode("utf-8"))
        print (seconds)
        print ('LED sequence for ' + str(seconds) + 'seconds')
        LEDSequenceOn = True
        w = threading.Thread(target=LEDSequence)
        w.start()
        time.sleep (int (seconds))
        LEDSequenceOn = False


client = mqtt.Client("LED controller")
client.on_message = on_message
client.connect(local_broker_address, local_broker_port)
client.loop_start() # Inicio del bucle
print ('Waiting connection from DASH...')
client.subscribe('connectPlatform')
#time.sleep(100) # Paramos el hilo para recibir mensajes.
#client.loop_stop() # Fin del bucle
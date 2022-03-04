
import paho.mqtt.client as mqtt


global_broker_address =  "127.0.0.1"
global_broker_port = 1884
local_broker_address =  "127.0.0.1"
local_broker_port = 1883
sendingVideoStream = False

def on_local_message(client, userdata, message):
    # just pass the message to the global broker

    global_client.publish(message.topic, message.payload)


def on_global_message(client, userdata, message):
    global sendingVideoStream
    global local_client
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
        local_client.subscribe('dataService/+')
        print ('Gate connected')
    if 'Command' in message.topic:
        # just pass the commend to the local broker
        local_client.publish(message.topic, message.payload)


global_client = mqtt.Client("Gate")
global_client.on_message = on_global_message
global_client.connect(global_broker_address, global_broker_port)


global_client.loop_start()
local_client = mqtt.Client("Gate")
print ('Waiting connection from DASH...')
global_client.subscribe('connectPlatform')


import paho.mqtt.client as mqtt


global_broker_address =  "127.0.0.1"
global_broker_port = 1884
local_broker_address =  "127.0.0.1"
local_broker_port = 1883
sendingVideoStream = False

def on_local_message(client, userdata, message):
    # just pass the message to the global broker
    print('Pass message from local to global: ' + message.topic)
    global_client.publish(message.topic, message.payload)


def on_global_message(client, userdata, message):
    global sendingVideoStream
    global local_client
    splited = message.topic.split('/')
    origin = splited [0]
    destination = splited[1]
    commnad = splited [2]

    if commnad == 'connectPlatform':
        print(origin + ' connects platform')

        # connect to local broker
        local_client.on_message = on_local_message
        local_client.connect(local_broker_address, local_broker_port)
        local_client.loop_start()

        # Inform services
        # ATENCION: quiza los servicios deberían saber quién ha conectado la plataforma
        # (dashBoard o APP). No estoy seguro de que eso sea necesario.
        # OTRA COSA: Si la App o el Dash piden conectar la plataforma cuando ya ha esta conectada
        # entonces esto no hay que hacerlo.
        local_client.publish("gate/LEDsService/connectPlatform")
        local_client.publish("gate/cameraService/connectPlatform")
        local_client.publish("gate/autopilotService/connectPlatform")
        local_client.publish("gate/radiationService/connectPlatform")

        # Subscribe to commands from services to the module (dash or App) that connected the platform
        local_client.subscribe('+/' + origin + '/#')



        # subscribe to commands from origin
        global_client.subscribe(origin+'/LEDsService/#')
        global_client.subscribe(origin+'/cameraService/#')
        global_client.subscribe(origin+'/autopilotService/#')
        global_client.subscribe(origin + '/radiationService/#')

        # subscribe to commands from dataService

        #global_client.subscribe('LEDsControllerCommand/+')
        #global_client.subscribe('cameraControllerCommand/+')
        #global_client.subscribe('autopilotControllerCommand/+')



        #local_client.publish("connectPlatform")
        # Subscribe to answers from controllers
        #local_client.subscribe('LEDsControllerAnswer/+')
        #local_client.subscribe('cameraControllerAnswer/+')
        #local_client.subscribe('autopilotControllerAnswer/+')
        #local_client.subscribe('dataService/+')
        print ('Gate connected')
    else:
        # just pass the command to the local broker
        print ('Pass message from global to local: ' + message.topic)
        local_client.publish(message.topic, message.payload)


global_client = mqtt.Client("Gate")
global_client.on_message = on_global_message
global_client.connect(global_broker_address, global_broker_port)


global_client.loop_start()
local_client = mqtt.Client("Gate")
print ('Waiting connection from DASH...')
global_client.subscribe('+/gate/connectPlatform')
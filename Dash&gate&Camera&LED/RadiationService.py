import random
import paho.mqtt.client as mqtt

def getRadiation():
    rad = round(random.uniform(0, 1), 4)
    return rad

def on_message(client, userdata, message):
    splited = message.topic.split('/')
    origin = splited[0]
    destination = splited[1]
    command = splited[2]

    if command == 'connectPlatform':
        print ('Radiation service connected by ' + origin)
        client.subscribe('+/radiationService/#')

    if command == 'getRadiation':
        rad = getRadiation()
        # The Equivalent Dose is the magnitude used to express the amount of energy deposited per unit mass (absorbed dose)
        # and the type of radiation that supplies said energy.
        # This magnitude is also measured in J/Kg, but is called Sievert ( Sw).
        print('Radiation is: '+str(rad)+' mSv')
        client.publish('radiationService/' + origin + '/Radiation', rad)

local_broker_address =  "127.0.0.1"
local_broker_port = 1883
LEDSequenceOn = False

client = mqtt.Client("Radiation service")
client.on_message = on_message
client.connect(local_broker_address, local_broker_port)
client.loop_start()
print ('Waiting connection from DASH...')
client.subscribe('gate/LEDsService/connectPlatform')

# --------------< General information about radiation >----------------------
# Symptoms in humans due to radiation accumulated during the same day:
#   0 - 0.25 Sv: None
#   0.25 - 1 Sv: Some people experience nausea and loss of appetite,
#                and may experience damage to the bone marrow, lymph nodes, or spleen.
#   1 - 3 Sv: Mild to severe nausea, loss of appetite, more severe bone marrow loss,
#             as well as damage to lymph nodes, spleen, with recovery only probable.
#   3 - 6 Sv: Severe nausea, loss of appetite, bleeding, infection, diarrhea,
#             scaling, sterility, and death if untreated.
#   6 - 10 Sv: Same symptoms, but deterioration of the central nervous system. Likely death.
#   > 10 Sv: Paralysis and death.


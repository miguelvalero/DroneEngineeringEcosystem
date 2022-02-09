
import paho.mqtt.client as mqtt
import base64
import time
import threading

import dronekit
from dronekit import connect


local_broker_address =  "147.83.118.92"
local_broker_port = 1883
LEDSequenceOn = False


def arm():
    """ Arms vehicle and fly to aTargetAltitude. """
    print("Basic pre-arm checks") # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = dronekit.VehicleMode("GUIDED")
    vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

def takeOff(aTargetAltitude):

    vehicle.simple_takeoff(aTargetAltitude)
    while True:
        print(" Altitude: ",vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


def on_message(client, userdata, message):
    global LEDSequenceOn
    global vehicle
    if message.topic == 'connectPlatform':
        print ('Autopilot controller connected')
        client.subscribe('autopilotControllerCommand/+')
        connection_string = "tcp:127.0.0.1:5763"
        vehicle = connect(connection_string, wait_ready=True, baud=115200)

    if message.topic == 'autopilotControllerCommand/armDrone':
        arm ()
    if message.topic == 'autopilotControllerCommand/takeOff':
        altitude = float (message.payload)
        takeOff (altitude)

    if message.topic == 'autopilotControllerCommand/getDroneAltitude':
        client.publish("autopilotControllerAnswer/droneAltitude", vehicle.location.global_relative_frame.alt)

    if message.topic == 'autopilotControllerCommand/getDroneHeading':
        client.publish("autopilotControllerAnswer/droneHeading" ,vehicle.heading)

    if message.topic == 'autopilotControllerCommand/getDroneGroundSpeed':
        client.publish("autopilotControllerAnswer/droneGroundSpeed", vehicle.groundspeed)

    if message.topic == 'autopilotControllerCommand/getDronePosition':
        lat = vehicle.location.global_frame.lat
        lon = vehicle.location.global_frame.lon
        position = str(lat) + '*' + str(lon)
        client.publish("autopilotControllerAnswer/dronePosition", position)

    if message.topic == 'autopilotControllerCommand/goToPosition':
        positionStr = str(message.payload.decode("utf-8"))
        position = positionStr.split ('*')
        lat = float (position[0])
        lon = float (position[1])
        point = dronekit.LocationGlobalRelative (lat,lon, 20)
        vehicle.simple_goto(point)

    if message.topic == 'autopilotControllerCommand/returnToLaunch':
        vehicle.mode = dronekit.VehicleMode("RTL")

    if message.topic == 'autopilotControllerCommand/disarmDrone':
        vehicle.armed = True

client = mqtt.Client("Autopilot controller")
client.on_message = on_message
client.connect(local_broker_address, local_broker_port)
client.loop_start() # Inicio del bucle
print ('Waiting DASH connection ....')
client.subscribe('connectPlatform')
#time.sleep(100) # Paramos el hilo para recibir mensajes.

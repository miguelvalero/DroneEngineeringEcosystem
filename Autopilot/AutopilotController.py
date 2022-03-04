import threading

import paho.mqtt.client as mqtt
import time

import dronekit
from dronekit import connect
import requests


local_broker_address =  "127.0.0.1"
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

def sendPosition():
    global timer
    # get the position and send it to the data service
    lat = vehicle.location.global_frame.lat
    lon = vehicle.location.global_frame.lon
    position = str(lat) + '*' + str(lon)
    print ("send new position")
    client.publish("dataService/storePosition", position)
    # we will repeat this in 5 seconds
    timer= threading.Timer(5.0, sendPosition)
    timer.start()


timer = threading.Timer(5.0, sendPosition)

def on_message(client, userdata, message):
    global LEDSequenceOn
    global vehicle
    global timer
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
        # we start a procedure to get the drone position every 5 seconds
        # and send it to the data service (to be stored there)
        timer = threading.Timer(5.0, sendPosition)
        sendPosition()

    if message.topic == 'autopilotControllerCommand/returnToLaunch':
        # stop the process of getting positions
        timer.cancel()
        vehicle.mode = dronekit.VehicleMode("RTL")

    if message.topic == 'autopilotControllerCommand/disarmDrone':
        vehicle.armed = True

client = mqtt.Client("Autopilot controller")
client.on_message = on_message
client.connect(local_broker_address, local_broker_port)
client.loop_start()
print ('Waiting DASH connection ....')
client.subscribe('connectPlatform')


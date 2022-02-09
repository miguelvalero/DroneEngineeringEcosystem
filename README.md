# Drone Engineering Ecosystem   
![software-arch](https://github.com/miguelvalero/DroneEngineeringEcosystem/blob/main/softwareArchitecture.png)
## Dasboard   
The dashboard is implemented in Python using Tkinter, that is a library to develop graphic user interfaces (GUI).   
More information about Tkinter can be found here:   

## Mobile app   
The mobile app is implemented in Python using Kivy, that is another library to develop GUI, but more suitable for mobile devices.
More information about Kivy can be found here:   

## Brokers   
Both the local and the global brokers use the MQTT protocol based on publication-subscription mechanism. Are implemented using Mosquitto, that automatically generates the broker.   
In the development environment, both the local and the global broker are run in the localhost, the global broker in port 1884 and the local broker in port 1883.  
More information about MQTT can be found here:   
More information about Mosquitto and how to install it in Windows and in Linux can be found here.   



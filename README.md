# Drone Engineering Ecosystem   
![software-arch](https://github.com/miguelvalero/DroneEngineeringEcosystem/blob/main/softwareArchitecture.png)
## Dasboard   
The dashboard is implemented in Python using Tkinter, that is a library to develop graphic user interfaces (GUI).   
A nice course on Tkinter can be found here:   
[Tkinter](https://www.youtube.com/watch?v=YXPyB4XeYLA)   

## Mobile app   
The mobile app is implemented in Python using Kivy, that is another library to develop GUI, but more suitable for mobile devices.
A nice course on Kivy can be found here:   
[Kivy](https://www.youtube.com/watch?v=l8Imtec4ReQ)   
 

## Brokers   
Both the local and the global brokers use the MQTT protocol based on publication-subscription mechanism. Are implemented using Mosquitto, that automatically generates the broker.    
In the development environment, both the local and the global broker are run in the localhost, the global broker in port 1884 and the local broker in port 1883.   
The basics of MQTT can be found here:
[MQTT](https://www.youtube.com/watch?v=EIxdz-2rhLs)   
More information about Mosquitto and how to install it in Windows and in Linux can be found here.   
[Mosquitto](https://www.youtube.com/watch?v=DH-VSAACtBk)      
This is a good example to start using MQTT (using a public broker):    
[Exa,ple](https://www.youtube.com/watch?v=kuyCd53AOtg)   




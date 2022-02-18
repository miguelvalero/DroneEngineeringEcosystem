# Drone Engineering Ecosystem   
![software-arch](https://github.com/miguelvalero/DroneEngineeringEcosystem/blob/main/softwareArchitecture.png)

## Demo   
[Drone Engineering Ecosystem demo](https://www.youtube.com/playlist?list=PL64O0POFYjHpXyP-T063RdKRJXuhqgaXY)    
      
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
[Exanple](https://www.youtube.com/watch?v=kuyCd53AOtg)   


## Suporting materials   
[Transversal project guide](https://github.com/miguelvalero/DroneEngineeringEcosystem/blob/main/TransversalProjectGuide.pdf)    


## Installations required   
### Git and GitHub   
We use Git and GitHub to have the software available to everybody in the cloud, to manage different versions of the software and to organice the integration of the contributions of different participants in the project.   
Create a GitHub account if you do not have one. 
[GitHub](https://github.com/)    
Install git in your computer.
[Git] (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
It is not recommended to install Gui Client because most of the times if you are a developer you may want to work with command lines instead of GUI programs.
Run these commands in a terminal, for some initial configurations:
```
git config --global user.name "Your name"
git config --global user.email youremail@domain.com
```

### Mosquitto     
Download Mosquitto broker:
[Mosquitto (https://mosquitto.org/download/)
It is necessary to create in mosquitto folder 2 new conf. files "mosquitto1883" and "mosquitto1884" with the following information RESPECTIVELY:
listener 1883
allow_anonymous true
listener 1884
allow_anonymous true




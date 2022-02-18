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
[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)      
It is not recommended to install Gui Client because most of the times if you are a developer you may want to work with command lines instead of GUI programs.      
Run these commands in a terminal, for some initial configurations:
```
git config --global user.name "Your name"
git config --global user.email youremail@domain.com
```

### Mosquitto     
Download Mosquitto broker:      
[Mosquitto](https://mosquitto.org/download/)    

In the folder where mosquitto has been downloaded, create two configuration files named "mosquitto1883.conf" and "mosquitto1884.conf". Include the following lines in these files:     
In "mosquitto1883.conf", that will be the local borker:   
```
listener 1883
allow_anonymous true
```
In "mosquitto1884.conf", that will be the global broker:   
```
listener 1884
allow_anonymous true
```
You can start running the local broker with this command (from a terminal opened in the mosquitto folder):
```
 .\mosquitto -c mosquitto1883.conf
```
Do the same to start the global broker, from another terminal.

### Mission Planner     
Download and install the latest Mission Planner installer:      
[Mission Planner](https://ardupilot.org/planner/docs/mission-planner-installation.html)     


### Python
You will need two versions of Python: python2.7 for the autopilot module and python3.7 for the rest
[python3.7](https://www.python.org/downloads/release/python-370/)    
[python2.7](https://www.python.org/downloads/release/python-2718/)    


### PyCharm 
PyCharm is the recommended IDE for development in Python.   
[PyCharm](https://www.jetbrains.com/pycharm/)   

Configure the system interpreter (the versions of python to be used). See this guide:   
[Configure interpreter](https://www.jetbrains.com/help/pycharm/configuring-local-python-interpreters.html)   
You will have to install some packages during development. Look at this guide for this:
Surely, some of the packages that are used in the project are not installed, for this, you must look at the following guide:      
[Installing packages](https://www.youtube.com/watch?v=zCO3KxV2zPI&ab_channel=PhilParisi)     




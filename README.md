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


## Tools required   
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
You will need two versions of Python: python2.7 for the autopilot module and python3.7 for the rest:       
[python3.7](https://www.python.org/downloads/release/python-370/)    
[python2.7](https://www.python.org/downloads/release/python-2718/)    


### PyCharm 
PyCharm is the recommended IDE for development in Python.   
[PyCharm](https://www.jetbrains.com/pycharm/)   

Configure the system interpreter (the versions of python to be used). See this guide:   
[Configure interpreter](https://www.jetbrains.com/help/pycharm/configuring-local-python-interpreters.html)   
      
You will have to install some packages during development. Look at this guide for this:        
[Installing packages](https://www.youtube.com/watch?v=zCO3KxV2zPI&ab_channel=PhilParisi)     

## Drone Engineering Ecosystem installation   
Follow these steps:     
     
Log in in your GitHub account. Then make a fork from the Drone Engineering Ecosystem repository. Now you have a copy of the original repository in your account. We will refer to this repository as "forked".    
     
Clone the forked repository in your computer:   
```
   git clone (URL of forked)
```
      
Now you have created the "local" repository. The system has created a connector between the local repository and the original. The connector is named "origin". See this with this command:
```
   git remote -v
```
      
Now change the the name of the connector:
```
   git remote rename origin forked
```
     
Create a new connector between the local repository and the original:
```
    git remote add origin https://github.com/miguelvalero/DroneEngineeringEcosystem
```
     
Check that now you have two connectors: "forked" connects your local repository with the forked one, and "origin" connects the local with the original:
```
   git remote -v
```

## Procedure for contributions 
El ciclo de contribución que hay que seguir es este:

1. El alumno hace en su GitHub personal un fork del repositorio que contiene la versión de desarrollo en curso.
 
2. Se clona la aplicación en local, desde su GitHub:
```
   git clone (URL del repositorio de la aplicación en desarrollo)
```
3. Se hace la instalación de las dependencias locales (este paso solo habrá que hacerlo en la instalación inicial):
```
   npm install
```
4. El paso 2 habrá creado un remoto que conecta el repositorio  local con el repositorio en el GitHub personal. Ese remoto se llama origin. Cambiaremos el nombre para que se llame mio.
```
  git remote remane origin mio
```
 
 
5. Creamos un remoto llamado origin que conecte el repositorio en local con el repositorio de la versión en desarrollo en curso:
 

```
  git remote add origin (URL del repositorio)
```
 
6. Crea una rama dev en local para hacer allí los desarrollos:
```
  git checkout –b dev
```
 
7. Cuando tenemos listo un conjunto de cambios de la aplicación, hacemos un commit describiendolos brevemente.
```
  git add .
  git commit –m “Descripción de los desarrollos realizados”
```

 
8. Hace un push en el repositorio del GitHub personal, para que se reflejen los cambios allí.
```
  git push mio dev
```
  
En el repositorio del GitHub personal se habrá creado una rama dev con los cambios realizados
 
9. Desde la rama dev del repositorio GitHub personal hacer un pull request para integrar los cambios realizados en la versión en desarrollo en curso. Es importante asegurarse de que los cambios se integran en la rama master de la version en desarrollo. Describir claramente los desarrollos realizados. Al hacer el pull request se indicará si hay conflictos o no. Si no hay conflictos el mismo alumno puede aceptar el pull request (todos tendrán permiso para hacerlo). Si hay conflicto entonces el autor del pull request debe intentar resolver los conflictos y contectar con alguno de los profesores responsables si tiene dificultades para hacerlo.
 
10. Una vez resuelto el pull request, el alumno se trae la versión de desarrollo en curso, en la que se han integrado sus contribuciones con las de otros alumnos.
 ```
  git checkout master
  git pull origin master
```
 
 11. Es posible que al descargar la nueva versión el compilador eche en falta algún paquete que ahora sea necesario como consecuencia de los cambios introducidos por algún otro contribuyente. En ese caso se producirá un fallo de compilación y habrá que hacer de nuevo la instalación de todas las dependencias locales:
 ```
   npm install
 ```

   Ahora es necesario pasar todas las pruebas del módulo para verificar que funciona correctamente. Si hubiese que hacer alguna modificación para resolver errores, se procedería tal y como se ha indicado a partir del paso 6.
 
12. Una vez verificado que la aplicacióno funciona correctamente, hay que enviar el código al repositorio del GitHub personal:
 ```
   git push mio master
 ```
 
13. Borra las ramas dev tanto de la copia local como la del repositorio del GitHub personal
 ```
   git branch -d dev
   git push mio --delete dev
 ```

 
En el momento que quiera hacer una nueva contribución, se repite el proceso desde el paso 6.


import time

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from functools import partial
import base64
import numpy as np
import paho.mqtt.client as mqtt
import cv2
from kivy.graphics.texture import Texture

Builder.load_string("""

## the main container has three blocks in vertical (top, buttons and connect blocks)

<TopWidget>:
# here we will show different elements depending on the button clicked
        size_hint:(1, .8)
        Label:
                id: wellcome
                text: "Wellcome"
    
<ButtonsWidget>:
        size_hint:(1, .1)
        BoxLayout:
                id: buttons
                Button:
                        id: LEDs
                        text: "LEDs"
                        on_press: root.LEDsControl()
                Button:
                        id: Camera
                        text: "Camera"
                        on_release: root.CameraControl()
                Button:
                        id: Autopilot
                        text: "Autopilot"
                        on_release: root.AutopilotControl()

<ConnectWidget>:
        size_hint:(1, .1)
        Button:
                id: connect
                text: "Connect"
                on_press: root.connectWithDronePlatform()

<ContainerBox>:
        orientation: 'vertical'
        id: container
        TopWidget:
                id: top
        ButtonsWidget:
                id: buttons
        ConnectWidget:
                id: connection
    
    
""")


class TopWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(TopWidget, self).__init__(**kwargs)

class ButtonsWidget(BoxLayout):
    videoStreaming = False
    def __init__(self, **kwargs):
        super(ButtonsWidget, self).__init__(**kwargs)

    # these are the functions to be run when the different buttons are clicked

    def startStopSequence (self, a):
        print ('Start')
    def NsecondsSequence (self,a):
        print  ('Nseconds')
        print (self.secondsInput.text)
        self.parent.ids.connection.client.publish("LEDsControllerCommand/LEDsSequenceForNSeconds", self.secondsInput.text)

    def takePicture (self, a):
        print ('take a picture')
        self.parent.ids.connection.client.publish("cameraControllerCommand/takePicture")

    def videoStream (self, a):
        if not self.videoStreaming:
            print ('Start video stream')
            self.parent.ids.connection.client.publish("cameraControllerCommand/startVideoStream")
            self.videoStreaming = True
            self.videoStreamButton.text = "Stop video stream"
        else :
            print('Stop video stream')
            self.parent.ids.connection.client.publish("cameraControllerCommand/stopVideoStream")
            self.videoStreaming = False
            self.videoStreamButton.text = "Start video stream"

    def armDisarm(self, a):
        print ('Arm disarm')
        self.parent.ids.connection.client.publish("autopilotControllerCommand/armDrone")

    def getAltitude(self, a):
            print('get Altitude')
            self.parent.ids.connection.client.publish("autopilotControllerCommand/getDroneAltitude")
    def getHeading(self, a):
            print('get heading')
            self.parent.ids.connection.client.publish("autopilotControllerCommand/getDroneHeading")

    def takeOff(self, a):
        print('take off')
        print (self.metersInput.text)
        self.parent.ids.connection.client.publish("autopilotControllerCommand/takeOff", self.metersInput.text)

    def getPosition(self, a):
        print('get position')
        self.parent.ids.connection.client.publish("autopilotControllerCommand/getDronePosition")

    def goTo(self, a):
            print('set position')
            position = self.latInput.text + '*' + self.lonInput.text
            self.parent.ids.connection.client.publish("autopilotControllerCommand/goToPosition", position)

    def returnToLaunch(self, a):
            print('return to launch')
            self.parent.ids.connection.client.publish("autopilotControllerCommand/returnToLaunch")

    def LEDsControl(self):
        # we create in the top block the widget required when LEDs control button is clicled
        # first remove all widgets in the top block
        self.parent.ids.top.clear_widgets()

        self.LEDsLayout = BoxLayout(spacing=10, orientation = "vertical")
        self.sequenceButton = Button(text='Start LED sequence')
        self.sequenceButton.bind(on_press=self.startStopSequence)
        self.LEDsLayout.add_widget(self.sequenceButton)

        self.NSecondsLayout = GridLayout(cols=2)

        self.NSecondsSequenceButton = Button(text='LED sequence for N seconds', size_hint=(.8, 1))
        self.NSecondsSequenceButton.bind(on_press=self.NsecondsSequence)
        self.secondsInput = TextInput(multiline=False, size_hint=(.2, 1))
        self.secondsInput.font_size = 100

        self.NSecondsLayout.add_widget( self.NSecondsSequenceButton)
        self.NSecondsLayout.add_widget(self.secondsInput)

        self.LEDsLayout.add_widget(self.NSecondsLayout)
        self.parent.ids.top.add_widget (self.LEDsLayout)

    def CameraControl(self):
        # we create in the top block the widget required when Camera control button is clicled
        # first remove all widgets in the top block
        self.parent.ids.top.clear_widgets()
        self.parent.ids.top.clear_widgets()


        self.cameraLayout = GridLayout(cols=2)
        self.takePictureButton = Button(text='Take a picture',  size_hint=(.5, .1))
        self.takePictureButton.bind(on_press=self.takePicture)
        self.cameraLayout.add_widget (self.takePictureButton);

        self.videoStreamButton = Button(text='Start video stream', size_hint=(.5, .1))
        self.videoStreamButton.bind(on_press=self.videoStream)
        self.cameraLayout.add_widget(self.videoStreamButton);

        self.pictureImage = Image(source='image.jpg')
        self.cameraLayout.add_widget(self.pictureImage)

        self.videoFrameImage = Image(source='image.jpg')
        self.cameraLayout.add_widget(self.videoFrameImage)

        self.parent.ids.top.add_widget(self.cameraLayout )

    def AutopilotControl(self):
        # we create in the top block the widget required when Autopilot control button is clicled
        # first remove all widgets in the top block
        self.parent.ids.top.clear_widgets()
        self.parent.ids.top.clear_widgets()
        self.autopilotLayout = BoxLayout( orientation="vertical")

        self.armDisarmButton = Button(text='Arm drone')
        self.armDisarmButton.bind(on_press=self.armDisarm)

        self.getsLayout = BoxLayout(orientation="horizontal")
        self.getAltitudeButton = Button(text='Get altitude', size_hint=(.25, 1))
        self.getAltitudeButton.bind(on_press=self.getAltitude)
        self.altitudeLabel = Label(text=' ', font_size='20sp', size_hint=(.25, 1))
        self.getHeadingButton = Button(text='Get heading', size_hint=(.25, 1))
        self.getHeadingButton.bind(on_press=self.getHeading)
        self.headingLabel = Label(text=' ', font_size='20sp', size_hint=(.25, 1))
        self.getsLayout.add_widget(self.getAltitudeButton)
        self.getsLayout.add_widget(self.altitudeLabel)
        self.getsLayout.add_widget(self.getHeadingButton)
        self.getsLayout.add_widget(self.headingLabel)


        self.takeOffLayout = BoxLayout(orientation="horizontal")
        self.takeOffButton = Button(text='Take off', size_hint=(.3, 1))
        self.takeOffButton.bind(on_press=self.takeOff)
        self.metersInput = TextInput(multiline=False, size_hint=(.3, 1))
        self.metersLabel = Label(text='meters', font_size='20sp', size_hint=(.3, 1))
        self.takeOffLayout.add_widget(self.takeOffButton)
        self.takeOffLayout.add_widget(self.metersInput)
        self.takeOffLayout.add_widget(self.metersLabel)


        self.positionLayout = GridLayout(cols=3)
        self.getPositionButton = Button(text='Get positon', size_hint=(.25, 1))
        self.getPositionButton.bind(on_press=self.getPosition)

        self.latLabel = Label(text=' ', font_size='20sp', size_hint=(.375, 1))

        self.getPositionButton.background_color= .0, .8, 0, 1
        self.lonLabel = Label(text=' ', font_size='20sp', size_hint=(.375, 1))
        self.goToButton = Button(text='Go To', size_hint=(.25, 1))
        self.goToButton.bind(on_press=self.goTo)
        self.latInput = TextInput(multiline=False, size_hint=(.375, 1))
        self.lonInput = TextInput(multiline=False, size_hint=(.375, 1))
        self.positionLayout.add_widget(self.getPositionButton)
        self.positionLayout.add_widget(self.latLabel)
        self.positionLayout.add_widget(self.lonLabel)
        self.positionLayout.add_widget(self.goToButton)
        self.positionLayout.add_widget(self.latInput)
        self.positionLayout.add_widget(self.lonInput)

        self.returnToLaunchButton = Button(text='Return to Launch')
        self.returnToLaunchButton.bind(on_press=self.returnToLaunch)

        self.autopilotLayout.add_widget(self.armDisarmButton)
        self.autopilotLayout.add_widget(self.getsLayout)
        self.autopilotLayout.add_widget (self.takeOffLayout)
        self.autopilotLayout.add_widget(self.positionLayout)
        self.autopilotLayout.add_widget(self.returnToLaunchButton)

        self.parent.ids.top.add_widget(self.autopilotLayout)

class ConnectWidget(BoxLayout):
    # the only element in the connect block is a button already defined in the builder load string
    connected = False

    def __init__(self, **kwargs):
        super(ConnectWidget, self).__init__(**kwargs)
        self.client = mqtt.Client('Dashboard')
        self.global_broker_address = "127.0.0.1"
        self.global_broker_port = 1884

    # to be done when the button is clicked
    def connectWithDronePlatform(self):
        if not self.connected:
                self.client.connect(self.global_broker_address)
                self.client.publish("connectPlatform")
                self.client.loop_start()
                self.client.on_message = self.on_message
                self.client.subscribe("#")
                print('Connected with drone platform')
                self.ids.connect.background_color = .0, 1, 0, 1
                self.ids.connect.text = "Disconnect"
                # change colors os buttons when connected

                self.parent.ids.buttons.ids.LEDs.background_color = .8, 0, 0, 1
                self.parent.ids.buttons.ids.Autopilot.background_color = .0, .8, 0, 1
                self.parent.ids.buttons.ids.Camera.background_color = .0, .0, .8, 1
                self.connected = True
        else:
                print('Disconnect')
                self.ids.connect.background_color = .5, .5, .5, 1
                self.ids.connect.text = "Disconnect"


                self.parent.ids.buttons.ids.LEDs.background_color = .5, .5, .5, 1
                self.parent.ids.buttons.ids.Autopilot.background_color = .5, .5, .5, 1
                self.parent.ids.buttons.ids.Camera.background_color = .5, .5, .5, 1
                self.connected = False



    def on_message(self, client, userdata, msg):
        if msg.topic == 'cameraControllerAnswer/picture':
            Clock.schedule_once(partial(self.showPicture, client, userdata, msg))
        if msg.topic == "cameraControllerAnswer/videoFrame":
            Clock.schedule_once(partial(self.showVideoFrame, client, userdata, msg))
        if (msg.topic == "autopilotControllerAnswer/droneAltitude"):
            answer = str(msg.payload.decode("utf-8"))
            self.parent.ids.buttons.altitudeLabel.text = answer[:5]
        if (msg.topic == "autopilotControllerAnswer/droneHeading"):
            answer = str(msg.payload.decode("utf-8"))
            self.parent.ids.buttons.headingLabel.text = answer[:5]

        if (msg.topic == "autopilotControllerAnswer/dronePosition"):
            positionStr = str(msg.payload.decode("utf-8"))
            position = positionStr.split('*')
            self.parent.ids.buttons.latLabel.text = position[0]
            self.parent.ids.buttons.lonLabel.text = position[1]

    def showPicture(self, client, userdata, msg, dt):

        # ATTENTION: this works well in the computer but not in the android phone
        img = base64.b64decode(msg.payload)
        npimg = np.frombuffer(img, dtype=np.uint8)
        if npimg.size != 0:
            # converting into numpy array from buffer
            self.frame = cv2.imdecode(npimg, 1)
            buffer = cv2.flip(self.frame, 0).tobytes()
            shape1 = self.frame.shape[1]
            shape0 = self.frame.shape[0]

            tex = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            tex.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.parent.ids.buttons.pictureImage.texture = tex

    def showVideoFrame(self, client, userdata, msg, dt):
        # ATTENTION: this works well in the computer but not in the android phone

        img = base64.b64decode(msg.payload)
        npimg = np.frombuffer(img, dtype=np.uint8)
        if npimg.size != 0:
            # converting into numpy array from buffer

            self.frame = cv2.imdecode(npimg, 1)
            buffer = cv2.flip(self.frame, 0).tobytes()
            tex = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            tex.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

            self.parent.ids.buttons.videoFrameImage.texture = tex


class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)


class TestApp(App):
    def build(self):
        return ContainerBox()


if __name__ == '__main__':
    TestApp().run()
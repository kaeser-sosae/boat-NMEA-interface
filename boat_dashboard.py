from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout 
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.logger import Logger

import websocket

# standard libraries (python 2.7)
import _thread
import time

import json

from kivy.config import Config
from kivy.core.window import Window

import os
import ctypes



kv = '''
<WindDirNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix

<WS>:
    cols: 1

    canvas.before:
        Color:
            rgba: 0, 0, 0, 1.0
        Rectangle:
            pos: self.pos
            size: self.size

    water_temp: water_temp
    water_speed: water_speed
    land_speed: land_speed
    wind_speed: wind_speed
    wind_direction: wind_direction
    wind_needle: wind_needle

    RelativeLayout:
        cols: 1
        canvas.before:
            Color:
                rgba: 255,255,255,1
            Rectangle:
                size: self.size
                pos: 0,0
        canvas:
            Color:
                rgba: 0,0,0,1
            Rectangle:
                size: self.width-20,self.height-20
                pos: 10,10
        Label:
            font_size: 30
            id: water_temp_label
            text: "Water Temperature"
            #size_hint_y: 0.1
            size: self.width, 100
            pos: 0,250
        Label:
            font_size: 75
            id: water_temp
            text: "0"
    RelativeLayout:
        cols: 1
        canvas.before:
            Color:
                rgba: 255,255,255,1
            Rectangle:
                size: self.size
                pos: 0,0
        canvas:
            Color:
                rgba: 0,0,0,1
            Rectangle:
                size: self.width-20,self.height-10
                pos: 10,10
        Label:
            font_size: 30
            id: water_speed_label
            text: "Water Speed"
            size_hint_y: 0.2
            pos: 0,500
        Label:
            font_size: 75
            id: water_speed
            text: "0"

    RelativeLayout:
        cols: 1
        canvas.before:
            Color:
                rgba: 255,255,255,1
            Rectangle:
                size: self.size
                pos: 0,0
        canvas:
            Color:
                rgba: 0,0,0,1
            Rectangle:
                size: self.width-20,self.height-10
                pos: 10,10
        Label:
            font_size: 30
            id: land_speed_label
            text: "Land Speed"
            size_hint_y: 0.2
            pos: 0,500
        Label:
            font_size: 75
            id: land_speed
            text: "0 kt"
    RelativeLayout:
        cols: 1
        canvas.before:
            Color:
                rgba: 0,0,0,1
            Rectangle:
                size: self.size
                pos: 0,0
        RelativeLayout:
            Image:
                source: 'wind_background.png'
                #size: 400,400
            Label:
                bold: True
                font_size: 20
                color: 0,0,0,1
                id: wind_speed
                text: "0 kt"
                size_hint_y: 0.2
                pos: 0,35 
            Label:
                bold: True
                font_size: 20
                color: 0,0,0,1
                id: wind_direction
                text: "000 S"
                size_hint_y: 0.2
                pos: 0,60                               
        RelativeLayout:        
            WindDirNeedle:
                id: wind_needle
                source: 'wind_needle.png'
                pos: 0,-6
 


'''

Builder.load_string(kv)

degree_sign = u'\N{DEGREE SIGN}'

screenwidth = 0
screenheight = 0

if os.name == 'nt':
    user32 = ctypes.windll.user32
    screenwidth = user32.GetSystemMetrics(0)
    screenheight = user32.GetSystemMetrics(1)
else:
    screenheight=1080
    screenwidth=1920

Config.set('graphics', 'resizable', True)

class KivyWebSocket(websocket.WebSocketApp):

    def __init__(self, *args, **kwargs):
        super(KivyWebSocket, self).__init__(*args, **kwargs)
        self.logger = Logger
        self.logger.info('WebSocket: logger initialized')

class WS(GridLayout):
    water_temp = ObjectProperty()
    water_speed = ObjectProperty()
    land_speed = ObjectProperty()
    wind_speed = ObjectProperty()
    wind_direction = ObjectProperty()

    pressed = False

    def __init__(self, **kwargs):
        super(WS, self).__init__(**kwargs)
        Logger.info('Layout: initialized')

class WebSocketTest(App):
    ws = None
    url = "ws://172.30.3.149:3000/signalk/v1/stream?subscribe=all"
    layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WebSocketTest, self).__init__(**kwargs)
        socket_server="ws://172.30.3.149:3000/signalk/v1/stream?subscribe=all"
        ws = KivyWebSocket(socket_server,
                           on_message=self.on_ws_message,
                           on_error=self.on_ws_error,
                           on_open=self.on_ws_open,
                           on_close=self.on_ws_close,)
        self.ws = ws
        self.logger = Logger
        self.logger.info('App: initiallzed')
        app = App.get_running_app()
        Clock.schedule_once(app.ws_connection)

    def build(self):
        Window.borderless = False
        Window.size = 350, screenheight-40
        Window.top = 0
        Window.left = screenwidth - 350
        return self.layout

    def on_ws_message(self, ws, message):

        json_message = json.loads(message)

        for update in json_message["updates"]:
            for value in update["values"]:
                if (value["path"] == "environment.water.temperature"):
                    print("Got water temp: " + str(value["value"]))
                    self.layout.water_temp.text = str(float("{:.2f}".format(float(value["value"]) - 273.15))) + " " + degree_sign + "C"
                if (value["path"] == "navigation.speedThroughWater"):
                    print("Got water speed: " + str(value["value"]))
                    self.layout.water_speed.text = str(value["value"]) + " kt"
                if (value["path"] == "navigation.speedOverGround"):
                    print("Got land speed: " + str(value["value"]))
                    self.layout.land_speed.text = str(value["value"]) + " kt"
                if (value["path"] == "navigation.attitude"):
                    print("Got yaw: " + str(value["value"]["yaw"]))
                    print("Got pitch: " + str(value["value"]["pitch"]))
                    print("Got roll: " + str(value["value"]["roll"]))
                    #self.layout.land_speed.text = str(value["value"]) + " kt"
                if (value["path"] == "environment.wind.speedApparent"):
                    print("Got apparent wind speed: " + str(value["value"]))
                    self.layout.wind_speed.text = str(float("{:.1f}".format(float(value["value"])))) + " kt"
                if (value["path"] == "environment.wind.angleApparent"):
                    print("Got apparent wind angle: " + str(value["value"]))
                    wind_angle_raw = value["value"]
                    wind_angle_degrees = wind_angle_raw * 57.29
                    wind_angle_translated = ""
                    if wind_angle_degrees > 0:
                        wind_angle_translated = str(int(float("{:.0f}".format(wind_angle_degrees)))) + " S"
                    if wind_angle_degrees < 0:
                        wind_angle_translated = str(int(float("{:.0f}".format(wind_angle_degrees)) * -1)) + " P"
                    print(" - Converted to degrees: " + str(wind_angle_degrees))
                    print(" - Converted to human: " + wind_angle_translated)
                    self.layout.wind_direction.text = wind_angle_translated
                    self.layout.wind_needle.angle = int(wind_angle_degrees) * -1








    def on_ws_error(self, ws, error):
        self.logger.info('WebSocket: [ERROR]  {}'.format(error))

    def ws_connection(self, dt, **kwargs):
        # start a new thread connected to the web socket
        _thread.start_new_thread(self.ws.run_forever, ())

    def on_ws_open(self, ws):
        def run(*args):
            #for i in range(1, 13):
            time.sleep(1)
            #    ws.send('Hello %d' % i)
            #time.sleep(10)
            #ws.close()
        _thread.start_new_thread(run, ())

    def on_ws_close(self, ws):
        self.layout.water_temp.text = "N/A"
        self.layout.water_speed.text = "N/A"
        self.layout.land_speed.text = "N/A"
        time.sleep(10)
        ws_connection()
        #self.layout.the_btn.text = '### closed ###'


if __name__ == "__main__":
    WebSocketTest().run()
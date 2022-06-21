from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout 
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.core.text import LabelBase
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import *


import websocket

# standard libraries (python 2.7)
import _thread
import time

import json



import os
import ctypes

LabelBase.register(name='CFLCD', fn_regular='CFLCD-Regular.ttf')
LabelBase.register(name='SFProSB', fn_regular='SF-Pro-Display-Semibold.otf')

degree_sign = u'\N{DEGREE SIGN}'

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

<DirNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix 

<DirDial@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix 

<YachtSide@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: 25
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix 

<YachtFront@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix

<Needle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix 

<SpeedNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            #angle: root.angle
            angle: 290
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix 

<SOGNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            #angle: root.angle
            angle: 270
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix 

<RPMsNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            #angle: root.angle
            angle: 180
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix                         



<WS>:
    cols: 1

    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'background.png'

    heel_yacht: heel_yacht
    heel_value: heel_value
    tilt_yacht: tilt_yacht
    tilt_value: tilt_value
    water_depth: water_depth
    water_temp: water_temp
    coolant_temp_needle: coolant_temp_needle

    # wind_needle: wind_needle
    # wind_speed: wind_speed
    sog_needle: sog_needle
    speed_needle: speed_needle
    rpms_needle: rpms_needle

    engine_battery: engine_battery
    house_battery: house_battery
    dir_dial: dir_dial
    dir_heading: dir_heading
    fuel_tank_needle: fuel_tank_needle
    engine_hours: engine_hours


    





    FloatLayout:

        # Yacht Heel Guage
        Image:
            source: 'tilt_heel_sky_v2.png'
            allow_stretch: True
            size_hint: 0.1,0.1
            pos: 546,884           
        YachtSide:
            id: heel_yacht
            source: 'yacht_side.png'
            allow_stretch: True
            size_hint: 0.18,0.18 
            pos: 472,793 
        Label:
            id: heel_value
            text: "20"
            size_hint: 0.2,0.2
            pos: 133, 730
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 50

        # Yacht Tilt Guage
        Image:
            source: 'tilt_heel_sky_v2.png'
            allow_stretch: True
            size_hint: 0.1,0.1
            pos: 226,884
        YachtFront:
            id: tilt_yacht
            source: 'yacht_front.png'
            allow_stretch: True
            size_hint: 0.18,0.18
            pos: 150,793
        Label:
            id: tilt_value
            text: "61"
            size_hint: 0.2,0.2
            pos: 451, 730
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 50 

        # Water Depth Guage
        Label:
            id: water_depth
            text: "35.6"
            size_hint: 0.2,0.2
            pos: 770,790
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60

        # Water Temp Guage
        Label:
            id: water_temp
            text: "21.5"
            size_hint: 0.2,0.2
            pos: 1090, 790
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60

        # Coolant Temp Needle
        Needle:
            id: coolant_temp_needle
            source: 'small_dial_needle.png'
            allow_stretch: True
            size_hint: 0.1, 0.1
            pos: 1505,836

        # SOG Needle
        SOGNeedle:
            id: sog_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 533,415

        # Speed Needle
        SpeedNeedle:
            id: speed_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 1003,415

        # RPMs Needle
        RPMsNeedle:
            id: rpms_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 1472,415 

        # Engine Battery
        Label:
            id: engine_battery
            text: "12.8"
            size_hint: 0.2,0.2
            pos: 130, 60
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60 

        # House Battery
        Label:
            id: house_battery
            text: "13.2"
            size_hint: 0.2,0.2
            pos: 450, 60
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60                                                
            
        # Compass
        Image:
            source: 'direction_and_depth_guage_color_wheel.png'
            allow_stretch: True
            size_hint: 0.21,0.21
            pos: 761,44
        Needle:
            id: dir_dial
            source: 'direction_and_depth_guage_dial.png'
            allow_stretch: True
            size_hint: 0.21, 0.21
            pos: 761,44
        Label:
            id: dir_heading
            text: "21"
            size_hint: 0.2,0.2
            pos: 770,50
            font_name: "SFProSB"
            color: "black"
            font_size: 60 

        # Fuel Tank Needle
        Needle:
            id: fuel_tank_needle
            source: 'small_dial_needle.png'
            allow_stretch: True
            size_hint: 0.1, 0.1
            pos: 1183, 104

        # Engine Hours
        Label:
            id: engine_hours
            text: "347"
            size_hint: 0.2,0.2
            pos: 1410, 60
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60                    


'''

Builder.load_string(kv)

screenwidth = 0
screenheight = 0

if os.name == 'nt':
    user32 = ctypes.windll.user32
    screenwidth = user32.GetSystemMetrics(0)
    screenheight = user32.GetSystemMetrics(1)
else:
    screenheight=1080
    screenwidth=1920

Config.set('graphics', 'resizable', False)

class KivyWebSocket(websocket.WebSocketApp):

    def __init__(self, *args, **kwargs):
        super(KivyWebSocket, self).__init__(*args, **kwargs)
        self.logger = Logger
        self.logger.info('WebSocket: logger initialized')

class WS(GridLayout):
    water_temp = ObjectProperty()
    water_speed = ObjectProperty()
    water_depth = ObjectProperty()
    #land_speed = ObjectProperty()
    wind_speed = ObjectProperty()
    wind_direction = ObjectProperty()
    engine_hours = ObjectProperty()
    engine_battery = ObjectProperty()
    house_battery = ObjectProperty()
    water_tank_needle = ObjectProperty()
    fuel_tank_needle = ObjectProperty()
    coolant_temp_needle = ObjectProperty()

    pressed = False

    def __init__(self, **kwargs):
        super(WS, self).__init__(**kwargs)
        Logger.info('Layout: initialized')

class SignalKInterface(App):
    ws = None
    url = "ws://172.30.3.149:3000/signalk/v1/stream?subscribe=all"
    layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SignalKInterface, self).__init__(**kwargs)
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
        #Window.size = 155, 520 # This is temp for viewing on a Mac
        Window.size = screenwidth, screenheight-40 # This is real setting for 1080p
        Window.top = 0
        Window.left = 0
        self.layout = WS()
        return self.layout

    def on_ws_message(self, ws, message):

        json_message = json.loads(message)

        for update in json_message["updates"]:
            print(Window.size)
            for value in update["values"]:
                if (value["path"] == "environment.water.temperature"):
                    print("Got water temp: " + str(value["value"]))
                    self.layout.water_temp.text = str(float("{:.1f}".format(float(value["value"]) - 273.15))) #+ " " + degree_sign + "C"
                if (value["path"] == "navigation.speedThroughWater"):
                    print("Got water speed: " + str(value["value"]))
                    self.layout.water_speed.text = str(value["value"]) + " kt"
                    self.layout.gps_speed.text = str(float("{:.1f}".format(float(value["value"])))) + " kt"
                if (value["path"] == "navigation.speedOverGround"):
                    print("Got land speed: " + str(value["value"]))
                    self.layout.land_speed.text = str(value["value"]) + " kt"
                if (value["path"] == "navigation.attitude"):
                    #print("Got yaw: " + str(value["value"]["yaw"]))
                    
                    print("Got roll: " + str(value["value"]["roll"]))

                    heel_angle_raw = value["value"]["roll"]
                    heel_angle_degrees = heel_angle_raw * 57.29
                    heel_angle_translated = ""
                    heel_angle_translated_clean = ""
                    if heel_angle_degrees > 0:
                        heel_angle_translated = str(int(float("{:.0f}".format(heel_angle_degrees)))) + degree_sign + " S"
                        heel_angle_translated_clean = str(int(float("{:.0f}".format(heel_angle_degrees))))
                    if heel_angle_degrees < 0:
                        heel_angle_translated = str(int(float("{:.0f}".format(heel_angle_degrees)) * -1)) + degree_sign + " P"
                        heel_angle_translated_clean = str(int(float("{:.0f}".format(heel_angle_degrees)) * -1))
                    print(" - Converted to degrees: " + str(heel_angle_degrees))
                    print(" - Converted to human: " + heel_angle_translated)
                    self.layout.heel_yacht.angle = int(heel_angle_degrees) * -1
                    self.layout.heel_actual.text = heel_angle_translated

                    print("Got pitch: " + str(value["value"]["pitch"]))

                    tilt_angle_raw = value["value"]["pitch"]
                    tilt_angle_degrees = tilt_angle_raw * 57.29
                    tilt_angle_translated = "0"
                    tilt_angle_translated_clean = ""
                    if tilt_angle_degrees > 0:
                        tilt_angle_translated = str(int(float("{:.0f}".format(tilt_angle_degrees)))) + degree_sign + " S"
                        tilt_angle_translated_clean = str(int(float("{:.0f}".format(tilt_angle_degrees))))
                    if tilt_angle_degrees < 0:
                        tilt_angle_translated = str(int(float("{:.0f}".format(tilt_angle_degrees)) * -1)) + degree_sign + " B"
                        tilt_angle_translated_clean = str(int(float("{:.0f}".format(tilt_angle_degrees)) * -1))
                    print(" - Converted to degrees: " + str(tilt_angle_degrees))
                    print(" - Converted to human: " + tilt_angle_translated)
                    self.layout.tilt_yacht.angle = int(tilt_angle_degrees)
                    self.layout.tilt_actual.text = tilt_angle_translated

                if (value["path"] == "environment.wind.speedApparent"):
                    print("Got apparent wind speed: " + str(value["value"]))
                    self.layout.wind_speed.text = str(float("{:.1f}".format(float(value["value"])))) + ""
                if (value["path"] == "environment.wind.angleApparent"):
                    print("Got apparent wind angle: " + str(value["value"]))
                    wind_angle_raw = value["value"]
                    wind_angle_degrees = wind_angle_raw * 57.29
                    wind_angle_translated = ""
                    wind_angle_translated_clean = ""
                    if wind_angle_degrees > 0:
                        wind_angle_translated = str(int(float("{:.0f}".format(wind_angle_degrees)))) + " S"
                        wind_angle_translated_clean = str(int(float("{:.0f}".format(wind_angle_degrees))))
                    if wind_angle_degrees < 0:
                        wind_angle_translated = str(int(float("{:.0f}".format(wind_angle_degrees)) * -1)) + " P"
                        wind_angle_translated_clean = str(int(float("{:.0f}".format(wind_angle_degrees)) * -1))
                    print(" - Converted to degrees: " + str(wind_angle_degrees))
                    print(" - Converted to human: " + wind_angle_translated)
                    #self.layout.wind_direction.text = wind_angle_translated
                    self.layout.wind_needle.angle = int(wind_angle_degrees) * -1

                    ## Code to move the direction dial - change this later
                    self.layout.dir_dial.angle = int(wind_angle_degrees) * -1
                    self.layout.dir_heading.text = wind_angle_translated_clean + " " + degree_sign + " M"









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
    SignalKInterface().run()
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout 
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.core.text import LabelBase
from kivy.config import Config
from kivy.core.window import Window


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
            angle: root.angle
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
            angle: 44
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
            angle: 44
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
            angle: 43
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

    water_temp: water_temp
    water_depth: water_depth
    # wind_speed: wind_speed
    # wind_needle: wind_needle
    # dir_dial: dir_dial
    # dir_heading: dir_heading
    # gps_speed: gps_speed
    heel_yacht: heel_yacht
    tilt_yacht: tilt_yacht
    # heel_actual: heel_actual
    # tilt_actual: tilt_actual
    engine_hours: engine_hours
    engine_battery: engine_battery
    house_battery: house_battery
    water_tank_needle: water_tank_needle
    fuel_tank_needle: fuel_tank_needle
    coolant_temp_needle: coolant_temp_needle

    FloatLayout:

        # Yacht Tilt Guage
        Image:
            source: 'tilt_heel_sky_v2.png'
            allow_stretch: True
            size_hint: 0.1,0.1
            pos: 450,1770
        YachtFront:
            id: heel_yacht
            source: 'yacht_front.png'
            allow_stretch: True
            size_hint: 0.18,0.18
            pos: 300, 1590
        Label:
            id: tilt_value
            text: "360"
            size_hint: 0.2,0.2
            pos: 900, 1475
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 100 

        # Yacht Heel Guage
        Image:
            source: 'tilt_heel_sky_v2.png'
            allow_stretch: True
            size_hint: 0.1,0.1
            pos: 1090,1770            
        YachtSide:
            id: tilt_yacht
            source: 'yacht_side.png'
            allow_stretch: True
            size_hint: 0.18,0.18 
            pos: 940, 1590
        Label:
            id: heel_value
            text: "360"
            size_hint: 0.2,0.2
            pos: 260, 1475
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 100

        # Water Depth Guage
        Label:
            id: water_depth
            text: "3.65 m"
            size_hint: 0.2,0.2
            pos: 1547, 1570
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 100

        # Water Temp
        Label:
            id: water_temp
            text: "21.5"
            size_hint: 0.2,0.2
            pos: 2180, 1570
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 100

        # Engine Hours
        Label:
            id: engine_hours
            text: "347"
            size_hint: 0.2,0.2
            pos: 2820, 105
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 100 

        # Engine Battery
        Label:
            id: engine_battery
            text: "12.8 v"
            size_hint: 0.2,0.2
            pos: 260, 105
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 100 

        # House Battery
        Label:
            id: house_battery
            text: "13.2 v"
            size_hint: 0.2,0.2
            pos: 900, 105
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 100                                                

        # Coolant Temp Needle
        Needle:
            id: coolant_temp_needle
            source: 'small_dial_needle.png'
            allow_stretch: True
            size_hint: 0.1, 0.1
            pos: 3011,1672
            
        # Fuel Tank Needle
        Needle:
            id: fuel_tank_needle
            source: 'small_dial_needle.png'
            allow_stretch: True
            size_hint: 0.1, 0.1
            pos: 1730,208

        # Water Tank Needle
        Needle:
            id: water_tank_needle
            source: 'small_dial_needle.png'
            allow_stretch: True
            size_hint: 0.1, 0.1
            pos: 2366,208

        # RPMs Needle
        RPMsNeedle:
            id: rpms_temp_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 2946,834

        # Speed Needle
        SpeedNeedle:
            id: speed_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 1068,834

        # SOG Needle
        SOGNeedle:
            id: sog_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 2006,834            



    # RelativeLayout:
    #     cols: 1
    #     canvas.before:
    #         Color:
    #             rgba: 0,0,0,1
    #         Rectangle:
    #             size: self.size
    #             pos: 0,0
    #     RelativeLayout:
    #         Image:
    #             source: 'direction_and_depth_guage_color_wheel.png'
    #         DirDial:
    #             id: dir_dial
    #             source: 'direction_and_depth_guage_dial.png'
    #         Image:
    #             source: 'direction_and_depth_guage_panels.png'                
    #         Label:
    #             bold: True
    #             italic: True
    #             font_size: 30
    #             color: 0,0,0,1
    #             id: dir_heading
    #             text: "asd"
    #             size_hint_y: 0.2
    #             pos: 0,5
    #         Label:
    #             italic: True
    #             font_size: 20
    #             color: 0,0,0,1
    #             text: "GPS Speed"
    #             pos: 0,30
    #         Label:
    #             bold: True
    #             italic: True
    #             font_size: 45
    #             color: 0,0,0,1
    #             id: gps_speed
    #             text: "0 kt"
    #             pos: 0,-15
    #         Label:
    #             #bold: True
    #             italic: True
    #             font_size: 12
    #             color: 0,0,0,1
    #             text: "Water Temp"
    #             size_hint_y: 0.2
    #             pos: -91,220
    #         Label:
    #             id: water_temp
    #             bold: True
    #             italic: True
    #             font_size: 28
    #             color: 0,0,0,1
    #             text: "Water Temp"
    #             size_hint_y: 0.2
    #             pos: -91,199                                                           

    # RelativeLayout:
    #     Image:
    #         source: 'tilt_heel_sky.png'
    #     YachtFront:
    #         id: heel_yacht
    #         source: 'yacht_front.png'
    #     Image:
    #         source: 'tilt_heel_water.png'
    #     Image:
    #         source: 'tilt_heel_surround.png'
    #     Image:
    #         source: 'tilt_heel_bottom_panel.png'  
    #     Label:
    #         italic: True
    #         font_size: 20
    #         color: 0,0,0,1
    #         text: "Heel"
    #         pos: 0,-65
    #     Label:
    #         bold: True
    #         italic: True
    #         font_size: 45
    #         color: 0,0,0,1
    #         id: heel_actual
    #         text: "0"
    #         pos: 0,-95                               
    # RelativeLayout:
    #     Image:
    #         source: 'tilt_heel_sky.png'
    #     YachtSide:
    #         id: tilt_yacht
    #         source: 'yacht_side.png'
    #     Image:
    #         source: 'tilt_heel_water.png'
    #     Image:
    #         source: 'tilt_heel_surround.png'
    #     Image:
    #         source: 'tilt_heel_bottom_panel.png'   
    #     Label:
    #         italic: True
    #         font_size: 20
    #         color: 0,0,0,1
    #         text: "Tilt"
    #         pos: 0,-65
    #     Label:
    #         bold: True
    #         italic: True
    #         font_size: 45
    #         color: 0,0,0,1
    #         id: tilt_actual
    #         text: "0"
    #         pos: 0,-95           

    # RelativeLayout:
    #     cols: 1
    #     canvas.before:
    #         Color:
    #             rgba: 0,0,0,1
    #         Rectangle:
    #             size: self.size
    #             pos: 0,0
    #     RelativeLayout:
    #         Image:
    #             source: 'wind_background.png'
    #         Label:
    #             #bold: True
    #             italic: True
    #             font_size: 15
    #             color: 0,0,0,1
    #             text: "Wind Speed"
    #             size_hint_y: 0.2
    #             pos: 0,60 
    #         Label:
    #             bold: True
    #             font_size: 35
    #             color: 0,0,0,1
    #             id: wind_speed
    #             text: "0 kt"
    #             size_hint_y: 0.2
    #             pos: 0,35
    #         Label:
    #             #bold: True
    #             italic: True
    #             font_size: 15
    #             color: 0,0,0,1
    #             text: "Knots"
    #             size_hint_y: 0.2
    #             pos: 0,12                
                          
    #     RelativeLayout:        
    #         WindDirNeedle:
    #             id: wind_needle
    #             source: 'wind_needle.png'
    #             pos: 0,-6
 


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
    WebSocketTest().run()
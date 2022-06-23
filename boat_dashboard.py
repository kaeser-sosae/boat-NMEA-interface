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
import _thread
import time
import json
import os
import ctypes

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

<CompassDial@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix        

<FuelTankNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix

<CoolantTempNeedle@Image>:
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
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix 

<SOGNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix 

<RPMsNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix

<TrueWindNeedle@Image>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0,0,1
            origin: root.center
    canvas.after:
        PopMatrix  

<ApparentWindNeedle@Image>:
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
    apparent_wind_needle: apparent_wind_needle
    apparent_wind_speed_value: apparent_wind_speed_value
    true_wind_needle: true_wind_needle
    true_wind_speed_value: true_wind_speed_value
    sog_needle: sog_needle
    sog_value: sog_value
    speed_needle: speed_needle
    speed_value: speed_value
    rpms_needle: rpms_needle
    rpms_value: rpms_value
    engine_battery_volts: engine_battery_volts
    engine_battery_percent: engine_battery_percent
    house_battery_volts: house_battery_volts
    house_battery_percent: house_battery_percent
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
        CoolantTempNeedle:
            id: coolant_temp_needle
            source: 'small_dial_needle.png'
            allow_stretch: True
            size_hint: 0.1, 0.1
            pos: 1507,836

        # Apparent Wind Value
        Label:
            id: apparent_wind_speed_value
            text: "-"
            size_hint: 0.07,0.05
            pos: 192,560
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 35

        #Apparent Wind Needle
        ApparentWindNeedle:
            id: apparent_wind_needle
            source: 'apparent_wind_arrow.png'
            allow_stretch: True
            size_hint: 0.23, 0.23
            pos: 37,401

        # True Wind Value
        Label:
            id: true_wind_speed_value
            text: "-"
            size_hint: 0.07,0.05
            pos: 192,430
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 35

        # True Wind Needle
        TrueWindNeedle:
            id: true_wind_needle
            source: 'true_wind_arrow.png'
            allow_stretch: True
            size_hint: 0.24, 0.24
            pos: 26,396
                    

        # SOG Value
        Label:
            id: sog_value
            text: "-"
            size_hint: 0.2,0.2
            pos: 533,335
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60

        # SOG Needle
        SOGNeedle:
            id: sog_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 534,415

        # Speed Value
        Label:
            id: speed_value
            text: "-"
            size_hint: 0.2,0.2
            pos: 1003,335
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60

        # Speed Needle
        SpeedNeedle:
            id: speed_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 1003,415

        # RPMs Value
        Label:
            id: rpms_value
            text: "-"
            size_hint: 0.2,0.2
            pos: 1472,335
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60

        # RPMs Needle
        RPMsNeedle:
            id: rpms_needle
            source: 'large_dial_needle.png'
            allow_stretch: True
            size_hint: 0.2, 0.2
            pos: 1472,415 

        # Engine Battery
        Label:
            id: engine_battery_percent
            text: "-"
            size_hint: 0.2,0.2
            pos: 130, 90
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60 
        Label:
            id: engine_battery_volts
            text: "-"
            size_hint: 0.2,0.2
            pos: 130, 35
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 30 

        # House Battery
        Label:
            id: house_battery_percent
            text: "-"
            size_hint: 0.2,0.2
            pos: 450, 90
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 60 
        Label:
            id: house_battery_volts
            text: "-"
            size_hint: 0.2,0.2
            pos: 450, 35
            font_name: "SFProSB"
            rgba: 245,245,245,1
            font_size: 30                                                
            
        # Compass
        Image:
            source: 'direction_and_depth_guage_color_wheel.png'
            allow_stretch: True
            size_hint: 0.21,0.21
            pos: 761,44
        CompassDial:
            id: dir_dial
            source: 'direction_and_depth_guage_dial.png'
            allow_stretch: True
            size_hint: 0.21, 0.21
            pos: 761,44
        Label:
            id: dir_heading
            text: "-"
            size_hint: 0.2,0.2
            pos: 770,50
            font_name: "SFProSB"
            color: "black"
            font_size: 60 

        # Fuel Tank Needle
        FuelTankNeedle:
            id: fuel_tank_needle
            source: 'small_dial_needle.png'
            allow_stretch: True
            size_hint: 0.1, 0.1
            pos: 1183, 104

        # Engine Hours
        Label:
            id: engine_hours
            text: "-"
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
    wind_speed = ObjectProperty()
    wind_direction = ObjectProperty()
    apparent_wind_needle = ObjectProperty()
    apparent_wind_speed_value = ObjectProperty()
    true_wind_needle = ObjectProperty()
    true_wind_speed_value = ObjectProperty()
    engine_hours = ObjectProperty()
    engine_battery_percent = ObjectProperty()
    engine_battery_volts = ObjectProperty()
    house_battery_percent = ObjectProperty()
    house_battery_volts = ObjectProperty()
    water_tank_needle = ObjectProperty()
    fuel_tank_needle = ObjectProperty()
    coolant_temp_needle = ObjectProperty()
    tilt_yacht = ObjectProperty()
    tilt_value = ObjectProperty()
    heel_yacht = ObjectProperty()
    heel_value = ObjectProperty()
    rpms_value = ObjectProperty()
    rpms_needle = ObjectProperty()

    pressed = False

    def __init__(self, **kwargs):
        super(WS, self).__init__(**kwargs)
        Logger.info('Layout: initialized')

class SignalKInterface(App):
    ws = None
    #url = "ws://172.30.3.149:3000/signalk/v1/stream?subscribe=all"
    #url2 = "ws://serenity-tweed.ddns.net:3000/signalk/v1/stream?subscribe=all"
    layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SignalKInterface, self).__init__(**kwargs)
        socket_server="ws://serenity-tweed.ddns.net:3000/signalk/v1/stream?subscribe=all"
        #socket_server="ws://172.30.3.149:3000/signalk/v1/stream?subscribe=all"
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
        Window.size = screenwidth, screenheight-40 # This is real setting for 1080p
        Window.top = 0
        Window.left = 0
        self.layout = WS()

        # Set the default angles and values
        self.layout.sog_needle.angle = 43
        self.layout.speed_needle.angle = 43
        self.layout.rpms_needle.angle = 43
        

        return self.layout

    def on_ws_message(self, ws, message):

        json_message = json.loads(message)

        for update in json_message["updates"]:
            #print(Window.size)
            for value in update["values"]:

                # Water Temperature
                if (value["path"] == "environment.water.temperature"):
                    #print("Got water temp: " + str(value["value"]))
                    self.layout.water_temp.text = str(float("{:.1f}".format(float(value["value"]) - 273.15))) #+ " " + degree_sign + "C"

                # Water Depth
                if (value["path"] == "environment.depth.belowTransducer"):
                    #print("Got water depth: " + str(value["value"]))
                    self.layout.water_depth.text = str(float("{:.2f}".format(float(value["value"])))) #+ " " + degree_sign + "C"

                # Coolant Temperature
                if (value["path"] == "propulsion.port.temperature"):
                    #print("Got coolant temp: " + str(value["value"]))
                    self.layout.coolant_temp_needle.angle = 0 - float("{:.1f}".format(float(value["value"]) - 273.15))*1.5

                # Petrol Tank Level
                if (value["path"] == "tanks.fuel.0.currentLevel"):
                    #print("Got petrol tank: " + str(value["value"]))
                    self.layout.fuel_tank_needle.angle = 0 - float("{:.1f}".format(float(value["value"])))/0.0055555555555555555

                # Heel and Tilt
                if (value["path"] == "navigation.attitude"):
                    #print("Got roll: " + str(value["value"]["roll"]))
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
                    #print(" - Converted to degrees: " + str(heel_angle_degrees))
                    #print(" - Converted to human: " + heel_angle_translated)
                    self.layout.heel_yacht.angle = int(heel_angle_degrees) * -1
                    self.layout.heel_value.text = heel_angle_translated

                    #print("Got pitch: " + str(value["value"]["pitch"]))
                    tilt_angle_raw = value["value"]["pitch"]
                    tilt_angle_degrees = tilt_angle_raw * 57.29
                    tilt_angle_translated = "0"
                    tilt_angle_translated_clean = ""
                    if tilt_angle_degrees > 0:
                        tilt_angle_translated = str(int(float("{:.0f}".format(tilt_angle_degrees)))) + degree_sign + " F"
                        tilt_angle_translated_clean = str(int(float("{:.0f}".format(tilt_angle_degrees))))
                    if tilt_angle_degrees < 0:
                        tilt_angle_translated = str(int(float("{:.0f}".format(tilt_angle_degrees)) * -1)) + degree_sign + " B"
                        tilt_angle_translated_clean = str(int(float("{:.0f}".format(tilt_angle_degrees)) * -1))
                    #print(" - Converted to degrees: " + str(tilt_angle_degrees))
                    #print(" - Converted to human: " + tilt_angle_translated)
                    self.layout.tilt_yacht.angle = int(tilt_angle_degrees)
                    self.layout.tilt_value.text = tilt_angle_translated

                # Engine Battery
                # Use Victron NMEA once we have it
                #if (value["path"] == "electrical.batteries.0.voltage"):
                #    print("Got engine battery: " + str(value["value"]))
                #    self.layout.engine_battery_volts.text = str(float("{:.2f}".format(float(value["value"]))))
                # House Battery
                # Use Victron NMEA once we have it
                #if (value["path"] == "electrical.batteries.0.voltage"):
                #    print("Got engine battery: " + str(value["value"]))
                #    self.layout.engine_battery_volts.text = str(float("{:.2f}".format(float(value["value"]))))

                # Speed through water
                if (value["path"] == "navigation.speedThroughWater"):
                    #print("Got water speed: " + str(value["value"]))
                    speed_in_knots = float("{:.2f}".format(float(value["value"]))) * 1.94384
                    self.layout.speed_value.text = str(float("{:.2f}".format(float(speed_in_knots))))
                    if speed_in_knots == 0:
                        self.layout.speed_needle.angle = 43
                    else:
                        self.layout.speed_needle.angle = 43-(266/(16/speed_in_knots))

                # Speed over ground
                if (value["path"] == "navigation.speedOverGround"):
                    sog = value["value"]
                    print("Got speed over ground: " + str(sog) + " m/s")

                    sog_in_knots = float("{:.2f}".format(float(sog))) * 1.94384
                    self.layout.sog_value.text = str(float("{:.2f}".format(float(sog_in_knots))))
                    if sog_in_knots == 0:
                        self.layout.sog_needle.angle = 43
                    else:                    
                        self.layout.sog_needle.angle = 43-(266/(16/sog_in_knots))

                # Engine RPMs
                # propulsion.port.revolutions
                if (value["path"] == "propulsion.port.revolutions"):
                    #print("Got RPMs: " + str(float(value["value"])*60))
                    rpms = float(value["value"])*60
                    self.layout.rpms_value.text = str(float("{:.2f}".format(rpms)))
                    if rpms == 0:
                        #print('RPMs are 0, setting needle to 0')
                        rpms_needle_angle = 43
                    else:
                        rpms_needle_angle = 43-(266/(4000/rpms))
                    self.layout.rpms_needle.angle = rpms_needle_angle


                # Engine hours
                # propulsion.port.temperature
                if (value["path"] == "propulsion.port.temperature"):
                    #print("Got engine hours: " + str(value["value"]))
                    self.layout.engine_hours.txt = str(float("{:.1f}".format(float(value["value"]))))           

                
                # Apparent Wind Speed
                if (value["path"] == "environment.wind.speedApparent"):
                    #print("Got apparent wind speed: " + str(value["value"]) + " m/s")
                    self.layout.apparent_wind_speed_value.text = str(float("{:.1f}".format(float(value["value"])*1.94384))) + " kts"
                
                if (value["path"] == "environment.wind.angleApparent"):
                    #print("Got apparent wind angle: " + str(value["value"]) + " rads")
                    wind_angle_raw = value["value"]
                    wind_angle_degrees = wind_angle_raw * 57.2958
                    #print("Got apparent wind angle: " + str(wind_angle_degrees) + " degrees")
                    wind_angle_translated = ""
                    wind_angle_translated_clean = ""
                    wind_angle_adjusted_for_needle = 0.0000001
                    if wind_angle_degrees > 0:
                        wind_angle_translated = str(int(float("{:.0f}".format(wind_angle_degrees)))) + " S"
                        wind_angle_translated_clean = str(int(float("{:.0f}".format(wind_angle_degrees))))
                        wind_angle_adjusted_for_needle = 0 - 90 - wind_angle_degrees
                    if wind_angle_degrees < 0:
                        wind_angle_translated = str(int(float("{:.0f}".format(wind_angle_degrees)))) + " P"
                        wind_angle_translated_clean = str(int(float("{:.0f}".format(wind_angle_degrees)) * -1))
                        wind_angle_adjusted_for_needle = 0 - 90 + wind_angle_degrees
                    self.layout.apparent_wind_needle.angle = float(wind_angle_adjusted_for_needle)
                    #print("The apparent wind arrow angle should be " + str(wind_angle_adjusted_for_needle))
                    #print(" - it is: " + str(self.layout.apparent_wind_needle.angle))

                if (value["path"] == "navigation.courseOverGroundTrue"):
                    cog = value["value"]
                    print("Got course over ground: " + str(cog) + " rads")
                    course_angle_degrees = float(float(cog) * 57.2958)
                    print("Got course over ground: " + str(course_angle_degrees) + " degrees")
                    self.layout.dir_dial.angle = course_angle_degrees
                    self.layout.dir_heading.text = str(int(course_angle_degrees)) + "" + degree_sign + ""


    def on_ws_error(self, ws, error):
        self.logger.info('WebSocket: [ERROR]  {}'.format(error))

    def ws_connection(self, dt, **kwargs):
        # start a new thread connected to the web socket
        _thread.start_new_thread(self.ws.run_forever, ())

    def on_ws_open(self, ws):
        def run(*args):
            time.sleep(1)
        _thread.start_new_thread(run, ())

    def on_ws_close(self, ws):
        print("Websockets connection closed, waiting 10 seconds...")
        time.sleep(10)
        ws_connection()
        print("Reconnecting websockets...")
        #self.layout.the_btn.text = '### closed ###'


if __name__ == "__main__":
    SignalKInterface().run()
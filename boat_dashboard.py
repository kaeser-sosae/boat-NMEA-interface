from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.logger import Logger

import websocket

# standard libraries (python 2.7)
import _thread
import time

import json

kv = '''
<WS>:

    canvas:
        Rectangle:
            id: first_line
            pos: (0,self.height/3*3)
            size: (self.width,10)
        Rectangle:
            id: first_line
            pos: (0,self.height/3*2)
            size: (self.width,10)
        Rectangle:
            id: first_line
            pos: (0,self.height/3)
            size: (self.width,10)
        Rectangle:
            id: first_line
            pos: (0,0)
            size: (10,self.height)  
        Rectangle:
            id: first_line
            pos: (self.width-10,0)
            size: (10,self.height)  
        Rectangle:
            id: first_line
            pos: (0,self.height-10)
            size: (self.width,10) 
        Rectangle:
            id: first_line
            pos: (0,0)
            size: (self.width,10)                  

    orientation: 'vertical'
    
    water_temp: water_temp
    water_speed: water_speed
    land_speed: land_speed

    Label:
        font_size: 75
        id: water_temp
        text: "0"
    Label:
        font_size: 75
        id: water_speed
        text: "0 kt"
    Label:
        font_size: 75
        id: land_speed
        text: "0 kt"


'''
Builder.load_string(kv)

degree_sign = u'\N{DEGREE SIGN}'

from kivy.config import Config
from kivy.core.window import Window

class KivyWebSocket(websocket.WebSocketApp):

    def __init__(self, *args, **kwargs):
        super(KivyWebSocket, self).__init__(*args, **kwargs)
        self.logger = Logger
        self.logger.info('WebSocket: logger initialized')

class WS(BoxLayout):
    water_temp = ObjectProperty()
    water_speed = ObjectProperty()
    land_speed = ObjectProperty()
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
        Window.borderless = True
        Window.size = 400, 930
        Window.top = 0
        Window.left = 1280
        self.layout = WS()
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
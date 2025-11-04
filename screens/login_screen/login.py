from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.graphics.svg import Svg
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, PushMatrix, PopMatrix, Scale, Translate, Rotate


from kivymd.uix.screen import MDScreen


from kaki.app import App
import requests
import json

from components.connection.connector import Connector
from components.connection.credentials import URL

class Login(MDScreen):

    def on_pre_enter(self):
        self.path = App.get_running_app().user_data_dir+"/"
    
        Clock.schedule_once(self.on_start, 1)
    

    def on_start(self, *args):
        store = JsonStore(self.path+"data.json")

        if store.exists('login_auth'):
            if store.get('login_auth')['access'] == True:

                self.manager.user_id = store.get('user')['id']

                self.change_screen("core_name")


    def do_login(self, *args):
        data = {
            "email": self.ids.id_text_email.text,
            "password": self.ids.id_text_password.text
        }
        head = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(URL+"/auth/login", data=json.dumps(data), headers=head)
        
        
        if response.status_code == 200:
            user = response.json()
            if type(user) is dict:
                # in app
                store =  JsonStore("config.json")
                store.put('credential', 
                    USERNAME=self.ids.id_text_email.text,
                    PASSWORD=self.ids.id_text_password.text
                )

                # user 
                store = JsonStore(self.path+"data.json")
                store.put('user', id=user['user'])
                store.put('authentication', token_access=user['token'], response=True)
                store.put('login_auth', access=True)

                self.change_screen("core_name")

    
    def change_screen(self, screen_name, *args):
        self.manager.current = screen_name
        



class LabelRegister(ButtonBehavior, Label):
    pass



class SVGWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.svg_path = "assets/img/wave.svg"
        
        Window.bind(on_resize=self.update_canvas)
        self.bind(size=self.update_canvas, pos=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()

            scale_x = self.width / 1000  # 1000 = largura original do SVG
            scale_y = self.height / 100   # 100 = altura original do SVG
            
            
            Scale(scale_x+1, 2.8, 1)

            
            Translate(0, 0)

            self.rot = Rotate(
                angle=180,
                origin=(200, 150, 0),  # ponto central no topo
                axis=(0, 0, 1)
            )

            self.svg = Svg(self.svg_path)

            PopMatrix()
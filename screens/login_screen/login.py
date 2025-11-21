from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.graphics.svg import Svg
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, PushMatrix, PopMatrix, Scale, Translate, Rotate
from kivy.metrics import dp

from kivymd.uix.snackbar.snackbar import MDSnackbar, MDSnackbarActionButton, MDSnackbarActionButtonText
from kivymd.uix.snackbar.snackbar import MDSnackbarButtonContainer, MDSnackbarSupportingText, MDSnackbarCloseButton, MDSnackbarText


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
        else:
            MDSnackbar(
                MDSnackbarText(
                    text="Credentials Not Match Or Server Down",
                ),
                MDSnackbarButtonContainer(
                    Widget(),
                    
                    MDSnackbarCloseButton(
                        icon="close",
                    ),
                ),
                y=dp(124),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.9,
                padding=[0, 0, "8dp", "8dp"],
            ).open()
    
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

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:

            PushMatrix()

            # carregue o SVG antes de calcular escala
            svg = Svg(self.svg_path)

            # tamanho original do SVG
            orig_w = svg.width
            orig_h = svg.height

            # escala proporcional ao tamanho do widget
            scale_x = self.width / orig_w
            scale_y = self.height / orig_h

            # usa a menor escala para não distorcer
            scale = min(scale_x, scale_y)

            Scale(scale, scale, 1)

            # centraliza corretamente
            Translate(-orig_w / 2, -orig_h / 2)

            # origem sempre no centro do widget, nunca números mágicos
            Rotate(
                angle=180,
                origin=(self.width / 2, self.height / 2, 0),
                axis=(0, 0, 1)
            )

            self.svg = svg

            PopMatrix()
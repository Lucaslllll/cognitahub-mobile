from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationbar import (
    MDNavigationBar, MDNavigationItem, MDNavigationItemLabel,
    MDNavigationItemIcon
)
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon
from kivymd.uix.swiper.swiper import MDSwiperItem

from kivymd.uix.snackbar.snackbar import MDSnackbar, MDSnackbarActionButton, MDSnackbarActionButtonText
from kivymd.uix.snackbar.snackbar import MDSnackbarButtonContainer, MDSnackbarSupportingText, MDSnackbarCloseButton, MDSnackbarText


from kivy.uix.widget import Widget
from kivy.graphics.svg import Svg
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, PushMatrix, PopMatrix, Scale, Translate, Rotate
from kivy.metrics import dp

from components.connection.connector import Connector
from components.connection.credentials import URL
import requests
import json

class Register(MDScreen):
    screen_name_pass = "register_name"


    def open_snackbar(self, msg:str, *args):
        MDSnackbar(
            MDSnackbarText(
                text=msg,
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
    
    def do_register(self):

        if self.ids.id_text_terms_of_use.active == True:

            if self.ids.id_text_password.text != "" and self.ids.id_text_password.text == self.ids.id_text_password_repeat.text:

                data = {
                    "name": self.ids.id_text_username.text,
                    "email": self.ids.id_text_email.text,
                    "password": self.ids.id_text_password.text
                }

                head = {
                    "Content-Type": "application/json"
                }
                
                response = requests.post(URL+"/auth/register", data=json.dumps(data), headers=head)
                
                
                if response.status_code == 200:
                    user = response.json()
                    if type(user) is dict:
                        self.open_snackbar("User Registered")
                        self.screen_name_pass = "login_name"
                        Clock.schedule_once(self.change_to_login, 1.5)
                else:
                    #print(response.text)
                    self.open_snackbar("Missing Fields Or User Already Created")
                    self.screen_name_pass = "login_name"
                    Clock.schedule_once(self.change_to_login, 1.5)
            else:
               self.open_snackbar("Passwords Do Not Match")
                    
        else:
            self.open_snackbar("Accept All Terms")
        
        


    def change_screen(self, screen_name, *args):
        self.manager.current = screen_name

    def change_to_login(self, *args):
        self.manager.current = self.screen_name_pass
    
    def on_pre_leave(self):
        self.ids.id_text_username.text = ""
        self.ids.id_text_email.text = ""
        self.ids.id_text_password.text = ""
        self.ids.id_text_password_repeat.text = "" 



class SVGWidgetR(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.svg_path = "assets/img/wave.svg"

        self.bind(size=self.update_canvas, pos=self.update_canvas)
        Window.bind(on_resize=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:

            PushMatrix()

            # Carrega SVG
            svg = Svg(self.svg_path)

            # dimensões originais do SVG
            orig_w = svg.width
            orig_h = svg.height

            # proporcional ao tamanho do widget
            scale_x = self.width / orig_w
            scale_y = self.height / orig_h
            scale = min(scale_x, scale_y)

            # testar essa escala responsiva
            Scale(scale, scale, 1)

            Translate(
                (self.width - orig_w * scale) / 2,
                (self.height - orig_h * scale) / 2
            )

            # rotação responsiva girando no centro do widget
            Rotate(
                angle=270,
                origin=(self.width / 2, self.height / 2, 0),
                axis=(0, 0, 1)
            )

            self.svg = svg

            PopMatrix()

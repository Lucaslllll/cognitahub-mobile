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


class Register(MDScreen):


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
                    "password": self.ids.id_text_password
                }

                head = {
                    "Content-Type": "application/json"
                }
                
                response = requests.post(URL+"/auth/register", data=json.dumps(data), headers=head)
                
                
                if response.status_code == 200:
                    user = response.json()
                    if type(user) is dict:
                        self.open_snackbar("User Registered")
                else:
                    self.open_snackbar("Missing Fields Or User Already Created")
            
            else:
               self.open_snackbar("Passwords Do Not Match")
                    
        else:
            self.open_snackbar("Accept All Terms")

    def change_screen(self, screen_name, *args):
        self.manager.current = screen_name




class SVGWidgetR(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 0.2, 1, 1)
            PushMatrix()
            # Mover
            Translate(0, 100)     # desloca em X e Y
            # tamanho
            Scale(1.3, 1.5, 1)
            self.rot = Rotate(
                angle=270,      # o ângulo
                origin=(300, 300, 0),  # ponto de rotação (x, y, z)
                axis=(0, 0, 1)     # eixo de rotação (z = 1 => plano 2D)
            )

            # Renderiza o SVG
            self.svg = Svg("assets/img/wave.svg")
            PopMatrix()
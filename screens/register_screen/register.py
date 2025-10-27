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


from kivy.uix.widget import Widget
from kivy.graphics.svg import Svg
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, PushMatrix, PopMatrix, Scale, Translate, Rotate


from components.connection.connector import Connector
from components.connection.credentials import URL


class Register(MDScreen):
    
    def do_register(self):
        self.manager.current = "core_name"

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
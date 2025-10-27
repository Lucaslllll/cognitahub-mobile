from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.clock import Clock



from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon

from kivymd.uix.screen import MDScreen


from kaki.app import App

from components.connection.connector import Connector

from kivy.utils import hex_colormap

class TrailingPressedIconButton( ButtonBehavior, RotateBehavior, MDListItemTrailingIcon ):
    pass

class Course(MDScreen):
    
    # def on_pre_enter(self):
    #     Clock.schedule_once(self.on_start, 2)
    
    # def on_start(self, *args):
    #     print(hex_colormap)

    def tap_expansion_chevron(self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton):
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(
            chevron
        ) if not panel.is_open else panel.set_chevron_up(chevron)


    def change_screen_to_core(self, number):
        self.manager.current = "core_name"
        self.manager.current_screen.ids.id_screen_manager.current = number

    def change_screen(self, name):
        self.manager.current = name



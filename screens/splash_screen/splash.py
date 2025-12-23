from kivy.core.window import Window
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kaki.app import App
import os
os.environ['KIVY_IMAGE'] = 'sdl2,gif'

class Splash(MDScreen):
    
    def on_pre_enter(self):
        self.path = App.get_running_app().user_data_dir+"/"
    
        Clock.schedule_once(self.on_start, 1)
    

    def on_start(self, *args):
        store = JsonStore(self.path+"data.json")

        if store.exists('login_auth'):
            if store.get('login_auth')['access'] == True:

                self.manager.user_id = store.get('user')['id']

                self.change_screen("core_name")
    
    def change_screen(self, screen_name, *args):
        self.manager.current = screen_name
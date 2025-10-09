# -*- coding: utf-8 -*-
import os

from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory

from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.core.window import Window 
from kivy.config import Config 
Window.softinput_mode = 'below_target'
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('kivy', 'exit_on_escape', 'False')

from components.connection.authentication import Authenticat



class CognitaHubApp(App, MDApp):

    def __init__(self, **kwargs):
        super(CognitaHubApp, self).__init__(**kwargs)
        self.path = self.user_data_dir+"/"
        self.auth = Authenticat()
        self.response = self.auth.do_auth()
        self.token_access = self.auth.get_token()
        self.backgroundColorDefault = "Aliceblue"
        self.store = JsonStore(self.path+"data.json")

        if self.response == True:
            self.store.put(
                'authentication',
                response=self.response,
                token_access=self.token_access
            )
        
        if self.store.exists('background'):
            self.backgroundColorDefault = self.store.get('background')['color']



        
        Clock.schedule_interval(self.reloads, 120)


    # lembrar de tirar no deploy
    DEBUG = 1

    KV_FILES = {
        os.path.join(os.getcwd(), "screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "screens/core_screen/core.kv"),
        
    }

    CLASSES = {
        "MainScreenManager": "screens.screenmanager",
        "Core": "screens.core_screen.core",
        
    }


    AUTORELOAD_PATHS = [
        (".", {"recursive": True}),
    ]


    def reloads(self, *args):
        self.response = self.auth.do_auth()
        self.token_access = self.auth.get_token()
        store = JsonStore(self.path+'data.json')
        store.put(
                'authentication',
                response=self.response,
                token_access=self.token_access
            )



    def build_app(self):
        self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = self.backgroundColorDefault

        return Factory.MainScreenManager()

    
    def on_start(self):
        # self.fps_monitor_start()
        pass


CognitaHubApp().run()
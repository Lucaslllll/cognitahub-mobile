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

from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.theming import ThemeManager
from kivy.properties import OptionProperty

from components.connection.authentication import Authenticat

from kivy.utils import hex_colormap
hex_colormap['azulprofundo'] = "#312C51"
hex_colormap['azulprofundoleve'] = "#48426D"


class MyThemeMngr(ThemeManager):
    primary_palette = OptionProperty(None,
        options=[name_color.capitalize() for name_color in hex_colormap.keys()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.primary_palette = 'Azulprofundo'
        self.secondary_palette = 'Azulprofundoleve'


class CognitaHubApp(App, MDApp):

    def __init__(self, **kwargs):
        super(CognitaHubApp, self).__init__(**kwargs)
        self.theme_cls = MyThemeMngr()  

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
        os.path.join(os.getcwd(), "screens/mainscreenmanager.kv"),
        os.path.join(os.getcwd(), "screens/core_screen/core.kv"),
        os.path.join(os.getcwd(), "screens/register_screen/register.kv"),
        os.path.join(os.getcwd(), "screens/login_screen/login.kv"),
        os.path.join(os.getcwd(), "screens/course_screen/course.kv"),
        os.path.join(os.getcwd(), "screens/list_article_screen/list-article.kv"),
        os.path.join(os.getcwd(), "screens/article_screen/article.kv"),
        os.path.join(os.getcwd(), "screens/list_exercise_screen/list-exercise.kv"),
        os.path.join(os.getcwd(), "screens/create_topic_screen/create-topic.kv"), 
    }

    CLASSES = {
        "MainScreenManager": "screens.mainscreenmanager",
        "Core": "screens.core_screen.core",
        "Register": "screens.register_screen.register",
        "Login": "screens.login_screen.login",
        "Course": "screens.course_screen.course",
        "ListArticle": "screens.list_article_screen.list-article",
        "Article": "screens.article_screen.article",
        "ListExercise": "screens.list_exercise_screen.list-exercise",
        "CreateTopic": "screens.create_topic_screen.create-topic",
    }


    AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]

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
        self.wave_path = os.path.join(os.path.dirname(__file__), "assets/img/bg.png")
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Darkblue"
        self.theme_cls.backgroundColor = "#312C51"
        self.theme_cls.secondaryColor = "#48426D"
        self.theme_cls.tertiaryColor = "#F0C38E"

        return Factory.MainScreenManager()


    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.primary_color,  # status bar color
            self.theme_cls.primary_color,  # navigation bar color
            "Dark",                        # icons color of status bar
        )

    
    def on_start(self):
        # self.fps_monitor_start()
        pass


CognitaHubApp().run()
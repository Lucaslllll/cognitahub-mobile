from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.metrics import dp
from kivy.uix.widget import Widget

from kivymd.uix.snackbar.snackbar import MDSnackbar, MDSnackbarActionButton, MDSnackbarActionButtonText
from kivymd.uix.snackbar.snackbar import MDSnackbarButtonContainer, MDSnackbarSupportingText, MDSnackbarCloseButton, MDSnackbarText

from kaki.app import App
from datetime import date
import json

from components.connection.connector import Connector




class CreateTopic(MDScreen):
    pass_two = BooleanProperty()
    only_one = BooleanProperty()

    def on_pre_enter(self):
        self.range_bar = 0
        self.only_one = False
        Clock.schedule_interval(self.check_form, 1)

    def check_form(self, *args):

        if self.ids.id_title.text != "" and self.range_bar <= 0:
            self.ids.progress_bar.value += 50
            self.range_bar += 1
            self.pass_two = False

        
        if self.ids.id_text.text != "" and self.range_bar == 1:
            self.ids.progress_bar.value += 50
            self.range_bar += 1

    
    def send_topic(self):
        
        data = {
            "name": self.ids.id_title.text,
            "details": self.ids.id_text.text,
            "date": date.today().isoformat(),
            "author": self.manager.user_id
        }

        user = Connector(name_url="topic/create", tag="CREATE A TOPIC")
        user = user.post(data=data)

        if type(user) is bool:
            if user == True:
                self.only_one = False
                MDSnackbar(
                    MDSnackbarText(
                        text="Question Posted",
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
                Clock.schedule_once(self.change_screen, 2)

    def change_screen(self, *args):
        self.manager.current = "core_name"


    def on_pre_leave(self):
        self.ids.id_title.text = ""
        self.ids.id_text.text = ""

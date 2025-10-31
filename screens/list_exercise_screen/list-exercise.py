from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon

from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar


from kaki.app import App

from components.connection.connector import Connector
from components.connection.credentials import URL
import os
import requests


class TrailingPressedIconButton( ButtonBehavior, RotateBehavior, MDListItemTrailingIcon ):
    pass


class MDExpansionPanelItem(MDExpansionPanel):
    screen_object = ObjectProperty()
    id_exercise = NumericProperty()
    text_exercise = StringProperty()
    details_exercise = StringProperty()
    link_download = StringProperty()


    def tap_expansion_chevron(self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton):
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(
            chevron
        ) if not panel.is_open else panel.set_chevron_up(chevron)

    
    def download(self):
        path_file_destination = os.path.join(os.getcwd(), self.link_download)

        try:
            self.ids.status_download.text = "Download arquivo..."
            
            response = requests.get(URL+"/download/task/{}".format(self.link_download), stream=True)
            response.raise_for_status()  # lança erro se algo deu errado

            with open(path_file_destination, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            self.ids.status_download.text = f"File saved in :\n{path_file_destination}"

        except Exception as e:
            self.ids.status_download.text = f"Error to download: {e}"
            print(e)


class ListExercise(MDScreen):

    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)

    def on_start(self, *args):
        self.id_course = self.manager.select_course
        self.ids.id_expansion_exercise.clear_widgets()

        tasks = Connector(name_url="tasks/course/{}".format(self.id_course), tag="List Exercise By Course")
        tasks = tasks.get()


        if type(tasks) is list:
            
            for task in tasks:
                self.ids.id_expansion_exercise.add_widget(
                    MDExpansionPanelItem(
                        screen_object=self,
                        id_exercise=task["id"],
                        text_exercise=task["name"],
                        details_exercise=task["details"],
                        link_download = "none" if task["downloadFile"] is None else task["downloadFile"] 

                    )
                
                )
        
        


    def change_screen(self, name):
        self.manager.current = name



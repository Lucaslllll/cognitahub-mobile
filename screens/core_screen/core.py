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

from components.connection.connector import Connector




class Core(MDScreen):
    
    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)
    
    def on_start(self, *args):
        self.ids.id_scroll.clear_widgets()

        courses = Connector(name_url="user/courses", tag="Courses List")
        courses = courses.get()

        if type(courses) is list:
            
            for course in courses:

                self.ids.id_scroll.add_widget(
                    ListItemCustom(
                        MDListItemLeadingAvatar(
                            source="assets/images/default-image.jpg"
                        ),
                        MDListItemHeadlineText(
                            text="name"
                        ),
                        MDListItemSupportingText(
                            text="Subtext suportando tudo que vier melhor"
                        ),
                        screen_object=self,
                        id_user=1,
                        name_user="name",
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        size_hint_x=0.9,
                        theme_bg_color="Custom",
                        md_bg_color=[0.1, 0.1, 0.1, 0.1]
                        
                    ),
                
                )


    def change_screen(self, number):
        self.ids.id_screen_manager.current = number



class ListItemCustom(MDListItem):
    id_user = NumericProperty()
    screen_object = ObjectProperty()
    name_user = StringProperty()

    def talk_with(self):
        self.screen_object.manager.user_id_chat = self.id_user
        self.screen_object.manager.user_name_chat = self.name_user
        self.screen_object.manager.current = "chat_name"
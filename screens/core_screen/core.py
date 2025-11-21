from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore

from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationbar import (
    MDNavigationBar, MDNavigationItem, MDNavigationItemLabel,
    MDNavigationItemIcon
)
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout 
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon
from kivymd.uix.swiper.swiper import MDSwiperItem

from components.connection.connector import Connector
from components.connection.credentials import URL
from urllib.parse import quote
from kaki.app import App


class Core(MDScreen):
    
    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)
    
    def on_start(self, *args):
        self.ids.id_scroll.clear_widgets()
        self.ids.id_swiper_course.clear_widgets()
        self.ids.content_settings.clear_widgets()
        
        self.ids.content_settings.add_widget(
                ConfigItemLogout(
                    MDListItemHeadlineText(text="logout"),
                    MDListItemSupportingText(text="disconnect from app"),
                    MDListItemTrailingIcon(icon="logout"),
                    screen_object=self,
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.secondaryColor,
                )
            )

        self.list_swiper = []

        courses = Connector(name_url="user/courses", tag="Courses List")
        courses = courses.get()

        

        if type(courses) is list:
            
            for course in courses:
                

                # se uma imagem tive um caractere especial isso garantira que
                # ela se adeque corretamente a ascii
                # Corrige a URL fazendo o encode adequado
                
                encoded_url = quote(URL+"/media/"+course["thumb"], safe=':/')
                cardSwiper = CardSwiper(id_course=course["id"], img_url=encoded_url, title=course["name"], screen_object=self)
                self.list_swiper.append(cardSwiper)

                
                self.ids.id_swiper_course.add_widget(
                    cardSwiper
                )

        topics = Connector(name_url="topics", tag="Topics List")
        topics = topics.get()

        if type(topics) is list:
            
            for topic in topics:

                self.ids.id_scroll.add_widget(
                    ListItemTopic(
                        MDListItemHeadlineText(
                            text=topic["name"]
                        ),
                        MDListItemSupportingText(
                            text=topic["details"]
                        ),
                        screen_object=self,
                        id_topic=topic["id"],
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        size_hint_x=0.9,
                        theme_bg_color="Custom",
                        md_bg_color=[0.1, 0.1, 0.1, 0.1]
                        
                    ),
                
                )

    
    

    def on_pre_leave(self):
        self.ids.id_scroll.clear_widgets()
        
        for r in self.list_swiper:
            self.ids.id_swiper_course.remove_widget(r)

    def change_screen(self, number):
        self.ids.id_screen_manager.current = number



class ListItemTopic(MDListItem):
    screen_object = ObjectProperty()
    id_topic = NumericProperty()

    def change_screen(self, *args):
        self.screen_object.manager.select_topic = self.id_topic
        self.screen_object.manager.current = "topic_name"



# lembrete: par buttonbehavior funcionar, ele tem que ser o primeiro a ser herdado
# ao inves do mdswiperitem por exemplo
class CardSwiper(ButtonBehavior, MDSwiperItem):
    id_course = NumericProperty()
    img_url = StringProperty()
    title = StringProperty()
    screen_object = ObjectProperty()

    def change_screen(self, screen_name, *args):
        self.screen_object.manager.select_course = self.id_course
        self.screen_object.manager.current = screen_name


class ConfigItemLogout(MDListItem):
    screen_object = ObjectProperty()

    def do_logout(self, *args):
        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')

        if store.exists('login_auth'):
            store.put('login_auth', access=False)

        if store.exists('user'):
            store.put('user', id=None)


        self.screen_object.manager.current = "login_name"
    
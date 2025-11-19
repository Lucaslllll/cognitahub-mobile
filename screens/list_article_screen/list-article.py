from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar


from kaki.app import App

from components.connection.connector import Connector




class ListArticle(MDScreen):
    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)
    
    def on_start(self, *args):
        self.ids.id_scroll_article.clear_widgets()
        
        self.list_swiper = []

        id_course = self.manager.select_course
        
        articles = Connector(name_url="user/course/{}/articles".format(id_course), tag="List Articles By Course")
        articles = articles.get()


        if type(articles) is list:
            
            for article in articles:

                self.ids.id_scroll_article.add_widget(
                    ListItemCustom(
                        MDListItemHeadlineText(
                            text=article["title"],
                            markup=False
                        ),
                        MDListItemSupportingText(text=article["preview"] if article["preview"] != None else "No Preview", markup=False),
                        screen_object=self,
                        id_article=article["idArticles"],
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        size_hint_x=0.9,
                        theme_bg_color="Custom",
                        md_bg_color=[0.1, 0.1, 0.1, 0.1]
                        
                    ),
                
                )



    def change_screen(self, name):
        self.manager.current = "core_name"



class ListItemCustom(MDListItem):
    id_article = NumericProperty()
    screen_object = ObjectProperty()

    def change_screen(self, screen_name, *args):
        self.screen_object.manager.select_article = self.id_article
        self.screen_object.manager.current = screen_name

    
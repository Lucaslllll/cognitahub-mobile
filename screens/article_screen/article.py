from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar


from kaki.app import App

from components.connection.connector import Connector




class Article(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_of_members_chips = []
        self.list_of_members_swiper = []
        self.user_to_chat = None
        
        self.title_example = "example title"
        self.text_example = """Lorem Ipsum é simplesmente uma simulação de texto 
        da indústria tipográfica e de impressos, e vem sendo utilizado desde o 
        século XVI, quando um impressor desconhecido pegou uma bandeja de tipos 
        e os embaralhou para fazer um livro de modelos de tipos. Lorem Ipsum 
        sobreviveu não só a cinco séculos, como também ao salto para a editoração
        eletrônica, permanecendo essencialmente inalterado. Se popularizou na 
        década de 60, quando a Letraset lançou decalques contendo passagens de 
        Lorem Ipsum, e mais recentemente quando passou a ser integrado a softwares
        de editoração eletrônica como Aldus PageMaker."""

    def on_pre_enter(self):
        self.start_content()

    def start_content(self):
        id_article = self.manager.select_article
        print(id_article)

        articles = Connector(name_url="user/course/article/{}".format(id_article), tag="Courses List")
        articles = articles.get()

        

        if type(articles) is dict:
            
            self.ids.title_article.text = articles["title"]
            self.ids.details_article.text = articles["details"]
            
         
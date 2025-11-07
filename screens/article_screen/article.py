from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.fitimage import FitImage

from kaki.app import App
import re
import webbrowser

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
        self.ids.categories_article.clear_widgets()

        article = Connector(name_url="user/course/article/{}".format(id_article), tag="Courses List")
        article = article.get()


        if type(article) is dict:

            self.ids.title_article.text = article["title"]
            self.ids.details_article.text = article["details"]
            self.ids.date_article.text = "Posted: "+article["date"]

            self.ids.categories_article.add_widget(MDLabel(text=article["course"]["name"]))
            

    def go_profile(self, *args):
        webbrowser.open("https://github.com/Lucaslllll")



class MDInteractiveLabel(MDBoxLayout):
    text = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing="8dp", adaptive_height=True, **kwargs)
        self.bind(text=self.on_text)

    def on_text(self, instance, value):
        # faz o conteúdo e calcula altura denov
        self.clear_widgets()

        parts = re.split(r'(\[img=.*?\])', value)
        for part in parts:
            if not part.strip():
                continue

            if part.startswith("[img=") and part.endswith("]"):
                url = part[5:-1]
                
                self.add_widget(
                    FitImage(
                        source=url,
                        size_hint_y=None,
                        height="200dp"
                        
                    )
                )

            else:
                lbl = MDLabel(
                    text=part.strip(),
                    halign="justify",
                    markup=True,
                    size_hint_y=None,
                    text_size=(self.width, None),
                )
                lbl.bind(
                    texture_size=lambda inst, val: setattr(inst, "height", val[1] + 10)
                )
                self.add_widget(lbl)

        #Atualizand altura total do componente
        self.update_height()

    def update_height(self, *args):
        #Força o layout a se ajustar ao conteúdo

        self.height = sum(
            (child.height if hasattr(child, "height") else 0)
            for child in self.children
        ) + (len(self.children) - 1) * self.spacing


 
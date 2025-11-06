from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout


from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)

from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField

from kaki.app import App
import re

from components.connection.connector import Connector




class Topic(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
        Clock.schedule_once(self.on_start, 1)

    def on_start(self, *args):
        topics = Connector(name_url="topic/messages/{}".format(1), tag="List Mesages Topic")
        topics = topics.get()

        if type(topics) is list:
            
            for topic in topics:
                self.ids.id_answers.add_widget(
                    MessageReply(
                        title_reply=topic["name"],
                        text_reply=topic["details"],
                        author_reply=topic["userDTO"]["name"],
                    )

                )

    
    def show_to_comment(self):
        layout = BoxLayout(
            orientation="vertical",
            spacing="20dp",
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))
        layout.add_widget(MDTextField(multiline=True))
        layout.add_widget(Widget(size_hint_y=None, height="100dp"))
        scrollview = ScrollView()
        scrollview.add_widget(layout)
        
        self.dialog = MDDialog(
            MDDialogIcon(
                icon="comment",
            ),
            MDDialogHeadlineText(
                text="Comment in this topic",
            ),
            MDDialogContentContainer(
                MDDivider(),
                MDBoxLayout(
                    scrollview,
                    orientation="vertical",
                    size_hint_y=None,
                    height="200dp",
                    padding="5dp"
                    
                ),
                MDDivider(),
                orientation="vertical",
                size_hint_y=None,
                height=layout.minimum_height,
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Reply"),
                    style="text",
                    on_release=self.create_topic_message,
                ),
                spacing="8dp",
            ),
            
        ).open()

    def create_topic_message(self, *args):
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
                    MDSnackbarSupportingText(
                        text="and close buttons at the bottom",
                        padding=[0, 0, 0, dp(56)],
                    ),
                    MDSnackbarButtonContainer(
                        Widget(),
                        MDSnackbarActionButton(
                            MDSnackbarActionButtonText(
                                text="Action button"
                            ),
                        ),
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
        

    def close_dialog(self, *args):
        print(args[0])
        args[0].dismiss()





class MessageReply(BoxLayout):
    title_reply = StringProperty()
    text_reply = StringProperty()
    author_reply = StringProperty()
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
from kivymd.uix.snackbar.snackbar import MDSnackbar, MDSnackbarActionButton, MDSnackbarActionButtonText
from kivymd.uix.snackbar.snackbar import MDSnackbarButtonContainer, MDSnackbarSupportingText, MDSnackbarCloseButton, MDSnackbarText


from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

from kaki.app import App
import re
from datetime import date
from kivy.metrics import dp

from components.connection.connector import Connector




class Topic(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.title_example = ""
        self.text_example = ""

    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)

    def on_start(self, *args):
        self.select_topic = self.manager.select_topic

        topic = Connector(name_url="topic/{}".format(self.select_topic), tag="Get The Topic")
        topic = topic.get()

        if type(topic) is dict:
            self.ids.name_topic.text = topic["name"]
            self.ids.details_topic.text = topic["details"]

        self.load_messages_topic()

    def load_messages_topic(self, *args):
        self.ids.id_answers.clear_widgets()

        messagesT = Connector(name_url="topic/messages/{}".format(self.select_topic), tag="List Mesages Topic")
        messagesT = messagesT.get()

        if type(messagesT) is list:
            
            for message in messagesT:
                self.ids.id_answers.add_widget(
                    MessageReply(
                        title_reply=message["name"],
                        text_reply=message["details"],
                        author_reply=message["userDTO"]["name"],
                    )

                )

    
    def show_to_comment(self):
        layout = BoxLayout(
            orientation="vertical",
            spacing="20dp",
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))
        layout.add_widget(Widget())
        layout.add_widget( MDTextFieldHintText(text="Say something") )

        text_field_title = MDTextField(id="title_reply", mode="filled")
        layout.add_widget( text_field_title )

        layout.add_widget( MDTextFieldHintText(text="Describe"))
        
        text_field_details = MDTextField( id="details_reply", multiline=True, size_hint_y=None, height="180dp",mode="filled")
        layout.add_widget(
            text_field_details
        )
        
        self.ids["title_reply"] = text_field_title
        self.ids["details_reply"] = text_field_details

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
            
        )
        self.dialog.open()

    def create_topic_message(self, *args):
        
        data = {
            "name": self.ids.title_reply.text,
            "details": self.ids.details_reply.text,
            "date": date.today().isoformat(),
            "author": self.manager.user_id,
            "topicId": self.select_topic,
        }

        messageTopic = Connector(name_url="topic/message/create", tag="CREATE A MESSAGE TO TOPIC")
        messageTopic = messageTopic.post(data=data)

        if type(messageTopic) is dict:
            MDSnackbar(
                MDSnackbarText(
                    text="Answer Posted",
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

            self.dialog.dismiss()
            Clock.schedule_once(self.load_messages_topic, 2)

    def change_screen(self, *args):
        self.manager.current = "core_name"
        

    def close_dialog(self, *args):
        print(args[0])
        args[0].dismiss()
    
    def on_pre_leave(self):
        self.ids.id_answers.clear_widgets()
        self.title_example = ""
        self.text_example = ""





class MessageReply(BoxLayout):
    title_reply = StringProperty()
    text_reply = StringProperty()
    author_reply = StringProperty()
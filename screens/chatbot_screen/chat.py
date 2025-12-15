from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import sp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator.progressindicator import MDCircularProgressIndicator


from components.connection.connector import Connector
from components.connection.credentials import USERNAME, PASSWORD, URL




class Chat(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history_answers = [] 
        
        



    def on_pre_enter(self):
        pass


    def on_pre_leave(self, *args):
        self.ids.id_box_chat.clear_widgets()
        



    


    def send_message(self):

        text = self.ids.id_chat_keyboard.text

        if text != "":
        
            self.history_answers.append(text)

            resume = ""; count = 0
            
            for t in self.history_answers:
                if type(t) is str:
                    if count != (len(self.history_answers)-1):
                        resume += "(apenas para você se orientar) histórico " + str(count) + " : " + t + "\n"
                    else:
                        resume += "pergunta atual " + str(count) + " : " + t + "\n"
                    count += 1

             
            chatbot = Connector(name_url="user/api/chatbot", tag="ChatBot")
            chatbot = chatbot.post(data={"message": resume})

            if type(chatbot) is dict:
                self.ids.id_box_chat.add_widget(
                    MessageOtherLayout(
                        texto=chatbot["reply"]
                    )
                )

                self.ids.id_chat_keyboard.text = ""
            
            


    def change_screen(self, screen_name, *args):
        self.manager.current = screen_name









class MessageLayout(BoxLayout):
    def __init__(self, texto, **kwargs):
        super().__init__(**kwargs)
        self.text = texto
        self.add_widget(Message(text=self.text))
        


class Message(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.font_size = sp(12)

    def on_size(self, *args):
        self.text_size = (self.width - sp(10), None)



    def on_texture_size(self, *args):
        self.size = self.texture_size
        self.height += sp(20)
        


class MessageOtherLayout(BoxLayout):
    def __init__(self, texto, **kwargs):
        super().__init__(**kwargs)
        self.text = texto
        self.add_widget(MessageOther(text=self.text))
        


class MessageOther(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.font_size = sp(12)

    def on_size(self, *args):
        self.text_size = (self.width - sp(10), None)

    def on_texture_size(self, *args):
        self.size = self.texture_size
        self.height += sp(20)
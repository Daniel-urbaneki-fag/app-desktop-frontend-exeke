import requests
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

def enviaSolicitacao(api, dados):
    box = BoxLayout(orientation="vertical")
    try:
        response = requests.post(url=api, data=dados)
        response = json.loads(response.content.decode())
    except:
        msg = Label(text="Erro na conexão !")
        pop = Popup(title="", content=box, size_hint=(None, None), separator_height=0, background="",
        size=(300, 60), pos_hint={"top": 0.97}, background_color=(220/255, 53/255, 69/255, 1))
    else:
        msg = Label(text=response["msg"])
        pop = Popup(title="", content=box, size_hint=(None, None), separator_height=0, background="",
        size=(300, 60), pos_hint={"top": 0.97}, background_color=response["color_msg"])
    box.add_widget(msg)
    
    pop.open()
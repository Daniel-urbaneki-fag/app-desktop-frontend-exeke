from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import requests
import json

Builder.load_file('screens/telaPrincipal.kv')
Builder.load_file('screens/barraAcao.kv')
Builder.load_file('screens/barraLateral.kv')
Builder.load_file('screens/telaCadastro.kv')
Builder.load_file('screens/telaCadastroUsuario.kv')

class TelaPrincipal(BoxLayout):
    pass

class TelaCadastro(Screen):
    def cadastrarDados(self):
        api = "http://127.0.0.1:5000/cadastrarEmpresa"

        if self.ids["cnpj"].text == "":
            box = BoxLayout(orientation="vertical")
            msg = Label(text="Cnpj vazio!")
            box.add_widget(msg)
            pop = Popup(title="", content=box, size_hint=(None, None), separator_height=0, background="",
            size=(300, 60), pos_hint={"top": 0.97}, background_color=(220/255, 53/255, 69/255, 1))
            pop.open()
            return
        dados_empresa = {
            'cnpj': self.ids['cnpj'].text,
            'razaoSocial': self.ids['razaoSocial'].text,
            'fantasia': self.ids['fantasia'].text,
            'telefone': self.ids['telefone'].text,
            'e-mail': self.ids['e-mail'].text,
            'cep': self.ids['cep'].text,
            'logradouro': self.ids['logradouro'].text,
            'bairro': self.ids['bairro'].text,
            'numero': self.ids['numero'].text,
            'cidade': self.ids['cidade'].text,
            'tipo': self.ids['tipo'].text,
            'matriz': self.ids['matriz'].text
        }
        response = requests.post(url=api, data=dados_empresa)
        response = json.loads(response.content.decode())
        box = BoxLayout(orientation="vertical")
        msg = Label(text=response["msg"])
        box.add_widget(msg)
        pop = Popup(title="", content=box, size_hint=(None, None), separator_height=0, background="",
            size=(300, 60), pos_hint={"top": 0.97}, background_color=response["color_msg"])
        pop.open()

class TelaCadastroUsuario(Screen):
    pass

class BarraLateral(BoxLayout):
    def mudaTela(self):
        for child in self.children:
            for item in child.children:
                print(item)
            if type(child) == MenuScreen:
                child.current = "TelaCadastroUsuario"

class BarraAcao(BoxLayout):
    pass

class MenuScreen(ScreenManager):
    pass
    
class ExekeApp(App):
    def build(self):
        Window.size = (1366, 768)
        self.icon = ('screens/icone.png')
        tela = TelaPrincipal()
        tela.add_widget(BarraAcao())
        main = BoxLayout()
        main.add_widget(BarraLateral())
        screenManager = MenuScreen()
        screenManager.add_widget(TelaCadastro(name="TelaCadastroEmpresa"))
        screenManager.add_widget(TelaCadastroUsuario(name="TelaCadastroUsuario"))
        main.add_widget(screenManager)
        tela.add_widget(main)
        return tela
    
if __name__ == '__main__':
    ExekeApp().run()
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from utils import enviaSolicitacao, pegaDados, pegaDadosPost

Builder.load_file('screens/base.kv')
Builder.load_file('screens/customs.kv')
Builder.load_file('screens/barraAcao.kv')
Builder.load_file('screens/barraLateral.kv')
Builder.load_file('screens/telaCadastroEmpresa.kv')
Builder.load_file('screens/telaCadastroUsuario.kv')
Builder.load_file('screens/telaUsuarios.kv')
Builder.load_file('screens/telaEmpresas.kv')

class MenuScreen(ScreenManager):
    pass

class Base(BoxLayout):
    pass

class CustomDropDown(DropDown):
    pass

class BarraAcao(BoxLayout):
    pass

class InputCpf(TextInput):
    def insert_text(self, substring, from_undo=False):
        try:
            int(substring)
            if len(substring) == 1:
                if len(self.text) < 14:
                    if len(self.text) == 3 or len(self.text) == 7:
                        self.text += "."
                    if len(self.text) == 11:
                        self.text += "-"
                    return super().insert_text(substring, from_undo=from_undo)
            else:
                if len(self.text) == 0:
                    filter = ""
                    for i in range(len(substring)):
                        filter = filter + substring[i]
                        if i == 2 or i == 5:
                            filter = filter + "."
                        elif i == 8:
                            filter = filter + "-"
                    return super().insert_text(filter, from_undo=from_undo)
        except ValueError as error:
            if len(substring) == 14:
                return super().insert_text(substring, from_undo=from_undo)

class InputCnpj(TextInput):
    def insert_text(self, substring, from_undo=False):
        try:
            int(substring)
            if len(substring) == 1:
                if len(self.text) < 18:
                    if(len(self.text) == 1 or len(self.text) == 5):
                        substring += "."
                    if(len(self.text) == 9):
                        substring += "/"
                    if(len(self.text) == 14):
                        substring += "-"
                    return super().insert_text(substring, from_undo=from_undo)
            else:
                if len(self.text) == 0:
                    filter = ""
                    for i in range(len(substring)):
                        filter = filter + substring[i]
                        if i == 1 or i == 4:
                            filter = filter + "."
                        elif i == 7:
                            filter = filter + "/"
                        elif i == 11:
                            filter = filter + "-"
                    return super().insert_text(filter, from_undo=from_undo)
        except ValueError as error:
            if len(substring) == 18:
                return super().insert_text(substring, from_undo=from_undo)

screenManager = ScreenManager(transition=NoTransition())

class BarraLateral(BoxLayout):
    def mudaTela(self, tela):
        screenManager.current = tela

class TelaEmpresas(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.lerTabelaEmpresas()
    
    def lerTabelaEmpresas(self):
        api = "http://127.0.0.1:5000/lerTabelaEmpresas"
        self.response = pegaDados(api)
        if self.response:
            for usuario in self.response:
                box = BoxLayout(size_hint=(1, None),  height=40)
                box.add_widget(Label(text=str(usuario["id"]), font_size="16sp", text_size=(self.width + 88, None)))
                box.add_widget(Label(text=str(usuario["razaoSocial"]), font_size="16sp", text_size=(self.width + 88, None)))
                box.add_widget(Label(text=str(usuario["cnpj"]), font_size="16sp", text_size=(self.width + 88, None)))
                editar = Button(text="Editar", ids={"id" : str(usuario["id"])})
                # editar.bind(on_press=self.editarUsuario)
                box.add_widget(editar)
                self.ids['tabela'].add_widget(box)

class TelaUsuarios(Screen):
    response = []

    def __init__(self, **kw):
        super().__init__(**kw)
        self.lerTabelaUsuarios()
    
    def editarUsuario(self, value):
        self.clear_widgets()
        telaEditar = TelaCadastroUsuario()
        telaEditar.ids["textoTela"].text = "Editar Usu??rio"

        api = "http://127.0.0.1:5000/lerDadosUsuario"
        response = pegaDadosPost(api, {"id" : value.ids["id"]})
        if response:
            response = response[0]
            # telaEditar.ids['tipo'].text = str(response["tipo"])
            telaEditar.ids['empresa'].text = response["empresa"]
            telaEditar.ids['nome'].text = response["nome"]
            telaEditar.ids['cpf'].text = str(response["cpf"])
            telaEditar.ids['telefone'].text = response["telefone"]
            telaEditar.ids['cep'].text = response["cep"]
            telaEditar.ids['logradouro'].text = response["logradouro"]
            telaEditar.ids['bairro'].text = response["bairro"]
            telaEditar.ids['numero'].text = response["numero"]
            telaEditar.ids['complemento'].text = response["complemento"]
            telaEditar.ids['cidade'].text = response["cidade"]
            telaEditar.ids['estado'].text = response["estado"]
            telaEditar.ids['email'].text = response["email"]
        self.add_widget(telaEditar)

    def lerTabelaUsuarios(self):
        api = "http://127.0.0.1:5000/lerTabelaUsuarios"
        self.response = pegaDados(api)
        if self.response:
            for usuario in self.response:
                box = BoxLayout(size_hint=(1, None),  height=40)
                box.add_widget(Label(text=str(usuario["id"]), font_size="16sp", text_size=(self.width + 88, None)))
                box.add_widget(Label(text=str(usuario["nome"]), font_size="16sp", text_size=(self.width + 88, None)))
                box.add_widget(Label(text=str(usuario["email"]), font_size="16sp", text_size=(self.width + 88, None)))
                box.add_widget(Label(text=str(usuario["empresa"]), font_size="16sp", text_size=(self.width + 88, None)))
                box.add_widget(Label(text=str(usuario["telefone"]), font_size="16sp", text_size=(self.width + 88, None)))
                editar = Button(text="Editar", ids={"id" : str(usuario["id"])})
                editar.bind(on_press=self.editarUsuario)
                box.add_widget(editar)
                self.ids['tabela'].add_widget(box)


class TelaCadastroEmpresa(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        inputCnpj = InputCnpj()
        self.ids['cnpj'] = inputCnpj
        self.ids['idCnpj'].add_widget(inputCnpj)

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
            'email': self.ids['email'].text,
            'cep': self.ids['cep'].text,
            'logradouro': self.ids['logradouro'].text,
            'bairro': self.ids['bairro'].text,
            'numero': self.ids['numero'].text,
            'cidade': self.ids['cidade'].text,
            'tipo': self.ids['tipo'].text,
            'matriz': self.ids['matriz'].text
        }
        enviaSolicitacao(api, dados_empresa)       

class TelaCadastroUsuario(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dropdown = CustomDropDown()
        self.mainbutton = Button(text='Selecione...')
        self.mainbutton.bind(on_release= self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.ids['tipo'].add_widget(self.mainbutton)
        inputCpf = InputCpf()
        self.ids['cpf'] = inputCpf
        self.ids['idCpf'].add_widget(inputCpf)             

    def cadastrarDados(self):
        api = "http://127.0.0.1:5000/cadastroUsuario"

        if self.ids['tipo'].children[0].text == "Selecione...":
            box = BoxLayout(orientation="vertical")
            msg = Label(text="Insira o tipo de usu??rio - Adm / Gestor / Representante!")
            box.add_widget(msg)
            pop = Popup(title="", content=box, size_hint=(None, None), separator_height=0, background="",
            size=(400, 50), pos_hint={"top": 0.97}, background_color=(220/255, 53/255, 69/255, 1))
            pop.open()
            return
        
        tipo = 0
        if self.ids['tipo'].children[0].text == "Administrador":
            tipo = 1
        elif self.ids['tipo'].children[0].text == "Gestor":
            tipo = 2
        
        if self.ids['senha'].text != "":
            if self.ids['confirmarSenha'].text != self.ids['senha'].text:
                box = BoxLayout(orientation="vertical")
                msg = Label(text="Senha e confirma????o de senha, n??o conferem!")
                box.add_widget(msg)
                pop = Popup(title="", content=box, size_hint=(None, None), separator_height=0, background="",
                size=(400, 50), pos_hint={"top": 0.97}, background_color=(220/255, 53/255, 69/255, 1))
                pop.open()
                return
        else:
            box = BoxLayout(orientation="vertical")
            msg = Label(text="Digite uma senha!")
            box.add_widget(msg)
            pop = Popup(title="", content=box, size_hint=(None, None), separator_height=0, background="",
            size=(400, 50), pos_hint={"top": 0.97}, background_color=(220/255, 53/255, 69/255, 1))
            pop.open()
            return

        dados_usuario = {
            'tipo': tipo,
            'empresa': self.ids['empresa'].text,
            'nome': self.ids['nome'].text,
            'cpf': self.ids['cpf'].text,
            'telefone': self.ids['telefone'].text,
            'cep': self.ids['cep'].text,
            'logradouro': self.ids['logradouro'].text,
            'bairro': self.ids['bairro'].text,
            'numero': self.ids['numero'].text,
            'complemento': self.ids['complemento'].text,
            'cidade': self.ids['cidade'].text,
            'estado': self.ids['estado'].text,
            'email': self.ids['email'].text,
            'senha': self.ids['senha'].text,
        }
        enviaSolicitacao(api, dados_usuario)

class ExekeApp(App):
    def build(self):
        Window.size = (1366, 768)
        self.icon = ('icone.png')
        self.title = "Exeke Vista"
        tela = Base()
        tela.add_widget(BarraAcao())
        main = BoxLayout()
        main.add_widget(BarraLateral())
        screenManager.add_widget(TelaEmpresas(name="TelaEmpresas"))
        screenManager.add_widget(TelaUsuarios(name="TelaUsuarios"))
        screenManager.add_widget(TelaCadastroEmpresa(name="TelaCadastroEmpresa"))
        screenManager.add_widget(TelaCadastroUsuario(name="TelaCadastroUsuario"))
        main.add_widget(screenManager)
        tela.add_widget(main)
        return tela
    
if __name__ == '__main__':
    ExekeApp().run()
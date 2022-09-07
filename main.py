# from kivy.config import Config
# Config.set('graphics', 'width', '720')
# Config.set('graphics', 'height', '650')
from cgi import test
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Builder.load_file('screens/cadastroEmpresa.kv')

class Login(ScrollView):
    def __init__(self, **kwargs): 
        super(Login, self).__init__(**kwargs)
        Window.softinput_mode = "below_target"
    
    def teste(self):
        print(self.ids['usuario'].text)

class CadastroEmpresa(BoxLayout):
    pass
    
class ExekeApp(App):
    def build(self):
        # Window.size = (720, 1440)
        return CadastroEmpresa()
    
if __name__ == '__main__':
    ExekeApp().run()
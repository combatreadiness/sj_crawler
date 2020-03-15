import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

kivy.require('1.11.1')


class inputLayout(GridLayout):
    pass

class KivyApp(App):
    def build(self):
        return inputLayout()

if __name__ == '__main__':
    KivyApp().run()

# File name: widgets.py
from kivy.app import App
from kivy.uix.widget import Widget


class MyWidget(Widget):
    pass


class WidgetApp(App):
    def budil(self):
        return MyWidget()


if __name__ == "__main__":
    WidgetApp().run()
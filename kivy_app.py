import threading
import time

from crawler import Crawler
import webbrowser

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.chip import MDChip
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.snackbar import Snackbar

from queue import Queue


class SearchPage(Screen):
    pass


class ResultPage(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MyListItem(TwoLineListItem):
    def setLink(self, link):
        self.link= link

    def move_to_link(self):
        webbrowser.open_new_tab(self.link)
    pass


class KivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stop_event = threading.Event()
        self.search_list = []
        self.keywords = []
        self.cr = Crawler()
        self.news_list = {}
        self.uploaded_news_list = {}
        self.news_queue = Queue()
        self.sb = None
        self.news_event = None

    def on_start(self):
        self.showPressList()

    def showPressList(self):
        press_list = self.cr.getListOfPress()
        for name in press_list:
            self.root.ids.SearchPage.ids.pressList.add_widget(
                MDChip(
                    label=f"{name}",
                    icon=f"alpha-{name.lower()[0]}-circle-outline",
                    check="True",
                    callback=self.selectPress,
                    color=[0, 0, 0, 0.3]
                )
            )

    def selectPress(self, name_chip, name):
        if len(name_chip.ids.box_check.children):
            self.search_list.append(name)
            name_chip.color = self.theme_cls.primary_color
        else:
            self.search_list.remove(name)
            name_chip.color = [0, 0, 0, 0.3]
        pass

    def runResultPage(self):
        self.keywords = (self.root.ids.SearchPage.ids.textField.text.replace(" ", "").split(','))
        self.uploaded_news_list = {}

        if len(self.keywords[0]) == 0:
            self.snackbar_show("Please Type Keywords")
            return
        if len(self.search_list) == 0:
            self.snackbar_show("Please Select at least one press")
            return
        print(self.keywords, " and ", self.search_list)
        self.root.ids.WM.current = "result"
        self.showNewsListThread()
        self.getNewsListThread()

    def snackbar_show(self, msg):
        if not self.sb:
            self.sb = Snackbar(text=msg)
            self.sb.show()
            anim = Animation(y=dp(72), d=.2)
            self.sb = None

    def showNewsListThread(self):
        Clock.schedule_once(self.showNewsList, 0)
        self.news_event = Clock.schedule_interval(self.showNewsList, 5)

    def showNewsList(self, dt):
        while self.news_queue.qsize():
            result = self.news_queue.get_nowait()
            for k, v in result.items():
                if k not in self.uploaded_news_list.keys():
                    m = MyListItem(text=k, secondary_text=v[0])
                    m.setLink(v[1])
                    self.root.ids.ResultPage.ids.NewsList.add_widget(m)
                    self.uploaded_news_list[k] = [v[0]]

    def getNewsListThread(self):
        for press in self.search_list:
            t = threading.Thread(target=self.getNews, args=(press,5))
            t.daemon = True
            t.start()

    def getNews(self, press, seconds):
        while True:
            self.news_queue.put(self.cr.findMyNews(press, self.keywords))
            if self.stop_event.isSet():
                break
            time.sleep(seconds)

    def clearThreads(self):
        self.root.ids.ResultPage.ids.NewsList.clear_widgets()
        self.stop_event.set()
        self.news_event.cancel()

    def on_stop(self):
        print("Exit")


if __name__ == '__main__':
    KivyApp().run()

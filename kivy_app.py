import logging
import threading

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


class KivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_list = []
        self.keywords = []
        self.cr = Crawler()
        self.news_list = {}
        self.uploaded_news_list = {}
        self.news_queue = Queue()
        self.snackbar = None
        self._interval = 0
        self.crawlerThread = None



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

    # def findNews(self):  #start Second Thread
    #    Thread(target=self.showNewsListThread).start()

    def runResultPage(self):
        print("here111")
        self.keywords = (self.root.ids.SearchPage.ids.textField.text.replace(" ", "").split(','))
        if len(self.keywords[0]) == 0:
            print("no keywords")
            self.snackbar_show("Please Type Keywords")
            return
        if len(self.search_list) == 0:
            print("no press selected")
            self.snackbar_show("Please Select at least one press")
            return

        self.root.ids.WM.current = "result"
        self.showNewsListThread()
        self.getNewsListThread()



    def snackbar_show(self, msg):
        if not self.snackbar:
            self.snackbar = Snackbar(text=msg)
            self.snackbar.show()
            anim = Animation(y= dp(72), d=.2)
            self.snackbar = None



    def showNewsListThread(self):
        Clock.schedule_once(self.showNewsList, 0)
        Clock.schedule_interval(self.showNewsList, 5)

    def showNewsList(self, dt):
        while self.news_queue.qsize():
            result = self.news_queue.get_nowait()
            for k, v in result.items():
                if k not in self.uploaded_news_list.keys():
                    self.root.ids.ResultPage.ids.NewsList.add_widget(
                        TwoLineListItem(
                            text=k,
                            secondary_text=v[0]
                        )
                    )
                    self.uploaded_news_list[k] = [v[0]]




    def getNewsListThread(self):
        self.crawlerThread = threading.Timer(0, self.getNews)
        self.crawlerThread.start()

    def getNews(self):
        for press in self.search_list:
            self.news_queue.put(self.cr.findMyNews(press, self.keywords))
        self.crawlerThread = threading.Timer(10, self.getNews)
        self.crawlerThread.daemon = True
        self.crawlerThread.start()

    def on_stop(self):
        print("Exit")


if __name__ == '__main__':
    KivyApp().run()

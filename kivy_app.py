from crawler import Crawler
from kivymd.app import MDApp
from kivymd.uix.chip import MDChip
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineListItem
import asyncio


class SearchPage(Screen):
    pass


class ResultPage(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class KivyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cr = Crawler()
        self.search_list = []

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
        print(self.search_list)
        pass

    def findNews(self):
        loop = asyncio.get_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.getNews())  # main이 끝날 때까지 기다림
        print("hi")
        loop.close()


    async def getNews(self):
        final_list = {}
        keywords = (self.root.ids.SearchPage.ids.textField.text.replace(" ", "").split(','))
        print(keywords)
        futures = [asyncio.ensure_future(self.cr.findMyNews(press, keywords)) for press in self.search_list]
        result = await asyncio.gather(*futures)
        print(result)
        #for press in self.search_list:
        #    final_list.update(self.cr.findMyNews(press, keywords))
        #for k, v in final_list.items():
        #    print(v[0], ":", k)


if __name__ == '__main__':
    KivyApp().run()

import model
import logging
import json
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

"""
Author: Charles Herrmann
Date: 12/2/2020
Description: GUI for Census2xlsx application
"""

# logging.basicConfig(filename='c2x.log', filemode='w', level=logging.INFO)
# logger = logging.getLogger('view')

"""
class TestApp(App):
    def build(self):
        sm = ScreenManager()

        # Add few screens
        for i in range(4):
            screen = Screen(name='Title %d' % i)
            sm.add_widget(screen)
        
        return sm


def main():
    logger.info("Started from view.py")
    TestApp().run()
"""


class MainWindow(Screen):
    pass


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("mymain.kv")


class MyMainApp(App):
    def build(self):
        return kv


def main():
    MyMainApp().run()


if __name__ == "__main__":
    main()

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.layout import Layout


class Interface(App):
    def build(self):
        return Button(text='Button')


if __name__ == '__main__':
    app = Interface().run()
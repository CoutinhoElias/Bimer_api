import flet as ft

class MyAppBar(ft.AppBar):
    
    def __init__(self, text, bg_color):
        super().__init__()
        self.bgcolor = bg_color
        self.title = ft.Text(text)
import flet as ft

class MyButton(ft.ElevatedButton):
    
    def __init__(self, text, on_click):
        super().__init__()
        self.bgcolor = ft.colors.ORANGE_300
        self.color = ft.colors.WHITE
        self.text = text
        self.on_click = on_click
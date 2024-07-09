# import datetime
import flet as ft

class MyDatePicker:
    def __init__(self, first_date, last_date, on_change, on_dismiss):
        self.first_date = first_date
        self.last_date = last_date
        self.on_change = on_change
        self.on_dismiss = on_dismiss

    def open(self, page):
        page.open(
            ft.DatePicker(
                first_date=self.first_date,
                last_date=self.last_date,
                on_change=self.on_change,
                on_dismiss=self.on_dismiss,
                
            )
        )

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


# import flet as ft

# class MyDatePicker:
#     def __init__(self, page, first_date, last_date):
#         self.page = page
#         self.first_date = first_date
#         self.last_date = last_date

#     def handle_change(self, e):
#         self.page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}"))

#     def handle_dismissal(self, e):
#         self.page.add(ft.Text(f"DatePicker dismissed"))

#     def open(self):
#         self.page.open(
#             ft.DatePicker(
#                 first_date=self.first_date,
#                 last_date=self.last_date,
#                 on_change=self.handle_change,
#                 on_dismiss=self.handle_dismissal,
#             )
#         )
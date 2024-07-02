import flet as ft
from partials.button import MyButton

class StoreView:
    def get_content(self):
        def cancel_clicked(e):
            print("Cancel clicked")

        button = MyButton(text="Cancel", on_click=cancel_clicked)
        items = [ft.Text(value=f"Item {i}", color=ft.colors.WHITE) for i in range(1, 6)]
        
        # Coluna
        # layout = ft.Column(
            
        #     controls=[
        #         *items,
        #         button
        #     ],
        #     alignment=ft.alignment.center,
        #     expand=True
        # )
        # Responsive Row
        
        rr_layout = ft.ResponsiveRow(
            columns=12,
            controls=[
                *items,
                button
            ],
            expand=True
        )


        return rr_layout

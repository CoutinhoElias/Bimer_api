import flet as ft

class MyNavigationDrawer(ft.NavigationDrawer):

    def __init__(self, on_change):
        super().__init__()  # Chamar o construtor da classe base

        self.selected_index = 0  # Corrigir a sintaxe aqui, removendo a vírgula
        self.on_change=on_change

        self.controls = [
            ft.Container(height=12),  # Ajuda a manter a distancia dos menus na vertical

            ft.Image(
                src="C:\\Users\\SV\\Desktop\\SV-2.png",
                width=200,
                height=200,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            ),

            # Botões de navegação
            ft.NavigationDrawerDestination(
                label="Home",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),

            ft.Divider(thickness=2),  # Divisor de menu.

            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Estoque",
                selected_icon=ft.icons.MAIL,
            ),

            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.DOCK_OUTLINED),
                label="Pedido de Compra",
                selected_icon=ft.icons.DOCK,
            ),

            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Tela Três",
                selected_icon=ft.icons.PHONE,
            ),            
        ]

        self.bgcolor = ft.colors.BACKGROUND

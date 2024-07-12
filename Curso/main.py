import flet as ft

# Telas e partes
from partials.navigation_drawer import MyNavigationDrawer
from partials.app_bar import MyAppBar
from views.home_view import HomeView
from views.store_view import StoreView
from views.pedido_view_local import PedidoView

# ===========================================================================================================

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.BLACK
        self.page.title = "Sistema SV em Flet"
        self.page.theme_mode = "dark"
        # self.page.theme_mode = ft.colors.BLACK
        self.page.window_center()

        page.window_width = 1465
        page.window_height = 999        

        self.page.theme = ft.Theme(page_transitions={
            'windows': ft.PageTransitionTheme.CUPERTINO
        })

        # Configuração do idioma
        self.page.locale_configuration = ft.LocaleConfiguration(
            supported_locales=[
                ft.Locale("pt", "BR"),  # Português, Brasil
                ft.Locale("de", "DE"),  # Alemão, Alemanha
                ft.Locale("fr", "FR"),  # Francês, França
                ft.Locale("es"),        # Espanhol
            ],
            current_locale=ft.Locale("pt", "BR"),  # Define o idioma inicial como Português do Brasil
        )

        self.setup_navigation()
        # current_locale = App.locale_service.get_locale()
        self.page.update()

    def setup_navigation(self):
        def indicador_de_tela(e):
            menu_selecionado = e.control.selected_index
            match menu_selecionado:
                case 0:
                    self.page.go("/")
                case 1:
                    self.page.go("/store")
                case 2:
                    self.page.go("/pedido")                    
                case _:
                    self.page.go("/")

        self.page.drawer = MyNavigationDrawer(on_change=indicador_de_tela)

        def route_change(event):
            route = event.route
            print(f"Route changed to: {route}")
            self.page.views.clear()

            match route:
                case "/":
                    view = HomeView().get_content()
                    app_bar_title = "Pagina Principal"
                    app_bar_color = ft.colors.GREY_800
                case "/store":
                    view = StoreView().get_content()
                    app_bar_title = "Store"
                    app_bar_color = ft.colors.GREY_800
                case "/pedido":
                    view = PedidoView(self.page).get_content()
                    app_bar_title = "Pedido de Compra"  
                    app_bar_color = ft.colors.GREY_800                  
                case _:
                    view = HomeView().get_content()
                    app_bar_title = "Pagina Principal"
                    app_bar_color = ft.colors.GREY_800

            self.page.views.append(
                ft.View(
                    route,
                    [
                        self.page.drawer,
                        MyAppBar(app_bar_title, app_bar_color),
                        view
                    ]
                )
            )
            self.page.update()

        self.page.on_route_change = route_change
        self.page.go("/pedido")  # Define the initial route

if __name__ == '__main__':
    ft.app(target=App, assets_dir='assets')

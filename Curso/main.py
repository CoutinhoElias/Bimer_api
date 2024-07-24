import flet as ft

# Importação de componentes customizados e views
from partials.navigation_drawer import MyNavigationDrawer
from partials.app_bar import MyAppBar
from views.home_view import HomeView
from views.store_view import StoreView
from views.pedido_view_local import PedidoView

class App:
    def __init__(self, page: ft.Page):
        """Inicializa a aplicação com a configuração da página e navegação"""
        self.page = page
        
        # Configurações da página
        self.page.bgcolor = ft.colors.BLACK
        self.page.title = "Sistema SV em Flet"
        self.page.theme_mode = "dark"  # Define o tema como escuro
        self.page.window.center()  # Centraliza a janela na tela

        # Define as dimensões da janela
        page.window.width = 1465
        page.window.height = 999        

        # Define a animação de transição de páginas
        self.page.theme = ft.Theme(page_transitions={
            'windows': ft.PageTransitionTheme.CUPERTINO
        })

        # Configuração do idioma da aplicação
        self.page.locale_configuration = ft.LocaleConfiguration(
            supported_locales=[
                ft.Locale("pt", "BR"),  # Português, Brasil
                ft.Locale("de", "DE"),  # Alemão, Alemanha
                ft.Locale("fr", "FR"),  # Francês, França
                ft.Locale("es"),        # Espanhol
            ],
            current_locale=ft.Locale("pt", "BR"),  # Define o idioma inicial como Português do Brasil
        )

        self.setup_navigation()  # Configura a navegação
        self.page.update()  # Atualiza a página

    def setup_navigation(self):
        """Configura a navegação da aplicação"""
        def indicador_de_tela(e):
            """Atualiza a rota da aplicação com base no item do menu selecionado"""
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

        # Define o drawer de navegação e seu comportamento ao mudar a seleção
        self.page.drawer = MyNavigationDrawer(on_change=indicador_de_tela)

        def route_change(event):
            """Atualiza a view da aplicação com base na rota"""
            route = event.route
            print(f"Route changed to: {route}")
            self.page.views.clear()  # Limpa as views atuais

            # Define a view e a app bar com base na rota
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

            # Adiciona a nova view com a app bar e o drawer
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
            self.page.update()  # Atualiza a página

        self.page.on_route_change = route_change  # Define o callback para mudanças de rota
        self.page.go("/pedido")  # Define a rota inicial

if __name__ == '__main__':
    # Inicializa a aplicação Flet com a classe App como alvo e o diretório de assets
    ft.app(target=App, assets_dir='assets')

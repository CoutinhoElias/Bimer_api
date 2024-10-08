# Gerar apk Windows
# pip install Pillow
# flet pack .\Curso\main.py --icon .\Curso\super_volt.png --add-data .\Curso\assets:assets --hidden-import pymssql pyodbc -n "NovoApp"

# Usando pyinstaller
# pyinstaller --onefile --add-data ".\Curso\assets;assets" --hidden-import pymssql .\Curso\main.py

import flet as ft

# Importação de componentes customizados e views
from partials.navigation_drawer import MyNavigationDrawer
from partials.app_bar import MyAppBar
from views.home_view import HomeView
from views.login import Cadastrar, Login
from views.editar_pedido_compra_view_local import PedidoView
from views.criar_pedido_compra_view import PedidoNovoView
from views.criar_pedido_compra_view_local import PedidoNovoViewLocal
from views.editar_pedido_compra_view_local_um import PedidoNovoViewLocalUm

class App:
    def __init__(self, page: ft.Page):
        """Inicializa a aplicação com a configuração da página e navegação"""
        self.page = page
        
        # Para que eu possa usar essas variáveis em outras classes devo passar a instância self na chamada das outras classes.
        # Exemplo: view = PedidoNovoViewLocal(self.page, self).get_content()
        # E nas classes, no init assim: def __init__(self, page: ft.Page, app_instance):
        
        self.user_info = None  # Variável para armazenar as informações do usuário
        self.password_api = None # Variável para armazenar as informações do usuário
        self.params_api = None
        self.id_bimer = None # Variável para armazenar as informações do usuário

        # Configurações da página
        self.page.bgcolor = ft.colors.BLACK
        self.page.title = "Sistema SV em Flet v1.02"
        self.page.theme_mode = "dark"  # Define o tema como escuro
        self.page.window.center()  # Centraliza a janela na tela

        # Define as dimensões da janela
        self.tamanho_tela(999, 1465)

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

    def tamanho_tela(self, height, width):
        self.page.window.width = width
        self.page.window.height = height
        self.page.window.center()
        self.page.update

    def setup_navigation(self):
        """Configura a navegação da aplicação"""
        def indicador_de_tela(e):
            """Atualiza a rota da aplicação com base no item do menu selecionado"""
            menu_selecionado = e.control.selected_index
            match menu_selecionado:
                case 0:
                    self.page.go("/")
                    self.tamanho_tela(999, 1465)
                case 1:
                    self.page.go("editar/pedido")
                    self.tamanho_tela(999, 1465)                 
                case 2:
                    self.page.go("criar/pedido/excel/local")
                    self.tamanho_tela(999, 1465)
                case 3:
                    self.page.go("criar/pedido/excel/api")
                    self.tamanho_tela(999, 1465)
                case 4:
                    self.page.go("editar/pedido/novo")
                    self.tamanho_tela(999, 1911)
                case 5:
                    self.page.go("/login")
                    self.tamanho_tela(999, 1465)
                case 6:
                    self.page.go("/login/novo")
                    self.tamanho_tela(999, 1465)
                case _:
                    self.page.go("/")
            print(f'Selecionei {menu_selecionado}')

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
                    app_bar_title = f"Pagina Principal"
                    app_bar_color = ft.colors.GREY_800
                    include_drawer = True
                case "criar/pedido/excel/local":
                    # Se desejar coletar alguma informação da página abaixo deve enviar self como parâmetro.
                    view = PedidoNovoViewLocal(self.page, self).get_content()
                    app_bar_title = "Importar Pedido de Compra do Excel (Local)"
                    app_bar_color = ft.colors.GREY_800
                    include_drawer = True
                case "editar/pedido":
                    view = PedidoView(self.page).get_content()
                    app_bar_title = "Pedido de Compra"  
                    app_bar_color = ft.colors.GREY_800  
                    include_drawer = True
                case "editar/pedido/novo":
                    # Se desejar coletar alguma informação da página abaixo deve enviar self como parâmetro.
                    view = PedidoNovoViewLocalUm(self.page, self).get_content()
                    app_bar_title = "Edita Pedido de Compra/Jonatha"  
                    app_bar_color = ft.colors.GREY_800  
                    include_drawer = True
                case "criar/pedido/excel/api":
                    view = PedidoNovoView(self.page).get_content()
                    app_bar_title = "Importar Pedido de Compra do Excel (API)"  
                    app_bar_color = ft.colors.GREY_800  
                    include_drawer = True
                case "/login":
                    # Se desejar coletar alguma informação da página abaixo deve enviar self como parâmetro.
                    view = Login(self.page, self).get_content()
                    app_bar_title = "Login"  
                    app_bar_color = ft.colors.GREY_800  
                    include_drawer = False
                case "/login/novo":
                    view = Cadastrar(self.page).get_content()
                    app_bar_title = "Novo Login"  
                    app_bar_color = ft.colors.GREY_800 
                    include_drawer = False
                case _:
                    view = HomeView().get_content()
                    app_bar_title = "Pagina Principal"
                    app_bar_color = ft.colors.GREY_800
                    include_drawer = True

            # Adiciona a nova view com a app bar e o drawer (condicionalmente)
            new_view_content = [
                MyAppBar(app_bar_title, app_bar_color),
                view
            ]
            if include_drawer:
                new_view_content.insert(0, self.page.drawer)

            self.page.views.append(
                ft.View(
                    route,
                    new_view_content
                )
            )
            self.page.update()  # Atualiza a página

        self.page.on_route_change = route_change  # Define o callback para mudanças de rota
        self.page.go("/login")  # Define a rota inicial
        self.page.update

if __name__ == '__main__':
    # Inicializa a aplicação Flet com a classe App como alvo e o diretório de assets
    ft.app(target=App, assets_dir='assets')

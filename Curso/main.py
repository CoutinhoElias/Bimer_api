# Gerar apk Windows
# pip install Pillow
# flet pack .\Curso\main.py --icon .\Curso\super_volt.png --add-data .\Curso\assets:assets --hidden-import pymssql -n "NovoApp"

# Usando pyinstaller
# pyinstaller --onefile --add-data ".\Curso\assets;assets" --hidden-import pymssql .\Curso\main.py


import flet as ft

# Importação de componentes customizados e views
from partials.navigation_drawer import MyNavigationDrawer
from partials.app_bar import MyAppBar
from views.home_view import HomeView
from views.login import Cadastrar, Login
from views.store_view import StoreView
from views.editar_pedido_compra_view_local import PedidoView
from views.criar_pedido_compra_view import PedidoNovoView
from views.criar_pedido_compra_view_local import PedidoNovoViewLocal
from database.users_firebase import FirebaseAuth

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
                    self.page.go("/pedido")                    
                case 2:
                    self.page.go("/pedido/novo/local")
                case 3:
                    self.page.go("/pedido/novo")
                case 4:
                    self.page.go("/login")
                case 5:
                    self.page.go("/login/novo")  
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
                    app_bar_title = f"Pagina Principal"
                    app_bar_color = ft.colors.GREY_800
                    include_drawer = True
                case "/pedido/novo/local":
                    view = PedidoNovoViewLocal(self.page, self).get_content()
                    app_bar_title = "Importar Pedido de Compra do Excel (Local)"
                    app_bar_color = ft.colors.GREY_800
                    include_drawer = True
                case "/pedido":
                    view = PedidoView(self.page).get_content()
                    app_bar_title = "Pedido de Compra"  
                    app_bar_color = ft.colors.GREY_800  
                    include_drawer = True
                case "/pedido/novo":
                    view = PedidoNovoView(self.page).get_content()
                    app_bar_title = "Importar Pedido de Compra do Excel (API)"  
                    app_bar_color = ft.colors.GREY_800  
                    include_drawer = True
                case "/login":
                    # view = Login(self.page).get_content()
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

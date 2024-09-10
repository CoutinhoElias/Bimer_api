import flet as ft
from partials.button import MyButton
from views.sign_up import Cadastrar
from querys.login_json import user_credentials
from database.users_firebase import FirebaseAuth
from configs.alterdata_api_config import BimerAPIParams
import json

class Login(ft.Row):
            
    def __init__(self, page: ft.Page, app_instance):

        super().__init__()
        self.page = page  # Certifique-se de armazenar a página na instância
        self.app_instance = app_instance  # Armazena a referência para a instância da classe App
        
        self.params = BimerAPIParams

        # Definição do Ref().
        self.ref_login = ft.Ref[ft.TextField]()
        self.ref_password = ft.Ref[ft.TextField]()

        # Campo responsivo.
        self.email = ft.ResponsiveRow(
            columns=12,
            controls=[
                ft.TextField(
                    ref=self.ref_login,
                    focused_border_color=ft.colors.RED,
                    hint_text='Digite seu Login Bimer', 
                    label='Login Bimer', 
                    width=250,
                    hint_style=ft.TextStyle(
                        font_family="Arial",
                        color=ft.colors.BLACK,
                        # weight="bold"
                    ),
                    label_style=ft.TextStyle(
                        font_family="Arial",
                        color=ft.colors.BLACK,
                        # weight="bold"
                    ),
                    color=ft.colors.BLACK,
                    expand=True,
                    # value='JONATHAARAUJO'
                )
            ],
        )

        # Campo responsivo.
        self.password = ft.ResponsiveRow(
            columns=12,
            controls=[
                ft.TextField(
                    ref=self.ref_password,
                    focused_border_color=ft.colors.RED,
                    hint_text='Digite sua senha', 
                    label='Password', 
                    width=250,
                    can_reveal_password=True, 
                    password=True,                    
                    hint_style=ft.TextStyle(
                        font_family="Arial",
                        color=ft.colors.BLACK,
                        # weight="bold"
                    ),
                    label_style=ft.TextStyle(
                        font_family="Arial",
                        color=ft.colors.BLACK,
                        # weight="bold"
                    ),
                    color=ft.colors.BLACK,
                    expand=True,
                    # value='11UJOJON'
                )
            ],
        )

        self.page.add(self.email, self.password)
        self.page.update()
        self.verifica_existencia_configuracao()
        

    def verifica_existencia_configuracao(self):
        try:
            # Tente abrir o arquivo JSON para leitura
            with open('cfg_api.json', 'r', encoding='utf-8') as f:
                # Carregue os dados do JSON para o dicionário 'existing_data'
                existing_data = json.load(f)

            email = existing_data["username"]
            password = existing_data["password"]

            # Acesse os controles TextField dentro de self.email e self.password
            self.email.controls[0].value = email
            self.password.controls[0].value = password

        except FileNotFoundError:
            # Se o arquivo não existir, use o conteúdo inicial definido
            self.email.value = None
            self.password.value = None

            # Atualize os campos para refletir os valores padrão
            self.email.controls[0].update()
            self.password.controls[0].update()

    def salva_valores_configuracao_api(e, username, password, password_api, id_bimer):
        cfg_api = {
            "username": username,
            "password": password,
            "password_api": password_api,
            "id_bimer": id_bimer,
        }

        with open('cfg_api.json', 'w', encoding='utf-8') as file:
            json.dump(cfg_api, file, ensure_ascii=False, indent=4)      

    def logar_clicked(self, e):
        # Obtenha os valores dos campos de texto
        username = self.email.controls[0].value
        password = self.password.controls[0].value

        auth_system = FirebaseAuth(self.app_instance)

        # Verifique se as credenciais estão corretas
        user_info = auth_system.login(username + '@sveletrica.com', password)
        # user_login = username #+ '@sveletrica.com'
        if user_info:
            print("Login realizado com sucesso!")
            self.app_instance.user_info = user_info  # Armazena as informações do usuário na classe principal

            self.password_api, self.id_bimer = auth_system.coleta_chave_api(username, user_info) # self.coleta_chave_api()

            self.salva_valores_configuracao_api(username=username, password=password, password_api=self.password_api, id_bimer=self.id_bimer)

            self.page.go('/')
        else:
            print("Usuário ou senha incorretos.")       

    def get_content(self):
        
        # Botão personalizado para realizar a filtragem
        botao_fazer_login = ft.ResponsiveRow(
            columns=12,
            controls=[MyButton(text="Enviar Alterações", on_click=self.logar_clicked)],
        )

        botao_fazer_cadastro = ft.ResponsiveRow(
            columns=12,
            controls=[ft.TextButton('Não tem uma conta?', on_click=lambda e: self.page.go('/login/novo'), data=0)],
        )

        texto_login = ft.ResponsiveRow(
                        columns=12,
                        controls=[
                            ft.Text(
                                    value='Login', 
                                    style=ft.TextThemeStyle.TITLE_LARGE,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK,
                                    text_align=ft.TextAlign.CENTER
                            ), 
                        ],
                    )

        login_senha = ft.Column(
            controls= [texto_login, self.email, self.password, botao_fazer_login, botao_fazer_cadastro],
            expand=True,
        )

        conteudo_campos = ft.Container(
            content=login_senha,
            bgcolor=ft.colors.WHITE,
            width=500,
            height=300,
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.all(5),
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                blur_radius=30, 
                color=ft.colors.RED, 
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
        )

        imagem = ft.Container(
            width=910,
            height=890,
            content=ft.Image(
                        src="images\login.jpg",
                        fit=ft.ImageFit.COVER,
                        # fit=ft.ImageFit.NONE,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        filter_quality=ft.FilterQuality.HIGH,
                        border_radius=ft.border_radius.all(10),
                        expand=True

                    ),
            padding=ft.padding.all(5),
        )

        linha = ft.Row(controls=[conteudo_campos, imagem])
        return linha

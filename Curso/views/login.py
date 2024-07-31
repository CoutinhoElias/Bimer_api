import flet as ft
from partials.button import MyButton
from views.sign_up import Cadastrar
from querys.login_json import user_credentials

class Login(ft.Row):

    def __init__(self, page: ft.Page):

        super().__init__()
        self.page = page  # Certifique-se de armazenar a página na instância

        # Campo responsivo.
        self.email = ft.ResponsiveRow(
            columns=12,
            controls=[
                ft.TextField(
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
                    expand=True
                )
            ],
        )

        # Campo responsivo.
        self.password = ft.ResponsiveRow(
            columns=12,
            controls=[
                ft.TextField(
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
                    expand=True
                )
            ],
        )

    def logar_clicked(self, e):
        # Obtenha os valores dos campos de texto
        username = self.email.controls[0].value
        password =  self.password.controls[0].value


        # Verifique se as credenciais estão corretas
        if username in user_credentials and user_credentials[username] == password:
            print("Login realizado com sucesso!")
            # Aqui você pode redirecionar o usuário para outra página, por exemplo:
            self.page.go('/dashboard')
        else:
            print("Usuário ou senha incorretos")

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

import flet as ft
from partials.button import MyButton
# from views.login import Login
from database.users_firebase import FirebaseAuth
# from configs.pyrebase_config import FirebaseConfig

class Cadastrar(ft.Row):

    def __init__(self, page: ft.Page):

        super().__init__()
        self.page = page  # Certifique-se de armazenar a página na instância

        self.label_do_formulário = ft.ResponsiveRow(
                        columns=12,
                        controls=[
                            ft.Text(
                                    value='Registre-se', 
                                    style=ft.TextThemeStyle.TITLE_LARGE,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK,
                                    text_align=ft.TextAlign.CENTER
                            ), 
                        ],
                    )

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
            columns=6,
            controls=[
                ft.TextField(
                    focused_border_color=ft.colors.RED,
                    hint_text='Digite sua senha', 
                    label='Password',
                    can_reveal_password=True, 
                    password=True,
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
        self.confirm_password = ft.ResponsiveRow(
            columns=6,
            controls=[
                ft.TextField(
                    focused_border_color=ft.colors.RED,
                    hint_text='Confirme sua senha', 
                    label='Confirmação de Senha',
                    can_reveal_password=True, 
                    password=True,
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
        self.password_api = ft.ResponsiveRow(
            columns=6,
            controls=[
                ft.TextField(
                    focused_border_color=ft.colors.RED,
                    hint_text='Password API', 
                    label='Senha API',
                    can_reveal_password=True, 
                    password=True,
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

    def registrar_clicked(self, e):
        auth_system = FirebaseAuth()

        username = self.email.controls[0].value
        password =  self.password.controls[0].value
        confirm_password =  self.confirm_password.controls[0].value
        password_api =  self.password_api.controls[0].value

        if password != confirm_password:
            print('Senhas estão diferentes!')
        else:
            # Sign up example
            uid_user = auth_system.signup(username+'@sveletrica.com', password, confirm_password)
            if uid_user:
                print("Cadastro realizado com sucesso!")
                auth_system.insere_perfil(username, password_api)
                self.page.go('/login')
            else:
                print("Falha no cadastro. Seu E-mail já existe!")        

    def get_content(self):
        
        # Botão personalizado para realizar a filtragem
        botao_fazer_cadastro = ft.ResponsiveRow(
            columns=12,
            controls=[MyButton(text="Registrar-se", on_click=self.registrar_clicked)],
        )

        botao_fazer_login = ft.ResponsiveRow(
            columns=12,
            controls=[ft.TextButton('Já tem uma conta?', on_click=lambda e: self.page.go('/login'), data=0)],
        )

        login_senha = ft.Column(
            controls= [self.label_do_formulário, self.email, self.password, self.confirm_password, self.password_api, botao_fazer_cadastro, botao_fazer_login],
            expand=True,
        )

        conteudo_campos = ft.Container(
            content=login_senha,
            bgcolor=ft.colors.WHITE,
            width=500,
            height=400,
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

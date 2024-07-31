import flet as ft
from partials.button import MyButton
# from views.login import Login

class Cadastrar(ft.Row):

    def __init__(self, page: ft.Page):

        super().__init__()
        self.page = page  # Certifique-se de armazenar a página na instância

    def registrar_clicked(self, e):
        print("Registrado com sucesso!")

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

        label_do_formulário = ft.ResponsiveRow(
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
        email = ft.ResponsiveRow(
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
        nome = ft.ResponsiveRow(
            columns=12,
            controls=[
                ft.TextField(
                    focused_border_color=ft.colors.RED,
                    hint_text='Digite seu Nome', 
                    label='Nome/Sobrenome',
                    
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
        password = ft.ResponsiveRow(
            columns=6,
            controls=[
                ft.TextField(
                    focused_border_color=ft.colors.RED,
                    hint_text='Digite sua senha', 
                    label='Password',
                    
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
        confirm_password = ft.ResponsiveRow(
            columns=6,
            controls=[
                ft.TextField(
                    focused_border_color=ft.colors.RED,
                    hint_text='Confirme sua senha', 
                    label='Confirmação de Senha',
                    
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


        login_senha = ft.Column(
            controls= [label_do_formulário, email, password, confirm_password, botao_fazer_cadastro, botao_fazer_login],
            expand=True,
        )

        conteudo_campos = ft.Container(
            content=login_senha,
            bgcolor=ft.colors.WHITE,
            width=500,
            height=350,
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

import flet as ft
from partials.button import MyButton

class Cadastrar(ft.Row):

    def __init__(self, page: ft.Page):
        super().__init__()

        self.texto_tem_conta = ft.TextButton(text='já tem uma conta?', on_click=lambda e: page.go('/login'))

        self.cadastrar_conta = ft.Container(
                                    margin=ft.margin.only(top=20), 
                                    width=250, 
                                    height=40, 
                                    bgcolor=ft.colors.GREEN, 
                                    border_radius=20,
                                    alignment=ft.alignment.center,
                                    content=ft.Text(
                                                'Login3', 
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.colors.BLACK
                                            ), 
                                    on_click=lambda x: print('apertei aqui')
                                )
        
        self.usuario = ft.Container(
                            margin=ft.margin.only(top=20),
                            content=ft.TextField(
                                        focused_border_color=ft.colors.RED,
                                        hint_text='Digite seu Nome', 
                                        label='Nome', 
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
                                    )
                        )
        
        self.login_usuario = ft.Container(
                                margin=ft.margin.only(top=10),
                                content=ft.TextField(
                                            focused_border_color=ft.colors.RED,
                                            hint_text='Digite seu email', 
                                            label='Email', 
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
                                        )
                            )
        
        self.senha_usuario = ft.Container(
                                margin=ft.margin.only(top=10),
                                content=ft.TextField(
                                            focused_border_color=ft.colors.RED,
                                            hint_text='Digite sua senha', 
                                            label='Senha', 
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
                                        )
                            )
        
        self.confirm_senha = ft.Container(
                                margin=ft.margin.only(top=10),
                                content=ft.TextField(
                                            focused_border_color=ft.colors.RED,
                                            hint_text='Digite sua senha novamente', 
                                            label='Confirmar Senha', 
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
                                        )
                            )
        
        self.chave_privada = ft.Container(
                                margin=ft.margin.only(top=10),
                                content=ft.TextField(
                                            focused_border_color=ft.colors.RED,
                                            hint_text='Digite sua chave privada metamask/trust wallet', 
                                            label='Chave Privada', 
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
                                        )
                            )
        
        self.wallet = ft.Container(
                            margin=ft.margin.only(top=10),
                            content=ft.TextField(
                                        focused_border_color=ft.colors.RED,
                                        hint_text='Digite sua wallet', 
                                        label='Wallet', 
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
                                    )
                        )

        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.controls = [
                ft.Container(
                    width=500, 
                    height=700, 
                    padding=ft.padding.symmetric(vertical=30, horizontal=40),
                    content=ft.Container(
                                bgcolor=ft.colors.GREY_100, 
                                border_radius=30, 
                                shadow=ft.BoxShadow(
                                            blur_radius=30, 
                                            color=ft.colors.RED, 
                                            blur_style=ft.ShadowBlurStyle.OUTER
                                        ),
                                content=ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                                            controls=[
                                                ft.Container(
                                                    alignment=ft.alignment.
                                                    center, padding=ft.padding.only(top=20),
                                                    content=ft.Text(
                                                                value='Registre-se', 
                                                                text_align=ft.TextAlign.CENTER,
                                                                style=ft.TextStyle(
                                                                            size=30, 
                                                                            weight=ft.FontWeight.BOLD,
                                                                            color=ft.colors.BLACK
                                                                        )
                                                            )
                                                ),
                                                self.usuario,
                                                self.login_usuario,
                                                self.senha_usuario,
                                                self.confirm_senha,
                                                self.chave_privada,
                                                self.wallet,
                                                self.cadastrar_conta,
                                                self.texto_tem_conta
                                            ]
                                        )
                            )
            ),

            ft.Container(
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

        ]


class Login(ft.Row):

    def __init__(self, page: ft.Page):

        super().__init__()
        self.page = page  # Certifique-se de armazenar a página na instância


        # self.login_conta = ft.Container(margin=ft.margin.only(top=20),
        #                                 width=250,
        #                                 height=40,
        #                                 bgcolor=ft.colors.RED,
        #                                 border_radius=20,
        #                                 alignment=ft.alignment.center,
        #                                 content=ft.Text(
        #                                     'Login1', 
        #                                     weight=ft.FontWeight.BOLD,
        #                                     color=ft.colors.BLACK
        #                                 ),
        #                                 on_click=lambda x: print(
        #                                     'apertei aqui')
        #                                 )

        # self.login_usuario = ft.Container(
        #                         margin=ft.margin.only(top=50),
        #                         content=ft.TextField(
        #                                     focused_border_color=ft.colors.RED,
        #                                     hint_text='Digite seu email', 
        #                                     label='Email', 
        #                                     width=250,
        #                                     hint_style=ft.TextStyle(
        #                                         font_family="Arial",
        #                                         color=ft.colors.BLACK,
        #                                         # weight="bold"
        #                                     ),
        #                                     label_style=ft.TextStyle(
        #                                         font_family="Arial",
        #                                         color=ft.colors.BLACK,
        #                                         # weight="bold"
        #                                     ),
        #                                     color=ft.colors.BLACK,)
        #                     )
        # self.senha_usuario = ft.Container(margin=ft.margin.only(top=20), 
        #                                         content=ft.TextField(
        #                                                     focused_border_color=ft.colors.RED,
        #                                                     hint_text='Digite sua senha', 
        #                                                     label='Senha', 
        #                                                     width=250, 
        #                                                     can_reveal_password=True, 
        #                                                     password=True,
        #                                                     hint_style=ft.TextStyle(
        #                                                         font_family="Arial",
        #                                                         color=ft.colors.BLACK,
        #                                                         # weight="bold"
        #                                                     ),
        #                                                     label_style=ft.TextStyle(
        #                                                         font_family="Arial",
        #                                                         color=ft.colors.BLACK,
        #                                                         # weight="bold"
        #                                                     ),
        #                                                     color=ft.colors.BLACK,
        #                                                 )
        #                     )
        # self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        # self.controls = [
        #     ft.Container(
        #         width=500,
        #         height=700,
        #         padding=ft.padding.symmetric(vertical=160, horizontal=40),
        #         content=ft.Container(
        #             bgcolor=ft.colors.GREY_100,
        #             border_radius=30,
        #             shadow=ft.BoxShadow(
        #                 blur_radius=30,
        #                 color=ft.colors.RED,
        #                 blur_style=ft.ShadowBlurStyle.OUTER
        #             ),
        #             content=ft.Column(
        #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        #                 controls=[
        #                     ft.Container(
        #                         alignment=ft.alignment.center, 
        #                         # padding=ft.padding.all(10), # only(top=20),
        #                         content=ft.Text(
        #                             value='Login2',
        #                             text_align=ft.TextAlign.CENTER,
        #                             style=ft.TextStyle(
        #                                         size=30, 
        #                                         weight=ft.FontWeight.BOLD,
        #                                         color=ft.colors.BLACK
        #                                     )
        #                         )
        #                     ),
        #                     self.login_usuario,
        #                     self.senha_usuario,
        #                     self.login_conta,
        #                     self.texto_criar
        #                 ]
        #             )
        #         )
        #     ),
        #     ft.Container(
        #         width=910,
        #         height=890,
        #         content=ft.Image(
        #                     src="images\login.jpg",
        #                     fit=ft.ImageFit.COVER,
        #                     # fit=ft.ImageFit.NONE,
        #                     repeat=ft.ImageRepeat.NO_REPEAT,
        #                     filter_quality=ft.FilterQuality.HIGH,
        #                     border_radius=ft.border_radius.all(10),
        #                     expand=True

        #                 ),
        #         padding=ft.padding.all(5),
        #     )
        # ]

    def logar_clicked(self, e):
        print("Produto alterado com sucesso!")

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
        password = ft.ResponsiveRow(
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

        login_senha = ft.Column(
            controls= [texto_login, email, password, botao_fazer_login, botao_fazer_cadastro],
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

import flet as ft

my_tab = ft.Tabs(
        # ref=tabs_from_main,
        tabs=[
            ft.Tab(
                text='Dados',
                icon=ft.icons.TABLE_ROWS_OUTLINED,
                content=ft.Container(
                            expand=False,
                            padding=ft.padding.all(5),
                            content= mytable,
                            # width=20,
                            # height=5,
                            # bgcolor=ft.colors.AMBER_100                
                ),
            ),

            ft.Tab(
                text='Parâmetros',
                icon=ft.icons.SETTINGS,
                content=ft.Container(
                    expand=False,
                    padding=ft.padding.all(2),
                    content=ft.Column(
                        expand=True,
                        controls= 
                            [
                                # norte, nordeste, ceara, centro_oeste, sudeste, sul, floating_action_button
                            ],
                    scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
                    on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos                         
                    ),                   
                )                
            ),            
        ],
        selected_index = 0,
        indicator_tab_size = True,
        label_color=ft.colors.GREEN,
        # width=100, # Ajuste da Largura
        height=850, # Ajuste da altura
        # expand=1,
        # on_change=lambda _: print(directory_path_or_file.value)
    )
import flet as ft

from datetime import datetime

from partials.data_table import create_datatable, my_table
from partials.button import MyButton
from querys.qry_pedidos import PedidosDeCompra
from querys.qry_fornecedor import Fornecedor

class PedidoView:
    def __init__(self, page):
        self.page = page
        self.id_fornecedor = None

        # Definição do Ref().
        self.tb_tabela = ft.Ref[ft.DataTable]()
        self.tb_tabela_itens_pedido = ft.Ref[ft.DataTable]()

        # ============================================================================================================================= 
        # Jogue aqui seus estilos:

        # Estilo para os butões de data.   
        self.button_style = ft.ButtonStyle(
                                        shape={
                                            ft.MaterialState.HOVERED: ft.CircleBorder(),
                                            ft.MaterialState.DEFAULT: ft.CircleBorder(),
                                        },
                                    )
        
        # Estilo para os campos de entrada
        # self.input_style = ft.TextStyle(
        #     color=ft.colors.WHITE,  # Cor do texto
        #     placeholder_color=ft.colors.GREY_400,  # Cor dos placeholders
        #     border_color=ft.colors.ORANGE_300  # Cor da borda
        # )        
        # =============================================================================================================================

        self.pg_codigo_chamada = ft.TextField(
            label="Código", 
            hint_text="FORNECEDOR",
            col={"md": 2},
            focused_border_color=ft.colors.YELLOW,
            input_filter=ft.NumbersOnlyInputFilter(),
            # text_style=self.input_style,
            on_blur = self.handle_change_cd_crm, 
        )

        self.pg_nome_fornecedor = ft.TextField(
            label="Nome", 
            hint_text="FORNECEDOR",
            col={"md": 7},
            focused_border_color=ft.colors.YELLOW,
        )

        self.pg_dd_codigo_empresa = ft.Dropdown(
            col={"md": 2},
            label="Escolha Empresa",
            hint_text="Empresa",
            value="04",
            focused_border_color=ft.colors.YELLOW,
            options=[
                ft.dropdown.Option("01", text="01 - MATRIZ"),
                ft.dropdown.Option("04", text="04 - FILIAL"),
                ft.dropdown.Option("12", text="12 - SV BM"),
                ft.dropdown.Option("59", text="59 - SV WS"),
            ],
            autofocus=True,
        )

        self.pg_dd_status_pedido = ft.Dropdown(
            col={"md": 1},
            label="Qual Status?",
            hint_text="Status",
            value="A",
            focused_border_color=ft.colors.YELLOW,
            options=[
                ft.dropdown.Option("A", text="A"),
                ft.dropdown.Option("C", text="C"),
                ft.dropdown.Option("D", text="D"),
                ft.dropdown.Option("F", text="F"),
                ft.dropdown.Option("G", text="G"),
                ft.dropdown.Option("P", text="P"),
                ft.dropdown.Option("T", text="T"),
                ft.dropdown.Option("X", text="X"),
            ],
            autofocus=True,
        )

        self.txt_pick_date_start = ft.TextField(
            label="Dt. Início", 
            hint_text="Dt. Inicial",
            col={"md": 2},
            focused_border_color=ft.colors.YELLOW,
            # icon=ft.icons.DATE_RANGE,
        )

        self.txt_pick_date_end = ft.TextField(
            label="Dt. Fim", 
            hint_text="Dt. Final",
            col={"md": 2},
            focused_border_color=ft.colors.YELLOW,
            # icon=ft.icons.DATE_RANGE,
        )

        # ---------------------------------------------------------------------------------------------------------------------------------------
        # TABELAS DA VIEW
        # ---------------------------------------------------------------------------------------------------------------------------------------
        # LISTA DE PEDIDOS        
        self.campos_pedido = [
            ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Status", width=40), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Data Emissao", width=150), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Data Entrega", width=150)),
            ft.DataColumn(ft.Text("Descricao", width=70), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Observacao", width=240), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
        ]
        self.datatable = create_datatable(self.tb_tabela, self.campos_pedido)
        self.table_order = my_table(self.datatable)

        # LISTA DE ITENS DO PEDIDO
        self.campos_pedido_itens = [
            ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Descricao", width=70), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("NCM", width=40), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Quantidade", width=80), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Vl. Unit.", width=80)),
            ft.DataColumn(ft.Text("IPI", width=50), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
            ft.DataColumn(ft.Text("ICMS", width=50), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
            ft.DataColumn(ft.Text("Vl. Total", width=80)),
        ]
        self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.campos_pedido_itens)
        self.table_order_items = my_table(self.datatable_itens_pedido)
        # ---------------------------------------------------------------------------------------------------------------------------------------

    def handle_date_change_start(self, e):
        # self.pg_codigo_chamada.focus()
        self.txt_pick_date_start.value = e.control.value.strftime('%d/%m/%Y')
        self.page.update()

    def handle_date_change_end(self, e):
        self.txt_pick_date_end.value = e.control.value.strftime('%d/%m/%Y')
        # self.pesquisa_pedidos()
        self.page.update()

    def handle_change_cd_crm(self, e):
        self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
        self.pg_codigo_chamada.update() 
        self.pesquisa_fornededor(codigo_crm=self.pg_codigo_chamada.value)
        self.pg_codigo_chamada.update()

    def handle_date_dismissal(self, e):
        self.page.add(ft.Text("DatePicker dismissed"))
        self.page.update()

    def filtrar_clicked(self, e):
        self.pesquisa_pedidos()
        self.datatable.rows = []
        # print("Cancel clicked")

    def create_date_picker(self):
        
        return ft.DatePicker(
            cancel_text='Cancelar',
            confirm_text='Selecionar',
            error_format_text='Data inválida',
            field_label_text='Digite uma data',
            help_text='Selecione uma data no calendário',
            expand=True,
            on_change=self.handle_date_change_start,
            on_dismiss=self.handle_date_dismissal,
        )
    
    def create_date_picker_end(self):
        return ft.DatePicker(
            cancel_text='Cancelar',
            confirm_text='Selecionar',
            error_format_text='Data inválida',
            field_label_text='Digite uma data',
            help_text='Selecione uma data no calendário',
            on_change=self.handle_date_change_end,
            on_dismiss=self.handle_date_dismissal
        )    

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # IDENTIFICANDO PEDIDO SELECIONADO - Order
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def change_select(self, e):
        e.control.selected = not e.control.selected
        e.control.update()

        if e.control.selected:
            if self.tb_tabela.current:
                selected_row = e.control  # Pega a linha selecionada diretamente do evento
                selected_cell_value = selected_row.cells[0].content.value
                print(selected_cell_value)
        else:
            print('Deselected')

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # POPULANDO TABELAS
    # ---------------------------------------------------------------------------------------------------------------------------------------

    #TABELA DE PEDIDOS
    def add_datatable_itens(self, codigo, status, data_emissao, data_entrega, descricao, observacao, selecionado=False):
        self.datatable.rows.append(
            ft.DataRow(
                [
                    ft.DataCell(ft.Text(value=codigo)),
                    ft.DataCell(ft.Text(status)),
                    ft.DataCell(ft.Text(data_emissao)),
                    ft.DataCell(ft.Text(data_entrega)),
                    ft.DataCell(ft.Text(descricao)),
                    ft.DataCell(ft.Text(observacao)),
                ],
                selected=selecionado,
                on_select_changed = self.change_select,
            )
        )
        self.datatable.update()
        # self.page.banner.content.controls[0].controls[1].controls[1].update()

    # TABELA DE ITESN DO PEDIDO
    def add_datatable_itens_pedido(self, codigo, status, data_emissao, data_entrega, descricao, observacao, selecionado=False):
        self.datatable_itens_pedido.rows.append(
            ft.DataRow(
                [
                    ft.DataCell(ft.Text(value=codigo)),
                    ft.DataCell(ft.Text(status)),
                    ft.DataCell(ft.Text(data_emissao)),
                    ft.DataCell(ft.Text(data_entrega)),
                    ft.DataCell(ft.Text(descricao)),
                    ft.DataCell(ft.Text(observacao)),
                ],
                selected=selecionado,
                on_select_changed = self.change_select,
            )
        )
        self.datatable_itens_pedido.update()
        # self.page.banner.content.controls[0].controls[1].controls[1].update()
    # ---------------------------------------------------------------------------------------------------------------------------------------

    def pesquisa_fornededor(self, codigo_crm):
        self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
        codigo_crm = self.pg_codigo_chamada.value.zfill(6)

        # Crie uma instância da classe, passando os parâmetros da consulta:
        fornecedor = Fornecedor(codigo_crm=codigo_crm)

        # Obtenha o DataFrame dos pedidos de compra:
        self.id_fornecedor, nm_fornecedor = fornecedor.consultar_fornecedor_api()

        # Obter os valores de id_fornecedor e nm_fornecedor
        self.pg_nome_fornecedor.value = nm_fornecedor
        self.pg_nome_fornecedor.update()

    def pesquisa_pedidos(self):
        # Crie uma instância da classe, passando os parâmetros da consulta:
        data_ini = self.txt_pick_date_start.value                
        # Converte a string para um objeto datetime
        data_ini_obj = datetime.strptime(data_ini, '%d/%m/%Y')

        # Crie uma instância da classe, passando os parâmetros da consulta:
        data_fim = self.txt_pick_date_end.value                
        # Converte a string para um objeto datetime
        data_fim_obj = datetime.strptime(data_fim, '%d/%m/%Y')        

        # Converte o objeto datetime para uma string no formato YYYY-MM-DD
        data_ini = data_ini_obj.strftime('%Y-%m-%d')
        # Converte o objeto datetime para uma string no formato YYYY-MM-DD
        data_fim = data_fim_obj.strftime('%Y-%m-%d')        

        pedido_de_compra = PedidosDeCompra(cd_empresa=self.pg_dd_codigo_empresa.value, codigo_crm=self.pg_codigo_chamada.value, id_fornecedor=self.id_fornecedor, status=self.pg_dd_status_pedido.value, dt_emissao_ini=data_ini, dt_emissao_fim=data_fim)

        # Obtenha o DataFrame dos pedidos de compra:
        df_pedidos = pedido_de_compra.obter_dataframe_pedidos_de_compra()

        for index, row in df_pedidos.iterrows():
            self.add_datatable_itens(row['Codigo'], row['Status'], row['DataEmissao'], row['DataEntrega'], row['Descricao'], row['Observacao'], selecionado=False)

    def get_content(self):

        empresa_codigo_fornecedor = ft.ResponsiveRow(
            columns=12,
            controls=[self.pg_dd_codigo_empresa, self.pg_dd_status_pedido, self.pg_codigo_chamada, self.pg_nome_fornecedor],
        )

        btn_pick_date_start = ft.IconButton(
                    icon=ft.icons.DATE_RANGE,
                    icon_color="blue400",
                    icon_size=30,
                    tooltip="Data Inicial.",
                    col={"md": .6},
                    style=self.button_style,
                    on_click=lambda e: self.page.open(self.create_date_picker()), 
                )

        btn_pick_date_end = ft.IconButton(
                    icon=ft.icons.DATE_RANGE,
                    icon_color="blue400",
                    icon_size=30,
                    tooltip="Data Inicial.",
                    col={"md": .6},
                    style=self.button_style,
                    on_click=lambda e: self.page.open(self.create_date_picker_end()),
                )

        spacer = ft.Container(col={"md": .4},)  # Espaçador

        # self.pesquisa_pedidos() / self.filtrar_clicked
        button = MyButton(text="Filtrar", on_click=self.filtrar_clicked)

        datas_e_botoes = ft.ResponsiveRow(
            columns=12,
            spacing=0,
            controls=[self.txt_pick_date_start, btn_pick_date_start, spacer, self.txt_pick_date_end, btn_pick_date_end, button],
        )


        layout = ft.Column(
            controls=[empresa_codigo_fornecedor, datas_e_botoes, self.table_order],
            alignment=ft.alignment.center,
            expand=True
        )

        my_tab = ft.Tabs(
                # ref=tabs_from_main,
                tabs=[
                    ft.Tab(
                        text='Lista de Pedidos',
                        icon=ft.icons.TABLE_VIEW_OUTLINED,
                        content=ft.Container(
                                    expand=False,
                                    padding=ft.padding.all(10),
                                    content= layout,
                                    # width=20,
                                    # height=5,
                                    # bgcolor=ft.colors.AMBER_100                
                        ),
                    ),

                    ft.Tab(
                        text='Itens do Pedido selecionado',
                        icon=ft.icons.TABLE_ROWS_OUTLINED,
                        content=ft.Container(
                            expand=False,
                            padding=ft.padding.all(2),
                            content=ft.Column(
                                expand=True,
                                controls= 
                                    [
                                        self.table_order_items # layout ******************  OUTRA TAB A SER PREENCHIDA ******************
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

        return my_tab

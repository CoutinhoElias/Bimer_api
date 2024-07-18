import flet as ft

from datetime import datetime

from partials.data_table import create_datatable, my_table
from partials.button import MyButton
from querys.qry_pedidos_local import PedidosDeCompra
from querys.qry_pedidos_itens import PedidosDeCompraItens
from querys.qry_produto import Produto
from querys.qry_fornecedor import Fornecedor

import sys
import os
from datetime import datetime, timedelta
import json
from pprint import pprint

# Adicionar o diretório "Curso" ao sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configs.settings import *

# Encontrar uma maneira de criar tabela com linha em branco
# self.add_datatable_itens('', '', '', '', 'NENHUM ITEM LISTADO', 'REDEFINA SEU FILTRO', selecionado=False)

class PedidoView:
    def __init__(self, page):
        self.page = page
        self.id_fornecedor = None

        # Definição do Ref().
        self.tb_tabela = ft.Ref[ft.DataTable]()
        self.tb_tabela_itens_pedido = ft.Ref[ft.DataTable]()
        self.tb_tab_pedido = ft.Ref[ft.Tab]()

        self.pedidos_json = {}

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
            ft.DataColumn(ft.Text("Data Emissao", width=110), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Data Entrega", width=110)),
            ft.DataColumn(ft.Text("Descricao", width=70), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Observacao", width=530, text_align="LEFT"), numeric=False,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
        ]
        self.datatable = create_datatable(self.tb_tabela, self.campos_pedido)
        self.table_order = my_table(self.datatable)

        # LISTA DE ITENS DO PEDIDO
        self.campos_pedido_itens = [
            ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Descricao", width=420), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Quantidade", width=80),  numeric=True, on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Vl. Unit.", width=80),  numeric=True),
            ft.DataColumn(ft.Text("IPI", width=50), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
            ft.DataColumn(ft.Text("ICMS", width=50), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
            ft.DataColumn(ft.Text("Vl. Total", width=80),  numeric=True,),
        ]

        self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.campos_pedido_itens)
        self.table_order_items = my_table(self.datatable_itens_pedido)
        # ---------------------------------------------------------------------------------------------------------------------------------------

    def get_first_and_last_day_of_month(self, date):
        # Obter o primeiro dia do mês
        first_day = date.replace(day=1)
        
        # Obter o último dia do mês
        next_month = first_day.replace(month=first_day.month % 12 + 1, day=1)
        last_day = next_month - timedelta(days=1)
        
        return first_day, last_day

    def handle_date_change_start(self, e):
        # self.pg_codigo_chamada.focus()
        self.txt_pick_date_start.value = e.control.value.strftime('%d/%m/%Y')
        self.page.update()

    def handle_date_change_end(self, e):
        self.txt_pick_date_end.value = e.control.value.strftime('%d/%m/%Y')
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
        # Data de hoje
        today = datetime.today()

        # Obter o primeiro e último dia do mês atual
        first_day, last_day = self.get_first_and_last_day_of_month(today)

        # Formatar as datas para exibição
        first_day_formatted = first_day.strftime('%d/%m/%Y')
        last_day_formatted = last_day.strftime('%d/%m/%Y')

        if self.txt_pick_date_start.value == '':
            self.txt_pick_date_start.value = first_day_formatted
            self.txt_pick_date_start.update()

        if self.txt_pick_date_end.value == '':
            self.txt_pick_date_end.value = last_day_formatted
            self.txt_pick_date_end.update()

        self.pedidos_json = self.pesquisa_pedidos()
        self.datatable.rows = []

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
                selected_row = e.control  # Pega a linha selecionada diretamente do evento.
                selected_cell_value = selected_row.cells[0].content.value # Copia o código do pedido de compra.
                # Troca a aba do controle TAB.
                self.tb_tab_pedido.current.selected_index = 1
                self.tb_tab_pedido.current.update()

                # print(self.pedidos_json[selected_cell_value]['IdPedidoDeCompra'], '<<<======')
                id_pedido_de_compra = self.pedidos_json[selected_cell_value]['IdPedidoDeCompra'] # Procura o ID do Pedido de compra no dicionário criado anteriormente.
                itens_pedido_de_compra = PedidosDeCompraItens(id_pedido_de_compra=id_pedido_de_compra) # Seta a classe dos itens do pedido de compra, note que envio o IdPedidoDeCompra.

                # Obtenha o DataFrame dos pedidos de compra:
                df_itens_pedidos = itens_pedido_de_compra.obter_dataframe_pedido_de_compra_itens() # Captura da API os itens deste pedido de compra que eu cliquei (Como DataFrame do Pandas).

                self.datatable_itens_pedido.rows = [] # Limpa a lista de produtos da tabela antes de adicionar a nova listagem.

                # Percorro o DataFrame usando iterrows.
                for index, row in df_itens_pedidos.iterrows():
                    # Para cada linha do DataFrame adicione uma linha do DataTable de 'itens do pedido'.
                    self.add_datatable_itens_pedido(id_produto=row['IdentificadorProduto'], 
                                                    quantidade=row['QuantidadePedida'], 
                                                    valor_unitario=row['ValorItem'], 
                                                    valor_item=row['ValorUnitario'], 
                                                    valor_icms=row['ValorIcms'], 
                                                    valor_ipi=row['ValorIPI'], 
                                                    selecionado=False)
        else:
            print('Deselected')

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # POPULANDO TABELAS
    # ---------------------------------------------------------------------------------------------------------------------------------------

    #TABELA DE PEDIDOS
    def add_datatable_itens(self, codigo, status, data_emissao, data_entrega, descricao, observacao, selecionado=False):
        # Adiciona uma nova linha à DataTable 'self.datatable'
        self.datatable.rows.append(
            ft.DataRow(
                [
                    # Adiciona uma célula com o valor 'codigo'
                    ft.DataCell(ft.Text(value=codigo)),
                    
                    # Adiciona uma célula com o valor 'status'
                    ft.DataCell(ft.Text(status)),
                    
                    # Adiciona uma célula com o valor 'data_emissao'
                    ft.DataCell(ft.Text(data_emissao)),
                    
                    # Adiciona uma célula com o valor 'data_entrega'
                    ft.DataCell(ft.Text(data_entrega)),
                    
                    # Adiciona uma célula com o valor 'descricao'
                    ft.DataCell(ft.Text(descricao)),
                    
                    # Adiciona uma célula com o valor 'observacao' e alinha o texto à esquerda
                    ft.DataCell(ft.Text(observacao, text_align="LEFT")),
                ],
                # Define se a linha está selecionada ou não
                selected=selecionado,
                
                # Define o manipulador de eventos para mudança de seleção da linha
                on_select_changed = self.change_select,
            )
        )
        # Atualiza a DataTable para refletir as mudanças
        self.datatable.update()
        # self.page.banner.content.controls[0].controls[1].controls[1].update()

    # TABELA DE ITESN DO PEDIDO
    def add_datatable_itens_pedido(self, id_produto, quantidade, valor_unitario, valor_item, valor_icms, valor_ipi, selecionado=False):
        # Cria uma instância da classe Produto para obter detalhes do produto com base no id_produto
        dados_produto = Produto(id_produto)
        
        # Consulta o código e a descrição do produto usando a API
        codigo, descricao = dados_produto.consultar_produto_codigo_api()

        # Adiciona uma nova linha à DataTable 'self.datatable_itens_pedido'
        self.datatable_itens_pedido.rows.append(
            ft.DataRow(
                [
                    # Adiciona uma célula com o valor 'codigo' do produto
                    ft.DataCell(ft.Text(value=codigo)),
                    
                    # Adiciona uma célula com a 'descricao' do produto
                    ft.DataCell(ft.Text(descricao)),
                    
                    # Adiciona uma célula com a 'quantidade' pedida
                    ft.DataCell(ft.Text(quantidade)),
                    
                    # Adiciona uma célula com o 'valor_item'
                    ft.DataCell(ft.Text(valor_item)),
                    
                    # Adiciona uma célula com o 'valor_ipi' do produto
                    ft.DataCell(ft.Text(valor_ipi)),
                    
                    # Adiciona uma célula com o 'valor_icms' do produto
                    ft.DataCell(ft.Text(valor_icms)),
                    
                    # Adiciona uma célula com o 'valor_unitario' do produto
                    ft.DataCell(ft.Text(valor_unitario)),
                ],
                # Define se a linha está selecionada ou não
                selected=selecionado,
                
                # Define o manipulador de eventos para mudança de seleção da linha
                on_select_changed=self.change_select,
            )
        )
        # Atualiza a DataTable para refletir as mudanças
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
        # Obtenha a data inicial do campo de texto e converta para objeto datetime
        data_ini = self.txt_pick_date_start.value                
        data_ini_obj = datetime.strptime(data_ini, '%d/%m/%Y')

        # Obtenha a data final do campo de texto e converta para objeto datetime
        data_fim = self.txt_pick_date_end.value                
        data_fim_obj = datetime.strptime(data_fim, '%d/%m/%Y')        

        # Converta os objetos datetime para strings no formato YYYY-MM-DD
        data_ini = data_ini_obj.strftime('%Y-%m-%d')
        data_fim = data_fim_obj.strftime('%Y-%m-%d')        

        try:
            # Crie uma instância da classe PedidosDeCompra com os parâmetros fornecidos
            db_handler = PedidosDeCompra(
                connection_string=connection_string,
                cd_empresa=self.pg_dd_codigo_empresa.value,
                codigo_crm=self.pg_codigo_chamada.value,
                id_fornecedor=self.id_fornecedor,
                status=self.pg_dd_status_pedido.value,
                dt_emissao_ini=data_ini,
                dt_emissao_fim=data_fim
            )
            
            # Obtenha os pedidos de compra filtrados
            pedidos_de_compras = db_handler.get_all_pedidos_de_compras_filtered()
        
        except Exception as e:
            # Captura e imprime qualquer erro ocorrido durante a busca dos pedidos
            print(f"Erro ao buscar pedidos: {e}")
            return {}

        # Construa um dicionário com os detalhes dos pedidos de compra
        pedidos_dict = {
            pedido.CdChamada: {
                "CdChamada": pedido.CdChamada,
                "IdPedidoDeCompra": pedido.IdPedidoDeCompra,
                "StPedidoDeCompra": pedido.StPedidoDeCompra,
                "DtEmissao": pedido.DtEmissao,
                "DtEntrega": pedido.DtEntrega,
                "DsPedidoDeCompra": pedido.DsPedidoDeCompra,
                "DsObservacao": pedido.DsObservacao,
                "Selecionado": False
            }
            for pedido in pedidos_de_compras
        }

        # Adicione cada pedido à DataTable
        for pedido in pedidos_dict.values():
            self.add_datatable_itens(
                pedido["CdChamada"], 
                pedido["StPedidoDeCompra"], 
                pedido["DtEmissao"], 
                pedido["DtEntrega"], 
                pedido["DsPedidoDeCompra"], 
                pedido["DsObservacao"], 
                selecionado=pedido["Selecionado"]
            )

        # Retorne o dicionário com os pedidos
        return pedidos_dict

    def get_content(self):
        # Criação de uma linha responsiva contendo os campos de código da empresa, status do pedido, código de chamada e nome do fornecedor
        empresa_codigo_fornecedor = ft.ResponsiveRow(
            columns=12,
            controls=[self.pg_dd_codigo_empresa, self.pg_dd_status_pedido, self.pg_codigo_chamada, self.pg_nome_fornecedor],
        )

        # Botão de ícone para selecionar a data inicial
        btn_pick_date_start = ft.IconButton(
            icon=ft.icons.DATE_RANGE,
            icon_color="blue400",
            icon_size=30,
            tooltip="Data Inicial.",
            col={"md": .6},
            style=self.button_style,
            on_click=lambda e: self.page.open(self.create_date_picker()), 
        )

        # Botão de ícone para selecionar a data final
        btn_pick_date_end = ft.IconButton(
            icon=ft.icons.DATE_RANGE,
            icon_color="blue400",
            icon_size=30,
            tooltip="Data Final.",
            col={"md": .6},
            style=self.button_style,
            on_click=lambda e: self.page.open(self.create_date_picker_end()),
        )

        # Espaçador para ajuste do layout
        spacer = ft.Container(col={"md": .4})

        # Botão personalizado para realizar a filtragem
        button = MyButton(text="Filtrar", on_click=self.filtrar_clicked)

        # Linha responsiva contendo os campos de data e os botões de seleção de data
        datas_e_botoes = ft.ResponsiveRow(
            columns=12,
            spacing=0,
            controls=[self.txt_pick_date_start, btn_pick_date_start, spacer, self.txt_pick_date_end, btn_pick_date_end, button],
        )

        # Criação de uma coluna contendo o layout principal com os controles e tabelas
        layout = ft.Column(
            controls=[empresa_codigo_fornecedor, datas_e_botoes, self.table_order],
            alignment=ft.alignment.center,
            expand=True
        )

        # Criação das abas para navegação entre a lista de pedidos e os itens do pedido selecionado
        my_tab = ft.Tabs(
            ref=self.tb_tab_pedido,
            tabs=[
                ft.Tab(
                    text='Lista de Pedidos',
                    icon=ft.icons.TABLE_VIEW_OUTLINED,
                    content=ft.Container(
                        expand=False,
                        padding=ft.padding.all(10),
                        content=layout,
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
                        padding=ft.padding.all(10),
                        content=ft.Column(
                            expand=True,
                            controls=[self.table_order_items],
                            scroll=ft.ScrollMode.ALWAYS,  # Define a existência de um Scroll
                            on_scroll_interval=0,  # Define o intervalo de exibição da Scroll
                        ),                   
                    )                
                ),            
            ],
            selected_index=0,
            indicator_tab_size=True,
            label_color=ft.colors.GREEN,
            # width=100, # Ajuste da Largura
            height=850, # Ajuste da altura
            # expand=1,
            # on_change=lambda _: print(directory_path_or_file.value)
        )

        # Retorna o objeto 'my_tab' contendo as abas configuradas
        return my_tab


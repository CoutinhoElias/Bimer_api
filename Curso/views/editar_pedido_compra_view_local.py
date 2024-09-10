import flet as ft

from datetime import datetime

from partials.data_table import create_datatable, my_table

from partials.button import MyButton
from querys.qry_pedido_compra_local import PedidosDeCompra
from querys.qry_pedido_compra_itens import PedidosDeCompraItens
from querys.qry_produto import Produto
# from querys.qry_produto_local import BuscaCodigoProduto
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
        self.id_pedido_de_compra = None
        self.total_pedido = 0

        # Definição do Ref().
        self.tb_tabela = ft.Ref[ft.DataTable]()
        self.tb_tabela_itens_pedido = ft.Ref[ft.DataTable]()
        self.tb_tab_pedido = ft.Ref[ft.Tab]()

        self.pedidos_json = {} # Todos os pedidos.
        self.pedido_produtos_json = {} # Todos os produtos de um pedido.
        self.codigo_x_id_json = {} # Específico para traduzir de código para id e vice versa.
        self.dicionario_envio_url = {} # Dicionario final para enviar, pode ser editado antes do envio.
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
        self.colunas_dos_pedidos = [
            ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Status", width=40), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Data Emissao", width=110), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Data Entrega", width=110)),
            ft.DataColumn(ft.Text("Descricao", width=70), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Observacao", width=330, text_align="LEFT"), numeric=False,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
        ]
        self.datatable = create_datatable(self.tb_tabela, self.colunas_dos_pedidos)
        self.table_order = my_table(self.datatable)

        # LISTA DE ITENS DO PEDIDO
        self.colunas_dos_itens_dos_pedidos = [
            ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Descricao", width=460), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Quantidade", width=80),  numeric=True, on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Vl. Unit.", width=85),  numeric=True),
            ft.DataColumn(ft.Text("IPI", width=60), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
            ft.DataColumn(ft.Text("ICMS", width=60), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
            ft.DataColumn(ft.Text("Vl. Total", width=85),  numeric=True,),
        ]

        self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.colunas_dos_itens_dos_pedidos)
        self.table_order_items = my_table(self.datatable_itens_pedido)

        self.mytable_pedidos = ft.Column(
            expand=True,
            controls=[
                ft.Row( 
                    controls = [self.table_order], 
                    scroll = ft.ScrollMode.ALWAYS
                )
            ],
            scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
            on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos           
        )       

        self.mytable_itens = ft.Column(
            expand=True,
            controls=[
                ft.Row( 
                    controls = [self.table_order_items], 
                    scroll = ft.ScrollMode.ALWAYS
                )
            ],
            scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
            on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos           
        )   
        # ---------------------------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # IDENTIFICANDO PEDIDO SELECIONADO - Order
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def change_select(self, e):
        e.control.selected = not e.control.selected
        e.control.update() # change_select_produtos

        if e.control.selected:
            if self.tb_tabela.current:
                selected_row = e.control  # Pega a linha selecionada diretamente do evento.
                selected_cell_value = selected_row.cells[0].content.value # Copia o código do pedido de compra.
                # Troca a aba do controle TAB.
                self.tb_tab_pedido.current.selected_index = 1
                self.tb_tab_pedido.current.update()

                # print(self.pedidos_json[selected_cell_value]['IdPedidoDeCompra'], '<<<======')
                self.id_pedido_de_compra = self.pedidos_json[selected_cell_value]['IdPedidoDeCompra'] # Procura o ID do Pedido de compra no dicionário criado anteriormente.
                itens_pedido_de_compra = PedidosDeCompraItens(id_pedido_de_compra=self.id_pedido_de_compra) # Seta a classe dos itens do pedido de compra, note que envio o IdPedidoDeCompra.

                # Obtenha o DataFrame dos pedidos de compra:
                df_itens_pedidos, self.pedido_produtos_json, self.dicionario_envio_url = itens_pedido_de_compra.obter_dataframe_pedido_de_compra_itens() # Captura da API os itens deste pedido de compra que eu cliquei (Como DataFrame do Pandas).

                self.datatable_itens_pedido.rows = [] # Limpa a lista de produtos da tabela antes de adicionar a nova listagem.
                self.codigo_x_id_json = {} # Limpa o dicionário para próxima consulta.

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
            print('Deselected2')


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

    # Função para buscar o valor pela chave
    def buscar_valor_por_chave(self, dicionario, chave):
        return dicionario.get(chave, "Chave não encontrada")

    # Função para buscar a chave pelo valor
    def buscar_chave_por_valor(self, dicionario, valor_procurado):
        for chave, valor in dicionario.items():
            if valor == valor_procurado:
                return chave
        return "Valor não encontrado"

    # Função para buscar o item pelo identificador do produto
    def buscar_item_por_identificador(self, itens, identificador):
        for index, item in enumerate(itens):
            if item['IdentificadorProduto'] == identificador:
                return index, item
        return None, None

    def calcula_total_pedido(self):
        valor = 0
        itens = self.dicionario_envio_url['Itens']
        for i, item in enumerate(itens):
            if item['TipoCadastro'] != 'E':
                valor += float(item['ValorUnitario']) * float(item['QuantidadePedida'])
        self.total_pedido = round(valor, 2)
        # return valor

    def calcula_parcelas_pedido(self, valor_parcela):
        pagamentos = self.dicionario_envio_url['Pagamentos']

        # Processa o primeiro item (índice 0)
        self.dicionario_envio_url['Pagamentos'][0]['TipoCadastro'] = 'A'
        self.dicionario_envio_url['Pagamentos'][0]['AliquotaParcela'] = '100'
        self.dicionario_envio_url['Pagamentos'][0]['Valor'] = self.total_pedido

        # Mantém apenas o primeiro item no dicionário e remove os demais
        self.dicionario_envio_url['Pagamentos'] = [pagamentos[0]]

    def change_select_produtos(self, e):
        e.control.selected = not e.control.selected
        e.control.update()

        selected_row = e.control  # Pega a linha selecionada diretamente do evento.
        selected_cell_value = selected_row.cells[0].content.value # Copia o código do produto no pedido de compra.
        chave_encontrada = self.buscar_chave_por_valor(self.codigo_x_id_json, selected_cell_value)

        # Busca o item
        index, item_encontrado = self.buscar_item_por_identificador(self.dicionario_envio_url['Itens'], chave_encontrada)

        if e.control.selected:
            if self.tb_tabela.current:
                if item_encontrado:  # Verifica se o item foi encontrado antes de modificar
                    item_encontrado['TipoCadastro'] = 'E'
        else:
            if item_encontrado:  # Apenas modifica se o item foi encontrado e está inicializado
                print('Deselected')
                item_encontrado['TipoCadastro'] = 'A'

        parcelas = len(self.dicionario_envio_url['Pagamentos'])
        self.calcula_total_pedido()
        valor_parcela = self.total_pedido / parcelas
        self.calcula_parcelas_pedido(valor_parcela)

    # TABELA DE ITENS DO PEDIDO
    def add_datatable_itens_pedido(self, id_produto, quantidade, valor_unitario, valor_item, valor_icms, valor_ipi, selecionado=False):
        # Cria uma instância da classe Produto para obter detalhes do produto com base no id_produto
        dados_produto = Produto()
        
        # Consulta o código e a descrição do produto usando a API
        id_produto, codigo, descricao = dados_produto.consultar_produto_codigo_api(id_produto)

        # Cria um dicionário para consultas futuras.
        self.codigo_x_id_json[id_produto] = codigo

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
                on_select_changed=self.change_select_produtos,
            )
        )
        # Atualiza a DataTable para refletir as mudanças
        self.datatable_itens_pedido.update()
        # self.page.banner.content.controls[0].controls[1].controls[1].update()
    # ---------------------------------------------------------------------------------------------------------------------------------------


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

    def handle_change_cd_crm(self, e):
        self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
        self.pg_codigo_chamada.update() 
        self.pesquisa_fornededor(codigo_crm=self.pg_codigo_chamada.value)
        self.pg_codigo_chamada.update()

    def get_first_and_last_day_of_month(self, date):
        # Obter o primeiro dia do mês
        first_day = date.replace(day=1)
        
        # Obter o último dia do mês
        next_month = first_day.replace(month=first_day.month % 12 + 1, day=1)
        last_day = next_month - timedelta(days=1)
        
        return first_day, last_day

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

    def salvar_clicked(self, e):
        # print("Envio o dicionário modificado para a API Alterdata.")
        # pprint(self.dicionario_envio_url)
        print('Objeto enviado ao Bimer \n', json.dumps(self.dicionario_envio_url, indent=4, ensure_ascii=False))
        itens_pedido_de_compra = PedidosDeCompraItens(id_pedido_de_compra=self.id_pedido_de_compra) # Seta a classe dos itens do pedido de compra, note que envio o IdPedidoDeCompra.

        # Obtenha o DataFrame dos pedidos de compra:
        itens_pedido_de_compra.editar_pedido_de_compra_itens_api(self.dicionario_envio_url) # Captura da API os itens deste pedido de compra que eu cliquei (Como DataFrame do Pandas).

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

    def get_content(self):
        # PRIMEIRA ABA -------------------------------------------------------------------------------------------------------------------

        # Botão personalizado para realizar a filtragem
        filtrar_pedido = MyButton(text="Filtrar", on_click=self.filtrar_clicked)

        filtrar_pedido_responsivo = ft.ResponsiveRow(
            columns=12,
            spacing=0,
            controls=[filtrar_pedido],
        )        

        # Criação de uma linha responsiva contendo os campos de código da empresa, status do pedido, código de chamada e nome do fornecedor
        empresa_codigo_fornecedor = ft.ResponsiveRow(
            columns=12,
            controls=[self.pg_dd_codigo_empresa, self.pg_dd_status_pedido, self.pg_codigo_chamada, self.pg_nome_fornecedor],
        )

        # Linha responsiva contendo os campos de data e os botões de seleção de data
        tabela_dos_pedidos = ft.ResponsiveRow(
            columns=12,
            spacing=0,
            controls=[self.mytable_pedidos],
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

        # Linha responsiva contendo os campos de data e os botões de seleção de data
        datas_e_botoes = ft.ResponsiveRow(
            columns=12,
            spacing=0,
            controls=[self.txt_pick_date_start, btn_pick_date_start, spacer, self.txt_pick_date_end, btn_pick_date_end],
        )

        # SEGUNDA ABA ---------------------------------------------------------------------------------------------------------------------

        # Botão personalizado para salvar o pedido.
        enviar_alteracao_pedido = MyButton(text="Enviar Alterações", on_click=self.salvar_clicked)


        filtrar_pedido_itens_responsivo = ft.ResponsiveRow(
            columns=12,
            spacing=0,
            controls=[enviar_alteracao_pedido],
        )  
        #----------------------------------------------------------------------------------------------------------------------------------
        # Início da tela aba 0
        tela_aba_zero_inicio = ft.Container(
            expand=True,
            # bgcolor=ft.colors.AMBER,
            content=ft.Column(
                controls=[empresa_codigo_fornecedor, datas_e_botoes, tabela_dos_pedidos]
            ),
            alignment=ft.alignment.top_right
        )

        # Final da tela
        tela_aba_zero_fim = ft.Container(
            # expand=True,
            # bgcolor=ft.colors.BLUE,
            content=ft.Column(
                controls=[filtrar_pedido_responsivo]
            ),
            alignment=ft.alignment.bottom_right
        )

        # Tela aba 0 final montada.
        layout_tab0 = ft.Container(
            expand=True,
            # bgcolor=ft.colors.AMBER,
            content=ft.Column(
                controls=[tela_aba_zero_inicio, tela_aba_zero_fim]
            )
        )

        # ---------------------------------------------------------------------------------------------------------------------------

        # Início da tela aba 1
        tela_aba_um_inicio = ft.Container(
            expand=True,
            # bgcolor=ft.colors.AMBER,
            content=ft.Column(
                controls=[self.mytable_itens]
            ),
            alignment=ft.alignment.top_right
        )

        # Final da tela aba 1
        tela_aba_um_fim = ft.Container(
            # expand=True,
            # bgcolor=ft.colors.BLUE,
            content=ft.Column(
                controls=[filtrar_pedido_itens_responsivo]
            ),
            alignment=ft.alignment.bottom_right
        )

        # Tela aba 1 final montada.
        layout_tab1 = ft.Container(
            expand=True,
            # bgcolor=ft.colors.AMBER,
            content=ft.Column(
                controls=[tela_aba_um_inicio, tela_aba_um_fim]
            )
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
                        content=layout_tab0,
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
                        content=layout_tab1,
                    )                
                ),            
            ],
            selected_index=0,
            indicator_tab_size=True,
            label_color=ft.colors.GREEN,
            # width=100, # Ajuste da Largura
            height=893, # Ajuste da altura
            # expand=1,
            # on_change=lambda _: print(directory_path_or_file.value)
        )

        # Retorna o objeto 'my_tab' contendo as abas configuradas
        return my_tab
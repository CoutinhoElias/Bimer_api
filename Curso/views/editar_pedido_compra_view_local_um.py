import flet as ft
from datetime import datetime
from partials.data_table import create_datatable, my_table, sort_column
from partials.button import MyButton
from partials.all_imports import *
from database.models import PedidoDeCompraItem, Produto, CodigoProduto
from querys.qry_pedido_compra_local import PedidosDeCompra
# from querys.qry_pedido_compra_itens import PedidosDeCompraItens
# from querys.qry_pedido_compra_itens_local import PedidosDeCompraItensLocal
# from querys.qry_produto import Produto
from querys.qry_fornecedor import Fornecedor
import sys
import os
from datetime import datetime, timedelta
import json
from pprint import pprint
from configs.settings import *

# Encontrar uma maneira de criar tabela com linha em branco
# self.add_datatable_itens('', '', '', '', 'NENHUM ITEM LISTADO', 'REDEFINA SEU FILTRO', selecionado=False)

class PedidoNovoViewLocalUm:
    def __init__(self, page, app_instance):
        # Para obter acesso da página principal nesta página é preciso iniciar self.page e self.app_instance importado do init.
        # Lá no main, na chamada dessa classe deve ser enviado como parâmetro.
        self.page = page
        self.app_instance = app_instance  # Armazena a instância da classe App

        self.id_fornecedor = None
        self.pedidos_dict = {}

        self.list_tile = ft.Ref[ft.Column]()
        self.tb_tabela = ft.Ref[ft.DataTable]()
        self.tb_tabela_itens_pedido = ft.Ref[ft.DataTable]()
        self.selecionado = ft.Ref[ft.ListTile]()

        self.itens_dict = {}
        self.itens_excluir = []

        # Botão personalizado para realizar a filtragem
        self.filtrar_pedido = MyButton(text="Filtrar", on_click=self.filtrar_clicked)

        # ============================================================================================================================= 
        # Jogue aqui seus estilos:

        # Estilo para os butões de data.   
        self.button_style = ft.ButtonStyle(
                                        shape={
                                            ft.MaterialState.HOVERED: ft.CircleBorder(),
                                            ft.MaterialState.DEFAULT: ft.CircleBorder(),
                                        },
                                    )
        # =============================================================================================================================

        # Lista para armazenar o estado dos switches
        self.switches_state = []

        # LISTA DE ITENS DO PEDIDO
        self.colunas_dos_itens_dos_pedidos = [
            ft.DataColumn(ft.Text("Código",  width=47,), on_sort=sort_column,),
            ft.DataColumn(ft.Text("Descricao", width=460), on_sort=sort_column,),
            ft.DataColumn(ft.Text("Qde.", width=50),  numeric=True, on_sort=sort_column,),
            ft.DataColumn(ft.Text("Valor Unit.", width=50),  numeric=True, on_sort=sort_column,),
            ft.DataColumn(ft.Text("IPI", width=40), numeric=True, on_sort=sort_column,), 
            ft.DataColumn(ft.Text("ICMS", width=40), numeric=True, on_sort=sort_column,), 
            ft.DataColumn(ft.Text("Vl. Total", width=80),  numeric=True, on_sort=sort_column,),
        ]

        self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.colunas_dos_itens_dos_pedidos)
        self.table_order_items = my_table(self.datatable_itens_pedido)


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

        self.pg_codigo_chamada = ft.TextField(
            label="Código", 
            hint_text="FORNECEDOR",
            col={"md": 2},
            focused_border_color=ft.colors.ORANGE_300,
            input_filter=ft.NumbersOnlyInputFilter(),
            # text_style=input_style,
            on_blur = self.handle_change_cd_crm, 
        )

        self.pg_codigo_chamada_pedido = ft.TextField(
            label="Código do Pedido", 
            hint_text="CÓDIGO DO PEDIDO",
            col={"md": 2},
            focused_border_color=ft.colors.ORANGE_300,
            input_filter=ft.NumbersOnlyInputFilter(),
            # text_style=input_style,
            on_blur = self.handle_change_cd_pedido, 
        )

        self.pg_nome_fornecedor = ft.TextField(
            label="Nome", 
            hint_text="FORNECEDOR",
            col={"md": 7},
            focused_border_color=ft.colors.ORANGE_300,
        )

        self.pg_dd_codigo_empresa = ft.Dropdown(
            col={"md": 2},
            label="Escolha Empresa",
            hint_text="Empresa",
            value="04",
            focused_border_color=ft.colors.ORANGE_300,
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
            focused_border_color=ft.colors.ORANGE_300,
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
            focused_border_color=ft.colors.ORANGE_300,
            # icon=ft.icons.DATE_RANGE,
        )

        self.txt_pick_date_end = ft.TextField(
            label="Dt. Fim", 
            hint_text="Dt. Final",
            col={"md": 2},
            focused_border_color=ft.colors.ORANGE_300,
            # icon=ft.icons.DATE_RANGE,
        )

        self.filtrar_pedido_responsivo = ft.ResponsiveRow(
            columns=12,
            spacing=0,
            controls=[self.filtrar_pedido],
            col={"md": 1.5},
        ) 

        self.coluna_um = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            controls=[  # Use "controls" para passar uma lista de controles
                ft.Card(
                    content=ft.Container(
                        width=500,
                        content=ft.Column(
                            ref=self.list_tile,
                            controls=[], # self.create_list_tiles(),  # Cria os ListTiles dinamicamente
                            spacing=0,
                            # scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
                            # on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos 
                        ),
                        padding=ft.padding.symmetric(vertical=10),
                    )
                )
            ],
            scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
            on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos 
        )


        # Botão de ícone para selecionar a data inicial
        self.btn_pick_date_start = ft.IconButton(
            icon=ft.icons.DATE_RANGE,
            icon_color="blue400",
            icon_size=30,
            tooltip="Data Inicial.",
            col={"md": .6},
            style=self.button_style,
            on_click=lambda e: page.open(self.create_date_picker()), 
        )

        # Botão de ícone para selecionar a data final
        self.btn_pick_date_end = ft.IconButton(
            icon=ft.icons.DATE_RANGE,
            icon_color="blue400",
            icon_size=30,
            tooltip="Data Final.",
            col={"md": .6},
            style=self.button_style,
            on_click=lambda e: page.open(self.create_date_picker_end()),
        )

        # Espaçador para ajuste do layout
        self.spacer = ft.Container(col={"md": .4})

        # Criação de uma linha responsiva contendo os campos de código da empresa, status do pedido, código de chamada e nome do fornecedor
        self.empresa_codigo_fornecedor = ft.ResponsiveRow(
            columns=12,
            controls=[self.pg_dd_codigo_empresa, self.pg_dd_status_pedido, self.pg_codigo_chamada, self.pg_nome_fornecedor],
        )

        # Linha responsiva contendo os campos de data e os botões de seleção de data
        self.datas_e_botoes = ft.ResponsiveRow(
            columns=12,
            spacing=0,
            controls=[self.txt_pick_date_start, self.btn_pick_date_start, self.spacer, self.txt_pick_date_end, self.btn_pick_date_end, self.pg_codigo_chamada_pedido, self.spacer, self.filtrar_pedido_responsivo],
        )

        # Botão personalizado para realizar a filtragem
        self.botao_criar_pedido = ft.ResponsiveRow(
            columns=12,
            controls=[MyButton(text="Salvar Pedido", on_click=self.delete_rows)],
        )

        self.coluna_esquerda = ft.Container(
            # bgcolor=ft.colors.BLUE,
            # expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                controls=[self.coluna_um]
            ),
            alignment=ft.alignment.center
        )

        self.coluna_direita = ft.Container(
            # bgcolor=ft.colors.RED,
            expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                controls=[self.mytable_itens]
            ),
            alignment=ft.alignment.top_left
        )

        # Tela aba 1 final montada.
        self.lista_e_tabela = ft.Container(
            expand=True,
            # bgcolor=ft.colors.AMBER,
            content=ft.Row(
                controls=[self.coluna_esquerda, self.coluna_direita]
            )
        )

        # Início da tela aba 1
        self.tela_inicio = ft.Container(
            expand=False,
            # bgcolor=ft.colors.AMBER,
            content=ft.Column(
                controls=[self.empresa_codigo_fornecedor, self.datas_e_botoes]
            ),
            alignment=ft.alignment.top_right
        )

        self.tela_meio = ft.Container(
            expand=True,
            content=ft.Column(
                controls=[self.lista_e_tabela]
            ),
            alignment=ft.alignment.top_left
        )

        # Final da tela aba 1
        self.tela_fim = ft.Container(
            expand=False,
            # bgcolor=ft.colors.BLUE,
            content=ft.Column(
                controls=[self.botao_criar_pedido]
            ),
            alignment=ft.alignment.bottom_right
        )
    # -----------------------------------------------------------------------------------

    def excluir_itens_pedido_compra(self, ids_itens_pedido):
        # Verifica se a lista de IDs não está vazia
        if not ids_itens_pedido:
            print("Nenhum item para excluir.")
            return

        try:
            # Realiza a exclusão dos itens cujo IdPedidoDeCompraItem está na lista fornecida
            session.query(PedidoDeCompraItem).filter(
                PedidoDeCompraItem.IdPedidoDeCompraItem.in_(ids_itens_pedido)
            ).delete(synchronize_session=False)

            # Confirma a exclusão
            session.commit()
            print("Itens excluídos com sucesso.")
        except Exception as e:
            # Em caso de erro, desfaz as alterações
            session.rollback()
            print(f"Erro ao excluir itens: {e}")

    def obter_itens_pedido_compra(self, id_pedido):
        # Realiza a consulta para obter os itens do pedido de compra
        itens = session.query(
                    PedidoDeCompraItem.IdProduto, PedidoDeCompraItem.IdPedidoDeCompra, PedidoDeCompraItem.IdPedidoDeCompraItem, PedidoDeCompraItem.QtPedida, PedidoDeCompraItem.VlUnitario, PedidoDeCompraItem.VlIPI, PedidoDeCompraItem.VlICMS, PedidoDeCompraItem.VlItem,
                    Produto.NmProduto,
                    CodigoProduto.CdChamada)\
                .join(CodigoProduto, PedidoDeCompraItem.IdProduto == CodigoProduto.IdProduto)\
                .join(Produto, CodigoProduto.IdProduto == Produto.IdProduto)\
                .filter(
                    # CodigoProduto.CdChamada == self.cd_produto,
                    CodigoProduto.StCodigoPrincipal == 'S',
                    CodigoProduto.IdTipoCodigoProduto == '00A0000002',
                    PedidoDeCompraItem.IdPedidoDeCompra == id_pedido
                ).all()

        # print(itens) Sem .all()
        # for pedido_de_compra_item, produto, codigo_produto in itens:
        #     print("Pedido de Compra Item:")
        #     print(vars(pedido_de_compra_item))  # Imprime as colunas de PedidoDeCompraItem
            
        #     print("\nProduto:")
        #     print(vars(produto))  # Imprime as colunas de Produto
            
        #     print("\nCodigo Produto:")
        #     print(vars(codigo_produto))  # Imprime as colunas de CodigoProduto
        #     print("-" * 50)
        
        # Cria uma instância da classe Produto para obter detalhes do produto com base no id_produto
        dados_produto = Produto()
        
        # # Consulta o código e a descrição do produto usando a API
        # id_produto, codigo, descricao = dados_produto.consultar_produto_codigo_api(id_produto)
        
        # # Transforma o resultado em uma lista de dicionários
        # itens_dict = [
        #     {
        #         'IdentificadorProduto': item.IdProduto,
        #         'IdPedidoDeCompra': item.IdPedidoDeCompra,
        #         'IdPedidoDeCompraItem': item.IdPedidoDeCompraItem,
        #         'CdItem': item.IdProduto,
        #         'QuantidadePedida': item.QtPedida,
        #         'ValorUnitario': round(item.VlUnitario, 4),
        #         'ValorIcms': round(item.VlICMS, 4),
        #         'ValorIPI': round(item.VlIPI, 4),
        #         'ValorItem': round(item.VlItem, 4),
        #     }
        #     for item in itens
        # ]

        itens_dict = [
            {
                'IdentificadorProduto': item.IdProduto,
                'IdPedidoDeCompra': item.IdPedidoDeCompra,
                'IdPedidoDeCompraItem': item.IdPedidoDeCompraItem,
                # 'CdItem': item.IdProduto,
                'QuantidadePedida': item.QtPedida,
                'ValorUnitario': round(item.VlUnitario, 4),
                'ValorIcms': round(item.VlICMS, 4),
                'ValorIPI': round(item.VlIPI, 4),
                'ValorItem': round(item.VlItem, 4),
                # Os valores da consulta são obtidos uma única vez e reutilizados
                'IdProduto': item.IdProduto,
                'CodigoProduto': item.CdChamada,
                'DescricaoProduto': item.NmProduto,
            }
            # Aqui a consulta só ocorre uma vez e seus resultados são armazenados na variável `produto`
            for item in itens
            # for produto in [dados_produto.consultar_produto_codigo_api(item.IdProduto)]
        ]

        # print(json.dumps(itens_dict, indent=4))

        # Cria o DataFrame a partir da lista de dicionários
        df = pd.DataFrame(itens_dict)

        return itens_dict

    def create_list_tiles(self):
        # Limpa a coluna antes de adicionar novos ListTiles
        self.list_tile.current.controls.clear()
        self.switches_state.clear()
        self.coluna_um.update()

        # Itera sobre os itens do dicionário self.pedidos_dict
        for index, (key, item) in enumerate(self.pedidos_dict.items()):
            def on_switch_change(e, idx=index):
                # Desativa todos os outros switches
                for i, switch in enumerate(self.switches_state):
                    if i != idx:
                        switch.value = False
                        switch.update()
                # Atualiza o estado do switch clicado
                self.pedidos_dict[key]["Selecionado"] = e.control.value
                self.switches_state[idx].value = e.control.value
                self.switches_state[idx].update()

            # Função chamada ao clicar no ListTile
            def on_tile_click(e, item=item):
                # Coleta o ListTile clicado
                list_tile = e.control

                for control in self.list_tile.current.controls:
                    if isinstance(control, ft.ListTile):
                        # Set the selected property to False for all ListTiles
                        control.selected = False
                        control.update()

                list_tile.selected = True
                list_tile.update()
                # print(self.selecionado.current)

                loading = ft.AlertDialog(
                    content=ft.Container(
                        content=ft.ProgressRing(),
                        alignment=ft.alignment.center,
                    ),
                    bgcolor=ft.colors.TRANSPARENT,
                    modal=True,
                    disabled=True,
                )
                self.page.open(loading)

                pedido_id = item["IdPedidoDeCompra"]  # Coleta o valor diretamente do dicionário
                print(f"Pedido clicado: {pedido_id}")

                # itens_pedido_de_compra = PedidosDeCompraItensLocal(id_pedido_de_compra=pedido_id) # Seta a classe dos itens do pedido de compra, note que envio o IdPedidoDeCompra.
                self.itens_dict = self.obter_itens_pedido_compra(pedido_id)
                # print(json.dumps(self.itens_dict, indent=4))

                self.datatable_itens_pedido.rows = [] # Limpa a lista de produtos da tabela antes de adicionar a nova listagem.
                # self.codigo_x_id_json = {} # Limpa o dicionário para próxima consulta.


                for row in self.itens_dict:
                    self.add_datatable_itens_pedido(
                        codigo_produto=row['CodigoProduto'],
                        id_produto=row['IdentificadorProduto'], 
                        descricao_produto=row['DescricaoProduto'],
                        quantidade=row['QuantidadePedida'], 
                        valor_unitario=row['ValorItem'], 
                        valor_item=row['ValorUnitario'], 
                        valor_icms=row['ValorIcms'], 
                        valor_ipi=row['ValorIPI'], 
                        selecionado=False
                    )

                # sleep(3)
                self.page.close(loading)

            # Cria o Switch
            switch = ft.Switch(value=item["Selecionado"], on_change=on_switch_change)
            self.switches_state.append(switch)

            # Verifica se as chaves existem no dicionário antes de criar o ListTile
            if "CdChamada" in item and "IdPedidoDeCompra" in item and "DtEmissao" in item and "DtEntrega" in item:
                # Adiciona o ListTile com a função de clique
                self.list_tile.current.controls.append(
                    ft.ListTile(
                        ref=self.selecionado,
                        leading=ft.Text(item["CdChamada"], style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=15)),
                        title=ft.Text(f"Fornecedor: {item['CdFornecedor'].strip()} - {item['NmFornecedor']}"),
                        subtitle=ft.Text(f"Emissão: {item['DtEmissao']} - Entrega: {item['DtEntrega']}"),
                        # trailing=switch,
                        toggle_inputs=True,
                        on_click=lambda e, item=item: on_tile_click(e, item),  # Passa o item no clique
                        selected=False,
                        selected_color=ft.colors.ORANGE_300,
                    )
                )
            else:
                print(f"Chaves faltando no item {index}")

        # Atualiza a coluna após adicionar todos os ListTiles
        self.coluna_um.update()
        return self.list_tile.current.controls

    # TABELA DE ITENS DO PEDIDO
    def add_datatable_itens_pedido(self, codigo_produto, id_produto, descricao_produto, quantidade, valor_unitario, valor_item, valor_icms, valor_ipi, selecionado=False):

        # Adiciona uma nova linha à DataTable 'self.datatable_itens_pedido'
        self.datatable_itens_pedido.rows.append(
            ft.DataRow(
                cells=[
                    # Adiciona uma célula com o valor 'codigo' do produto
                    ft.DataCell(ft.Text(value=codigo_produto)),
                    
                    # Adiciona uma célula com a 'descricao' do produto
                    ft.DataCell(ft.Text(descricao_produto)),
                    
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
                on_select_changed = self.change_select_itens,

                # Define o manipulador de eventos para mudança de seleção da linha
                # on_select_changed=self.change_select_produtos,
            )
        )
        # Atualiza a DataTable para refletir as mudanças
        self.datatable_itens_pedido.update()
        # self.page.banner.content.controls[0].controls[1].controls[1].update()

    def buscar_id_produto_por_codigo(self, codigo_produto):
        for item in self.itens_dict:
            if item["CodigoProduto"] == codigo_produto: # .strip()
                print(f'Encontrei {item["CodigoProduto"]} igual a {codigo_produto}')
                return item["IdPedidoDeCompraItem"]
        return None  # Caso o código não seja encontrado

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # IDENTIFICANDO PEDIDO SELECIONADO - Order
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def change_select_itens(self, e):
        e.control.selected = not e.control.selected
        e.control.update()

        # Captura a linha selecionada diretamente do evento
        selected_row = e.control  
        # Captura o valor da célula da primeira coluna
        selected_cell_value = selected_row.cells[0].content.value
        # Busca o ID do produto baseado no valor da célula selecionada
        elemento = self.buscar_id_produto_por_codigo(selected_cell_value) #.strip()

        if e.control.selected:
            # Adiciona à lista caso a linha esteja selecionada
            if elemento not in self.itens_excluir:
                self.itens_excluir.append(elemento)
        else:
            # Remove da lista caso a linha seja desmarcada
            if elemento in self.itens_excluir:
                self.itens_excluir.remove(elemento)
            # print(f'Deselected**** {elemento}')

        print(self.itens_excluir) # PRECISO AGORA EXCLUIR DO PEDIDO DE COMPRA USANDO ESTA LISTA

    def delete_rows(self, e):
        rows = self.datatable_itens_pedido.rows[:]

        for row in rows:
            if row.selected:
                self.datatable_itens_pedido.rows.remove(row)

        self.excluir_itens_pedido_compra(self.itens_excluir)

        self.datatable_itens_pedido.update()

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
                on_select_changed = self.change_select_itens,
            )
        )
        # Atualiza a DataTable para refletir as mudanças
        self.datatable.update()
        # self.page.banner.content.controls[0].controls[1].controls[1].update()


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

    # def handle_change_cd_crm(self, e):
    #     print(e)
    #     self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
    #     self.pg_codigo_chamada.update() 
    #     self.pesquisa_fornededor(codigo_crm=self.pg_codigo_chamada.value)
    #     self.pg_codigo_chamada.update()

    def get_first_and_last_day_of_month(self, date):
        # Obter o primeiro dia do mês
        first_day = date.replace(day=1)
        
        # Obter o último dia do mês
        next_month = first_day.replace(month=first_day.month % 12 + 1, day=1)
        last_day = next_month - timedelta(days=1)
        
        return first_day, last_day

    def pesquisa_pedidos(self):
        if self.pg_codigo_chamada_pedido.value == '':
            # Obtenha a data inicial do campo de texto e converta para objeto datetime
            data_ini = self.txt_pick_date_start.value                
            data_ini_obj = datetime.strptime(data_ini, '%d/%m/%Y')

            # Obtenha a data final do campo de texto e converta para objeto datetime
            data_fim = self.txt_pick_date_end.value                
            data_fim_obj = datetime.strptime(data_fim, '%d/%m/%Y')        

            # Converta os objetos datetime para strings no formato YYYY-MM-DD
            data_ini = data_ini_obj.strftime('%Y-%m-%d')
            data_fim = data_fim_obj.strftime('%Y-%m-%d')    
        else:
            self.txt_pick_date_start.value = None
            self.txt_pick_date_end.value = None
            self.txt_pick_date_start.update()
            self.txt_pick_date_end.update()
            data_ini = None
            data_fim = None

        try:
            # Crie uma instância da classe PedidosDeCompra com os parâmetros fornecidos
            db_handler = PedidosDeCompra(
                connection_string=connection_string,
                cd_empresa=self.pg_dd_codigo_empresa.value,
                codigo_crm=self.pg_codigo_chamada.value,
                pg_codigo_chamada_pedido=self.pg_codigo_chamada_pedido.value, # <<<=====
                id_fornecedor=self.id_fornecedor,
                status=self.pg_dd_status_pedido.value,
                dt_emissao_ini=data_ini,
                dt_emissao_fim=data_fim
            )
            
            # Obtenha os pedidos de compra filtrados
            pedidos_de_compras = db_handler.get_all_pedidos_de_compras_filtered()
            # print(pedidos_de_compras)

            self.pedidos_dict = {
                pedido.CdChamada.strip(): {
                    "CdChamada": pedido.CdChamada.strip(),
                    "IdPedidoDeCompra": pedido.IdPedidoDeCompra,
                    "StPedidoDeCompra": pedido.StPedidoDeCompra,
                    "CdFornecedor": pedido.CdFornecedor,
                    "NmFornecedor": pedido.NmCurto,
                    "DtEmissao": pedido.DtEmissao.strftime("%d/%m/%Y") if pedido.DtEmissao else None,
                    "DtEntrega": pedido.DtEntrega.strftime("%d/%m/%Y") if pedido.DtEntrega else None,
                    "DsPedidoDeCompra": pedido.DsPedidoDeCompra,
                    "DsObservacao": pedido.DsObservacao,
                    "Selecionado": False
                }
                for pedido in pedidos_de_compras
            }
            # print(self.pedidos_dict)
            # print('Objeto enviado ao Bimer \n', json.dumps(self.pedidos_dict, indent=4, ensure_ascii=False))
        
        except Exception as e:
            # Captura e imprime qualquer erro ocorrido durante a busca dos pedidos
            print(f"Erro ao buscar pedidos: {e}")
            return {}

        # Retorne o dicionário com os pedidos
        self.create_list_tiles()
        # self.coluna_um.update()
        # print(self.container_pedido.current.content.controls,  '<<<<<======')
        # self.container_pedido.current.content.controls=self.pedidos_dict

        # self.page.update()
        return self.pedidos_dict

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
        # self.datatable.rows = [] <<<======

    def salvar_clicked(self, e):
        # print("Envio o dicionário modificado para a API Alterdata.")
        # pprint(self.dicionario_envio_url)
        print('Objeto enviado ao Bimer \n', json.dumps(self.pedidos_dict, indent=4, ensure_ascii=False))
        # itens_pedido_de_compra = PedidosDeCompraItens(id_pedido_de_compra=self.id_pedido_de_compra) # Seta a classe dos itens do pedido de compra, note que envio o IdPedidoDeCompra.

        # Obtenha o DataFrame dos pedidos de compra:
        # itens_pedido_de_compra.editar_pedido_de_compra_itens_api(self.dicionario_envio_url) # Captura da API os itens deste pedido de compra que eu cliquei (Como DataFrame do Pandas).

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
        self.txt_pick_date_start.update()

    def handle_date_change_end(self, e):
        self.txt_pick_date_end.value = e.control.value.strftime('%d/%m/%Y')
        self.txt_pick_date_end.update()

    def handle_change_cd_crm(self, e):
        print(e.control.value)
        self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
        self.pg_codigo_chamada.update() 
        self.pesquisa_fornededor(codigo_crm=self.pg_codigo_chamada.value)
        self.pg_codigo_chamada.update()

    def handle_change_cd_pedido(self, e):
        print(e.control.value)
        if self.pg_codigo_chamada_pedido.value != '':
            self.pg_codigo_chamada_pedido.value = self.pg_codigo_chamada_pedido.value.zfill(6)
            self.pg_codigo_chamada_pedido.update() 

    def handle_date_dismissal(self, e):
        self.page.add(ft.Text("DatePicker dismissed"))
        self.page.update()

    def get_content(self):
        # Tela aba 0 final montada.
        layout = ft.Container(
            expand=True,
            # bgcolor=ft.colors.AMBER,
            content=ft.Column(
                controls=[self.tela_inicio, self.tela_meio, self.tela_fim]
            )
        )

        # Retorna o objeto 'my_tab' contendo as abas configuradas
        return layout
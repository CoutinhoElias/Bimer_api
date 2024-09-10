import flet as ft
import json
from datetime import datetime

import pandas as pd


from partials.data_table import create_datatable, my_table
from partials.button import MyButton
# from querys.qry_pedidos_compra import PedidosDeCompra
from querys.qry_pedido_compra_itens import PedidosDeCompraItens
from querys.qry_fornecedor import Fornecedor

# Encontrar uma maneira de criar tabela com linha em branco
# self.add_datatable_itens('', '', '', '', 'NENHUM ITEM LISTADO', 'REDEFINA SEU FILTRO', selecionado=False)

class PedidoNovoView:
    def __init__(self, page):
        self.page = page
        self.id_fornecedor = None

        self.df_itens_planilha = None
        self.dicionario_final = {}

        # Seta a classe dos itens do pedido de compra, note que envio um ID qualquer pois neste ponto não será necessário.
        self.itens_pedido_de_compra = PedidosDeCompraItens(id_pedido_de_compra='ASDFG1234') 

        # Definição do Ref().
        self.tb_tabela = ft.Ref[ft.DataTable]()
        self.tb_tabela_itens_pedido = ft.Ref[ft.DataTable]()
        self.tb_tab_pedido = ft.Ref[ft.Tab]()

        # ============================================================================================================================= 

        # LISTA DE ITENS DO PEDIDO
        self.campos_pedido_itens = [
            ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Descricao", width=80), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Und", width=29), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Preço", width=40), numeric=True, on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Icms", width=30), numeric=True, on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Ipi", width=30), numeric=True, on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Observacao", width=90, text_align="LEFT"), numeric=False,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
            ft.DataColumn(ft.Text("Informações Gerais", width=90, text_align="LEFT"), numeric=False,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
        ]

        self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.campos_pedido_itens)
        self.table_order_items = my_table(self.datatable_itens_pedido)
        # ---------------------------------------------------------------------------------------------------------------------------------------

        # Inicialização do FilePicker e texto para exibir arquivos selecionados
        self.selected_files = ft.Text()
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)

        self.dialogo = ft.AlertDialog(
            title=ft.Text(value="Não encontrei este código"), 
            content=ft.Text(value="Continue seu trabalho!"),
            title_padding=ft.padding.all(10),
            content_padding=ft.padding.all(10),
            shape=ft.RoundedRectangleBorder(radius=5),        
            on_dismiss=lambda e: print("Dialog dismissed!")
        )
    # =============================================================================================================================
    def open_dialogo(self, e):
        self.dialogo.title = ft.Text(e)
        self.page.dialog = self.dialogo
        self.dialogo.open = True
        self.page.update()
    # =============================================================================================================================

    def filtrar_clicked(self, e):
        self.pesquisa_pedidos()
        self.datatable.rows = []
        # print("Cancel clicked")

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
                # print(selected_cell_value)
                self.tb_tab_pedido.current.selected_index = 1
                self.tb_tab_pedido.current.update()
        else:
            print('Deselected')

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # POPULANDO TABELAS
    # ---------------------------------------------------------------------------------------------------------------------------------------

    # TABELA DE ITESN DO PEDIDO
    def add_datatable_itens_pedido(self, codigo, descricao, und, preco, icms, ipi, observacao, informacoes_gerais, selecionado=False):
        self.datatable_itens_pedido.rows.append(
            ft.DataRow(
                [
                    ft.DataCell(ft.Text(value=codigo)),
                    ft.DataCell(ft.Text(descricao)),
                    ft.DataCell(ft.Text(und)),
                    ft.DataCell(ft.Text(preco)),
                    ft.DataCell(ft.Text(icms)),
                    ft.DataCell(ft.Text(ipi)),
                    ft.DataCell(ft.Text(observacao)),
                    ft.DataCell(ft.Text(informacoes_gerais)),
                ],
                selected=selecionado,
                on_select_changed = self.change_select,
            )
        )
        self.datatable_itens_pedido.update()
        # self.page.banner.content.controls[0].controls[1].controls[1].update()
    # ---------------------------------------------------------------------------------------------------------------------------------------

    def preenche_tabela(self):
        for row in self.df_itens_planilha.itertuples(index=False, name='Pandas'):
            # print(f"Índice: {row.Index}")
            # print(f"Valor da coluna: {row}")
            self.add_datatable_itens_pedido(row.codigo_produto, row.nome_produto, row.und, row.preco, row.icms, row.ipi, row.observacao, row.informacoes_gerais, selecionado=False)
            

    def criar_pedido_clicked(self, e):
        # print("Chamou botão de arquivo!")
        # print(json.dumps(self.dicionario_final, indent=4))
        resposta = self.itens_pedido_de_compra.criar_pedido_de_compra_itens_api(self.dicionario_final)
        
        self.open_dialogo(f"Pedido {resposta['ListaObjetos'][0]['Codigo']} criado com sucesso!")
        self.datatable_itens_pedido.rows = []
        self.datatable_itens_pedido.update()

    def transformar_df_em_dicionario(self):
        # Crie a lista de itens a partir do dataframe
        itens = []
        total_pagamentos = 0
        id_fornecedor = None
        for _, row in self.df_itens_planilha.iterrows():
            item = {
                # "IdentificadorAplicacao": "",
                "IdentificadorProduto": row["id_produto"],
                # "IdentificadorProdutoLote": row["IdentificadorProdutoLote"],
                "IdentificadorUnidade": row["id_unidade"], 
                "Bonificacao": row.get("Bonificacao", False),  # Valor padrão True
                "DataEntrega": row.get("DataEntrega", datetime.now().isoformat()),  # Data padrão
                "DataValidade": row.get("DataValidade", datetime.now().isoformat()),  # Data padrão
                "Observacao": row.get("observacao", "Item do pedido cadastrado pela api"), # xxxxxxxxxxxxx
                # "QuantidadeEmbalagem": row["QuantidadeEmbalagem"],
                "QuantidadePedida": row["quantidade"], # <<<<===== A quantidade na planilha
                "ValorUnitario": row["preco"], # <<<<===== O valor unitário na planilha
                "Status": row.get("Status", "A"),
                "IdentificadorNaturezaLancamento": "00A0000030",
                "LancamentosCentroCusto": [
                    {
                        "AliquotaPorcentagem": row.get("AliquotaPorcentagem", 100),
                        "IdentificadorCentroDeCusto": "00A000001D",
                        # "DataLancamento": row.get("DataLancamento", datetime.now().isoformat()),  # Data padrão
                        "QuantidadeLancamento": row["quantidade"],
                        "ValorLancamento":  round(float(row["quantidade"]) * float(row["preco"]), 4) # row["preco"]
                    }
                ]
            }
            id_fornecedor = row["id_fornecedor"]
            total_pagamentos = total_pagamentos + round(float(row["quantidade"]) * float(row["preco"]), 4) # <<<<===== O total calculado
            itens.append(item)
        
        # Preencha o dicionário final
        dicionario_final = {
            "Itens": itens,
            "Pagamentos": [
                {
                    # "IdentificadorContaBancaria": "00A0000001",# xxxxxxxxxxxxx
                    "IdentificadorFormaPagamento": "00A0000003",
                    "AliquotaParcela": 100,
                    "Antecipado": False,
                    "DataReferencia": datetime.now().isoformat(),
                    "NumeroDias": 15,
                    "Valor": round(total_pagamentos,4)
                }
            ],
            "CodigoEmpresa": 4,
            "CodigoEmpresaFinanceiro": 4,
            # "IdentificadorBairro": "00A0000001",# xxxxxxxxxxxxx
            # "IdentificadorCidade": "00A0000001",# xxxxxxxxxxxxx
            "IdentificadorFornecedor": id_fornecedor,# xxxxxxxxxxxxx
            # "IdentificadorIndexador": "00A0000001",# xxxxxxxxxxxxx
            "IdentificadorNaturezaLancamento": "00A0000030",# xxxxxxxxxxxxx
            # "IdentificadorTransportador": "00A0000001",# xxxxxxxxxxxxx
            # "IdentificadorUsuarioLiberacao": "00A0000001",# xxxxxxxxxxxxx
            # "ValorAcrescimo": 0,
            # "ValorDesconto": 0,
            # "ValorFrete": 0,
            # "ValorSeguro": 0,
            # "ValorOutrasDespesas": 0,
            # "ValorACT": 0,
            # "ConhecimentoTransporte": {
            #     "TransportePagamentos": [
            #         {
            #             "IdentificadorContaBancaria": "00A0000001",
            #             "IdentificadorFormaPagamento": "00A0000001",
            #             "NumeroTitulo": "123456",
            #             "DataReferencia": "2020-06-10T17:53:34.896Z",
            #             "NumeroDias": 15,
            #             "AliquotaParcela": 10,
            #             "ValorParcela": 10
            #         }
            #     ],
            #     "PrazoTransporte": {
            #         "Identificador": "00A0000001",
            #         "IdentificadorFormaPagamentoEntrada": "00A0000001",
            #         "IdentificadorFormaPagamentoParcelas": "00A0000001"
            #     }
            # },
            # "TipoFrete": "D",
            # "CEP": "25123123",
            # "Codigo": "00001",
            # "ComplementoEndereco": "Apto 123",
            "DataEmissao": datetime.now().isoformat(),
            # "DataEmissaoACT": "2020-06-10T17:53:34.896Z",
            "DataEntrega": datetime.now().isoformat(),
            # "Descricao": "Pedido cadastrado pela BimerAPI",
            # "IdentificadorEntidadeOrigem": "00A0000001",
            # "NomeEntidadeOrigem": "Entidade",
            # "EntregaParcial": False,
            # "Logradouro": "Avenida principal",
            # "NumeroEndereco": "400",
            # "NumeroOrcamento": "123",
            # "Observacao": "Cadastrado pela Bimer API",
            # "Prazo": {
            #     "Identificador": "00A0000001",# xxxxxxxxxxxxx
            #     "IdentificadorFormaPagamentoEntrada": "00A0000001",# xxxxxxxxxxxxx
            #     "IdentificadorFormaPagamentoParcelas": "00A0000001"# xxxxxxxxxxxxx
            # },
            # "TipoLogradouro": "A",
            # "UF": "RJ",
            # "Status": "A"
        }
        
        return dicionario_final

    # Exemplo de uso:
    # dicionario = transformar_df_em_dicionario(df_itens_planilha)


    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            # Concatena o caminho completo do diretório com o nome do arquivo
            file_paths = [f.path for f in e.files]
            self.selected_files.value = "\n".join(file_paths)
            
            self.df_itens_planilha = self.itens_pedido_de_compra.ler_arquivo_pedido_de_compra(self.selected_files.value)
            self.preenche_tabela()
            self.dicionario_final = self.transformar_df_em_dicionario()

            # print(json.dumps(dicionario, indent=4))

        else:
            self.selected_files.value = "Cancelado!"
        self.selected_files.update()
        self.page.update()

    def get_content(self):
        # Botão personalizado para realizar a filtragem
        botao_criar_pedido = ft.ResponsiveRow(
            columns=12,
            controls=[MyButton(text="Criar Pedido", on_click=self.criar_pedido_clicked)],
        )

        # Botão para selecionar arquivos
        file_picker_button = MyButton(
            text="Selecionar Arquivo",
            on_click=lambda _: self.pick_files_dialog.pick_files(
                                    file_type=ft.FilePickerFileType.CUSTOM, 
                                    allowed_extensions=["xls", "xlsx"], 
                                    allow_multiple=False
                                ),
        )

        file_and_button =  ft.Row( 
                controls = [file_picker_button, self.selected_files], 
            )

        self.mytable_itens = ft.Column(
            expand=True,
            controls=[
                ft.Row( 
                    controls = [self.datatable_itens_pedido], 
                    scroll = ft.ScrollMode.ALWAYS
                )
            ],
            scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
            on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos           
        ) 

        # Início da tela aba 1
        tela_inicio = ft.Container(
            expand=False,
            # bgcolor=ft.colors.AMBER,
            content=ft.Column(
                controls=[file_and_button]
            ),
            alignment=ft.alignment.top_right
        )

        tela_meio = ft.Container(
            expand=True,
            content=ft.Column(
                controls=[self.mytable_itens]
            ),
            alignment=ft.alignment.top_left
        )

        # Final da tela aba 1
        tela_fim = ft.Container(
            expand=False,
            # bgcolor=ft.colors.BLUE,
            content=ft.Column(
                controls=[botao_criar_pedido]
            ),
            alignment=ft.alignment.bottom_right
        )

        # Tela aba 1 final montada.
        layout_fim = ft.Container(
            expand=True,
            # bgcolor=ft.colors.AMBER,
            content=ft.Column(
                controls=[tela_inicio, tela_meio, tela_fim]
            )
        )

        return layout_fim

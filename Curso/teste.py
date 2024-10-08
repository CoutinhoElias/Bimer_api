# import json

# def transformar_dicionario(dicionario_original, tipo_cadastro_novo=None, identificador_produto=None):
#     # Função auxiliar para mapear um item
#     def mapear_item(item, tipo_cadastro):
#         return {
#             "IdentificadorPedidoDeCompraItem": item["Identificador"],
#             "TipoCadastro": tipo_cadastro,
#             "IdentificadorAplicacao": item.get("IdentificadorAplicacao", "00A0000001"),
#             "IdentificadorProduto": item["IdentificadorProduto"],
#             "IdentificadorProdutoLote": item.get("ProdutoLote", "00A0000001"),
#             "IdentificadorUnidade": item["IdentificadorUnidade"],
#             "Bonificacao": item["Bonificacao"],
#             "DataEntrega": item["DataEntrega"],
#             "DataValidade": item["DataValidade"],
#             "Observacao": item["Observacao"],
#             "QuantidadeEmbalagem": item["QuantidadeEmbalagem"],
#             "QuantidadePedida": item["QuantidadePedida"],
#             "ValorUnitario": item["ValorUnitario"]
#         }

#     # Mapeamento dos itens e ajuste dos totais
#     itens = []
#     valor_acrescimo = 0
#     valor_desconto = 0
#     valor_frete = 0
#     valor_seguro = 0
#     valor_outras_despesas = 0
#     valor_act = 0

#     for item in dicionario_original["Itens"]:
#         # Usamos get para evitar KeyError se a chave não existir
#         tipo_cadastro = item.get("TipoCadastro", None)

#         # Se o identificador do produto for o que desejamos alterar
#         if identificador_produto and item["IdentificadorProduto"] == identificador_produto:
#             tipo_cadastro = tipo_cadastro_novo

#         # Mapear item com o tipo_cadastro atualizado
#         itens.append(mapear_item(item, tipo_cadastro))

#         # Calcular totais apenas se tipo_cadastro for I ou A
#         if tipo_cadastro in ['I', 'A']:
#             valor_acrescimo += item["ValorAcrescimoRateado"]
#             valor_desconto += item["ValorDesconto"]
#             valor_frete += item["ValorFreteRateado"]
#             valor_seguro += item["ValorSeguroRateado"]
#             valor_outras_despesas += item["ValorOutrasDespesasRateado"]
#             valor_act += item["ValorItem"]

#     # Mapeamento dos pagamentos
#     pagamentos = []
#     for pagamento in dicionario_original["Pagamentos"]:
#         pagamentos.append({
#             "IdentificadorPedidoDeCompraPagamento": pagamento["Identificador"],
#             "TipoCadastro": tipo_cadastro_novo if identificador_produto else pagamento["TipoCadastro"],
#             "IdentificadorContaBancaria": pagamento.get("IdentificadorContaBancaria", "00A0000001"),
#             "IdentificadorFormaPagamento": pagamento["IdentificadorFormaPagamento"],
#             "AliquotaParcela": pagamento["AliquotaParcela"],
#             "Antecipado": pagamento["Antecipado"],
#             "DataReferencia": pagamento["DataReferencia"],
#             "NumeroDias": pagamento["NumeroDias"],
#             "Valor": pagamento["Valor"]
#         })

#     # Mapeamento do ConhecimentoTransporte
#     transporte_pagamentos = [
#         {
#             "IdentificadorContaBancaria": "00A0000001",
#             "IdentificadorFormaPagamento": "00A0000001",
#             "NumeroTitulo": "123456",
#             "DataReferencia": "2020-06-10T17:53:34.896Z",
#             "NumeroDias": 15,
#             "AliquotaParcela": 10,
#             "ValorParcela": 10
#         }
#     ]

#     prazo_transporte = {
#         "Identificador": "00A0000001",
#         "IdentificadorFormaPagamentoEntrada": "00A0000001",
#         "IdentificadorFormaPagamentoParcelas": "00A0000001"
#     }

#     conhecimento_transporte = {
#         "TransportePagamentos": transporte_pagamentos,
#         "PrazoTransporte": prazo_transporte
#     }

#     # Construção do novo dicionário
#     novo_dicionario = {
#         "Itens": itens,
#         "Pagamentos": pagamentos,
#         "CodigoEmpresa": dicionario_original.get("IdentificadorEmpresa", "01"),
#         "CodigoEmpresaFinanceiro": dicionario_original.get("IdentificadorEmpresaFinanceiro", "01"),
#         "IdentificadorBairro": dicionario_original.get("IdentificadorBairro", "00A0000001"),
#         "IdentificadorCidade": dicionario_original.get("IdentificadorCidade", "00A0000001"),
#         "IdentificadorFornecedor": dicionario_original.get("IdentificadorFornecedor", "00A0000001"),
#         "IdentificadorIndexador": dicionario_original.get("IdentificadorIndexador", "00A0000001"),
#         "IdentificadorNaturezaLancamento": dicionario_original.get("IdentificadorNaturezaLancamento", "00A0000001"),
#         "IdentificadorTransportador": dicionario_original.get("IdentificadorTransportadora", "00A0000001"),
#         "IdentificadorUsuarioLiberacao": dicionario_original.get("IdentificadorUsuarioLiberacao", "00A0000001"),
#         "ValorAcrescimo": valor_acrescimo,
#         "ValorDesconto": valor_desconto,
#         "ValorFrete": valor_frete,
#         "ValorSeguro": valor_seguro,
#         "ValorOutrasDespesas": valor_outras_despesas,
#         "ValorACT": valor_act,
#         "ConhecimentoTransporte": conhecimento_transporte,
#         "TipoFrete": dicionario_original.get("TipoFrete", "D"),
#         "CEP": dicionario_original.get("CEP", "25123123"),
#         "Codigo": dicionario_original.get("Codigo", "00001"),
#         "ComplementoEndereco": dicionario_original.get("ComplementoEndereco", "Apto 123"),
#         "DataEmissao": dicionario_original.get("DataEmissao", "2020-06-10T17:53:34.896Z"),
#         "DataEmissaoACT": dicionario_original.get("DataEmissaoACT", "2020-06-10T17:53:34.896Z"),
#         "DataEntrega": dicionario_original.get("DataEntrega", "2020-06-10T17:53:34.896Z"),
#         "Descricao": dicionario_original.get("Descricao", "Pedido cadastrado pela BimerAPI"),
#         "IdentificadorEntidadeOrigem": dicionario_original.get("IdentificadorEntidadeOrigem", "00A0000001"),
#         "NomeEntidadeOrigem": dicionario_original.get("NomeEntidadeOrigem", "Entidade"),
#         "EntregaParcial": dicionario_original.get("EntregaParcial", True),
#         "Logradouro": dicionario_original.get("Logradouro", "Avenida principal"),
#         "NumeroEndereco": dicionario_original.get("NumeroEndereco", "400"),
#         "NumeroOrcamento": dicionario_original.get("NumeroOrcamento", "123"),
#         "Observacao": dicionario_original.get("Observacao", "Cadastrado pela Bimer API"),
#         "Prazo": {
#             "Identificador": "00A0000001",
#             "IdentificadorFormaPagamentoEntrada": "00A0000001",
#             "IdentificadorFormaPagamentoParcelas": "00A0000001"
#         },
#         "TipoLogradouro": dicionario_original.get("TipoLogradouro", "A"),
#         "UF": dicionario_original.get("UF", "RJ")
#     }

#     return novo_dicionario

# # Exemplo de uso:
# dicionario_original = {
#         "ConhecimentoTransporte": {
#         "TransportePagamentos": [],
#         "PrazoTransporte": None
#     },
#     "Itens": [
#         {
#             "AliquotaDesconto": 0.0,
#             "AliquotaDescontoSimples": 0.0,
#             "AliquotaICMS": 0.0,
#             "AliquotaIPI": 0.0,
#             "AliquotaISS": 0.0,
#             "DesoneraICMS": False,
#             "Identificador": "00A000J5SO",
#             "QuantidadeAtendida": 0.0,
#             "Status": "D",
#             "ValorAcrescimoRateado": 0.0,
#             "ValorDesconto": 0.0,
#             "ValorDescontoRateado": 0.0,
#             "ValorFreteRateado": 0.0,
#             "ValorICMS": 0.0,
#             "ValorIPI": 0.0,
#             "ValorISS": 0.0,
#             "ValorItem": 126.07,
#             "ValorOutrasDespesasRateado": 0.0,
#             "ValorSeguroRateado": 0.0,
#             "LancamentosCentroCusto": [],
#             "ProdutoLote": None,
#             "IdentificadorAplicacao": None,
#             "IdentificadorNaturezaLancamento": "00A0000030",
#             "IdentificadorProduto": "00A00003N8",
#             "IdentificadorUnidade": "001000001F",
#             "IdentificadorUsuarioLiberacaoFaixa": "00A0000001",
#             "Bonificacao": False,
#             "DataEntrega": "2024-07-19T00:00:00",
#             "DataValidade": "0001-01-01T00:00:00",
#             "Observacao": "Item do pedido cadastrado pela api",
#             "QuantidadeEmbalagem": 0.0,
#             "QuantidadePedida": 1.0,
#             "ValorUnitario": 126.07
#         },
#         {
#             "AliquotaDesconto": 0.0,
#             "AliquotaDescontoSimples": 0.0,
#             "AliquotaICMS": 0.0,
#             "AliquotaIPI": 0.0,
#             "AliquotaISS": 0.0,
#             "DesoneraICMS": False,
#             "Identificador": "00A000J5SC",
#             "QuantidadeAtendida": 0.0,
#             "Status": "D",
#             "ValorAcrescimoRateado": 0.0,
#             "ValorDesconto": 0.0,
#             "ValorDescontoRateado": 0.0,
#             "ValorFreteRateado": 0.0,
#             "ValorICMS": 0.0,
#             "ValorIPI": 0.0,
#             "ValorISS": 0.0,
#             "ValorItem": 378.21,
#             "ValorOutrasDespesasRateado": 0.0,
#             "ValorSeguroRateado": 0.0,
#             "LancamentosCentroCusto": [],
#             "ProdutoLote": None,
#             "IdentificadorAplicacao": None,
#             "IdentificadorNaturezaLancamento": "00A0000030",
#             "IdentificadorProduto": "00A00003N8",
#             "IdentificadorUnidade": "001000001F",
#             "IdentificadorUsuarioLiberacaoFaixa": "00A0000001",
#             "Bonificacao": False,
#             "DataEntrega": "2024-07-19T00:00:00",
#             "DataValidade": "0001-01-01T00:00:00",
#             "Observacao": "Item do pedido cadastrado pela api",
#             "QuantidadeEmbalagem": 0.0,
#             "QuantidadePedida": 3.0,
#             "ValorUnitario": 126.07
#         },
#         {
#             "AliquotaDesconto": 0.0,
#             "AliquotaDescontoSimples": 0.0,
#             "AliquotaICMS": 0.0,
#             "AliquotaIPI": 0.0,
#             "AliquotaISS": 0.0,
#             "DesoneraICMS": False,
#             "Identificador": "00A000J9HE",
#             "QuantidadeAtendida": 0.0,
#             "Status": "D",
#             "ValorAcrescimoRateado": 0.0,
#             "ValorDesconto": 0.0,
#             "ValorDescontoRateado": 0.0,
#             "ValorFreteRateado": 0.0,
#             "ValorICMS": 0.0,
#             "ValorIPI": 0.0,
#             "ValorISS": 0.0,
#             "ValorItem": 3.2,
#             "ValorOutrasDespesasRateado": 0.0,
#             "ValorSeguroRateado": 0.0,
#             "LancamentosCentroCusto": [],
#             "ProdutoLote": None,
#             "IdentificadorAplicacao": None,
#             "IdentificadorNaturezaLancamento": "00A0000030",
#             "IdentificadorProduto": "00A00001UU",
#             "IdentificadorUnidade": "00A000002C",
#             "IdentificadorUsuarioLiberacaoFaixa": "00A00000N4",
#             "Bonificacao": False,
#             "DataEntrega": "2024-07-19T00:00:00",
#             "DataValidade": "0001-01-01T00:00:00",
#             "Observacao": "Item do pedido cadastrado pela api",
#             "QuantidadeEmbalagem": 0.0,
#             "QuantidadePedida": 2.0,
#             "ValorUnitario": 1.6
#         }
#     ],
#     "Pagamentos": [
#         {
#             "AliquotaParcela": 50.0,
#             "Antecipado": False,
#             "DataReferencia": "2024-07-19T00:00:00",
#             "Identificador": "00A000R4E0",
#             "NumeroDias": 90,
#             "Tipo": "A",
#             "Valor": 253.74,
#             "LancamentosCentroCusto": [],
#             "IdentificadorContaBancaria": None,
#             "IdentificadorFormaPagamento": "00A0000003",
#             "IdentificadorNaturezaLancamento": None
#         },
#         {
#             "AliquotaParcela": 50.0,
#             "Antecipado": False,
#             "DataReferencia": "2024-07-19T00:00:00",
#             "Identificador": "00A000R4DZ",
#             "NumeroDias": 60,
#             "Tipo": "A",
#             "Valor": 253.74,
#             "LancamentosCentroCusto": [],
#             "IdentificadorContaBancaria": None,
#             "IdentificadorFormaPagamento": "00A0000003",
#             "IdentificadorNaturezaLancamento": None
#         }
#     ],
#     "DataCancelamento": "0001-01-01T00:00:00",
#     "DataLiberacao": "2024-07-19T16:02:46",
#     "Status": "D",
#     "TipoFrete": "E",
#     "IdentificadorBairro": None,
#     "IdentificadorCidade": None,
#     "IdentificadorEmpresa": "4",
#     "IdentificadorEmpresaFinanceiro": "4",
#     "IdentificadorIndexador": None,
#     "IdentificadorNaturezaLancamento": None,
#     "IdentificadorFornecedor": "00A00001GG",
#     "IdentificadorTransportadora": None,
#     "IdentificadorPrazo": "00A000005T",
#     "IdentificadorUsuario": "00A00000N4",
#     "IdentificadorUsuarioCancelamento": None,
#     "IdentificadorUsuarioLiberacao": "00A00000N4",
#     "IdentificadorUsuarioResponsavelLiberacao": None,
#     "CEP": "",
#     "Codigo": "088366",
#     "ComplementoEndereco": "",
#     "DataEmissao": "2024-07-19T00:00:00",
#     "DataEmissaoACT": "0001-01-01T00:00:00",
#     "DataEntrega": "2024-07-19T00:00:00",
#     "Descricao": "TESTE DE API -NÃO USE COMO PARAMETRO",
#     "EntregaParcial": False,
#     "Logradouro": "",
#     "NumeroEndereco": "",
#     "NumeroOrcamento": "",
#     "Observacao": "OBSERVACAO DO PEDIDO",
#     "Prazo": None,
#     "TipoLogradouro": "",
#     "UF": None,
#     "IdentificadorEntidadeOrigem": "",
#     "NomeEntidadeOrigem": ""
# }

# # Modificar o tipo de cadastro de um item específico
# novo_dicionario = transformar_dicionario(dicionario_original, tipo_cadastro_novo='E', identificador_produto='00A00003N8')

# # Se quiser modificar para outro tipo, como 'A' ou 'I', basta alterar o parâmetro tipo_cadastro_novo.
# print(json.dumps(novo_dicionario, indent=4, ensure_ascii=False))
# ----------------------------------------------------------------------------------------------------------------------------------------

# modelo para excluir linhas de um datatable
import flet as ft

def main(page: ft.Page):
    def select_row(e):
        e.control.selected = not e.control.selected
        e.control.update()
    
    # dt equivale a table_order_items
    dt = ft.DataTable(
        columns=[ft.DataColumn(label=ft.Text('Col 1'))],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(content=ft.Text(f'Row {num}'))], 
                selected=False, 
                on_select_changed=select_row
            ) for num in range(20)
        ],
        show_checkbox_column=True,
    )

    def delete_rows(e):
        rows = dt.rows[:]

        for row in rows:
            if row.selected:
                dt.rows.remove(row)

        dt.update()

    btn = ft.ElevatedButton(text='Excluir linhas', on_click=delete_rows)

    page.add(btn, dt)

if __name__ == '__main__':
    ft.app(target = main)

# ----------------------------------------------------------------------------------------------------------------------------------------

# import flet as ft

# def main(page: ft.Page):
#     page.title = "Flet counter example"
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER

#     txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

#     def minus_click(e):
#         txt_number.value = str(int(txt_number.value) - 1)
#         page.update()

#     def plus_click(e):
#         txt_number.value = str(int(txt_number.value) + 1)
#         page.update()

#     page.add(
#         ft.Row(
#             [
#                 ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
#                 txt_number,
#                 ft.IconButton(ft.icons.ADD, on_click=plus_click),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#         )
#     )

# ft.app(main)

# ----------------------------------------------------------------------------------------------------------------------------------------

# import flet as ft

# def main(page):
#     page.title = "ListTile Examples"
#     page.add(
#         ft.Card(
#             content=ft.Container(
#                 width=500,
#                 content=ft.Column(
#                     [
#                         ft.ListTile(
#                             leading = ft.Text("123456", style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=15)),
#                             title=ft.Text("JOAQUIM JOSE DA SILVA XAVIER"),
#                             subtitle=ft.Text("JONATHAARAUJO"),
#                             trailing=ft.Switch(),
#                             toggle_inputs=True
#                         ),
#                         ft.ListTile(
#                             leading = ft.Text("789101", style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=15)),
#                             title=ft.Text("MARIA DAS GRACAS XUXA MENEGUEL"),
#                             subtitle=ft.Text("OLAVIANAPINHO"),
#                             selected=True,
#                             trailing=ft.Switch(),
#                             toggle_inputs=True
#                         ),
#                         ft.ListTile(
#                             leading = ft.Text("121314", style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=15)),
#                             title=ft.Text("MARIA ERUNDINA DO PT"),
#                             subtitle=ft.Text("MARLEYMORAES"),
#                             trailing=ft.Switch(),
#                             toggle_inputs=True
#                         ),
#                         ft.ListTile(
#                             leading = ft.Text("151617", style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=15)),
#                             title=ft.Text("LEONARDO VIEIRA CARNEIRO"),
#                             subtitle=ft.Text("JONATHAARAUJO"),
#                             trailing=ft.Switch(),
#                             toggle_inputs=True
#                         ),
#                         # ft.ListTile(
#                         #     leading = ft.Text("123456", style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=15)),
#                         #     title=ft.Text("JOAQUIM JOSE DA SILVA XAVIER"),
#                         #     subtitle= ft.Column(
#                         #         [
#                         #             ft.Text("JONATHAARAUJO"),
#                         #             ft.Text("MARLEYMORAES"),
#                         #             ft.Text("ARNALDOARAUJO"),
#                         #         ]

#                         #     ), # ft.Text("JONATHAARAUJO"),
#                         # ),
#                     ],
#                     spacing=0,
#                 ),
#                 padding=ft.padding.symmetric(vertical=10),
#             )
#         )
#     )

# ft.app(main)


# ----------------------------------------------------------------------------------------------------------------------------------------

# import flet as ft

# from datetime import datetime

# from partials.data_table import create_datatable, my_table

# from partials.button import MyButton
# from querys.qry_pedido_compra_local import PedidosDeCompra
# from querys.qry_pedido_compra_itens import PedidosDeCompraItens
# from querys.qry_produto import Produto
# # from querys.qry_produto_local import BuscaCodigoProduto
# from querys.qry_fornecedor import Fornecedor

# import sys
# import os
# from datetime import datetime, timedelta
# import json
# from pprint import pprint

# # Adicionar o diretório "Curso" ao sys.path
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from configs.settings import *

# # Encontrar uma maneira de criar tabela com linha em branco
# # self.add_datatable_itens('', '', '', '', 'NENHUM ITEM LISTADO', 'REDEFINA SEU FILTRO', selecionado=False)

# class PedidoView:
#     def __init__(self, page):
#         self.page = page
#         self.id_fornecedor = None
#         self.id_pedido_de_compra = None
#         self.total_pedido = 0

#         # Definição do Ref().
#         self.tb_tabela = ft.Ref[ft.DataTable]()
#         self.tb_tabela_itens_pedido = ft.Ref[ft.DataTable]()
#         self.tb_tab_pedido = ft.Ref[ft.Tab]()

#         self.pedidos_json = {} # Todos os pedidos.
#         self.pedido_produtos_json = {} # Todos os produtos de um pedido.
#         self.codigo_x_id_json = {} # Específico para traduzir de código para id e vice versa.
#         self.dicionario_envio_url = {} # Dicionario final para enviar, pode ser editado antes do envio.
#         # ============================================================================================================================= 
#         # Jogue aqui seus estilos:

#         # Estilo para os butões de data.   
#         self.button_style = ft.ButtonStyle(
#                                         shape={
#                                             ft.MaterialState.HOVERED: ft.CircleBorder(),
#                                             ft.MaterialState.DEFAULT: ft.CircleBorder(),
#                                         },
#                                     )
        
#         # Estilo para os campos de entrada
#         # self.input_style = ft.TextStyle(
#         #     color=ft.colors.WHITE,  # Cor do texto
#         #     placeholder_color=ft.colors.GREY_400,  # Cor dos placeholders
#         #     border_color=ft.colors.ORANGE_300  # Cor da borda
#         # )        
#         # =============================================================================================================================

#         self.pg_codigo_chamada = ft.TextField(
#             label="Código", 
#             hint_text="FORNECEDOR",
#             col={"md": 2},
#             focused_border_color=ft.colors.ORANGE_300,
#             input_filter=ft.NumbersOnlyInputFilter(),
#             # text_style=self.input_style,
#             on_blur = self.handle_change_cd_crm, 
#         )

#         self.pg_nome_fornecedor = ft.TextField(
#             label="Nome", 
#             hint_text="FORNECEDOR",
#             col={"md": 7},
#             focused_border_color=ft.colors.ORANGE_300,
#         )

#         self.pg_dd_codigo_empresa = ft.Dropdown(
#             col={"md": 2},
#             label="Escolha Empresa",
#             hint_text="Empresa",
#             value="04",
#             focused_border_color=ft.colors.ORANGE_300,
#             options=[
#                 ft.dropdown.Option("01", text="01 - MATRIZ"),
#                 ft.dropdown.Option("04", text="04 - FILIAL"),
#                 ft.dropdown.Option("12", text="12 - SV BM"),
#                 ft.dropdown.Option("59", text="59 - SV WS"),
#             ],
#             autofocus=True,
#         )

#         self.pg_dd_status_pedido = ft.Dropdown(
#             col={"md": 1},
#             label="Qual Status?",
#             hint_text="Status",
#             value="A",
#             focused_border_color=ft.colors.ORANGE_300,
#             options=[
#                 ft.dropdown.Option("A", text="A"),
#                 ft.dropdown.Option("C", text="C"),
#                 ft.dropdown.Option("D", text="D"),
#                 ft.dropdown.Option("F", text="F"),
#                 ft.dropdown.Option("G", text="G"),
#                 ft.dropdown.Option("P", text="P"),
#                 ft.dropdown.Option("T", text="T"),
#                 ft.dropdown.Option("X", text="X"),
#             ],
#             autofocus=True,
#         )

#         self.txt_pick_date_start = ft.TextField(
#             label="Dt. Início", 
#             hint_text="Dt. Inicial",
#             col={"md": 2},
#             focused_border_color=ft.colors.ORANGE_300,
#             # icon=ft.icons.DATE_RANGE,
#         )

#         self.txt_pick_date_end = ft.TextField(
#             label="Dt. Fim", 
#             hint_text="Dt. Final",
#             col={"md": 2},
#             focused_border_color=ft.colors.ORANGE_300,
#             # icon=ft.icons.DATE_RANGE,
#         )

#         # Lista de dados dinâmicos
#         self.items = [
#             {"id": "123456", "name": "JOAQUIM JOSE DA SILVA XAVIER", "username": "JONATHAARAUJO"},
#             {"id": "789101", "name": "MARIA DAS GRACAS XUXA MENEGUEL", "username": "OLAVIANAPINHO"},
#             {"id": "121314", "name": "MARIA ERUNDINA DO PT", "username": "MARLEYMORAES"},
#             {"id": "151617", "name": "LEONARDO VIEIRA CARNEIRO", "username": "JONATHAARAUJO"},
#             {"id": "135248", "name": "ELIAS FROTA COUTINHO", "username": "RICARDOARAUJO"},
#             {"id": "658945", "name": "LEONARDO VIEIRA CARNEIRO", "username": "BRUNAESCOSSIO"},
#         ]

#         # Lista para armazenar o estado dos switches
#         self.switches_state = []

#         # ---------------------------------------------------------------------------------------------------------------------------------------
#         # TABELAS DA VIEW
#         # ---------------------------------------------------------------------------------------------------------------------------------------
#         # LISTA DE PEDIDOS        
#         self.colunas_dos_pedidos = [
#             ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
#             ft.DataColumn(ft.Text("Status", width=40), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
#             ft.DataColumn(ft.Text("Data Emissao", width=110), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
#             ft.DataColumn(ft.Text("Data Entrega", width=110)),
#             ft.DataColumn(ft.Text("Descricao", width=70), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
#             ft.DataColumn(ft.Text("Observacao", width=330, text_align="LEFT"), numeric=False,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
#         ]
#         self.datatable = create_datatable(self.tb_tabela, self.colunas_dos_pedidos)
#         self.table_order = my_table(self.datatable)

#         # LISTA DE ITENS DO PEDIDO
#         self.colunas_dos_itens_dos_pedidos = [
#             ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
#             ft.DataColumn(ft.Text("Descricao", width=460), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
#             ft.DataColumn(ft.Text("Quantidade", width=80),  numeric=True, on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
#             ft.DataColumn(ft.Text("Vl. Unit.", width=85),  numeric=True),
#             ft.DataColumn(ft.Text("IPI", width=60), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
#             ft.DataColumn(ft.Text("ICMS", width=60), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
#             ft.DataColumn(ft.Text("Vl. Total", width=85),  numeric=True,),
#         ]

#         self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.colunas_dos_itens_dos_pedidos)
#         self.table_order_items = my_table(self.datatable_itens_pedido)

#         self.mytable_pedidos = ft.Column(
#             expand=True,
#             controls=[
#                 ft.Row( 
#                     controls = [self.table_order], 
#                     scroll = ft.ScrollMode.ALWAYS
#                 )
#             ],
#             scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
#             on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos           
#         )       

#         self.mytable_itens = ft.Column(
#             expand=True,
#             controls=[
#                 ft.Row( 
#                     controls = [self.table_order_items], 
#                     scroll = ft.ScrollMode.ALWAYS
#                 )
#             ],
#             scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
#             on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos           
#         )   
#         # ---------------------------------------------------------------------------------------------------------------------------------------

#     # ---------------------------------------------------------------------------------------------------------------------------------------
#     # IDENTIFICANDO PEDIDO SELECIONADO - Order
#     # ---------------------------------------------------------------------------------------------------------------------------------------
#     def change_select(self, e):
#         e.control.selected = not e.control.selected
#         e.control.update() # change_select_produtos

#         if e.control.selected:
#             if self.tb_tabela.current:
#                 selected_row = e.control  # Pega a linha selecionada diretamente do evento.
#                 selected_cell_value = selected_row.cells[0].content.value # Copia o código do pedido de compra.
#                 # Troca a aba do controle TAB.
#                 self.tb_tab_pedido.current.selected_index = 1
#                 self.tb_tab_pedido.current.update()

#                 # print(self.pedidos_json[selected_cell_value]['IdPedidoDeCompra'], '<<<======')
#                 self.id_pedido_de_compra = self.pedidos_json[selected_cell_value]['IdPedidoDeCompra'] # Procura o ID do Pedido de compra no dicionário criado anteriormente.
#                 itens_pedido_de_compra = PedidosDeCompraItens(id_pedido_de_compra=self.id_pedido_de_compra) # Seta a classe dos itens do pedido de compra, note que envio o IdPedidoDeCompra.

#                 # Obtenha o DataFrame dos pedidos de compra:
#                 df_itens_pedidos, self.pedido_produtos_json, self.dicionario_envio_url = itens_pedido_de_compra.obter_dataframe_pedido_de_compra_itens() # Captura da API os itens deste pedido de compra que eu cliquei (Como DataFrame do Pandas).

#                 self.datatable_itens_pedido.rows = [] # Limpa a lista de produtos da tabela antes de adicionar a nova listagem.
#                 self.codigo_x_id_json = {} # Limpa o dicionário para próxima consulta.

#                 # Percorro o DataFrame usando iterrows.
#                 for index, row in df_itens_pedidos.iterrows():
#                     # Para cada linha do DataFrame adicione uma linha do DataTable de 'itens do pedido'.
#                     self.add_datatable_itens_pedido(id_produto=row['IdentificadorProduto'], 
#                                                     quantidade=row['QuantidadePedida'], 
#                                                     valor_unitario=row['ValorItem'], 
#                                                     valor_item=row['ValorUnitario'], 
#                                                     valor_icms=row['ValorIcms'], 
#                                                     valor_ipi=row['ValorIPI'], 
#                                                     selecionado=False)
#         else:
#             print('Deselected2')


# # ---------------------------------------------------------------------------------------------------------------------------------------
#     # POPULANDO TABELAS
#     # ---------------------------------------------------------------------------------------------------------------------------------------

#     #TABELA DE PEDIDOS
#     def add_datatable_itens(self, codigo, status, data_emissao, data_entrega, descricao, observacao, selecionado=False):
#         # Adiciona uma nova linha à DataTable 'self.datatable'
#         self.datatable.rows.append(
#             ft.DataRow(
#                 [
#                     # Adiciona uma célula com o valor 'codigo'
#                     ft.DataCell(ft.Text(value=codigo)),
                    
#                     # Adiciona uma célula com o valor 'status'
#                     ft.DataCell(ft.Text(status)),
                    
#                     # Adiciona uma célula com o valor 'data_emissao'
#                     ft.DataCell(ft.Text(data_emissao)),
                    
#                     # Adiciona uma célula com o valor 'data_entrega'
#                     ft.DataCell(ft.Text(data_entrega)),
                    
#                     # Adiciona uma célula com o valor 'descricao'
#                     ft.DataCell(ft.Text(descricao)),
                    
#                     # Adiciona uma célula com o valor 'observacao' e alinha o texto à esquerda
#                     ft.DataCell(ft.Text(observacao, text_align="LEFT")),
#                 ],
#                 # Define se a linha está selecionada ou não
#                 selected=selecionado,
                
#                 # Define o manipulador de eventos para mudança de seleção da linha
#                 on_select_changed = self.change_select,
#             )
#         )
#         # Atualiza a DataTable para refletir as mudanças
#         self.datatable.update()
#         # self.page.banner.content.controls[0].controls[1].controls[1].update()

#     # Função para buscar o valor pela chave
#     def buscar_valor_por_chave(self, dicionario, chave):
#         return dicionario.get(chave, "Chave não encontrada")

#     # Função para buscar a chave pelo valor
#     def buscar_chave_por_valor(self, dicionario, valor_procurado):
#         for chave, valor in dicionario.items():
#             if valor == valor_procurado:
#                 return chave
#         return "Valor não encontrado"

#     # Função para buscar o item pelo identificador do produto
#     def buscar_item_por_identificador(self, itens, identificador):
#         for index, item in enumerate(itens):
#             if item['IdentificadorProduto'] == identificador:
#                 return index, item
#         return None, None

#     def calcula_total_pedido(self):
#         valor = 0
#         itens = self.dicionario_envio_url['Itens']
#         for i, item in enumerate(itens):
#             if item['TipoCadastro'] != 'E':
#                 valor += float(item['ValorUnitario']) * float(item['QuantidadePedida'])
#         self.total_pedido = round(valor, 2)
#         # return valor

#     def calcula_parcelas_pedido(self, valor_parcela):
#         pagamentos = self.dicionario_envio_url['Pagamentos']

#         # Processa o primeiro item (índice 0)
#         self.dicionario_envio_url['Pagamentos'][0]['TipoCadastro'] = 'A'
#         self.dicionario_envio_url['Pagamentos'][0]['AliquotaParcela'] = '100'
#         self.dicionario_envio_url['Pagamentos'][0]['Valor'] = self.total_pedido

#         # Mantém apenas o primeiro item no dicionário e remove os demais
#         self.dicionario_envio_url['Pagamentos'] = [pagamentos[0]]

#     def change_select_produtos(self, e):
#         e.control.selected = not e.control.selected
#         e.control.update()

#         selected_row = e.control  # Pega a linha selecionada diretamente do evento.
#         selected_cell_value = selected_row.cells[0].content.value # Copia o código do produto no pedido de compra.
#         chave_encontrada = self.buscar_chave_por_valor(self.codigo_x_id_json, selected_cell_value)

#         # Busca o item
#         index, item_encontrado = self.buscar_item_por_identificador(self.dicionario_envio_url['Itens'], chave_encontrada)

#         if e.control.selected:
#             if self.tb_tabela.current:
#                 if item_encontrado:  # Verifica se o item foi encontrado antes de modificar
#                     item_encontrado['TipoCadastro'] = 'E'
#         else:
#             if item_encontrado:  # Apenas modifica se o item foi encontrado e está inicializado
#                 print('Deselected')
#                 item_encontrado['TipoCadastro'] = 'A'

#         parcelas = len(self.dicionario_envio_url['Pagamentos'])
#         self.calcula_total_pedido()
#         valor_parcela = self.total_pedido / parcelas
#         self.calcula_parcelas_pedido(valor_parcela)

#     # TABELA DE ITENS DO PEDIDO
#     def add_datatable_itens_pedido(self, id_produto, quantidade, valor_unitario, valor_item, valor_icms, valor_ipi, selecionado=False):
#         # Cria uma instância da classe Produto para obter detalhes do produto com base no id_produto
#         dados_produto = Produto()
        
#         # Consulta o código e a descrição do produto usando a API
#         id_produto, codigo, descricao = dados_produto.consultar_produto_codigo_api(id_produto)

#         # Cria um dicionário para consultas futuras.
#         self.codigo_x_id_json[id_produto] = codigo

#         # Adiciona uma nova linha à DataTable 'self.datatable_itens_pedido'
#         self.datatable_itens_pedido.rows.append(
#             ft.DataRow(
#                 [
#                     # Adiciona uma célula com o valor 'codigo' do produto
#                     ft.DataCell(ft.Text(value=codigo)),
                    
#                     # Adiciona uma célula com a 'descricao' do produto
#                     ft.DataCell(ft.Text(descricao)),
                    
#                     # Adiciona uma célula com a 'quantidade' pedida
#                     ft.DataCell(ft.Text(quantidade)),
                    
#                     # Adiciona uma célula com o 'valor_item'
#                     ft.DataCell(ft.Text(valor_item)),
                    
#                     # Adiciona uma célula com o 'valor_ipi' do produto
#                     ft.DataCell(ft.Text(valor_ipi)),
                    
#                     # Adiciona uma célula com o 'valor_icms' do produto
#                     ft.DataCell(ft.Text(valor_icms)),
                    
#                     # Adiciona uma célula com o 'valor_unitario' do produto
#                     ft.DataCell(ft.Text(valor_unitario)),
#                 ],
#                 # Define se a linha está selecionada ou não
#                 selected=selecionado,

#                 # Define o manipulador de eventos para mudança de seleção da linha
#                 on_select_changed=self.change_select_produtos,
#             )
#         )
#         # Atualiza a DataTable para refletir as mudanças
#         self.datatable_itens_pedido.update()
#         # self.page.banner.content.controls[0].controls[1].controls[1].update()
#     # ---------------------------------------------------------------------------------------------------------------------------------------


#     def pesquisa_pedidos(self):
#         # Obtenha a data inicial do campo de texto e converta para objeto datetime
#         data_ini = self.txt_pick_date_start.value                
#         data_ini_obj = datetime.strptime(data_ini, '%d/%m/%Y')

#         # Obtenha a data final do campo de texto e converta para objeto datetime
#         data_fim = self.txt_pick_date_end.value                
#         data_fim_obj = datetime.strptime(data_fim, '%d/%m/%Y')        

#         # Converta os objetos datetime para strings no formato YYYY-MM-DD
#         data_ini = data_ini_obj.strftime('%Y-%m-%d')
#         data_fim = data_fim_obj.strftime('%Y-%m-%d')        

#         try:
#             # Crie uma instância da classe PedidosDeCompra com os parâmetros fornecidos
#             db_handler = PedidosDeCompra(
#                 connection_string=connection_string,
#                 cd_empresa=self.pg_dd_codigo_empresa.value,
#                 codigo_crm=self.pg_codigo_chamada.value,
#                 id_fornecedor=self.id_fornecedor,
#                 status=self.pg_dd_status_pedido.value,
#                 dt_emissao_ini=data_ini,
#                 dt_emissao_fim=data_fim
#             )
            
#             # Obtenha os pedidos de compra filtrados
#             pedidos_de_compras = db_handler.get_all_pedidos_de_compras_filtered()
        
#         except Exception as e:
#             # Captura e imprime qualquer erro ocorrido durante a busca dos pedidos
#             print(f"Erro ao buscar pedidos: {e}")
#             return {}

#         # Construa um dicionário com os detalhes dos pedidos de compra
#         pedidos_dict = {
#             pedido.CdChamada: {
#                 "CdChamada": pedido.CdChamada,
#                 "IdPedidoDeCompra": pedido.IdPedidoDeCompra,
#                 "StPedidoDeCompra": pedido.StPedidoDeCompra,
#                 "DtEmissao": pedido.DtEmissao,
#                 "DtEntrega": pedido.DtEntrega,
#                 "DsPedidoDeCompra": pedido.DsPedidoDeCompra,
#                 "DsObservacao": pedido.DsObservacao,
#                 "Selecionado": False
#             }
#             for pedido in pedidos_de_compras
#         }

#         # Adicione cada pedido à DataTable
#         for pedido in pedidos_dict.values():
#             self.add_datatable_itens(
#                 pedido["CdChamada"], 
#                 pedido["StPedidoDeCompra"], 
#                 pedido["DtEmissao"], 
#                 pedido["DtEntrega"], 
#                 pedido["DsPedidoDeCompra"], 
#                 pedido["DsObservacao"], 
#                 selecionado=pedido["Selecionado"]
#             )

#         # Retorne o dicionário com os pedidos
#         return pedidos_dict

#     def pesquisa_fornededor(self, codigo_crm):
#         self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
#         codigo_crm = self.pg_codigo_chamada.value.zfill(6)

#         # Crie uma instância da classe, passando os parâmetros da consulta:
#         fornecedor = Fornecedor(codigo_crm=codigo_crm)

#         # Obtenha o DataFrame dos pedidos de compra:
#         self.id_fornecedor, nm_fornecedor = fornecedor.consultar_fornecedor_api()

#         # Obter os valores de id_fornecedor e nm_fornecedor
#         self.pg_nome_fornecedor.value = nm_fornecedor
#         self.pg_nome_fornecedor.update()

#     def handle_change_cd_crm(self, e):
#         self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
#         self.pg_codigo_chamada.update() 
#         self.pesquisa_fornededor(codigo_crm=self.pg_codigo_chamada.value)
#         self.pg_codigo_chamada.update()

#     def get_first_and_last_day_of_month(self, date):
#         # Obter o primeiro dia do mês
#         first_day = date.replace(day=1)
        
#         # Obter o último dia do mês
#         next_month = first_day.replace(month=first_day.month % 12 + 1, day=1)
#         last_day = next_month - timedelta(days=1)
        
#         return first_day, last_day

#     def filtrar_clicked(self, e):
#         # Data de hoje
#         today = datetime.today()

#         # Obter o primeiro e último dia do mês atual
#         first_day, last_day = self.get_first_and_last_day_of_month(today)

#         # Formatar as datas para exibição
#         first_day_formatted = first_day.strftime('%d/%m/%Y')
#         last_day_formatted = last_day.strftime('%d/%m/%Y')

#         if self.txt_pick_date_start.value == '':
#             self.txt_pick_date_start.value = first_day_formatted
#             self.txt_pick_date_start.update()

#         if self.txt_pick_date_end.value == '':
#             self.txt_pick_date_end.value = last_day_formatted
#             self.txt_pick_date_end.update()

#         self.pedidos_json = self.pesquisa_pedidos()
#         self.datatable.rows = []

#     def salvar_clicked(self, e):
#         # print("Envio o dicionário modificado para a API Alterdata.")
#         # pprint(self.dicionario_envio_url)
#         print('Objeto enviado ao Bimer \n', json.dumps(self.dicionario_envio_url, indent=4, ensure_ascii=False))
#         itens_pedido_de_compra = PedidosDeCompraItens(id_pedido_de_compra=self.id_pedido_de_compra) # Seta a classe dos itens do pedido de compra, note que envio o IdPedidoDeCompra.

#         # Obtenha o DataFrame dos pedidos de compra:
#         itens_pedido_de_compra.editar_pedido_de_compra_itens_api(self.dicionario_envio_url) # Captura da API os itens deste pedido de compra que eu cliquei (Como DataFrame do Pandas).

#     def create_date_picker(self):
        
#         return ft.DatePicker(
#             cancel_text='Cancelar',
#             confirm_text='Selecionar',
#             error_format_text='Data inválida',
#             field_label_text='Digite uma data',
#             help_text='Selecione uma data no calendário',
#             expand=True,
#             on_change=self.handle_date_change_start,
#             on_dismiss=self.handle_date_dismissal,
#         )
    
#     def create_date_picker_end(self):
#         return ft.DatePicker(
#             cancel_text='Cancelar',
#             confirm_text='Selecionar',
#             error_format_text='Data inválida',
#             field_label_text='Digite uma data',
#             help_text='Selecione uma data no calendário',
#             on_change=self.handle_date_change_end,
#             on_dismiss=self.handle_date_dismissal
#         )    

#     def handle_date_change_start(self, e):
#         # self.pg_codigo_chamada.focus()
#         self.txt_pick_date_start.value = e.control.value.strftime('%d/%m/%Y')
#         self.page.update()

#     def handle_date_change_end(self, e):
#         self.txt_pick_date_end.value = e.control.value.strftime('%d/%m/%Y')
#         self.page.update()

#     def handle_change_cd_crm(self, e):
#         self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
#         self.pg_codigo_chamada.update() 
#         self.pesquisa_fornededor(codigo_crm=self.pg_codigo_chamada.value)
#         self.pg_codigo_chamada.update()

#     def handle_date_dismissal(self, e):
#         self.page.add(ft.Text("DatePicker dismissed"))
#         self.page.update()

#     # Função para alternar o Switch selecionado
#     def toggle_switch(self, index):
#         for i in range(len(self.switches_state)):
#             self.switches_state[i].value = False  # Desmarca todos os switches
#         self.switches_state[index].value = True  # Marca apenas o switch atual
#         self.page.update()

#     # Função para criar os ListTiles dinamicamente
#     def create_list_tiles(self):
#         list_tiles = []
#         for index, item in enumerate(self.items):
#             switch = ft.Switch(value=False, on_change=lambda e, idx=index: self.toggle_switch(idx))
#             self.switches_state.append(switch)  # Armazena o switch na lista
            
#             list_tiles.append(
#                 ft.ListTile(
#                     leading=ft.Text(item["id"], style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=15)),
#                     title=ft.Text(item["name"]),
#                     subtitle=ft.Text(item["username"]),
#                     trailing=switch,
#                     toggle_inputs=True
#                 )
#             )
#         return list_tiles

#     def get_content(self):
#         # PRIMEIRA ABA -------------------------------------------------------------------------------------------------------------------

#         # Botão personalizado para realizar a filtragem
#         filtrar_pedido = MyButton(text="Filtrar", on_click=self.filtrar_clicked)

#         filtrar_pedido_responsivo = ft.ResponsiveRow(
#             columns=12,
#             spacing=0,
#             controls=[filtrar_pedido],
#         )        

#         # Criação de uma linha responsiva contendo os campos de código da empresa, status do pedido, código de chamada e nome do fornecedor
#         empresa_codigo_fornecedor = ft.ResponsiveRow(
#             columns=12,
#             controls=[self.pg_dd_codigo_empresa, self.pg_dd_status_pedido, self.pg_codigo_chamada, self.pg_nome_fornecedor],
#         )

#         # Linha responsiva contendo os campos de data e os botões de seleção de data
#         tabela_dos_pedidos = ft.ResponsiveRow(
#             columns=12,
#             spacing=0,
#             controls=[self.mytable_pedidos],
#         )

#         coluna_um = ft.Column(
#             expand=True,
#             alignment=ft.MainAxisAlignment.START,
#             controls=[  # Use "controls" para passar uma lista de controles
#                 ft.Card(
#                     content=ft.Container(
#                         width=500,
#                         content=ft.Column(
#                             self.create_list_tiles(),  # Cria os ListTiles dinamicamente
#                             spacing=0,
#                         ),
#                         padding=ft.padding.symmetric(vertical=10),
#                     )
#                 )
#             ]
#         )

#         coluna_esquerda = ft.Container(
#             # bgcolor=ft.colors.BLUE,
#             # expand=True,
#             content=ft.Column(
#                 alignment=ft.MainAxisAlignment.START,
#                 controls=[coluna_um]
#             ),
#             alignment=ft.alignment.center
#         )

#         coluna_direita = ft.Container(
#             # bgcolor=ft.colors.RED,
#             expand=True,
#             content=ft.Column(
#                 alignment=ft.MainAxisAlignment.START,
#                 controls=[self.mytable_itens]
#             ),
#             alignment=ft.alignment.top_left
#         )

#         # Tela aba 1 final montada.
#         lista_e_tabela = ft.Container(
#             expand=True,
#             # bgcolor=ft.colors.AMBER,
#             content=ft.Row(
#                 controls=[coluna_esquerda, coluna_direita]
#             )
#         )

#         tela_meio = ft.Container(
#             expand=True,
#             content=ft.Column(
#                 controls=[lista_e_tabela]
#             ),
#             alignment=ft.alignment.top_left
#         )

#         # Botão de ícone para selecionar a data inicial
#         btn_pick_date_start = ft.IconButton(
#             icon=ft.icons.DATE_RANGE,
#             icon_color="blue400",
#             icon_size=30,
#             tooltip="Data Inicial.",
#             col={"md": .6},
#             style=self.button_style,
#             on_click=lambda e: self.page.open(self.create_date_picker()), 
#         )

#         # Botão de ícone para selecionar a data final
#         btn_pick_date_end = ft.IconButton(
#             icon=ft.icons.DATE_RANGE,
#             icon_color="blue400",
#             icon_size=30,
#             tooltip="Data Final.",
#             col={"md": .6},
#             style=self.button_style,
#             on_click=lambda e: self.page.open(self.create_date_picker_end()),
#         )

#         # Espaçador para ajuste do layout
#         spacer = ft.Container(col={"md": .4})

#         # Linha responsiva contendo os campos de data e os botões de seleção de data
#         datas_e_botoes = ft.ResponsiveRow(
#             columns=12,
#             spacing=0,
#             controls=[self.txt_pick_date_start, btn_pick_date_start, spacer, self.txt_pick_date_end, btn_pick_date_end],
#         )

#         # SEGUNDA ABA ---------------------------------------------------------------------------------------------------------------------

#         # Botão personalizado para salvar o pedido.
#         enviar_alteracao_pedido = MyButton(text="Enviar Alterações", on_click=self.salvar_clicked)

#         #----------------------------------------------------------------------------------------------------------------------------------
#         # Início da tela aba 0
#         tela_aba_zero_inicio = ft.Container(
#             expand=True,
#             # bgcolor=ft.colors.AMBER,
#             content=ft.Column(
#                 controls=[empresa_codigo_fornecedor, datas_e_botoes, tabela_dos_pedidos]
#             ),
#             alignment=ft.alignment.top_right
#         )

#         # Final da tela
#         tela_aba_zero_fim = ft.Container(
#             # expand=True,
#             # bgcolor=ft.colors.BLUE,
#             content=ft.Column(
#                 controls=[filtrar_pedido_responsivo]
#             ),
#             alignment=ft.alignment.bottom_right
#         )

#         # Tela aba 0 final montada.
#         layout_tab0 = ft.Container(
#             expand=True,
#             # bgcolor=ft.colors.AMBER,
#             content=ft.Column(
#                 controls=[tela_aba_zero_inicio, tela_aba_zero_fim]
#             )
#         )

#         # Retorna o objeto 'my_tab' contendo as abas configuradas
#         return layout_tab0


# ----------------------------------------------------------------------------------------------------------------------------------------

# import flet as ft
# from partials.button import MyButton
# from datetime import datetime, timedelta
# import json

# def main(page):

#     page.title = "ListTile Examples"

#     # Configurações da página
#     page.bgcolor = ft.colors.BLACK
#     page.title = "Sistema SV em Flet"
#     page.theme_mode = "dark"  # Define o tema como escuro
#     page.window.center()  # Centraliza a janela na tela

#     # Define as dimensões da janela
#     page.window.width = 1465
#     page.window.height = 999     


#     # ============================================================================================================================= 
#     # Jogue aqui seus estilos:

#     # Estilo para os butões de data.   
#     button_style = ft.ButtonStyle(
#                                     shape={
#                                         ft.MaterialState.HOVERED: ft.CircleBorder(),
#                                         ft.MaterialState.DEFAULT: ft.CircleBorder(),
#                                     },
#                                 )
    
#     # Estilo para os campos de entrada
#     # self.input_style = ft.TextStyle(
#     #     color=ft.colors.WHITE,  # Cor do texto
#     #     placeholder_color=ft.colors.GREY_400,  # Cor dos placeholders
#     #     border_color=ft.colors.ORANGE_300  # Cor da borda
#     # )        
#     # =============================================================================================================================



#     # Lista para armazenar o estado dos switches
#     switches_state = []

#     def handle_change_cd_crm(self, e):
#         self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
#         self.pg_codigo_chamada.update() 
#         self.pesquisa_fornededor(codigo_crm=self.pg_codigo_chamada.value)
#         self.pg_codigo_chamada.update()

#     def get_first_and_last_day_of_month(self, date):
#         # Obter o primeiro dia do mês
#         first_day = date.replace(day=1)
        
#         # Obter o último dia do mês
#         next_month = first_day.replace(month=first_day.month % 12 + 1, day=1)
#         last_day = next_month - timedelta(days=1)
        
#         return first_day, last_day

#     def filtrar_clicked(self, e):
#         # Data de hoje
#         today = datetime.today()

#         # Obter o primeiro e último dia do mês atual
#         first_day, last_day = self.get_first_and_last_day_of_month(today)

#         # Formatar as datas para exibição
#         first_day_formatted = first_day.strftime('%d/%m/%Y')
#         last_day_formatted = last_day.strftime('%d/%m/%Y')

#         if self.txt_pick_date_start.value == '':
#             self.txt_pick_date_start.value = first_day_formatted
#             self.txt_pick_date_start.update()

#         if self.txt_pick_date_end.value == '':
#             self.txt_pick_date_end.value = last_day_formatted
#             self.txt_pick_date_end.update()

#         self.pedidos_json = self.pesquisa_pedidos()
#         self.datatable.rows = []

#     def salvar_clicked(self, e):
#         # print("Envio o dicionário modificado para a API Alterdata.")
#         # pprint(self.dicionario_envio_url)
#         print('Objeto enviado ao Bimer \n', json.dumps(self.dicionario_envio_url, indent=4, ensure_ascii=False))
#         # itens_pedido_de_compra = PedidosDeCompraItens(id_pedido_de_compra=self.id_pedido_de_compra) # Seta a classe dos itens do pedido de compra, note que envio o IdPedidoDeCompra.

#         # Obtenha o DataFrame dos pedidos de compra:
#         # itens_pedido_de_compra.editar_pedido_de_compra_itens_api(self.dicionario_envio_url) # Captura da API os itens deste pedido de compra que eu cliquei (Como DataFrame do Pandas).

#     def create_date_picker(self):
        
#         return ft.DatePicker(
#             cancel_text='Cancelar',
#             confirm_text='Selecionar',
#             error_format_text='Data inválida',
#             field_label_text='Digite uma data',
#             help_text='Selecione uma data no calendário',
#             expand=True,
#             on_change=self.handle_date_change_start,
#             on_dismiss=self.handle_date_dismissal,
#         )
    
#     def create_date_picker_end(self):
#         return ft.DatePicker(
#             cancel_text='Cancelar',
#             confirm_text='Selecionar',
#             error_format_text='Data inválida',
#             field_label_text='Digite uma data',
#             help_text='Selecione uma data no calendário',
#             on_change=self.handle_date_change_end,
#             on_dismiss=self.handle_date_dismissal
#         )    

#     def handle_date_change_start(self, e):
#         # self.pg_codigo_chamada.focus()
#         self.txt_pick_date_start.value = e.control.value.strftime('%d/%m/%Y')
#         self.page.update()

#     def handle_date_change_end(self, e):
#         self.txt_pick_date_end.value = e.control.value.strftime('%d/%m/%Y')
#         self.page.update()

#     def handle_change_cd_crm(self, e):
#         self.pg_codigo_chamada.value = self.pg_codigo_chamada.value.zfill(6)
#         self.pg_codigo_chamada.update() 
#         self.pesquisa_fornededor(codigo_crm=self.pg_codigo_chamada.value)
#         self.pg_codigo_chamada.update()

#     def handle_date_dismissal(self, e):
#         self.page.add(ft.Text("DatePicker dismissed"))
#         self.page.update()

#     pg_codigo_chamada = ft.TextField(
#         label="Código", 
#         hint_text="FORNECEDOR",
#         col={"md": 2},
#         focused_border_color=ft.colors.ORANGE_300,
#         input_filter=ft.NumbersOnlyInputFilter(),
#         # text_style=input_style,
#         on_blur = handle_change_cd_crm, 
#     )

#     pg_nome_fornecedor = ft.TextField(
#         label="Nome", 
#         hint_text="FORNECEDOR",
#         col={"md": 7},
#         focused_border_color=ft.colors.ORANGE_300,
#     )

#     pg_dd_codigo_empresa = ft.Dropdown(
#         col={"md": 2},
#         label="Escolha Empresa",
#         hint_text="Empresa",
#         value="04",
#         focused_border_color=ft.colors.ORANGE_300,
#         options=[
#             ft.dropdown.Option("01", text="01 - MATRIZ"),
#             ft.dropdown.Option("04", text="04 - FILIAL"),
#             ft.dropdown.Option("12", text="12 - SV BM"),
#             ft.dropdown.Option("59", text="59 - SV WS"),
#         ],
#         autofocus=True,
#     )

#     pg_dd_status_pedido = ft.Dropdown(
#         col={"md": 1},
#         label="Qual Status?",
#         hint_text="Status",
#         value="A",
#         focused_border_color=ft.colors.ORANGE_300,
#         options=[
#             ft.dropdown.Option("A", text="A"),
#             ft.dropdown.Option("C", text="C"),
#             ft.dropdown.Option("D", text="D"),
#             ft.dropdown.Option("F", text="F"),
#             ft.dropdown.Option("G", text="G"),
#             ft.dropdown.Option("P", text="P"),
#             ft.dropdown.Option("T", text="T"),
#             ft.dropdown.Option("X", text="X"),
#         ],
#         autofocus=True,
#     )

#     txt_pick_date_start = ft.TextField(
#         label="Dt. Início", 
#         hint_text="Dt. Inicial",
#         col={"md": 2},
#         focused_border_color=ft.colors.ORANGE_300,
#         # icon=ft.icons.DATE_RANGE,
#     )

#     txt_pick_date_end = ft.TextField(
#         label="Dt. Fim", 
#         hint_text="Dt. Final",
#         col={"md": 2},
#         focused_border_color=ft.colors.ORANGE_300,
#         # icon=ft.icons.DATE_RANGE,
#     )


#     # Função para alternar o Switch selecionado
#     def toggle_switch(index):
#         for i in range(len(switches_state)):
#             switches_state[i].value = False  # Desmarca todos os switches
#         switches_state[index].value = True  # Marca apenas o switch atual
#         page.update()

#     # Lista de dados dinâmicos
#     items = [
#         {"id": "123456", "name": "JOAQUIM JOSE DA SILVA XAVIER", "username": "JONATHAARAUJO"},
#         {"id": "789101", "name": "MARIA DAS GRACAS XUXA MENEGUEL", "username": "OLAVIANAPINHO"},
#         {"id": "121314", "name": "MARIA ERUNDINA DO PT", "username": "MARLEYMORAES"},
#         {"id": "151617", "name": "LEONARDO VIEIRA CARNEIRO", "username": "JONATHAARAUJO"},
#         {"id": "135248", "name": "ELIAS FROTA COUTINHO", "username": "RICARDOARAUJO"},
#         {"id": "658945", "name": "LEONARDO VIEIRA CARNEIRO", "username": "BRUNAESCOSSIO"},
#     ]

#     # Função para criar os ListTiles dinamicamente
#     def create_list_tiles():
#         list_tiles = []
#         for index, item in enumerate(items):
#             switch = ft.Switch(value=False, on_change=lambda e, idx=index: toggle_switch(idx))
#             switches_state.append(switch)  # Armazena o switch na lista
            
#             list_tiles.append(
#                 ft.ListTile(
#                     leading=ft.Text(item["id"], style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=15)),
#                     title=ft.Text(item["name"]),
#                     subtitle=ft.Text(item["username"]),
#                     trailing=switch,
#                     toggle_inputs=True
#                 )
#             )
#         return list_tiles

#     coluna_um = ft.Column(
#         expand=True,
#         alignment=ft.MainAxisAlignment.START,
#         controls=[  # Use "controls" para passar uma lista de controles
#             ft.Card(
#                 content=ft.Container(
#                     width=500,
#                     content=ft.Column(
#                         create_list_tiles(),  # Cria os ListTiles dinamicamente
#                         spacing=0,
#                     ),
#                     padding=ft.padding.symmetric(vertical=10),
#                 )
#             )
#         ],
#         scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
#         on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos 
#     )

#     mytable_itens =  ft.Column(
#         # expand=True,
#         # alignment=ft.MainAxisAlignment.START,
#         controls=
#             [
#                 ft.DataTable(
#                 width=700,
#                 # bgcolor="yellow",
#                 border=ft.border.all(2, "red"),
#                 border_radius=10,
#                 vertical_lines=ft.BorderSide(3, "blue"),
#                 horizontal_lines=ft.BorderSide(1, "green"),
#                 sort_column_index=0,
#                 sort_ascending=True,
#                 heading_row_color=ft.colors.BLACK12,
#                 heading_row_height=100,
#                 data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
#                 show_checkbox_column=True,
#                 divider_thickness=0,
#                 column_spacing=200,
#                 columns=[
#                     ft.DataColumn(
#                         ft.Text("Column 1"),
#                         on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
#                     ),
#                     ft.DataColumn(
#                         ft.Text("Column 2"),
#                         tooltip="This is a second column",
#                         numeric=True,
#                         on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
#                     ),
#                     ],
#                 rows=[
#                     ft.DataRow(
#                         [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#                         selected=True,
#                         on_select_changed=lambda e: print(f"row select changed: {e.data}"),
#                     ),
#                     ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
#                     ],
#                 )
#             ]
#     )


#     # Botão personalizado para realizar a filtragem
#     filtrar_pedido = MyButton(text="Filtrar", on_click=print('Cliquei'))#on_click=filtrar_clicked

#     filtrar_pedido_responsivo = ft.ResponsiveRow(
#         columns=12,
#         spacing=0,
#         controls=[filtrar_pedido],
#     )        

#     # Criação de uma linha responsiva contendo os campos de código da empresa, status do pedido, código de chamada e nome do fornecedor
#     empresa_codigo_fornecedor = ft.ResponsiveRow(
#         columns=12,
#         controls=[pg_dd_codigo_empresa, pg_dd_status_pedido, pg_codigo_chamada, pg_nome_fornecedor],
#     )

#     # Linha responsiva contendo os campos de data e os botões de seleção de data
#     # tabela_dos_pedidos = ft.ResponsiveRow(
#     #     columns=12,
#     #     spacing=0,
#     #     controls=[mytable_itens],
#     # )

#     # Botão de ícone para selecionar a data inicial
#     btn_pick_date_start = ft.IconButton(
#         icon=ft.icons.DATE_RANGE,
#         icon_color="blue400",
#         icon_size=30,
#         tooltip="Data Inicial.",
#         col={"md": .6},
#         style=button_style,
#         on_click=lambda e: page.open(create_date_picker()), 
#     )

#     # Botão de ícone para selecionar a data final
#     btn_pick_date_end = ft.IconButton(
#         icon=ft.icons.DATE_RANGE,
#         icon_color="blue400",
#         icon_size=30,
#         tooltip="Data Final.",
#         col={"md": .6},
#         style=button_style,
#         on_click=lambda e: page.open(create_date_picker_end()),
#     )

#     # Espaçador para ajuste do layout
#     spacer = ft.Container(col={"md": .4})

#     # Linha responsiva contendo os campos de data e os botões de seleção de data
#     datas_e_botoes = ft.ResponsiveRow(
#         columns=12,
#         spacing=0,
#         controls=[txt_pick_date_start, btn_pick_date_start, spacer, txt_pick_date_end, btn_pick_date_end],
#     )



#     coluna_esquerda = ft.Container(
#         # bgcolor=ft.colors.BLUE,
#         # expand=True,
#         content=ft.Column(
#             alignment=ft.MainAxisAlignment.START,
#             controls=[coluna_um]
#         ),
#         alignment=ft.alignment.center
#     )

#     coluna_direita = ft.Container(
#         # bgcolor=ft.colors.RED,
#         expand=True,
#         content=ft.Column(
#             alignment=ft.MainAxisAlignment.START,
#             controls=[mytable_itens]
#         ),
#         alignment=ft.alignment.top_left
#     )


#     # Botão personalizado para realizar a filtragem
#     botao_criar_pedido = ft.ResponsiveRow(
#         columns=12,
#         controls=[MyButton(text="Criar Pedido", on_click=print('Clicado!'))], #criar_pedido_clicked
#     )


#     # Tela aba 1 final montada.
#     lista_e_tabela = ft.Container(
#         expand=True,
#         # bgcolor=ft.colors.AMBER,
#         content=ft.Row(
#             controls=[coluna_esquerda, coluna_direita]
#         )
#     )

#     # mytable_itens = ft.Column(
#     #     expand=True,
#     #     controls=[
#     #         ft.Row( 
#     #             controls = [datatable_itens_pedido], 
#     #             scroll = ft.ScrollMode.ALWAYS
#     #         )
#     #     ],
#     #     scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
#     #     on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos           
#     # ) 

#     # ----------------------------------------------------------------------------------
#     # Início da tela aba 1
#     tela_inicio = ft.Container(
#         expand=False,
#         # bgcolor=ft.colors.AMBER,
#         content=ft.Column(
#             controls=[empresa_codigo_fornecedor,datas_e_botoes]
#         ),
#         alignment=ft.alignment.top_right
#     )

#     tela_meio = ft.Container(
#         expand=True,
#         content=ft.Column(
#             controls=[lista_e_tabela]
#         ),
#         alignment=ft.alignment.top_left
#     )

#     # Final da tela aba 1
#     tela_fim = ft.Container(
#         expand=False,
#         # bgcolor=ft.colors.BLUE,
#         content=ft.Column(
#             controls=[botao_criar_pedido]
#         ),
#         alignment=ft.alignment.bottom_right
#     )
#     # ----------------------------------------------------------------------------------

#     # Tela aba 1 final montada.
#     layout = ft.Container(
#         expand=True,
#         # bgcolor=ft.colors.AMBER,
#         content=ft.Column(
#             controls=[tela_inicio, tela_meio, tela_fim]
#         )
#     )

#     # Adiciona os ListTiles à página
#     page.add(
#         layout
#     )

# ft.app(main)

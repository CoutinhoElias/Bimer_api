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


import flet as ft

def main(page: ft.Page):
    def select_row(e):
        e.control.selected = not e.control.selected
        e.control.update()
    
    # dt equivale a self.table_order_items
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
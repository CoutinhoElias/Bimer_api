# Importa as bibliotecas necessárias
import requests  # Para fazer solicitações HTTP
import json  # Para manipular dados JSON
import pandas as pd  # Biblioteca de manipulação de dados
from urllib.parse import quote  # Para codificar URLs
from pprint import pprint

# from querys.qry_fornecedor import Fornecedor  # Comentado, pois não está sendo utilizado

# from pprint import pprint  # Para impressão de dados formatados

class PedidosDeCompraItens:
    def __init__(self, id_pedido_de_compra):
        """Inicializa a classe PedidosDeCompraItens com o ID do pedido de compra"""
        self.id_pedido_de_compra = id_pedido_de_compra

    def _obter_token(self):
        """Obtém um token de autenticação via API"""
        # URL do endpoint para obter o token
        url = "http://192.168.254.1:8091/oauth/token"
        
        # Cabeçalhos da solicitação
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Parâmetros necessários para a solicitação do token
        params = {
            "client_id": "IntegracaoBimer.js",
            "client_secret": "30ab7b08360b0850521b7f714d067ded",
            "grant_type": "password",
            "username": "EVERTONCOSTA",
            "nonce": "123456789",
            "password": "f2c0d35e8965bf9d5201769880749ff5",
        }
        
        # Faz a solicitação POST para obter o token
        response = requests.post(url, headers=headers, data=params)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code != 200:
            # Lança uma exceção se a solicitação falhar
            raise Exception(f"Erro na solicitação do Token: {response.status_code}")

        # Carrega a resposta JSON em um dicionário
        data = json.loads(response.text)
        
        # Retorna o token de acesso
        return data['access_token']

    def _consultar_pedido_de_compra_itens_api(self):
        """Consulta a API para obter os itens de um pedido de compra pelo seu ID"""
        # URL do endpoint da API para consultar o pedido de compra
        url = f"http://192.168.254.1:8091/api/compras/pedidos/{self.id_pedido_de_compra}"
        
        # Obtém o token de autenticação
        token = self._obter_token()
        
        # Cabeçalhos da solicitação GET
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        # Faz a solicitação GET para a API do pedido de compra
        response = requests.get(url, headers=headers)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code != 200:
            # Lança uma exceção se a solicitação falhar
            raise Exception(f"Erro na solicitação do PedidoDeVenda API: ")  # {response.status_code}

        # Carrega a resposta JSON em um dicionário
        data = json.loads(response.text)
        
        # Retorna os dados da resposta
        return data

    def editar_pedido_de_compra_itens_api(self, dicionario_envio_url):
        """Consulta a API para obter os itens de um pedido de compra pelo seu ID"""
        # URL do endpoint da API para consultar o pedido de compra
        url = f"http://192.168.254.1:8091/api/compras/pedidos/{self.id_pedido_de_compra}"
        
        # Obtém o token de autenticação
        token = self._obter_token()
        
        # Cabeçalhos da solicitação PUT
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        # Faz a solicitação PUT para a API do pedido de compra
        response = requests.put(url, json=dicionario_envio_url, headers=headers)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code != 200:
            # Lança uma exceção se a solicitação falhar
            raise Exception(f"Erro na solicitação do PedidoDeVenda API: {response.status_code}, {response.text}")

        # Carrega a resposta JSON em um dicionário
        data = response.json()
        
        # Retorna os dados da resposta
        return data

    def montar_dicionario(self, dados):
        objeto = dados["ListaObjetos"][0]
        
        # Substituições específicas
        items = []
        for item in objeto["Itens"]:
            items.append({
                "IdentificadorPedidoDeCompraItem": item["Identificador"],
                "TipoCadastro": "A", # A - Alteração, E - Exclusão, I - Inclusão
                "IdentificadorAplicacao": None, # item["IdentificadorAplicacao"] or "00A0000001",
                "IdentificadorProduto": item["IdentificadorProduto"],
                "IdentificadorProdutoLote": None, # item["ProdutoLote"] or "00A0000001",
                "IdentificadorUnidade": item["IdentificadorUnidade"],
                "Bonificacao": item["Bonificacao"],
                "DataEntrega": item["DataEntrega"],
                "DataValidade": item["DataValidade"],
                "Observacao": item["Observacao"] or "Item do pedido cadastrado pela api",
                "QuantidadeEmbalagem": item["QuantidadeEmbalagem"],
                "QuantidadePedida": item["QuantidadePedida"],
                "ValorUnitario": item["ValorUnitario"]
            })
        
        pagamentos = []
        for pagamento in objeto["Pagamentos"]:
            pagamentos.append({
                "IdentificadorPedidoDeCompraPagamento": pagamento["Identificador"],
                "TipoCadastro": pagamento["Tipo"],
                "IdentificadorContaBancaria": pagamento["IdentificadorContaBancaria"], # or "00A0000001",
                "IdentificadorFormaPagamento": pagamento["IdentificadorFormaPagamento"],
                "AliquotaParcela": pagamento["AliquotaParcela"],
                "Antecipado": pagamento["Antecipado"],
                "DataReferencia": pagamento["DataReferencia"],
                "NumeroDias": pagamento["NumeroDias"],
                "Valor": pagamento["Valor"]
            })
        
        dicionario_montado = {
            "Itens": items,
            "Pagamentos": pagamentos,
            "CodigoEmpresa": objeto["IdentificadorEmpresa"],
            "CodigoEmpresaFinanceiro": objeto["IdentificadorEmpresaFinanceiro"],
            "IdentificadorBairro": objeto["IdentificadorBairro"], # or "00A0000001",
            "IdentificadorCidade": objeto["IdentificadorCidade"], # or "00A0000001",
            "IdentificadorFornecedor": objeto["IdentificadorFornecedor"],
            "IdentificadorIndexador": objeto["IdentificadorIndexador"], # or "00A0000001",
            "IdentificadorNaturezaLancamento": objeto["IdentificadorNaturezaLancamento"], # or "00A0000001",
            "IdentificadorTransportador": objeto["IdentificadorTransportadora"], # or "00A0000001",
            "IdentificadorUsuarioLiberacao": objeto["IdentificadorUsuarioLiberacao"],
            "ValorAcrescimo": 0,
            "ValorDesconto": 0,
            "ValorFrete": 0,
            "ValorSeguro": 0,
            "ValorOutrasDespesas": 0,
            "ValorACT": 0,
            # "ConhecimentoTransporte": {
            #     # "TransportePagamentos": [
            #     #     {
            #     #         "IdentificadorContaBancaria": None, # "00A0000001",
            #     #         "IdentificadorFormaPagamento":  None, # "00A0000001",
            #     #         "NumeroTitulo":  None, # "123456",
            #     #         "DataReferencia":  None, # "2020-06-10T17:53:34.896Z",
            #     #         "NumeroDias":  None, # 15,
            #     #         "AliquotaParcela":  None, # 10,
            #     #         "ValorParcela":  None, # 10
            #     #     }
            #     # ],
            #     "PrazoTransporte": {
            #         "Identificador":  None, # "00A0000001",
            #         "IdentificadorFormaPagamentoEntrada":  None, # "00A0000001",
            #         "IdentificadorFormaPagamentoParcelas":  None, # "00A0000001"
            #     }
            # },
            "TipoFrete": objeto["TipoFrete"],
            "CEP":  None, # "25123123",
            "Codigo": objeto["Codigo"],
            "ComplementoEndereco":  None, # "Apto 123",
            "DataEmissao":  objeto["DataEmissao"],
            "DataEmissaoACT":  None, # "2020-06-10T17:53:34.896Z",
            "DataEntrega":  objeto["DataEntrega"],
            "Descricao":  objeto["Descricao"],
            "IdentificadorEntidadeOrigem":  None, # "00A0000001",
            "NomeEntidadeOrigem":  None, # "Entidade",
            "EntregaParcial":  objeto["EntregaParcial"],
            "Logradouro":  None, # "Avenida principal",
            "NumeroEndereco":  None, # "400",
            "NumeroOrcamento":  None, # "123",
            "Observacao":  objeto["Observacao"],
            # "Prazo": {
            #     "Identificador":  None, # "00A0000001",
            #     "IdentificadorFormaPagamentoEntrada":  None, # "00A0000001",
            #     "IdentificadorFormaPagamentoParcelas":  None, # "00A0000001"
            # },
            "TipoLogradouro":  None, # "A",
            "UF":  None, # "RJ"
        }
        
        return dicionario_montado

    def obter_dataframe_pedido_de_compra_itens(self):
        """Obtém os itens do pedido de compra e os retorna em um DataFrame do pandas"""
        # Consulta a API para obter os dados dos itens do pedido de compra
        dados_api = self._consultar_pedido_de_compra_itens_api()
        
        # Lista para armazenar os itens do pedido de compra
        lista_itens = []
        
        # Itera sobre os objetos retornados pela API
        for objeto in dados_api['ListaObjetos']:
            # Itera sobre os itens dentro de cada objeto
            for item in objeto['Itens']:
                # Adiciona um dicionário com os detalhes do item à lista
                lista_itens.append({
                    'Identificador': item['Identificador'],
                    'IdentificadorProduto': item['IdentificadorProduto'],
                    'Observacao': item['Observacao'],
                    'QuantidadePedida': item['QuantidadePedida'],
                    'ValorItem': item['ValorItem'],
                    'ValorUnitario': item['ValorUnitario'],
                    'ValorIcms': item['ValorICMS'],
                    'ValorIPI': item['ValorIPI'],
                })
        
        # print(json.dumps(dados_api, indent=4, ensure_ascii=False))

        # Cria um DataFrame do pandas a partir da lista de itens
        df_itens_pedidos_selecionado = pd.DataFrame(lista_itens)
        dicionario_envio_url = self.montar_dicionario(dados_api)
        
        # Retorna o DataFrame e o dicionário contendo os itens do pedido de compra
        return df_itens_pedidos_selecionado, dados_api, dicionario_envio_url

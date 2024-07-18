# Importa as bibliotecas necessárias
import requests  # Para fazer solicitações HTTP
import json  # Para manipular dados JSON
import pandas as pd  # Biblioteca de manipulação de dados
from urllib.parse import quote  # Para codificar URLs

# from querys.qry_fornecedor import Fornecedor  # Comentado, pois não está sendo utilizado

from pprint import pprint  # Para impressão de dados formatados

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
        
        # Cria um DataFrame do pandas a partir da lista de itens
        df_itens_pedidos_selecionado = pd.DataFrame(lista_itens)
        
        # Retorna o DataFrame contendo os itens do pedido de compra
        return df_itens_pedidos_selecionado

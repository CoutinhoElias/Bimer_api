# Importa as bibliotecas necessárias
import requests  # Para fazer solicitações HTTP
import json  # Para manipular dados JSON
import pandas as pd  # Biblioteca de manipulação de dados
from urllib.parse import quote  # Para codificar URLs

# from querys.qry_fornecedor import Fornecedor  # Comentado, pois não está sendo utilizado

from pprint import pprint  # Para impressão de dados formatados

class Produto:
    # def __init__(self, id_produto):
    #     """Inicializa a classe Produto com o ID do produto"""
    #     self.id_produto = id_produto

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

    def consultar_produto_codigo_api(self, id_produto):
        """Consulta a API para obter informações do produto pelo seu código"""
        # URL do endpoint da API para consultar o produto
        url = f"http://192.168.254.1:8091/api/produtos/{id_produto}"
        
        # Obtém o token de autenticação
        token = self._obter_token()

        # Cabeçalhos da solicitação GET
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        # Faz a solicitação GET para a API do produto
        response = requests.get(url, headers=headers)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code != 200:
            # Imprime uma mensagem de erro se a solicitação falhar
            print(f"Erro na solicitação do Produto API: {response.status_code}")

        # Carrega a resposta JSON em um dicionário
        data = json.loads(response.text)

        # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        # pprint(data)

        # Verifica se não há erros na resposta da API
        if data['Erros'] == []:
            # Retorna o código e o nome do produto
            return data['ListaObjetos'][0]['Identificador'], data['ListaObjetos'][0]['Codigo'], data['ListaObjetos'][0]['Nome']
        else:
            # Imprime uma mensagem se o produto não for encontrado
            print('Não encontrei seu produto!')
            # Retorna valores vazios
            return '', '', ''
        
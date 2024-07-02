import requests
import json
import pandas as pd
from urllib.parse import quote

class Fornecedor:
    def __init__(self, codigo_crm):
        self.codigo_crm = codigo_crm

    def _obter_token(self):
        url = "http://192.168.254.1:8091/oauth/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            "client_id": "IntegracaoBimer.js",
            "client_secret": "30ab7b08360b0850521b7f714d067ded",
            "grant_type": "password",
            "username": "EVERTONCOSTA",
            "nonce": "123456789",
            "password": "f2c0d35e8965bf9d5201769880749ff5",
        }
        response = requests.post(url, headers=headers, data=params)

        if response.status_code != 200:
            raise Exception(f"Erro na solicitação do Token: {response.status_code}")

        data = json.loads(response.text)
        return data['access_token']

    def consultar_fornecedor_api(self):
        url = f"http://192.168.254.1:8091/api/pessoas/codigo/{self.codigo_crm}"
        token = self._obter_token()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Erro na solicitação do Fornecedor API: {response.status_code}")

        data = json.loads(response.text)

        id_fornecedor = data['ListaObjetos'][0]['Identificador']
        nm_fornecedor = data['ListaObjetos'][0]['Nome']

        return id_fornecedor, nm_fornecedor

# # Crie uma instância da classe, passando os parâmetros da consulta:
# pedido_de_compra = PedidosDeCompra(cd_empresa='04', codigo_crm='000012', status='T', dt_emissao_ini='2023-06-21', dt_emissao_fim='2024-06-21')

# # Obtenha o DataFrame dos pedidos de compra:
# df_pedidos = pedido_de_compra.obter_dataframe_pedidos_de_compra()

# # Imprima o DataFrame:
# print(df_pedidos)
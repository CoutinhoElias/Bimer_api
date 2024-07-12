import requests
import json
import pandas as pd
from urllib.parse import quote
from querys.qry_fornecedor import Fornecedor

class PedidosDeCompra:
    def __init__(self, cd_pedido):
        self.cd_pedido = cd_pedido

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

    def _consultar_pedido_de_compra_api(self):

        url = f"http://192.168.254.1:8091/api/compras/pedidos/consultar/status?codigoEmpresa={self.cd_empresa}&identificadorFornecedor={self.id_fornecedor}&status={self.status}&dataInicialEmissao={self.dt_emissao_ini}&dataFinalEmissao={self.dt_emissao_fim}"
        token = self._obter_token()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Erro na solicitação do PedidoDeVenda API: ")# {response.status_code}

        data = json.loads(response.text)
        return data

    def obter_dataframe_pedidos_de_compra(self):
        dados_api = self._consultar_pedido_de_compra_api()
        df_pedidos = pd.DataFrame(dados_api['ListaObjetos'])
        df_pedidos_selecionado = df_pedidos[['Codigo', 'Status', 'DataEmissao', 'DataEntrega', 'Descricao', 'Observacao']]
        return df_pedidos_selecionado
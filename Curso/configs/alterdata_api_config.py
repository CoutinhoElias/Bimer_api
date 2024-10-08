import json  # Para manipular dados JSON

class BimerAPIParams:
    def __init__(self):
        """Inicializa a classe com as credenciais do usuário"""
        self.client_id = "IntegracaoBimer.js"
        self.client_secret = "30ab7b08360b0850521b7f714d067ded"
        self.grant_type = "password"
        self.nonce = "123456789"
        self.username = None
        self.password = None

    def ler_cfg(self):
        """Lê as credenciais do arquivo JSON e atribui às variáveis da classe"""
        with open("cfg_api.json", "r") as f:
            data = json.load(f)

            # Acessar a lista de itens
            self.username = data.get("username")
            self.password = data.get("password_api")
            # self.client_secret = data.get("password_api")

    def get_params(self):
        """Retorna os parâmetros necessários para a autenticação na API"""
        # Certifique-se de que os valores são lidos do arquivo antes de retornar os parâmetros
        self.ler_cfg()

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
            "username": self.username,
            "nonce": self.nonce,
            "password":  self.password,
        }

        # if self.username == 'MARLEYMORAES':
        #     self.nonce, = '10AESMAR'
        return params


# Testar, Testar, Testar, Testar, Testar,  excluir.

# def params_api_bimer(username, password):
#     params = {
#         "client_id": "IntegracaoBimer.js",
#         "client_secret": "30ab7b08360b0850521b7f714d067ded",
#         "grant_type": "password",
#         "username": username,
#         "nonce": "123456789",
#         "password": password,
#     }
#     return params

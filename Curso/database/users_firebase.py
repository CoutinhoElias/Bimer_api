import flet as ft
import pyrebase
import json
import requests
from configs.pyrebase_config import FirebaseConfig

class FirebaseAuth:
    def __init__(self, app_instance):

        self.firebase_config = FirebaseConfig().get_config()
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.auth = self.firebase.auth()
        self.app_instance = app_instance  # Guarda a instância da classe App
        self.user_info = None  # Variável para armazenar as informações do usuário

    def signup(self, email, password, confirm_password):
        mensagem_de_erro = ''

        if password == confirm_password:
            try:
                retorno = self.auth.create_user_with_email_and_password(email, password)
                print(f'Usuário criado com sucesso!\nEfetue seu login agora!')
                return True, retorno['localId']
            except requests.exceptions.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
                # print(error)

                if error == "EMAIL_EXISTS":
                    mensagem_de_erro = "Seu E-mail já existe!"
                elif error == "WEAK_PASSWORD : Password should be at least 6 characters":
                    mensagem_de_erro = "SENHA FRACA!\nA senha deve ter pelo menos 6 caracteres"
                elif password != confirm_password:
                    mensagem_de_erro = "As senhas não coincidem!"
                # print(mensagem_de_erro)
                return False, False
        else:
            print("Senhas diferentes")
            return False

    def login(self, email, password):
        try:
            self.token = self.auth.sign_in_with_email_and_password(email, password)
            print(f'Conectado com sucesso')
            return self.token['idToken']
        except:
            print('Usuário ou senha inválidos!')
            return False

    def insere_perfil(self, user_login, password_api):
        # *****************************************************************
        # Necessário para gravar o id do usuário do Alterdata API.
        # no Firebase.
        
        auth_system = FirebaseAuth()
        token = auth_system.login('supervisor@sveletrica.com', 123456)
        # *****************************************************************

        db = self.firebase.database()

        # print(self.token['email'])
        data = {
            "password": password_api,
        }
        
        # print(token)
        db.child("users").child(user_login).set(data, token=token)


    def coleta_chave_api(self, user_login, token):

        db = self.firebase.database()
        self.user_info = user_login
        id_api = db.child("users").child(self.user_info).child("password").shallow().get(token=token)
        id_bimer = db.child("users").child(self.user_info).child("id_bimer").shallow().get(token=token)
        
        # Atualiza o id_bimer na instância da classe App
        self.app_instance.id_bimer = id_bimer.val()

        # print(id_api.val())
        return id_api.val(), id_bimer.val()
        
# Exemplo de uso da classe
if __name__ == "__main__":
    auth_system = FirebaseAuth()
    
    # Sign up example
    # if auth_system.signup('chiquinho@sveletrica.com', '123456', '123456'):
    #     print("Cadastro realizado com sucesso!")
    # else:
    #     print("Falha no cadastro. Seu E-mail já existe!")

    # Login example
    # if auth_system.login('chiquinho@sveletrica.com', '123456'):
    #     print("Login realizado com sucesso!")
    # else:
    #     print("Falha no login.")

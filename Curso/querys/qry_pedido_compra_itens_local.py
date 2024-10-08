# Importa as bibliotecas necessárias
import requests  # Para fazer solicitações HTTP
import json  # Para manipular dados JSON
import pandas as pd  # Biblioteca de manipulação de dados
from urllib.parse import quote  # Para codificar URLs
from pprint import pprint
from querys.qry_fornecedor import Fornecedor  # Importa a classe Fornecedor do módulo querys.qry_fornecedor
from querys.qry_produto_local import BuscaCodigoProduto
from configs.alterdata_api_config import BimerAPIParams
from configs.settings import *
from sqlalchemy import create_engine, text, Column, update, insert, select, desc, func, and_
from sqlalchemy.orm import sessionmaker
from partials.all_imports import connection_string
from database.models import Pessoa, PedidoDeCompra, PedidoDeCompraItem, ControleAlcadaRegra, Codigo, Produto, CodigoProduto, Unidade
import flet as ft
from datetime import datetime

class PedidosDeCompraItensLocal:
    def __init__(self, id_pedido_de_compra, app_instance):
        """Inicializa a classe PedidosDeCompraItens com o ID do pedido de compra"""
        self.app_instance = app_instance  # Guarda a instância de App
        self.id_pedido_de_compra = id_pedido_de_compra
        self.new_params = BimerAPIParams()

        self.dialogo = ft.AlertDialog(
            title=ft.Text(value="Não encontrei este código"), 
            content=ft.Text(value="Continue seu trabalho!"),
            title_padding=ft.padding.all(10),
            content_padding=ft.padding.all(10),
            shape=ft.RoundedRectangleBorder(radius=5),        
            on_dismiss=lambda e: print("Dialog dismissed!")
        )

        """Inicializa a classe PedidosDeCompra com os parâmetros fornecidos e cria a engine e sessão do SQLAlchemy"""
        self.engine = create_engine(connection_string)  # Cria a engine de conexão com o banco de dados
        self.Session = sessionmaker(bind=self.engine)  # Cria uma fábrica de sessões (não é a sessão em si)


        data = datetime.now()
        self.data_formatada = data.strftime('%Y-%m-%d 00:00:00.000')

    def create_session(self):
        """Cria e retorna uma nova sessão"""
        return self.session()

    def _obter_token(self):
        """Obtém um token de autenticação via API"""
        # URL do endpoint para obter o token
        url = "http://192.168.254.1:8091/oauth/token"
        
        # Cabeçalhos da solicitação
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # print(self.new_params.get_params())
        # Parâmetros necessários para a solicitação do token
        params = self.new_params.get_params()
        
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
        
        # print(json.dumps(dados_api, indent=4, ensure_ascii=False))

        # Cria um DataFrame do pandas a partir da lista de itens
        df_itens_pedidos_selecionado = pd.DataFrame(lista_itens)
        dicionario_envio_url = self.montar_dicionario(dados_api)
        
        # Retorna o DataFrame e o dicionário contendo os itens do pedido de compra
        return df_itens_pedidos_selecionado, dados_api, dicionario_envio_url

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

    def ler_arquivo_pedido_de_compra(self, diretorio):
        # Ler a planilha
        df_itens_planilha = pd.read_excel(diretorio)
        df_itens_planilha['Código'] = df_itens_planilha['Código'].astype(str).str.zfill(6)
        df_itens_planilha['CodigoFornecedor'] = df_itens_planilha['CodigoFornecedor'].astype(str).str.zfill(6)
        df_itens_planilha['id_produto'] = None
        df_itens_planilha['id_unidade'] = None
        
        # Função que será aplicada a cada linha do dataframe para consultar o fornecedor
        def consultar_fornecedor(row):
            codigo_crm_fornecedor = row['CodigoFornecedor']
            fornecedor = Fornecedor(codigo_crm_fornecedor)
            id_fornecedor, nm_fornecedor = fornecedor.consultar_fornecedor_api()
            row['id_fornecedor'] = id_fornecedor
            # row['Fornecedor'] = fornecedor
            row['nm_fornecedor'] = nm_fornecedor
            return row

        # Aplicando a função a cada linha do dataframe
        df_itens_planilha = df_itens_planilha.apply(consultar_fornecedor, axis=1)

        # Função que será aplicada a cada linha do dataframe para consultar o fornecedor
        def consultar_produto_local(row):
            codigo_produto_local = row['Código']
            produto = BuscaCodigoProduto(codigo_produto_local)
            result_dict = produto.get_all_produtos_filtered()
            # print(result_dict[0]['IdProduto'])
            row['id_produto'] = result_dict[0]['IdProduto']
            row['id_unidade'] = result_dict[0]['IdUnidade']
            row['id_classificacao_fiscal'] = result_dict[0]['IdClassificacaoFiscal']
            # row['Fornecedor'] = nm_fornecedor
            return row

        df_itens_planilha = df_itens_planilha.apply(consultar_produto_local, axis=1)

        # Renomear colunas
        df_itens_planilha.rename(columns={'Fornecedor': 'fornecedor',
                                        'CodigoFornecedor': 'codigo_fornecedor',
                                        'Código': 'codigo_produto',
                                        'Und': 'und',
                                        'Sug Compras': 'quantidade',
                                        'P. Comp Novo': 'preco',
                                        'Icms': 'icms',
                                        'IPI': 'ipi',
                                        'Observacao': 'observacao',
                                        'Informações Gerais': 'informacoes_gerais',
                                        'Nome do produto': 'nome_produto'}, inplace=True)

        # Reordenar as colunas do DataFrame
        nova_ordem = ['id_fornecedor', 'codigo_fornecedor', 'fornecedor', 'nm_fornecedor','codigo_produto', 'id_produto', 'id_classificacao_fiscal', 'id_unidade', 'nome_produto', 
                    'und', 'quantidade', 'preco', 'icms', 'ipi', 'observacao', 'informacoes_gerais']
        df_itens_planilha = df_itens_planilha[nova_ordem]

        # df_itens_planilha.to_excel("Excluir.xlsx", index=False)
        
        # print(df_itens_planilha)

        return df_itens_planilha

    # Retorna o próximo código inteiro da tabela escolhida
    def retornar_proximo_codigo_inteiro(self, nome_tabela, nome_campo):
        # Cria uma sessão real a partir do sessionmaker
        session = self.Session()

        try:
            result = session.execute(text(f"SELECT OBJECT_ID('Sq_{nome_tabela}_{nome_campo}')")).scalar()
            if result is not None:
                codigo = session.execute(text(f"SELECT NEXT VALUE FOR dbo.Sq_{nome_tabela}_{nome_campo}")).scalar()
            else:
                codigo = session.execute(text(f"SELECT VlUltimoCodigo FROM Codigo WHERE NmTabela = '{nome_tabela}' AND NmCampo = '{nome_campo}'")).scalar()

                if codigo is None:
                    codigo = 1
                    session.execute(text(f"INSERT INTO Codigo (NmTabela, NmCampo, VlUltimoCodigo) VALUES ('{nome_tabela}', '{nome_campo}', {codigo})"))
                else:
                    codigo += 1
                    stmt_altera_novo_codigo = (update(Codigo)
                        .where(Codigo.NmTabela == 'PedidoDeCompra', Codigo.NmCampo == 'CdChamada')
                        .values(VlUltimoCodigo=codigo)
                    )

                    session.execute(stmt_altera_novo_codigo)
                    session.commit()

        except Exception as e:
            session.rollback()  # Caso ocorra algum erro, faz o rollback da transação
            raise e
        finally:
            session.close()  # Fecha a sessão ao final

        return codigo

    # Função para executar a stored procedure com pyodbc
    def retornar_proximo_codigo_id(self, entity, column, value):
        try:
            # Conecta ao banco de dados
            with pyodbc.connect(connection_string_odbc) as conn:
                with conn.cursor() as cursor:
                    # Executa a stored procedure diretamente
                    cursor.execute("{CALL stp_GetMultiCode(?, ?, ?)}", (entity, column, value))
                    
                    # Recupera os resultados
                    result = cursor.fetchall()
                    # print(type(result))
                    return result[0][0]
        except pyodbc.DatabaseError as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return None

    def criar_pedido_de_compra(self, dicionario_final):
        # # Crio um novo ID de um pedido de compra e de quebra a sequencia inteira do pedido.
        # id_pedido_de_compra = self.retornar_proximo_codigo_id('PedidoDeCompra', 'IdPedidoDeCompra', 1) # Modifica
        # # Coleto a sequencia inteira do pedido para usar no insert.
        # codigo_chamada_pedido = self.retornar_proximo_codigo_inteiro('PedidoDeCompra', 'CdChamada') # Retorna Id
        # codigo_chamada_pedido = "{:0>6}".format(codigo_chamada_pedido)

        # Cria uma sessão real a partir do sessionmaker
        session = self.Session()

        # Cria a conexão a partir da engine
        connection = self.engine.connect()

        try:
            # Crio um novo ID de um pedido de compra e de quebra a sequencia inteira do pedido.
            id_pedido_de_compra = self.retornar_proximo_codigo_id('PedidoDeCompra', 'IdPedidoDeCompra', 1) # Modifica
            # Coleto a sequencia inteira do pedido para usar no insert.
            codigo_chamada_pedido = self.retornar_proximo_codigo_inteiro('PedidoDeCompra', 'CdChamada') # Retorna Id
            codigo_chamada_pedido = "{:0>6}".format(codigo_chamada_pedido)            


            capa = dicionario_final.iloc[[0]] # Seleciona apenas a primeira linha

            # quantidade_registros = len(capa)
            # print(f"Quantidade de registros: {quantidade_registros}")

            print(capa)

            for _, row in capa.iterrows():
                try:
                    pedido = PedidoDeCompra(
                        IdPedidoDeCompra=id_pedido_de_compra,
                        CdChamada=codigo_chamada_pedido,
                        CdEmpresa=4,
                        DsPedidoDeCompra=row['fornecedor'], # <<<<====================
                        CdEndereco=None,
                        IdPessoaTransportador=None,
                        IdUsuario=self.app_instance.id_bimer,
                        TpFretePorConta='E',
                        IdPessoaFornecedor=row['id_fornecedor'],
                        DtEmissao=self.data_formatada,
                        IdCotacao=None,
                        StPedidoDeCompra='A',
                        DtEntrega=self.data_formatada,
                        DsObservacao=None,
                        IdPrazo='00A000000O',
                        VlAjusteFinanceiro=0,
                        IdTipoContato=None,
                        VlAcrescimo=0,
                        VlDesconto=0,
                        VlFrete=0,
                        VlSeguro=0,
                        VlOutrasDespesas=0,
                        IdNaturezaLancamento='00A0000030',
                        IdCentroDeCusto=None,
                        StEntregaParcial='N',
                        NrOrcamento=None,
                        IdIndexador=None,
                        IdUsuarioLiberacao='00A0000001',
                        DtLiberacao=self.data_formatada,
                        IdUsuarioCancelamento=None,
                        DtCancelamento=None,
                        CdCEP=None,
                        NmLogradouro=None,
                        DsComplemento=None,
                        NrLogradouro=None,
                        TpLogradouro=None,
                        IdBairro=None,
                        IdCidade=None,
                        CdEmpresaFinanceiro=4,
                        DsAplicacao=None,
                        IdPrazoTransportador=None,
                        VlACT=0,
                        DtEmissaoACT=None,
                        IdEntidadeOrigem=None,
                        NmEntidadeOrigem=None,
                        IdUsuarioResponsavelLiberacao=None,
                        IdOperacao=None,
                        VlICMSFrete=0,
                        VlICMSSTFrete=0,
                        AlICMSFrete=0,
                        AlICMSSTFrete=0,
                        VlBCICMSFrete=0,
                        VlBCICMSSTFrete=0,
                        IdControleAlcadaRegra=None
                    )
                    session.add(pedido)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(e)
                    return e
            codigo = session.execute(text(f"SELECT CdChamada FROM PedidoDeCompra WHERE IdPedidoDeCompra = '{id_pedido_de_compra}'")).scalar()
            session.close()
            connection.close()
        except Exception as e:
            # session.rollback()
            print(e)
            return e
        finally:
            return {
                        "Erros": [
                            {
                            "ErrorCode": "",
                            "ErrorMessage": "",
                            "PossibleCause": "",
                            "StackTrace": ""
                            }
                        ],
                        "ListaObjetos": [
                            {
                            "Identificador": "00A0000001",
                            "Codigo": codigo_chamada_pedido
                            }
                        ]
                    }, id_pedido_de_compra

    def criar_pedido_de_compra_itens(self, dicionario_final, id_pedido_de_compra):

        # Cria uma sessão real a partir do sessionmaker
        session = self.Session()

        # Cria a conexão a partir da engine
        connection = self.engine.connect()

        try:
            # Percorre os itens do pedido
            for index, row in dicionario_final.iterrows(): 
                # Inicializa id_pedido_de_compra_item como None para iniciar o loop
                id_pedido_de_compra_item = None

                # Tenta obter o código do item até que um valor válido seja retornado
                while id_pedido_de_compra_item is None:
                    print('----------------------------------------------------')
                    print(id_pedido_de_compra_item, '<<=== É para ser nulo')

                    # Executar a stored procedure para obter um novo código para os itens
                    id_pedido_de_compra_item = self.retornar_proximo_codigo_id('PedidoDeCompraItem', 'IdPedidoDeCompraItem', 1) # Modifica

                    print(id_pedido_de_compra_item, 'É para ser diferente do anterior.')
                    print('----------------------------------------------------')
                try:
                    pedido_item = PedidoDeCompraItem(
                        IdPedidoDeCompraItem=id_pedido_de_compra_item,
                        IdPedidoDeCompra=id_pedido_de_compra,
                        NmProduto=row['nome_produto'],
                        IdProduto=row['id_produto'],
                        IdProdutoLote=None,
                        StPedidoDeCompraItem='A',
                        QtPedida=row['quantidade'],
                        DtEntrega=self.data_formatada,
                        VlItem=(row['quantidade'] * row['preco']),
                        AlIPI=row['ipi'] * 100,
                        VlIPI=(row['quantidade'] * row['preco']) * row['ipi'],
                        IdUnidade=row['id_unidade'] if row['id_unidade'] else None,
                        VlUnitario=row['preco'],
                        DsObservacao=row['observacao'],
                        AlICMS=row['icms'] * 100,
                        VlICMS=(row['quantidade'] * row['preco']) * row['icms'],
                        DsAplicacao=row['informacoes_gerais'],
                        IdClassificacaoFiscal=row['id_classificacao_fiscal'][0],
                        IdNaturezaLancamento='00A0000030',
                        # Outros campos...
                    )
                    session.add(pedido_item)
                    session.commit()
            
                except Exception as e:
                    session.rollback()
                    print(e)
        except Exception as e:
            print(e)

        finally:
            session.close()
            connection.close()
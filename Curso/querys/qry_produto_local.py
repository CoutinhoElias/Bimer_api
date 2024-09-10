from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import CodigoProduto, Produto  # Importa a classe CodigoProduto do módulo database.models
from partials.all_imports import connection_string
import pandas as pd

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class BuscaCodigoProduto:
    def __init__(self, cd_produto):
        """Inicializa a classe PedidosDeCompra com os parâmetros fornecidos e cria a engine e sessão do SQLAlchemy"""
        self.engine = create_engine(connection_string)  # Cria a engine de conexão com o banco de dados
        self.Session = sessionmaker(bind=self.engine)  # Cria uma fábrica de sessões

        self.cd_produto = cd_produto

    def create_session(self):
        """Cria e retorna uma nova sessão"""
        return self.Session()

    def as_dict(self):
        return {
            'IdProduto': self.IdProduto,
            'CdChamada': self.CdChamada,
            'StCodigoPrincipal': self.StCodigoPrincipal,
            'IdTipoCodigoProduto': self.IdTipoCodigoProduto,
            'NomeProduto': self.NomeProduto
        }

    def get_all_produtos(self):
        """Obtém todos os produtos do banco de dados"""
        session = self.create_session()
        try:
            produtos = session.query(CodigoProduto).all()  # Consulta todos os produtos
            return produtos
        except Exception as e:
            print(f'Erro ao obter produtos: {e}')
            return []
        finally:
            session.close()  # Fecha a sessão

    # def get_all_produtos_filtered(self):
    #     """Obtém todos os produtos filtrados por codigo de chamada e retorna como um dicionário"""
    #     session = self.create_session()
    #     try:
    #         produtos = session.query(CodigoProduto, Produto.IdUnidade)\
    #             .join(CodigoProduto, Produto.IdProduto == CodigoProduto.IdProduto) \
    #             .filter(
    #             CodigoProduto.CdChamada == self.cd_produto,
    #             CodigoProduto.StCodigoPrincipal == 'S',
    #             CodigoProduto.IdTipoCodigoProduto == '00A0000002'
    #         ).order_by(CodigoProduto.CdChamada).all()  # Consulta e ordena os produtos filtrados

    #         if not produtos:  # Verifica se a lista está vazia
    #             print("Nenhum produto encontrado.")
    #             return []

    #         # Converte os resultados em uma lista de dicionários
    #         produtos_dicts = []
    #         for codigo_produto, id_unidade in produtos:
    #             produto_dict = codigo_produto.__dict__
    #             produto_dict['IdUnidade'] = id_unidade  # Adiciona o IdUnidade ao dicionário
    #             produto_dict.pop('_sa_instance_state', None)  # Remove metadados do SQLAlchemy
    #             produtos_dicts.append(produto_dict)

    #         # Cria um DataFrame a partir da lista de dicionários
    #         df = pd.DataFrame(produtos_dicts)

    #         # Converte o DataFrame para um dicionário
    #         result_dict = df.to_dict(orient='records')

    #         return result_dict
    #     except Exception as e:
    #         print(f'Erro ao obter produtos filtrados: {e}')
    #         return []
    #     finally:
    #         session.close()  # Fecha a sessão

    def get_all_produtos_filtered(self):
        """Obtém todos os produtos filtrados por código de chamada e retorna como um dicionário"""
        session = self.create_session()
        try:
            # Adiciona IdClassificacaoFiscal à consulta
            produtos = session.query(CodigoProduto, Produto.IdUnidade, Produto.IdClassificacaoFiscal)\
                .join(CodigoProduto, Produto.IdProduto == CodigoProduto.IdProduto) \
                .filter(
                CodigoProduto.CdChamada == self.cd_produto,
                CodigoProduto.StCodigoPrincipal == 'S',
                CodigoProduto.IdTipoCodigoProduto == '00A0000002'
            ).order_by(CodigoProduto.CdChamada).all()  # Consulta e ordena os produtos filtrados

            if not produtos:  # Verifica se a lista está vazia
                print("Nenhum produto encontrado.")
                return []

            # Converte os resultados em uma lista de dicionários
            produtos_dicts = []
            for codigo_produto, id_unidade, id_classificacao_fiscal in produtos:
                produto_dict = codigo_produto.__dict__
                produto_dict['IdUnidade'] = id_unidade  # Adiciona o IdUnidade ao dicionário
                produto_dict['IdClassificacaoFiscal'] = id_classificacao_fiscal  # Adiciona o IdClassificacaoFiscal ao dicionário
                produto_dict.pop('_sa_instance_state', None)  # Remove metadados do SQLAlchemy
                produtos_dicts.append(produto_dict)

            # Cria um DataFrame a partir da lista de dicionários
            df = pd.DataFrame(produtos_dicts)

            # Converte o DataFrame para um dicionário
            result_dict = df.to_dict(orient='records')

            return result_dict
        except Exception as e:
            print(f'Erro ao obter produtos filtrados: {e}')
            return []
        finally:
            session.close()  # Fecha a sessão

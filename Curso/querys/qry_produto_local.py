from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import CodigoProduto  # Importa a classe CodigoProduto do módulo database.models
import pandas as pd

class BuscaCodigoProduto:
    def __init__(self, connection_string, cd_produto):
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

    def get_all_produtos_filtered(self):
        """Obtém todos os produtos filtrados por codigo de chamada e retorna como um dicionário"""
        session = self.create_session()
        try:
            produtos = session.query(CodigoProduto).filter(
                CodigoProduto.CdChamada == self.cd_produto,
                CodigoProduto.StCodigoPrincipal == 'S',
                CodigoProduto.IdTipoCodigoProduto == '00A0000002'
            ).order_by(CodigoProduto.CdChamada).all()  # Consulta e ordena os produtos filtrados

            # Converte os resultados em uma lista de dicionários
            produtos_dicts = [produto.__dict__ for produto in produtos]
            for produto_dict in produtos_dicts:
                produto_dict.pop('_sa_instance_state', None)  # Remove metadados do SQLAlchemy

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

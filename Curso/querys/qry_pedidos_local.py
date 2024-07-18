from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import PedidoDeCompra  # Importa a classe PedidoDeCompra do módulo database.models

class PedidosDeCompra:
    def __init__(self, connection_string, cd_empresa, codigo_crm, id_fornecedor, status, dt_emissao_ini, dt_emissao_fim):
        """Inicializa a classe PedidosDeCompra com os parâmetros fornecidos e cria a engine e sessão do SQLAlchemy"""
        self.engine = create_engine(connection_string)  # Cria a engine de conexão com o banco de dados
        self.Session = sessionmaker(bind=self.engine)  # Cria uma fábrica de sessões

        self.cd_empresa = cd_empresa
        self.codigo_crm = codigo_crm
        self.status = status
        self.dt_emissao_ini = dt_emissao_ini
        self.dt_emissao_fim = dt_emissao_fim
        self.id_fornecedor = id_fornecedor        
    
    def create_session(self):
        """Cria e retorna uma nova sessão"""
        return self.Session()

    def add_pedidos_de_compra(self, nome, email):
        """Adiciona um novo pedido de compra ao banco de dados"""
        session = self.create_session()
        try:
            novo_pedidos_de_compra = PedidoDeCompra(nome=nome, email=email)  # Cria um novo objeto PedidoDeCompra
            session.add(novo_pedidos_de_compra)  # Adiciona o objeto à sessão
            session.commit()  # Confirma a transação
            print(f'Pedido {nome} adicionado com sucesso.')
        except Exception as e:
            session.rollback()  # Desfaz a transação em caso de erro
            print(f'Erro ao adicionar pedido de compra: {e}')
        finally:
            session.close()  # Fecha a sessão

    def get_all_pedidos_de_compras(self):
        """Obtém todos os pedidos de compra do banco de dados"""
        session = self.create_session()
        try:
            pedidos_de_compras = session.query(PedidoDeCompra).all()  # Consulta todos os pedidos de compra
            return pedidos_de_compras
        except Exception as e:
            print(f'Erro ao obter pedidos de compra: {e}')
            return []
        finally:
            session.close()  # Fecha a sessão

    def get_all_pedidos_de_compras_filtered(self):
        """Obtém todos os pedidos de compra filtrados por empresa, fornecedor, status e período de emissão"""
        session = self.create_session()
        try:
            pedidos_de_compras = session.query(PedidoDeCompra).filter(
                PedidoDeCompra.CdEmpresa == self.cd_empresa,
                PedidoDeCompra.IdPessoaFornecedor == self.id_fornecedor,
                PedidoDeCompra.StPedidoDeCompra != 'T',
                PedidoDeCompra.DtEmissao.between(self.dt_emissao_ini, self.dt_emissao_fim)
            ).order_by(PedidoDeCompra.CdChamada).all()  # Consulta e ordena os pedidos de compra filtrados
            return pedidos_de_compras
        except Exception as e:
            print(f'Erro ao obter pedidos de compra filtrados: {e}')
            return []
        finally:
            session.close()  # Fecha a sessão

    def update_pedidos_de_compra_email(self, nome, novo_email):
        """Atualiza o email de um pedido de compra no banco de dados"""
        session = self.create_session()
        try:
            pedidos_de_compra = session.query(PedidoDeCompra).filter_by(nome=nome).first()  # Consulta o pedido de compra pelo nome
            if pedidos_de_compra:
                pedidos_de_compra.email = novo_email  # Atualiza o email
                session.commit()  # Confirma a transação
                print(f'Email do pedido {nome} atualizado para {novo_email}.')
            else:
                print(f'Pedido {nome} não encontrado.')
        except Exception as e:
            session.rollback()  # Desfaz a transação em caso de erro
            print(f'Erro ao atualizar email: {e}')
        finally:
            session.close()  # Fecha a sessão

    def delete_pedidos_de_compra(self, nome):
        """Deleta um pedido de compra do banco de dados"""
        session = self.create_session()
        try:
            pedidos_de_compra = session.query(PedidoDeCompra).filter_by(nome=nome).first()  # Consulta o pedido de compra pelo nome
            if pedidos_de_compra:
                session.delete(pedidos_de_compra)  # Deleta o pedido de compra
                session.commit()  # Confirma a transação
                print(f'Pedido {nome} deletado com sucesso.')
            else:
                print(f'Pedido {nome} não encontrado.')
        except Exception as e:
            session.rollback()  # Desfaz a transação em caso de erro
            print(f'Erro ao deletar pedido de compra: {e}')
        finally:
            session.close()  # Fecha a sessão

# Exemplo de uso
# if __name__ == '__main__':
#     connection_string = 'mssql+pymssql://seu_pedidos_de_compra:sua_senha@seu_servidor/seu_banco_de_dados'
#     db_handler = PedidosDeCompra(connection_string, cd_empresa='01', codigo_crm='CRM123', id_fornecedor='Fornecedor01', status='A', dt_emissao_ini='2023-01-01', dt_emissao_fim='2023-12-31')

#     # Create
#     db_handler.add_pedidos_de_compra(nome='Elias', email='elias@exemplo.com')

#     # Read
#     pedidos_de_compras = db_handler.get_all_pedidos_de_compras()
#     for pedidos_de_compra in pedidos_de_compras:
#         print(pedidos_de_compra.CdCEP, pedidos_de_compra.DsObservacao)

#     # Update
#     db_handler.update_pedidos_de_compra_email(nome='Elias', novo_email='novoemail@exemplo.com')

#     # Delete
#     db_handler.delete_pedidos_de_compra(nome='Elias')

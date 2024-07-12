

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import PedidoDeCompra 

class PedidosDeCompra:
    def __init__(self, connection_string, cd_empresa, codigo_crm, id_fornecedor, status, dt_emissao_ini, dt_emissao_fim):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

        self.cd_empresa = cd_empresa
        self.codigo_crm = codigo_crm
        self.status = status
        self.dt_emissao_ini = dt_emissao_ini
        self.dt_emissao_fim = dt_emissao_fim
        self.id_fornecedor = id_fornecedor        
    
    def create_session(self):
        return self.Session()

    def add_pedidos_de_compra(self, nome, email):
        session = self.create_session()
        try:
            novo_pedidos_de_compra = PedidoDeCompra(nome=nome, email=email)
            session.add(novo_pedidos_de_compra)
            session.commit()
            print(f'Pedido {nome} adicionado com sucesso.')
        except Exception as e:
            session.rollback()
            print(f'Erro ao adicionar usuário: {e}')
        finally:
            session.close()

    def get_all_pedidos_de_compras(self):
        session = self.create_session()
        try:
            pedidos_de_compras = session.query(PedidoDeCompra).all()
            return pedidos_de_compras
        except Exception as e:
            print(f'Erro ao obter usuários: {e}')
            return []
        finally:
            session.close()

    def get_all_pedidos_de_compras_filtered(self):
        session = self.create_session()
        try:
            pedidos_de_compras = session.query(PedidoDeCompra).filter(PedidoDeCompra.CdEmpresa == self.cd_empresa,
                                                                      PedidoDeCompra.IdPessoaFornecedor == self.id_fornecedor,
                                                                      PedidoDeCompra.StPedidoDeCompra != 'T',
                                                                      PedidoDeCompra.DtEmissao.between(self.dt_emissao_ini, self.dt_emissao_fim)

                                                                      ).order_by(PedidoDeCompra.CdChamada).all()
            return pedidos_de_compras
        except Exception as e:
            print(f'Erro ao obter usuários: {e}')
            return []
        finally:
            session.close()

    def update_pedidos_de_compra_email(self, nome, novo_email):
        session = self.create_session()
        try:
            pedidos_de_compra = session.query(PedidoDeCompra).filter_by(nome=nome).first()
            if pedidos_de_compra:
                pedidos_de_compra.email = novo_email
                session.commit()
                print(f'Email do usuário {nome} atualizado para {novo_email}.')
            else:
                print(f'Pedido {nome} não encontrado.')
        except Exception as e:
            session.rollback()
            print(f'Erro ao atualizar email: {e}')
        finally:
            session.close()

    def delete_pedidos_de_compra(self, nome):
        session = self.create_session()
        try:
            pedidos_de_compra = session.query(PedidoDeCompra).filter_by(nome=nome).first()
            if pedidos_de_compra:
                session.delete(pedidos_de_compra)
                session.commit()
                print(f'Pedido {nome} deletado com sucesso.')
            else:
                print(f'Pedido {nome} não encontrado.')
        except Exception as e:
            session.rollback()
            print(f'Erro ao deletar usuário: {e}')
        finally:
            session.close()

# Exemplo de uso
# if __name__ == '__main__':
    # connection_string = 'mssql+pymssql://seu_pedidos_de_compra:sua_senha@seu_servidor/seu_banco_de_dados'
    # db_handler = PedidosDeCompra(connection_string)

    # # Create
    # db_handler.add_pedidos_de_compra(nome='Elias', email='elias@exemplo.com')

    # Read
    # pedidos_de_compras = db_handler.get_all_pedidos_de_compras()
    # for pedidos_de_compra in pedidos_de_compras:
    #     print(pedidos_de_compra.CdCEP, pedidos_de_compra.DsObservacao)

    # # Update
    # db_handler.update_pedidos_de_compra_email(nome='Elias', novo_email='novoemail@exemplo.com')

    # # Delete
    # db_handler.delete_pedidos_de_compra(nome='Elias')

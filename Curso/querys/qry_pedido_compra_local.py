from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import PedidoDeCompra, Pessoa  # Importa a classe PedidoDeCompra do módulo database.models

class PedidosDeCompra:
    def __init__(self, connection_string, cd_empresa, codigo_crm, id_fornecedor, status, dt_emissao_ini, dt_emissao_fim, pg_codigo_chamada_pedido):
        """Inicializa a classe PedidosDeCompra com os parâmetros fornecidos e cria a engine e sessão do SQLAlchemy"""
        self.engine = create_engine(connection_string)  # Cria a engine de conexão com o banco de dados
        self.Session = sessionmaker(bind=self.engine)  # Cria uma fábrica de sessões

        self.cd_empresa = cd_empresa
        self.codigo_crm = codigo_crm
        self.pg_codigo_chamada_pedido = pg_codigo_chamada_pedido
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
            filter_conditions = []
            
            if self.cd_empresa is not None:
                filter_conditions.append(PedidoDeCompra.CdEmpresa == self.cd_empresa)
            
            if self.id_fornecedor is not None:
                filter_conditions.append(PedidoDeCompra.IdPessoaFornecedor == self.id_fornecedor)
            
            if self.pg_codigo_chamada_pedido != '':
                filter_conditions.append(PedidoDeCompra.CdChamada == self.pg_codigo_chamada_pedido)
                self.dt_emissao_ini = None
                self.dt_emissao_fim = None

            if self.dt_emissao_ini is not None and self.dt_emissao_fim is not None:
                filter_conditions.append(PedidoDeCompra.DtEmissao.between(self.dt_emissao_ini, self.dt_emissao_fim))
            
            filter_conditions.append(PedidoDeCompra.StPedidoDeCompra == self.status)
            
            pedidos_de_compras = session.query(PedidoDeCompra.IdPedidoDeCompra, PedidoDeCompra.CdChamada, PedidoDeCompra.StPedidoDeCompra, PedidoDeCompra.DtEmissao, PedidoDeCompra.DtEntrega, PedidoDeCompra.DsPedidoDeCompra, PedidoDeCompra.DsObservacao, 
                                               Pessoa.CdChamada.label('CdFornecedor'), Pessoa.NmCurto, Pessoa.CdCPF_CGC)\
                                         .join(Pessoa, PedidoDeCompra.IdPessoaFornecedor == Pessoa.IdPessoa)\
                                         .filter(*filter_conditions).order_by(PedidoDeCompra.CdChamada) #.all()
            # print(pedidos_de_compras)
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

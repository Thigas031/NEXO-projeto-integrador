import database_config  # integração futura com o banco de dados
from partes_do_sistema.pedido import Pedido
from logica_do_sistema.relatorios import Relatorio

class Loja:
    def __init__(self, nome):
        self.nome = nome
        self.clientes = []
        self.estoque = []
        self.pedidos = []

    def cadastrar_cliente(self, cliente):
        self.clientes.append(cliente)

    def adicionar_produto(self, produto):
        self.estoque.append(produto)

    def registrar_pedido(self, pedido):
        self.pedidos.append(pedido)

    def listar_clientes(self):
    # Implementar integração com banco de dados usando database_config.conectar()
        for cliente in self.clientes:
            print(cliente)

    def listar_estoque(self):
    # Implementar integração com banco de dados usando database_config.conectar()
        for produto in self.estoque:
            print(produto)

    def gerar_relatorio(self):
        relatorio = Relatorio(self)
        print(relatorio.gerar_relatorio_texto())
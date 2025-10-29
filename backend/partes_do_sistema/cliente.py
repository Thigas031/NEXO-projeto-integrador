from partes_do_sistema.usuario_base import UsuarioBase

class Cliente(UsuarioBase):

    def __init__(self, id_cliente, user_cliente, email, telefone, endereco, senha=None):
        super().__init__(id_cliente, user_cliente, email, telefone, endereco, senha)
        self.historico_pedidos = []
        self.favoritos = []  # Lista de produtos favoritos

    def adicionar_pedido(self, pedido):
        #Adiciona um pedido ao histórico do cliente.
        self.historico_pedidos.append(pedido)

    def listar_pedidos(self):
        #Lista todos os pedidos realizados pelo cliente.
        for pedido in self.historico_pedidos:
            print(pedido)

    # ----------- SISTEMA DE FAVORITOS -----------

    def adicionar_favorito(self, produto):
        #Adiciona um produto à lista de favoritos, se ainda não estiver.
        if produto not in self.favoritos:
            self.favoritos.append(produto)
            print(f"Produto '{produto.nome}' adicionado aos favoritos.")
        else:
            print("Este produto já está nos seus favoritos.")

    def remover_favorito(self, produto):
        #Remove um produto dos favoritos.
        if produto in self.favoritos:
            self.favoritos.remove(produto)
            print(f"Produto '{produto.nome}' removido dos favoritos.")
        else:
            print("Este produto não está nos seus favoritos.")

    def listar_favoritos(self):
        #Lista os produtos favoritos do cliente.
        if not self.favoritos:
            print("Nenhum produto favorito ainda.")
        else:
            print("Seus produtos favoritos:")
            for p in self.favoritos:
                print(f" - {p.nome} (R${p.preco:.2f})")

    def __str__(self):
        return f"Cliente: {self.user_name} ({self.email})"
from models.pedido import Pedido

class ItemPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = produto.preco

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def to_dict(self):
        return {
            "produto": self.produto.nome,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "subtotal": self.subtotal()
        }
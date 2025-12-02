"""Modelo de Item do Pedido."""


class ItemPedido:
    """Representa um item dentro de um pedido."""
    
    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade
        self._preco_unitario = produto.preco

    @property
    def produto(self):
        return self._produto

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, value):
        self._quantidade = value

    @property
    def preco_unitario(self):
        return self._preco_unitario

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def to_dict(self):
        return {"produto": self.produto.nome, "quantidade": self.quantidade, "preco_unitario": self.preco_unitario, "subtotal": self.subtotal()}

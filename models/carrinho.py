"""Gerenciamento de Carrinho."""
from models.itempedido import ItemPedido


class Carrinho:
    """Carrinho de compras do cliente."""
    
    def __init__(self):
        self._itens = []

    @property
    def itens(self):
        return self._itens

    def adicionar(self, produto, quantidade):
        self._itens.append(ItemPedido(produto, quantidade))

    def limpar(self):
        self._itens = []

    def total(self):
        return sum(i.subtotal() for i in self.itens)

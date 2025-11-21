from backend.itempedido import ItemPedido

class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar(self, produto, quantidade):
        item = ItemPedido(produto, quantidade)
        self.itens.append(item)

    def limpar(self):
        self.itens = []

    def total(self):
        return sum(i.subtotal() for i in self.itens)
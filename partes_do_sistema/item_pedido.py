class ItemPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade
        self.subtotal = produto.preco * quantidade

    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade} - R${self.subtotal:.2f}"
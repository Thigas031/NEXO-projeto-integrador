import database_config  # integração futura com o banco de dados
from partes_do_sistema.item_pedido import ItemPedido

class CarrinhoDeCompras:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto, quantidade):
        self.itens.append(ItemPedido(produto, quantidade))

    def calcular_total(self):
        return sum(item.subtotal for item in self.itens)

    def limpar_carrinho(self):
        self.itens.clear()
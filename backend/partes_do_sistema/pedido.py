from datetime import datetime
from partes_do_sistema.item_pedido import ItemPedido

class Pedido:
    def __init__(self, id_pedido, cliente):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.itens = []
        self.data = datetime.now()
        self.status = "Em aberto"
        self.valor_total = 0.0

    def adicionar_item(self, produto, quantidade):
        if quantidade <= produto.quantidade_estoque:
            item = ItemPedido(produto, quantidade)
            self.itens.append(item)
            produto.quantidade_estoque -= quantidade
            self.atualizar_valor_total()
        else:
            print(f"Estoque insuficiente para o produto {produto.nome}")

    def atualizar_valor_total(self):
        self.valor_total = sum(item.subtotal for item in self.itens)

    def finalizar_pedido(self):
        self.status = "Concluído"
        self.data = datetime.now()

    def __str__(self):
        return f"Pedido {self.id_pedido} - Cliente: {self.cliente.user_cliente} - Total: R$ {self.valor_total:.2f} - Status: {self.status}"
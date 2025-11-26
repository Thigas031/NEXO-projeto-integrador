from datetime import datetime

class Pedido:
    def __init__(self, id, itens, cliente=None):
        self.id = id
        self.itens = itens
        self.cliente = cliente
        self.data = datetime.now()

    def total(self):
        return sum(i.subtotal() for i in self.itens)

    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente.nome if self.cliente else "Não informado",
            "data": self.data.strftime("%d/%m/%Y %H:%M"),
            "total": self.total(),
            "itens": [i.to_dict() for i in self.itens]
        }
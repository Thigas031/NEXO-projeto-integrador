"""Modelo de Pedido."""
from datetime import datetime


class Pedido:
    """Representa um pedido do cliente."""
    
    def __init__(self, id, itens, cliente=None):
        self._id = id
        self._itens = itens
        self._cliente = cliente
        self._data = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def itens(self):
        return self._itens

    @itens.setter
    def itens(self, value):
        self._itens = value

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, value):
        self._cliente = value

    @property
    def data(self):
        return self._data

    def total(self):
        return sum(i.subtotal() for i in self.itens)

    def to_dict(self):
        return {"id": self.id, "cliente": self.cliente.nome if self.cliente else "Não informado", "data": self.data.strftime("%d/%m/%Y %H:%M"), "total": self.total(), "itens": [i.to_dict() for i in self.itens]}

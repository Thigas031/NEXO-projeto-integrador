"""Gerenciamento de Estoque."""


class Estoque:
    """Gerencia produtos em estoque."""
    
    def __init__(self):
        self._produtos = []

    @property
    def produtos(self):
        return self._produtos

    def adicionar(self, produto):
        self._produtos.append(produto)

    def procurar(self, nome):
        return next((p for p in self._produtos if p.nome.lower() == nome.lower()), None)

    def todos(self):
        return self._produtos

    def remover(self, produto_id):
        for p in self._produtos[:]:
            if p.id == produto_id:
                self._produtos.remove(p)
                return True
        return False

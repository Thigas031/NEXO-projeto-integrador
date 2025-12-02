"""Sistema de Favoritos."""


class Favoritos:
    """Gerencia favoritos do usuário."""
    
    def __init__(self):
        self._itens = []

    def adicionar(self, produto_id):
        if produto_id not in self._itens:
            self._itens.append(produto_id)
            return True
        return False

    def remover(self, produto_id):
        if produto_id in self._itens:
            self._itens.remove(produto_id)
            return True
        return False

    def listar(self):
        return self._itens.copy()

    def tem(self, produto_id):
        return produto_id in self._itens

    def limpar(self):
        self._itens = []

    def to_dict(self):
        return {"itens": self._itens}

    @staticmethod
    def from_dict(data):
        fav = Favoritos()
        fav._itens = data.get("itens", [])
        return fav

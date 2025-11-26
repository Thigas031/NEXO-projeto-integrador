"""
Sistema de Favoritos
Gerencia lista de produtos favoritados pelo usuário
"""


class Favoritos:
    """Gerencia favoritos do usuário."""
    
    def __init__(self):
        self.itens = []

    def adicionar(self, produto_id):
        """Adiciona um produto aos favoritos."""
        if produto_id not in self.itens:
            self.itens.append(produto_id)
            return True
        return False

    def remover(self, produto_id):
        """Remove um produto dos favoritos."""
        if produto_id in self.itens:
            self.itens.remove(produto_id)
            return True
        return False

    def listar(self):
        """Retorna a lista de IDs de favoritos."""
        return self.itens.copy()

    def tem(self, produto_id):
        """Verifica se um produto está nos favoritos."""
        return produto_id in self.itens

    def limpar(self):
        """Limpa todos os favoritos."""
        self.itens = []

    def to_dict(self):
        """Converte para dicionário."""
        return {"itens": self.itens}

    @staticmethod
    def from_dict(data):
        """Cria objeto a partir de dicionário."""
        fav = Favoritos()
        fav.itens = data.get("itens", [])
        return fav

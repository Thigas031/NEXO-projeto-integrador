import os

class Produto:
    def __init__(self, id, nome, categoria, preco, estoque, imagem=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco = float(preco)
        self.estoque = int(estoque)
        self.imagem = imagem  # caminho da imagem

    def baixar_estoque(self, quantidade):
        self.estoque -= quantidade

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "estoque": self.estoque,
            "imagem": self.imagem
        }
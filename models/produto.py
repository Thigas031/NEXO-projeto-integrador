import os

class Produto:
    def __init__(self, id, nome, categoria, preco, estoque, imagem=None, descricao="", id_do_vendedor=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco = float(preco)
        self.estoque = int(estoque)
        self.imagem = imagem  # caminho da imagem
        self.descricao = descricao
        self.id_do_vendedor = id_do_vendedor  # ID do vendedor que criou o produto

    def baixar_estoque(self, quantidade):
        self.estoque -= quantidade

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "estoque": self.estoque,
            "imagem": self.imagem,
            "descricao": self.descricao,
            "id_do_vendedor": self.id_do_vendedor
        }

    @staticmethod
    def from_dict(data):
        return Produto(
            data.get("id"),
            data.get("nome"),
            data.get("categoria"),
            data.get("preco"),
            data.get("estoque"),
            data.get("imagem"),
            data.get("descricao", ""),
            data.get("id_do_vendedor")
        )
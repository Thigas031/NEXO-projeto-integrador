"""Modelo de Produto."""


class Produto:
    """Representa um produto no estoque."""

    def __init__(self, id, nome, categoria, preco, estoque, imagem=None, descricao="", id_do_vendedor=None):
        self._id = id
        self._nome = nome
        self._categoria = categoria
        self._preco = float(preco)
        self._estoque = int(estoque)
        self._imagem = imagem
        self._descricao = descricao
        self._id_do_vendedor = id_do_vendedor

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, value):
        self._categoria = value

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, value):
        self._preco = float(value)

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, value):
        self._estoque = int(value)

    @property
    def imagem(self):
        return self._imagem

    @imagem.setter
    def imagem(self, value):
        self._imagem = value

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        self._descricao = value

    @property
    def id_do_vendedor(self):
        return self._id_do_vendedor

    @id_do_vendedor.setter
    def id_do_vendedor(self, value):
        self._id_do_vendedor = value

    def baixar_estoque(self, quantidade):
        self._estoque -= quantidade

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
        return Produto(data.get("id"), data.get("nome"), data.get("categoria"), data.get("preco"), data.get("estoque"), data.get("imagem"), data.get("descricao", ""), data.get("id_do_vendedor"))

from models.favoritos import Favoritos


class Cliente:
    """Representa um cliente da loja."""
    
    def __init__(self, id, nome, email, telefone="", endereco=""):
        self._id = id
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self._endereco = endereco
        self._favoritos = Favoritos()

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
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, value):
        self._telefone = value

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, value):
        self._endereco = value

    @property
    def favoritos(self):
        return self._favoritos

    @favoritos.setter
    def favoritos(self, value):
        self._favoritos = value

    def atualizar_dados(self, nome=None, email=None, telefone=None, endereco=None):
        if nome:
            self.nome = nome
        if email:
            self.email = email
        if telefone:
            self.telefone = telefone
        if endereco:
            self.endereco = endereco

    def adicionar_favorito(self, produto_id):
        return self.favoritos.adicionar(produto_id)

    def remover_favorito(self, produto_id):
        return self.favoritos.remover(produto_id)

    def listar_favoritos(self):
        return self.favoritos.listar()

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "favoritos": self.favoritos.to_dict()
        }

    @staticmethod
    def from_dict(data):
        cliente = Cliente(data.get("id"), data.get("nome"), data.get("email"), data.get("telefone", ""), data.get("endereco", ""))
        cliente.favoritos = Favoritos.from_dict(data.get("favoritos", {}))
        return cliente


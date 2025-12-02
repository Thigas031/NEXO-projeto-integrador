from models.favoritos import Favoritos


class Usuario:
    """Usuário base com suporte a favoritos."""

    def __init__(self, id, nome, email, senha, telefone="", endereco="", papel="vendedor"):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha
        self._telefone = telefone
        self._endereco = endereco
        self._papel = papel
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
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, value):
        self._senha = value

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
    def papel(self):
        return self._papel

    @papel.setter
    def papel(self, value):
        self._papel = value

    @property
    def favoritos(self):
        return self._favoritos

    @favoritos.setter
    def favoritos(self, value):
        self._favoritos = value

    def editar_perfil(self, nome=None, email=None, telefone=None, endereco=None, nova_senha=None):
        """Edita dados do perfil."""
        if nome:
            self.nome = nome
        if email:
            self.email = email
        if telefone:
            self.telefone = telefone
        if endereco:
            self.endereco = endereco
        if nova_senha:
            self.senha = nova_senha

    def adicionar_favorito(self, produto_id):
        return self.favoritos.adicionar(produto_id)

    def remover_favorito(self, produto_id):
        return self.favoritos.remover(produto_id)

    def tem_favorito(self, produto_id):
        return self.favoritos.tem(produto_id)

    def to_dict(self):
        """Converte para dicionário."""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "papel": self.papel,
            "favoritos": self.favoritos.to_dict()
        }

    @staticmethod
    def from_dict(data):
        """Cria objeto a partir de dicionário."""
        user = Usuario(data.get("id"), data.get("nome"), data.get("email"), data.get("senha", ""), data.get("telefone", ""), data.get("endereco", ""), data.get("papel", "vendedor"))
        user.favoritos = Favoritos.from_dict(data.get("favoritos", {}))
        return user

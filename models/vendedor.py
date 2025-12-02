from models.usuariobase import Usuario


class Vendedor(Usuario):
    """Vendedor com produtos próprios."""
    
    def __init__(self, id, nome, email, senha, telefone="", endereco="", cpf="", nome_loja=""):
        super().__init__(id, nome, email, senha, telefone, endereco, papel="vendedor")
        self._cpf = cpf
        self._nome_loja = nome_loja
        self._produtos_do_vendedor = []

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, value):
        self._cpf = value

    @property
    def nome_loja(self):
        return self._nome_loja

    @nome_loja.setter
    def nome_loja(self, value):
        self._nome_loja = value

    @property
    def produtos_do_vendedor(self):
        return self._produtos_do_vendedor

    @produtos_do_vendedor.setter
    def produtos_do_vendedor(self, value):
        self._produtos_do_vendedor = value

    def listar_produtos(self):
        return self.produtos_do_vendedor.copy()

    def to_dict(self):
        data = super().to_dict()
        data.update({"cpf": self.cpf, "nome_loja": self.nome_loja, "produtos_do_vendedor": self.produtos_do_vendedor.copy()})
        return data

    @staticmethod
    def from_dict(data):
        vendedor = Vendedor(data.get("id"), data.get("nome"), data.get("email"), data.get("senha", ""), data.get("telefone", ""), data.get("endereco", ""), data.get("cpf", ""), data.get("nome_loja", ""))
        vendedor.produtos_do_vendedor = data.get("produtos_do_vendedor", [])
        from models.favoritos import Favoritos
        vendedor.favoritos = Favoritos.from_dict(data.get("favoritos", {}))
        return vendedor

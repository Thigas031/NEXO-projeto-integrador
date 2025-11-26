"""
MODELO DE CLIENTE
Dados do cliente/usuário que realiza compras
"""

from models.favoritos import Favoritos


class Cliente:
    """Representa um cliente da loja."""
    
    def __init__(self, id, nome, email, telefone="", endereco=""):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.favoritos = Favoritos()

    def atualizar_dados(self, nome=None, email=None, telefone=None, endereco=None):
        """Atualiza dados do cliente."""
        if nome:
            self.nome = nome
        if email:
            self.email = email
        if telefone:
            self.telefone = telefone
        if endereco:
            self.endereco = endereco

    def adicionar_favorito(self, produto_id):
        """Adiciona produto aos favoritos."""
        return self.favoritos.adicionar(produto_id)

    def remover_favorito(self, produto_id):
        """Remove produto dos favoritos."""
        return self.favoritos.remover(produto_id)

    def listar_favoritos(self):
        """Lista todos os favoritos."""
        return self.favoritos.listar()

    def to_dict(self):
        """Converte para dicionário."""
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
        """Cria objeto a partir de dicionário."""
        cliente = Cliente(
            data.get("id"),
            data.get("nome"),
            data.get("email"),
            data.get("telefone", ""),
            data.get("endereco", "")
        )
        fav_data = data.get("favoritos", {})
        cliente.favoritos = Favoritos.from_dict(fav_data)
        return cliente

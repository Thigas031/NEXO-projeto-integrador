"""
MODELO BASE PARA USUÁRIOS
Classe base para Vendedor e outros tipos de usuário
"""

from models.favoritos import Favoritos


class UsuarioBase:
    """Classe base para usuários do sistema."""
    
    def __init__(self, id, nome, email, senha, telefone="", endereco="", papel="vendedor"):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.endereco = endereco
        self.papel = papel
        self.favoritos = Favoritos()

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
        """Adiciona produto aos favoritos."""
        return self.favoritos.adicionar(produto_id)

    def remover_favorito(self, produto_id):
        """Remove produto dos favoritos."""
        return self.favoritos.remover(produto_id)

    def tem_favorito(self, produto_id):
        """Verifica se produto está nos favoritos."""
        return self.favoritos.tem(produto_id)

    def to_dict(self):
        """Converte para dicionário."""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "papel": self.papel,
            "favoritos": self.favoritos.to_dict()
        }

    @staticmethod
    def from_dict(data):
        """Cria objeto a partir de dicionário."""
        user = UsuarioBase(
            data.get("id"),
            data.get("nome"),
            data.get("email"),
            data.get("senha", ""),
            data.get("telefone", ""),
            data.get("endereco", ""),
            data.get("papel", "vendedor")
        )
        fav_data = data.get("favoritos", {})
        user.favoritos = Favoritos.from_dict(fav_data)
        return user

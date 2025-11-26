"""
MODELO VENDEDOR
Extensão de UsuarioBase para vendedores
"""

from models.usuariobase import UsuarioBase


class Vendedor(UsuarioBase):
    """Representa um vendedor no sistema."""
    
    def __init__(self, id, nome, email, senha, telefone="", endereco="", cpf="", nome_loja=""):
        super().__init__(id, nome, email, senha, telefone, endereco, papel="vendedor")
        self.cpf = cpf
        self.nome_loja = nome_loja
        self.produtos_do_vendedor = []  # Lista de IDs de produtos

    def cadastrar_produto(self, id_produto, nome, preco, descricao, categoria, imagem=None):
        """Cadastra um novo produto para este vendedor."""
        from models.produto import Produto
        produto = Produto(
            id_produto,
            nome,
            categoria,
            preco,
            estoque=10,  # estoque inicial
            imagem=imagem,
            descricao=descricao,
            id_do_vendedor=self.id
        )
        self.produtos_do_vendedor.append(id_produto)
        return produto

    def listar_produtos(self):
        """Retorna lista de IDs de produtos do vendedor."""
        return self.produtos_do_vendedor.copy()

    def to_dict(self):
        """Converte para dicionário."""
        data = super().to_dict()
        data["cpf"] = self.cpf
        data["nome_loja"] = self.nome_loja
        data["produtos_do_vendedor"] = self.produtos_do_vendedor.copy()
        return data

    @staticmethod
    def from_dict(data):
        """Cria objeto a partir de dicionário."""
        vendedor = Vendedor(
            data.get("id"),
            data.get("nome"),
            data.get("email"),
            data.get("senha", ""),
            data.get("telefone", ""),
            data.get("endereco", ""),
            data.get("cpf", ""),
            data.get("nome_loja", "")
        )
        vendedor.produtos_do_vendedor = data.get("produtos_do_vendedor", [])
        fav_data = data.get("favoritos", {})
        from models.favoritos import Favoritos
        vendedor.favoritos = Favoritos.from_dict(fav_data)
        return vendedor

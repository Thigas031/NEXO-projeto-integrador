from backend.usuariobase import UsuarioBase

class Vendedor(UsuarioBase):
    def __init__(self, id, nome, senha):
        super().__init__(id, nome, senha, papel="vendedor")
class UsuarioBase:
    def __init__(self, id, nome, senha, papel="vendedor"):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.papel = papel
        self.favoritos = []

    def editar_perfil(self, novo_nome=None, nova_senha=None):
        if novo_nome:
            self.nome = novo_nome
        if nova_senha:
            self.senha = nova_senha

    def favoritar_produto(self, produto):
        if produto not in self.favoritos:
            self.favoritos.append(produto)

    def desfavoritar_produto(self, produto):
        if produto in self.favoritos:
            self.favoritos.remove(produto)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "papel": self.papel,
            "favoritos": [p.nome for p in self.favoritos]
        }
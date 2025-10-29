class UsuarioBase:

    def __init__(self, id_usuario, user_name, email, telefone, endereco, senha=None):
        self.id_usuario = id_usuario
        self.user_name = user_name
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.senha = senha  # Pode ser usada futuramente para login

    # ======= MÉTODOS COMUNS =======

    def atualizar_endereco(self, novo_endereco):
        self.endereco = novo_endereco

    def atualizar_telefone(self, novo_telefone):
        self.telefone = novo_telefone

    def atualizar_email(self, novo_email):
        self.email = novo_email

    def alterar_senha(self, senha_antiga, nova_senha):
        if self.senha is None or self.senha == senha_antiga:
            self.senha = nova_senha
            print("Senha alterada com sucesso!")
        else:
            print("Senha antiga incorreta.")

    def __str__(self):
        return f"{self.user_name} ({self.email})"
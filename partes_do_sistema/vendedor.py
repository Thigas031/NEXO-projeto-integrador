from partes_do_sistema.usuario_base import UsuarioBase

class Vendedor(UsuarioBase):

    def __init__(self, id_vendedor, user_vendedor, email, telefone, endereco, senha=None):
        super().__init__(id_vendedor, user_vendedor, email, telefone, endereco, senha)
        self.possui_loja = False
        self.nome_loja = None
        self.endereco_loja = None

    def cadastrar_loja(self):
        #Pergunta se o vendedor possui loja e cadastra as informações.
        resposta = input(f"{self.user_name}, você possui uma loja própria?: ").strip().lower()

        if resposta == 'sim':
            self.possui_loja = True
            self.nome_loja = input("Digite o nome da sua loja: ").strip()
            self.endereco_loja = input("Digite o endereço da sua loja: ").strip()
            print(f"Loja '{self.nome_loja}' cadastrada com sucesso!")
        else:
            print("Ok! Você continuará como vendedor sem loja própria.")

    def exibir_informacoes_loja(self):
        #Mostra as informações da loja, se existir.
        if self.possui_loja:
            print(f"Loja: {self.nome_loja} - Endereço: {self.endereco_loja}")
        else:
            print(f"{self.user_name} ainda não possui uma loja cadastrada.")

    def __str__(self):
        loja_info = f" - Loja: {self.nome_loja}" if self.possui_loja else ""
        return f"Vendedor: {self.user_name} ({self.email}){loja_info}"
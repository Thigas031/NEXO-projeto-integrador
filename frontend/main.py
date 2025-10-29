# main.py
import customtkinter as ctk
import os
from database import Database
from config import ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NOME

# importa telas
from telas.tela_login import TelaLogin
from telas.tela_cadastro import TelaCadastro
from telas.tela_principal import TelaPrincipal
from telas.tela_produto import TelaProduto
from telas.tela_perfil import TelaPerfil
from telas.tela_editarperfil import TelaEditarPerfil
from telas.tela_relatorio import TelaRelatorio
from telas.tela_menu import TelaMenu

class App(ctk.CTk):
    def __init__(self, backend):
        super().__init__()
        self.title("NEXO - App")
        self.geometry("1100x700")
        self.backend = backend
        # cria admin se não existir
        self.backend.criar_admin_se_nao_existir(ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NOME)
        self.usuario_logado = None  # dicionário com id, nome, email, tipo

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.telas = {}
        # criar instâncias
        self.telas["login"] = TelaLogin(self.container, self, self.backend)
        self.telas["cadastro"] = TelaCadastro(self.container, self, self.backend)
        self.telas["principal"] = TelaPrincipal(self.container, self, self.backend)
        self.telas["produto"] = TelaProduto(self.container, self, self.backend)
        self.telas["perfil"] = TelaPerfil(self.container, self, self.backend)
        self.telas["editarperfil"] = TelaEditarPerfil(self.container, self, self.backend)
        self.telas["relatorio"] = TelaRelatorio(self.container, self, self.backend)
        self.telas["menu"] = TelaMenu(self.container, self, self.backend)

        # empilha (esconder todas)
        for t in self.telas.values():
            t.pack_forget()

        # iniciar em login
        self.mostrar_tela("login")

    def mostrar_tela(self, nome, *args):
        # esconde tudo
        for t in self.telas.values():
            t.pack_forget()
        tela = self.telas.get(nome)
        if not tela:
            return
        tela.pack(fill="both", expand=True)
        # se a tela tiver método atualizar
        if hasattr(tela, "atualizar"):
            tela.atualizar()
        # se abrir produto com id
        if nome == "produto" and args:
            try:
                produto_id = int(args[0])
                tela.abrir(produto_id)
            except:
                pass

if __name__ == "__main__":
    # cria assets/telas se necessário
    if not os.path.exists("telas"):
        os.makedirs("telas", exist_ok=True)

    # iniciar DB
    db = Database()
    app = App(db)
    app.mainloop()
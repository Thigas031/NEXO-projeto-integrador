import database_config  # integração futura com o banco de dados
import customtkinter as ctk

class TelaCadastro(ctk.CTkFrame):
    def __init__(self, master, app, backend, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.backend = backend

        ctk.CTkLabel(self, text="Criar Conta", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=14)
        frm = ctk.CTkFrame(self)
        frm.pack(padx=30, pady=6)

        self.nome = ctk.CTkEntry(frm, placeholder_text="Nome completo", width=420)
        self.nome.pack(pady=6)
        self.email = ctk.CTkEntry(frm, placeholder_text="E-mail", width=420)
        self.email.pack(pady=6)
        self.senha = ctk.CTkEntry(frm, placeholder_text="Senha", show="*", width=420)
        self.senha.pack(pady=6)
        self.telefone = ctk.CTkEntry(frm, placeholder_text="Telefone (opcional)", width=420)
        self.telefone.pack(pady=6)

        self.tipo = ctk.CTkOptionMenu(frm, values=["comprador","vendedor"])
        self.tipo.set("comprador")
        self.tipo.pack(pady=6)

        self.msg = ctk.CTkLabel(self, text="", text_color="red")
        self.msg.pack(pady=4)

        ctk.CTkButton(frm, text="Cadastrar", width=200, command=self.cadastrar).pack(pady=8)
        ctk.CTkButton(self, text="Voltar ao login", fg_color="transparent", command=lambda: self.app.mostrar_tela("login")).pack(pady=(6,0))

    def cadastrar(self):
        nome = self.nome.get().strip()
        email = self.email.get().strip()
        senha = self.senha.get().strip()
        telefone = self.telefone.get().strip()
        tipo = self.tipo.get()
        if not nome or not email or not senha:
            self.msg.configure(text="Preencha nome, e-mail e senha.")
            return
        uid = self.backend.criar_usuario(nome, email, senha, telefone or None, tipo=tipo)
        if uid:
            self.msg.configure(text="", text_color="green")
            # logar automaticamente
            usuario = self.backend.autenticar(email, senha)
            self.app.usuario_logado = usuario
            self.app.mostrar_tela("principal")
        else:
            self.msg.configure(text="E-mail já cadastrado.")
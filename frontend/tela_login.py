import customtkinter as ctk

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, app, backend, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.backend = backend

        ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        frm = ctk.CTkFrame(self)
        frm.pack(padx=30, pady=10)

        self.email = ctk.CTkEntry(frm, placeholder_text="E-mail", width=380)
        self.email.pack(pady=6)
        self.senha = ctk.CTkEntry(frm, placeholder_text="Senha", show="*", width=380)
        self.senha.pack(pady=6)

        ctk.CTkButton(frm, text="Entrar", width=200, command=self.entrar).pack(pady=12)
        ctk.CTkButton(self, text="Criar conta", fg_color="transparent", command=lambda: self.app.mostrar_tela("cadastro")).pack(pady=(6,0))

        self.msg = ctk.CTkLabel(self, text="", text_color="red")
        self.msg.pack(pady=6)

    def entrar(self):
        email = self.email.get().strip()
        senha = self.senha.get().strip()
        if not email or not senha:
            self.msg.configure(text="Preencha e-mail e senha.")
            return
        usuario = self.backend.autenticar(email, senha)
        if usuario:
            # armazenar usuário na app
            self.app.usuario_logado = usuario
            self.msg.configure(text="")
            self.app.mostrar_tela("principal")
        else:
            self.msg.configure(text="Credenciais inválidas.")

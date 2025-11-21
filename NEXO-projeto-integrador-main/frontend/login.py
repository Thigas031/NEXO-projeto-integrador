import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

# ================================
# INTEGRAÇÃO COM BACKEND
# ================================
from frontend.core import loja, usuario_logado


class LoginCadastroScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Acesso")
        self.state("zoomed")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Fundo gradiente
        self.bg_image = self.criar_gradiente(
            self.winfo_screenwidth(),
            self.winfo_screenheight()
        )
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # CARD principal
        self.card = ctk.CTkFrame(
            self,
            width=460,
            height=520,
            fg_color="#7d89e6",
            corner_radius=0
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        self.modo = "login"
        self.construir_login()

    # -----------------------------
    # GRADIENTE
    # -----------------------------
    def criar_gradiente(self, w, h):
        cor1 = (30, 120, 255)
        cor2 = (10, 25, 80)

        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)

        for i in range(h):
            ratio = i / h
            r = int(cor1[0] * (1 - ratio) + cor2[0] * ratio)
            g = int(cor1[1] * (1 - ratio) + cor2[1] * ratio)
            b = int(cor1[2] * (1 - ratio) + cor2[2] * ratio)
            draw.line([(0, i), (w, i)], fill=(r, g, b))

        return ImageTk.PhotoImage(img)

    # -----------------------------
    # LOGIN
    # -----------------------------
    def construir_login(self):
        for w in self.card.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.card,
            text="Entrar no NEXO",
            text_color="white",
            font=("Arial", 30, "bold")
        ).pack(pady=(40, 20))

        self.login_usuario = ctk.CTkEntry(
            self.card, width=330, placeholder_text="Usuário"
        )
        self.login_usuario.pack(pady=10)

        self.login_senha = ctk.CTkEntry(
            self.card, width=330, placeholder_text="Senha", show="*"
        )
        self.login_senha.pack(pady=10)

        ctk.CTkButton(
            self.card,
            text="Entrar",
            width=330,
            height=40,
            fg_color="#1b1f3b",
            hover_color="#2c355e",
            text_color="white",
            font=("Arial", 16, "bold"),
            command=self.fazer_login
        ).pack(pady=20)

        self.status = ctk.CTkLabel(self.card, text="", text_color="white")
        self.status.pack()

        ctk.CTkButton(
            self.card,
            text="Criar nova conta",
            fg_color="transparent",
            text_color="white",
            hover_color="#5a6bc4",
            command=self.construir_cadastro
        ).pack(pady=25)

    # -----------------------------
    # CADASTRO
    # -----------------------------
    def construir_cadastro(self):
        for w in self.card.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.card,
            text="Criar Conta",
            text_color="white",
            font=("Arial", 30, "bold")
        ).pack(pady=(40, 20))

        self.cad_email = ctk.CTkEntry(
            self.card, width=330, placeholder_text="Email"
        )
        self.cad_email.pack(pady=10)

        self.cad_usuario = ctk.CTkEntry(
            self.card, width=330, placeholder_text="Nome de usuário"
        )
        self.cad_usuario.pack(pady=10)

        self.cad_senha = ctk.CTkEntry(
            self.card, width=330, placeholder_text="Senha", show="*"
        )
        self.cad_senha.pack(pady=10)

        self.cad_senha_confirmar = ctk.CTkEntry(
            self.card, width=330, placeholder_text="Confirmar senha", show="*"
        )
        self.cad_senha_confirmar.pack(pady=10)

        ctk.CTkButton(
            self.card,
            text="Criar conta",
            width=330,
            height=40,
            fg_color="#1b1f3b",
            hover_color="#2c355e",
            text_color="white",
            font=("Arial", 16, "bold"),
            command=self.fazer_cadastro
        ).pack(pady=20)

        self.status = ctk.CTkLabel(self.card, text="", text_color="white")
        self.status.pack()

        ctk.CTkButton(
            self.card,
            text="Já tenho conta",
            fg_color="transparent",
            hover_color="#5a6bc4",
            text_color="white",
            command=self.construir_login
        ).pack(pady=25)

    # -----------------------------
    # LÓGICA DE LOGIN (INTEGRAÇÃO)
    # -----------------------------
    def fazer_login(self):
        usuario = self.login_usuario.get()
        senha = self.login_senha.get()

        # Procurar usuário cadastrado
        for u in loja.usuarios:
            if u.nome == usuario and u.senha == senha:
                usuario_logado["id"] = u.id
                usuario_logado["nome"] = u.nome

                self.status.configure(text="✔ Login realizado!", text_color="lightgreen")
                self.after(600, self.abrir_home)
                return

        self.status.configure(text="❌ Usuário ou senha inválidos", text_color="red")

    def abrir_home(self):
        from frontend.home import TelaHome
        self.destroy()
        TelaHome().mainloop()

    # -----------------------------
    # LÓGICA DE CADASTRO (INTEGRAÇÃO)
    # -----------------------------
    def fazer_cadastro(self):
        email = self.cad_email.get()
        usuario = self.cad_usuario.get()
        senha = self.cad_senha.get()
        confirmar = self.cad_senha_confirmar.get()

        if senha != confirmar:
            self.status.configure(text="❌ As senhas não coincidem", text_color="red")
            return

        # Verificar se já existe
        for u in loja.usuarios:
            if u.nome == usuario:
                self.status.configure(text="❌ Usuário já existe", text_color="red")
                return

        # Criar usuário
        novo = loja.cadastrar_usuario(usuario, senha, papel="vendedor")

        self.status.configure(text="✔ Conta criada!", text_color="lightgreen")
        self.after(800, self.construir_login)


if __name__ == "__main__":
    app = LoginCadastroScreen()
    app.mainloop()
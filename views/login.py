import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import os

from views.core import loja, usuario_logado, atualizar_usuario_logado
from views import theme

class LoginCadastroScreen(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        self.title("NEXO - Login")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass

        theme.apply_global()

        # Fundo gradiente
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.bg_image = self._criar_gradiente(w, h)
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Frame principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.82, relheight=0.95)

        # Título com logo
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(pady=20)

        # LOGO atualizada
        logo_path = os.path.join("img", "nexologo.png")
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open(logo_path),
                size=(130, 90)
            )
            logo_label = ctk.CTkLabel(header_frame, image=logo_img, text="")
            logo_label.image = logo_img
            logo_label.pack(side="left", padx=20, pady=0)
        except Exception as e:
            print("Erro ao carregar a logo:", e)

        subtitulo = ctk.CTkLabel(
            self.main_frame,
            text="Faça login na sua conta",
            font=("Arial", 14),
            text_color="#A4B3C9"
        )
        subtitulo.pack(pady=(0, 30))

        # Card com campos
        self.card = ctk.CTkFrame(self.main_frame, fg_color=theme.CARD_BG, corner_radius=12)
        self.card.pack(fill="both", expand=True, padx=28, pady=28)

        # Scroll interno
        self.scroll = ctk.CTkScrollableFrame(self.card, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self._criar_formulario_login()

        # Botão login
        self.btn_login = ctk.CTkButton(
            self.card,
            text="✓ Entrar",
            height=50,
            font=("Arial", 14, "bold"),
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=self._fazer_login
        )
        self.btn_login.pack(fill="x", padx=24, pady=(8, 20))

        # Link para cadastro
        cadastro_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cadastro_frame.pack(pady=20)

        ctk.CTkLabel(
            cadastro_frame,
            text="Não tem conta? ",
            text_color="white"
        ).pack(side="left")

        ctk.CTkButton(
            cadastro_frame,
            text="Crie uma aqui",
            fg_color="transparent",
            text_color=theme.PRIMARY,
            hover_color="#cfe0ff",
            command=self._ir_para_cadastro
        ).pack(side="left")

    def _criar_gradiente(self, w, h):
        """Cria gradiente para fundo."""
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

    def _criar_formulario_login(self):
        """Cria formulário de login."""
        campos = [
            ("Nome de Usuário", "entry_usuario"),
            ("Senha", "entry_senha"),
        ]

        for label, attr in campos:
            ctk.CTkLabel(
                self.scroll,
                text=label,
                text_color="white",
                font=("Arial", 11)
            ).pack(anchor="w", pady=(15, 5))

            show_char = "*" if "Senha" in label else ""
            entry = ctk.CTkEntry(
                self.scroll,
                placeholder_text=label,
                show=show_char
            )
            entry.pack(anchor="w", pady=(0, 10), fill="x", expand=True)
            setattr(self, attr, entry)

        # Label de status
        self.status = ctk.CTkLabel(
            self.scroll,
            text="",
            text_color="#ff6b6b",
            font=("Arial", 10)
        )
        self.status.pack(pady=20)

    def _fazer_login(self):
        """Realiza login do usuário."""
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            self.status.configure(text="⚠ Preencha todos os campos", text_color="#ff6b6b")
            return

        # Autentica via backend
        usuario_obj = loja.autenticar_usuario(usuario, senha)
        if not usuario_obj:
            self.status.configure(text="❌ Usuário ou senha inválidos", text_color="#ff6b6b")
            return

        # Atualiza usuário logado globalmente
        atualizar_usuario_logado(usuario_obj.id, usuario_obj.nome)

        self.status.configure(text="✔ Login realizado!", text_color="#4ade80")
        # agendar abertura da home e guardar id para possível cancelamento
        try:
            self._after_id = self.after(500, self._abrir_home)
        except Exception:
            self._abrir_home()

    def destroy(self):
        """Cancela callbacks pendentes e destrói a janela."""
        try:
            if hasattr(self, '_after_id') and self._after_id:
                self.after_cancel(self._after_id)
        except Exception:
            pass
        super().destroy()

    def _abrir_home(self):
        """Abre a tela Home."""
        from views.home import TelaHome
        self.destroy()
        TelaHome().mainloop()

    def _ir_para_cadastro(self):
        """Vai para tela de cadastro."""
        from views.cadastro import TelaCadastroInicial
        self.destroy()
        TelaCadastroInicial().mainloop()


if __name__ == "__main__":
    app = LoginCadastroScreen()
    app.mainloop()
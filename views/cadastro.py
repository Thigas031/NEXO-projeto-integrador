import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import os

from views.core import loja, atualizar_usuario_logado
from views import theme


class TelaCadastroInicial(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        self.title("NEXO - Cadastro")
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

        # Tipo de cadastro
        self.tipo = "usuario"

        # Frame principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        # aumentar a área principal do cadastro
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.95)

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
            text="Crie sua conta para começar",
            font=("Arial", 14),
            text_color="#A4B3C9"
        )
        subtitulo.pack(pady=(0, 30))

        # Segmentado para tipo de cadastro
        seg = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["👤 Usuário Comum", "🏢 Vendedor"],
            command=self._mudar_tipo,
            selected_color=theme.PRIMARY
        )
        seg.pack(pady=10, padx=20, fill="x")
        seg.set("👤 Usuário Comum")

        # Card com campos
        # card central maior e mais arejado
        self.card = ctk.CTkFrame(self.main_frame, fg_color=theme.CARD_BG, corner_radius=14)
        self.card.pack(fill="both", expand=True, padx=30, pady=30)

        # Scroll interno
        self.scroll = ctk.CTkScrollableFrame(self.card, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=24, pady=24)

        self._criar_formulario_usuario()

        # Botão cadastrar
        self.btn_cadastrar = ctk.CTkButton(
            self.card,
            text="✓ Criar Conta",
            height=52,
            font=("Arial", 14, "bold"),
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            corner_radius=12,
            command=self._fazer_cadastro
        )
        self.btn_cadastrar.pack(fill="x", padx=24, pady=(10, 20))

        # Link para login
        login_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        login_frame.pack(pady=20)

        ctk.CTkLabel(
            login_frame,
            text="Já tem conta? ",
            text_color="white"
        ).pack(side="left")

        ctk.CTkButton(
            login_frame,
            text="Faça login aqui",
            fg_color="transparent",
            text_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_LIGHT,
            command=self._ir_para_login
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

    def _mudar_tipo(self, valor):
        """Muda entre cadastro de usuário comum e vendedor."""
        if "Usuário" in valor:
            self.tipo = "usuario"
        else:
            self.tipo = "vendedor"

        for w in self.scroll.winfo_children():
            w.destroy()

        if self.tipo == "usuario":
            self._criar_formulario_usuario()
        else:
            self._criar_formulario_vendedor()

    def _criar_formulario_usuario(self):
        """Cria formulário para usuário comum."""
        campos = [
            ("Nome Completo", "entry_nome"),
            ("Email", "entry_email"),
            ("Nome de Usuário", "entry_usuario"),
            ("Senha", "entry_senha"),
            ("Confirmar Senha", "entry_senha_confirm"),
            ("Telefone", "entry_telefone"),
            ("Endereço Completo", "entry_endereco"),
        ]

        self._criar_campos(campos)

    def _criar_formulario_vendedor(self):
        """Cria formulário para vendedor."""
        campos = [
            ("Nome Completo", "entry_nome"),
            ("Email", "entry_email"),
            ("Nome de Usuário", "entry_usuario"),
            ("Senha", "entry_senha"),
            ("Confirmar Senha", "entry_senha_confirm"),
            ("CPF", "entry_cpf"),
            ("Telefone", "entry_telefone"),
            ("Endereço Completo", "entry_endereco"),
            ("Nome da Loja (opcional)", "entry_loja"),
        ]

        self._criar_campos(campos)

    def _criar_campos(self, campos):
        """Cria campos de entrada."""
        for label, attr in campos:
            ctk.CTkLabel(
                self.scroll,
                text=label,
                text_color="white",
                font=("Arial", 11)
            ).pack(anchor="w", pady=(15, 5))

            entry = ctk.CTkEntry(
                self.scroll,
                placeholder_text=label,
                show="*" if "Senha" in label else ""
            )
            entry.pack(anchor="w", pady=(0, 10), fill="x", expand=True)
            setattr(self, attr, entry)

    def _fazer_cadastro(self):
        """Realiza o cadastro."""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        confirmar = self.entry_senha_confirm.get()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get().strip()

        # Delegar validação e cadastro para backend
        if senha != confirmar:
            messagebox.showwarning("Validação", "As senhas não coincidem")
            return

        cpf = self.entry_cpf.get().strip() if hasattr(self, 'entry_cpf') else ""
        loja_nome = self.entry_loja.get().strip() if hasattr(self, 'entry_loja') else ""

        papel = "cliente" if self.tipo == "usuario" else "vendedor"

        sucesso, msg, user = loja.validar_e_cadastrar_usuario(usuario, email, senha, telefone, endereco, papel, cpf, loja_nome)
        if not sucesso:
            messagebox.showerror("Erro", msg)
            return

        messagebox.showinfo("Sucesso", msg + "\nFaça login para continuar.")
        self._ir_para_login()

    def _ir_para_login(self):
        """Vai para tela de login."""
        from views.login import LoginCadastroScreen
        self.destroy()
        LoginCadastroScreen().mainloop()


if __name__ == "__main__":
    app = TelaCadastroInicial()
    app.mainloop()
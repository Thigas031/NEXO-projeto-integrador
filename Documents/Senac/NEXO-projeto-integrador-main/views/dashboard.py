import customtkinter as ctk
from views.assets import criar_logo_label, criar_rodape


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Dashboard")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # MENU LATERAL
        self.sidebar = ctk.CTkFrame(self, width=230, fg_color="#1b1f3b", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # logo no menu lateral
        try:
            logo = criar_logo_label(self.sidebar, mostrar_texto=False, tamanho=22)
            logo.pack(pady=(20, 28))
        except Exception:
            titulo = ctk.CTkLabel(
                self.sidebar,
                text="NEXO",
                font=("Arial", 32, "bold"),
                text_color="white"
            )
            titulo.pack(pady=(30, 40))

        botoes = [
            ("Produtos", self._abrir_produtos),
            ("Estoque", self._abrir_estoque),
            ("Pedidos", self._abrir_pedidos),
            ("Favoritos", self._abrir_favoritos),
            ("Perfil", self._abrir_perfil),
            ("Sair", self._sair)
        ]

        for nome, cmd in botoes:
            ctk.CTkButton(
                self.sidebar,
                text=nome,
                width=180,
                height=40,
                fg_color="#273469",
                hover_color="#3c4f9b",
                text_color="white",
                command=cmd
            ).pack(pady=10)

        # ÁREA PRINCIPAL
        self.main = ctk.CTkFrame(self, fg_color="#2b2e3b")
        self.main.pack(side="right", fill="both", expand=True)

        msg = ctk.CTkLabel(
            self.main,
            text="Bem-vindo ao painel principal.",
            font=("Arial", 26, "bold"),
            text_color="white"
        )
        msg.place(relx=0.5, rely=0.5, anchor="center")

        # rodapé
        try:
            criar_rodape(self)
        except Exception:
            pass

    def _abrir_produtos(self):
        self.destroy()
        from views.produtos import TelaProdutos
        TelaProdutos().mainloop()

    def _abrir_estoque(self):
        self.destroy()
        from views.estoque import TelaEstoque
        TelaEstoque().mainloop()

    def _abrir_pedidos(self):
        self.destroy()
        from views.pedidos import TelaPedidos
        TelaPedidos().mainloop()

    def _abrir_favoritos(self):
        self.destroy()
        from views.favoritos import TelaFavoritos
        TelaFavoritos().mainloop()

    def _abrir_perfil(self):
        self.destroy()
        from views.perfil import TelaPerfil
        TelaPerfil().mainloop()

    def _sair(self):
        self.destroy()
        from views.login import LoginCadastroScreen
        LoginCadastroScreen().mainloop()


if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
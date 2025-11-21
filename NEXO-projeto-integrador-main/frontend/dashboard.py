import customtkinter as ctk

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Dashboard")
        self.state("zoomed")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # MENU LATERAL
        self.sidebar = ctk.CTkFrame(self, width=230, fg_color="#1b1f3b", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        titulo = ctk.CTkLabel(
            self.sidebar,
            text="NEXO",
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        titulo.pack(pady=(30, 40))

        botoes = [
            "Produtos",
            "Estoque",
            "Pedidos",
            "Favoritos",
            "Perfil",
            "Sair"
        ]

        for nome in botoes:
            ctk.CTkButton(
                self.sidebar,
                text=nome,
                width=180,
                height=40,
                fg_color="#273469",
                hover_color="#3c4f9b",
                text_color="white",
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


if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
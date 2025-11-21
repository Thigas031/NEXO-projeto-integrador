import customtkinter as ctk

class TelaProdutos(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Produtos")
        self.state("zoomed")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        titulo = ctk.CTkLabel(
            self,
            text="Gerenciamento de Produtos",
            font=("Arial", 30, "bold"),
            text_color="white"
        )
        titulo.pack(pady=20)

        self.lista = ctk.CTkFrame(self, fg_color="#2b2e3b")
        self.lista.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self.lista,
            text="(Produtos aparecerão aqui após integração)",
            font=("Arial", 16),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = TelaProdutos()
    app.mainloop()
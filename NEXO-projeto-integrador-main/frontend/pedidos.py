import customtkinter as ctk

class TelaPedidos(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Pedidos")
        self.state("zoomed")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(
            self,
            text="Pedidos e Carrinho",
            font=("Arial", 30, "bold"),
            text_color="white"
        ).pack(pady=20)

        painel = ctk.CTkFrame(self, fg_color="#2b2e3b")
        painel.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            painel,
            text="(Pedidos aparecerão aqui após integração)",
            font=("Arial", 16),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = TelaPedidos()
    app.mainloop()
import customtkinter as ctk

from views.core import loja
from views.assets import criar_logo_label, criar_rodape


class TelaEstoque(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Estoque")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Controle de Estoque",
                     font=("Arial", 30, "bold"), text_color="white").pack(pady=20)

        # logo no topo
        try:
            logo = criar_logo_label(self, mostrar_texto=False)
            logo.place(x=140, y=20)
        except Exception:
            pass

        self.container = ctk.CTkFrame(self, fg_color="#2b2e3b")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # botão voltar padrão
        from views.assets import criar_back_button
        criar_back_button(self, command=self._voltar, x=20, y=20)

        self._carregar()

        # rodapé
        try:
            criar_rodape(self)
        except Exception:
            pass

    def _voltar(self):
        self.destroy()
        from views.dashboard import Dashboard
        Dashboard().mainloop()

    def _carregar(self):
        for w in self.container.winfo_children():
            w.destroy()

        produtos = loja.estoque.todos()
        if not produtos:
            ctk.CTkLabel(self.container, text="Nenhum produto em estoque",
                         font=("Arial", 16), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
            return

        for p in produtos:
            frame = ctk.CTkFrame(self.container, fg_color="#3b3b5c", corner_radius=6)
            frame.pack(fill="x", pady=6)
            ctk.CTkLabel(frame, text=f"{p.nome}", font=("Arial", 14), text_color="white").pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(frame, text=f"Estoque: {p.estoque}", font=("Arial", 14), text_color="#ffffff").pack(side="left", padx=12)


if __name__ == "__main__":
    app = TelaEstoque()
    app.mainloop()
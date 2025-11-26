import customtkinter as ctk
from tkinter import messagebox

from views.core import loja, usuario_logado
from views.assets import criar_logo_label, criar_rodape


class TelaPedidos(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Pedidos")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Carrinho e Pedidos",
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
        from views.home import TelaHome
        TelaHome().mainloop()

    def _carregar(self):
        for w in self.container.winfo_children():
            w.destroy()

        itens = loja.carrinho.itens
        if not itens:
            ctk.CTkLabel(self.container, text="Carrinho vazio",
                         font=("Arial", 16), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
            return

        total = loja.carrinho.total()

        for i, it in enumerate(itens):
            frame = ctk.CTkFrame(self.container, fg_color="#3b3b5c", corner_radius=6)
            frame.pack(fill="x", pady=8)

            txt = f"{it.produto.nome}  |  Qtd: {it.quantidade}  |  R$ {it.subtotal():.2f}"
            ctk.CTkLabel(frame, text=txt, font=("Arial", 14), text_color="white").pack(side="left", padx=10, pady=10)

            btns = ctk.CTkFrame(frame, fg_color="transparent")
            btns.pack(side="right", padx=10)
            ctk.CTkButton(btns, text="Remover", width=120,
                          fg_color="#7f1f1f", hover_color="#9b2a2a",
                          command=lambda idx=i: self._remover(idx)).pack()

        # total e ações
        rodape = ctk.CTkFrame(self, fg_color="#2b2e3b")
        rodape.pack(fill="x", side="bottom")

        ctk.CTkLabel(rodape, text=f"Total: R$ {total:.2f}", font=("Arial", 18, "bold"), text_color="#16A34A").pack(side="left", padx=20, pady=12)

        ctk.CTkButton(rodape, text="Limpar Carrinho", fg_color="#1b1f3b", hover_color="#2c355e",
                      command=self._limpar).pack(side="right", padx=12, pady=12)

        ctk.CTkButton(rodape, text="Fechar Pedido", fg_color="#0f172a", hover_color="#213055",
                      command=self._fechar).pack(side="right", padx=12, pady=12)

    def _remover(self, idx):
        try:
            loja.carrinho.itens.pop(idx)
        except Exception:
            pass
        self._carregar()

    def _limpar(self):
        loja.carrinho.limpar()
        self._carregar()

    def _fechar(self):
        uid = usuario_logado.get("id")
        pedido = loja.fechar_pedido(cliente_id=uid)
        if not pedido:
            messagebox.showerror("Pagamento", "Falha no processamento do pagamento.")
            return
        messagebox.showinfo("Pedido", f"Pedido #{pedido.id} fechado com sucesso. Total: R$ {pedido.total():.2f}")
        self._carregar()


if __name__ == "__main__":
    app = TelaPedidos()
    app.mainloop()
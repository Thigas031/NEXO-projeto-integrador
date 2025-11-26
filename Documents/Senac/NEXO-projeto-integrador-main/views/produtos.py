import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageOps

from views.core import loja, usuario_logado
from views.assets import criar_logo_label, criar_rodape, criar_back_button, criar_produto_card


class TelaProdutos(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Produtos")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        titulo = ctk.CTkLabel(
            self,
            text="Produtos",
            font=("Arial", 30, "bold"),
            text_color="white"
        )
        titulo.pack(pady=20)

        # logo (placeholder emoji) ao lado do topo
        try:
            logo = criar_logo_label(self, mostrar_texto=False)
            logo.place(x=140, y=20)
        except Exception:
            pass

        self.container = ctk.CTkFrame(self, fg_color="#2b2e3b")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # botão voltar
        # botão voltar (helper)
        criar_back_button(self, command=self._voltar, x=20, y=20)

        self._carregar_lista()

        # rodapé
        try:
            criar_rodape(self)
        except Exception:
            pass

    def _voltar(self):
        self.destroy()
        from views.dashboard import Dashboard
        Dashboard().mainloop()

    def _carregar_lista(self):
        for w in self.container.winfo_children():
            w.destroy()

        produtos = loja.estoque.todos()
        if not produtos:
            ctk.CTkLabel(self.container, text="Nenhum produto cadastrado",
                         font=("Arial", 16), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
            return

        for p in produtos:
            card = ctk.CTkFrame(self.container, fg_color="#3b3b5c", corner_radius=6)
            card.pack(fill="x", pady=8)

            lbl = ctk.CTkLabel(card, text=f"{p.nome} — {p.categoria}  |  R$ {p.preco:.2f}  |  Estoque: {p.estoque}",
                                font=("Arial", 14), text_color="white")
            lbl.pack(side="left", padx=10, pady=12)

            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(side="right", padx=10)

            ctk.CTkButton(btns, text="Adicionar ao carrinho", width=180,
                          fg_color="#0f172a", hover_color="#213055",
                          command=lambda nome=p.nome: self._adicionar(nome)).pack(side="left", padx=6)

            # favoritar (apenas se houver usuário)
            ctk.CTkButton(btns, text="❤",
                          width=60, fg_color="#1b1f3b",
                          hover_color="#2c355e",
                          command=lambda pid=p.id: self._favoritar(pid)).pack(side="left", padx=6)

            # editar / remover
            ctk.CTkButton(btns, text="Editar", width=80,
                          fg_color="#2563eb", hover_color="#1e40af",
                          command=lambda prod=p: self._abrir_editar(prod)).pack(side="left", padx=6)

            ctk.CTkButton(btns, text="Remover", width=80,
                          fg_color="#7f1f1f", hover_color="#9b2a2a",
                          command=lambda pid=p.id: self._remover_confirm(pid)).pack(side="left", padx=6)

    def _adicionar(self, nome):
        ok = loja.adicionar_ao_carrinho(nome, 1)
        if ok:
            messagebox.showinfo("Carrinho", f"{nome} adicionado ao carrinho!")
        else:
            messagebox.showerror("Erro", "Estoque insuficiente.")

    def _favoritar(self, produto_id):
        uid = usuario_logado.get("id")
        if not uid:
            messagebox.showinfo("Favoritos", "Você precisa estar logado.")
            return
        loja.favoritar(uid, produto_id)
        messagebox.showinfo("Favoritos", "Produto favoritado.")

    # ------------------ edição / remoção ------------------
    def _abrir_editar(self, produto):
        DialogEditarProduto(self, produto, self._on_editado)

    def _on_editado(self, ok):
        if ok:
            self._carregar_lista()

    def _remover_confirm(self, produto_id):
        if messagebox.askyesno("Remover produto", "Deseja realmente remover este produto?"):
            loja.remover_produto(produto_id)
            messagebox.showinfo("Remover", "Produto removido.")
            self._carregar_lista()


class DialogEditarProduto(ctk.CTkToplevel):
    def __init__(self, parent, produto, callback):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title("Editar Produto")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass
        self.produto = produto
        self.callback = callback

        container = ctk.CTkFrame(self, fg_color="#0F172A")
        container.place(relwidth=1, relheight=1)

        ctk.CTkLabel(container, text="Editar Produto", font=("Arial", 18, "bold"), text_color="white").place(relx=0.5, rely=0.06, anchor="center")

        y = 0.18
        self.entry_nome = ctk.CTkEntry(container, width=380, placeholder_text="Nome")
        self.entry_nome.place(relx=0.1, rely=y)
        self.entry_nome.insert(0, produto.nome)

        y += 0.12
        self.entry_categoria = ctk.CTkEntry(container, width=380, placeholder_text="Categoria")
        self.entry_categoria.place(relx=0.1, rely=y)
        self.entry_categoria.insert(0, produto.categoria)

        y += 0.12
        self.entry_preco = ctk.CTkEntry(container, width=180, placeholder_text="Preço")
        self.entry_preco.place(relx=0.1, rely=y)
        self.entry_preco.insert(0, f"{produto.preco:.2f}")

        self.entry_estoque = ctk.CTkEntry(container, width=180, placeholder_text="Estoque")
        self.entry_estoque.place(relx=0.6, rely=y)
        self.entry_estoque.insert(0, str(produto.estoque))

        y += 0.14
        ctk.CTkButton(container, text="Escolher imagem", fg_color="#334155", hover_color="#475569", command=self._escolher_imagem).place(relx=0.1, rely=y)

        ctk.CTkButton(container, text="Salvar", fg_color="#0f172a", hover_color="#213055", command=self._salvar).place(relx=0.5, rely=0.86, anchor="center")

        self.imagem_path = produto.imagem

    def _escolher_imagem(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if path:
            self.imagem_path = path

    def _salvar(self):
        nome = self.entry_nome.get().strip()
        categoria = self.entry_categoria.get().strip()
        preco = self.entry_preco.get().strip()
        estoque = self.entry_estoque.get().strip()

        if not nome or not preco or not estoque:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return

        try:
            preco_val = float(preco.replace(",", "."))
            estoque_val = int(estoque)
        except:
            messagebox.showerror("Erro", "Preço ou estoque inválido")
            return

        ok = loja.editar_produto(self.produto.id, novo_nome=nome, nova_categoria=categoria, novo_preco=preco_val, novo_estoque=estoque_val, nova_imagem=self.imagem_path)
        if ok:
            messagebox.showinfo("OK", "Produto atualizado")
            self.callback(True)
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar produto")


if __name__ == "__main__":
    app = TelaProdutos()
    app.mainloop()
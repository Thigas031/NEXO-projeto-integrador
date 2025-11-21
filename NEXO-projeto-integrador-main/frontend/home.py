import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageFont

from frontend.core import loja, usuario_logado

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TelaHome(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEXO - Home")
        self.state("zoomed")

        # filtros
        self.filtro_categoria = None
        self.filtro_texto = ""

        # fundo gradiente
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        gradient = self.gerar_gradiente(w, h)
        self.bg = ctk.CTkLabel(self, text="", image=gradient)
        self.bg.image = gradient
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        # TOPBAR
        self.topbar = ctk.CTkFrame(self, height=72, fg_color="#2f49c8", corner_radius=0)
        self.topbar.place(relx=0, rely=0, relwidth=1)

        ctk.CTkLabel(self.topbar, text="❤ Favoritos",
                     text_color="white", font=("Arial", 18, "bold")).place(x=20, y=20)

        self.search_entry = ctk.CTkEntry(
            self.topbar, width=500, height=38,
            placeholder_text="Buscar produtos, marcas e muito mais..."
        )
        self.search_entry.place(relx=0.5, y=36, anchor="center")
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_change())

        ctk.CTkLabel(self.topbar, text="🛒 Carrinho", text_color="white",
                     font=("Arial", 18)).place(relx=0.85, y=22)
        ctk.CTkLabel(self.topbar, text="😀", font=("Arial", 34)).place(relx=0.93, y=10)

        # CATEGORIAS
        self.catbar = ctk.CTkFrame(self, height=48, fg_color="#3f5dff", corner_radius=0)
        self.catbar.place(relx=0, y=72, relwidth=1)

        self.btn_categorias = ctk.CTkButton(
            self.catbar, text="Categorias ⌄", width=160,
            fg_color="transparent", hover_color="#5670ff",
            text_color="white", command=self.toggle_dropdown
        )
        self.btn_categorias.place(relx=0.12, rely=0.5, anchor="center")

        categorias_top = ["Ofertas", "Supermercado", "Moda", "Eletrônicos",
                          "Esportes", "Casa", "Contato"]
        pos = 0.28
        for nome in categorias_top:
            lbl = ctk.CTkLabel(self.catbar, text=nome,
                               text_color="white", font=("Arial", 16))
            lbl.place(relx=pos, rely=0.5, anchor="center")
            lbl.bind("<Button-1>", lambda e, n=nome: self._categoria_label_click(n))
            pos += 0.11

        # DROPDOWN
        self.dropdown = ctk.CTkFrame(self, fg_color="#2d3a8c", corner_radius=6)
        self.dropdown_visible = False

        for nome in ["Supermercado", "Moda", "Eletrônicos", "Esportes", "Casa"]:
            ctk.CTkButton(self.dropdown, text=nome,
                          fg_color="transparent", hover_color="#3c4ca8",
                          text_color="white",
                          command=lambda n=nome: self.selecionar_categoria(n)).pack(padx=8, pady=6)

        self.bind("<Button-1>", self.verificar_click)

        # ÁREA DE PRODUTOS (SCROLL)
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            width=int(self.winfo_screenwidth() * 0.9), height=700
        )
        self.scroll_frame.place(relx=0.5, rely=0.56, anchor="center")

        # Botão adicionar produto
        self.btn_add_prod = ctk.CTkButton(
            self, text="➕ Adicionar Produto",
            fg_color="#1E293B", hover_color="#334155",
            width=180, command=self.abrir_dialogo_novo_produto
        )
        self._ajustar_visibilidade_adicionar()

        # CARREGAR GRID
        self.carregar_produtos()

    def _usuario_logado_obj(self):
        try:
            if usuario_logado.get("id"):
                return loja.buscar_usuario(usuario_logado["id"])
        except:
            return None
        return None

    def _ajustar_visibilidade_adicionar(self):
        u = self._usuario_logado_obj()
        if u and u.papel == "vendedor":
            self.btn_add_prod.place(relx=0.86, rely=0.23, anchor="center")
        else:
            self.btn_add_prod.place_forget()

    # GRADIENTE
    def gerar_gradiente(self, w, h):
        cor1 = (10, 60, 200)
        cor2 = (3, 18, 70)
        img = Image.new("RGB", (w, h), cor1)
        draw = ImageDraw.Draw(img)
        for y in range(h):
            r = int(cor1[0] + (cor2[0] - cor1[0]) * (y / h))
            g = int(cor1[1] + (cor2[1] - cor1[1]) * (y / h))
            b = int(cor1[2] + (cor2[2] - cor1[2]) * (y / h))
            draw.line([(0, y), (w, y)], fill=(r, g, b))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))

    # FILTROS
    def _on_search_change(self):
        self.filtro_texto = self.search_entry.get().strip().lower()
        self.carregar_produtos()

    def _categoria_label_click(self, nome):
        self.filtro_categoria = None if self.filtro_categoria == nome else nome
        self.carregar_produtos()

    # CARREGAR PRODUTOS EM GRID 4xN
    def carregar_produtos(self):
        # limpar
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        todos = loja.estoque.todos()

        filtrados = []
        for p in todos:
            if self.filtro_texto and self.filtro_texto not in f"{p.nome} {p.categoria}".lower():
                continue
            if self.filtro_categoria and p.categoria.lower() != self.filtro_categoria.lower():
                continue
            filtrados.append(p)

        if len(filtrados) == 0:
            ctk.CTkLabel(self.scroll_frame, text="Nenhum produto encontrado",
                         text_color="white", font=("Arial", 20, "bold")).grid(row=0, column=0)
            return

        cols = 4
        for i, p in enumerate(filtrados):
            r = i // cols
            c = i % cols
            self._criar_card_produto(p, r, c)

    def _criar_card_produto(self, produto, row, col):
        card = ctk.CTkFrame(self.scroll_frame, width=300, height=360,
                            corner_radius=12, fg_color="#6f7dc8")
        card.grid(row=row, column=col, padx=20, pady=20)
        card.pack_propagate(False)

        img_w, img_h = 260, 160
        img = self._carregar_imagem_produto(produto, img_w, img_h)

        img_frame = ctk.CTkFrame(card, width=img_w, height=img_h,
                                 corner_radius=8, fg_color="#d7eefc")
        img_frame.pack(pady=(18, 8))
        img_frame.pack_propagate(False)

        lbl_img = ctk.CTkLabel(img_frame, image=img, text="")
        lbl_img.image = img
        lbl_img.pack(fill="both", expand=True)

        ctk.CTkLabel(card, text=produto.nome,
                     font=("Arial", 16, "bold"), text_color="white").pack()

        ctk.CTkLabel(card, text=produto.categoria,
                     font=("Arial", 12), text_color="#CCCCCC").pack()

        ctk.CTkLabel(card, text=f"R$ {produto.preco:.2f}",
                     font=("Arial", 15, "bold"), text_color="#16A34A").pack(pady=4)

        bottom = ctk.CTkFrame(card, fg_color="transparent")
        bottom.pack(fill="x", pady=8)

        # favorito
        fav_btn = ctk.CTkButton(bottom, text="♡", width=60, fg_color="#1b1f3b",
                                hover_color="#2c355e",
                                command=lambda p=produto: self._toggle_favorito(p))
        fav_btn.pack(side="left", padx=6)
        self._atualizar_estado_favorito_visual(fav_btn, produto)

        # carrinho
        ctk.CTkButton(bottom, text="Adicionar", width=120,
                      fg_color="#0f172a", hover_color="#213055",
                      command=lambda p=produto: self._adicionar_ao_carrinho(p)).pack(side="right")

    def _carregar_imagem_produto(self, produto, w, h):
        if hasattr(produto, "imagem") and produto.imagem and os.path.exists(produto.imagem):
            try:
                img = Image.open(produto.imagem).convert("RGB")
                final = ImageOps.fit(img, (w, h), Image.LANCZOS)
                return ctk.CTkImage(final, size=(w, h))
            except:
                pass

        # placeholder
        ph = Image.new("RGB", (w, h), (215, 238, 252))
        draw = ImageDraw.Draw(ph)
        try:
            fnt = ImageFont.truetype("arial.ttf", 22)
        except:
            fnt = ImageFont.load_default()
        draw.text((w//3, h//3), "Imagem\nProduto", fill="black", font=fnt)
        return ctk.CTkImage(ph, size=(w, h))

    # FAVORITO
    def _toggle_favorito(self, produto):
        u = self._usuario_logado_obj()
        if not u:
            messagebox.showinfo("Favoritos", "Você precisa estar logado.")
            return

        if produto in u.favoritos:
            loja.desfavoritar(u.id, produto.id)
        else:
            loja.favoritar(u.id, produto.id)

        self.carregar_produtos()

    def _atualizar_estado_favorito_visual(self, btn, produto):
        u = self._usuario_logado_obj()
        if not u:
            return
        if produto in u.favoritos:
            btn.configure(text="❤", fg_color="#7b1f1f")
        else:
            btn.configure(text="♡", fg_color="#1b1f3b")

    # CARRINHO
    def _adicionar_ao_carrinho(self, produto):
        ok = loja.adicionar_ao_carrinho(produto.nome, 1)
        if ok:
            messagebox.showinfo("Carrinho", f"{produto.nome} adicionado ao carrinho!")
        else:
            messagebox.showerror("Erro", "Estoque insuficiente.")

    # DROPDOWN
    def toggle_dropdown(self):
        if self.dropdown_visible:
            self.dropdown.place_forget()
            self.dropdown_visible = False
            return

        self.update_idletasks()

        bx = self.btn_categorias.winfo_rootx()
        by = self.btn_categorias.winfo_rooty() + self.btn_categorias.winfo_height()
        x = bx - self.winfo_rootx()
        y = by - self.winfo_rooty()

        self.dropdown.place(x=x, y=y)
        self.dropdown_visible = True

    def selecionar_categoria(self, nome):
        self.filtro_categoria = nome
        self.dropdown.place_forget()
        self.dropdown_visible = False
        self.carregar_produtos()

    def verificar_click(self, event):
        if not self.dropdown_visible:
            return

        x, y = event.x_root, event.y_root
        if not (
            self.dropdown.winfo_rootx() <= x <= self.dropdown.winfo_rootx() + self.dropdown.winfo_width() and
            self.dropdown.winfo_rooty() <= y <= self.dropdown.winfo_rooty() + self.dropdown.winfo_height()
        ):
            self.dropdown.place_forget()
            self.dropdown_visible = False

    # POPUP — ADICIONAR PRODUTO
    def abrir_dialogo_novo_produto(self):
        DialogNovoProduto(self, self._on_novo_produto_criado)

    def _on_novo_produto_criado(self, prod):
        self.carregar_produtos()


# POPUP
class DialogNovoProduto(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Adicionar Produto")
        self.geometry("720x520")
        self.transient(parent)
        self.grab_set()

        self.callback = callback
        self.imagem_path = None

        container = ctk.CTkFrame(self, fg_color="#0F172A")
        container.place(relwidth=1, relheight=1)

        ctk.CTkLabel(container, text="Novo Produto", font=("Arial", 22, "bold"),
                     text_color="white").place(relx=0.5, rely=0.07, anchor="center")

        # CARD
        card = ctk.CTkFrame(container, width=640, height=380, fg_color="#1E293B", corner_radius=6)
        card.place(relx=0.5, rely=0.16, anchor="n")
        card.pack_propagate(False)

        # IMAGEM
        left = ctk.CTkFrame(card, width=240, height=320, fg_color="#111827", corner_radius=6)
        left.place(x=20, y=20)
        left.pack_propagate(False)

        self.preview = ctk.CTkLabel(left, text="")
        self.preview.pack(expand=True, fill="both", padx=6, pady=6)

        ctk.CTkButton(left, text="Escolher imagem", fg_color="#334155",
                      hover_color="#475569", command=self._escolher_imagem).pack(pady=8)

        # CAMPOS
        right = ctk.CTkFrame(card, width=360, height=320, fg_color="transparent")
        right.place(x=280, y=20)
        right.pack_propagate(False)

        self.entry_nome = ctk.CTkEntry(right, placeholder_text="Nome do produto", width=320)
        self.entry_nome.pack(pady=6)

        # CATEGORIA COMBOBOX
        self.combo_categoria = ctk.CTkComboBox(
            right,
            values=["Supermercado", "Moda", "Eletrônicos", "Esportes", "Casa", "Outros"],
            width=320
        )
        self.combo_categoria.pack(pady=6)
        self.combo_categoria.set("Outros")

        self.entry_preco = ctk.CTkEntry(right, placeholder_text="Preço", width=320)
        self.entry_preco.pack(pady=6)

        self.entry_estoque = ctk.CTkEntry(right, placeholder_text="Estoque", width=320)
        self.entry_estoque.pack(pady=6)

        ctk.CTkButton(container, text="Salvar Produto", fg_color="#0f172a", width=200,
                      hover_color="#213055", command=self._salvar).place(relx=0.5, rely=0.88, anchor="center")

    def _escolher_imagem(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not path:
            return
        self.imagem_path = path
        img = Image.open(path).convert("RGB")
        final = ImageOps.fit(img, (220, 180), Image.LANCZOS)
        tkimg = ctk.CTkImage(final, size=(220, 180))
        self.preview.configure(image=tkimg)
        self.preview.image = tkimg

    def _salvar(self):
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get().strip()
        preco = self.entry_preco.get().strip()
        estoque = self.entry_estoque.get().strip()

        if not nome or not preco or not estoque:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            preco = float(preco.replace(",", "."))
            estoque = int(estoque)
        except:
            messagebox.showerror("Erro", "Preço ou estoque inválido.")
            return

        produto = loja.cadastrar_produto(nome, categoria, preco, estoque, imagem=self.imagem_path)

        if callable(self.callback):
            self.callback(produto)

        messagebox.showinfo("OK", "Produto cadastrado!")
        self.destroy()


if __name__ == "__main__":
    TelaHome().mainloop()
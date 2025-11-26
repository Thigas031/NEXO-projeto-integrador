"""
TELA DE FAVORITOS
Exibe produtos favoritados pelo usuário
"""

import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageOps

from views.core import loja, usuario_logado
from views import theme


class TelaFavoritos(ctk.CTk):
    """Tela de produtos favoritados."""
    
    def __init__(self):
        super().__init__()

        self.title("NEXO - Favoritos")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass

        theme.apply_global()

        # Fundo
        bg = ctk.CTkFrame(self, fg_color=theme.BG)
        bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color=theme.CARD_BG, height=80, corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1)
        header.pack_propagate(False)

        # Título com ícone
        fav_icon = theme.load_icon('favoritos.png', size=(32, 32))
        if fav_icon:
            fav_label = ctk.CTkLabel(header, image=fav_icon, text="")
            fav_label.image = fav_icon
            fav_label.pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            header, text="Meus Favoritos",
            font=("Arial", 28, "bold"),
            text_color="white"
        ).pack(side="left", padx=(0, 30), pady=20)

        # Botão voltar
        ctk.CTkButton(
            header,
            text="← Voltar",
            width=100,
            fg_color=theme.ACCENT,
            hover_color=theme.PRIMARY,
            command=self._voltar
        ).pack(side="right", padx=30, pady=20)

        # Frame principal
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)

        # Scroll frame para favoritos
        self.scroll_frame = ctk.CTkScrollableFrame(
            main, fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Carregar favoritos
        self._carregar_favoritos()

    def _carregar_favoritos(self):
        """Carrega e exibe os favoritos do usuário."""
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        uid = usuario_logado.get("id")
        if not uid:
            ctk.CTkLabel(
                self.scroll_frame,
                text="Faça login para acessar seus favoritos",
                text_color="#9AA6C0",
                font=("Arial", 14)
            ).pack(pady=40)
            return

        # Obter produtos favoritos
        produtos = loja.listar_produtos_favoritos(uid)

        if not produtos:
            ctk.CTkLabel(
                self.scroll_frame,
                text="Nenhum produto nos favoritos ainda",
                text_color="#9AA6C0",
                font=("Arial", 14)
            ).pack(pady=40)
            return

        # Exibir produtos em grid
        cols = 5
        for i, p in enumerate(produtos):
            row = i // cols
            col = i % cols
            self._criar_card_favorito(p, row, col)

    def _criar_card_favorito(self, produto, row, col):
        """Cria um card para produto favoritado."""
        card = ctk.CTkFrame(self.scroll_frame, fg_color=theme.CARD_BG, corner_radius=12)
        card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

        # Imagem
        img = self._carregar_imagem_produto(produto, 180, 140)
        img_label = ctk.CTkLabel(card, image=img, text="")
        img_label.image = img
        img_label.pack(padx=8, pady=8, fill="both", expand=True)

        # Nome
        ctk.CTkLabel(
            card,
            text=produto.nome,
            font=("Arial", 12, "bold"),
            text_color="white"
        ).pack(padx=10, pady=(0, 3), anchor="w")

        # Preço
        ctk.CTkLabel(
            card,
            text=f"R$ {produto.preco:.2f}",
            font=("Arial", 13, "bold"),
            text_color="#00d084"
        ).pack(padx=10, anchor="w")

        # Categoria
        ctk.CTkLabel(
            card,
            text=f"{produto.categoria}",
            font=("Arial", 10),
            text_color="#A4B3C9"
        ).pack(padx=10, anchor="w")

        # Botões
        btnframe = ctk.CTkFrame(card, fg_color="transparent")
        btnframe.pack(fill="x", padx=8, pady=(10, 8))

        ctk.CTkButton(
            btnframe,
            text="Ver",
            width=50,
            font=("Arial", 10),
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=lambda: self._ver_produto(produto)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btnframe,
            text="Adicionar",
            width=60,
            font=("Arial", 10),
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=lambda: self._adicionar_ao_carrinho(produto)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btnframe,
            text="✕ Remover",
            width=70,
            font=("Arial", 10),
            fg_color=theme.ALT_BG,
            hover_color=theme.PRIMARY_DARK,
            command=lambda: self._remover_favorito(produto.id)
        ).pack(side="left", padx=2)

    def _carregar_imagem_produto(self, produto, w, h):
        """Carrega ou cria imagem para o produto."""
        if produto.imagem and os.path.exists(produto.imagem):
            try:
                img = Image.open(produto.imagem).convert("RGB")
                img = ImageOps.fit(img, (w, h), Image.LANCZOS)
                return ctk.CTkImage(img, size=(w, h))
            except:
                pass

        # Imagem padrão
        img = Image.new("RGB", (w, h), (100, 140, 255))
        return ctk.CTkImage(img, size=(w, h))

    def _ver_produto(self, produto):
        """Mostra informações do produto."""
        info = f"""
Produto: {produto.nome}
Categoria: {produto.categoria}
Preço: R$ {produto.preco:.2f}
Estoque: {produto.estoque}
        """
        messagebox.showinfo("Detalhes do Produto", info.strip())

    def _adicionar_ao_carrinho(self, produto):
        """Adiciona produto ao carrinho."""
        if produto.estoque <= 0:
            messagebox.showwarning("Estoque", "Produto fora de estoque")
            return

        # Verifica se já existe
        para_atualizar = None
        for item in loja.carrinho.itens:
            if item.produto.id == produto.id:
                para_atualizar = item
                break

        if para_atualizar:
            para_atualizar.quantidade += 1
            messagebox.showinfo("Carrinho", "Quantidade atualizada!")
        else:
            loja.carrinho.adicionar(produto, 1)
            messagebox.showinfo("Carrinho", f"{produto.nome} adicionado!")

    def _remover_favorito(self, produto_id):
        """Remove produto dos favoritos."""
        uid = usuario_logado.get("id")
        if uid:
            loja.remover_favorito(uid, produto_id)
            self._carregar_favoritos()

    def _voltar(self):
        """Volta para home."""
        from views.home import TelaHome
        self.destroy()
        TelaHome().mainloop()


if __name__ == "__main__":
    TelaFavoritos().mainloop()

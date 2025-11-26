import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageOps

from views.core import loja, usuario_logado, limpar_usuario_logado, get_usuario_obj
from views import theme

theme.apply_global()


class TelaHome(ctk.CTk):
    """Tela principal com catálogo de produtos."""
    
    def __init__(self):
        super().__init__()

        self.title("NEXO - Home")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass

        # Estado de filtros
        self.filtro_categoria = None
        self.filtro_texto = ""

        # Fundo gradiente
        self._criar_fundo()

        # Header com logo e busca
        self._criar_topbar()

        # Categorias
        self._criar_catbar()

        # Área de produtos - MAIOR E MAIS LARGA
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.scroll_frame.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.95, relheight=0.82)

        # Carregar produtos
        self.carregar_produtos()

    def _criar_fundo(self):
        """Cria fundo com gradiente."""
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        gradient = self._criar_gradiente(w, h, (10, 60, 200), (3, 18, 70))

        self.bg = ctk.CTkLabel(self, text="", image=gradient)
        self.bg.image = gradient
        self.bg.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    def _criar_gradiente(self, w, h, cor_inicio, cor_fim):
        """Cria gradiente para fundo."""
        img = Image.new("RGB", (min(w, 1400), min(h, 900)))
        draw = ImageDraw.Draw(img)

        for i in range(img.height):
            ratio = i / img.height
            r = int(cor_inicio[0] * (1 - ratio) + cor_fim[0] * ratio)
            g = int(cor_inicio[1] * (1 - ratio) + cor_fim[1] * ratio)
            b = int(cor_inicio[2] * (1 - ratio) + cor_fim[2] * ratio)
            draw.line([(0, i), (img.width, i)], fill=(r, g, b))

        return ctk.CTkImage(light_image=img, size=(w, h))

    def _criar_topbar(self):
        """Cria barra superior com logo, busca e botões."""
        topbar = ctk.CTkFrame(self, fg_color=theme.CARD_BG, height=70, corner_radius=0)
        topbar.place(relx=0, rely=0, relwidth=1)
        topbar.pack_propagate(False)

        # LOGO
        logo_path = os.path.join("img", "nexologo.png")

        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open(logo_path),
                size=(70, 40)
            )

            logo_label = ctk.CTkLabel(
                topbar,
                image=logo_img,
                text=""
            )
            logo_label.image = logo_img
            logo_label.pack(side="left", padx=20, pady=0)

        except Exception as e:
            print("Erro ao carregar a logo:", e)

        # Barra de busca
        self.search_entry = ctk.CTkEntry(
            topbar,
            width=320,
            placeholder_text="🔍 Buscar produtos...",
            fg_color=theme.BG,
            text_color="white"
        )
        self.search_entry.pack(side="left", padx=10, pady=15)
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_change())

        # Botões direita
        # Botões do vendedor (se aplicável)
        usuario_obj = self._get_usuario_obj()
        if usuario_obj and usuario_obj.papel == "vendedor":
            ctk.CTkButton(
                topbar,
                text="📦 Meus Produtos",
                width=130,
                fg_color=theme.ACCENT,
                hover_color=theme.PRIMARY_DARK,
                command=self._abrir_meus_produtos
            ).pack(side="right", padx=10, pady=15)
            
            ctk.CTkButton(
                topbar,
                text="📊 Estatísticas",
                width=130,
                fg_color=theme.ACCENT,
                hover_color=theme.PRIMARY_DARK,
                command=self._abrir_estatisticas
            ).pack(side="right", padx=10, pady=15)
            
            ctk.CTkButton(
                topbar,
                text="📋 Relatórios",
                width=130,
                fg_color=theme.ACCENT,
                hover_color=theme.PRIMARY_DARK,
                command=self._abrir_relatorios
            ).pack(side="right", padx=10, pady=15)
        
        # Botões gerais
        fav_icon = theme.load_icon('favoritos.png', size=(20, 20))
        cart_icon = theme.load_icon('carrinho.png', size=(20, 20))
        
        ctk.CTkButton(
            topbar,
            text="Favoritos" if fav_icon else "❤️ Favoritos",
            image=fav_icon,
            width=120,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=self._abrir_favoritos
        ).pack(side="right", padx=10, pady=15)

        ctk.CTkButton(
            topbar,
            text="Carrinho" if cart_icon else "🛒 Carrinho",
            image=cart_icon,
            width=100,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=self._abrir_carrinho
        ).pack(side="right", padx=10, pady=15)

        ctk.CTkButton(
            topbar,
            text="👤 Perfil",
            width=100,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=self._abrir_perfil
        ).pack(side="right", padx=10, pady=15)

        ctk.CTkButton(
            topbar,
            text="🚪 Sair",
            width=80,
            fg_color=theme.ALT_BG,
            hover_color=theme.PRIMARY_DARK,
            command=self._fazer_logout
        ).pack(side="right", padx=10, pady=15)

    def _criar_catbar(self):
        """Cria barra de categorias."""
        self.catbar = ctk.CTkFrame(self, fg_color=theme.BG, height=60, corner_radius=0)
        self.catbar.place(relx=0, rely=0.065, relwidth=1)
        self.catbar.pack_propagate(False)

        categorias = ["Todas", "Eletrônicos", "Moda", "Supermercado", "Esportes", "Casa"]

        for cat in categorias:
            ctk.CTkButton(
                self.catbar,
                text=cat,
                width=120,
                fg_color=theme.ACCENT,
                hover_color=theme.PRIMARY,
                command=lambda c=cat: self._filtrar_categoria(c)
            ).pack(side="left", padx=10, pady=12)

    def _on_search_change(self):
        """Chamado quando o texto de busca muda."""
        self.filtro_texto = self.search_entry.get().lower()
        self.carregar_produtos()

    def _filtrar_categoria(self, categoria):
        """Filtra por categoria."""
        if categoria == "Todas":
            self.filtro_categoria = None
        else:
            self.filtro_categoria = categoria
        self.carregar_produtos()

    def carregar_produtos(self):
        """Carrega produtos na tela."""
        # Limpar
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Filtrar produtos
        produtos = loja.estoque.todos()

        if self.filtro_categoria:
            produtos = [p for p in produtos if p.categoria == self.filtro_categoria]

        if self.filtro_texto:
            produtos = [p for p in produtos if self.filtro_texto in p.nome.lower()]

        if not produtos:
            label = ctk.CTkLabel(
                self.scroll_frame,
                text="Nenhum produto encontrado",
                font=("Arial", 16),
                text_color="#aaa"
            )
            label.pack(pady=50)
            return

        # Grid de produtos (5 colunas)
        cols = 5
        for i, produto in enumerate(produtos):
            row = i // cols
            col = i % cols
            self._criar_card_produto(produto, row, col)

    def _criar_card_produto(self, produto, row, col):
        """Cria card de um produto."""
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=theme.BG,
            corner_radius=8,
            border_width=2,
            border_color=theme.PRIMARY_LIGHT
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Imagem do produto
        img_frame = ctk.CTkFrame(card, fg_color=theme.ACCENT, height=150, corner_radius=8)
        img_frame.pack(padx=8, pady=8, fill="x", expand=True)
        img_frame.pack_propagate(False)

        if produto.imagem and os.path.exists(produto.imagem):
            try:
                img = Image.open(produto.imagem).resize((160, 150), Image.Resampling.LANCZOS)
                img = ImageOps.fit(img, (160, 150), Image.Resampling.LANCZOS)
                ctk.CTkImage(img, size=(160, 150))
            except:
                pass

        img_label = ctk.CTkLabel(img_frame, text="Sem imagem", text_color="#aaa")
        img_label.pack()

        # Nome
        nome_label = ctk.CTkLabel(
            card,
            text=produto.nome[:20],
            font=("Arial", 11, "bold"),
            text_color="white"
        )
        nome_label.pack(padx=8, pady=(8, 4))

        # Categoria e preço
        info = ctk.CTkLabel(
            card,
            text=f"{produto.categoria} • R$ {produto.preco:.2f}",
            font=("Arial", 9),
            text_color="#aaa"
        )
        info.pack(padx=8, pady=2)

        # Estoque
        estoque_cor = "#4ade80" if produto.estoque > 0 else "#ff6b6b"
        estoque = ctk.CTkLabel(
            card,
            text=f"Estoque: {produto.estoque}",
            font=("Arial", 9),
            text_color=estoque_cor
        )
        estoque.pack(padx=8, pady=2)

        # Botões
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=8, pady=8)

        # Botão Adicionar
        ctk.CTkButton(
            btn_frame,
            text="Adicionar",
            width=70,
            height=28,
            font=("Arial", 9),
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=lambda p=produto: self._adicionar_ao_carrinho(p)
        ).pack(side="left", padx=2)

        # Botão Favorito com ícone dinâmico
        is_fav = self._is_favorito(produto.id)
        fav_icon = theme.load_icon('favoritosvermelho.png' if is_fav else 'favoritos.png', size=(20, 20))
        fav_cor = theme.PRIMARY if is_fav else theme.ALT_BG
        
        ctk.CTkButton(
            btn_frame,
            text="" if fav_icon else ("♡" if not is_fav else "❤️"),
            image=fav_icon,
            width=50,
            height=28,
            font=("Arial", 14),
            fg_color=fav_cor,
            hover_color=theme.PRIMARY_DARK,
            command=lambda p=produto: self._toggle_favorito(p)
        ).pack(side="left", padx=2)

    def _get_usuario_obj(self):
        """Obtém objeto do usuário logado."""
        uid = usuario_logado.get("id")
        if uid:
            return loja.buscar_usuario(uid)
        return None

    def _adicionar_ao_carrinho(self, produto):
        """Adiciona um produto ao carrinho."""
        if produto.estoque <= 0:
            messagebox.showwarning("Estoque", "Produto fora de estoque")
            return

        # Verifica se já existe no carrinho
        para_atualizar = None
        for item in loja.carrinho.itens:
            if item.produto.id == produto.id:
                para_atualizar = item
                break

        if para_atualizar:
            para_atualizar.quantidade += 1
            messagebox.showinfo("Carrinho", f"Quantidade atualizada!")
        else:
            loja.carrinho.adicionar(produto, 1)
            messagebox.showinfo("Carrinho", f"{produto.nome} adicionado!")

    def _is_favorito(self, produto_id):
        """Verifica se produto está nos favoritos."""
        uid = usuario_logado.get("id")
        if not uid:
            return False
        return loja.tem_favorito(uid, produto_id)

    def _toggle_favorito(self, produto):
        """Alterna favorito do produto."""
        uid = usuario_logado.get("id")
        if not uid:
            messagebox.showinfo("Login", "Faça login para favoritar")
            return

        if self._is_favorito(produto.id):
            loja.remover_favorito(uid, produto.id)
            messagebox.showinfo("Favoritos", f"Removido dos favoritos")
        else:
            loja.adicionar_favorito(uid, produto.id)
            messagebox.showinfo("Favoritos", f"Adicionado aos favoritos")

        self.carregar_produtos()

    def _abrir_carrinho(self):
        """Abre a tela do carrinho."""
        from views.carrinho import TelaCarrinho
        self.destroy()
        TelaCarrinho().mainloop()

    def _abrir_favoritos(self):
        """Abre a tela de favoritos."""
        from views.favoritos import TelaFavoritos
        self.destroy()
        TelaFavoritos().mainloop()

    def _abrir_perfil(self):
        """Abre a tela de perfil."""
        from views.perfil import TelaPerfil
        self.destroy()
        TelaPerfil().mainloop()

    def _abrir_meus_produtos(self):
        """Abre a tela de meus produtos (vendedor)."""
        from views.vendedor_produtos import TelaVendedorProdutos
        self.destroy()
        root = ctk.CTk()
        try:
            root.after(10, lambda: root.state("zoomed"))
        except Exception:
            pass
        TelaVendedorProdutos(root)
        root.mainloop()

    def _abrir_estatisticas(self):
        """Abre a tela de estatísticas (vendedor)."""
        from views.estatisticas import TelaEstatisticas
        self.destroy()
        root = ctk.CTk()
        try:
            root.after(10, lambda: root.state("zoomed"))
        except Exception:
            pass
        TelaEstatisticas(root)
        root.mainloop()

    def _abrir_relatorios(self):
        """Abre a tela de relatórios (vendedor)."""
        from views.relatorios import TelaRelatorios
        self.destroy()
        root = ctk.CTk()
        try:
            root.after(10, lambda: root.state("zoomed"))
        except Exception:
            pass
        TelaRelatorios(root)
        root.mainloop()

    def _fazer_logout(self):
        """Faz logout do usuário."""
        if messagebox.askyesno("Logout", "Deseja fazer logout?"):
            limpar_usuario_logado()
            from views.login import LoginCadastroScreen
            self.destroy()
            LoginCadastroScreen().mainloop()


if __name__ == "__main__":
    TelaHome().mainloop()
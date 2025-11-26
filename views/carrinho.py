"""
TELA DE CARRINHO
Permite adicionar, remover e alterar quantidades de produtos
"""

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from views.core import loja, usuario_logado
from views import theme


class TelaCarrinho(ctk.CTk):
    """Tela de gerenciamento do carrinho de compras."""
    
    def __init__(self, voltar_callback=None):
        super().__init__()

        self.title("NEXO - Carrinho")
        try:
            self.after(10, lambda: self.state("zoomed"))
        except Exception:
            pass
        
        self.voltar_callback = voltar_callback

        theme.apply_global()

        # Fundo
        bg = ctk.CTkFrame(self, fg_color=theme.BG)
        bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color=theme.CARD_BG, height=80, corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1)
        header.pack_propagate(False)

        # Título com ícone
        cart_icon = theme.load_icon('carrinho.png', size=(32, 32))
        if cart_icon:
            cart_label = ctk.CTkLabel(header, image=cart_icon, text="")
            cart_label.image = cart_icon
            cart_label.pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            header, text="Seu Carrinho",
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

        # Esquerda: Lista de itens
        left_frame = ctk.CTkFrame(main, fg_color="transparent")
        left_frame.place(relx=0.02, rely=0.02, relwidth=0.58, relheight=0.96)

        ctk.CTkLabel(
            left_frame,
            text="Produtos no carrinho",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=10, pady=(0, 15))

        # Scroll frame para itens
        self.scroll_frame = ctk.CTkScrollableFrame(
            left_frame,
            fg_color=theme.BG,
            corner_radius=8
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10)

        # Direita: Resumo
        right_frame = ctk.CTkFrame(main, fg_color="transparent")
        right_frame.place(relx=0.62, rely=0.02, relwidth=0.36, relheight=0.96)

        self._criar_resumo(right_frame)

        # Carrega itens do carrinho
        self._carregar_itens()

    def _criar_resumo(self, parent):
        """Cria a seção de resumo do pedido."""
        resumo = ctk.CTkFrame(parent, fg_color=theme.CARD_BG, corner_radius=12)
        resumo.pack(fill="both", expand=True, padx=10)

        ctk.CTkLabel(
            resumo,
            text="Resumo do Pedido",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(padx=20, pady=(20, 10), anchor="w")

        # Subtotal
        self.lbl_subtotal = ctk.CTkLabel(
            resumo,
            text="Subtotal: R$ 0.00",
            font=("Arial", 14),
            text_color="#A4B3C9"
        )
        self.lbl_subtotal.pack(padx=20, pady=5, anchor="w")

        # Frete
        self.lbl_frete = ctk.CTkLabel(
            resumo,
            text="Frete: R$ 0.00",
            font=("Arial", 14),
            text_color="#A4B3C9"
        )
        self.lbl_frete.pack(padx=20, pady=5, anchor="w")

        # Separador
        sep = ctk.CTkFrame(resumo, fg_color=theme.BG, height=1)
        sep.pack(fill="x", padx=20, pady=10)

        # Total
        self.lbl_total = ctk.CTkLabel(
            resumo,
            text="Total: R$ 0.00",
            font=("Arial", 18, "bold"),
            text_color="#00d084"
        )
        self.lbl_total.pack(padx=20, pady=10, anchor="w")

        # Botão finalizar
        ctk.CTkButton(
            resumo,
            text="✓ Finalizar Compra",
            height=50,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            font=("Arial", 14, "bold"),
            command=self._finalizar_compra
        ).pack(fill="x", padx=20, pady=20)

        # Botão limpar carrinho
        ctk.CTkButton(
            resumo,
            text="🗑️ Limpar Carrinho",
            height=40,
            fg_color=theme.ALT_BG,
            hover_color=theme.PRIMARY_DARK,
            command=self._limpar_carrinho
        ).pack(fill="x", padx=20, pady=(0, 20))

    def _carregar_itens(self):
        """Carrega os itens do carrinho."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        itens = loja.carrinho.itens

        if not itens:
            ctk.CTkLabel(
                self.scroll_frame,
                text="Carrinho vazio",
                text_color="#9AA6C0",
                font=("Arial", 14)
            ).pack(pady=40)
            self._atualizar_totais()
            return

        for idx, item in enumerate(itens):
            self._criar_linha_item(idx, item)

        self._atualizar_totais()

    def _criar_linha_item(self, idx, item):
        """Cria uma linha para um item do carrinho."""
        frame = ctk.CTkFrame(self.scroll_frame, fg_color=theme.CARD_BG, corner_radius=8)
        frame.pack(fill="x", pady=8, padx=0)

        # Nome e preço
        info_frame = ctk.CTkFrame(frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=12)

        ctk.CTkLabel(
            info_frame,
            text=item.produto.nome,
            font=("Arial", 14, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame,
            text=f"R$ {item.produto.preco:.2f} cada",
            font=("Arial", 12),
            text_color="#A4B3C9"
        ).pack(anchor="w")

        # Controles de quantidade
        ctrl_frame = ctk.CTkFrame(frame, fg_color="transparent")
        ctrl_frame.pack(side="right", padx=15, pady=12)

        ctk.CTkButton(
            ctrl_frame,
            text="-",
            width=30,
            fg_color=theme.ALT_BG,
            hover_color=theme.PRIMARY_DARK,
            command=lambda: self._alterar_quantidade(idx, -1)
        ).pack(side="left", padx=5)

        self.lbl_qty = ctk.CTkLabel(
            ctrl_frame,
            text=f"QTD: {item.quantidade}",
            font=("Arial", 12, "bold"),
            text_color="white",
            width=80
        )
        self.lbl_qty.pack(side="left", padx=5)

        ctk.CTkButton(
            ctrl_frame,
            text="+",
            width=30,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=lambda: self._alterar_quantidade(idx, 1)
        ).pack(side="left", padx=5)

        # Subtotal
        ctk.CTkLabel(
            ctrl_frame,
            text=f"R$ {item.subtotal():.2f}",
            font=("Arial", 12, "bold"),
            text_color="#00d084",
            width=80
        ).pack(side="left", padx=15)

        # Remover
        ctk.CTkButton(
            ctrl_frame,
            text="✕",
            width=30,
            fg_color=theme.ALT_BG,
            hover_color=theme.PRIMARY_DARK,
            command=lambda: self._remover_item(idx)
        ).pack(side="left", padx=5)

    def _alterar_quantidade(self, idx, delta):
        """Altera a quantidade de um item."""
        if 0 <= idx < len(loja.carrinho.itens):
            item = loja.carrinho.itens[idx]
            nova_qty = item.quantidade + delta

            if nova_qty <= 0:
                self._remover_item(idx)
            elif nova_qty <= item.produto.estoque:
                item.quantidade = nova_qty
                self._carregar_itens()
            else:
                messagebox.showwarning(
                    "Estoque",
                    f"Apenas {item.produto.estoque} unidades disponíveis"
                )

    def _remover_item(self, idx):
        """Remove um item do carrinho."""
        if 0 <= idx < len(loja.carrinho.itens):
            item_removido = loja.carrinho.itens.pop(idx)
            messagebox.showinfo("Removido", f"{item_removido.produto.nome} removido do carrinho")
            self._carregar_itens()

    def _atualizar_totais(self):
        """Atualiza os totais exibidos."""
        subtotal = loja.carrinho.total()
        frete = 0 if subtotal == 0 else 15.00
        total = subtotal + frete

        self.lbl_subtotal.configure(text=f"Subtotal: R$ {subtotal:.2f}")
        self.lbl_frete.configure(text=f"Frete: R$ {frete:.2f}")
        self.lbl_total.configure(text=f"Total: R$ {total:.2f}")

    def _limpar_carrinho(self):
        """Limpa todos os itens do carrinho."""
        if not loja.carrinho.itens:
            messagebox.showinfo("Carrinho", "Carrinho já está vazio")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente limpar o carrinho?"):
            loja.carrinho.limpar()
            self._carregar_itens()

    def _finalizar_compra(self):
        """Abre a tela de finalização da compra."""
        if not loja.carrinho.itens:
            messagebox.showwarning("Carrinho Vazio", "Adicione produtos ao carrinho antes de finalizar")
            return

        from views.finalizar_venda import TelaFinalizarVenda
        self.destroy()
        TelaFinalizarVenda().mainloop()

    def _voltar(self):
        """Volta para a tela anterior."""
        self.destroy()
        if self.voltar_callback:
            self.voltar_callback()
        else:
            from views.home import TelaHome
            TelaHome().mainloop()

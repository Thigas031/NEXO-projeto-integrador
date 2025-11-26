"""
TELA DE FINALIZAÇÃO DA VENDA
Coleta dados do cliente e registra o pedido
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from views.core import loja, usuario_logado
from views import theme


class TelaFinalizarVenda(ctk.CTk):
    """Tela para finalizar a compra com dados do cliente."""
    
    def __init__(self):
        super().__init__()

        self.title("NEXO - Finalizar Compra")
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

        ctk.CTkLabel(
            header, text="Finalizar Compra",
            font=("Arial", 28, "bold"),
            text_color="white"
        ).pack(side="left", padx=30, pady=20)

        # Botão cancelar
        ctk.CTkButton(
            header,
            text="← Cancelar",
            width=100,
            fg_color=theme.ALT_BG,
            hover_color=theme.PRIMARY_DARK,
            command=self._cancelar
        ).pack(side="right", padx=30, pady=20)

        # Frame principal
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)

        # Esquerda: Formulário
        left_frame = ctk.CTkFrame(main, fg_color="transparent")
        left_frame.place(relx=0.05, rely=0.02, relwidth=0.55, relheight=0.96)

        self._criar_formulario(left_frame)

        # Direita: Resumo
        right_frame = ctk.CTkFrame(main, fg_color="transparent")
        right_frame.place(relx=0.62, rely=0.02, relwidth=0.33, relheight=0.96)

        self._criar_resumo(right_frame)

    def _criar_formulario(self, parent):
        """Cria o formulário de dados do cliente."""
        form_title = ctk.CTkLabel(
            parent,
            text="Dados Pessoais",
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        form_title.pack(anchor="w", padx=0, pady=(0, 20))

        # Nome
        ctk.CTkLabel(parent, text="Nome Completo", text_color="white").pack(anchor="w", pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(parent, placeholder_text="Seu nome completo")
        self.entry_nome.pack(anchor="w", pady=(5, 15), fill="x", expand=True)

        # CPF
        ctk.CTkLabel(parent, text="CPF", text_color="white").pack(anchor="w", pady=(10, 0))
        self.entry_cpf = ctk.CTkEntry(parent, placeholder_text="000.000.000-00")
        self.entry_cpf.pack(anchor="w", pady=(5, 15), fill="x", expand=True)

        # Endereço
        ctk.CTkLabel(parent, text="Endereço Completo", text_color="white").pack(anchor="w", pady=(10, 0))
        self.entry_endereco = ctk.CTkEntry(parent, placeholder_text="Rua, número, bairro, cidade, CEP")
        self.entry_endereco.pack(anchor="w", pady=(5, 15), fill="x", expand=True)

        # Pagamento
        ctk.CTkLabel(
            parent,
            text="Forma de Pagamento",
            font=("Arial", 14, "bold"),
            text_color="white"
        ).pack(anchor="w", pady=(20, 10))

        self.var_pagamento = ctk.StringVar(value="debito")

        ctk.CTkRadioButton(
            parent,
            text="💳 Débito",
            variable=self.var_pagamento,
            value="debito",
            text_color="white"
        ).pack(anchor="w", pady=5)

        ctk.CTkRadioButton(
            parent,
            text="💳 Crédito",
            variable=self.var_pagamento,
            value="credito",
            text_color="white"
        ).pack(anchor="w", pady=5)

        ctk.CTkRadioButton(
            parent,
            text="💸 Dinheiro",
            variable=self.var_pagamento,
            value="dinheiro",
            text_color="white"
        ).pack(anchor="w", pady=5)

        ctk.CTkRadioButton(
            parent,
            text="📱 Pix",
            variable=self.var_pagamento,
            value="pix",
            text_color="white"
        ).pack(anchor="w", pady=5)

    def _criar_resumo(self, parent):
        """Cria a seção de resumo do pedido."""
        resumo = ctk.CTkFrame(parent, fg_color=theme.CARD_BG, corner_radius=12)
        resumo.pack(fill="both", expand=True)

        ctk.CTkLabel(
            resumo,
            text="Resumo Final",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(padx=20, pady=(20, 10), anchor="w")

        # Itens
        scroll = ctk.CTkScrollableFrame(resumo, fg_color=theme.BG, corner_radius=8)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for item in loja.carrinho.itens:
            linha = ctk.CTkFrame(scroll, fg_color="transparent")
            linha.pack(fill="x", pady=5)

            ctk.CTkLabel(
                linha,
                text=f"{item.quantidade}x {item.produto.nome}",
                text_color="white",
                font=("Arial", 11)
            ).pack(side="left", anchor="w")

            ctk.CTkLabel(
                linha,
                text=f"R$ {item.subtotal():.2f}",
                text_color="#00d084",
                font=("Arial", 11, "bold")
            ).pack(side="right", anchor="e")

        # Separador
        sep = ctk.CTkFrame(resumo, fg_color=theme.BG, height=1)
        sep.pack(fill="x", padx=20, pady=10)

        # Total
        subtotal = loja.carrinho.total()
        frete = 0 if subtotal == 0 else 15.00
        total = subtotal + frete

        self.lbl_total = ctk.CTkLabel(
            resumo,
            text=f"Total: R$ {total:.2f}",
            font=("Arial", 16, "bold"),
            text_color="#00d084"
        )
        self.lbl_total.pack(padx=20, pady=10, anchor="w")

        # Botão finalizar
        ctk.CTkButton(
            resumo,
            text="✓ Confirmar Pedido",
            height=50,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            font=("Arial", 14, "bold"),
            command=self._confirmar_pedido
        ).pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkButton(
            resumo,
            text="← Voltar",
            height=40,
            fg_color=theme.ALT_BG,
            hover_color=theme.PRIMARY_DARK,
            command=self._voltar
        ).pack(fill="x", padx=20, pady=(0, 20))

    def _validar_dados(self):
        """Valida os dados preenchidos."""
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not nome:
            messagebox.showwarning("Validação", "Preencha o nome completo")
            return False

        if not cpf or len(cpf) < 11:
            messagebox.showwarning("Validação", "Preencha um CPF válido")
            return False

        if not endereco:
            messagebox.showwarning("Validação", "Preencha o endereço")
            return False

        return True

    def _confirmar_pedido(self):
        """Confirma e registra o pedido."""
        if not self._validar_dados():
            return

        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        endereco = self.entry_endereco.get().strip()
        pagamento = self.var_pagamento.get()

        # Cria cliente
        cliente = loja.cadastrar_cliente(nome, cpf)

        # Processa pagamento
        total = loja.carrinho.total() + (0 if loja.carrinho.total() == 0 else 15.00)
        if not loja.pag.processar(total):
            messagebox.showerror("Pagamento", "Erro ao processar pagamento")
            return

        # Registra pedido
        from models.pedido import Pedido
        pedido = Pedido(loja.next_pedido_id, loja.carrinho.itens.copy(), cliente)
        pedido.endereco = endereco
        pedido.pagamento = pagamento

        # Baixa estoque
        for item in loja.carrinho.itens:
            item.produto.baixar_estoque(item.quantidade)

        loja.pedidos.append(pedido)
        loja.next_pedido_id += 1
        loja.carrinho.limpar()

        messagebox.showinfo(
            "Sucesso",
            f"✓ Pedido #{pedido.id} registrado com sucesso!\nTotal: R$ {total:.2f}"
        )

        self._voltar_home()

    def _cancelar(self):
        """Cancela e volta ao carrinho."""
        if messagebox.askyesno("Cancelar", "Deseja voltar ao carrinho?"):
            self._voltar()

    def _voltar(self):
        """Volta para o carrinho."""
        from views.carrinho import TelaCarrinho
        self.destroy()
        TelaCarrinho().mainloop()

    def _voltar_home(self):
        """Volta para a home."""
        from views.home import TelaHome
        self.destroy()
        TelaHome().mainloop()

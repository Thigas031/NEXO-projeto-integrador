"""
TELA DE PERFIL DO USUÁRIO
Exibe informações do usuário logado, edição e favoritos
"""

import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

from views.core import loja, usuario_logado
from views import theme


class TelaPerfil(ctk.CTk):
    """Tela de perfil do usuário logado."""
    
    def __init__(self):
        super().__init__()

        self.title("NEXO - Perfil")
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
            header, text="Meu Perfil",
            font=("Arial", 28, "bold"),
            text_color="white"
        ).pack(side="left", padx=30, pady=20)

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
        main.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.92)

        # Obter usuário
        self.usuario = loja.buscar_usuario(usuario_logado.get("id"))

        if not self.usuario:
            ctk.CTkLabel(
                main,
                text="Usuário não encontrado",
                text_color="white",
                font=("Arial", 16)
            ).pack(pady=40)
            return

        # Seção de info do usuário
        info_frame = ctk.CTkFrame(main, fg_color=theme.CARD_BG, corner_radius=12)
        info_frame.pack(fill="x", padx=0, pady=(0, 20))

        # Avatar
        avatar = self._criar_avatar()
        avatar_label = ctk.CTkLabel(info_frame, image=avatar, text="")
        avatar_label.image = avatar
        avatar_label.pack(side="left", padx=20, pady=20)

        # Info
        info_text = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_text.pack(side="left", fill="both", expand=True, pady=20)

        nome = self.usuario.nome
        ctk.CTkLabel(
            info_text,
            text=nome,
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_text,
            text=f"@{nome.lower().replace(' ', '_')}",
            font=("Arial", 14),
            text_color="#9AA6C0"
        ).pack(anchor="w", pady=(5, 0))

        papel = "Vendedor" if self.usuario.papel == "vendedor" else "Cliente"
        ctk.CTkLabel(
            info_text,
            text=f"{papel} | {self.usuario.email}",
            font=("Arial", 12),
            text_color="#B7C4DB"
        ).pack(anchor="w", pady=(10, 0))

        # Botões de ação
        btn_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=20)

        ctk.CTkButton(
            btn_frame,
            text="✏️ Editar",
            width=100,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=self._editar_perfil
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="❤️ Favoritos",
            width=120,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=self._ver_favoritos
        ).pack(side="left", padx=10)

        # Seção de dados detalhados
        if self.usuario.papel == "vendedor":
            self._criar_secao_vendedor(main)

        # Seção de favoritos
        ctk.CTkLabel(
            main,
            text="❤️ Seus Favoritos",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=0, pady=(20, 10))

        self.favoritos_box = ctk.CTkScrollableFrame(
            main,
            fg_color=theme.BG,
            corner_radius=8,
            height=200
        )
        self.favoritos_box.pack(fill="x", padx=0, pady=(0, 20))

        self._carregar_favoritos()

    def _criar_secao_vendedor(self, parent):
        """Cria seção adicional para vendedor."""
        vendedor_frame = ctk.CTkFrame(parent, fg_color=theme.CARD_BG, corner_radius=12)
        vendedor_frame.pack(fill="x", padx=0, pady=(20, 0))

        ctk.CTkLabel(
            vendedor_frame,
            text="📦 Informações da Loja",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        info_text = f"""
CPF: {self.usuario.cpf}
Nome da Loja: {self.usuario.nome_loja or 'Não informado'}
        """

        ctk.CTkLabel(
            vendedor_frame,
            text=info_text.strip(),
            font=("Arial", 11),
            text_color="#A4B3C9",
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))

    def _carregar_favoritos(self):
        """Carrega lista de favoritos."""
        for widget in self.favoritos_box.winfo_children():
            widget.destroy()

        favoritos_ids = self.usuario.favoritos.listar()
        produtos_fav = []

        for pid in favoritos_ids:
            p = loja.buscar_produto(pid)
            if p:
                produtos_fav.append(p)

        if not produtos_fav:
            ctk.CTkLabel(
                self.favoritos_box,
                text="Nenhum produto nos favoritos",
                text_color="#9AA6C0",
                font=("Arial", 12)
            ).pack(pady=20)
            return

        for p in produtos_fav:
            linha = ctk.CTkFrame(self.favoritos_box, fg_color="#1a2332", corner_radius=8)
            linha.pack(fill="x", pady=6, padx=10)

            # Nome e preço
            info = ctk.CTkFrame(linha, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=15, pady=12)

            ctk.CTkLabel(
                info,
                text=p.nome,
                font=("Arial", 12, "bold"),
                text_color="white"
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=f"{p.categoria} | R$ {p.preco:.2f}",
                font=("Arial", 11),
                text_color="#A4B3C9"
            ).pack(anchor="w", pady=(3, 0))

            # Botões
            btn = ctk.CTkFrame(linha, fg_color="transparent")
            btn.pack(side="right", padx=15, pady=12)

            ctk.CTkButton(
                btn,
                text="➕",
                width=40,
                font=("Arial", 10),
                fg_color=theme.PRIMARY,
                hover_color=theme.PRIMARY_DARK,
                command=lambda prod=p: self._adicionar_ao_carrinho(prod)
            ).pack(side="left", padx=5)

    def _criar_avatar(self, size=100):
        """Cria um avatar circular padrão."""
        nome = self.usuario.nome
        cores = [
            (52, 152, 219),
            (46, 204, 113),
            (155, 89, 182),
        ]
        cor = cores[hash(nome) % len(cores)]

        img = Image.new("RGB", (size, size), cor)
        return ctk.CTkImage(img, size=(size, size))

    def _editar_perfil(self):
        """Abre diálogo para editar perfil."""
        # Criar janela de edição
        edit_win = ctk.CTkToplevel(self)
        edit_win.title("Editar Perfil")
        try:
            edit_win.after(10, lambda: edit_win.state("zoomed"))
        except Exception:
            pass
        edit_win.transient(self)
        edit_win.grab_set()

        # Campos
        ctk.CTkLabel(edit_win, text="Nome", text_color="white").pack(padx=20, pady=(20, 5), anchor="w")
        entry_nome = ctk.CTkEntry(edit_win)
        entry_nome.insert(0, self.usuario.nome)
        entry_nome.pack(padx=20, pady=(0, 15), anchor="w", fill="x", expand=True)

        ctk.CTkLabel(edit_win, text="Email", text_color="white").pack(padx=20, pady=(10, 5), anchor="w")
        entry_email = ctk.CTkEntry(edit_win)
        entry_email.insert(0, self.usuario.email)
        entry_email.pack(padx=20, pady=(0, 15), anchor="w", fill="x", expand=True)

        ctk.CTkLabel(edit_win, text="Telefone", text_color="white").pack(padx=20, pady=(10, 5), anchor="w")
        entry_tel = ctk.CTkEntry(edit_win)
        entry_tel.insert(0, self.usuario.telefone)
        entry_tel.pack(padx=20, pady=(0, 15), anchor="w", fill="x", expand=True)

        ctk.CTkLabel(edit_win, text="Endereço", text_color="white").pack(padx=20, pady=(10, 5), anchor="w")
        entry_end = ctk.CTkEntry(edit_win)
        entry_end.insert(0, self.usuario.endereco)
        entry_end.pack(padx=20, pady=(0, 20), anchor="w", fill="x", expand=True)

        def salvar():
            loja.editar_perfil(
                self.usuario.id,
                entry_nome.get(),
                entry_email.get(),
                entry_tel.get(),
                entry_end.get()
            )
            messagebox.showinfo("Sucesso", "Perfil atualizado!")
            edit_win.destroy()
            # Recarregar a página
            self.destroy()
            TelaPerfil().mainloop()

        ctk.CTkButton(edit_win, text="Salvar", command=salvar, fg_color=theme.PRIMARY).pack(pady=20)

    def _adicionar_ao_carrinho(self, produto):
        """Adiciona produto ao carrinho."""
        if produto.estoque <= 0:
            messagebox.showwarning("Estoque", "Produto fora de estoque")
            return

        for item in loja.carrinho.itens:
            if item.produto.id == produto.id:
                item.quantidade += 1
                messagebox.showinfo("Carrinho", "Quantidade atualizada!")
                return

        loja.carrinho.adicionar(produto, 1)
        messagebox.showinfo("Carrinho", f"{produto.nome} adicionado!")

    def _ver_favoritos(self):
        """Abre a tela de favoritos."""
        from views.favoritos import TelaFavoritos
        self.destroy()
        TelaFavoritos().mainloop()

    def _voltar(self):
        """Volta para a home."""
        from views.home import TelaHome
        self.destroy()
        TelaHome().mainloop()

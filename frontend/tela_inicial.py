import customtkinter as ctk

class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, master, app, backend, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.backend = backend

        header = ctk.CTkLabel(self, text="Painel NEXO", font=ctk.CTkFont(size=22, weight="bold"))
        header.pack(pady=12)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(top, text="Bem-vindo(a)!").pack(side="left")
        ctk.CTkButton(top, text="Meu Perfil", command=lambda: app.mostrar_tela("perfil")).pack(side="right", padx=6)

        # Lista produtos
        self.lista_frame = ctk.CTkScrollableFrame(self, height=420)
        self.lista_frame.pack(fill="both", expand=True, padx=20, pady=8)

        # botão criar produto (apenas para vendedores/admin)
        ctk.CTkButton(self, text="Adicionar Produto (vendedor)", command=self.abrir_criar_produto).pack(pady=6)

        # carregar produtos
        self.atualizar()

    def atualizar(self):
        # limpar
        for w in self.lista_frame.winfo_children():
            w.destroy()
        produtos = self.backend.listar_produtos()
        if not produtos:
            ctk.CTkLabel(self.lista_frame, text="Nenhum produto cadastrado.").pack(pady=8)
            return
        for p in produtos:
            card = ctk.CTkFrame(self.lista_frame, height=90, corner_radius=6)
            card.pack(fill="x", padx=8, pady=6)
            txt = f"{p['nome']} — R$ {p['preco']:.2f} — Vendedor: {p.get('vendedor_nome','?')}"
            ctk.CTkLabel(card, text=txt).pack(side="left", padx=8)
            ctk.CTkButton(card, text="Ver", width=80, command=lambda pid=p['id']: self.app.mostrar_tela("produto", pid)).pack(side="right", padx=8)

    def abrir_criar_produto(self):
        # abre uma pequena janela para criar produto
        from tkinter import Toplevel
        win = Toplevel(self)
        win.title("Criar Produto")
        frm = ctk.CTkFrame(win)
        frm.pack(padx=12, pady=12)
        nome = ctk.CTkEntry(frm, placeholder_text="Nome do produto", width=380); nome.pack(pady=6)
        descricao = ctk.CTkEntry(frm, placeholder_text="Descrição", width=380); descricao.pack(pady=6)
        preco = ctk.CTkEntry(frm, placeholder_text="Preço (ex: 49.90)", width=200); preco.pack(pady=6)
        estoque = ctk.CTkEntry(frm, placeholder_text="Estoque (ex: 10)", width=200); estoque.pack(pady=6)
        msg = ctk.CTkLabel(frm, text="")

        def criar():
            user = self.app.usuario_logado
            if not user:
                msg.configure(text="Faça login")
                return
            if user['tipo'] not in ('vendedor','admin'):
                msg.configure(text="Apenas vendedores/admin podem criar produtos")
                return
            try:
                p = float(preco.get())
                e = int(estoque.get())
            except:
                msg.configure(text="Preço/estoque inválidos")
                return
            pid = self.backend.adicionar_produto(user['id'], nome.get(), descricao.get(), p, e)
            if pid:
                msg.configure(text="Produto criado com sucesso")
                self.atualizar()
            else:
                msg.configure(text="Erro ao criar produto")
        ctk.CTkButton(frm, text="Criar", command=criar).pack(pady=8)
        msg.pack()
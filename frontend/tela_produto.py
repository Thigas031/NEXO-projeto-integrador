import database_config  # integração futura com o banco de dados
import customtkinter as ctk

class TelaProduto(ctk.CTkFrame):
    def __init__(self, master, app, backend, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.backend = backend
        self.produto_atual = None

        self.header = ctk.CTkLabel(self, text="Detalhes do Produto", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(pady=12)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=12, pady=6)

        self.titulo = ctk.CTkLabel(self.container, text="Nome", font=ctk.CTkFont(size=18, weight="bold"))
        self.titulo.pack(anchor="w", pady=(6,0))
        self.preco = ctk.CTkLabel(self.container, text="R$ 0,00", font=ctk.CTkFont(size=16))
        self.preco.pack(anchor="w", pady=(2,12))

        self.descricao = ctk.CTkLabel(self.container, text="Descrição", wraplength=900, anchor="w", justify="left")
        self.descricao.pack(fill="x", pady=(0,12))

        btns = ctk.CTkFrame(self)
        btns.pack(pady=8)
        ctk.CTkButton(btns, text="Favoritar", command=self.favoritar).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Adicionar ao carrinho", command=self.adicionar_carrinho).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Editar (se permitido)", command=self.editar_produto).pack(side="left", padx=6)

    def abrir(self, produto_id):
        p = self.backend.obter_produto(produto_id)
        if not p:
            self.titulo.configure(text="Produto não encontrado")
            return
        self.produto_atual = p
        self.titulo.configure(text=p['nome'])
        self.preco.configure(text=f"R$ {float(p['preco']):.2f}")
        self.descricao.configure(text=p.get('descricao') or "Sem descrição")
        # mostrar informações do vendedor
        vendedor = f"Vendedor: {p.get('vendedor_nome')} ({p.get('vendedor_email')})"
        self.descricao.configure(text=(self.descricao.cget("text") + "\n\n" + vendedor))

    def favoritar(self):
        user = self.app.usuario_logado
        if not user:
            return
        self.backend.adicionar_favorito(user['id'], self.produto_atual['id'])

    def adicionar_carrinho(self):
        user = self.app.usuario_logado
        if not user:
            return
        self.backend.adicionar_ao_carrinho(user['id'], self.produto_atual['id'], quantidade=1)

    def editar_produto(self):
        user = self.app.usuario_logado
        if not user:
            return
        # abre diálogo simples para editar se for dono ou admin
        allowed = (user['tipo']=='admin') or (user['id'] == self.produto_atual['id_usuario'])
        if not allowed and user['tipo']!='admin':
            from tkinter import messagebox
            messagebox.showinfo("Sem permissão", "Apenas o dono do produto ou admin pode editar.")
            return
        from tkinter import Toplevel
        win = Toplevel(self)
        win.title("Editar produto")
        frm = ctk.CTkFrame(win); frm.pack(padx=10, pady=10)
        nome = ctk.CTkEntry(frm, placeholder_text="Nome", width=360); nome.insert(0, self.produto_atual['nome']); nome.pack(pady=6)
        descricao = ctk.CTkEntry(frm, placeholder_text="Descrição", width=360); descricao.insert(0, self.produto_atual.get('descricao') or ''); descricao.pack(pady=6)
        preco = ctk.CTkEntry(frm, placeholder_text="Preço", width=200); preco.insert(0, str(self.produto_atual['preco'])); preco.pack(pady=6)
        estoque = ctk.CTkEntry(frm, placeholder_text="Estoque", width=200); estoque.insert(0, str(self.produto_atual['estoque'])); estoque.pack(pady=6)

        def salvar():
    # TODO: Implementar integração com banco de dados usando database_config.conectar()
            try:
                pval = float(preco.get())
                est = int(estoque.get())
            except:
                return
            # if admin, force edit
            force = (user['tipo']=='admin')
            ok = self.backend.editar_produto(self.produto_atual['id'], user['id'], nome=nome.get(), descricao=descricao.get(), preco=pval, estoque=est, forcar=force)
            if ok:
                win.destroy()
                self.abrir(self.produto_atual['id'])
        ctk.CTkButton(frm, text="Salvar", command=salvar).pack(pady=8)
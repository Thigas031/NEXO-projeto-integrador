import customtkinter as ctk

class TelaPerfil(ctk.CTkFrame):
    def __init__(self, master, app, backend, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.backend = backend

        self.header = ctk.CTkLabel(self, text="Perfil", font=ctk.CTkFont(size=22, weight="bold"))
        self.header.pack(pady=12)

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(padx=16, pady=6, fill="x")

        self.lbl_nome = ctk.CTkLabel(self.info_frame, text="Nome: --", anchor="w")
        self.lbl_nome.pack(fill="x", pady=4)
        self.lbl_email = ctk.CTkLabel(self.info_frame, text="E-mail: --", anchor="w")
        self.lbl_email.pack(fill="x", pady=4)
        self.lbl_tipo = ctk.CTkLabel(self.info_frame, text="Tipo: --", anchor="w")
        self.lbl_tipo.pack(fill="x", pady=4)

        ctk.CTkButton(self, text="Editar Perfil", command=lambda: self.app.mostrar_tela("editarperfil")).pack(pady=8)
        ctk.CTkButton(self, text="Ver meus produtos", command=self.ver_meus_produtos).pack(pady=6)

    def atualizar(self):
        # atualiza com base no usuário logado (se houver)
        u = self.app.usuario_logado
        if not u:
            self.lbl_nome.configure(text="Nome: --")
            self.lbl_email.configure(text="E-mail: --")
            self.lbl_tipo.configure(text="Tipo: --")
            return
        user = self.backend.obter_usuario_por_id(u['id'])
        self.lbl_nome.configure(text=f"Nome: {user['nome']}")
        self.lbl_email.configure(text=f"E-mail: {user['email']}")
        self.lbl_tipo.configure(text=f"Tipo: {user['tipo']}")

    def ver_meus_produtos(self):
        u = self.app.usuario_logado
        if not u:
            return
        produtos = self.backend.listar_produtos(apenas_do_usuario_id=u['id'])
        from tkinter import Toplevel
        win = Toplevel(self)
        win.title("Meus Produtos")
        frm = ctk.CTkFrame(win); frm.pack(fill="both", padx=10, pady=10)
        if not produtos:
            ctk.CTkLabel(frm, text="Você não possui produtos").pack()
            return
        for p in produtos:
            card = ctk.CTkFrame(frm); card.pack(fill="x", pady=6)
            ctk.CTkLabel(card, text=f"{p['nome']} — R$ {p['preco']:.2f}").pack(side="left", padx=8)
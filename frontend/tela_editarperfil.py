import database_config  # integração futura com o banco de dados
import customtkinter as ctk

class TelaEditarPerfil(ctk.CTkFrame):
    def __init__(self, master, app, backend, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.backend = backend

        ctk.CTkLabel(self, text="Editar Perfil", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12)
        frm = ctk.CTkFrame(self); frm.pack(padx=10, pady=6)

        self.nome = ctk.CTkEntry(frm, placeholder_text="Nome", width=420); self.nome.pack(pady=6)
        self.telefone = ctk.CTkEntry(frm, placeholder_text="Telefone", width=420); self.telefone.pack(pady=6)

        ctk.CTkButton(frm, text="Salvar", command=self.salvar).pack(pady=8)

    def atualizar(self):
    # TODO: Implementar integração com banco de dados usando database_config.conectar()
        u = self.app.usuario_logado
        if not u: return
        dados = self.backend.obter_usuario_por_id(u['id'])
        self.nome.delete(0, 'end'); self.nome.insert(0, dados['nome'])
        self.telefone.delete(0, 'end'); self.telefone.insert(0, dados.get('telefone') or '')

    def salvar(self):
    # TODO: Implementar integração com banco de dados usando database_config.conectar()
        # Para simplificar, implementamos apenas atualização simples via SQL direto
        u = self.app.usuario_logado
        if not u: return
        cursor = self.backend.conn.cursor()
        cursor.execute("UPDATE usuarios SET nome=%s, telefone=%s WHERE id=%s", (self.nome.get(), self.telefone.get(), u['id']))
        self.backend.conn.commit()
        cursor.close()
        # atualizar app
        self.app.usuario_logado = self.backend.obter_usuario_por_id(u['id'])
        self.app.mostrar_tela("perfil")
import database_config  # integração futura com o banco de dados
import customtkinter as ctk

class TelaRelatorio(ctk.CTkFrame):
    def __init__(self, master, app, backend, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.backend = backend

        ctk.CTkLabel(self, text="Relatórios", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12)
        self.frame = ctk.CTkFrame(self); self.frame.pack(fill="both", expand=True, padx=12, pady=8)
        self.kpi_label = ctk.CTkLabel(self.frame, text="")
        self.kpi_label.pack(pady=8)

    def atualizar(self):
    # TODO: Implementar integração com banco de dados usando database_config.conectar()
        u = self.app.usuario_logado
        if not u:
            self.kpi_label.configure(text="Faça login para ver relatórios.")
            return
        if u['tipo'] not in ('vendedor','admin'):
            self.kpi_label.configure(text="Relatórios disponíveis apenas para vendedores/admin.")
            return
        data = self.backend.relatorio_vendedor(u['id'])
        texto = f"Produtos: {data['num_produtos']}  |  Vendas: {data['num_vendas']}  |  Receita: R$ {data['soma_total']:.2f}"
        self.kpi_label.configure(text=texto)
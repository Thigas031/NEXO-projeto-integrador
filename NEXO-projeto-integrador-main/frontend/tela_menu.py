import database_config  # integração futura com o banco de dados
import customtkinter as ctk

class TelaMenu(ctk.CTkFrame):
    def __init__(self, master, app, backend, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.backend = backend

        ctk.CTkLabel(self, text="Menu", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=12)
        btns = [
            ("Início", "principal"),
            ("Perfil", "perfil"),
            ("Relatórios", "relatorio"),
            ("Sair", "logout")
        ]
        for text, key in btns:
            ctk.CTkButton(self, text=text, width=180, command=lambda k=key: self._action(k)).pack(pady=6)

    def _action(self, key):
        if key == "logout":
            self.app.usuario_logado = None
            self.app.mostrar_tela("login")
            return
        self.app.mostrar_tela(key)
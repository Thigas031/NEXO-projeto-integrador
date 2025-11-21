from backend.loja import Loja

loja = Loja()
usuario_logado = {"id": None, "nome": None}

# ⚠ Usuário de teste automático
loja.cadastrar_usuario("admin", "123")
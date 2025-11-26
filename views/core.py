"""
CORE - Módulo de configuração global
Define a loja e o usuário logado que são acessíveis em todas as telas
"""

from models.loja import Loja

# Instância única da loja (GLOBAL)
loja = Loja()

# Usuário logado como dicionário
usuario_logado = {"id": None, "nome": None}


def atualizar_usuario_logado(usuario_id, usuario_nome):
    """Atualiza o estado do usuário logado globalmente."""
    global usuario_logado
    usuario_logado["id"] = usuario_id
    usuario_logado["nome"] = usuario_nome


def limpar_usuario_logado():
    """Limpa o estado do usuário logado (logout)."""
    global usuario_logado
    usuario_logado["id"] = None
    usuario_logado["nome"] = None


def get_usuario_obj():
    """Retorna o objeto do usuário logado."""
    if usuario_logado.get("id"):
        return loja.buscar_usuario(usuario_logado["id"])
    return None


# ================================
# PRODUTOS DE TESTE
# ================================
def _criar_produtos_teste():
    """Cria produtos de teste automaticamente."""
    produtos_teste = [
        ("Notebook Dell", "Eletrônicos", 2500.00, 5),
        ("Mouse Logitech", "Eletrônicos", 150.00, 20),
        ("Teclado Mecânico", "Eletrônicos", 450.00, 8),
        ("Monitor LG 24\"", "Eletrônicos", 800.00, 3),
        ("Webcam HD", "Eletrônicos", 300.00, 15),
        ("Camiseta Básica", "Moda", 45.00, 50),
        ("Calça Jeans", "Moda", 120.00, 30),
        ("Tênis Esportivo", "Moda", 250.00, 20),
        ("Jaqueta de Inverno", "Moda", 350.00, 10),
        ("Queijo Parmesão", "Supermercado", 85.00, 25),
        ("Leite Integral", "Supermercado", 6.50, 100),
        ("Pão Integral", "Supermercado", 12.00, 50),
        ("Frutas Variadas", "Supermercado", 35.00, 40),
        ("Bola de Futebol", "Esportes", 120.00, 15),
        ("Bicicleta Mountain", "Esportes", 1200.00, 5),
        ("Roupão de Banho", "Casa", 89.00, 20),
        ("Jogo de Cama", "Casa", 200.00, 15),
        ("Cortinas Blackout", "Casa", 180.00, 10),
    ]
    
    for nome, categoria, preco, estoque in produtos_teste:
        loja.cadastrar_produto(nome, categoria, preco, estoque)

# Criar produtos ao inicializar
_criar_produtos_teste()

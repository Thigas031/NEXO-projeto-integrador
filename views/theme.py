import customtkinter as ctk
from PIL import Image
import os

# Paleta roxa moderna e suave
PRIMARY = "#8b5cf6"       # roxo médio principal
PRIMARY_LIGHT = "#a78bfa" # roxo claro para detalhes
PRIMARY_DARK = "#6d28d9"  # roxo escuro para hover
ACCENT = "#7c3aed"        # roxo auxiliar

# Backgrounds (manter base escura)
BG = "#0a0e27"             # fundo principal (dark)
CARD_BG = "#152033"        # fundo de cartões / frames centrais
ALT_BG = "#1b1f3b"         # alternativa para listas/linhas

# Caminho base para imagens
IMG_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'img')

def apply_global():
    try:
        ctk.set_appearance_mode("dark")
    except Exception:
        pass

def load_icon(filename, size=(40, 40)):
    """Carrega ícone da pasta img com tratamento de erro."""
    try:
        path = os.path.join(IMG_BASE, filename)
        if os.path.exists(path):
            img = Image.open(path)
            return ctk.CTkImage(img, size=size)
    except Exception as e:
        print(f"Erro ao carregar {filename}: {e}")
    return None

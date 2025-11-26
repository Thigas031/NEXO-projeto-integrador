"""
Helpers de UI para a tela de Perfil.
Tudo que for repetitivo ou volumoso da `views/perfil.py` foi movido para cá.
"""
import customtkinter as ctk
from PIL import Image, ImageOps
import os


def criar_avatar_widget(parent, pil_image, size=120, relx=0.04, rely=0.12):
    """
    Cria um widget de avatar (CTkLabel com CTkImage) e o posiciona dentro do `parent`.
    Retorna o label criado.
    """
    try:
        tkimg = ctk.CTkImage(pil_image, size=(size, size))
    except Exception:
        # fallback: cria imagem lisa
        img = Image.new("RGB", (size, size), (150, 150, 200))
        tkimg = ctk.CTkImage(img, size=(size, size))

    lbl = ctk.CTkLabel(parent, image=tkimg, text="")
    lbl.image = tkimg
    lbl.place(relx=relx, rely=rely, anchor="nw", width=size, height=size)
    return lbl


def popular_produtos_scroll(scroll_frame, produtos):
    """
    Popula o `scroll_frame` com a lista de produtos fornecida.
    Substitui o código repetitivo nas views.
    """
    for w in scroll_frame.winfo_children():
        try:
            w.destroy()
        except Exception:
            pass

    if not produtos:
        ctk.CTkLabel(scroll_frame, text="Nenhum produto", text_color="white").pack(pady=20)
        return

    for p in produtos:
        f = ctk.CTkFrame(scroll_frame, fg_color="#203149", corner_radius=8)
        f.pack(fill="x", pady=8, padx=6)
        ctk.CTkLabel(f, text=f"{p.nome} — R$ {p.preco:.2f}", text_color="white").pack(side="left", padx=12, pady=12)


def carregar_imagem_produto(produto, w, h):
    """
    Helper simples para carregar a imagem do produto (PIL -> CTkImage).
    Retorna `ctk.CTkImage` pronto para usar.
    """
    if getattr(produto, "imagem", None) and os.path.exists(produto.imagem):
        try:
            img = Image.open(produto.imagem).convert("RGB")
            final = ImageOps.fit(img, (w, h), Image.LANCZOS)
            return ctk.CTkImage(final, size=(w, h))
        except Exception:
            pass

    ph = Image.new("RGB", (w, h), (215, 238, 252))
    return ctk.CTkImage(ph, size=(w, h))

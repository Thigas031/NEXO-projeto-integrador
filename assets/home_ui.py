"""
UI helpers for the Home screen. Move repetitive UI code here so `views/home.py`
stays concise.
"""
import customtkinter as ctk
from PIL import Image, ImageOps
import os


def criar_topbar(parent, on_search_change, on_open_pedidos, on_open_perfil):
    """
    Create a topbar (frame) with a search entry and cart/profile buttons.
    Returns: (topbar_frame, search_entry)
    """
    topbar = ctk.CTkFrame(parent, height=72, fg_color="#2f49c8", corner_radius=0)
    topbar.place(relx=0, rely=0, relwidth=1)

    search_entry = ctk.CTkEntry(
        topbar, width=500, height=38,
        placeholder_text="Buscar produtos, marcas e muito mais..."
    )
    search_entry.place(relx=0.5, rely=0.5, anchor="center")
    if callable(on_search_change):
        search_entry.bind("<KeyRelease>", lambda e: on_search_change())

    ctk.CTkButton(
        topbar,
        text="🛒 Carrinho",
        width=120,
        fg_color="#1e1e3a",
        hover_color="#353562",
        command=on_open_pedidos
    ).place(relx=0.82, rely=0.5, anchor="center")

    ctk.CTkButton(
        topbar,
        text="👤 Perfil",
        width=120,
        fg_color="#1e1e3a",
        hover_color="#353562",
        command=on_open_perfil
    ).place(relx=0.93, rely=0.5, anchor="center")

    return topbar, search_entry


def criar_catbar(parent, categorias, on_categoria_click):
    """
    Create the category bar. Returns a dict with references that the view can use:
    { 'catbar': frame, 'btn_categorias': button, 'categoria_labels': dict }
    """
    catbar = ctk.CTkFrame(parent, height=48, fg_color="#3f5dff", corner_radius=0)
    catbar.place(relx=0, y=72, relwidth=1)

    btn_categorias = ctk.CTkButton(
        catbar, text="Categorias ⌄", width=160,
        fg_color="transparent", hover_color="#5670ff",
        text_color="white"
    )
    btn_categorias.place(relx=0.12, rely=0.5, anchor="center")

    categoria_labels = {}
    n = len(categorias)
    start = 0.18
    span = 0.64
    for idx, nome in enumerate(categorias):
        relx = start + (span * idx / (n - 1)) if n > 1 else 0.5
        lbl = ctk.CTkLabel(catbar, text=nome, text_color="white", font=("Arial", 16))
        lbl.place(relx=relx, rely=0.5, anchor="center")
        lbl.bind("<Button-1>", lambda e, n=nome: on_categoria_click(n))
        categoria_labels[nome] = lbl

    dropdown = ctk.CTkFrame(parent, fg_color="#2d3a8c", corner_radius=6)

    for nome in categorias[:5]:
        ctk.CTkButton(
            dropdown, text=nome,
            fg_color="transparent", hover_color="#3c4ca8",
            text_color="white",
            command=lambda n=nome: on_categoria_click(n)
        ).pack(padx=8, pady=6)

    return {
        'catbar': catbar,
        'btn_categorias': btn_categorias,
        'categoria_labels': categoria_labels,
        'dropdown': dropdown
    }


def carregar_imagem_produto(produto, w, h):
    """
    Load product image into a CTkImage. Falls back to placeholder.
    """
    from customtkinter import CTkImage
    if getattr(produto, 'imagem', None) and os.path.exists(produto.imagem):
        try:
            img = Image.open(produto.imagem).convert('RGB')
            final = ImageOps.fit(img, (w, h), Image.LANCZOS)
            return CTkImage(final, size=(w, h))
        except Exception:
            pass
    ph = Image.new('RGB', (w, h), (215, 238, 252))
    return CTkImage(ph, size=(w, h))


def filtrar_produtos(produtos, filtro_texto=None, filtro_categoria=None):
    """
    Retorna a lista de produtos filtrada por texto e categoria.
    """
    if not produtos:
        return []
    filtro_texto = (filtro_texto or "").strip().lower()
    resultado = []
    for p in produtos:
        if filtro_texto and filtro_texto not in f"{p.nome} {p.categoria}".lower():
            continue
        if filtro_categoria and p.categoria.lower() != filtro_categoria.lower():
            continue
        resultado.append(p)
    return resultado


def render_products_grid(scroll_frame, produtos, on_add=None, on_fav=None, on_edit=None, on_remove=None, on_set_fav_visual=None, cols=4, criar_produto_card_fn=None):
    """
    Renderiza os produtos dentro do `scroll_frame` em uma grid com `cols` colunas.

    - `criar_produto_card_fn` deve ser a função que cria cards (ex: views.assets.criar_produto_card).
    - callbacks: on_add(produto), on_fav(produto_id), on_edit(produto), on_remove(produto_id)
    """
    # limpa
    for w in list(scroll_frame.winfo_children()):
        try:
            w.destroy()
        except Exception:
            pass

    if not produtos:
        ctk.CTkLabel(scroll_frame, text="Nenhum produto encontrado", text_color="white", font=("Arial", 20, "bold")).grid(row=0, column=0)
        return

    if criar_produto_card_fn is None:
        # tenta importar a função padrão
        try:
            from views.assets import criar_produto_card as criar_produto_card_fn
        except Exception:
            criar_produto_card_fn = None

    for i, p in enumerate(produtos):
        r = i // cols
        c = i % cols
        # tenta carregar imagem via helper local
        img = None
        try:
            img = carregar_imagem_produto(p, 260, 160)
        except Exception:
            img = None

        # cria card usando a função fornecida
        if criar_produto_card_fn:
            card = criar_produto_card_fn(scroll_frame, p, img=img, on_add=on_add, on_fav=on_fav, on_edit=on_edit, on_remove=on_remove)
            try:
                card.grid(row=r, column=c, padx=20, pady=20)
            except Exception:
                # fallback: pack
                card.pack(padx=12, pady=12)
            # se for passada uma função para ajustar estado do botão favorito, chama-a
            try:
                if callable(on_set_fav_visual):
                    # o helper pode expor o botão como atributo `fav_btn` do card
                    fav_btn = getattr(card, 'fav_btn', None)
                    on_set_fav_visual(fav_btn, p)
            except Exception:
                pass
        else:
            # fallback mínimo
            f = ctk.CTkFrame(scroll_frame, fg_color="#3b3b5c", corner_radius=6)
            f.grid(row=r, column=c, padx=20, pady=20)
            ctk.CTkLabel(f, text=f"{p.nome} — R$ {p.preco:.2f}", text_color="white").pack(padx=8, pady=8)

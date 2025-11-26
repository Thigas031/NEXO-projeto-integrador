"""
Módulo centralizado para geração de assets (imagens, gradientes, etc.)
Objetivo: Reduzir duplicação de código nos arquivos de views
"""

import customtkinter as ctk
from PIL import Image, ImageDraw
import os


def criar_gradiente(largura: int, altura: int, cor_inicio: tuple, cor_fim: tuple) -> ctk.CTkImage:
    """
    Cria uma imagem de gradiente vertical.
    
    Args:
        largura: Largura da imagem em pixels
        altura: Altura da imagem em pixels
        cor_inicio: RGB tuple para cor inicial (topo)
        cor_fim: RGB tuple para cor final (fundo)
    
    Returns:
        ctk.CTkImage pronta para usar em widgets CustomTkinter
    """
    img = Image.new("RGB", (largura, altura))
    draw = ImageDraw.Draw(img)
    
    r1, g1, b1 = cor_inicio
    r2, g2, b2 = cor_fim
    
    for y in range(altura):
        ratio = y / altura
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (largura, y)], fill=(r, g, b))
    
    return ctk.CTkImage(light_image=img, size=(largura, altura))


def criar_gradiente_otimizado(tela_largura: int, tela_altura: int, 
                               cor_inicio: tuple, cor_fim: tuple) -> ctk.CTkImage:
    """
    Cria gradiente com tamanho otimizado para performance.
    Tamanho reduzido internamente, expandido pelo CustomTkinter.
    
    Args:
        tela_largura: Largura da tela (para proporção)
        tela_altura: Altura da tela (para proporção)
        cor_inicio: RGB tuple para cor inicial
        cor_fim: RGB tuple para cor final
    
    Returns:
        ctk.CTkImage com tamanho reduzido internamente
    """
    # Tamanho base reduzido para economizar memória
    base_w = min(tela_largura, 1400)
    base_h = min(tela_altura, 900)
    
    # Limita tamanho mínimo
    base_w = max(base_w, 800)
    base_h = max(base_h, 600)
    
    return criar_gradiente(base_w, base_h, cor_inicio, cor_fim)


def criar_avatar_placeholder(nome: str, tamanho: int = 80) -> Image.Image:
    """
    Cria um avatar placeholder com iniciais do nome.
    
    Args:
        nome: Nome do usuário
        tamanho: Tamanho em pixels
    
    Returns:
        PIL.Image com o avatar
    """
    cores = [
        (52, 152, 219),    # Azul
        (46, 204, 113),    # Verde
        (155, 89, 182),    # Roxo
        (230, 126, 34),    # Laranja
        (231, 76, 60),     # Vermelho
    ]
    
    # Seleciona cor baseado no hash do nome
    cor_idx = sum(ord(c) for c in nome.lower()) % len(cores)
    cor = cores[cor_idx]
    
    img = Image.new("RGB", (tamanho, tamanho), color=cor)
    draw = ImageDraw.Draw(img)
    
    # Pega iniciais
    iniciais = "".join(word[0].upper() for word in nome.split() if word)[:2]
    
    # Desenha texto centralizado (nota: fonte pode variar)
    # Usa tamanho proporcional ao tamanho do avatar
    font_size = int(tamanho * 0.4)
    
    # Posição aproximada para centralizar
    x = tamanho // 3
    y = tamanho // 3
    
    draw.text((x, y), iniciais, fill="white", font=None)
    
    return img


def limpar_cache_imagens():
    """Limpa cache de imagens se necessário (futuro otimização)."""
    pass


def criar_logo_label(parent, texto="NEXO", mostrar_texto=True, tamanho=18):
    """
    Retorna um widget `CTkLabel` com a logo do sistema (placeholder emoji).

    Args:
        parent: widget pai onde o label será inserido
        texto: texto do sistema a ser exibido ao lado da logo

    Observação: por enquanto a logo é um emoji de carrinho como placeholder.
    """
    import customtkinter as ctk

    logo_txt = "🧺"  # emoji de cesta/carrinho como placeholder
    if mostrar_texto and texto:
        txt = f"{logo_txt}  {texto}"
    else:
        txt = f"{logo_txt}"
    lbl = ctk.CTkLabel(parent, text=txt, font=("Arial", tamanho, "bold"), text_color="white")
    return lbl


def criar_rodape(root, texto_adicional=""):
    """
    Cria e posiciona um rodapé simples no `root` (janela principal).

    Args:
        root: a janela principal (CTk)
        texto_adicional: texto extra a ser exibido junto ao copyright

    Retorna:
        o frame do rodapé criado
    """
    import customtkinter as ctk
    from datetime import datetime

    ano = datetime.now().year
    rodape = ctk.CTkFrame(root, height=28, fg_color="#111217")
    try:
        # posiciona no rodapé
        rodape.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0)
    except Exception:
        # fallback: pack
        rodape.pack(side="bottom", fill="x")

    texto = f"© {ano} NEXO. {texto_adicional}"
    lbl = ctk.CTkLabel(rodape, text=texto, font=("Arial", 10), text_color="#9CA3AF")
    lbl.place(relx=0.5, rely=0.5, anchor="center")

    return rodape


def criar_back_button(parent, command, x=20, y=20, width=120):
    """
    Cria e posiciona um botão de voltar padrão.
    Retorna o widget criado.
    """
    import customtkinter as ctk

    btn = ctk.CTkButton(parent, text="← Voltar", width=width,
                        fg_color="#273469", hover_color="#3c4f9b",
                        command=command)
    try:
        btn.place(x=x, y=y)
    except Exception:
        try:
            btn.pack(side="left", padx=6, pady=6)
        except Exception:
            pass
    return btn


def criar_produto_card(parent, produto, img=None, on_add=None, on_fav=None, on_edit=None, on_remove=None):
    """
    Cria um card de produto reutilizável com layout padrão.

    Args:
        parent: container onde o card será adicionado
        produto: objeto Produto
        img: CTkImage opcional já preparado
        on_add: função chamada com (produto) ao adicionar ao carrinho
        on_fav: função chamada com (produto.id) ao favoritar
        on_edit: função chamada com (produto) ao editar
        on_remove: função chamada com (produto.id) ao remover

    Retorna o frame do card.
    """
    import customtkinter as ctk

    card = ctk.CTkFrame(parent, width=300, height=360, corner_radius=12, fg_color="#6f7dc8")
    card.pack_propagate(False)

    # imagem
    img_w, img_h = 260, 160
    img_frame = ctk.CTkFrame(card, width=img_w, height=img_h, corner_radius=8, fg_color="#d7eefc")
    img_frame.pack(pady=(18, 8))
    img_frame.pack_propagate(False)

    if img is not None:
        lbl_img = ctk.CTkLabel(img_frame, image=img, text="")
        lbl_img.image = img
        lbl_img.pack(fill="both", expand=True)
    else:
        lbl_img = ctk.CTkLabel(img_frame, text="", text_color="")
        lbl_img.pack(fill="both", expand=True)

    ctk.CTkLabel(card, text=produto.nome, font=("Arial", 16, "bold"), text_color="white").pack()
    ctk.CTkLabel(card, text=produto.categoria, font=("Arial", 12), text_color="#CCCCCC").pack()
    ctk.CTkLabel(card, text=f"R$ {produto.preco:.2f}", font=("Arial", 15, "bold"), text_color="#16A34A").pack(pady=4)

    bottom = ctk.CTkFrame(card, fg_color="transparent")
    bottom.pack(fill="x", pady=8)

    fav_btn = ctk.CTkButton(bottom, text="♡", width=60, fg_color="#1b1f3b", hover_color="#2c355e",
                            command=(lambda p=produto: on_fav(p.id) if callable(on_fav) else None))
    fav_btn.pack(side="left", padx=6)

    ctk.CTkButton(bottom, text="Adicionar", width=120, fg_color="#0f172a", hover_color="#213055",
                  command=(lambda p=produto: on_add(p) if callable(on_add) else None)).pack(side="right")

    tools = ctk.CTkFrame(card, fg_color="transparent")
    tools.place(relx=0.5, rely=0.85, anchor="center")

    ctk.CTkButton(tools, text="Editar", width=80, fg_color="#2563eb", hover_color="#1e40af",
                  command=(lambda p=produto: on_edit(p) if callable(on_edit) else None)).pack(side="left", padx=6)

    ctk.CTkButton(tools, text="Remover", width=80, fg_color="#7f1f1f", hover_color="#9b2a2a",
                  command=(lambda pid=produto.id: on_remove(pid) if callable(on_remove) else None)).pack(side="left", padx=6)

    return card
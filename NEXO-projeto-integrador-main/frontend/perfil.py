import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageOps

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class TelaPerfil(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Perfil")
        self.state("zoomed")  # Tela cheia

        # ============================
        # FUNDO GRADIENTE (CORRIGIDO)
        # ============================
        self.canvas_bg = ctk.CTkCanvas(self, highlightthickness=0, bd=0)
        self.canvas_bg.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)

        # ============================
        # CARD PRINCIPAL
        # ============================
        self.card = ctk.CTkFrame(
            self.canvas_bg,
            fg_color="#0F172A",
            corner_radius=0,
            width=780,
            height=900
        )
        self.card.place(relx=0.5, rely=0.52, anchor="center")

        self._capa()
        self._foto_perfil()
        self._info_usuario()
        self._metricas()
        self._abas()
        self._scroll_produtos()

    # =============================================================
    # FUNDO GRADIENTE REAL (IGUAL À HOME)
    # =============================================================
    def _draw_gradient(self, event=None):
        self.canvas_bg.delete("grad")

        w = self.winfo_width()
        h = self.winfo_height()

        # Gradiente verdadeiro igual às suas telas anteriores
        c1 = (7, 12, 40)     # Azul muito escuro (topo)
        c2 = (12, 20, 80)    # Azul escuro intermediário
        c3 = (12, 138, 144)  # Azul petróleo da parte inferior

        for i in range(h):
            # Transição c1 → c2
            r = int(c1[0] + (c2[0] - c1[0]) * (i / h))
            g = int(c1[1] + (c2[1] - c1[1]) * (i / h))
            b = int(c1[2] + (c2[2] - c1[2]) * (i / h))

            # Transição c2 → c3 (parte final)
            if i > h * 0.65:
                f = (i - h * 0.65) / (h * 0.35)
                r = int(r + (c3[0] - r) * f)
                g = int(g + (c3[1] - g) * f)
                b = int(b + (c3[2] - b) * f)

            self.canvas_bg.create_line(0, i, w, i, fill=f"#{r:02x}{g:02x}{b:02x}", tags="grad")

    # =============================================================
    # CAPA DO PERFIL
    # =============================================================
    def _capa(self):
        try:
            img = Image.open("capa.png").resize((780, 260))
        except:
            img = Image.new("RGB", (780, 260), "#1E293B")

        self.capa_img = ImageTk.PhotoImage(img)
        ctk.CTkLabel(self.card, image=self.capa_img, text="").place(x=0, y=0)

    # =============================================================
    # FOTO DE PERFIL (CIRCULAR + BORDA)
    # =============================================================
    def _foto_perfil(self):
        size = 160

        try:
            img = Image.open("perfil.png").resize((size, size))
        except:
            img = Image.new("RGB", (size, size), "#444444")

        # máscara circular
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        circular = ImageOps.fit(img, (size, size))
        circular.putalpha(mask)

        # Borda fina branca
        border = 4
        final = Image.new("RGBA", (size + border * 2, size + border * 2), (255, 255, 255, 255))
        final.paste(circular, (border, border), circular)

        self.profile_img = ImageTk.PhotoImage(final)

        ctk.CTkLabel(self.card, image=self.profile_img, text="").place(x=40, y=180)

    # =============================================================
    # NOME + @user + DESCRIÇÃO + ★ AVALIAÇÃO
    # =============================================================
    def _info_usuario(self):
        ctk.CTkLabel(
            self.card, text="Palhaço caçaçorola",
            font=("Arial", 24, "bold"), text_color="white"
        ).place(x=230, y=190)

        ctk.CTkLabel(
            self.card, text="@palhaco123",
            font=("Arial", 15), text_color="#A0A0A0"
        ).place(x=230, y=225)

        ctk.CTkLabel(
            self.card,
            text="Descrição do perfil.\nblablablablabla",
            font=("Arial", 15),
            text_color="white",
            justify="left"
        ).place(x=230, y=260)

        # ------------------------
        # ⭐⭐ AVALIAÇÃO ⭐⭐
        # ------------------------
        estrelas = "⭐ ⭐ ⭐ ⭐ ☆"
        ctk.CTkLabel(
            self.card,
            text=estrelas,
            font=("Arial", 20),
            text_color="#FACC15"
        ).place(x=230, y=310)

        # botão editar
        ctk.CTkButton(
            self.card,
            text="Editar Perfil",
            width=140,
            fg_color="#1E293B",
            hover_color="#334155",
            corner_radius=6
        ).place(x=600, y=200)

    # =============================================================
    # MÉTRICAS (Produtos / Seguidores)
    # =============================================================
    def _metricas(self):
        ctk.CTkLabel(
            self.card,
            text="125 Produtos",
            text_color="white",
            font=("Arial", 16)
        ).place(x=250, y=350)

        ctk.CTkLabel(
            self.card,
            text="125.000 Seguidores",
            text_color="white",
            font=("Arial", 16)
        ).place(x=430, y=350)

    # =============================================================
    # ABAS
    # =============================================================
    def _abas(self):
        self.btn_prod = ctk.CTkButton(
            self.card, text="Produtos",
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="white",
            width=150,
            corner_radius=4
        )
        self.btn_prod.place(x=260, y=400)

        self.btn_rel = ctk.CTkButton(
            self.card, text="Relatórios",
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="white",
            width=150,
            corner_radius=4
        )
        self.btn_rel.place(x=420, y=400)

        # linha azul da aba selecionada
        self.linha = ctk.CTkFrame(self.card, fg_color="#60A5FA", height=3, width=120)
        self.linha.place(x=295, y=437)

    # =============================================================
    # LISTAGEM SCROLL DE PRODUTOS
    # =============================================================
    def _scroll_produtos(self):
        self.scroll = ctk.CTkScrollableFrame(
            self.card,
            fg_color="#0F172A",
            width=760,
            height=430
        )
        self.scroll.place(x=10, y=470)

        for i in range(6):
            self._produto_card(i)

    # =============================================================
    # CARD DE PRODUTO
    # =============================================================
    def _produto_card(self, i):
        card = ctk.CTkFrame(
            self.scroll,
            fg_color="#1E293B",
            width=200,
            height=260,
            corner_radius=8
        )
        card.grid(row=i // 3, column=i % 3, padx=25, pady=20)
        card.pack_propagate(False)

        try:
            img = Image.open("produto.png").resize((160, 110))
        except:
            img = Image.new("RGB", (160, 110), "#3A3A3A")

        img_tk = ImageTk.PhotoImage(img)

        ctk.CTkLabel(card, image=img_tk, text="").pack(pady=10)
        card.img_ref = img_tk  # evita garbage collector

        ctk.CTkLabel(card, text="Produto", font=("Arial", 16, "bold"),
                     text_color="white").pack()

        ctk.CTkLabel(card, text="Descrição...", font=("Arial", 13),
                     text_color="#CCCCCC").pack()

        ctk.CTkLabel(card, text="R$ 12,90", font=("Arial", 15, "bold"),
                     text_color="#16A34A").pack(pady=4)


if __name__ == "__main__":
    TelaPerfil().mainloop()
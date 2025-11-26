"""
TELA ESTATÍSTICAS - VENDEDOR
Exibe estatísticas de vendas do vendedor
"""

import customtkinter as ctk
from views.core import loja, usuario_logado


class TelaEstatisticas:
    """Tela para visualização de estatísticas de vendas."""
    
    def __init__(self, container):
        self.container = container
        self.container.title("Estatísticas de Vendas")
        try:
            self.container.after(10, lambda: self.container.state("zoomed"))
        except Exception:
            pass
        
        self.construir()
        self.carregar_estatisticas()
    
    def construir(self):
        """Constrói a interface."""
        # Topbar
        topbar = ctk.CTkFrame(self.container, fg_color="#0a0e27", height=50)
        topbar.pack(fill="x", pady=0)
        topbar.pack_propagate(False)
        
        btn_voltar = ctk.CTkButton(
            topbar, text="← Voltar", width=80, height=40,
            fg_color="#1b1f3b", hover_color="#2a2e4b",
            command=self._voltar
        )
        btn_voltar.pack(side="left", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(
            topbar, text="📊 Estatísticas de Vendas", font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        titulo.pack(side="left", padx=20)
        
        # Área principal
        main_frame = ctk.CTkFrame(self.container, fg_color="#0a0e27")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Scroll para conteúdo
        self.scroll_frame = ctk.CTkScrollableFrame(
            main_frame, fg_color="#0a0e27"
        )
        self.scroll_frame.pack(fill="both", expand=True)
    
    def carregar_estatisticas(self):
        """Carrega e exibe estatísticas."""
        # Limpar
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        uid = usuario_logado.get("id")
        stats = loja.gerar_estatisticas(uid)
        
        if not stats:
            label_erro = ctk.CTkLabel(
                self.scroll_frame,
                text="Erro ao carregar estatísticas.",
                font=("Arial", 14),
                text_color="#ff6666"
            )
            label_erro.pack(pady=50)
            return
        
        # Seção: Total de Vendas
        self._criar_secao_estatistica(
            "Total de Vendas",
            str(stats["total_vendas"]),
            "unidades vendidas",
            "#77dd77"
        )
        
        # Seção: Faturamento Total
        self._criar_secao_estatistica(
            "Faturamento Total",
            f"R$ {stats['total_faturamento']:.2f}",
            "em receita",
            "#77aadd"
        )
        
        # Seção: Produtos Mais Vendidos
        self._criar_secao_produtos_vendidos(stats["produtos_mais_vendidos"])
    
    def _criar_secao_estatistica(self, titulo, valor, subtitulo, cor):
        """Cria uma seção de estatística."""
        frame = ctk.CTkFrame(
            self.scroll_frame, fg_color="#1b1f3b",
            corner_radius=10, border_width=2, border_color=cor
        )
        frame.pack(fill="x", pady=15, padx=10)
        
        # Título
        titulo_label = ctk.CTkLabel(
            frame, text=titulo, font=("Arial", 14, "bold"),
            text_color="#ffffff"
        )
        titulo_label.pack(pady=10, padx=10)
        
        # Valor (grande)
        valor_label = ctk.CTkLabel(
            frame, text=valor, font=("Arial", 32, "bold"),
            text_color=cor
        )
        valor_label.pack(pady=5, padx=10)
        
        # Subtítulo
        sub_label = ctk.CTkLabel(
            frame, text=subtitulo, font=("Arial", 12),
            text_color="#aaaaaa"
        )
        sub_label.pack(pady=(0, 15), padx=10)
    
    def _criar_secao_produtos_vendidos(self, produtos_dict):
        """Cria seção de produtos mais vendidos."""
        frame = ctk.CTkFrame(
            self.scroll_frame, fg_color="#1b1f3b",
            corner_radius=10, border_width=2, border_color="#ddaa77"
        )
        frame.pack(fill="x", pady=15, padx=10)
        
        # Título
        titulo_label = ctk.CTkLabel(
            frame, text="Produtos Mais Vendidos", font=("Arial", 14, "bold"),
            text_color="#ffffff"
        )
        titulo_label.pack(pady=10, padx=10, anchor="w")
        
        if not produtos_dict:
            label_vazio = ctk.CTkLabel(
                frame, text="Nenhuma venda registrada ainda.",
                font=("Arial", 12), text_color="#aaaaaa"
            )
            label_vazio.pack(pady=20, padx=10)
            return
        
        # Ordenar por quantidade vendida
        produtos_ordenados = sorted(
            produtos_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Criar lista de produtos
        for i, (nome_produto, quantidade) in enumerate(produtos_ordenados[:10], 1):
            item_frame = ctk.CTkFrame(frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=15, pady=5)
            
            # Posição
            pos_label = ctk.CTkLabel(
                item_frame, text=f"{i}º", font=("Arial", 12, "bold"),
                text_color="#ddaa77", width=30, anchor="w"
            )
            pos_label.pack(side="left", padx=5)
            
            # Nome do produto
            nome_label = ctk.CTkLabel(
                item_frame, text=nome_produto, font=("Arial", 11),
                text_color="#ffffff", anchor="w"
            )
            nome_label.pack(side="left", padx=5, expand=True, fill="x")
            
            # Quantidade (barra visual)
            max_qty = max([q for _, q in produtos_ordenados])
            percentual = (quantidade / max_qty) * 100
            
            barra_frame = ctk.CTkFrame(item_frame, fg_color="#0a0e27", height=20)
            barra_frame.pack(side="left", padx=5, fill="x", expand=True)
            
            barra = ctk.CTkFrame(
                barra_frame, fg_color="#ddaa77", height=20,
                corner_radius=3
            )
            barra.place(relwidth=percentual/100, relheight=1)
            
            # Quantidade (texto)
            qty_label = ctk.CTkLabel(
                item_frame, text=f"{quantidade} un.", font=("Arial", 11, "bold"),
                text_color="#ddaa77", width=80, anchor="e"
            )
            qty_label.pack(side="left", padx=5)
    
    def _voltar(self):
        """Volta para home."""
        self.container.destroy()
        from views.home import TelaHome
        TelaHome().mainloop()

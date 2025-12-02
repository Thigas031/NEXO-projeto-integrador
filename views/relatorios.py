"""
TELA RELATÓRIOS - VENDEDOR
Exibe relatórios de vendas do vendedor com filtros por período
"""

import customtkinter as ctk
from views.core import loja, usuario_logado
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog


class TelaRelatorios:
    """Tela para visualização de relatórios de vendas."""
    
    def __init__(self, container):
        self.container = container
        self.container.title("Relatórios de Vendas")
        try:
            self.container.after(10, lambda: self.container.state("zoomed"))
        except Exception:
            pass
        
        self.periodo_selecionado = "mes"
        
        self.construir()
        self.carregar_relatorio()
    
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
            topbar, text="📋 Relatórios de Vendas", font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        titulo.pack(side="left", padx=20)
        
        # Frame de filtros
        filtro_frame = ctk.CTkFrame(self.container, fg_color="#1b1f3b", height=50)
        filtro_frame.pack(fill="x", padx=10, pady=10)
        filtro_frame.pack_propagate(False)
        
        lbl_filtro = ctk.CTkLabel(
            filtro_frame, text="Período:", font=("Arial", 12),
            text_color="#ffffff"
        )
        lbl_filtro.pack(side="left", padx=10, pady=10)
        
        # Segmented button para período
        self.seg_periodo = ctk.CTkSegmentedButton(
            filtro_frame,
            values=["Dia", "Mês", "Ano"],
            command=self._mudar_periodo,
            font=("Arial", 11),
            fg_color="#2a2e4b",
            selected_color="#1f7f1f",
            selected_hover_color="#2d9d2d"
        )
        self.seg_periodo.set("Mês")
        self.seg_periodo.pack(side="left", padx=10)

        # Botões de exportação
        btn_export_pdf = ctk.CTkButton(
            filtro_frame, text="Exportar PDF", width=120, height=36,
            fg_color="#3b6bd8", hover_color="#4a7bf0",
            command=self._exportar_pdf
        )
        btn_export_pdf.pack(side="right", padx=10)

        btn_export_xlsx = ctk.CTkButton(
            filtro_frame, text="Exportar XLSX", width=120, height=36,
            fg_color="#3b8f5a", hover_color="#4aa46f",
            command=self._exportar_excel
        )
        btn_export_xlsx.pack(side="right", padx=10)
        
        # Área principal
        main_frame = ctk.CTkFrame(self.container, fg_color="#0a0e27")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scroll para relatório
        self.scroll_frame = ctk.CTkScrollableFrame(
            main_frame, fg_color="#0a0e27"
        )
        self.scroll_frame.pack(fill="both", expand=True)
    
    def _mudar_periodo(self, valor):
        """Muda período do relatório."""
        periodo_map = {"Dia": "dia", "Mês": "mes", "Ano": "ano"}
        self.periodo_selecionado = periodo_map.get(valor, "mes")
        self.carregar_relatorio()
    
    def carregar_relatorio(self):
        """Carrega e exibe relatório."""
        # Limpar
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        uid = usuario_logado.get("id")
        vendas = loja.gerar_relatorio(uid, self.periodo_selecionado)
        
        if not vendas:
            label_vazio = ctk.CTkLabel(
                self.scroll_frame,
                text="Nenhuma venda registrada neste período.",
                font=("Arial", 14),
                text_color="#aaaaaa"
            )
            label_vazio.pack(pady=50)
            return
        
        # Resumo no topo
        total_quantidade = sum(v["quantidade"] for v in vendas)
        total_faturamento = sum(v["total"] for v in vendas)
        
        self._criar_resumo(total_quantidade, total_faturamento)
        
        # Separador
        sep = ctk.CTkFrame(
            self.scroll_frame, fg_color="#2a2e4b", height=2
        )
        sep.pack(fill="x", pady=15, padx=20)
        
        # Tabela de vendas
        self._criar_tabela_vendas(vendas)
    
    def _criar_resumo(self, total_qty, total_valor):
        """Cria seção de resumo."""
        resumo_frame = ctk.CTkFrame(
            self.scroll_frame, fg_color="#1b1f3b",
            corner_radius=8, border_width=1, border_color="#2a2e4b"
        )
        resumo_frame.pack(fill="x", padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            resumo_frame, text="Resumo do Período",
            font=("Arial", 12, "bold"), text_color="#ffffff"
        )
        titulo.pack(pady=10, padx=10, anchor="w")
        
        # Grid de info
        info_frame = ctk.CTkFrame(resumo_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Quantidade
        qty_frame = ctk.CTkFrame(
            info_frame, fg_color="#0a0e27",
            corner_radius=5, border_width=1, border_color="#77dd77"
        )
        qty_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        qty_label1 = ctk.CTkLabel(
            qty_frame, text="Total Vendido", font=("Arial", 10),
            text_color="#aaaaaa"
        )
        qty_label1.pack(pady=5, padx=5)
        
        qty_label2 = ctk.CTkLabel(
            qty_frame, text=f"{total_qty} unidades", font=("Arial", 14, "bold"),
            text_color="#77dd77"
        )
        qty_label2.pack(pady=(0, 5), padx=5)
        
        # Faturamento
        fat_frame = ctk.CTkFrame(
            info_frame, fg_color="#0a0e27",
            corner_radius=5, border_width=1, border_color="#77aadd"
        )
        fat_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        fat_label1 = ctk.CTkLabel(
            fat_frame, text="Faturamento", font=("Arial", 10),
            text_color="#aaaaaa"
        )
        fat_label1.pack(pady=5, padx=5)
        
        fat_label2 = ctk.CTkLabel(
            fat_frame, text=f"R$ {total_valor:.2f}", font=("Arial", 14, "bold"),
            text_color="#77aadd"
        )
        fat_label2.pack(pady=(0, 5), padx=5)
    
    def _criar_tabela_vendas(self, vendas):
        """Cria tabela de vendas."""
        # Cabeçalho da tabela
        header_frame = ctk.CTkFrame(
            self.scroll_frame, fg_color="#2a2e4b",
            corner_radius=5
        )
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        headers = [
            ("Produto", 0.35),
            ("Quantidade", 0.15),
            ("Preço Unit.", 0.15),
            ("Total", 0.15),
            ("Data", 0.2)
        ]
        
        for header, width in headers:
            lbl = ctk.CTkLabel(
                header_frame, text=header, font=("Arial", 11, "bold"),
                text_color="#ffffff"
            )
            lbl.pack(side="left", fill="x", expand=True, padx=10, pady=8)
        
        # Linhas de dados
        for i, venda in enumerate(vendas):
            linha_frame = ctk.CTkFrame(
                self.scroll_frame, fg_color="#1b1f3b" if i % 2 == 0 else "#0a0e27",
                corner_radius=5
            )
            linha_frame.pack(fill="x", padx=10, pady=2)
            
            # Produto
            lbl_prod = ctk.CTkLabel(
                linha_frame, text=venda["nome_produto"][:30],
                font=("Arial", 10), text_color="#ffffff", anchor="w"
            )
            lbl_prod.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            # Quantidade
            lbl_qty = ctk.CTkLabel(
                linha_frame, text=str(venda["quantidade"]),
                font=("Arial", 10), text_color="#77dd77", anchor="center"
            )
            lbl_qty.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            # Preço unitário
            lbl_preco = ctk.CTkLabel(
                linha_frame, text=f"R$ {venda['preco']:.2f}",
                font=("Arial", 10), text_color="#aaaaaa", anchor="center"
            )
            lbl_preco.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            # Total
            lbl_total = ctk.CTkLabel(
                linha_frame, text=f"R$ {venda['total']:.2f}",
                font=("Arial", 10, "bold"), text_color="#77aadd", anchor="center"
            )
            lbl_total.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            # Data
            data_str = str(venda.get("data_pedido", "-"))[:10]
            lbl_data = ctk.CTkLabel(
                linha_frame, text=data_str,
                font=("Arial", 10), text_color="#999999", anchor="e"
            )
            lbl_data.pack(side="left", fill="x", expand=True, padx=10, pady=8)
    
    def _voltar(self):
        """Volta para home."""
        self.container.destroy()
        from views.home import TelaHome
        TelaHome().mainloop()

    def _exportar_pdf(self):
        """Gera e salva relatório em PDF usando a loja e mostra resultado."""
        uid = usuario_logado.get("id")
        periodo = self.periodo_selecionado
        # Pergunta ao usuário onde salvar (diálogo)
        from datetime import datetime
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_name = f'relatorio_{uid}_{periodo}_{ts}.pdf'
        caminho = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            filetypes=[('PDF', '*.pdf')],
            initialfile=default_name,
            initialdir='relatorios',
            title='Salvar relatório em PDF'
        )
        if not caminho:
            return
        try:
            saved = loja.exportar_relatorio_pdf(uid, periodo, caminho)
            if saved:
                messagebox.showinfo('Exportado', f'Relatório PDF salvo em:\n{saved}')
            else:
                messagebox.showerror('Erro', 'Falha ao gerar o relatório PDF.')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao exportar PDF:\n{e}')

    def _exportar_excel(self):
        """Gera e salva relatório em XLSX usando a loja e mostra resultado."""
        uid = usuario_logado.get("id")
        periodo = self.periodo_selecionado
        # Pergunta ao usuário onde salvar (diálogo)
        from datetime import datetime
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_name = f'relatorio_{uid}_{periodo}_{ts}.xlsx'
        caminho = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Excel', '*.xlsx'), ('All files', '*.*')],
            initialfile=default_name,
            initialdir='relatorios',
            title='Salvar relatório em XLSX'
        )
        if not caminho:
            return
        try:
            saved = loja.exportar_relatorio_excel(uid, periodo, caminho)
            if saved:
                messagebox.showinfo('Exportado', f'Relatório XLSX salvo em:\n{saved}')
            else:
                messagebox.showerror('Erro', 'Falha ao gerar o relatório XLSX.')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao exportar XLSX:\n{e}')

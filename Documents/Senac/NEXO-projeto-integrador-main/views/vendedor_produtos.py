"""
TELA MEUS PRODUTOS - VENDEDOR
Permite ao vendedor visualizar e cadastrar seus produtos
"""

import customtkinter as ctk
from views.core import loja, usuario_logado, get_usuario_obj
from views import theme
from tkinter import messagebox, filedialog
from PIL import Image
import io


class TelaVendedorProdutos:
    """Tela para gerenciamento de produtos do vendedor."""
    
    def __init__(self, container):
        self.container = container
        self.container.title("Meus Produtos")
        try:
            self.container.after(10, lambda: self.container.state("zoomed"))
        except Exception:
            pass
        
        self.produtos = []
        self.modo_cadastro = False
        
        self.construir()
        self.carregar_produtos()
    
    def construir(self):
        """Constrói a interface."""
        # Topbar
        topbar = ctk.CTkFrame(self.container, fg_color=theme.BG, height=50)
        topbar.pack(fill="x", pady=0)
        topbar.pack_propagate(False)
        
        btn_voltar = ctk.CTkButton(
            topbar, text="← Voltar", width=80, height=40,
            fg_color=theme.ALT_BG, hover_color=theme.PRIMARY_DARK,
            command=self._voltar
        )
        btn_voltar.pack(side="left", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(
            topbar, text="Meus Produtos", font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        titulo.pack(side="left", padx=20)
        
        btn_novo = ctk.CTkButton(
            topbar, text="Novo Produto", width=140, height=40,
            fg_color=theme.ACCENT, hover_color=theme.PRIMARY_DARK,
            command=self._abrir_cadastro
        )
        btn_novo.pack(side="right", padx=10, pady=5)
        
        # Área principal
        main_frame = ctk.CTkFrame(self.container, fg_color=theme.BG)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scroll para lista de produtos
        self.scroll_frame = ctk.CTkScrollableFrame(
            main_frame, fg_color=theme.BG
        )
        self.scroll_frame.pack(fill="both", expand=True)
        
        # Frame para cadastro (inicialmente oculto)
        self.cadastro_frame = ctk.CTkFrame(main_frame, fg_color=theme.CARD_BG)
        
    def _abrir_cadastro(self):
        """Abre formulário de cadastro."""
        self.modo_cadastro = True
        self.scroll_frame.pack_forget()
        self.cadastro_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Limpar frame
        for widget in self.cadastro_frame.winfo_children():
            widget.destroy()
        
        # Título
        titulo = ctk.CTkLabel(
            self.cadastro_frame, text="Cadastrar Novo Produto",
            font=("Arial", 16, "bold"), text_color="#ffffff"
        )
        titulo.pack(pady=10)
        
        # Scrollable form
        form_scroll = ctk.CTkScrollableFrame(
            self.cadastro_frame, fg_color="#1b1f3b"
        )
        form_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Campos
        campos = [
            ("Nome do Produto", "nome", "entry"),
            ("Preço", "preco", "entry"),
            ("Descrição", "descricao", "text"),
            ("Categoria", "categoria", "combo"),
            ("Estoque Inicial", "estoque", "entry"),
            ("Imagem (opcional)", "imagem", "file"),
        ]
        
        self.campos_cadastro = {}
        
        for label, key, tipo in campos:
            frame_campo = ctk.CTkFrame(form_scroll, fg_color="transparent")
            frame_campo.pack(fill="x", pady=8)
            
            lbl = ctk.CTkLabel(
                frame_campo, text=label, font=("Arial", 12),
                text_color="#ffffff", width=200, anchor="w"
            )
            lbl.pack(side="left", padx=5)
            
            if tipo == "entry":
                entry = ctk.CTkEntry(frame_campo)
                entry.pack(side="left", padx=5, fill="x", expand=True)
                self.campos_cadastro[key] = entry
                
            elif tipo == "text":
                text = ctk.CTkTextbox(frame_campo, height=80)
                text.pack(side="left", padx=5, fill="x", expand=True)
                self.campos_cadastro[key] = text
                
            elif tipo == "combo":
                combo = ctk.CTkComboBox(
                    frame_campo,
                    values=["Eletrônicos", "Moda", "Supermercado", "Esportes", "Casa", "Outro"]
                )
                combo.set("Eletrônicos")
                combo.pack(side="left", padx=5)
                self.campos_cadastro[key] = combo
                
            elif tipo == "file":
                btn_arquivo = ctk.CTkButton(
                    frame_campo, text="Selecionar...", width=120,
                    fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_DARK,
                    command=self._selecionar_imagem
                )
                btn_arquivo.pack(side="left", padx=5)
                lbl_arquivo = ctk.CTkLabel(
                    frame_campo, text="Nenhum arquivo", text_color="#aaaaaa"
                )
                lbl_arquivo.pack(side="left", padx=5)
                self.campos_cadastro["imagem_label"] = lbl_arquivo
        
        # Botões de ação
        frame_botoes = ctk.CTkFrame(form_scroll, fg_color="transparent")
        frame_botoes.pack(fill="x", pady=15)
        
        btn_salvar = ctk.CTkButton(
            frame_botoes, text="Salvar Produto", width=180,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_DARK,
            command=self._salvar_produto
        )
        btn_salvar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes, text="Cancelar", width=150,
            fg_color=theme.ALT_BG, hover_color=theme.PRIMARY_DARK,
            command=self._fechar_cadastro
        )
        btn_cancelar.pack(side="left", padx=10)
    
    def _selecionar_imagem(self):
        """Abre diálogo para selecionar imagem."""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif"), ("Todos", "*.*")]
        )
        if arquivo:
            self.campos_cadastro["imagem"] = arquivo
            self.campos_cadastro["imagem_label"].configure(text=arquivo.split("/")[-1])
    
    def _salvar_produto(self):
        """Salva novo produto."""
        try:
            # Validações
            nome = self.campos_cadastro["nome"].get().strip()
            preco_str = self.campos_cadastro["preco"].get().strip()
            descricao = self.campos_cadastro["descricao"].get("1.0", "end-1c").strip()
            categoria = self.campos_cadastro["categoria"].get()
            estoque_str = self.campos_cadastro["estoque"].get().strip()
            imagem = self.campos_cadastro.get("imagem", None)
            
            if not nome or not preco_str or not estoque_str:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            try:
                preco = float(preco_str)
                estoque = int(estoque_str)
            except:
                messagebox.showerror("Erro", "Preço e Estoque devem ser números válidos!")
                return
            
            # Dados do produto
            dados_produto = {
                "nome": nome,
                "preco": preco,
                "descricao": descricao,
                "categoria": categoria,
                "estoque": max(estoque, 1),
                "imagem": imagem
            }
            
            # Cadastrar no backend
            uid = usuario_logado.get("id")
            produto = loja.cadastrar_produto_para_vendedor(uid, dados_produto)
            
            if produto:
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                self._fechar_cadastro()
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar produto.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def _fechar_cadastro(self):
        """Fecha formulário de cadastro."""
        self.modo_cadastro = False
        self.cadastro_frame.pack_forget()
        self.scroll_frame.pack(fill="both", expand=True)
        self.carregar_produtos()
    
    def carregar_produtos(self):
        """Carrega e exibe produtos do vendedor."""
        # Limpar
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        uid = usuario_logado.get("id")
        self.produtos = loja.listar_produtos_do_vendedor(uid)
        
        if not self.produtos:
            label_vazio = ctk.CTkLabel(
                self.scroll_frame,
                text="Nenhum produto cadastrado ainda.",
                font=("Arial", 14),
                text_color="#aaaaaa"
            )
            label_vazio.pack(pady=50)
            return
        
        # Criar cards de produtos
        for i, produto in enumerate(self.produtos):
            row = i // 3
            col = i % 3
            self._criar_card_produto(produto, row, col)
    
    def _criar_card_produto(self, produto, row, col):
        """Cria card de produto."""
        card = ctk.CTkFrame(
            self.scroll_frame, fg_color=theme.CARD_BG,
            corner_radius=8, border_width=1, border_color=theme.PRIMARY_LIGHT
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Nome
        nome_label = ctk.CTkLabel(
            card, text=produto.nome[:25], font=("Arial", 12, "bold"),
            text_color="#ffffff", wraplength=200
        )
        nome_label.pack(padx=8, pady=5)
        
        # Categoria e preço
        info_label = ctk.CTkLabel(
            card, text=f"{produto.categoria} • R$ {produto.preco:.2f}",
            font=("Arial", 10), text_color="#aaaaaa"
        )
        info_label.pack(padx=8, pady=2)
        
        # Estoque
        estoque_label = ctk.CTkLabel(
            card, text=f"Estoque: {produto.estoque} un.",
            font=("Arial", 10), text_color="#77dd77"
        )
        estoque_label.pack(padx=8, pady=2)
        
        # Descrição (truncada)
        desc = produto.descricao[:50] if produto.descricao else "Sem descrição"
        desc_label = ctk.CTkLabel(
            card, text=desc + ("..." if len(produto.descricao) > 50 else ""),
            font=("Arial", 9), text_color="#999999", wraplength=200
        )
        desc_label.pack(padx=8, pady=5)
        
        # Botões
        frame_botoes = ctk.CTkFrame(card, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=8, pady=5)
        
        btn_editar = ctk.CTkButton(
            frame_botoes, text="Editar", width=90, height=30,
            fg_color=theme.ACCENT, hover_color=theme.PRIMARY_DARK,
            command=lambda p=produto: self._editar_produto(p)
        )
        btn_editar.pack(side="left", padx=2)
        
        btn_remover = ctk.CTkButton(
            frame_botoes, text="Remover", width=90, height=30,
            fg_color=theme.ALT_BG, hover_color=theme.PRIMARY_DARK,
            command=lambda p=produto: self._remover_produto(p)
        )
        btn_remover.pack(side="left", padx=2)
    
    def _editar_produto(self, produto):
        """Abre diálogo para editar produto."""
        messagebox.showinfo("Info", f"Edição do produto '{produto.nome}' em desenvolvimento.")
    
    def _remover_produto(self, produto):
        """Remove produto."""
        if messagebox.askyesno("Confirmar", f"Remover '{produto.nome}'?"):
            loja.remover_produto(produto.id)
            self.carregar_produtos()
            messagebox.showinfo("Sucesso", "Produto removido!")
    
    def _voltar(self):
        """Volta para home."""
        self.container.destroy()
        from views.home import TelaHome
        TelaHome().mainloop()

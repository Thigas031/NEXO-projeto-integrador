"""
MODELO LOJA
Sistema central de gerenciamento em memória (sem persistência JSON)
"""
from models.estoque import Estoque
from models.pedido import Pedido
from models.carrinho import Carrinho
from models.estatisticas import Estatisticas
from models.relatorios import Relatorios
from models.pagamento import Pagamento
from models.cliente import Cliente
from models.vendedor import Vendedor
from models.usuariobase import UsuarioBase
from models.produto import Produto


class Loja:
    """Gerencia todos os dados da loja com persistência."""
    
    ARQUIVO_DADOS = "dados_loja.json"
    
    def __init__(self):
        self.estoque = Estoque()
        self.pedidos = []
        self.clientes = []
        self.usuarios = []
        self.carrinho = Carrinho()
        self.rel = Relatorios()
        self.est = Estatisticas()
        self.pag = Pagamento()
        self.next_produto_id = 1
        self.next_pedido_id = 1
        self.next_cliente_id = 1
        self.next_usuario_id = 1
        
        # Iniciar com dados em memória (sem JSON)
        self.carregar_dados()

    def cadastrar_usuario(self, nome, email, senha, telefone="", endereco="", papel="vendedor", cpf="", nome_loja=""):
        """Cadastra novo usuário."""
        if papel == "vendedor":
            u = Vendedor(self.next_usuario_id, nome, email, senha, telefone, endereco, cpf, nome_loja)
        else:
            u = UsuarioBase(self.next_usuario_id, nome, email, senha, telefone, endereco, papel)
        
        self.usuarios.append(u)
        self.next_usuario_id += 1
        return u

    def validar_e_cadastrar_usuario(self, nome, email, senha, telefone="", endereco="", papel="cliente", cpf="", nome_loja=""):
        """Valida dados e cadastra usuário; retorna (sucesso, mensagem, usuario).
        Não usa JSON; opera em memória."""
        # Validações básicas
        if not all([nome, email, senha]):
            return (False, "Preencha os campos obrigatórios", None)
        if len(senha) < 3:
            return (False, "Senha deve ter no mínimo 3 caracteres", None)
        # Verifica usuário único
        if self.buscar_usuario_por_nome(nome):
            return (False, "Usuário já existe", None)

        u = self.cadastrar_usuario(nome, email, senha, telefone, endereco, papel, cpf, nome_loja)
        return (True, "Usuário cadastrado com sucesso", u)

    def autenticar_usuario(self, nome, senha):
        """Autentica usuário e retorna objeto de usuário ou None."""
        u = self.buscar_usuario_por_nome(nome)
        if not u:
            return None
        if getattr(u, 'senha', None) == senha:
            return u
        return None

    def buscar_usuario_por_nome(self, nome):
        """Busca usuário por nome."""
        for u in self.usuarios:
            if u.nome == nome:
                return u
        return None

    def buscar_usuario(self, usuario_id):
        """Busca usuário por ID."""
        for u in self.usuarios:
            if u.id == usuario_id:
                return u
        return None

    def editar_perfil(self, usuario_id, nome=None, email=None, telefone=None, endereco=None, nova_senha=None):
        """Edita perfil do usuário."""
        u = self.buscar_usuario(usuario_id)
        if u:
            u.editar_perfil(nome, email, telefone, endereco, nova_senha)
            self.salvar_dados()
            return True
        return False

    def cadastrar_cliente(self, nome, email, telefone="", endereco=""):
        """Cadastra novo cliente."""
        c = Cliente(self.next_cliente_id, nome, email, telefone, endereco)
        self.clientes.append(c)
        self.next_cliente_id += 1
        # Sem persistência
        return c

    def buscar_cliente(self, cliente_id):
        """Busca cliente por ID."""
        for c in self.clientes:
            if c.id == cliente_id:
                return c
        return None

    def cadastrar_produto(self, nome, categoria, preco, estoque, imagem=None):
        """Cadastra novo produto."""
        p = Produto(self.next_produto_id, nome, categoria, preco, estoque, imagem)
        self.estoque.adicionar(p)
        self.next_produto_id += 1
        return p

    def buscar_produto(self, produto_id):
        """Busca produto por ID."""
        for p in self.estoque.produtos:
            if p.id == produto_id:
                return p
        return None

    def editar_produto(self, produto_id, novo_nome=None, nova_categoria=None, novo_preco=None, novo_estoque=None, nova_imagem=None):
        """Edita dados do produto."""
        p = self.buscar_produto(produto_id)
        if not p:
            return False
        if novo_nome is not None:
            p.nome = novo_nome
        if nova_categoria is not None:
            p.categoria = nova_categoria
        if novo_preco is not None:
            try:
                p.preco = float(novo_preco)
            except:
                pass
        if novo_estoque is not None:
            try:
                p.estoque = int(novo_estoque)
            except:
                pass
        if nova_imagem is not None:
            p.imagem = nova_imagem
        # Sem persistência
        return True

    def remover_produto(self, produto_id):
        """Remove produto do estoque."""
        result = self.estoque.remover(produto_id)
        if result:
            pass
        return result

    def adicionar_favorito(self, usuario_id, produto_id):
        """Adiciona produto aos favoritos do usuário."""
        u = self.buscar_usuario(usuario_id)
        if u:
            u.adicionar_favorito(produto_id)
            return True
        return False

    def remover_favorito(self, usuario_id, produto_id):
        """Remove produto dos favoritos do usuário."""
        u = self.buscar_usuario(usuario_id)
        if u:
            u.remover_favorito(produto_id)
            return True
        return False

    def tem_favorito(self, usuario_id, produto_id):
        """Verifica se produto está nos favoritos."""
        u = self.buscar_usuario(usuario_id)
        if u:
            return u.tem_favorito(produto_id)
        return False

    def get_favoritos_do_usuario(self, usuario_id):
        """Retorna lista de IDs dos favoritos do usuário."""
        u = self.buscar_usuario(usuario_id)
        if u:
            return u.favoritos.listar()
        return []

    def listar_produtos_favoritos(self, usuario_id):
        """Retorna lista de objetos Produto dos favoritos."""
        favoritos_ids = self.get_favoritos_do_usuario(usuario_id)
        produtos = []
        for pid in favoritos_ids:
            p = self.buscar_produto(pid)
            if p:
                produtos.append(p)
        return produtos

    def cadastrar_produto_para_vendedor(self, vendedor_id, dados_produto):
        """Cadastra produto para um vendedor específico."""
        vendedor = self.buscar_usuario(vendedor_id)
        if not vendedor or getattr(vendedor, 'papel', None) != 'vendedor':
            return None

        nome = dados_produto.get('nome')
        categoria = dados_produto.get('categoria')
        preco = dados_produto.get('preco')
        estoque = dados_produto.get('estoque', 1)
        imagem = dados_produto.get('imagem')
        descricao = dados_produto.get('descricao', '')

        p = Produto(self.next_produto_id, nome, categoria, preco, estoque, imagem, descricao, id_do_vendedor=vendedor_id)
        self.estoque.adicionar(p)
        # registrar no vendedor
        if not hasattr(vendedor, 'produtos_do_vendedor'):
            vendedor.produtos_do_vendedor = []
        vendedor.produtos_do_vendedor.append(p.id)
        self.next_produto_id += 1
        return p

    def listar_produtos_do_vendedor(self, vendedor_id):
        """Lista produtos cadastrados por um vendedor."""
        produtos = [p for p in self.estoque.todos() if getattr(p, 'id_do_vendedor', None) == vendedor_id]
        return produtos

    def gerar_estatisticas(self, vendedor_id):
        """Gera estatísticas de vendas do vendedor."""
        total_vendas = 0
        total_faturamento = 0.0
        produtos_mais_vendidos = {}

        for pedido in self.pedidos:
            for item in pedido.itens:
                prod = item.produto
                if getattr(prod, 'id_do_vendedor', None) == vendedor_id:
                    quantidade = item.quantidade
                    total_vendas += quantidade
                    total_faturamento += item.subtotal()
                    produtos_mais_vendidos[prod.nome] = produtos_mais_vendidos.get(prod.nome, 0) + quantidade

        return {
            'total_vendas': total_vendas,
            'total_faturamento': round(total_faturamento, 2),
            'produtos_mais_vendidos': produtos_mais_vendidos
        }

    def gerar_relatorio(self, vendedor_id, periodo='mes'):
        """Gera relatório de vendas do vendedor por período ('dia','mes','ano')."""
        from datetime import datetime
        vendas = []
        now = datetime.now()
        for pedido in self.pedidos:
            for item in pedido.itens:
                prod = item.produto
                if getattr(prod, 'id_do_vendedor', None) != vendedor_id:
                    continue
                data = getattr(pedido, 'data', None)
                if data:
                    if periodo == 'dia' and (data.date() != now.date()):
                        continue
                    if periodo == 'mes' and (data.year != now.year or data.month != now.month):
                        continue
                    if periodo == 'ano' and (data.year != now.year):
                        continue

                vendas.append({
                    'nome_produto': prod.nome,
                    'quantidade': item.quantidade,
                    'preco': item.preco_unitario,
                    'total': round(item.subtotal(), 2),
                    'data_pedido': data.strftime('%d/%m/%Y %H:%M') if data else 'N/A'
                })

        return vendas

    def adicionar_ao_carrinho(self, nome_produto, quantidade):
        """Adiciona produto ao carrinho."""
        p = self.estoque.procurar(nome_produto)
        if p and p.estoque >= quantidade:
            self.carrinho.adicionar(p, quantidade)
            return True
        return False

    def fechar_pedido(self, cliente_id=None):
        """Fecha o pedido e registra."""
        cliente = None
        if cliente_id:
            cliente = self.buscar_cliente(cliente_id)
        
        total = self.carrinho.total()
        if not self.pag.processar(total):
            return None
        
        for item in self.carrinho.itens:
            item.produto.baixar_estoque(item.quantidade)
        
        pedido = Pedido(self.next_pedido_id, self.carrinho.itens.copy(), cliente)
        self.pedidos.append(pedido)
        self.next_pedido_id += 1
        self.carrinho.limpar()
        self.carrinho.limpar()

    def salvar_dados(self):
        """Sem persistência: método reservado para futura integração com DB."""
        return None

    def carregar_dados(self):
        """Inicializa dados em memória (sem JSON)."""
        # Criar usuários de teste em memória
        self.cadastrar_usuario(
            "admin", "admin@nexo.com", "123",
            "11999999999", "Rua A, 100",
            papel="vendedor", cpf="11111111111", nome_loja="NEXO Admin"
        )
        
        self.cadastrar_usuario(
            "vendedor", "vendedor@nexo.com", "123",
            "11888888888", "Rua B, 200",
            papel="vendedor", cpf="22222222222", nome_loja="Loja Teste"
        )

        # Criar produtos de teste
        self.cadastrar_produto("Notebook Dell", "Eletrônicos", 2500.00, 5)
        self.cadastrar_produto("Mouse Logitech", "Eletrônicos", 150.00, 20)
        self.cadastrar_produto("Teclado Mecânico", "Eletrônicos", 450.00, 10)
        self.cadastrar_produto("Monitor LG 24\"", "Eletrônicos", 1200.00, 8)
        self.cadastrar_produto("Headphone Sony", "Eletrônicos", 800.00, 15)
        self.cadastrar_produto("Webcam Logitech", "Eletrônicos", 350.00, 12)
        self.cadastrar_produto("Camiseta Básica", "Moda", 50.00, 50)
        self.cadastrar_produto("Calça Jeans", "Moda", 120.00, 30)
        self.cadastrar_produto("Arroz 5kg", "Supermercado", 25.00, 100)
        self.cadastrar_produto("Feijão 1kg", "Supermercado", 8.00, 80)

        return None

    # End of Loja

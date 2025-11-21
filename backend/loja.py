from backend.estoque import Estoque
from backend.pedido import Pedido
from backend.carrinho import Carrinho
from backend.estatisticas import Estatisticas
from backend.relatorios import Relatorios
from backend.pagamento import Pagamento
from backend.cliente import Cliente
from backend.vendedor import Vendedor
from backend.produto import Produto

class Loja:
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

    def cadastrar_produto(self, nome, categoria, preco, estoque, imagem=None):
        p = Produto(self.next_produto_id, nome, categoria, preco, estoque, imagem)
        self.estoque.adicionar(p)
        self.next_produto_id += 1
        
        return p

        p = Produto(self.next_produto_id, nome, categoria, preco, estoque, imagem=imagem)
        self.estoque.adicionar(p)
        self.next_produto_id += 1
        return p

    def cadastrar_cliente(self, nome, contato=""):
        c = Cliente(self.next_cliente_id, nome, contato)
        self.clientes.append(c)
        self.next_cliente_id += 1
        return c

    def cadastrar_usuario(self, nome, senha, papel="vendedor"):
        u = Vendedor(self.next_usuario_id, nome, senha)
        u.papel = papel
        self.usuarios.append(u)
        self.next_usuario_id += 1
        return u

    def buscar_usuario(self, usuario_id):
        for u in self.usuarios:
            if u.id == usuario_id:
                return u
        return None

    def editar_perfil(self, usuario_id, novo_nome=None, nova_senha=None):
        u = self.buscar_usuario(usuario_id)
        if u:
            u.editar_perfil(novo_nome, nova_senha)
            return True
        return False

    def buscar_produto(self, produto_id):
        for p in self.estoque.produtos:
            if p.id == produto_id:
                return p
        return None

    def favoritar(self, usuario_id, produto_id):
        u = self.buscar_usuario(usuario_id)
        p = self.buscar_produto(produto_id)
        if u and p:
            u.favoritar_produto(p)
            return True
        return False

    def desfavoritar(self, usuario_id, produto_id):
        u = self.buscar_usuario(usuario_id)
        p = self.buscar_produto(produto_id)
        if u and p:
            u.desfavoritar_produto(p)
            return True
        return False

    def adicionar_ao_carrinho(self, nome_produto, quantidade):
        p = self.estoque.procurar(nome_produto)
        if p and p.estoque >= quantidade:
            self.carrinho.adicionar(p, quantidade)
            return True
        return False

    def fechar_pedido(self, cliente_id=None):
        cliente = None
        for c in self.clientes:
            if c.id == cliente_id:
                cliente = c
        total = self.carrinho.total()
        if not self.pag.processar(total):
            return None
        for item in self.carrinho.itens:
            item.produto.baixar_estoque(item.quantidade)
        pedido = Pedido(self.next_pedido_id, self.carrinho.itens.copy(), cliente)
        self.pedidos.append(pedido)
        self.next_pedido_id += 1
        self.carrinho.limpar()
        return pedido
"""
LOJA - Sistema central de gerenciamento de dados
Carrega 100% do JSON, persiste todas as operações.
"""
from models.estoque import Estoque
from models.pedido import Pedido
from models.carrinho import Carrinho
from models.estatisticas import Estatisticas
from models.relatorios import Relatorios
from models.pagamento import Pagamento
from models.cliente import Cliente
from models.vendedor import Vendedor
from models.usuariobase import Usuario
from models.produto import Produto
from models.itempedido import ItemPedido
import os
import json


class Loja:
    """Gerencia todos os dados com persistência JSON."""
    
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
        self.carregar_dados()

    def _salvar_dados_seguro(self):
        """Helper que salva dados com fallback seguro."""
        try:
            self.salvar_dados()
        except Exception:
            pass

    # CRUD USUARIO
    def cadastrar_usuario(self, nome, email, senha, telefone="", endereco="", papel="vendedor", cpf="", nome_loja=""):
        u = Vendedor(self.next_usuario_id, nome, email, senha, telefone, endereco, cpf, nome_loja) if papel == "vendedor" else Usuario(self.next_usuario_id, nome, email, senha, telefone, endereco, papel)
        self.usuarios.append(u)
        self.next_usuario_id += 1
        self._salvar_dados_seguro()
        return u

    def validar_e_cadastrar_usuario(self, nome, email, senha, telefone="", endereco="", papel="cliente", cpf="", nome_loja=""):
        if not all([nome, email, senha]) or len(senha) < 3:
            return (False, "Dados inválidos", None)
        if self.buscar_usuario_por_nome(nome):
            return (False, "Usuário já existe", None)
        u = self.cadastrar_usuario(nome, email, senha, telefone, endereco, papel, cpf, nome_loja)
        return (True, "Usuário cadastrado", u)

    def autenticar_usuario(self, nome, senha):
        u = self.buscar_usuario_por_nome(nome)
        return u if u and getattr(u, 'senha', None) == senha else None

    def buscar_usuario_por_nome(self, nome):
        return next((u for u in self.usuarios if u.nome == nome), None)

    def buscar_usuario(self, usuario_id):
        return next((u for u in self.usuarios if u.id == usuario_id), None)

    def editar_perfil(self, usuario_id, nome=None, email=None, telefone=None, endereco=None, nova_senha=None):
        u = self.buscar_usuario(usuario_id)
        if u:
            u.editar_perfil(nome, email, telefone, endereco, nova_senha)
            self._salvar_dados_seguro()
            return True
        return False

    # CRUD CLIENTE
    def cadastrar_cliente(self, nome, email, telefone="", endereco=""):
        c = Cliente(self.next_cliente_id, nome, email, telefone, endereco)
        self.clientes.append(c)
        self.next_cliente_id += 1
        self._salvar_dados_seguro()
        return c

    def buscar_cliente(self, cliente_id):
        return next((c for c in self.clientes if c.id == cliente_id), None)

    # CRUD PRODUTO
    def cadastrar_produto(self, nome, categoria, preco, estoque, imagem=None):
        p = Produto(self.next_produto_id, nome, categoria, preco, estoque, imagem)
        self.estoque.adicionar(p)
        self.next_produto_id += 1
        self._salvar_dados_seguro()
        return p

    def buscar_produto(self, produto_id):
        return next((p for p in self.estoque.produtos if p.id == produto_id), None)

    def editar_produto(self, produto_id, novo_nome=None, nova_categoria=None, novo_preco=None, novo_estoque=None, nova_imagem=None):
        p = self.buscar_produto(produto_id)
        if not p:
            return False
        if novo_nome:
            p.nome = novo_nome
        if nova_categoria:
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
        self._salvar_dados_seguro()
        return True

    def remover_produto(self, produto_id):
        if self.estoque.remover(produto_id):
            self._salvar_dados_seguro()
            return True
        return False

    # FAVORITOS
    def _atualizar_favoritos(self, usuario_id, produto_id, acao="adicionar"):
        u = self.buscar_usuario(usuario_id)
        if not u:
            return False
        if acao == "adicionar":
            u.adicionar_favorito(produto_id)
        elif acao == "remover":
            u.remover_favorito(produto_id)
        self._salvar_dados_seguro()
        return True

    def adicionar_favorito(self, usuario_id, produto_id):
        return self._atualizar_favoritos(usuario_id, produto_id, "adicionar")

    def remover_favorito(self, usuario_id, produto_id):
        return self._atualizar_favoritos(usuario_id, produto_id, "remover")

    def favoritar(self, usuario_id, produto_id):  # Alias
        return self.adicionar_favorito(usuario_id, produto_id)

    def tem_favorito(self, usuario_id, produto_id):
        u = self.buscar_usuario(usuario_id)
        return u.tem_favorito(produto_id) if u else False

    def get_favoritos_do_usuario(self, usuario_id):
        u = self.buscar_usuario(usuario_id)
        return u.favoritos.listar() if u else []

    def listar_produtos_favoritos(self, usuario_id):
        return [self.buscar_produto(pid) for pid in self.get_favoritos_do_usuario(usuario_id) if self.buscar_produto(pid)]

    # VENDEDOR
    def cadastrar_produto_para_vendedor(self, vendedor_id, dados_produto):
        vendedor = self.buscar_usuario(vendedor_id)
        if not vendedor or getattr(vendedor, 'papel', None) != 'vendedor':
            return None
        p = Produto(self.next_produto_id, dados_produto.get('nome'), dados_produto.get('categoria'), dados_produto.get('preco'), dados_produto.get('estoque', 1), dados_produto.get('imagem'), dados_produto.get('descricao', ''), vendedor_id)
        self.estoque.adicionar(p)
        if not hasattr(vendedor, 'produtos_do_vendedor'):
            vendedor.produtos_do_vendedor = []
        vendedor.produtos_do_vendedor.append(p.id)
        self.next_produto_id += 1
        self._salvar_dados_seguro()
        return p

    def listar_produtos_do_vendedor(self, vendedor_id):
        return [p for p in self.estoque.todos() if getattr(p, 'id_do_vendedor', None) == vendedor_id]

    # ESTATISTICAS E RELATORIOS
    def gerar_estatisticas(self, vendedor_id):
        total_vendas = 0
        total_faturamento = 0.0
        produtos_mais_vendidos = {}
        for pedido in self.pedidos:
            for item in pedido.itens:
                prod = item.produto
                if getattr(prod, 'id_do_vendedor', None) == vendedor_id:
                    total_vendas += item.quantidade
                    total_faturamento += item.subtotal()
                    produtos_mais_vendidos[prod.nome] = produtos_mais_vendidos.get(prod.nome, 0) + item.quantidade
        return {'total_vendas': total_vendas, 'total_faturamento': round(total_faturamento, 2), 'produtos_mais_vendidos': produtos_mais_vendidos}

    def gerar_relatorio(self, vendedor_id, periodo='mes'):
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
                    if periodo == 'dia' and data.date() != now.date():
                        continue
                    if periodo == 'mes' and (data.year != now.year or data.month != now.month):
                        continue
                    if periodo == 'ano' and data.year != now.year:
                        continue
                vendas.append({'nome_produto': prod.nome, 'quantidade': item.quantidade, 'preco': item.preco_unitario, 'total': round(item.subtotal(), 2), 'data_pedido': data.strftime('%d/%m/%Y %H:%M') if data else 'N/A'})
        return vendas

    def obter_pedidos_do_vendedor(self, vendedor_id):
        """Retorna lista de pedidos contendo ao menos um item do vendedor."""
        resultado = []
        for ped in self.pedidos:
            for it in getattr(ped, 'itens', []):
                if getattr(getattr(it, 'produto', None), 'id_do_vendedor', None) == vendedor_id:
                    resultado.append(ped)
                    break
        return resultado

    def exportar_relatorio_pdf(self, vendedor_id, periodo='mes', caminho=None):
        """Exporta relatório em PDF para o vendedor.

        Se `caminho` for None, salva em `relatorios/relatorio_<vendedor>_<ts>.pdf`.
        Retorna caminho salvo ou None em caso de falha.
        """
        from datetime import datetime
        pedidos = self.obter_pedidos_do_vendedor(vendedor_id)
        if not pedidos:
            return None
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        if not caminho:
            caminho = os.path.join('relatorios', f'relatorio_{vendedor_id}_{periodo}_{ts}.pdf')
        return self.rel.gerar_pdf(pedidos, caminho, titulo=f'Relatório {periodo}', vendedor_id=vendedor_id)

    def exportar_relatorio_excel(self, vendedor_id, periodo='mes', caminho=None):
        """Exporta relatório em Excel (xlsx) para o vendedor.

        Se `caminho` for None, salva em `relatorios/relatorio_<vendedor>_<ts>.xlsx`.
        Retorna caminho salvo ou None em caso de falha.
        """
        from datetime import datetime
        pedidos = self.obter_pedidos_do_vendedor(vendedor_id)
        if not pedidos:
            return None
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        if not caminho:
            caminho = os.path.join('relatorios', f'relatorio_{vendedor_id}_{periodo}_{ts}.xlsx')
        return self.rel.gerar_excel(pedidos, caminho, titulo=f'Relatório {periodo}', vendedor_id=vendedor_id)

    # CARRINHO E PEDIDOS
    def adicionar_ao_carrinho(self, nome_produto, quantidade):
        p = self.estoque.procurar(nome_produto)
        if p and p.estoque >= quantidade:
            self.carrinho.adicionar(p, quantidade)
            return True
        return False

    def fechar_pedido(self, cliente_id=None):
        cliente = self.buscar_cliente(cliente_id) if cliente_id else None
        total = self.carrinho.total()
        if not self.pag.processar(total):
            return None
        for item in self.carrinho.itens:
            item.produto.baixar_estoque(item.quantidade)
        pedido = Pedido(self.next_pedido_id, self.carrinho.itens.copy(), cliente)
        self.pedidos.append(pedido)
        self.next_pedido_id += 1
        self._salvar_dados_seguro()
        self.carrinho.limpar()
        return pedido

    # PERSISTENCIA
    def salvar_dados(self):
        """Salva estado completo em JSON."""
        data = {
            "next_produto_id": self.next_produto_id,
            "next_pedido_id": self.next_pedido_id,
            "next_cliente_id": self.next_cliente_id,
            "next_usuario_id": self.next_usuario_id,
            "usuarios": [],
            "produtos": [],
            "clientes": [],
            "pedidos": []
        }
        
        def safe_serialize(obj, default_dict):
            try:
                return obj.to_dict() if hasattr(obj, 'to_dict') else default_dict
            except:
                return default_dict

        for u in self.usuarios:
            try:
                data['usuarios'].append(safe_serialize(u, {'id': u.id, 'nome': getattr(u, 'nome', None), 'email': getattr(u, 'email', None), 'senha': getattr(u, 'senha', None), 'telefone': getattr(u, 'telefone', None), 'endereco': getattr(u, 'endereco', None), 'papel': getattr(u, 'papel', None)}))
            except:
                pass

        for p in self.estoque.produtos:
            try:
                data['produtos'].append(safe_serialize(p, {'id': p.id, 'nome': getattr(p, 'nome', None), 'categoria': getattr(p, 'categoria', None), 'preco': getattr(p, 'preco', None), 'estoque': getattr(p, 'estoque', None), 'imagem': getattr(p, 'imagem', None), 'descricao': getattr(p, 'descricao', None), 'id_do_vendedor': getattr(p, 'id_do_vendedor', None)}))
            except:
                pass

        for c in self.clientes:
            try:
                data['clientes'].append(safe_serialize(c, {'id': c.id, 'nome': getattr(c, 'nome', None), 'email': getattr(c, 'email', None), 'telefone': getattr(c, 'telefone', None), 'endereco': getattr(c, 'endereco', None)}))
            except:
                pass

        for ped in self.pedidos:
            try:
                ped_dict = {'id': ped.id, 'cliente': ped.cliente.id if ped.cliente else None, 'data': getattr(ped, 'data', None).strftime('%d/%m/%Y %H:%M') if getattr(ped, 'data', None) else None, 'itens': []}
                for it in getattr(ped, 'itens', []):
                    try:
                        ped_dict['itens'].append({'produto_id': it.produto.id if getattr(it.produto, 'id', None) else None, 'quantidade': it.quantidade, 'preco_unitario': getattr(it, 'preco_unitario', None)})
                    except:
                        pass
                data['pedidos'].append(ped_dict)
            except:
                pass

        try:
            with open(self.ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
        return True

    def carregar_dados(self):
        """Carrega dados EXCLUSIVAMENTE do JSON."""
        self.estoque = Estoque()
        self.pedidos = []
        self.clientes = []
        self.usuarios = []

        if not os.path.exists(self.ARQUIVO_DADOS):
            return None
        
        try:
            with open(self.ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return None
                data = json.loads(content)
        except:
            return None

        # Atualizar IDs
        self.next_produto_id = int(data.get("next_produto_id", 1))
        self.next_pedido_id = int(data.get("next_pedido_id", 1))
        self.next_cliente_id = int(data.get("next_cliente_id", 1))
        self.next_usuario_id = int(data.get("next_usuario_id", 1))

        # HELPER: Resolver ID de produto de diferentes formatos
        def _resolve_produto_id(ref):
            if isinstance(ref, dict):
                return ref.get('produto_id') or ref.get('id_produto') or ref.get('id') or ref.get('produto')
            try:
                return int(ref) if isinstance(ref, (int, float)) or (isinstance(ref, str) and ref.isdigit()) else None
            except:
                return None

        # 1. Carregar produtos
        for p_data in data.get('produtos', []):
            try:
                prod = Produto.from_dict(p_data) if hasattr(Produto, 'from_dict') else Produto(p_data.get('id'), p_data.get('nome'), p_data.get('categoria'), p_data.get('preco', 0), p_data.get('estoque', 0), p_data.get('imagem'), p_data.get('descricao', ''), p_data.get('id_do_vendedor'))
                self.estoque.adicionar(prod)
            except:
                pass

        # 2. Carregar usuários
        for u_data in data.get('usuarios', []):
            try:
                papel = u_data.get('papel', '')
                user = Vendedor.from_dict(u_data) if papel == 'vendedor' and hasattr(Vendedor, 'from_dict') else Vendedor(u_data.get('id'), u_data.get('nome'), u_data.get('email'), u_data.get('senha', ''), u_data.get('telefone', ''), u_data.get('endereco', ''), u_data.get('cpf', ''), u_data.get('nome_loja', '')) if papel == 'vendedor' else Usuario(u_data.get('id'), u_data.get('nome'), u_data.get('email'), u_data.get('senha', ''), u_data.get('telefone', ''), u_data.get('endereco', ''), papel)
                self.usuarios.append(user)
            except:
                pass

        # 3. Vincular produtos aos vendedores
        for v in [u for u in self.usuarios if getattr(u, 'papel', None) == 'vendedor']:
            if not hasattr(v, 'produtos_do_vendedor'):
                v.produtos_do_vendedor = []
            for p in self.estoque.produtos:
                if getattr(p, 'id_do_vendedor', None) == v.id and p.id not in v.produtos_do_vendedor:
                    v.produtos_do_vendedor.append(p.id)

        # 4. Carregar clientes
        for c_data in data.get('clientes', []):
            try:
                cliente = Cliente.from_dict(c_data) if hasattr(Cliente, 'from_dict') else Cliente(c_data.get('id'), c_data.get('nome'), c_data.get('email'), c_data.get('telefone', ''), c_data.get('endereco', ''))
                self.clientes.append(cliente)
            except:
                pass

        # 5. Carregar pedidos
        for ped_data in data.get('pedidos', []):
            try:
                pid = ped_data.get('id')
                cliente_id = ped_data.get('cliente')
                cliente_obj = self.buscar_cliente(cliente_id) if isinstance(cliente_id, int) else None
                
                itens_list = []
                for it in ped_data.get('itens', []):
                    try:
                        prod_id = _resolve_produto_id(it) if not isinstance(it, dict) else _resolve_produto_id(it)
                        produto_obj = self.buscar_produto(prod_id) if prod_id else None
                        if not produto_obj:
                            continue
                        quantidade = int(it.get('quantidade', 1)) if isinstance(it, dict) else 1
                        preco_unitario = float(it.get('preco_unitario', 0)) if isinstance(it, dict) and it.get('preco_unitario') else None
                        
                        item_obj = ItemPedido(produto_obj, quantidade)
                        if preco_unitario:
                            item_obj._preco_unitario = preco_unitario
                        itens_list.append(item_obj)
                    except:
                        pass
                
                pedido_obj = Pedido(pid, itens_list, cliente_obj)
                self.pedidos.append(pedido_obj)
            except:
                pass

        return None
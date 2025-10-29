class Estoque:
    def __init__(self):
        self.produtos = {}

    def adicionar_produto(self, produto):
        self.produtos[produto.id_produto] = produto

    def remover_produto(self, id_produto):
        if id_produto in self.produtos:
            del self.produtos[id_produto]

    def listar_estoque(self):
        for produto in self.produtos.values():
            print(produto)

    def buscar_produto(self, termo):
        #Busca produtos no estoque por nome.
        termo = termo.lower()
        return [p for p in self.produtos.values() if termo in p.nome.lower()]
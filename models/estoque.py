class Estoque:
    def __init__(self):
        self.produtos = []

    def adicionar(self, produto):
        self.produtos.append(produto)

    def procurar(self, nome):
        for p in self.produtos:
            if p.nome.lower() == nome.lower():
                return p
        return None

    def todos(self):
        return self.produtos

    def remover(self, produto_id):
        for p in list(self.produtos):
            if p.id == produto_id:
                self.produtos.remove(p)
                return True
        return False
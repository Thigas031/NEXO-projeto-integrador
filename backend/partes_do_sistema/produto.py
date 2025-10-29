class Produto:
    def __init__(self, id_produto, nome, preco, quantidade_estoque, categoria):
        self.id_produto = id_produto
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.categoria = categoria

    def atualizar_estoque(self, quantidade):
        self.quantidade_estoque += quantidade

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} ({self.quantidade_estoque} disponíveis)"

    @staticmethod
    def pesquisar_por_nome(lista_produtos, termo):
        #Pesquisa produtos por nome ou parte do nome (case insensitive).
        termo = termo.lower()
        resultados = [p for p in lista_produtos if termo in p.nome.lower()]
        return resultados
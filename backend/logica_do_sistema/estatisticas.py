import database_config  # integração futura com o banco de dados
class Estatisticas:
    def __init__(self, loja):
        self.loja = loja 

    def produtos_mais_vendidos(self):
        #Retorna uma lista dos produtos mais vendidos com base nos pedidos.
        contagem = {}
        for pedido in self.loja.pedidos:
            for item in pedido.itens:
                nome = item.produto.nome
                contagem[nome] = contagem.get(nome, 0) + item.quantidade
        return sorted(contagem.items(), key=lambda x: x[1], reverse=True)

    def total_vendas(self):
        #Soma o valor total de todas as vendas realizadas.
        total = 0
        for pedido in self.loja.pedidos:
            total += pedido.calcular_total()
        return total

    def vendas_por_vendedor(self):
        #Mostra quanto cada vendedor vendeu.
        vendas = {}
        for pedido in self.loja.pedidos:
            vendedor = pedido.vendedor.nome if hasattr(pedido, 'vendedor') else 'Desconhecido'
            vendas[vendedor] = vendas.get(vendedor, 0) + pedido.calcular_total()
        return vendas

    def estoque_atual(self):
        #Retorna a quantidade atual de cada produto no estoque.
        situacao = {}
        for produto in self.loja.estoque.produtos:
            situacao[produto.nome] = produto.quantidade
        return situacao

    def produtos_em_baixo_estoque(self, limite=5):
        #Mostra produtos com estoque abaixo do limite informado.
        return [p.nome for p in self.loja.estoque.produtos if p.quantidade <= limite]
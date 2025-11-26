class Estatisticas:
    def produtos_mais_vendidos(self, pedidos):
        contagem = {}
        for p in pedidos:
            for i in p.itens:
                if i.produto.nome not in contagem:
                    contagem[i.produto.nome] = 0
                contagem[i.produto.nome] += i.quantidade
        lista = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
        return lista
"""Análise e cálculo de estatísticas."""


class Estatisticas:
    """Calcula estatísticas de vendas."""

    def produtos_mais_vendidos(self, pedidos, limite=10):
        """Retorna lista de (nome, quantidade) dos mais vendidos."""
        contagem = {}
        for p in pedidos:
            for i in getattr(p, 'itens', []):
                try:
                    nome = getattr(i.produto, 'nome', 'Desconhecido') if hasattr(i, 'produto') else 'Desconhecido'
                    qtd = getattr(i, 'quantidade', 0)
                    contagem[nome] = contagem.get(nome, 0) + qtd
                except:
                    pass
        return sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:limite]

    def total_faturamento(self, pedidos):
        """Calcula faturamento total."""
        total = 0.0
        for p in pedidos:
            if hasattr(p, 'total') and callable(p.total):
                try:
                    total += p.total()
                except:
                    pass
        return round(total, 2)

    def total_vendas(self, pedidos):
        """Conta total de itens vendidos."""
        return sum(len(getattr(p, 'itens', [])) for p in pedidos)

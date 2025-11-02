import database_config  # integração futura com o banco de dados
from datetime import datetime

class Relatorio:
    def __init__(self, loja):
        self.loja = loja

    def produtos_mais_vendidos(self):
        contagem = {}
        for pedido in self.loja.pedidos:
            for item in pedido.itens:
                nome = item.produto.nome
                contagem[nome] = contagem.get(nome, 0) + item.quantidade
        return sorted(contagem.items(), key=lambda x: x[1], reverse=True)

    def relatorio_vendas(self):
        total_vendas = 0
        total_itens = 0
        for pedido in self.loja.pedidos:
            for item in pedido.itens:
                total_vendas += item.subtotal
                total_itens += item.quantidade
        return {
            "total_pedidos": len(self.loja.pedidos),
            "total_itens": total_itens,
            "total_vendas": round(total_vendas, 2),
        }

    def gerar_relatorio_texto(self):
        dados = self.relatorio_vendas()
        mais_vendidos = self.produtos_mais_vendidos()

        relatorio = []
        relatorio.append("=== RELATÓRIO DE VENDAS ===")
        relatorio.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        relatorio.append(f"Total de pedidos: {dados['total_pedidos']}")
        relatorio.append(f"Total de itens vendidos: {dados['total_itens']}")
        relatorio.append(f"Total arrecadado: R$ {dados['total_vendas']:.2f}")
        relatorio.append("\n--- Produtos mais vendidos ---")
        for nome, qtd in mais_vendidos:
            relatorio.append(f"{nome} - {qtd} unidades")

        return "\n".join(relatorio)
"""Geração de relatórios em PDF e Excel.

Funções aceitam lista de objetos `Pedido` e permitem filtrar
por `vendedor_id` (opcional). O arquivo de saída é criado em
`caminho` informado — o diretório será criado automaticamente.
"""
from reportlab.pdfgen import canvas
from openpyxl import Workbook
import os
from datetime import datetime


class Relatorios:
    """Gera relatórios em PDF e Excel com filtros por vendedor."""

    def _ensure_dir(self, caminho):
        d = os.path.dirname(os.path.abspath(caminho))
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

    def _iterar_itens_filtrados(self, pedido, vendedor_id=None):
        for it in getattr(pedido, 'itens', []):
            prod = getattr(it, 'produto', None)
            if vendedor_id is None or getattr(prod, 'id_do_vendedor', None) == vendedor_id:
                yield it

    def gerar_pdf(self, pedidos, caminho, titulo="Relatório de Vendas", vendedor_id=None):
        """Gera um PDF detalhado. Filtra itens por `vendedor_id` quando fornecido.

        Retorna o caminho salvo em caso de sucesso, ou None em caso de erro.
        """
        try:
            self._ensure_dir(caminho)
            c = canvas.Canvas(caminho)
            y = 800
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, titulo)
            y -= 30

            for p in pedidos:
                # calcular subtotal apenas para itens do vendedor
                itens = list(self._iterar_itens_filtrados(p, vendedor_id))
                if not itens:
                    continue
                pedido_total = sum(getattr(it, 'subtotal', lambda: 0)() for it in itens)
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y, f"Pedido {getattr(p, 'id', 'N/A')} - Total: R$ {pedido_total:.2f}")
                y -= 18
                c.setFont("Helvetica", 10)
                for it in itens:
                    nome = getattr(getattr(it, 'produto', None), 'nome', 'Desconhecido')
                    qtd = getattr(it, 'quantidade', 0)
                    preco = getattr(it, 'preco_unitario', getattr(getattr(it, 'produto', None), 'preco', 0.0))
                    linha = f" - {nome} | {qtd} un. x R$ {preco:.2f} = R$ {qtd * preco:.2f}"
                    c.drawString(60, y, linha)
                    y -= 14
                    if y < 60:
                        c.showPage()
                        y = 800
                # separar pedidos
                y -= 8
                if y < 80:
                    c.showPage()
                    y = 800

            c.save()
            return caminho
        except Exception as e:
            return None

    def gerar_excel(self, pedidos, caminho, titulo="Relatório de Vendas", vendedor_id=None):
        """Gera um arquivo Excel (xlsx) com uma linha por item filtrado.

        Retorna o caminho salvo em caso de sucesso, ou None em caso de erro.
        """
        try:
            self._ensure_dir(caminho)
            wb = Workbook()
            ws = wb.active
            ws.title = "Vendas"
            ws.append(["ID Pedido", "Produto", "Quantidade", "Preço Unit.", "Subtotal", "Cliente", "Data"])

            for p in pedidos:
                data = getattr(p, 'data', None)
                data_str = data.strftime("%d/%m/%Y %H:%M") if getattr(data, 'strftime', None) else str(data or "N/A")
                cliente_nome = getattr(getattr(p, 'cliente', None), 'nome', "Não informado")
                pid = getattr(p, 'id', None)
                for it in self._iterar_itens_filtrados(p, vendedor_id):
                    nome = getattr(getattr(it, 'produto', None), 'nome', 'Desconhecido')
                    qtd = getattr(it, 'quantidade', 0)
                    preco = getattr(it, 'preco_unitario', getattr(getattr(it, 'produto', None), 'preco', 0.0))
                    subtotal = round(qtd * preco, 2)
                    ws.append([pid, nome, qtd, float(preco), float(subtotal), cliente_nome, data_str])

            wb.save(caminho)
            return caminho
        except Exception:
            return None

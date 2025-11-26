from reportlab.pdfgen import canvas
from openpyxl import Workbook

class Relatorios:
    def gerar_pdf(self, pedidos, caminho):
        c = canvas.Canvas(caminho)
        y = 800
        c.drawString(50, y, "Relatório de Vendas")
        y -= 40
        for p in pedidos:
            c.drawString(50, y, f"Pedido {p.id} - Total: R$ {p.total()}")
            y -= 20
        c.save()

    def gerar_excel(self, pedidos, caminho):
        wb = Workbook()
        ws = wb.active
        ws.append(["ID", "Cliente", "Total", "Data"])
        for p in pedidos:
            ws.append([
                p.id,
                p.cliente.nome if p.cliente else "",
                p.total(),
                p.data.strftime("%d/%m/%Y %H:%M")
            ])
        wb.save(caminho)
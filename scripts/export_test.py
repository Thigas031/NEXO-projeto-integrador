from models.loja import Loja
import traceback, os

l = Loja()
print('Produtos:', len(l.estoque.produtos))
print('Pedidos:', len(l.pedidos))

def try_call(name):
    try:
        caminho = getattr(l, name)(1, 'mes')
        print(f'{name} -> OK -> {caminho}')
        if caminho:
            print('Arquivo existe?:', os.path.exists(caminho))
    except Exception as e:
        print(f'{name} -> ERRO')
        traceback.print_exc()

try_call('exportar_relatorio_pdf')
try_call('exportar_relatorio_excel')

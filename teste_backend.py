from models.loja import Loja

loja = Loja()

print("\n--- Testando cadastro de produtos ---")
p1 = loja.cadastrar_produto("Camiseta", "Roupas", 50, 20)
p2 = loja.cadastrar_produto("Boné", "Acessórios", 30, 10)
print(p1.to_dict())
print(p2.to_dict())

print("\n--- Testando cadastro de cliente ---")
c1 = loja.cadastrar_cliente("Thiago", "1199999-0000")
print(c1.to_dict())

print("\n--- Testando cadastro de usuário ---")
u1 = loja.cadastrar_usuario("vendedor1", "123")
print(u1.to_dict())

print("\n--- Testando favoritar produto ---")
loja.favoritar(u1.id, p1.id)
print(u1.to_dict())

print("\n--- Testando adicionar ao carrinho ---")
loja.adicionar_ao_carrinho("Camiseta", 2)
loja.adicionar_ao_carrinho("Boné", 1)
print("Total do carrinho:", loja.carrinho.total())

print("\n--- Testando fechar pedido ---")
pedido = loja.fechar_pedido(cliente_id=c1.id)
print(pedido.to_dict())

print("\n--- Testando estatísticas ---")
print(loja.est.produtos_mais_vendidos(loja.pedidos))
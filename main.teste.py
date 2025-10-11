from partes_do_sistema.usuario_base import UsuarioBase
from partes_do_sistema.cliente import Cliente
from partes_do_sistema.vendedor import Vendedor
from partes_do_sistema.produto import Produto
from logica_do_sistema.estoque import Estoque


def linha():
    print("-" * 60)


def exibir_menu_principal():
    print("\n===== MENU PRINCIPAL =====")
    print("1. Cadastrar Cliente")
    print("2. Cadastrar Vendedor")
    print("3. Adicionar Produto")
    print("4. Listar Estoque")
    print("5. Buscar Produto")
    print("6. Adicionar Favorito (Cliente)")
    print("7. Listar Favoritos (Cliente)")
    print("8. Sair")
    print("===========================")


# ============================
# INÍCIO DO PROGRAMA
# ============================

if __name__ == "__main__":
    print("=== Bem-vindo ao Projeto Integrador (Criação de Classes) ===")

    # Instancia estoque geral da loja
    estoque = Estoque()

    # Listas para armazenar usuários e clientes (futuramente via MySQL)
    clientes = []
    vendedores = []

    # Exemplo inicial de produtos
    estoque.adicionar_produto(Produto(1, "Teclado Gamer", 250.0, 10, "Periféricos"))
    estoque.adicionar_produto(Produto(2, "Mouse Óptico", 80.0, 15, "Periféricos"))
    estoque.adicionar_produto(Produto(3, "Monitor 24''", 750.0, 5, "Monitores"))

    # Criação de um cliente padrão para testar favoritos
    cliente_teste = Cliente(1, "user_cliente", "cliente@email.com", "87999999999", "Rua A, 123", "1234")
    clientes.append(cliente_teste)

    # Criação de um vendedor padrão
    vendedor_teste = Vendedor(1, "user_vendedor", "vendedor@email.com", "87988887777", "Rua B, 45", "senha")
    vendedores.append(vendedor_teste)

    while True:
        linha()
        exibir_menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n=== Cadastro de Cliente ===")
            nome = input("Nome do cliente: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            senha = input("Senha: ")

            novo_cliente = Cliente(len(clientes) + 1, nome, email, telefone, endereco, senha)
            clientes.append(novo_cliente)
            print(f"✅ Cliente '{nome}' cadastrado com sucesso!")

        elif opcao == "2":
            print("\n=== Cadastro de Vendedor ===")
            nome = input("Nome do vendedor: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            senha = input("Senha: ")

            novo_vendedor = Vendedor(len(vendedores) + 1, nome, email, telefone, endereco, senha)
            vendedores.append(novo_vendedor)
            print(f"✅ Vendedor '{nome}' cadastrado com sucesso!")

            # Pergunta se possui loja
            novo_vendedor.cadastrar_loja()

        elif opcao == "3":
            print("\n=== Cadastro de Produto ===")
            id_produto = len(estoque.produtos) + 1
            nome = input("Nome do produto: ")
            preco = float(input("Preço: "))
            qtd = int(input("Quantidade em estoque: "))
            categoria = input("Categoria: ")

            novo_produto = Produto(id_produto, nome, preco, qtd, categoria)
            estoque.adicionar_produto(novo_produto)
            print(f"✅ Produto '{nome}' adicionado ao estoque!")

        elif opcao == "4":
            print("\n=== Produtos em Estoque ===")
            estoque.listar_estoque()

        elif opcao == "5":
            termo = input("\nDigite o nome do produto para buscar: ")
            resultados = estoque.buscar_produto(termo)
            if resultados:
                print(f"\n🔍 Resultados para '{termo}':")
                for p in resultados:
                    print(f" - {p}")
            else:
                print("Nenhum produto encontrado com esse nome.")

        elif opcao == "6":
            print("\n=== Adicionar Favorito ===")
            cliente_teste.listar_favoritos()
            termo = input("Digite o nome do produto a favoritar: ")
            resultados = estoque.buscar_produto(termo)
            if resultados:
                produto = resultados[0]
                cliente_teste.adicionar_favorito(produto)
            else:
                print("Produto não encontrado.")

        elif opcao == "7":
            print("\n=== Favoritos do Cliente ===")
            cliente_teste.listar_favoritos()

        elif opcao == "8":
            print("\nEncerrando o sistema. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")
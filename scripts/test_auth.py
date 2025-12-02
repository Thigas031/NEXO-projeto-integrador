from models.loja import Loja

l = Loja()
print('Usuários carregados:', [u.nome for u in l.usuarios])

for nome, senha in [('admV', 'admV123'), ('admc', 'admc123')]:
    u = l.autenticar_usuario(nome, senha)
    print(f"Login {nome} com senha '{senha}':", 'OK' if u else 'FALHOU', '-> id=' + str(u.id) if u else '')

# Salvar e recarregar para garantir persistência
l._salvar_dados_seguro()
print('Salvo. Recarregando...')

l2 = Loja()
for nome, senha in [('admV', 'admV123'), ('admc', 'admc123')]:
    u = l2.autenticar_usuario(nome, senha)
    print(f"Após reload: Login {nome} com senha '{senha}':", 'OK' if u else 'FALHOU')

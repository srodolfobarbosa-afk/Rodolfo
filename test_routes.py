from app import create_app

app = create_app()

print('App criado com sucesso')
print('Rotas registradas:')
for rule in app.url_map.iter_rules():
    print(f'  {rule.rule} -> {rule.endpoint}')

# Testar uma rota específica
with app.test_client() as client:
    response = client.get('/api/market-intelligence')
    print(f'\nTeste da rota /api/market-intelligence:')
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        print(f'Resposta: {response.get_json()}')
    else:
        print(f'Erro: {response.data.decode()}')


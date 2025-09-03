from flask import Flask
from flask_cors import CORS
from app.proactive.routes import proactive_bp

# Criar app simples para teste
app = Flask(__name__)
CORS(app)

# Registrar apenas o blueprint proativo
app.register_blueprint(proactive_bp, url_prefix="/api")

@app.route("/")
def index():
    return "Teste local funcionando!"

print('App de teste criado com sucesso')
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


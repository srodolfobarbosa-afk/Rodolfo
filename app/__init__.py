from flask import Flask, send_from_directory
from flask_cors import CORS
import os

def create_app():
    # A linha abaixo foi alterada para incluir o 'static_folder'
    app = Flask(__name__, static_folder='static', static_url_path='/')
    CORS(app) # Habilitar CORS para todas as rotas
    
    # Configurações do aplicativo
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

    # Importar e registrar Blueprints
    from app.agents.routes import agents_bp
    from app.chat.routes import chat_bp
    from app.auth.routes import auth_bp
    from app.proactive.routes import proactive_bp

    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(agents_bp, url_prefix='/api/agents')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(proactive_bp, url_prefix='/api/proactive')

    # Rota para servir o frontend React (index.html)
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    # Rota catch-all para o React Router
    @app.errorhandler(404)
    def not_found(e):
        # A nova lógica abaixo tenta servir o index.html caso a rota não seja da API
        if not str(e).startswith("404 Not Found: /api/"):
            return send_from_directory(app.static_folder, 'index.html'), 200
        # Caso contrário, retorne o erro 404 padrão
        return e

    # Rota de ping para verificar o status do servidor
    @app.route('/api/ping', methods=['GET'])
    def ping():
        return 'pong', 200

    return app

# Adicione esta linha no final do arquivo:
app = create_app()
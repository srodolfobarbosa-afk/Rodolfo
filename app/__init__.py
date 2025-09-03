from flask import Flask, send_from_directory
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    CORS(app)  # Habilitar CORS para todas as rotas

    # Configurações do aplicativo
    app.config["SECRET_KEY"] = "sua_chave_secreta_aqui"

    # Importar e registrar Blueprints
    from app.chat.routes import chat_bp
    from app.agents.routes import agents_bp
    from app.auth.routes import auth_bp
    from app.proactive.routes import proactive_bp

    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(agents_bp, url_prefix="/api/agents")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(proactive_bp, url_prefix="/api")

    # Rota para servir o frontend React
    @app.route("/")
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')

    # Rota para servir arquivos estáticos do React
    @app.route("/<path:path>")
    def serve_static_files(path):
        try:
            return send_from_directory(app.static_folder, path)
        except:
            # Se o arquivo não for encontrado, serve o index.html (para React Router)
            return send_from_directory(app.static_folder, 'index.html')

    # Rota de ping para verificar o status do servidor
    @app.route("/api/ping", methods=["GET"])
    def ping():
        return "pong", 200

    return app

# Adicione esta linha no final do arquivo:
app = create_app()



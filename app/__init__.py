from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilitar CORS para todas as rotas

    # Configurações do aplicativo
    app.config["SECRET_KEY"] = "sua_chave_secreta_aqui"

    socketio.init_app(app)

    # Importar e registrar Blueprints
    from app.chat.routes import chat_bp
    from app.agents.routes import agents_bp
    from app.auth.routes import auth_bp
    from app.proactive.routes import proactive_bp

    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(agents_bp, url_prefix="/api/agents")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(proactive_bp, url_prefix="/api")

    # Adicione esta nova rota para a página inicial
    @app.route("/")
    def index():
        return "Olá, sua aplicação está no ar!"

    # Rota de ping para verificar o status do servidor
    @app.route("/api/ping", methods=["GET"])
    def ping():
        return "pong", 200

    return app

# Adicione esta linha no final do arquivo:
app = create_app()



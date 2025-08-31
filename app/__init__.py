from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    CORS(app) # Habilitar CORS para todas as rotas

    # Configurações do aplicativo (se houver)
    app.config["SECRET_KEY"] = "sua_chave_secreta_aqui" # Substitua por uma chave secreta real

    socketio.init_app(app)

    # Importar e registrar Blueprints
    from app.chat.routes import chat_bp
    from app.agents.routes import agents_bp
    from app.auth.routes import auth_bp

    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(agents_bp, url_prefix="/api/agents")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Rota de ping para verificar o status do servidor
    @app.route("/api/ping", methods=["GET"])
    def ping():
        return "pong", 200

    return app



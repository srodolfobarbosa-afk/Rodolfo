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

    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(agents_bp, url_prefix="/api/agents")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Adicione esta nova rota para a página inicial
    @app.route("/")
    def index():
        return "Olá, sua aplicação está no ar!"

    # Rota de ping para verificar o status do servidor
    @app.route("/api/ping", methods=["GET"])
    def ping():
        return "pong", 200

    # ROTAS PROATIVAS IMPLEMENTADAS
    from flask import jsonify
    
    # Inteligência de Mercado
    @app.route("/api/market-intelligence", methods=["GET"])
    def market_intelligence():
        return jsonify({
            "status": "success",
            "opportunities": [
                {"id": 1, "trend": "AI Agents in Finance", "roi_potential": "85%", "market_size": "$2.1B"},
                {"id": 2, "trend": "Decentralized AI Marketplaces", "roi_potential": "92%", "market_size": "$1.8B"},
                {"id": 3, "trend": "Autonomous Trading Systems", "roi_potential": "78%", "market_size": "$3.2B"}
            ],
            "total_opportunities": 47,
            "last_updated": "2025-02-09T23:45:00Z"
        })

    # Performance dos Agentes
    @app.route("/api/agent-performance", methods=["GET"])
    def agent_performance():
        return jsonify({
            "status": "success",
            "agents": [
                {"name": "Nexo Gênesis", "performance": 95.2, "status": "active"},
                {"name": "EcoFinance", "performance": 89.7, "status": "active"},
                {"name": "EcoSofia", "performance": 91.3, "status": "active"},
                {"name": "Eco-Explorer", "performance": 87.8, "status": "active"},
                {"name": "Eco-Writer", "performance": 88.5, "status": "active"}
            ],
            "average_performance": 90.5
        })

    # Tokenomics
    @app.route("/api/tokenomics/info", methods=["GET"])
    def tokenomics_info():
        return jsonify({
            "status": "success",
            "token_name": "EcoGuardians Token",
            "token_symbol": "ECG",
            "total_supply": 1000000000,
            "circulating_supply": 490000000,
            "burned_tokens": 10000000,
            "current_price_usd": 0.0012,
            "blockchain": "Binance Smart Chain (BSC)"
        })

    # Dashboard KPIs
    @app.route("/api/dashboard/kpis", methods=["GET"])
    def dashboard_kpis():
        return jsonify({
            "status": "success",
            "kpis": {
                "autonomia_operacional": {"value": 98.5, "unit": "%", "status": "green"},
                "receita_gerada": {"value": 150000, "unit": "USD", "status": "green"},
                "eficiencia_operacional": {"value": 0.85, "unit": "$/tarefa", "status": "green"},
                "novos_agentes_mes": {"value": 3, "unit": "agentes", "status": "green"},
                "retencao_clientes": {"value": 92, "unit": "%", "status": "green"}
            }
        })

    # Marketplace de Agentes
    @app.route("/api/marketplace/agents", methods=["GET"])
    def marketplace_agents():
        return jsonify({
            "status": "success",
            "agents": [
                {"id": 1, "name": "Agente de Vendas AI", "price": 100.0, "status": "approved"},
                {"id": 2, "name": "Agente de Suporte", "price": 50.0, "status": "approved"},
                {"id": 3, "name": "Agente de Marketing", "price": 75.0, "status": "pending_review"}
            ]
        })

    return app

# Adicione esta linha no final do arquivo:
app = create_app()



from flask import Blueprint, render_template_string, jsonify, request
from flask_socketio import emit
import os
from app import socketio

chat_bp = Blueprint("chat", __name__)

# ... (o conteúdo de HTML_TEMPLATE, CSS_TEMPLATE, e JS_TEMPLATE permanece o mesmo)
HTML_TEMPLATE = ''
CSS_TEMPLATE = ''
JS_TEMPLATE = ''

# Eventos SocketIO
@socketio.on("user_message")
def handle_message(data):
    user_message = data["message"]
    agent_id = data["agent_id"]

    # Resposta simples para teste
    agent_response = f"Olá! Sou o agente {agent_id}. Recebi sua mensagem: '{user_message}'. Como posso ajudá-lo com questões ambientais?"

    # Enviar resposta
    socketio.emit("agent_response", {"message": agent_response})

# Rotas da API
@chat_bp.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@chat_bp.route("/static/style.css")
def serve_css():
    return CSS_TEMPLATE, 200, {"Content-Type": "text/css"}

@chat_bp.route("/static/script.js")
def serve_js():
    return JS_TEMPLATE, 200, {"Content-Type": "application/javascript"}

@chat_bp.route("/send", methods=["POST"])
def send_message():
    try:
        data = request.get_json()
        user_message = data.get("message")
        agent_id = data.get("agent_id", "nexo_genesis")
        session_id = data.get("session_id", "default")

        if not user_message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400

        # Resposta simples baseada no agente selecionado
        agent_responses = {
            "nexo_genesis": f"Olá! Sou o Nexo Gênesis, o agente principal do EcoGuardians. Recebi sua mensagem: '{user_message}'. Como criador de outros agentes, posso ajudá-lo a encontrar soluções ambientais inovadoras!",
            "ecofinanceiro": f"Olá! Sou o EcoFinanceiro, especialista em finanças sustentáveis. Sobre sua pergunta: '{user_message}' - posso ajudá-lo com investimentos verdes, economia circular e sustentabilidade financeira!",
            "ecosofia": f"Olá! Sou a EcoSofia, especialista em sabedoria ecológica. Sua mensagem: '{user_message}' - me inspira a compartilhar conhecimentos sobre harmonia com a natureza e práticas sustentáveis!",
            "assistente_ecologico": f"Olá! Sou o Assistente Ecológico. Recebi sua mensagem: '{user_message}'. Estou aqui para ajudá-lo com questões ambientais gerais e práticas sustentáveis do dia a dia!"
        }

        agent_response = agent_responses.get(agent_id, f"Olá! Recebi sua mensagem: '{user_message}'. Como posso ajudá-lo com questões ambientais?")
        
        agent_names = {
            "nexo_genesis": "Nexo Gênesis",
            "ecofinanceiro": "EcoFinanceiro", 
            "ecosofia": "EcoSofia",
            "assistente_ecologico": "Assistente Ecológico"
        }

        return jsonify({
            "response": agent_response,
            "agent": agent_names.get(agent_id, "EcoGuardians Assistant"),
            "session_id": session_id
        })

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@chat_bp.route("/api/ping")
def ping():
    return jsonify({"status": "ok", "version": "3.2"})



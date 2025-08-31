from flask import Blueprint, render_template_string, jsonify, request
from flask_socketio import emit
from ia_router import ia_router
from supabase_client import supabase_manager
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

    # Buscar informações do agente no Supabase
    agent_info = supabase_manager.get_agent_by_id(agent_id)

    if agent_info:
        agent_name = agent_info["name"]
        system_prompt = agent_info["system_prompt"]

        # Gerar resposta com IA real
        agent_response = ia_router.generate_response(
            user_message,
            agent_name,
            system_prompt,
            provider_preference=os.getenv("NEXO_LLM_PROVIDER")  # Usar provedor preferencial
        )

        # Salvar no Supabase
        supabase_manager.save_message(agent_id, user_message, agent_response)

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

@chat_bp.route("/api/ping")
def ping():
    return jsonify({"status": "ok", "version": "3.2"})



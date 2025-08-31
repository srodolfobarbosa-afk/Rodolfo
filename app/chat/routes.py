from flask import Blueprint, request, jsonify
from flask_socketio import emit
from ia_router import ia_router
from supabase_client import supabase_manager
import os

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["GET"])
def chat_index():
    return "Chat Blueprint"

@chat_bp.route("/message", methods=["POST"])
def handle_http_message():
    data = request.get_json()
    user_message = data["message"]
    agent_id = data["agent_id"]

    agent_info = supabase_manager.get_agent_by_id(agent_id)

    if agent_info:
        agent_name = agent_info["name"]
        system_prompt = agent_info["system_prompt"]

        agent_response = ia_router.generate_response(
            user_message,
            agent_name,
            system_prompt,
            provider_preference=os.getenv("NEXO_LLM_PROVIDER")
        )

        supabase_manager.save_message(agent_id, user_message, agent_response)

        return jsonify({"message": agent_response})
    return jsonify({"error": "Agent not found"}), 404

# SocketIO event (ainda será tratado no app.py principal ou refatorado para cá)
# @socketio.on("user_message")
# def handle_socket_message(data):
#     user_message = data["message"]
#     agent_id = data["agent_id"]
#
#     agent_info = supabase_manager.get_agent_by_id(agent_id)
#
#     if agent_info:
#         agent_name = agent_info["name"]
#         system_prompt = agent_info["system_prompt"]
#
#         agent_response = ia_router.generate_response(
#             user_message,
#             agent_name,
#             system_prompt,
#             provider_preference=os.getenv("NEXO_LLM_PROVIDER")
#         )
#
#         supabase_manager.save_message(agent_id, user_message, agent_response)
#
#         emit("agent_response", {"message": agent_response})



from app import create_app, socketio
from flask import request, jsonify
from ia_router import ia_router
from supabase_client import supabase_manager
import os

app = create_app()

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

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)



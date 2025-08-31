from app import create_app, socketio
from flask import request, jsonify
from ia_router import ia_router
from supabase_client import supabase_manager
import os

app = create_app()

# Eventos SocketIO (movidos para app/chat/routes.py para melhor organização)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)



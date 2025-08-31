from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    # Lógica de login de usuário (placeholder)
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if username == "test" and password == "test": # Exemplo simples
        return jsonify({"message": "Login bem-sucedido", "token": "fake-token"})
    return jsonify({"message": "Credenciais inválidas"}), 401

@auth_bp.route("/register", methods=["POST"])
def register():
    # Lógica de registro de usuário (placeholder)
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        return jsonify({"message": "Usuário registrado com sucesso"})
    return jsonify({"message": "Dados inválidos"}), 400



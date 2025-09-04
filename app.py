import os
from flask import Flask, jsonify, render_template
from supabase import create_client, Client
from dotenv import load_dotenv

# 🔑 Carregar variáveis do .env (se existir)
load_dotenv()

app = Flask(__name__)

# 🔗 Configuração Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Conectado ao Supabase")
    except Exception as e:
        print("⚠️ Erro ao conectar Supabase:", e)
else:
    print("⚠️ Supabase não configurado. Verifique suas credenciais.")

# Rota de saúde
@app.route("/health")
def health():
    return jsonify({"ok": True})

# Página inicial (renderiza index.html em /templates)
@app.route("/")
def index():
    return render_template("index.html")

# API para listar tasks
@app.route("/api/tasks")
def list_tasks():
    if not supabase:
        return jsonify({"error": "Supabase não configurado"}), 500
    try:
        response = supabase.table("tasks").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
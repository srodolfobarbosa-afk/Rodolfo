from flask import Blueprint, render_template_string, jsonify, request
from flask_socketio import emit
from ia_router import ia_router
from supabase_client import supabase_manager
import os

chat_bp = Blueprint("chat", __name__)

# Template HTML atualizado com cache busting
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EcoGuardians v3.2</title>
    <link rel="stylesheet" href="/static/style.css?v=20250831">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌱 EcoGuardians v3.2</h1>
            <p>Sistema de Agentes Inteligentes</p>
        </header>
        
        <div class="main-content">
            <div class="agents-panel">
                <h3>Agentes Disponíveis</h3>
                <div id="agents-list"></div>
            </div>
            
            <div class="chat-panel">
                <div id="chat-messages"></div>
                <div class="input-area">
                    <input type="text" id="message-input" placeholder="Digite sua mensagem...">
                    <button onclick="sendMessage()">Enviar</button>
                </div>
                <div class="status">
                    <span id="connection-status">🟢 Online</span>
                    <span id="selected-agent">Agente: Nexo Gênesis</span>
                </div>
            </div>
        </div>
    </div>
    
    <script src="/static/script.js?v=20250831"></script>
</body>
</html>
'''

CSS_TEMPLATE = '''
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    margin-bottom: 30px;
    color: white;
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

.main-content {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 20px;
    height: 70vh;
}

.agents-panel, .chat-panel {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.agents-panel h3 {
    margin-bottom: 15px;
    color: #667eea;
}

.agent-item {
    padding: 10px;
    margin: 5px 0;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.agent-item:hover {
    background: #f0f8ff;
    border-color: #667eea;
}

.agent-item.selected {
    background: #667eea;
    color: white;
}

#chat-messages {
    height: 400px;
    overflow-y: auto;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    background: #f9f9f9;
}

.message {
    margin: 10px 0;
    padding: 10px;
    border-radius: 8px;
}

.user-message {
    background: #667eea;
    color: white;
    margin-left: 20%;
}

.agent-message {
    background: #e8f4f8;
    color: #333;
    margin-right: 20%;
}

.input-area {
    display: flex;
    gap: 10px;
}

#message-input {
    flex: 1;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
}

button {
    padding: 12px 20px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s ease;
}

button:hover {
    background: #5a6fd8;
}

.status {
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #666;
}

@media (max-width: 768px) {
    .main-content {
        grid-template-columns: 1fr;
        height: auto;
    }
    
    .agents-panel {
        order: 2;
    }
}
'''

JS_TEMPLATE = '''
const socket = io();
let selectedAgentId = 1;
let agents = [];

// Conectar ao servidor
socket.on('connect', function() {
    document.getElementById('connection-status').innerHTML = '🟢 Online';
    loadAgents();
});

socket.on('disconnect', function() {
    document.getElementById('connection-status').innerHTML = '🔴 Offline';
});

// Receber resposta do agente
socket.on('agent_response', function(data) {
    addMessage(data.message, 'agent');
});

// Carregar agentes
function loadAgents() {
    fetch('/api/agents')
        .then(response => response.json())
        .then(data => {
            agents = data;
            displayAgents();
        })
        .catch(error => {
            console.error('Erro ao carregar agentes:', error);
        });
}

// Exibir agentes
function displayAgents() {
    const agentsList = document.getElementById('agents-list');
    agentsList.innerHTML = '';
    
    agents.forEach(agent => {
        const agentDiv = document.createElement('div');
        agentDiv.className = 'agent-item';
        if (agent.id === selectedAgentId) {
            agentDiv.classList.add('selected');
        }
        
        agentDiv.innerHTML = `
            <strong>${agent.name}</strong>
            <br>
            <small>${agent.description}</small>
        `;
        
        agentDiv.onclick = () => selectAgent(agent.id, agent.name);
        agentsList.appendChild(agentDiv);
    });
}

// Selecionar agente
function selectAgent(agentId, agentName) {
    selectedAgentId = agentId;
    document.getElementById('selected-agent').textContent = `Agente: ${agentName}`;
    displayAgents();
}

// Enviar mensagem
function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, 'user');
        
        // Enviar via SocketIO
        socket.emit('user_message', {
            message: message,
            agent_id: selectedAgentId
        });
        
        input.value = '';
    }
}

// Adicionar mensagem ao chat
function addMessage(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = message;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Enter para enviar
document.getElementById('message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
'''

# Rotas da API
@chat_bp.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@chat_bp.route('/static/style.css')
def serve_css():
    return CSS_TEMPLATE, 200, {'Content-Type': 'text/css'}

@chat_bp.route('/static/script.js')
def serve_js():
    return JS_TEMPLATE, 200, {'Content-Type': 'application/javascript'}

# Eventos SocketIO
@chat_bp.route('/user_message', methods=['POST'])
def handle_message_http():
    data = request.get_json()
    user_message = data['message']
    agent_id = data['agent_id']

    # Buscar informações do agente no Supabase
    agent_info = supabase_manager.get_agent_by_id(agent_id)

    if agent_info:
        agent_name = agent_info['name']
        system_prompt = agent_info['system_prompt']

        # Gerar resposta com IA real
        agent_response = ia_router.generate_response(
            user_message,
            agent_name,
            system_prompt,
            provider_preference=os.getenv("NEXO_LLM_PROVIDER")  # Usar provedor preferencial
        )

        # Salvar no Supabase
        supabase_manager.save_message(agent_id, user_message, agent_response)

        # Emitir resposta via SocketIO (se o cliente estiver conectado)
        emit("agent_response", {"message": agent_response}, broadcast=True, namespace='/')
        return jsonify({"status": "success", "message": agent_response})
    return jsonify({"status": "error", "message": "Agent not found"}), 404

@chat_bp.route('/api/ping')
def ping():
    return jsonify({"status": "ok", "version": "3.2"})




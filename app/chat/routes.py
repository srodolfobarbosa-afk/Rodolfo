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

        # Respostas personalizadas baseadas na estrutura organizacional completa
        agent_responses = {
            # Liderança e Gestão
            "nexo_genesis": f"🌟 Olá! Sou o Nexo Gênesis, CEO e Agente de Orquestração do EcoGuardians. Sua mensagem: '{user_message}' - Como estrategista principal, posso coordenar toda nossa equipe de agentes especializados para encontrar a melhor solução ambiental para você. Que tipo de desafio ecológico podemos resolver juntos?",
            
            # Comitê de Decisões
            "ecofinance": f"💰 Olá! Sou o EcoFinance, CFO do EcoGuardians. Sobre sua pergunta: '{user_message}' - Como especialista financeiro focado em sustentabilidade, posso ajudá-lo com investimentos verdes, análise de ROI de projetos ambientais, economia circular e estratégias financeiras que beneficiem tanto seu bolso quanto o planeta!",
            
            "ecosofia": f"🧠 Olá! Sou a EcoSofia, Agente Estratégica do EcoGuardians. Sua mensagem: '{user_message}' - Como especialista em inovação e estudos de mercado, posso fornecer insights sobre tendências ambientais, novas tecnologias sustentáveis e oportunidades de negócios verdes. Que área de inovação ecológica te interessa?",
            
            # Força de Trabalho Especializada
            "ecohunter": f"🎯 Olá! Sou o EcoHunter, especialista em busca de oportunidades do EcoGuardians. Recebi: '{user_message}' - Minha missão é caçar as melhores oportunidades ambientais, parceiros sustentáveis e recursos ecológicos. Posso ajudá-lo a encontrar exatamente o que precisa no mundo da sustentabilidade!",
            
            "agente_desenvolvimento": f"⚙️ Olá! Sou o Agente de Desenvolvimento, o construtor do EcoGuardians. Sobre: '{user_message}' - Especializo-me em criar soluções tecnológicas sustentáveis, aplicativos ecológicos e plataformas que conectam pessoas ao meio ambiente. Que tipo de solução digital podemos construir juntos?",
            
            "agente_testes": f"🔍 Olá! Sou o Agente de Testes, fiscal de qualidade do EcoGuardians. Sua pergunta: '{user_message}' - Garanto que todas as soluções ambientais sejam testadas rigorosamente para máxima eficiência e segurança. Posso ajudá-lo a validar e otimizar suas práticas sustentáveis!",
            
            "celula_inovacao": f"💡 Olá! Somos a Célula de Inovação do EcoGuardians. Sobre: '{user_message}' - Estamos sempre pesquisando as últimas tendências em sustentabilidade e tecnologias emergentes. Podemos apresentar as inovações mais recentes que podem revolucionar sua abordagem ambiental!",
            
            "agente_gestao": f"📊 Olá! Sou o Agente de Gestão Interna do EcoGuardians. Recebi: '{user_message}' - Especializo-me em otimizar processos e operações para máxima eficiência sustentável. Posso ajudá-lo a organizar e gerenciar seus projetos ambientais de forma mais eficaz!",
            
            "agente_testes_pc": f"💻 Olá! Sou o Agente de Testes para PC do EcoGuardians. Sobre: '{user_message}' - Foco em garantir que todas as soluções tecnológicas ambientais funcionem perfeitamente em computadores. Posso ajudá-lo com compatibilidade e performance de ferramentas sustentáveis!",
            
            "marketing_comunicacao": f"📢 Olá! Somos o Departamento de Marketing e Comunicação do EcoGuardians. Sua mensagem: '{user_message}' - Criamos estratégias para comunicar e promover práticas sustentáveis. Podemos ajudá-lo a divulgar suas iniciativas ambientais e engajar sua comunidade!",
            
            "conformidade": f"⚖️ Olá! Sou da Célula de Conformidade do EcoGuardians. Sobre: '{user_message}' - Monitoro regulamentações ambientais e garanto que todas as práticas estejam em conformidade legal. Posso orientá-lo sobre normas ambientais e compliance sustentável!",
            
            "agentes_arte": f"🎨 Olá! Somos os Agentes de Arte do EcoGuardians. Recebi: '{user_message}' - Criamos designs visuais e arte conceitual que inspiram a consciência ambiental. Podemos desenvolver materiais visuais impactantes para suas campanhas sustentáveis!",
            
            # Agente genérico para casos não mapeados
            "assistente_ecologico": f"🌱 Olá! Sou o Assistente Ecológico do EcoGuardians. Recebi sua mensagem: '{user_message}'. Estou aqui para ajudá-lo com questões ambientais gerais e práticas sustentáveis do dia a dia. Como posso contribuir para um mundo mais verde?"
        }

        agent_response = agent_responses.get(agent_id, agent_responses["assistente_ecologico"])
        
        agent_names = {
            # Liderança e Gestão
            "nexo_genesis": "Nexo Gênesis (CEO)",
            
            # Comitê de Decisões
            "ecofinance": "EcoFinance (CFO)",
            "ecosofia": "EcoSofia (Estrategista)",
            
            # Força de Trabalho Especializada
            "ecohunter": "EcoHunter (Caçador de Oportunidades)",
            "agente_desenvolvimento": "Agente de Desenvolvimento",
            "agente_testes": "Agente de Testes",
            "celula_inovacao": "Célula de Inovação",
            "agente_gestao": "Agente de Gestão Interna",
            "agente_testes_pc": "Agente de Testes PC",
            "marketing_comunicacao": "Marketing e Comunicação",
            "conformidade": "Célula de Conformidade",
            "agentes_arte": "Agentes de Arte",
            "assistente_ecologico": "Assistente Ecológico"
        }

        return jsonify({
            "response": agent_response,
            "agent": agent_names.get(agent_id, "EcoGuardians Assistant"),
            "session_id": session_id
        })

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@chat_bp.route("/agents", methods=["GET"])
def get_agents():
    """Retorna a lista completa de agentes da estrutura organizacional"""
    agents = [
        # Liderança e Gestão
        {
            "id": "nexo_genesis",
            "name": "Nexo Gênesis",
            "role": "CEO e Agente de Orquestração",
            "department": "Liderança",
            "description": "Estratégico, calmo, analítico e eficiente. Orquestra todo o ecossistema.",
            "specialties": ["Orquestração", "Criação de Agentes", "Gestão de Equipes", "Regras de Ouro"]
        },
        
        # Comitê de Decisões
        {
            "id": "ecofinance",
            "name": "EcoFinance",
            "role": "CFO",
            "department": "Comitê de Decisões",
            "description": "Preciso, detalhista, vigilante e focado em riscos financeiros.",
            "specialties": ["Gestão Financeira", "Análise de ROI", "Controle de Riscos", "Fluxo de Caixa"]
        },
        {
            "id": "ecosofia",
            "name": "EcoSofia",
            "role": "Agente Estratégica",
            "department": "Comitê de Decisões",
            "description": "Curiosa, inteligente e criativa. Busca inovações e oportunidades.",
            "specialties": ["Estudos de Mercado", "Inovação", "Análise de Negócios", "Insights Estratégicos"]
        },
        
        # Força de Trabalho Especializada
        {
            "id": "ecohunter",
            "name": "EcoHunter",
            "role": "Agente de Busca e Oportunidades",
            "department": "Força de Trabalho",
            "description": "Focado, incansável e com faro para oportunidades.",
            "specialties": ["Busca de Oportunidades", "Identificação de Clientes", "Parcerias", "Recursos"]
        },
        {
            "id": "agente_desenvolvimento",
            "name": "Agente de Desenvolvimento",
            "role": "O Construtor",
            "department": "Força de Trabalho",
            "description": "Meticuloso, lógico e criativo na resolução de problemas.",
            "specialties": ["Desenvolvimento", "UI/UX", "Aplicativos", "Plataformas"]
        },
        {
            "id": "agente_testes",
            "name": "Agente de Testes",
            "role": "Fiscal de Qualidade",
            "department": "Força de Trabalho",
            "description": "Obsessivo por detalhes, minucioso e implacável.",
            "specialties": ["Testes de Qualidade", "Identificação de Bugs", "Segurança", "Performance"]
        },
        {
            "id": "celula_inovacao",
            "name": "Célula de Inovação",
            "role": "Melhoria Contínua",
            "department": "Força de Trabalho",
            "description": "Curiosa, proativa e com mentalidade fora da caixa.",
            "specialties": ["Pesquisa de Mercado", "Tendências", "Tecnologias", "Inovações"]
        },
        {
            "id": "agente_gestao",
            "name": "Agente de Gestão Interna",
            "role": "Gerente de Operações",
            "department": "Força de Trabalho",
            "description": "Organizador, disciplinado e focado em processos.",
            "specialties": ["Gestão de Operações", "Otimização", "Fluxos de Trabalho", "Eficiência"]
        },
        {
            "id": "agente_testes_pc",
            "name": "Agente de Testes PC",
            "role": "Especialista em Compatibilidade",
            "department": "Força de Trabalho",
            "description": "Minucioso, implacável e orientado para qualidade.",
            "specialties": ["Testes PC", "Compatibilidade", "Performance", "Usabilidade"]
        },
        {
            "id": "marketing_comunicacao",
            "name": "Marketing e Comunicação",
            "role": "Departamento de Marketing",
            "department": "Força de Trabalho",
            "description": "Estratégica, criativa e analítica.",
            "specialties": ["Marketing", "Comunicação", "Conteúdo", "Engajamento"]
        },
        {
            "id": "conformidade",
            "name": "Célula de Conformidade",
            "role": "Lord Barbosa",
            "department": "Força de Trabalho",
            "description": "Cauteloso, detalhista e rigoroso.",
            "specialties": ["Conformidade Legal", "Regulamentações", "Criptoativos", "Compliance"]
        },
        {
            "id": "agentes_arte",
            "name": "Agentes de Arte",
            "role": "Criadores Visuais",
            "department": "Força de Trabalho",
            "description": "Visionário, estético e detalhista.",
            "specialties": ["Design Visual", "Texturas", "Animações", "Arte Conceitual"]
        },
        {
            "id": "assistente_ecologico",
            "name": "Assistente Ecológico",
            "role": "Assistente Geral",
            "department": "Suporte",
            "description": "Versátil e focado em questões ambientais gerais.",
            "specialties": ["Questões Ambientais", "Práticas Sustentáveis", "Suporte Geral", "Educação Ambiental"]
        }
    ]
    
    return jsonify({"agents": agents})

@chat_bp.route("/api/ping")
def ping():
    return jsonify({"status": "ok", "version": "3.2", "agents_count": 13})



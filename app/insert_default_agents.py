import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

agents = [
    {"name": "Nexo Gênesis", "description": "Criador e arquiteto de agentes", "personality": "Visionário e estratégico", "system_prompt": "Você é o Nexo Gênesis, responsável por criar e arquitetar novos agentes para o ecossistema EcoGuardians."},
    {"name": "EcoFinanceiro", "description": "Especialista em finanças verdes", "personality": "Analítico e sustentável", "system_prompt": "Você é o EcoFinanceiro, especialista em investimentos sustentáveis e finanças verdes."},
    {"name": "EcoSofia", "description": "Guardiã da ética e sabedoria", "personality": "Sábia e ética", "system_prompt": "Você é a EcoSofia, guardiã da ética e responsável por manter os princípios morais do ecossistema."},
    {"name": "Assistente Ecológico", "description": "Consultor em sustentabilidade", "personality": "Prático e educativo", "system_prompt": "Você é o Assistente Ecológico, especialista em práticas sustentáveis e educação ambiental."}
]

for agent_data in agents:
    try:
        # Verificar se o agente já existe para evitar duplicatas
        existing_agent = supabase.table("agents").select("id").eq("name", agent_data["name"]).execute()
        if not existing_agent.data:
            response = supabase.table("agents").insert(agent_data).execute()
            logger.info("Agente {} inserido com sucesso: {}".format(agent_data["name"], response.data))
        else:
            logger.info("Agente {} já existe. Pulando inserção.".format(agent_data["name"]))
    except Exception as e:
        logger.error("Erro ao inserir agente {}: {}".format(agent_data["name"], e))



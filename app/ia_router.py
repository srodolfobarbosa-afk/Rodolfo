import os
import google.generativeai as genai
import openai
from dotenv import load_dotenv
import logging

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IARouter:
    def __init__(self):
        self.providers = {
            'google': self._init_gemini,
            'openai': self._init_openai,
            'mock': self._init_mock
        }
        
        # Configurar provedores disponíveis
        self.available_providers = []
        self._setup_providers()
        
    def _setup_providers(self):
        """Configura os provedores de IA disponíveis"""
        
        # Configurar Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                self.available_providers.append('google')
                logger.info("Gemini configurado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao configurar Gemini: {e}")
        
        # Configurar OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                openai.api_key = openai_key
                self.available_providers.append('openai')
                logger.info("OpenAI configurado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao configurar OpenAI: {e}")
        
        # Mock sempre disponível como fallback
        self.available_providers.append('mock')
        
        logger.info(f"Provedores disponíveis: {self.available_providers}")
    
    def _init_gemini(self):
        """Inicializa o modelo Gemini"""
        return genai.GenerativeModel('gemini-1.5-flash')
    
    def _init_openai(self):
        """Inicializa o cliente OpenAI"""
        return openai
    
    def _init_mock(self):
        """Inicializa o provedor mock"""
        return "mock"
    
    def generate_response(self, message, agent_name, system_prompt, provider_preference=None):
        """
        Gera resposta usando o provedor especificado ou o primeiro disponível
        """
        # Determinar provedor a usar
        if provider_preference and provider_preference in self.available_providers:
            providers_to_try = [provider_preference]
        else:
            providers_to_try = self.available_providers
        
        # Tentar cada provedor até conseguir uma resposta
        for provider in providers_to_try:
            try:
                logger.info(f"Tentando provedor: {provider}")
                
                if provider == 'google':
                    return self._generate_gemini_response(message, agent_name, system_prompt)
                elif provider == 'openai':
                    return self._generate_openai_response(message, agent_name, system_prompt)
                elif provider == 'mock':
                    return self._generate_mock_response(message, agent_name, system_prompt)
                    
            except Exception as e:
                logger.error(f"Erro com provedor {provider}: {e}")
                continue
        
        # Se todos falharam, retornar resposta de erro
        return f"[{agent_name}] Desculpe, estou com dificuldades técnicas no momento. Tente novamente em alguns instantes."
    
    def _generate_gemini_response(self, message, agent_name, system_prompt):
        """Gera resposta usando Gemini"""
        model = self._init_gemini()
        
        # Construir prompt completo
        full_prompt = f"""
{system_prompt}

Você é {agent_name}. Responda como este agente específico, mantendo sua personalidade e especialização.

Usuário: {message}

Resposta:"""
        
        response = model.generate_content(full_prompt)
        return f"[{agent_name}] {response.text}"
    
    def _generate_openai_response(self, message, agent_name, system_prompt):
        """Gera resposta usando OpenAI"""
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{system_prompt}\n\nVocê é {agent_name}. Responda como este agente específico."},
                {"role": "user", "content": message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return f"[{agent_name}] {response.choices[0].message.content}"
    
    def _generate_mock_response(self, message, agent_name, system_prompt):
        """Gera resposta mock para testes"""
        responses = {
            "Nexo Gênesis": f"Como criador de agentes, posso ajudar você com: {message}. Que tipo de agente você gostaria que eu criasse?",
            "EcoFinanceiro": f"Analisando sua questão financeira: {message}. Recomendo investimentos sustentáveis e estratégias verdes.",
            "EcoSofia": f"Refletindo sobre a ética da sua pergunta: {message}. É importante considerar o impacto em todos os seres.",
            "Assistente Ecológico": f"Sobre sustentabilidade: {message}. Posso sugerir práticas ecológicas para sua situação."
        }
        
        return responses.get(agent_name, f"[{agent_name}] Recebi sua mensagem: '{message}'. Como posso ajudar?")

# Instância global do roteador
ia_router = IARouter()


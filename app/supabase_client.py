import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseManager:
    def __init__(self):
        self.supabase = None
        self._init_client()
    
    def _init_client(self):
        """Inicializa o cliente Supabase"""
        try:
            url = os.getenv('SUPABASE_URL')
            key = os.getenv('SUPABASE_KEY')
            
            if url and key:
                self.supabase: Client = create_client(url, key)
                logger.info("Cliente Supabase inicializado com sucesso")
                
                # Criar tabelas se não existirem
                self._create_tables()
            else:
                logger.error("Credenciais do Supabase não encontradas")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar Supabase: {e}")
    
    def _create_tables(self):
        """Cria as tabelas necessárias no Supabase"""
        try:
            # Verificar se as tabelas existem
            # Se não existirem, elas serão criadas via SQL no painel do Supabase
            logger.info("Verificando estrutura das tabelas...")
            
        except Exception as e:
            logger.error(f"Erro ao verificar tabelas: {e}")
    
    def save_agent(self, name, description, personality, system_prompt):
        """Salva um agente no Supabase"""
        try:
            if not self.supabase:
                return None
                
            data = {
                'name': name,
                'description': description,
                'personality': personality,
                'system_prompt': system_prompt,
                'created_at': datetime.now().isoformat()
            }
            
            result = self.supabase.table('agents').insert(data).execute()
            logger.info(f"Agente {name} salvo com sucesso")
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Erro ao salvar agente: {e}")
            return None
    
    def get_agents(self):
        """Recupera todos os agentes do Supabase"""
        try:
            if not self.supabase:
                return []
                
            result = self.supabase.table('agents').select('*').execute()
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Erro ao recuperar agentes: {e}")
            return []
    
    def get_agent_by_id(self, agent_id):
        """Recupera um agente específico por ID"""
        try:
            if not self.supabase:
                return None
                
            result = self.supabase.table('agents').select('*').eq('id', agent_id).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Erro ao recuperar agente {agent_id}: {e}")
            return None
    
    def save_message(self, agent_id, user_message, agent_response, session_id=None):
        """Salva uma mensagem no histórico"""
        try:
            if not self.supabase:
                return None
                
            data = {
                'agent_id': agent_id,
                'user_message': user_message,
                'agent_response': agent_response,
                'session_id': session_id,
                'created_at': datetime.now().isoformat()
            }
            
            result = self.supabase.table('messages').insert(data).execute()
            logger.info(f"Mensagem salva para agente {agent_id}")
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Erro ao salvar mensagem: {e}")
            return None
    
    def get_message_history(self, agent_id, limit=50):
        """Recupera o histórico de mensagens de um agente"""
        try:
            if not self.supabase:
                return []
                
            result = (self.supabase.table('messages')
                     .select('*')
                     .eq('agent_id', agent_id)
                     .order('created_at', desc=True)
                     .limit(limit)
                     .execute())
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Erro ao recuperar histórico: {e}")
            return []
    
    def save_user_session(self, user_id, session_data):
        """Salva dados da sessão do usuário"""
        try:
            if not self.supabase:
                return None
                
            data = {
                'user_id': user_id,
                'session_data': session_data,
                'created_at': datetime.now().isoformat()
            }
            
            result = self.supabase.table('user_sessions').insert(data).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Erro ao salvar sessão: {e}")
            return None

# Instância global do gerenciador Supabase
supabase_manager = SupabaseManager()


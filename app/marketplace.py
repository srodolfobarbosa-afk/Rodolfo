from flask import jsonify, request
import sqlite3
import os

DATABASE = 'marketplace.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            token_id TEXT,
            status TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

class Marketplace:
    def __init__(self):
        init_db()

    def list_agents(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, price, token_id, status, created_at FROM agents")
        agents = cursor.fetchall()
        conn.close()
        
        result = []
        for agent in agents:
            result.append({
                "id": agent[0],
                "name": agent[1],
                "description": agent[2],
                "price": agent[3],
                "token_id": agent[4],
                "status": agent[5],
                "created_at": agent[6]
            })
        return {"status": "success", "agents": result}

    def add_agent(self, name, description, price, token_id):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO agents (name, description, price, token_id, status) VALUES (?, ?, ?, ?, ?)",
                       (name, description, price, token_id, "pending_review"))
        conn.commit()
        conn.close()
        return {"status": "success", "message": f"Agente {name} adicionado ao marketplace para revisão."}

    def update_agent_status(self, agent_id, status):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE agents SET status = ? WHERE id = ?", (status, agent_id))
        conn.commit()
        conn.close()
        return {"status": "success", "message": f"Status do agente {agent_id} atualizado para {status}."}

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    marketplace = Marketplace()
    
    print("\n--- Adicionando Agentes ---")
    print(marketplace.add_agent("Agente de Vendas AI", "Agente especializado em otimização de vendas.", 100.0, "ECG001"))
    print(marketplace.add_agent("Agente de Suporte ao Cliente", "Agente para atendimento automatizado.", 50.0, "ECG002"))

    print("\n--- Listando Agentes ---")
    print(marketplace.list_agents())

    print("\n--- Atualizando Status de Agente ---")
    # Supondo que o ID do Agente de Vendas AI seja 1
    print(marketplace.update_agent_status(1, "approved"))
    print(marketplace.list_agents())





from app.web_automation import WebAgent
from flask import jsonify
from bs4 import BeautifulSoup
import sqlite3
import os

DATABASE = 'eco_explorer_data.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            search_url TEXT NOT NULL,
            title TEXT NOT NULL,
            relevance TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

class EcoExplorer:
    def __init__(self):
        self.web_agent = WebAgent()
        init_db()

    def search_and_analyze(self, query, search_url="https://www.google.com"):
        try:
            print(f"Eco-Explorer: Iniciando busca por \'{query}\' em {search_url}")
            self.web_agent.navigate(search_url)
            page_source = self.web_agent.search(query, "textarea[name=\'q\']")
            
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Exemplo de extração de títulos de resultados usando BeautifulSoup
            # Pode ser necessário ajustar o seletor CSS dependendo do site
            search_results_elements = soup.select('h3') # Exemplo para Google search results
            search_results_titles = [elem.get_text() for elem in search_results_elements]
            
            opportunities = []
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            for title in search_results_titles:
                relevance = "low"
                if "sustentabilidade" in title.lower() or "inovação verde" in title.lower():
                    relevance = "high"
                elif "cripto" in title.lower() or "blockchain" in title.lower():
                    relevance = "medium"
                
                opportunities.append({"title": title, "relevance": relevance})
                
                # Salvar no banco de dados
                cursor.execute("INSERT INTO search_results (query, search_url, title, relevance) VALUES (?, ?, ?, ?)",
                               (query, search_url, title, relevance))
            
            conn.commit()
            conn.close()

            return {
                "status": "success",
                "query": query,
                "search_url": search_url,
                "results_titles": search_results_titles,
                "identified_opportunities": opportunities,
                "raw_page_source_sample": page_source[:500] # Amostra do HTML
            }
        except Exception as e:
            print(f"Eco-Explorer: Erro durante a busca: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            self.web_agent.close()

    def get_historical_data(self, query=None, limit=100):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        if query:
            cursor.execute("SELECT query, search_url, title, relevance, timestamp FROM search_results WHERE query LIKE ? ORDER BY timestamp DESC LIMIT ?", (f'%{query}%', limit))
        else:
            cursor.execute("SELECT query, search_url, title, relevance, timestamp FROM search_results ORDER BY timestamp DESC LIMIT ?", (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                "query": row[0],
                "search_url": row[1],
                "title": row[2],
                "relevance": row[3],
                "timestamp": row[4]
            })
        return results

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    explorer = EcoExplorer()
    print("\n--- Teste de Busca e Análise ---")
    result = explorer.search_and_analyze("inteligência artificial sustentável")
    print(f"Status da Busca: {result.get("status")}")
    print(f"Oportunidades Identificadas: {len(result.get("identified_opportunities", []))}")
    
    print("\n--- Teste de Dados Históricos ---")
    historical_data = explorer.get_historical_data(query="inteligência artificial")
    print(f"Dados Históricos Encontrados: {len(historical_data)}")
    for data in historical_data:
        print(f"  - Query: {data["query"]}, Título: {data["title"]}")
    print("----------------------------")



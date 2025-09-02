from app.web_automation import WebAgent
from flask import jsonify

class EcoExplorer:
    def __init__(self):
        self.web_agent = WebAgent()

    def search_and_analyze(self, query, search_url="https://www.google.com"):
        try:
            print(f"Eco-Explorer: Iniciando busca por \'{query}\' em {search_url}")
            self.web_agent.navigate(search_url)
            page_source = self.web_agent.search(query, "textarea[name=\'q\"]")
            
            # Exemplo de extração de títulos de resultados (pode variar)
            search_results_titles = self.web_agent.get_text_by_selector("h3")
            
            # Simulação de análise de dados e identificação de oportunidades
            opportunities = []
            for title in search_results_titles:
                if "sustentabilidade" in title.lower() or "inovação verde" in title.lower():
                    opportunities.append({"title": title, "relevance": "high"})
                elif "cripto" in title.lower() or "blockchain" in title.lower():
                    opportunities.append({"title": title, "relevance": "medium"})
            
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

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    explorer = EcoExplorer()
    result = explorer.search_and_analyze("novas tecnologias de energia renovável")
    print("\n--- Relatório Eco-Explorer ---")
    print(f"Status: {result.get("status")}")
    print(f"Consulta: {result.get("query")}")
    print(f"Oportunidades Identificadas: {len(result.get("identified_opportunities", []))}")
    for opp in result.get("identified_opportunities", []):
        print(f"  - Título: {opp["title"]}", f"Relevância: {opp["relevance"]}")
    print("----------------------------")



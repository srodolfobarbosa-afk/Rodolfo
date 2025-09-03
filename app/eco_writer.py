import os
from flask import jsonify
from google.generativeai import GenerativeModel

class EcoWriter:
    def __init__(self):
        # Inicializa o modelo Gemini
        # Certifique-se de que GOOGLE_API_KEY está configurada no ambiente
        self.model = GenerativeModel("gemini-pro")

    def generate_content(self, topic, length="médio", style="informativo"):
        try:
            prompt = f"Gere um artigo sobre '{topic}' com estilo {style} e tamanho {length}."
            
            # Adicionar contexto para otimização SEO (exemplo simples)
            if "sustentabilidade" in topic.lower() or "ecologia" in topic.lower():
                prompt += " Inclua palavras-chave como 'sustentabilidade', 'meio ambiente', 'inovação verde'."
            
            response = self.model.generate_content(prompt)
            generated_text = response.text
            
            return {
                "status": "success",
                "topic": topic,
                "length": length,
                "style": style,
                "content": generated_text
            }
        except Exception as e:
            print(f"Eco-Writer: Erro ao gerar conteúdo: {e}")
            return {"status": "error", "message": str(e)}

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    # Para testar, você precisará configurar a variável de ambiente GOOGLE_API_KEY
    # os.environ["GOOGLE_API_KEY"] = "SUA_CHAVE_API_AQUI"
    
    writer = EcoWriter()
    print("\n--- Teste de Geração de Conteúdo ---")
    result = writer.generate_content("benefícios da energia solar", length="curto", style="persuasivo")
    print(f"Status da Geração: {result.get('status')}")
    print(f"Conteúdo Gerado: {result.get('content')[:200]}...") # Imprime os primeiros 200 caracteres
    print("----------------------------")



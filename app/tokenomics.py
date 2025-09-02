import os
from flask import jsonify

class Tokenomics:
    def __init__(self):
        # Simulação de um contrato inteligente de token ECG na BSC
        self.total_supply = 1_000_000_000  # 1 bilhão de tokens
        self.circulating_supply = 500_000_000 # 500 milhões em circulação
        self.burned_tokens = 0
        self.treasury_balance = 500_000_000 # Tokens para desenvolvimento e recompensas
        self.token_price_usd = 0.001 # Preço inicial simulado

    def get_token_info(self):
        return {
            "status": "success",
            "token_name": "EcoGuardians Token",
            "token_symbol": "ECG",
            "total_supply": self.total_supply,
            "circulating_supply": self.circulating_supply,
            "burned_tokens": self.burned_tokens,
            "treasury_balance": self.treasury_balance,
            "current_price_usd": self.token_price_usd,
            "blockchain": "Binance Smart Chain (BSC) - Simulado"
        }

    def simulate_burn(self, amount):
        if amount <= 0:
            return {"status": "error", "message": "Quantidade para queimar deve ser positiva"}
        if amount > self.circulating_supply:
            return {"status": "error", "message": "Quantidade para queimar excede o supply circulante"}
        
        self.circulating_supply -= amount
        self.burned_tokens += amount
        self.token_price_usd *= (1 + (amount / self.total_supply) * 0.05) # Simula aumento de preço
        
        return {
            "status": "success",
            "message": f"{amount} ECG tokens queimados com sucesso.",
            "new_circulating_supply": self.circulating_supply,
            "total_burned": self.burned_tokens,
            "new_price_usd": self.token_price_usd
        }

    def simulate_transfer(self, sender, receiver, amount):
        # Em um sistema real, isso interagiria com a blockchain
        if amount <= 0:
            return {"status": "error", "message": "Quantidade para transferir deve ser positiva"}
        
        # Simulação simples de que o sender tem fundos
        # Em um sistema real, verificaria o saldo do sender
        print(f"Simulando transferência de {amount} ECG de {sender} para {receiver}")
        
        return {
            "status": "success",
            "message": f"Transferência simulada de {amount} ECG de {sender} para {receiver} concluída."
        }

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    tokenomics = Tokenomics()
    print("\n--- Informações Iniciais do Token ---")
    print(tokenomics.get_token_info())

    print("\n--- Simulação de Queima de Tokens ---")
    print(tokenomics.simulate_burn(10_000_000)) # Queima 10 milhões de tokens
    print(tokenomics.get_token_info())

    print("\n--- Simulação de Transferência ---")
    print(tokenomics.simulate_transfer("Rodolfo", "AgenteEcoFinance", 5000))
    print("----------------------------")



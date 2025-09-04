#!/bin/bash

# Este script automatiza a configuração e execução do projeto EcoGuardians.

# 1. Ativa ou cria o ambiente virtual
if [ ! -d "venv" ]; then
    echo "🌱 Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "✅ Ativando ambiente virtual..."
source venv/bin/activate

# 2. Instala as dependências do projeto
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Define variáveis de ambiente
echo "⚙️ Definindo variáveis de ambiente..."
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY="sua_chave_super_secreta"

# 4. Cria o banco de dados local (se não existir)
if [ ! -f "ecoguardians.db" ]; then
    echo "🗃️ Criando banco de dados local 'ecoguardians.db'..."
    python -c "import sqlite3; sqlite3.connect('ecoguardians.db').close()"
fi

# 5. Roda o script para inserir os agentes padrão
echo "🤖 Inserindo agentes padrão..."
python insert_default_agents.py

# 6. Inicia o servidor Flask
echo "🚀 Iniciando o servidor Flask..."
flask run
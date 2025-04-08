import os
from dotenv import load_dotenv

# Carrega as variáveis do ambiente a partir do arquivo .env
load_dotenv()

# ---------------------------------------------------
# Configurações Gerais da Aplicação
# ---------------------------------------------------
APP_NAME = "Sistema Jurídico"
PAGE_LAYOUT = "wide"

# ---------------------------------------------------
# Configurações da API DeepSeek
# ---------------------------------------------------
# A chave e o endpoint da API são carregados via variável de ambiente.
# Certifique-se de definir DEEPSEEK_API_KEY e (opcionalmente) DEEPSEEK_ENDPOINT no seu arquivo .env.
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sua_chave_default")
DEEPSEEK_ENDPOINT = os.getenv("DEEPSEEK_ENDPOINT", "https://api.deepseek.com/v1/chat/completions")

# ---------------------------------------------------
# Configuração do Google Apps Script
# ---------------------------------------------------
# URL do Web App do Google que integra com o Google Sheets.
GAS_WEB_APP_URL = os.getenv("GAS_WEB_APP_URL", "https://script.google.com/macros/s/AKfycbytp0BA1x2PnjcFhunbgWEoMxZmCobyZHNzq3Mxabr41RScNAH-nYIlBd-OySWv5dcx/exec")


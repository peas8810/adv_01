import requests
import httpx
from dotenv import load_dotenv

load_dotenv()
GAS_WEB_APP_URL = os.getenv("GAS_WEB_APP_URL")

@st.cache_data(ttl=300, show_spinner=False)
def carregar_dados_da_planilha(tipo, debug=False):
    # implementação de requisição GET ao GAS

# def enviar_dados_para_planilha(tipo, dados): implementação de POST ao GAS

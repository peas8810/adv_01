import os
import requests
import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
GAS_WEB_APP_URL = os.getenv("GAS_WEB_APP_URL")

@st.cache_data(ttl=300, show_spinner=False)
def carregar_dados_da_planilha(tipo, debug=False):
    """
    Faz GET ao Google Apps Script para obter dados de uma aba específica.
    Retorna lista de dicionários ou [] em caso de erro.
    """
    try:
        response = requests.get(GAS_WEB_APP_URL, params={"tipo": tipo}, timeout=10)
        response.raise_for_status()
        if debug:
            st.text(f"URL chamada: {response.url}")
            st.text(f"Resposta bruta: {response.text[:500]}")
        return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar dados ({tipo}): {e}")
        return []


def enviar_dados_para_planilha(tipo, dados):
    """
    Envia via POST ao Google Apps Script um payload JSON contendo 'tipo' e demais campos.
    Retorna True se o GAS responder "OK".
    """
    try:
        payload = {"tipo": tipo, **dados}
        with httpx.Client(timeout=10, follow_redirects=True) as client:
            response = client.post(GAS_WEB_APP_URL, json=payload)
        if response.text.strip() == "OK":
            return True
        st.error(f"Erro no envio ({tipo}): {response.text}")
        return False
    except Exception as e:
        st.error(f"Erro ao enviar dados ({tipo}): {e}")
        return False

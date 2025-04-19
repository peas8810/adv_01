# servicos/planilhas.py

import os
import requests
import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
GAS_WEB_APP_URL = os.getenv("GAS_WEB_APP_URL")

@st.cache_data(ttl=300, show_spinner=False)
def carregar_dados_da_planilha(tipo, debug=False):
    try:
        resp = requests.get(GAS_WEB_APP_URL, params={"tipo": tipo}, timeout=10)
        resp.raise_for_status()
        if debug:
            st.text(f"URL: {resp.url}")
            st.text(f"Resp raw: {resp.text[:200]}")
        return resp.json()
    except Exception as e:
        st.error(f"Erro ao carregar dados ({tipo}): {e}")
        return []

def enviar_dados_para_planilha(tipo, dados):
    try:
        payload = {"tipo": tipo, **dados}
        with httpx.Client(timeout=10, follow_redirects=True) as cli:
            resp = cli.post(GAS_WEB_APP_URL, json=payload)
        if resp.text.strip() == "OK":
            return True
        st.error(f"Erro no envio ({tipo}): {resp.text}")
        return False
    except Exception as e:
        st.error(f"Erro ao enviar ({tipo}): {e}")
        return False

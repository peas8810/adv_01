import json
import requests
import httpx
import time
import datetime
import streamlit as st

from config import GAS_WEB_APP_URL, DEEPSEEK_API_KEY, DEEPSEEK_ENDPOINT

def enviar_dados_para_planilha(tipo: str, dados: dict) -> bool:
    """
    Envia dados para o Google Sheets por meio do Google Apps Script.

    Args:
        tipo (str): Tipo dos dados (ex.: "Cliente", "Processo", etc.).
        dados (dict): Dicionário com os dados a serem enviados.

    Returns:
        bool: True se o envio foi bem-sucedido; False caso contrário.
    """
    try:
        payload = {"tipo": tipo, **dados}
        response = requests.post(
            GAS_WEB_APP_URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        return response.text.strip() == "OK"
    except Exception as e:
        st.error(f"❌ Erro ao enviar dados ({tipo}): {e}")
        return False


def carregar_dados_da_planilha(tipo: str, debug: bool = False) -> list:
    """
    Carrega dados do Google Sheets por meio do Google Apps Script.

    Args:
        tipo (str): Tipo de dados a serem carregados.
        debug (bool, optional): Se True, exibe informações de depuração. Padrão é False.

    Returns:
        list: Lista com os dados retornados ou lista vazia em caso de erro.
    """
    try:
        response = requests.get(GAS_WEB_APP_URL, params={"tipo": tipo})
        response.raise_for_status()
        if debug:
            st.text(f"🔍 URL chamada: {response.url}")
            st.text(f"📄 Resposta bruta: {response.text[:500]}")
        return response.json()
    except json.JSONDecodeError:
        st.error(f"❌ Resposta inválida para o tipo '{tipo}'. O servidor não retornou JSON válido.")
        return []
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados ({tipo}): {e}")
        return []


def gerar_peticao_ia(prompt: str, temperatura: float = 0.7, max_tokens: int = 2000, tentativas: int = 3) -> str:
    """
    Gera uma petição jurídica utilizando a API DeepSeek.

    Esta função integra com a API DeepSeek para gerar petições jurídicas, implementando
    tratamento de timeout e retry para melhorar a robustez da requisição.

    Args:
        prompt (str): O prompt que descreve os detalhes do caso.
        temperatura (float, optional): Parâmetro de controle da aleatoriedade da resposta. Padrão é 0.7.
        max_tokens (int, optional): Número máximo de tokens para a resposta. Padrão é 2000.
        tentativas (int, optional): Número de tentativas em caso de falha. Padrão é 3.

    Returns:
        str: A resposta gerada pela API ou uma mensagem de erro caso a solicitação falhe.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "Você é um assistente jurídico especializado. Responda com linguagem técnica formal."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperatura,
        "max_tokens": max_tokens
    }
    
    for tentativa in range(tentativas):
        try:
            start_time = time.time()
            with httpx.Client(timeout=30) as client:
                response = client.post(
                    DEEPSEEK_ENDPOINT,
                    headers=headers,
                    json=payload
                )
            response_time = time.time() - start_time
            st.sidebar.metric("Tempo de resposta API", f"{response_time:.2f}s")
            
            response.raise_for_status()
            resposta_json = response.json()

            if not resposta_json.get('choices'):
                raise ValueError("Resposta da API incompleta")
                
            return resposta_json['choices'][0]['message']['content']
        except httpx.ReadTimeout:
            if tentativa < tentativas - 1:
                st.warning(f"Tentativa {tentativa + 1} falhou (timeout). Tentando novamente...")
                continue
            else:
                raise Exception("O servidor demorou muito para responder após várias tentativas")
        except httpx.HTTPStatusError as e:
            error_msg = f"Erro HTTP {e.response.status_code}"
            if e.response.status_code == 402:
                error_msg += " - Saldo insuficiente na API"
            raise Exception(f"{error_msg}: {e.response.text}")
        except Exception as e:
            if tentativa == tentativas - 1:
                raise Exception(f"Erro na requisição: {str(e)}")
            continue
    
    return "❌ Falha ao gerar petição após múltiplas tentativas"


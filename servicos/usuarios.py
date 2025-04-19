# servicos/usuarios.py
import streamlit as st
from .planilhas import carregar_dados_da_planilha

def carregar_usuarios_da_planilha():
    """
    Carrega usuários vindos do GAS e monta st.session_state.USERS.
    """
    funcs = carregar_dados_da_planilha("Funcionario") or []
    users = {}
    if not funcs:
        users["dono"] = {"username": "dono", "senha": "dono123", "papel": "owner"}
        return users

    for f in funcs:
        key = f.get("usuario")
        if not key: continue
        users[key] = {
            "username":   key,
            "senha":      f.get("senha", ""),
            "papel":      f.get("papel", "assistant"),
            "escritorio": f.get("escritorio", "Global"),
            "area":       f.get("area", "Todas")
        }
    return users

def login(usuario, senha):
    """
    Valida credenciais contra st.session_state.USERS.
    """
    users = st.session_state.get("USERS", {})
    u = users.get(usuario)
    if u and u.get("senha") == senha:
        return u
    return None

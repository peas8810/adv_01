import streamlit as st
import importlib
from servicos.usuarios import carregar_usuarios_da_planilha, login

st.set_page_config(page_title="Sistema Jurídico", layout="wide")

def main():
    # Autenticação
    st.session_state.USERS = carregar_usuarios_da_planilha()

    with st.sidebar:
        st.header("🔐 Login")
        usr = st.text_input("Usuário")
        pwd = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user = login(usr, pwd)
            if user:
                st.session_state.usuario = usr
                st.session_state.papel   = user["papel"]
                st.session_state.dados_usuario = user
                st.success("Login realizado com sucesso!")
            else:
                st.error("Credenciais inválidas")

        if "usuario" in st.session_state:
            if st.button("Sair"):
                for k in ["usuario","papel","dados_usuario"]:
                    st.session_state.pop(k, None)
                st.success("Você saiu do sistema!")
                st.experimental_rerun()

    if "usuario" in st.session_state:
        st.sidebar.success(f"Bem‑vindo, {st.session_state.usuario} ({st.session_state.papel})")

        PAGES = {
            "Dashboard":              "pages.dashboard",
            "Clientes":               "pages.clientes",
            "Processos":              "pages.processos",
            "Históricos":             "pages.historicos",
            "Gerenciar Funcionários": "pages.gerenciar_funcionarios",
        }
        if st.session_state.papel == "owner":
            PAGES["Gerenciar Escritórios"] = "pages.gerenciar_escritorios"
            PAGES["Gerenciar Permissões"]  = "pages.gerenciar_permissoes"

        escolha = st.sidebar.selectbox("Menu", list(PAGES.keys()))
        mod = importlib.import_module(PAGES[escolha])
        mod.main()
    else:
        st.info("Por favor, faça login para acessar o sistema.")

if __name__ == "__main__":
    main()

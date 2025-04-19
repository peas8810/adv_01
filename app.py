import streamlit as st
import importlib
from utils import carregar_usuarios_da_planilha, login

# Configuração da página
st.set_page_config(page_title="Sistema Jurídico", layout="wide")

def main():
    # Carrega os usuários a partir da planilha para autenticação
    st.session_state.USERS = carregar_usuarios_da_planilha()

    # ---------------- Sidebar: Login / Logout ----------------
    with st.sidebar:
        st.header("🔐 Login")
        usuario_input = st.text_input("Usuário")
        senha_input = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user = login(usuario_input, senha_input)
            if user:
                st.session_state.usuario = usuario_input
                st.session_state.papel = user["papel"]
                st.session_state.dados_usuario = user
                st.success("Login realizado com sucesso!")
            else:
                st.error("Credenciais inválidas")

        # Botão de logout visível apenas após login
        if "usuario" in st.session_state:
            if st.button("Sair"):
                for key in ["usuario", "papel", "dados_usuario"]:
                    st.session_state.pop(key, None)
                st.success("Você saiu do sistema!")
                st.experimental_rerun()

    # ---------------- Interface principal após login ----------------
    if "usuario" in st.session_state:
        st.sidebar.success(f"Bem-vindo, {st.session_state.usuario} ({st.session_state.papel})")

        # Mapeamento do menu para arquivos em pages/
        PAGES = {
            "Dashboard":                 "pages.dashboard",
            "Clientes":                  "pages.clientes",
            "Processos":                 "pages.processos",
            "Históricos":                "pages.historicos",
            "Gerenciar Funcionários":    "pages.gerenciar_funcionarios",
        }
        # Apenas owner vê escritórios e permissões
        if st.session_state.papel == "owner":
            PAGES["Gerenciar Escritórios"] = "pages.gerenciar_escritorios"
            PAGES["Gerenciar Permissões"] = "pages.gerenciar_permissoes"

        escolha = st.sidebar.selectbox("Menu", list(PAGES.keys()))
        module = importlib.import_module(PAGES[escolha])
        module.main()

    else:
        st.info("Por favor, faça login para acessar o sistema.")

if __name__ == "__main__":
    main()


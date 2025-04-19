import streamlit as st
import datetime
from utils.helpers import get_dataframe_with_cols, exportar_pdf
from servicos.planilhas import carregar_dados_da_planilha, enviar_dados_para_planilha


def main():
    st.subheader("👥 Cadastro de Funcionários")

    # Carrega dados de escritórios e funcionários
    ESCRITORIOS = carregar_dados_da_planilha("Escritorio") or []
    nomes_escritorios = [e.get("nome", "Global") for e in ESCRITORIOS] or ["Global"]
    FUNCIONARIOS = carregar_dados_da_planilha("Funcionario") or []

    # Formulário de cadastro
    with st.form("form_funcionario"):
        nome = st.text_input("Nome Completo*")
        email = st.text_input("E-mail*")
        telefone = st.text_input("Telefone*")
        usuario_novo = st.text_input("Usuário*")
        senha_novo = st.text_input("Senha*", type="password")
        escritorio = st.selectbox("Escritório*", nomes_escritorios)
        area_atuacao = st.selectbox(
            "Área de Atuação*", ["Cível", "Criminal", "Trabalhista", "Previdenciário", "Tributário", "Todas"]
        )
        papel_func = st.selectbox("Papel no Sistema*", ["manager", "lawyer", "assistant"])

        if st.form_submit_button("Cadastrar Funcionário"):
            if not all([nome, email, telefone, usuario_novo, senha_novo]):
                st.warning("Campos obrigatórios não preenchidos!")
            else:
                novo_funcionario = {
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "usuario": usuario_novo,
                    "senha": senha_novo,
                    "escritorio": escritorio,
                    "area": area_atuacao,
                    "papel": papel_func,
                    "data_cadastro": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "cadastrado_por": st.session_state.usuario
                }
                if enviar_dados_para_planilha("Funcionario", novo_funcionario):
                    st.success("Funcionário cadastrado com sucesso!")

    # Lista de funcionários
    st.subheader("Lista de Funcionários")
    papel = st.session_state.get("papel", "")
    escritorio_usuario = st.session_state.dados_usuario.get("escritorio", "Global")
    if papel == "manager":
        funcionarios_visiveis = [f for f in FUNCIONARIOS if f.get("escritorio") == escritorio_usuario]
    else:
        funcionarios_visiveis = FUNCIONARIOS

    if funcionarios_visiveis:
        df_func = get_dataframe_with_cols(
            funcionarios_visiveis,
            ["nome", "email", "telefone", "usuario", "papel", "escritorio", "area"]
        )
        st.dataframe(df_func)

        col_txt, col_pdf = st.columns(2)
        with col_txt:
            txt = "\n".join([
                f"{f.get('nome','')} | {f.get('email','')} | {f.get('telefone','')}"
                for f in funcionarios_visiveis
            ])
            st.download_button(
                label="Exportar Funcionários (TXT)",
                data=txt,
                file_name="funcionarios.txt",
                mime="text/plain"
            )
        with col_pdf:
            texto_pdf = "\n".join([
                f"{f.get('nome','')} | {f.get('email','')} | {f.get('telefone','')}"
                for f in funcionarios_visiveis
            ])
            pdf_file = exportar_pdf(texto_pdf, nome_arquivo="funcionarios")
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Exportar Funcionários (PDF)",
                    data=f,
                    file_name="funcionarios.pdf",
                    mime="application/pdf"
                )
    else:
        st.info("Nenhum funcionário cadastrado ainda")


if __name__ == "__main__":
    main()


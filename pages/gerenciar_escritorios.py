import streamlit as st
import datetime
from utils.helpers import get_dataframe_with_cols, exportar_pdf
from servicos.planilhas import carregar_dados_da_planilha, enviar_dados_para_planilha


def main():
    st.subheader("🏢 Gerenciamento de Escritórios")
    ESCRITORIOS = carregar_dados_da_planilha("Escritorio") or []

    tab1, tab2, tab3 = st.tabs([
        "Cadastrar Escritório", "Lista de Escritórios", "Administradores"
    ])

    # Aba: Cadastrar Escritório
    with tab1:
        with st.form("form_escritorio"):
            nome = st.text_input("Nome do Escritório*")
            endereco = st.text_input("Endereço Completo*")
            telefone = st.text_input("Telefone*")
            email = st.text_input("E-mail*")
            cnpj = st.text_input("CNPJ*")
            st.subheader("Responsável Técnico")
            responsavel_tecnico = st.text_input("Nome do Responsável Técnico*")
            telefone_tecnico = st.text_input("Telefone do Responsável*")
            email_tecnico = st.text_input("E-mail do Responsável*")
            area_atuacao = st.multiselect(
                "Áreas de Atuação", [
                    "Cível", "Criminal", "Trabalhista", "Previdenciário", "Tributário"
                ]
            )
            if st.form_submit_button("Salvar Escritório"):
                obrigatorios = [nome, endereco, telefone, email, cnpj,
                                responsavel_tecnico, telefone_tecnico, email_tecnico]
                if not all(obrigatorios):
                    st.warning("Todos os campos obrigatórios (*) devem ser preenchidos!")
                else:
                    novo_escritorio = {
                        "nome": nome,
                        "endereco": endereco,
                        "telefone": telefone,
                        "email": email,
                        "cnpj": cnpj,
                        "data_cadastro": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "responsavel_tecnico": responsavel_tecnico,
                        "telefone_tecnico": telefone_tecnico,
                        "email_tecnico": email_tecnico,
                        "area_atuacao": ", ".join(area_atuacao)
                    }
                    if enviar_dados_para_planilha("Escritorio", novo_escritorio):
                        ESCRITORIOS.append(novo_escritorio)
                        st.success("Escritório cadastrado com sucesso!")

    # Aba: Lista de Escritórios
    with tab2:
        if ESCRITORIOS:
            df_esc = get_dataframe_with_cols(
                ESCRITORIOS,
                ["nome", "endereco", "telefone", "email", "cnpj"]
            )
            st.dataframe(df_esc)
            col_txt, col_pdf = st.columns(2)
            with col_txt:
                txt = "\n".join([
                    f"{e.get('nome','')} | {e.get('endereco','')} | {e.get('telefone','')}"
                    for e in ESCRITORIOS
                ])
                st.download_button(
                    "Exportar Escritórios (TXT)",
                    data=txt,
                    file_name="escritorios.txt",
                    mime="text/plain"
                )
            with col_pdf:
                txt_pdf = "\n".join([
                    f"{e.get('nome','')} | {e.get('endereco','')} | {e.get('telefone','')}"
                    for e in ESCRITORIOS
                ])
                pdf_file = exportar_pdf(txt_pdf, nome_arquivo="escritorios")
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "Exportar Escritórios (PDF)",
                        data=f,
                        file_name="escritorios.pdf",
                        mime="application/pdf"
                    )
        else:
            st.info("Nenhum escritório cadastrado ainda")

    # Aba: Administradores
    with tab3:
        st.subheader("Administradores de Escritórios")
        st.info("Funcionalidade em desenvolvimento.")


if __name__ == "__main__":
    main()


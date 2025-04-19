import streamlit as st
import datetime
from utils.helpers import get_dataframe_with_cols, exportar_pdf
from servicos.planilhas import carregar_dados_da_planilha, enviar_dados_para_planilha

def main():

def main():


def main():
    st.subheader("👥 Cadastro de Clientes")
    
    # Carrega dados de clientes e escritórios
    CLIENTES = carregar_dados_da_planilha("Cliente") or []
    ESCRITORIOS = carregar_dados_da_planilha("Escritorio") or []
    nomes_escritorios = [e.get("nome", "") for e in ESCRITORIOS]

    # Formulário de cadastro
    with st.form("form_cliente"):
        nome = st.text_input("Nome Completo*", key="nome_cliente")
        email = st.text_input("E-mail*")
        telefone = st.text_input("Telefone*")
        aniversario = st.date_input("Data de Nascimento")
        endereco = st.text_input("Endereço*", placeholder="Rua, número, bairro, cidade, CEP")
        escritorio = st.selectbox("Escritório", nomes_escritorios + ["Outro"])
        observacoes = st.text_area("Observações")
        if st.form_submit_button("Salvar Cliente"):
            if not nome or not email or not telefone or not endereco:
                st.warning("Campos obrigatórios não preenchidos!")
            else:
                novo_cliente = {
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "aniversario": aniversario.strftime("%Y-%m-%d"),
                    "endereco": endereco,
                    "observacoes": observacoes,
                    "cadastro": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "responsavel": st.session_state.usuario,
                    "escritorio": escritorio
                }
                if enviar_dados_para_planilha("Cliente", novo_cliente):
                    CLIENTES.append(novo_cliente)
                    st.success("Cliente cadastrado com sucesso!")

    # Lista de clientes
    st.subheader("Lista de Clientes")
    if CLIENTES:
        df_cliente = get_dataframe_with_cols(
            CLIENTES,
            ["nome", "email", "telefone", "endereco", "cadastro"]
        )
        st.dataframe(df_cliente)

        # Exportação
        col_txt, col_pdf = st.columns(2)
        with col_txt:
            txt = "\n".join([
                f"{c.get('nome','')} | {c.get('email','')} | {c.get('telefone','')}"
                for c in CLIENTES
            ])
            st.download_button(
                label="Exportar Clientes (TXT)",
                data=txt,
                file_name="clientes.txt",
                mime="text/plain"
            )
        with col_pdf:
            texto_pdf = "\n".join([
                f"{c.get('nome','')} | {c.get('email','')} | {c.get('telefone','')}"
                for c in CLIENTES
            ])
            pdf_file = exportar_pdf(texto_pdf, nome_arquivo="clientes")
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Exportar Clientes (PDF)",
                    data=f,
                    file_name="clientes.pdf",
                    mime="application/pdf"
                )
    else:
        st.info("Nenhum cliente cadastrado ainda")


if __name__ == "__main__":
    main()


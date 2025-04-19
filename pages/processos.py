import streamlit as st
import datetime
from utils.helpers import get_dataframe_with_cols, converter_data, calcular_status_processo, exportar_pdf
from servicos.planilhas import carregar_dados_da_planilha, enviar_dados_para_planilha


def main():
    st.subheader("📄 Cadastro de Processos")

    # Carrega dados
    PROCESSOS = carregar_dados_da_planilha("Processo") or []
    ESCRITORIOS = carregar_dados_da_planilha("Escritorio") or []

    # Formulário de cadastro
    with st.form("form_processo"):
        cliente_nome = st.text_input("Cliente*")
        numero_processo = st.text_input("Número do Processo*")
        tipo_contrato = st.selectbox("Tipo de Contrato*", ["Fixo", "Por Ato", "Contingência"])
        descricao = st.text_area("Descrição do Caso*")
        col1, col2 = st.columns(2)
        with col1:
            valor_total = st.number_input("Valor Total (R$)*", min_value=0.0, format="%.2f")
        with col2:
            valor_movimentado = st.number_input("Valor Movimentado (R$)", min_value=0.0, format="%.2f")
        prazo_inicial = st.date_input("Prazo Inicial*", value=datetime.date.today())
        prazo_final = st.date_input("Prazo Final*", value=datetime.date.today() + datetime.timedelta(days=30))
        houve_movimentacao = st.checkbox("Houve movimentação recente?")
        area = st.selectbox("Área Jurídica*", ["Cível", "Criminal", "Trabalhista", "Previdenciário", "Tributário"])
        link_material = st.text_input("Link do Material Complementar (opcional)")
        encerrado = st.checkbox("Processo Encerrado?")
        if st.form_submit_button("Salvar Processo"):
            if not cliente_nome or not numero_processo or not descricao:
                st.warning("Campos obrigatórios (*) não preenchidos!")
            else:
                novo_processo = {
                    "cliente": cliente_nome,
                    "numero": numero_processo,
                    "contrato": tipo_contrato,
                    "descricao": descricao,
                    "valor_total": valor_total,
                    "valor_movimentado": valor_movimentado,
                    "prazo_inicial": prazo_inicial.strftime("%Y-%m-%d"),
                    "prazo": prazo_final.strftime("%Y-%m-%d"),
                    "houve_movimentacao": houve_movimentacao,
                    "encerrado": encerrado,
                    "responsavel": st.session_state.usuario,
                    "area": area,
                    "link_material": link_material,
                    "data_cadastro": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                if enviar_dados_para_planilha("Processo", novo_processo):
                    PROCESSOS.append(novo_processo)
                    st.success("Processo cadastrado com sucesso!")

    # Lista de processos cadastrados
    st.subheader("Lista de Processos Cadastrados")
    if PROCESSOS:
        df_proc = get_dataframe_with_cols(
            PROCESSOS,
            ["numero", "cliente", "area", "prazo", "responsavel"]
        )
        # Calcula e adiciona status
        df_proc['Status'] = df_proc.apply(
            lambda row: calcular_status_processo(
                converter_data(row.get('prazo')),
                row.get('houve_movimentacao', False),
                row.get('encerrado', False)
            ), axis=1
        )
        # Ordena por status
        status_order = {"🔴 Atrasado": 0, "🟡 Atenção": 1, "🟢 Normal": 2, "🔵 Movimentado": 3, "⚫ Encerrado": 4}
        df_proc['Status_Order'] = df_proc['Status'].map(status_order)
        df_proc = df_proc.sort_values('Status_Order').drop('Status_Order', axis=1)

        st.dataframe(df_proc)

        # Botões de exportação
        col_txt, col_pdf = st.columns(2)
        with col_txt:
            txt = "\n".join([
                f"{p.get('numero','')} | {p.get('cliente','')} | {p.get('area','')} | {p.get('prazo','')} | {p.get('responsavel','')}"
                for p in PROCESSOS
            ])
            st.download_button(
                label="Exportar Processos (TXT)",
                data=txt,
                file_name="processos.txt",
                mime="text/plain"
            )
        with col_pdf:
            texto_pdf = "\n".join([
                f"{p.get('numero','')} | {p.get('cliente','')} | {p.get('area','')} | {p.get('prazo','')} | {p.get('responsavel','')}"
                for p in PROCESSOS
            ])
            pdf_file = exportar_pdf(texto_pdf, nome_arquivo="processos")
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Exportar Processos (PDF)",
                    data=f,
                    file_name="processos.pdf",
                    mime="application/pdf"
                )
    else:
        st.info("Nenhum processo cadastrado ainda")


if __name__ == "__main__":
    main()

import streamlit as st
import plotly.express as px
import datetime
from utils.helpers import converter_data, calcular_status_processo, get_dataframe_with_cols
from servicos.planilhas import carregar_dados_da_planilha


def main():
    st.subheader("📋 Painel de Controle de Processos")
    
    # Carrega dados
    PROCESSOS = carregar_dados_da_planilha("Processo") or []
    CLIENTES = carregar_dados_da_planilha("Cliente") or []

    # Filtros
    with st.expander("🔍 Filtros", expanded=True):
        col1, col2, col3 = st.columns(3)
        filtro_area = st.selectbox(
            "Área", ["Todas"] + sorted(set(p.get("area", "") for p in PROCESSOS)),
            index=0
        )
        filtro_status = st.selectbox(
            "Status", ["Todos", "🔴 Atrasado", "🟡 Atenção", "🟢 Normal", "🔵 Movimentado", "⚫ Encerrado"]
        )
        filtro_escritorio = st.selectbox(
            "Escritório", ["Todos"] + sorted(set(p.get("escritorio", "") for p in PROCESSOS)),
            index=0
        )

    # Aplica filtros
    visiveis = []
    for p in PROCESSOS:
        status = calcular_status_processo(
            converter_data(p.get("prazo")),
            p.get("houve_movimentacao", False),
            encerrado=p.get("encerrado", False)
        )
        if (filtro_area == "Todas" or p.get("area") == filtro_area) and \
           (filtro_escritorio == "Todos" or p.get("escritorio") == filtro_escritorio) and \
           (filtro_status == "Todos" or status == filtro_status):
            p["Status"] = status
            visiveis.append(p)

    # Métricas
    total = len(visiveis)
    atrasados = sum(1 for p in visiveis if p["Status"] == "🔴 Atrasado")
    atencao = sum(1 for p in visiveis if p["Status"] == "🟡 Atenção")
    movimentados = sum(1 for p in visiveis if p["Status"] == "🔵 Movimentado")
    encerrados = sum(1 for p in visiveis if p["Status"] == "⚫ Encerrado")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total", total)
    col2.metric("Atrasados", atrasados)
    col3.metric("Atenção", atencao)
    col4.metric("Movimentados", movimentados)
    col5.metric("Encerrados", encerrados)

    # Gráfico de pizza
    if total > 0:
        fig = px.pie(
            values=[atrasados, atencao, movimentados, encerrados, total - (atrasados + atencao + movimentados + encerrados)],
            names=["Atrasados", "Atenção", "Movimentados", "Encerrados", "Outros"],
            title="Distribuição dos Processos"
        )
        st.plotly_chart(fig)

    # Tabela de processos
    st.subheader("📋 Lista de Processos")
    if visiveis:
        df = get_dataframe_with_cols(visiveis, ["numero", "cliente", "area", "prazo", "responsavel", "Status"])
        st.dataframe(df)
    else:
        st.info("Nenhum processo encontrado com os filtros aplicados")


# Permite execução direta
if __name__ == "__main__":
    main()

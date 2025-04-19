import streamlit as st
import datetime
from servicos.planilhas import carregar_dados_da_planilha


def main():
    st.subheader("📜 Histórico de Processos + Consulta TJMG")
    
    # Carrega dados de histórico
    HISTORICO_PETICOES = carregar_dados_da_planilha("Historico_Peticao") or []

    # Consulta de histórico interno
    num_proc = st.text_input("Digite o número do processo para consultar o histórico")
    if num_proc:
        historico_filtrado = [h for h in HISTORICO_PETICOES if h.get("numero") == num_proc]
        if historico_filtrado:
            st.write(f"{len(historico_filtrado)} registro(s) encontrado(s) para o processo {num_proc}:")
            for item in historico_filtrado:
                with st.expander(f"{item.get('tipo','')} - {item.get('data','')} - {item.get('cliente_associado','')}" , expanded=False):
                    st.write(f"**Responsável:** {item.get('responsavel','')}  ")
                    st.write(f"**Escritório:** {item.get('escritorio','')}  ")
                    st.text_area("Conteúdo", value=item.get("conteudo",""), key=item.get('data',''), disabled=True)
        else:
            st.info("Nenhum histórico encontrado para esse processo.")

    # Iframe de consulta externa
    st.markdown("**Consulta TJMG (iframe)**")
    iframe_html = '''
<div style="overflow: auto; height:600px;">
  <iframe src="https://www.tjmg.jus.br/portal-tjmg/processos/andamento-processual/"
          style="width:100%; height:100%; border:none;"
          scrolling="yes">
  </iframe>
</div>
'''
    st.components.v1.html(iframe_html, height=600)


if __name__ == "__main__":
    main()


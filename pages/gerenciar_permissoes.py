import streamlit as st
import pandas as pd
from servicos.planilhas import carregar_dados_da_planilha, enviar_dados_para_planilha


def main():
    st.subheader("🔧 Gerenciar Permissões de Funcionários")

    # Carrega lista de funcionários
    FUNCIONARIOS = carregar_dados_da_planilha("Funcionario") or []
    if not FUNCIONARIOS:
        st.info("Nenhum funcionário cadastrado.")
        return

    # Exibe tabela de funcionários
    df = pd.DataFrame(FUNCIONARIOS)
    st.dataframe(df)

    # Seleciona funcionário
    nomes = df["nome"].tolist()
    selecionado = st.selectbox("Funcionário", nomes)

    # Define novas áreas permitidas
    novas_areas = st.multiselect(
        "Áreas Permitidas", ["Cível", "Criminal", "Trabalhista", "Previdenciário", "Tributário"]
    )

    if st.button("Atualizar Permissões"):
        atualizado = False
        area_str = ", ".join(novas_areas)
        # Atualiza lista local e session_state
        for func in FUNCIONARIOS:
            if func.get("nome") == selecionado:
                func["area"] = area_str
                atualizado = True
                # Também atualiza o estado de sessão
                for key, user in st.session_state.USERS.items():
                    if user.get("username") == func.get("usuario"):
                        st.session_state.USERS[key]["area"] = area_str
        if atualizado:
            payload = {"nome": selecionado, "area": area_str, "atualizar": True}
            if enviar_dados_para_planilha("Funcionario", payload):
                st.success("Permissões atualizadas com sucesso!")
            else:
                st.error("Falha ao atualizar permissões.")
        else:
            st.warning("Não foi possível localizar o funcionário selecionado.")


if __name__ == "__main__":
    main()


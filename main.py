import streamlit as st

def main():
    # Título e descrição
    st.title("💻 Job Scheduler - MATA82")
    st.markdown(
        """
        <h4 style="color: gray;">Um sistema simples de escalonamento de tarefas.</h4>
        <p>🔹 Desenvolvido por <b>Carlos Eduardo</b> e <b>João Paulo Rios</b>.</p>
        <p>🔹 Professor responsável: <b>Paul Denis Etienne Regnier</b>.</p>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Opções")
        st.write("Configure seu job scheduler abaixo.")
        st.divider()


if __name__ == "__main__":
    main()
import streamlit as st
import plotly.figure_factory as ff
import pandas as pd

def main():
    # Alterando o título da página
    st.set_page_config(page_title="Job Scheduler - MATA82", page_icon="📅")

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
        st.write("Configure seu Job Scheduler abaixo.")
        st.divider()

    # Dados simulados para o escalonamento de jobs
    jobs = [
        {"Task": "Job 1", "Start": 0, "Finish": 3},  # Job 1 executa do tempo 0 ao 3
        {"Task": "Job 2", "Start": 3, "Finish": 6},  # Job 2 executa do tempo 3 ao 6
        {"Task": "Job 3", "Start": 6, "Finish": 9},  # Job 3 executa do tempo 6 ao 9
        {"Task": "Job 1", "Start": 9, "Finish": 12},  # Job 1 é retomado do tempo 9 ao 12
    ]

    # Criando o DataFrame para o gráfico de Gantt
    df = pd.DataFrame(jobs)

    # Criando o gráfico de Gantt
    fig = ff.create_gantt(
        df,
        index_col="Task",
        show_colorbar=True,
        bar_width=0.4,
        showgrid_x=True,
        showgrid_y=True,
        title="Escalonamento de Jobs",
        group_tasks=True,
    )

    fig.update_xaxes(type="linear", title_text="Tempo")
    fig.update_yaxes(title_text="Jobs")

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
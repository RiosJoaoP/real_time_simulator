import streamlit as st
import plotly.graph_objects as go
import time
import random

def main():
    st.set_page_config(page_title="Job Scheduler - MATA82", page_icon="💻")

    if "jobs" not in st.session_state:
        st.session_state.jobs = []

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
        algorithm = st.selectbox("Escolha o Algoritmo de Escalonamento", ["Rate Monotonic", "Earliest Deadline First"])
        st.divider()

        st.subheader("Adicionar Novo Job")
        task_name = st.text_input("Nome da Tarefa")
        period = st.number_input("Período", min_value=1, value=5)
        cost = st.number_input("Custo", min_value=1, value=2)
        if st.button("Adicionar Job"):
            if task_name.strip():
                st.session_state.jobs.append({"Task": task_name, "Period": period, "Cost": cost})

        st.subheader("Remover Job")
        if st.session_state.jobs:
            job_to_remove = st.selectbox("Escolha um job para remover", [job["Task"] for job in st.session_state.jobs])
            if st.button("Remover Job"):
                st.session_state.jobs = [job for job in st.session_state.jobs if job["Task"] != job_to_remove]

        if st.button("Limpar Simulação"):
            st.session_state.jobs = []
            # draw_empty_chart(chart_placeholder)

    st.subheader("📋 Tabela de Jobs")
    st.table(st.session_state.jobs)

    # Lista de jobs
    jobs = [
        {"Task": "Job 1", "Start": 0, "Finish": 3},
        {"Task": "Job 2", "Start": 3, "Finish": 6},
        {"Task": "Job 3", "Start": 6, "Finish": 9},
        {"Task": "Job 1", "Start": 12, "Finish": 15},
    ]

    # Atribuir cores únicas para cada job
    task_colors = {}
    colors = ["blue", "red", "green", "purple", "orange", "cyan", "pink"]
    random.shuffle(colors)
    for job in jobs:
        if job["Task"] not in task_colors:
            task_colors[job["Task"]] = colors[len(task_colors) % len(colors)]

    chart_placeholder = st.empty()
    job_traces = []
    current_time = 0
    max_time = max(job["Finish"] for job in jobs)

    # Escalonamento de jobs - Simulação
    while current_time <= max_time:
        fig = go.Figure()

        for trace in job_traces:
            fig.add_trace(trace)

        active_job = next((job for job in jobs if job["Start"] <= current_time < job["Finish"]), None)
        if active_job:
            task_name = active_job["Task"]
            start_time = active_job["Start"]

            new_trace = go.Bar(
                x=[current_time - start_time],
                y=[task_name],
                base=start_time,
                orientation='h',
                marker=dict(color=task_colors[task_name])
            )
            fig.add_trace(new_trace)
            job_traces.append(new_trace)

        fig.add_shape(
            type="line",
            x0=current_time,
            x1=current_time,
            y0=-0.5,
            y1=len(set(job["Task"] for job in jobs)) - 0.5,
            line=dict(color="white", width=2, dash="dash"),
        )

        fig.update_layout(
            title="Escalonamento de Jobs",
            xaxis_title="Tempo",
            yaxis_title="Jobs",
            xaxis=dict(range=[0, max_time]),
            yaxis=dict(categoryorder="category descending"),
            barmode="overlay",
            showlegend=False
        )

        chart_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.1)
        current_time += 0.1

if __name__ == "__main__":
    main()

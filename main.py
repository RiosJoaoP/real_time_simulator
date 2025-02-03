import streamlit as st
import plotly.graph_objects as go
import time
import random

def main():
    st.set_page_config(page_title="Job Scheduler - MATA82", page_icon="📅")

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

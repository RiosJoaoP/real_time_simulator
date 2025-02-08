import streamlit as st
import plotly.graph_objects as go
import time
import random
import pandas as pd
from io import BytesIO

from scheduling import schedule, Job
from utils import least_common_multiple

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
        period = st.number_input("Período", min_value=1, value=5)
        cost = st.number_input("Custo", min_value=1, value=2)
        if st.button("Adicionar Job"):
            new_task_name = f"T{len(st.session_state.jobs) + 1}"
            st.session_state.jobs.append({"Task": new_task_name, "Period": period, "Cost": cost})

        st.divider()
        st.subheader("Remover Job")
        if st.session_state.jobs:
            job_to_remove = st.selectbox("Escolha um job para remover", [job["Task"] for job in st.session_state.jobs])
            if st.button("Remover Job"):
                st.session_state.jobs = [job for job in st.session_state.jobs if job["Task"] != job_to_remove]
                # Renomear tarefas para manter sequência
                for i, job in enumerate(st.session_state.jobs):
                    job["Task"] = f"T{i + 1}"

        if st.button("Limpar Simulação"):
            st.session_state.jobs = []

    # Espaço reservado para o gráfico e alertas
    chart_placeholder = st.empty()
    alert_placeholder = st.empty()
    table_header_placeholder = st.empty()
    table_placeholder = st.empty()
    download_placeholder = st.empty()

    # Função para atualizar o gráfico
    def update_chart():
        jobs = [Job(job["Cost"], job["Period"], job["Task"], i+1) for i, job in enumerate(st.session_state.jobs)]
        
        # Executar o agendamento
        cycles = 2 * least_common_multiple([job.period for job in jobs])
        scheduled_jobs, deadline_missed_time = schedule(jobs, cycles, method="RM" if algorithm == "Rate Monotonic" else "EDF")

        if deadline_missed_time is not None:
            alert_placeholder.error(f"⚠️ Deadline perdida no tempo {deadline_missed_time}")

        task_colors = {}
        colors = ["blue", "red", "green", "purple", "orange", "cyan", "pink"]
        random.shuffle(colors)
        for job in scheduled_jobs:
            if job["Task"] not in task_colors:
                task_colors[job["Task"]] = colors[len(task_colors) % len(colors)]

        job_traces = []
        current_time = 0
        max_time = max(job["Finish"] for job in scheduled_jobs)
        mmc = least_common_multiple([job.period for job in jobs])

        while current_time <= max_time:
            fig = go.Figure()
            
            for trace in job_traces:
                fig.add_trace(trace)

            active_job = next((job for job in scheduled_jobs if job["Start"] <= current_time < job["Finish"]), None)
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
                y1=len(set(job["Task"] for job in scheduled_jobs)) - 0.5,
                line=dict(color="white", width=2, dash="dash"),
            )
            
            fig.add_shape(
                type="line",
                x0=mmc,
                x1=mmc,
                y0=-0.5,
                y1=len(set(job["Task"] for job in scheduled_jobs)) - 0.5,
                line=dict(color="yellow", width=2, dash="dot"),
                name="MMC"
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

            if deadline_missed_time is not None and current_time >= deadline_missed_time:
                break
        
        # Exibir tabela com o schedule ordenada por Start Time
        df = pd.DataFrame(scheduled_jobs).sort_values(by="Start")
        table_placeholder.dataframe(df, hide_index=True)
        table_header_placeholder.subheader("📊 Tabela de Escalonamento")

        # Adicionar opção para download com título antes do botão
        csv = df.to_csv(index=False).encode('utf-8')
        download_placeholder.download_button("📥 Baixar CSV", data=csv, file_name="schedule.csv", mime="text/csv")

    # Tabela de Jobs e Botão de Iniciar Animação
    if st.session_state.jobs:
        st.subheader("🗉 Tabela de Jobs")
        st.dataframe(st.session_state.jobs, hide_index=True)

        # Botão para iniciar a animação
        if st.button("Iniciar Animação"):
            alert_placeholder.empty()
            update_chart()
    else:
        st.info("Adicione pelo menos um job para visualizar a tabela e iniciar a simulação.")

if __name__ == "__main__":
    main()
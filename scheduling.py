from operator import attrgetter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CYCLES = 20

class SystemClock:
    """Gerencia o tempo global do sistema."""
    TIME = 0
    TIME_STATUS = False

    @classmethod
    def tick(cls):
        if not cls.TIME_STATUS:
            cls.TIME += 1
        cls.TIME_STATUS = False

class Scheduler:
    """Classe base para os escalonadores EDF e RM."""
    
    def __init__(self, jobs, attribute, reverse):
        self.jobs = self.sort_jobs(jobs, attribute, reverse)
        self.curr_jobs = self.jobs.copy()
        self.attribute = attribute
        self.reverse = reverse

    @staticmethod
    def sort_jobs(jobs, attribute, reverse=True):
        return sorted(jobs, key=attrgetter(attribute), reverse=reverse)

    def check_jobs(self):
        """Verifica quais tarefas precisam ser despertadas."""
        for job in self.jobs:
            if job.wake():
                self.add_job(job)
                job.update_deadline()
        self.curr_jobs = self.sort_jobs(self.curr_jobs, self.attribute, self.reverse)

    def remove_job(self, job):
        self.curr_jobs.remove(job)

    def add_job(self, job):
        self.curr_jobs.append(job)
        self.curr_jobs = self.sort_jobs(self.curr_jobs, self.attribute, self.reverse)

    def update_time_to_deadline(self):
        for job in self.jobs:
            job.update_deadline()

    def run(self, cycles):
        """Método base para execução dos escalonadores."""
        while SystemClock.TIME < cycles:
            self.check_jobs()
            if self.curr_jobs:
                curr_job = self.curr_jobs[0]
                job_status = curr_job.run()
                if curr_job.finished():
                    self.remove_job(curr_job)
                if not job_status:
                    print(f"Uma deadline foi perdida em T={SystemClock.TIME}!")
                    return SystemClock.TIME  # Retorna o tempo em que a deadline foi perdida
            SystemClock.tick()
            self.update_time_to_deadline()
        return None  # Retorna None se nenhuma deadline foi perdida

class EarliestDeadlineFirst(Scheduler):
    """Escalonador EDF (Menor deadline tem maior prioridade)."""
    
    def __init__(self, jobs):
        super().__init__(jobs, 'to_deadline', reverse=False)

class RateMonotonic(Scheduler):
    """Escalonador RM (Menor período tem maior prioridade)."""
    
    def __init__(self, jobs):
        super().__init__(jobs, 'rm_priority', reverse=True)

class Processor:
    """Processador que executa os escalonadores."""
    
    def __init__(self, jobs, cycles=180):
        self.jobs = jobs
        self.cycles = cycles

    def edf(self):
        return EarliestDeadlineFirst(self.jobs).run(self.cycles)

    def rm(self):
        return RateMonotonic(self.jobs).run(self.cycles)

class Job:
    """Classe que representa uma tarefa periódica."""

    def __init__(self, duration, period, name, pid, priority=0):
        self.duration = duration
        self.period = period
        self.priority = priority
        self.rm_priority = 1 / period
        self.deadline = period
        self.runtime = 0
        self.ran = []
        self.active = True
        self.name = name
        self.to_deadline = period - SystemClock.TIME
        self.deadlines = []
        self.pid = pid

    def wake(self):
        """Reativa a tarefa periodicamente."""
        if SystemClock.TIME % self.period == 0 and not self.active:
            print(f'T={SystemClock.TIME} Reiniciando {self.name}')
            self.runtime = 0
            self.active = True
            self.deadline = SystemClock.TIME + self.period
            return True
        return False

    def run(self):
        """Executa a tarefa."""
        if not self.finished():
            SystemClock.TIME_STATUS = True
            self.ran.append(SystemClock.TIME)
            print(f'T={SystemClock.TIME} Executando {self.name}, tempo={self.runtime}')
            self.runtime += 1
            SystemClock.TIME += 1
            if self.check_deadline():
                return False
            self.update_deadline()
        return True

    def finished(self):
        """Verifica se a tarefa foi concluída."""
        if self.runtime >= self.duration:
            self.active = False
            print(f'T={SystemClock.TIME-1} Finalizada {self.name}')
            return True
        return False

    def check_deadline(self):
        """Verifica se a tarefa perdeu a deadline."""
        self.deadlines.append(self.deadline)
        if SystemClock.TIME > self.deadline:
            print(f'Atenção! {self.name} perdeu a deadline em T={SystemClock.TIME}.')
            return True
        return False

    def update_deadline(self):
        """Atualiza o tempo restante para a deadline."""
        self.to_deadline = self.deadline - SystemClock.TIME

def schedule(jobs, cycles, method="RM"):
    SystemClock.TIME = 0
    processor = Processor(jobs, cycles)
    
    if method == "EDF":
        deadline_missed_time = processor.edf()  # Retorna o tempo em que a deadline foi perdida
    else:
        deadline_missed_time = processor.rm()  # Retorna o tempo em que a deadline foi perdida

    times = []
    for job in jobs:
        for value in job.ran:
            times.append({"Job": job.name, "Start": value, "Finish": value + 1, "Resource": "Running", "PID": job.pid})
        for value in job.deadlines:
            times.append({"Job": job.name, "Start": value, "Finish": value + 0.3, "Resource": "Deadline", "PID": job.pid})

    df = pd.DataFrame(times)
    df["Delta"] = df["Finish"] - df["Start"]
    df.sort_values(by="Start", inplace=True)

    jobs = df[df["Resource"] == "Running"]
    schedule = []
    
    for _, row in jobs.iterrows():
        schedule.append({"Task": row["Job"], "Start": row["Start"], "Finish": row["Finish"]})
    
    grouped = []
    schedule_sorted = sorted(schedule, key=lambda x: (x['Task'], x['Start']))
    
    for entry in schedule_sorted:
        if not grouped or grouped[-1]['Task'] != entry['Task'] or grouped[-1]['Finish'] < entry['Start']:
            grouped.append(entry)
        else:
            grouped[-1]['Finish'] = entry['Finish']
    
    return grouped, deadline_missed_time
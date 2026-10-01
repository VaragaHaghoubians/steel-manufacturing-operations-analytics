"""Four recruiter-friendly chart exports with explicit units and simulation labels."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def create_figures(machine, daily, downtime, defects, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    def save(fig, name):
        fig.tight_layout()
        fig.savefig(output/f'{name}.png', dpi=180, bbox_inches='tight')
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(10,4.8))
    ranked = machine.sort_values('oee')
    ax.barh(ranked['machine_id'], ranked['oee'], color='#0369a1')
    ax.set_xlim(0,1)
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.set(xlabel='OEE', title='OEE by machine | synthetic six-month simulation')
    save(fig,'oee_by_machine')
    fig, ax = plt.subplots(figsize=(10,4.8))
    ax.bar(downtime['downtime_reason'], downtime['lost_time_min']/60, color='#0369a1')
    ax.set(ylabel='Lost planned time (hours)', title='Downtime Pareto | setup included separately')
    ax.tick_params(axis='x', rotation=30)
    second = ax.twinx()
    second.plot(downtime['downtime_reason'], downtime['cumulative_share'], color='#ea580c', marker='o')
    second.set_ylim(0,1.05)
    second.yaxis.set_major_formatter(PercentFormatter(1))
    second.set_ylabel('Cumulative share')
    save(fig,'downtime_pareto')
    fig, ax = plt.subplots(figsize=(10,4.8))
    ax.barh(defects['defect_type'][::-1], defects['scrap_quantity'][::-1], color='#b45309')
    ax.set(xlabel='Scrapped process-stage units',title='Scrap by attributed defect | synthetic data')
    save(fig,'scrap_by_defect')
    fig, ax = plt.subplots(figsize=(10,4.8))
    ax.plot(daily['date'], daily['planned_quantity'],label='Plan',color='#64748b')
    ax.plot(daily['date'], daily['actual_quantity'],label='Actual',color='#0369a1')
    ax.set(ylabel='Process-stage units (not finished goods)',title='Daily production plan vs actual')
    ax.legend()
    fig.autofmt_xdate()
    save(fig,'production_plan_vs_actual')

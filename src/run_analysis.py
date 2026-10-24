"""Run comparison, convergence, runtime, and damping sensitivity experiments."""
import csv
from pathlib import Path
from time import perf_counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from suspension import Parameters, simulate, analytical, rmse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
P = Parameters()

def save_rows(name, headers, rows):
    with (OUT/name).open('w', newline='') as f:
        writer=csv.writer(f);writer.writerow(headers);writer.writerows(rows)

def main():
    fig,ax=plt.subplots(figsize=(8,4.5))
    t0=np.linspace(0,5,1001)
    ax.plot(t0,analytical(t0,P)[:,0],label='Analytical',lw=2)
    for method in ['Euler','RK4']:
        t,y=simulate(method,P,dt=0.1)
        ax.plot(t,y[:,0],label=f'{method}, dt=0.1 s',ls='--' if method=='Euler' else ':')
    ax.set(xlabel='Time (s)',ylabel='Displacement (m)',title='Suspension free vibration: solver comparison')
    ax.grid(alpha=.3);ax.legend();fig.tight_layout();fig.savefig(OUT/'solver_comparison.png',dpi=170);plt.close(fig)

    rows=[]
    steps=[0.2,0.1,0.05,0.025,0.0125]
    for method in ['Euler','RK4']:
        for dt in steps:
            t,y=simulate(method,P,dt=dt)
            ref=analytical(t,P)
            start=perf_counter()
            for _ in range(30):simulate(method,P,dt=dt)
            runtime=(perf_counter()-start)/30*1000
            rows.append([method,dt,len(t),rmse(y[:,0],ref[:,0]),float(np.max(np.abs(y[:,0]-ref[:,0]))),runtime])
    save_rows('convergence.csv',['method','dt_s','points','displacement_rmse_m','max_absolute_error_m','runtime_ms'],rows)
    fig,ax=plt.subplots(figsize=(7,4.5))
    for method in ['Euler','RK4']:
        subset=[r for r in rows if r[0]==method]
        ax.loglog([r[1] for r in subset],[r[3] for r in subset],'o-',label=method)
    ax.set(xlabel='Step size (s)',ylabel='Displacement RMSE (m)',title='Convergence against analytical solution')
    ax.grid(alpha=.3,which='both');ax.legend();fig.tight_layout();fig.savefig(OUT/'convergence.png',dpi=170);plt.close(fig)
    sensitivity=[]
    fig,ax=plt.subplots(figsize=(8,4.5))
    for c in [600,1500,3000]:
        p=Parameters(damping=c)
        t,y=simulate('RK4',p,dt=.01)
        sensitivity.append([c, float(np.max(np.abs(y[:,0]))),float(np.max(np.abs(y[:,1])))])
        ax.plot(t,y[:,0],label=f'c={c} N s/m')
    save_rows('sensitivity.csv',['damping_Ns_per_m','peak_absolute_displacement_m','peak_absolute_velocity_m_per_s'],sensitivity)
    ax.set(xlabel='Time (s)',ylabel='Displacement (m)',title='Damping sensitivity (RK4)')
    ax.legend();ax.grid(alpha=.3);fig.tight_layout();fig.savefig(OUT/'damping_sensitivity.png',dpi=170);plt.close(fig)
    print('Generated results in',OUT)
    for row in rows: print(row)

if __name__=='__main__':main()

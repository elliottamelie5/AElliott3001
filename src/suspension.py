"""Single-degree-of-freedom suspension free-vibration model and numerical solvers."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Parameters:
    """Model parameters: mass (kg), stiffness (N/m), damping (N s/m)."""
    mass: float = 300.0
    stiffness: float = 18000.0
    damping: float = 1500.0

    def __post_init__(self):
        if min(self.mass, self.stiffness) <= 0 or self.damping < 0:
            raise ValueError('mass and stiffness must be positive; damping nonnegative')

def derivative(t, state, p):
    """Return [velocity, acceleration] for m*x''+c*x'+k*x=0."""
    x, v = state
    return np.array([v, -(p.damping*v + p.stiffness*x)/p.mass], dtype=float)

def euler_step(t, y, h, p):
    """Advance state one time step using explicit Euler."""
    return y + h*derivative(t, y, p)

def rk4_step(t, y, h, p):
    """Advance state one time step using classical fourth-order Runge-Kutta."""
    k1 = derivative(t, y, p)
    k2 = derivative(t+h/2, y+h*k1/2, p)
    k3 = derivative(t+h/2, y+h*k2/2, p)
    k4 = derivative(t+h, y+h*k3, p)
    return y + h*(k1+2*k2+2*k3+k4)/6

def simulate(method, p=Parameters(), initial=(0.08, 0.0), duration=5.0, dt=0.05):
    """Integrate displacement and velocity. Return time and two-column states.

    Raises ValueError for invalid inputs. The last interval ends at duration.
    """
    if duration <= 0 or dt <= 0 or not np.isfinite([duration, dt]).all():
        raise ValueError('duration and dt must be finite and positive')
    state = np.asarray(initial, dtype=float)
    if state.shape != (2,) or not np.isfinite(state).all():
        raise ValueError('initial state must contain two finite numbers')
    if method not in ('Euler', 'RK4'):
        raise ValueError('method must be Euler or RK4')
    step = euler_step if method == 'Euler' else rk4_step
    n = int(np.ceil(duration/dt))
    times = np.linspace(0, duration, n+1) if np.isclose(n*dt,duration) else np.r_[np.arange(n)*dt, duration]
    times = np.unique(np.clip(times,0,duration))
    states = np.zeros((len(times), 2))
    states[0] = state
    for i in range(len(times)-1):
        states[i+1] = step(times[i], states[i], times[i+1]-times[i], p)
    return times, states

def analytical(t, p=Parameters(), initial=(0.08, 0.0)):
    """Exact displacement and velocity for underdamped free vibration."""
    alpha = p.damping/(2*p.mass)
    omega0 = np.sqrt(p.stiffness/p.mass)
    if alpha >= omega0:
        raise ValueError('analytical formula supports only underdamped systems')
    wd = np.sqrt(omega0**2-alpha**2)
    x0,v0 = initial
    a=x0; b=(v0+alpha*x0)/wd
    t=np.asarray(t,dtype=float)
    ex=np.exp(-alpha*t)
    x=ex*(a*np.cos(wd*t)+b*np.sin(wd*t))
    v=ex*((-alpha*a+wd*b)*np.cos(wd*t)+(-alpha*b-wd*a)*np.sin(wd*t))
    return np.column_stack([x,v])

def rmse(a,b):
    """Root-mean-square error of equally shaped arrays."""
    return float(np.sqrt(np.mean((np.asarray(a)-np.asarray(b))**2)))

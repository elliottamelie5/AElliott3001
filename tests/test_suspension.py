"""Verification tests for solver and physical model."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pytest
from suspension import Parameters, simulate, analytical, rmse

def test_initial_condition():
    for method in ('Euler','RK4'):
        t,y=simulate(method)
        assert t[0]==0 and np.allclose(y[0],[.08,0])

def test_rk4_more_accurate_than_euler():
    t,a=simulate('Euler',dt=.05)
    _,b=simulate('RK4',dt=.05)
    ref=analytical(t)
    assert rmse(b[:,0],ref[:,0]) < rmse(a[:,0],ref[:,0])

def test_refinement_reduces_error():
    for method in ('Euler','RK4'):
        t1,y1=simulate(method,dt=.1)
        t2,y2=simulate(method,dt=.05)
        assert rmse(y2[:,0],analytical(t2)[:,0]) < rmse(y1[:,0],analytical(t1)[:,0])

def test_analytical_initial_velocity():
    assert np.allclose(analytical([0],initial=(.05,.2))[0],[.05,.2])

def test_invalid_inputs():
    with pytest.raises(ValueError):Parameters(mass=-1)
    with pytest.raises(ValueError):simulate('Euler',dt=0)
    with pytest.raises(ValueError):simulate('invalid')
    with pytest.raises(ValueError):analytical([0],Parameters(damping=10000))

def test_energy_nonincreasing_for_rk4():
    p=Parameters();_,y=simulate('RK4',p,dt=.01)
    energy=.5*p.stiffness*y[:,0]**2+.5*p.mass*y[:,1]**2
    assert np.all(np.diff(energy)<1e-9)

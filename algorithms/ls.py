import logging
from pydoc import cli
from time import clock_settime

import dolfinx
from dolfinx.fem import (
    Constant,
    Function,
    FunctionSpace,
    dirichletbc,
    form,
    assemble_scalar,
    locate_dofs_geometrical,
)
from petsc4py import PETSc
from slepc4py import SLEPc
from dolfinx.cpp.log import log, LogLevel
import ufl
import numpy as np
from pathlib import Path

import mpi4py
import numpy as np
from ufl import Measure


comm = mpi4py.MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# create a class naled linesearch

class LineSearch(object):
    def __init__(self, energy, state):
        super(LineSearch, self).__init__()
        # self.u_0 = dolfin.Vector(state['u'].vector())
        # self.alpha_0 = dolfin.Vector(state['alpha'].vector())

        self.energy = energy
        self.state = state
        # initial state

        self.V_u = state["u"].function_space
        self.V_alpha = state["alpha"].function_space
        self.mesh = self.V_u.mesh

        self.u0 = Function(state['u'].function_space)
        self.alpha0 = Function(state['alpha'].function_space)


    def search(self, state, perturbation, m=3, mode=0, hmax=.1):
        dx = Measure("dx", domain=self.mesh) #-> volume measure

        # self._state = state

        v = perturbation["v"]
        beta = perturbation["beta"]

        u_0 = Function(state["u"].function_space)
        alpha_0 = Function(state["alpha"].function_space)
        
        state["u"].vector.copy(u_0.vector)
        state["alpha"].vector.copy(alpha_0.vector)
        
        en_0 = assemble_scalar(form(self.energy))

        # get admissible interval
        # discretise interval for polynomial interpolation at order m

        htest = np.linspace(0, hmax, np.int32(m+1))
        energies_1d = []

        # compute energy at discretised points
        for h in htest:
            with state["u"].vector.localForm() as u_local, \
                state["alpha"].vector.localForm() as alpha_local, \
                v.vector.localForm() as v_local, \
                beta.vector.localForm() as beta_local:

                u_local.array[:] = u_local.array[:] + h*v_local.array[:]
                alpha_local.array[:] = alpha_local.array[:] + h*beta_local.array[:]
        
            state["alpha"].vector.ghostUpdate(addv=PETSc.InsertMode.INSERT_VALUES, mode=PETSc.ScatterMode.FORWARD)
            state["u"].vector.ghostUpdate(addv=PETSc.InsertMode.INSERT_VALUES, mode=PETSc.ScatterMode.FORWARD)

            en_h = assemble_scalar(form(self.energy))
            energies_1d.append(en_h-en_0)


        # compute polynomial coefficients

        z = np.polyfit(htest, energies_1d, m)
        p = np.poly1d(z)

        # compute minimum of polynomial
        if m==2:
            log(LogLevel.INFO, 'Line search using quadratic interpolation')
            h_opt = - z[1]/(2*z[0])
        else:
            log(LogLevel.INFO, 'Line search using polynomial interpolation (order {})'.format(m))
            h = np.linspace(0, 10*hmax, 30)
            h_opt = h[np.argmin(p(h))]

        return h_opt, (0, hmax), energies_1d
        # return arg-minimum of 1d energy-perturbations

    
    def admissible_interval(self, state, perturbation, alpha_lb, bifurcation):
        """Computes the admissible interval for the line search, based on 
        the solution to the rate problem"""

        alpha = state["alpha"]
        # beta = perturbation["beta"]
        beta = bifurcation[1]

        one = max(1., max(alpha.vector[:]))
        upperbound = one
        lowerbound = alpha_lb


        # positive
        mask = np.int32(np.where(beta.vector[:]>0)[0])

        hp2 = (one-alpha.vector[mask])/beta.vector[mask]  if len(mask)>0 else [np.inf]
        hp1 = (alpha_lb.vector[mask]-alpha.vector[mask])/beta.vector[mask]  if len(mask)>0 else [-np.inf]
        hp = (max(hp1), min(hp2))

        # negative
        mask = np.int32(np.where(beta.vector[:]<0)[0])

        hn2 = (one-alpha.vector[mask])/beta.vector[mask] if len(mask)>0 else [-np.inf]
        hn1 = (alpha_lb.vector[mask]-alpha.vector[mask])/beta.vector[mask]  if len(mask)>0 else [np.inf]
        hn = (max(hn2), min(hn1))

        hmax = np.array(np.min([hp[1], hn[1]]))
        hmin = np.array(np.max([hp[0], hn[0]]))

        hmax_glob = np.array(0.0,'d')
        hmin_glob = np.array(0.0,'d')

        comm.Allreduce(hmax, hmax_glob, op=mpi4py.MPI.MIN)
        comm.Allreduce(hmin, hmin_glob, op=mpi4py.MPI.MAX)

        hmax = float(hmax_glob)
        hmin = float(hmin_glob)


        if hmin>0:
            log(LogLevel.INFO, 'Line search troubles: found hmin>0')
            return (0., 0.)
        if hmax==0 and hmin==0:
            log(LogLevel.INFO, 'Line search failed: found zero step size')
            # import pdb; pdb.set_trace()
            return (0., 0.)
        if hmax < hmin:
            log(LogLevel.INFO, 'Line search failed: optimal h* not admissible')
            return (0., 0.)
            # get next perturbation mode

        assert hmax > hmin, 'hmax > hmin'

        return (hmin, hmax)

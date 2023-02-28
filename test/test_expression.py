#!/usr/bin/env python3
from re import A
import numpy as np
import yaml
import json
from pathlib import Path
import sys
import os
from mpi4py import MPI
import petsc4py
from petsc4py import PETSc
import dolfinx
import dolfinx.plot
from dolfinx import log
import ufl
import numpy as np
sys.path.append("../")
from utils.plots import plot_energies
from utils import ColorPrint
import matplotlib.pyplot as plt
import matplotlib.tri as tri

from models import DamageElasticityModel as Brittle
from algorithms.am import AlternateMinimisation

from meshes.pacman import mesh_pacman
from dolfinx.common import Timer, list_timings, TimingType

from ufl import Circumradius, FacetNormal, SpatialCoordinate

import logging

logging.basicConfig(level=logging.DEBUG)

import dolfinx
import dolfinx.plot
from dolfinx.io import XDMFFile, gmshio
from dolfinx.fem import (
    Constant,
    Expression,
    # UserExpression,
    Function,
    FunctionSpace,
    assemble_scalar,
    dirichletbc,
    form,
    locate_dofs_geometrical,
    locate_dofs_topological,
    set_bc,
)
import dolfinx.mesh
from dolfinx.mesh import CellType, locate_entities_boundary

import ufl

from mpi4py import MPI
import petsc4py
from petsc4py import PETSc
import sys
import yaml

sys.path.append("../")
from solvers import SNESSolver
from algorithms.so import StabilitySolver

# ///////////


petsc4py.init(sys.argv)
comm = MPI.COMM_WORLD

# Mesh on node model_rank and then distribute
model_rank = 0

with open("output/test_notch/parameters.yml") as f:
    parameters = yaml.load(f, Loader=yaml.FullLoader)


# Get mesh parameters
_r = parameters["geometry"]["r"]
_omega = parameters["geometry"]["omega"]
tdim = parameters["geometry"]["geometric_dimension"]
_nameExp = parameters["geometry"]["geom_type"]
ell_ = parameters["model"]["ell"]
lc = ell_ / 1.0

parameters["geometry"]["lc"] = lc


# Get geometry model
geom_type = parameters["geometry"]["geom_type"]

# Create the mesh of the specimen with given dimensions

gmsh_model, tdim = mesh_pacman(geom_type, parameters["geometry"], tdim)

# Get mesh and meshtags
mesh, mts, fts = gmshio.model_to_mesh(gmsh_model, comm, model_rank, tdim)

from dolfinx.mesh import CellType, create_unit_square
# mesh = create_unit_square(MPI.COMM_WORLD, 3, 3, CellType.triangle)


outdir = "output"
prefix = os.path.join(outdir, "test_notch")
if comm.rank == 0:
    Path(prefix).mkdir(parents=True, exist_ok=True)

with XDMFFile(comm, f"{prefix}/{_nameExp}.xdmf", "w", encoding=XDMFFile.Encoding.HDF5) as file:
    file.write_mesh(mesh)


# Function spaces
element_u = ufl.VectorElement("Lagrange", mesh.ufl_cell(), degree=1, dim=tdim)
V_u = FunctionSpace(mesh, element_u)

# Define the state
u = Function(V_u, name="Displacement")
u_ = Function(V_u, name="Boundary Displacement")
zero_u = Function(V_u, name="   Boundary Displacement")

# Data

uD = Function(V_u)

class Asymptotic():
    def __init__(self, omega, **kwargs):
        self.omega = omega

    def value_shape(self):
        return (tdim,)
    
    def eval(self, value, x):
        self.theta = ufl.atan_2(x[1], x[0])
        # print(self.theta)
        value[0] = x[0]
        value[1] = x[1]
        

class MyExpr:
    def __init__(self, a, **kwargs):
        self.a = a

    def eval(self, value, x):
        value[0] = x[0] + self.a

class MyVExpr:
    def __init__(self, t, **kwargs):
        self.t = t

    def value_shape(self):
        return (2,)
    
    def eval(self, x):
        theta = np.arctan2(x[1], x[0])
        _r = np.sqrt(x[0]**2 + x[1]**2)
        e_n = (x[0], x[1]) / _r
        e_t = (-x[1], x[0]) / _r
        return e_n + e_t
        

def singularity_exp(omega):
    """Exponent of singularity, λ\in [1/2, 1]
    lmbda : = sin(2*lmbda*(pi - omega)) + lmbda*sin(2(pi-lmbda)) = 0"""
    from sympy import nsolve, pi, sin, symbols

    x = symbols('x')

    return nsolve(
        sin(2*x*(pi - omega)) + x*sin(2*(pi-omega)), 
        x, .5)

import sympy as sp

class NotchOpening:
    """Asymptotic displacement for a notch of opening omega,
    Linear elasticity, cf. Leguillon and Sanchez-Palencia (1987)
    """

    def __init__(self, t, ω, **kwargs):
        self.t = t
        self.lmbda = singularity_exp(ω)
        self.ω = ω

    def eff(self, λ, ω):
        """auxiliary function"""
        return ( (1+λ) * np.sin( (1+λ) * (np.pi - ω) ) ) / ( (1-λ) * np.sin( (1-λ) * (np.pi - ω) ) )

    def F(self, Θ):
        """auxiliary Function"""
        λ = self.lmbda
        coeff = self.eff(λ, self.ω)
        return (np.pi)**(λ - 1) * (np.cos( (1+λ) * Θ)- coeff * np.cos((1-λ) * Θ))/(1-coeff)

    def Fprime(self, Θ):
        _F = self.F(Θ)
        return sp.diff(_F, Θ)

    def Fpprime(self, Θ):
        _F = self.F(Θ)
        return sp.diff(_F, Θ, 2)

    def Fppprime(self, Θ):
        _F = self.F(Θ)
        return sp.diff(_F, Θ, 3)

    def value_shape(self):
        return (2,)
    
    def eval(self, x):
        Θ = np.arctan2(x[1], x[0])
        _r = np.sqrt(x[0]**2 + x[1]**2)
        e_n = (x[0], x[1]) / _r
        e_t = (-x[1], x[0]) / _r
        return e_n + e_t



f = MyExpr(1, domain=mesh)
fv = MyVExpr(1, domain=mesh)
fv = NotchOpening(1, _omega, domain=mesh)


n = FacetNormal(mesh)
t = ufl.as_vector([n[1], -n[0]])

bd_facets = locate_entities_boundary(
    mesh, dim=1, marker=lambda x: np.greater((x[0]**2 + x[1]**2), _r**2)
    )

bd_facets = locate_entities_boundary(
    mesh, dim=1, marker=lambda x: np.greater((x[0]**2 + x[1]**2), _r**2)
    )
  
bd_cells = locate_entities_boundary(mesh, dim=1, marker = lambda x: np.greater(x[0], 0.5))

bd_facets2 = locate_entities_boundary(
    mesh, dim=1, marker=lambda x: np.greater(x[0], 0.)
    )


bd_facets3 = locate_entities_boundary(mesh, dim=1, marker = lambda x: np.full(x.shape[1], True, dtype=bool))
boundary_dofs = locate_dofs_topological(V_u, mesh.topology.dim - 1, bd_facets3)

u_expr = n + t

boundary_facets = dolfinx.mesh.exterior_facet_indices(mesh.topology)
cells0 = dolfinx.mesh.locate_entities(mesh, 2, lambda x: x[0] <= 0.5)

assert((boundary_facets == bd_facets3).all())

# uD.interpolate(fv.eval)
_x = ufl.SpatialCoordinate(mesh)


def _expression(x):
    values = np.zeros((tdim, x.shape[1]))
    values[0] = 1.
    values[1] = 0.
    return values

uD.interpolate(_expression)


with XDMFFile(comm, f"{prefix}/{_nameExp}.xdmf", "a", encoding=XDMFFile.Encoding.HDF5) as file:
    file.write_function(uD, 0)

from utils.viz import (
    plot_mesh,
    plot_profile,
    plot_scalar,
    plot_vector
)
import pyvista
from pyvista.utilities import xvfb

xvfb.start_xvfb(wait=0.05)
pyvista.OFF_SCREEN = True

plotter = pyvista.Plotter(
    title="Test Viz",
    window_size=[1600, 600],
    shape=(1, 1),
)

plt.figure()
ax = plot_mesh(mesh)
fig = ax.get_figure()
fig.savefig(f"{prefix}/test_mesh.png")

_plt = plot_vector(uD, plotter)
logging.critical('plotted vector')
_plt.screenshot(f"{prefix}/test_vector.png")

__import__('pdb').set_trace()


dirichletbc(uD, boundary_dofs, V_u)

# Test derivatives of an expression

# x = ufl.SpatialCoordinate(mesh)
# f = ufl.as_vector((x[0], x[1]))
# expr = Expression(f, V_u.element.interpolation_points())


# TODO: Plot field to check
# import pyvista

# from utils.viz import plot_vector
# from pyvista.utilities import xvfb

# xvfb.start_xvfb(wait=0.05)
# pyvista.OFF_SCREEN = True

# plotter = pyvista.Plotter(
#     title="Test Viz",
#     window_size=[1600, 600],
#     shape=(1, 2),
# )

# _plt = plot_vector(u, plotter, subplot=(0, 1))


_asym = Asymptotic(omega = parameters["geometry"]["omega"])
__import__('pdb').set_trace()

uD.interpolate(_asym)


uD.interpolate(lambda x: [np.zeros_like(x[0]), np.zeros_like(x[1])])
uD.interpolate(_asym)


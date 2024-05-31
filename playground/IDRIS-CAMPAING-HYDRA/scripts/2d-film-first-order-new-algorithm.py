#!/usr/bin/env python3
import hashlib
import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from libidris.core import (elastic_energy_density_film, damage_energy_density, stress)
from libidris.core import a
from libidris.core import setup_output_directory, save_parameters, create_function_spaces_2d, initialize_functions

import dolfinx
import dolfinx.mesh
import dolfinx.plot
import numpy as np
import pandas as pd
import petsc4py
import pyvista
import ufl
import yaml
from dolfinx.common import list_timings
from dolfinx.fem import (Constant, Function, assemble_scalar, dirichletbc,
                         form, locate_dofs_geometrical, set_bc)
from dolfinx.fem.petsc import assemble_vector, set_bc
from dolfinx.io import XDMFFile, gmshio
from irrevolutions.algorithms.am import HybridSolver
from irrevolutions.solvers.function import vec_to_functions
from irrevolutions.utils import (ColorPrint, ResultsStorage, Visualization,
                                 _logger, _write_history_data, history_data,
                                 norm_H1, norm_L2)
from irrevolutions.utils.plots import (plot_AMit_load, plot_energies,
                                       plot_force_displacement)
from irrevolutions.utils.viz import (plot_mesh, plot_profile, plot_scalar,
                                     plot_vector)
from irrevolutions.models import BrittleMembraneOverElasticFoundation as ThinFilm
from irrevolutions.meshes.primitives import mesh_circle_gmshapi

from mpi4py import MPI
from petsc4py import PETSc
from pyvista.utilities import xvfb

from irrevolutions.utils.viz import _plot_bif_spectrum_profiles

petsc4py.init(sys.argv)
comm = MPI.COMM_WORLD

# Mesh on node model_rank and then distribute
model_rank = 0


class ThinFilmWithImposedDisplacement(ThinFilm):
    
    def __init__(self, model_parameters={}, u_0=0):
        """
        Initialie material parameters.
        * Sound material:
            - E_0: sound Young modulus
            - K: elastic foundation modulus
            - nu_0: sound plasticity ratio
            - u_0: substrate deformation
            - sig_d_0: sound damage yield stress
            - ell: internal length
            - k_res: residual stiffness
        """
        # Initialize elastic parameters
        super().__init__(model_parameters)
        if model_parameters:
            self.model_parameters.update(model_parameters)
        
        # Initialize the damage parameters
        self.w1 = self.model_parameters["w1"]
        self.ell = self.model_parameters["ell"]
        self.ell_e = self.model_parameters["ell_e"]
        self.k_res = self.model_parameters["k_res"]
        self.u_0 = u_0

    def elastic_energy_density(self, state):
        """
        Returns the elastic energy density from the state.
        """
        # Parameters
        alpha = state["alpha"]
        u = state["u"]
        u_0 = self.u_0 
        return self.elastic_energy_density_strain(
            self.eps(u), alpha) + self.elastic_foundation_density(u - u_0)

def run_computation(parameters, storage=None):
    _nameExp = parameters["geometry"]["geom_type"]
    R = parameters["geometry"]["R"]
    lc = parameters["model"]["ell"] / parameters["geometry"]["mesh_size_factor"]    
    
    # Get geometry model
    parameters["geometry"]["geom_type"]

    gmsh_model, tdim = mesh_circle_gmshapi(_nameExp,
                        R,
                        lc,
                        tdim=2,
                        order=1,
                        msh_file=None,
                        comm=MPI.COMM_WORLD)
    mesh, mts, fts = gmshio.model_to_mesh(gmsh_model, comm, model_rank, tdim)

    outdir = os.path.join(os.path.dirname(__file__), "output")

    prefix = setup_output_directory(storage, parameters, outdir)

    signature = save_parameters(parameters, prefix)
    
    with XDMFFile(
        comm, f"{prefix}/{_nameExp}.xdmf", "w", encoding=XDMFFile.Encoding.HDF5
    ) as file:
        file.write_mesh(mesh)

    # Functional Setting

    V_u, V_alpha = create_function_spaces_2d(mesh)
    u, u_, alpha, β, v, state = initialize_functions(V_u, V_alpha)

    # Bounds
    alpha_ub = dolfinx.fem.Function(V_alpha, name="UpperBoundDamage")
    alpha_lb = dolfinx.fem.Function(V_alpha, name="LowerBoundDamage")

    # Define the state
    zero_u = Function(V_u, name="BoundaryUnknown")
    zero_u.interpolate(lambda x: (np.zeros_like(x[0]), np.zeros_like(x[1])))
    
    u_zero = Function(V_u, name="InelasticDisplacement")

    def radial_field(x):
        # r = np.sqrt(x[0]**2 + x[1]**2)
        u_x = x[0]
        u_y = x[1]
        return np.array([u_x, u_y])

    eps_t = dolfinx.fem.Constant(mesh, np.array(1., dtype=PETSc.ScalarType))
    u_zero.interpolate(lambda x: radial_field(x) * eps_t)
    
    tdim = mesh.topology.dim
    fdim = tdim - 1
    mesh.topology.create_connectivity(fdim, tdim)
    boundary_facets = dolfinx.mesh.exterior_facet_indices(mesh.topology)
    
    alpha_lb.interpolate(lambda x: np.zeros_like(x[0]))
    alpha_ub.interpolate(lambda x: np.ones_like(x[0]))

    u_boundary_dofs = dolfinx.fem.locate_dofs_topological(V_u, fdim, boundary_facets)

    for f in [u, zero_u, u_zero, alpha_lb, alpha_ub]:
        f.vector.ghostUpdate(
            addv=PETSc.InsertMode.INSERT, mode=PETSc.ScatterMode.FORWARD
        )

    bcs_u = [dirichletbc(u_zero, u_boundary_dofs)]

    bcs_alpha = []
    bcs = {"bcs_u": bcs_u, "bcs_alpha": bcs_alpha}
    
    # Measures
    dx = ufl.Measure("dx", domain=mesh)
    model = ThinFilmWithImposedDisplacement(parameters["model"], u_0=u_zero)
    
    f = Constant(mesh, np.array([0, 0], dtype=PETSc.ScalarType))
    external_work = ufl.dot(f, state["u"]) * dx
    total_energy = model.total_energy_density(state) * dx - external_work

    load_par = parameters["loading"]
    loads = np.linspace(load_par["min"], load_par["max"], load_par["steps"])

    equilibrium = HybridSolver(
        total_energy,
        state,
        bcs,
        bounds=(alpha_lb, alpha_ub),
        solver_parameters=parameters.get("solvers"),
    )

    for i_t, t in enumerate(loads):
        eps_t.value = t
        u_zero.interpolate(lambda x: radial_field(x) * eps_t)
        u_zero.vector.ghostUpdate(
            addv=PETSc.InsertMode.INSERT, mode=PETSc.ScatterMode.FORWARD
        )

        alpha.vector.copy(alpha_lb.vector)
        alpha_lb.vector.ghostUpdate(
            addv=PETSc.InsertMode.INSERT, mode=PETSc.ScatterMode.FORWARD
        )

        _logger.critical(f"-- Solving for t = {t:3.2f} --")
        with dolfinx.common.Timer(f"~First Order: Equilibrium") as timer:
            equilibrium.solve(alpha_lb)
        
        with dolfinx.common.Timer(f"~Postprocessing and Vis") as timer:
            if comm.rank == 0:
                plot_energies(history_data, file=f"{prefix}/{_nameExp}_energies.pdf")
                plot_AMit_load(history_data, file=f"{prefix}/{_nameExp}_it_load.pdf")
                # plot_force_displacement(
                #     history_data, file=f"{prefix}/{_nameExp}_stress-load.pdf"
                # )

            xvfb.start_xvfb(wait=0.05)
            pyvista.OFF_SCREEN = True

            # plotter = pyvista.Plotter(
            #     title="Profiles",
            #     window_size=[800, 600],
            #     shape=(1, 1),
            # )

            # tol = 1e-3
            # xs = np.linspace(0 + tol, parameters["geometry"]["Lx"] - tol, 101)
            # points = np.zeros((3, 101))
            # points[0] = xs

            # _plt, data = plot_profile(
            #     state["alpha"],
            #     points,
            #     plotter,
            #     lineproperties={
            #         "c": "k",
            #         "label": f"$\\alpha$ with $\ell$ = {parameters['model']['ell']:.2f}"
            #     },
            # )
            # ax = _plt.gca()
            # _plt, data = plot_profile(
            #     state["u"],
            #     points,
            #     plotter,
            #     fig=_plt,
            #     ax=ax,
            #     lineproperties={
            #         "c": "g",
            #         "label": "$u$",
            #         "marker": "o",
            #     },
            # )
            # _plt, data = plot_profile(
            #     u_zero,
            #     points,
            #     plotter,
            #     fig=_plt,
            #     ax=ax,
            #     lineproperties={
            #         "c": "r",
            #         "lw": 3,
            #         "label": "$u_0$"
            #     },
            # )
            # _plt.legend()
            # _plt.title("Solution state")
            # # ax.set_ylim(-2.1, 2.1)
            # ax.axhline(0, color="k", lw=.5)
            # _plt.savefig(f"{prefix}/state_profile-{i_t}.png")

            fracture_energy = comm.allreduce(
                assemble_scalar(form(damage_energy_density(state, parameters) * dx)),
                op=MPI.SUM,
            )
            elastic_energy = comm.allreduce(
                assemble_scalar(form(elastic_energy_density_film(state, parameters, u_zero) * dx)),
                op=MPI.SUM,
            )
            # _F = assemble_scalar(form(stress(state, parameters)))
        
        
        # compute the average of the alpha field
        import matplotlib
        # fig_state, ax1 = matplotlib.pyplot.subplots()
        
        # with dolfinx.common.Timer(f"~Postprocessing and Vis") as timer:
        #     file=f"{prefix}/{_nameExp}_state_t.pdf"
        #     _alpha_t = (assemble_scalar( form(1 * dx)))**(-1) \
        #         * assemble_scalar(form(alpha * dx))
        #     _u_t = t
        #     time_series.append(t)
        #     alpha_values.append(_alpha_t)
        #     displacement_tip_values.append(_u_t)

        #     ax1.set_title("State", fontsize=12)
        #     ax1.set_xlabel(r"Load", fontsize=12)
        #     ax1.plot(
        #         time_series,
        #         alpha_values,
        #         color="tab:blue",
        #         linestyle="-",
        #         linewidth=1.0,
        #         markersize=4.0,
        #         marker="o",
        #     )
        #     history_data["F"].append(_F)
            
        #     ax2 = ax1.twinx()
        #     ax2.plot(
        #         time_series,
        #         displacement_tip_values,
        #         color="black",
        #         linestyle="-",
        #         linewidth=2.0,
        #         markersize=4.0,
        #         marker="o",
        #     )
        #     fig_state.tight_layout()
        #     fig_state.savefig(file)
        #     matplotlib.pyplot.close()

        with dolfinx.common.Timer(f"~Output and Storage") as timer:
            with XDMFFile(
                comm, f"{prefix}/{_nameExp}.xdmf", "a", encoding=XDMFFile.Encoding.HDF5
            ) as file:
                file.write_function(u, t)
                file.write_function(alpha, t)

            if comm.rank == 0:
                a_file = open(f"{prefix}/time_data.json", "w")
                json.dump(history_data, a_file)
                a_file.close()


            _write_history_data(
            equilibrium = equilibrium,
            bifurcation = None,
            stability = None,
            history_data = history_data,
            t=t,
            stable = np.nan,
            energies = [elastic_energy, fracture_energy],
        )
        
    print(pd.DataFrame(history_data).drop(columns=["cone_data", "eigs_ball",
                                                   "eigs_cone", "stable", "unique", "inertia"]))
    return history_data, {}, state

def load_parameters(file_path, ndofs, model="at1"):
    """
    Load parameters from a YAML file.

    Args:
        file_path (str): Path to the YAML parameter file.

    Returns:
        dict: Loaded parameters.
    """
    import hashlib

    with open(file_path) as f:
        parameters = yaml.load(f, Loader=yaml.FullLoader)

    parameters["model"]["model_dimension"] = 2
    parameters["model"]["model_type"] = "2D"

    if model == "at2":
        parameters["model"]["at_number"] = 2
        parameters["loading"]["min"] = 0.0
        parameters["loading"]["max"] = 3.0
        parameters["loading"]["steps"] = 30
    else:
        parameters["model"]["at_number"] = 1
        parameters["loading"]["min"] = 0.0
        parameters["loading"]["max"] = 1.3
        parameters["loading"]["steps"] = 10
        
    parameters["geometry"]["geom_type"] = "circle"
    parameters["geometry"]["mesh_size_factor"] = 2

    parameters["stability"]["cone"]["cone_max_it"] = 400000
    parameters["stability"]["cone"]["cone_atol"] = 1e-6
    parameters["stability"]["cone"]["cone_rtol"] = 1e-6
    parameters["stability"]["cone"]["scaling"] = 1e-3

    parameters["model"]["w1"] = 1
    parameters["model"]["ell"] = 0.1
    parameters["model"]["k_res"] = 0.0
    parameters["model"]["mu"] = 1
    parameters["model"]["ell_e"] = .3
    # parameters["model"]["kappa"] = (.3)**(-2)

    signature = hashlib.md5(str(parameters).encode("utf-8")).hexdigest()

    return parameters, signature

if __name__ == "__main__":
    # Set the logging level
    logging.basicConfig(level=logging.INFO)

    # Load parameters
    parameters, signature = load_parameters(
        os.path.join(os.path.dirname(__file__), "../parameters", "2d_parameters.yaml"), 
        ndofs=100, 
        model="at1")
    
    # Run computation
    _storage = f"../output/2d-film-first-new-hybrid-redundant/MPI-{MPI.COMM_WORLD.Get_size()}/{signature[0:6]}"
    visualization = Visualization(_storage)

    with dolfinx.common.Timer(f"~Computation Experiment") as timer:
        history_data, _, state = run_computation(parameters, _storage)
    
    from irrevolutions.utils import table_timing_data
    
    tasks = ["~First Order: Equilibrium",
        "~First Order: AltMin-Damage solver",
        "~First Order: AltMin-Elastic solver",
        "~Postprocessing and Vis",
        "~Output and Storage",
        "~Computation Experiment"
        ]
    
    _timings = table_timing_data(tasks)
    visualization.save_table(_timings, "timing_data")
    list_timings(MPI.COMM_WORLD, [dolfinx.common.TimingType.wall])

    ColorPrint.print_bold(f"===================- {signature} -=================")
    ColorPrint.print_bold(f"===================- {_storage} -=================")

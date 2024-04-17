"""
Solve for wave propagation in classical mechanics in the given domain.
"""

import os

import meshio
import numpy as np
import solidspy.assemutil as ass
from scipy.sparse.linalg import eigsh

from .constants import MESHES_FOLDER, SOLUTIONS_FOLDER
from .fem_utils import acoust_tri6
from .gmesher import create_mesh
from .utils import parse_solution_identifier


def load_mesh(mesh_file):
    mesh = meshio.read(mesh_file)

    points = mesh.points
    cells = mesh.cells
    tri6 = cells["triangle6"]
    line3 = cells["line3"]
    npts = points.shape[0]
    nels = tri6.shape[0]

    nodes = np.zeros((npts, 3))
    nodes[:, 1:] = points[:, 0:2]

    # Constraints
    line_nodes = list(set(line3.flatten()))
    cons = np.zeros((npts, 1), dtype=int)
    cons[line_nodes, :] = -1

    # Elements
    elements = np.zeros((nels, 9), dtype=int)
    elements[:, 1] = 2
    elements[:, 3:] = tri6

    return cons, elements, nodes


def solver(geometry_type: str, params: dict, force_reprocess: bool = False):
    solution_id = parse_solution_identifier(geometry_type, params)

    bc_array_file = f"{SOLUTIONS_FOLDER}/{solution_id}-bc_array.csv"
    eigvals_file = f"{SOLUTIONS_FOLDER}/{solution_id}-eigvals.csv"
    eigvecs_file = f"{SOLUTIONS_FOLDER}/{solution_id}-eigvecs.csv"

    # Check if solutions already exist
    if (
        os.path.exists(bc_array_file)
        and os.path.exists(eigvals_file)
        and os.path.exists(eigvecs_file)
        and not force_reprocess
    ):
        # Load existing solutions
        bc_array = np.loadtxt(bc_array_file, delimiter=",")
        eigvals = np.loadtxt(eigvals_file, delimiter=",")
        eigvecs = np.loadtxt(eigvecs_file, delimiter=",")
    else:
        mats = np.array([[1.0]])
        mesh_file = f"{MESHES_FOLDER}/{solution_id}.msh"
        if not os.path.exists(mesh_file) or force_reprocess:
            create_mesh(geometry_type, params, mesh_file)

        cons, elements, nodes = load_mesh(mesh_file)
        # Assembly
        assem_op, bc_array, neq = ass.DME(cons, elements, ndof_node=1, ndof_el_max=6)
        stiff_mat, mass_mat = ass.assembler(
            elements, mats, nodes, neq, assem_op, uel=acoust_tri6
        )

        # Solution
        eigvals, eigvecs = eigsh(stiff_mat, M=mass_mat, k=10, which="LM", sigma=1e-6)

        np.savetxt(bc_array_file, bc_array, delimiter=",")
        np.savetxt(eigvals_file, eigvals, delimiter=",")
        np.savetxt(eigvecs_file, eigvecs, delimiter=",")

    # dev code, add breakpoint and check solution
    # import solidspy.postprocesor as pos
    # sol = pos.complete_disp(bc_array, nodes, eigvecs[:, 0], ndof_node=1)
    # pos.plot_node_field(sol[:, 0], nodes, elements)

    return bc_array, eigvals, eigvecs

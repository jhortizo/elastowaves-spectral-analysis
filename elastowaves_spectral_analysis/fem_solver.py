"""
Solve for wave propagation in classical mechanics in the given domain.
"""

import meshio
import numpy as np
import solidspy.assemutil as ass
from scipy.sparse.linalg import eigsh
from solidspy_uels.solidspy_uels import elast_tri6

from .constants import MATERIAL_PARAMETERS
from .gmesher import create_mesh
from .utils import (
    check_solution_files_exists,
    generate_solution_filenames,
    load_solution_files,
    save_solution_files,
)


def _load_mesh(mesh_file):
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
    cons = np.zeros((npts, 2), dtype=int)
    cons[line_nodes, :] = -1

    # Elements
    elements = np.zeros((nels, 9), dtype=int)
    elements[:, 1] = 2
    elements[:, 3:] = tri6

    return cons, elements, nodes


def _compute_solution(geometry_type: str, params: dict, files_dict: dict):
    mats = [
        MATERIAL_PARAMETERS["E"],
        MATERIAL_PARAMETERS["NU"],
        MATERIAL_PARAMETERS["RHO"],
    ]  # order imposed by elast_tri6

    mats = np.array([mats])

    create_mesh(geometry_type, params, files_dict["mesh"])

    cons, elements, nodes = _load_mesh(files_dict["mesh"])
    # Assembly
    assem_op, bc_array, neq = ass.DME(cons, elements, ndof_node=2, ndof_el_max=12)
    stiff_mat, mass_mat = ass.assembler(
        elements, mats, nodes, neq, assem_op, uel=elast_tri6
    )

    # Solution
    eigvals, eigvecs = eigsh(
        stiff_mat, M=mass_mat, k=stiff_mat.shape[0] - 1, which="SM"
    )

    save_solution_files(bc_array, eigvals, eigvecs, files_dict)

    return bc_array, eigvals, eigvecs, nodes, elements


def retrieve_solution(geometry_type: str, params: dict, force_reprocess: bool = False):
    files_dict = generate_solution_filenames(geometry_type, params)

    if check_solution_files_exists(files_dict) and not force_reprocess:
        bc_array, eigvals, eigvecs = load_solution_files(files_dict)
        _, elements, nodes = _load_mesh(files_dict["mesh"])

    else:
        bc_array, eigvals, eigvecs, nodes, elements = _compute_solution(
            geometry_type, params, files_dict
        )

    return bc_array, eigvals, eigvecs, nodes, elements

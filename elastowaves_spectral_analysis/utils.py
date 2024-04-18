import os

import numpy as np

from .constants import MESHES_FOLDER, SIDE_TO_MESH_SIZE_RATIO, SOLUTIONS_FOLDER


def _parse_solution_identifier(geometry_type, params):
    "Returnss strign associated with run parameters"

    params_str = [
        str(this_key) + "_" + str(this_value).replace(".", "")
        for this_key, this_value in params.items()
    ]  # TODO: if value is 1.0, it is left as 10, which may be confusing later...

    filename = geometry_type + "-" + "-".join(params_str)

    return filename


def generate_solution_filenames(geometry_type, params):
    "Returns filenames for solution files"
    solution_id = _parse_solution_identifier(geometry_type, params)
    bc_array_file = f"{SOLUTIONS_FOLDER}/{solution_id}-bc_array.csv"
    eigvals_file = f"{SOLUTIONS_FOLDER}/{solution_id}-eigvals.csv"
    eigvecs_file = f"{SOLUTIONS_FOLDER}/{solution_id}-eigvecs.csv"
    mesh_file = f"{MESHES_FOLDER}/{solution_id}.msh"
    return {
        "bc_array": bc_array_file,
        "eigvals": eigvals_file,
        "eigvecs": eigvecs_file,
        "mesh": mesh_file,
    }


def check_solution_files_exists(files_dict):
    "Checks if solution files exist"
    return all([os.path.exists(this_file) for this_file in files_dict.values()])


def load_solution_files(files_dict):
    "Loads solution files"
    bc_array = np.loadtxt(files_dict["bc_array"], delimiter=",", dtype=int)
    bc_array = bc_array.reshape(-1, 1) if bc_array.ndim == 1 else bc_array
    eigvals = np.loadtxt(files_dict["eigvals"], delimiter=",")
    eigvecs = np.loadtxt(files_dict["eigvecs"], delimiter=",")
    return bc_array, eigvals, eigvecs


def save_solution_files(bc_array, eigvals, eigvecs, files_dict):
    "Saves solution files"
    np.savetxt(files_dict["bc_array"], bc_array, delimiter=",")
    np.savetxt(files_dict["eigvals"], eigvals, delimiter=",")
    np.savetxt(files_dict["eigvecs"], eigvecs, delimiter=",")


def square_mesh_params_from_area(area: float):
    "Returns square mesh parameters from area"
    side = (area) ** 0.5
    mesh_size = side / SIDE_TO_MESH_SIZE_RATIO
    return {"side": side, "mesh_size": mesh_size}


def circle_mesh_params_from_area(area: float):
    "Returns circle mesh parameters from area"
    radius = (area / np.pi) ** 0.5
    mesh_size = radius / SIDE_TO_MESH_SIZE_RATIO
    return {"radius": radius, "mesh_size": mesh_size}


def triangle_mesh_params_from_area(area: float):
    "Returns triangle mesh parameters from area"
    cathethus = (2 * area) ** 0.5
    mesh_size = cathethus / SIDE_TO_MESH_SIZE_RATIO
    return {"cathethus": cathethus, "mesh_size": mesh_size}

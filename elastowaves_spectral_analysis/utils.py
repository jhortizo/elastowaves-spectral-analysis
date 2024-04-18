import numpy as np

from .constants import SIDE_TO_MESH_SIZE_RATIO


def parse_solution_identifier(geometry_type, params):
    "Returnss strign associated with run parameters"

    params_str = [
        str(this_key) + "_" + str(this_value).replace(".", "")
        for this_key, this_value in params.items()
    ]  # TODO: if value is 1.0, it is left as 10, which may be confusing later...

    filename = geometry_type + "-" + "-".join(params_str)

    return filename


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

import numpy as np
import matplotlib.pyplot as plt
from elastowaves_spectral_analysis.constants import IMAGES_FOLDER
from elastowaves_spectral_analysis.fem_solver import retrieve_solution

def calculate_params(geometry_type, area):
    if geometry_type == "square":
        side = area**0.5
        mesh_size = side / 10
        params = {"side": side, "mesh_size": mesh_size}
    elif geometry_type == "triangle":
        cathetus = (2 * area) ** 0.5
        mesh_size = cathetus / 10
        params = {"cathetus": cathetus, "mesh_size": mesh_size}
    else:
        raise ValueError("Invalid geometry type")
    return params


def calculate_eigenvalues(geometry_type, area):
    params = calculate_params(geometry_type, area)
    _, eigvals, _, _, _ = retrieve_solution(geometry_type, params)
    return eigvals


def calculate_N(R, eigvals):
    """Return the number of eigenvalues less than R."""
    return np.sum(eigvals < R)


def calculate_slope(x, y):
    return np.sum(x * y) / np.sum(x**2)


def calculate_rsquared(x, y):
    r = np.sum(x * y) / np.sqrt(np.sum(x**2) * np.sum(y**2))
    return r**2


def plot_N_R_behavior(eigvalss, shapes, area_sampling, test_id):
    R = np.min([np.max(eigvals) for eigvals in eigvalss])
    R = np.ceil(R)
    Rs = np.linspace(1, R, 100)

    plt.figure(figsize=(4, 3))
    for eigvals in eigvalss:
        Ns = [calculate_N(R, eigvals) for R in Rs]
        plt.plot(Rs, Ns)

    plt.xlabel("R")
    plt.ylabel("N(R)")
    plt.legend([f"{shape} area={area}" for shape in shapes for area in area_sampling])
    plt.savefig(f"{IMAGES_FOLDER}/N_R_behavior_{test_id}.png", dpi=300)
    plt.show()


def plot_weyls_law_analog(eigvalss, areas_tested, test_id):
    N_R_max = np.array([len(eigvals) / np.max(eigvals) for eigvals in eigvalss])

    slope = calculate_slope(N_R_max, areas_tested)
    r_squared = calculate_rsquared(N_R_max, areas_tested)
    N_R_sample = np.linspace(np.min(N_R_max), np.max(N_R_max), 100)

    plt.figure(figsize=(4, 3))
    plt.plot(N_R_max, areas_tested, "ko", label="Data")
    plt.plot(N_R_sample, slope * N_R_sample, label="Linear Fit")
    plt.xlabel("N(R_max) / R_max")
    plt.ylabel("Area")
    plt.title("Linear Relation between Area and N(R_max) / R_max")
    plt.legend()
    plt.savefig(f"{IMAGES_FOLDER}/weyls_law_analog_{test_id}.png", dpi=300)
    plt.show()

    return slope, r_squared


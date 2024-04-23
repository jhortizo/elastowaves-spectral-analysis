import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from elastowaves_spectral_analysis.constants import IMAGES_FOLDER
from elastowaves_spectral_analysis.fem_solver import retrieve_solution


def _calculate_params(geometry_type, area):
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
    params = _calculate_params(geometry_type, area)
    _, eigvals, _, _, _ = retrieve_solution(geometry_type, params)
    return eigvals


def _calculate_N(R, eigvals):
    """Return the number of eigenvalues less than R."""
    return np.sum(eigvals < R)


def _calculate_slope(x, y):
    return np.sum(x * y) / np.sum(x**2)


def _calculate_rsquared(x, y):
    r = np.sum(x * y) / np.sqrt(np.sum(x**2) * np.sum(y**2))
    return r**2


def _plot_N_R_behavior(eigvalss, shapes, area_sampling, test_id):
    combinations = [(shape, area) for area in area_sampling for shape in shapes]
    colors = ["k", "r", "b", "g", "m", "c"]
    line_styles = ["-", "--", "-.", ":", "-"]

    R = np.min([np.max(eigvals) for eigvals in eigvalss])
    R = np.ceil(R)
    Rs = np.linspace(1, R, 100)

    plt.figure(figsize=(8, 4))
    for i, eigvals in enumerate(eigvalss):
        shape, area = combinations[i]
        shape_id = list(shapes).index(shape)
        line_style = line_styles[shape_id % len(line_styles)]

        area_id = list(area_sampling).index(area)
        color = colors[area_id % len(colors)]

        Ns = [_calculate_N(R, eigvals) for R in Rs]
        plt.plot(Rs, Ns, f"{color}{line_style}")

    plt.xlabel("R")
    plt.ylabel("N(R)")
    plt.legend(
        [f"{shape} area={area}" for shape, area in combinations],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    plt.tight_layout()
    plt.show()
    plt.savefig(f"{IMAGES_FOLDER}/N_R_behavior_{test_id}.png", dpi=300)
    plt.show()


def _plot_weyls_law_analog(
    eigvalss, areas_tested, shapes, area_sampling, test_id, fit_per_shape=False
):
    N_R_max = np.array([len(eigvals) / np.max(eigvals) for eigvals in eigvalss])
    plt.figure(figsize=(6, 4))
    marker_styles = ["o", "s", "D", "^", "v", "P"]
    colors = ["b", "g", "m", "c"]

    combinations = [(shape, area) for area in area_sampling for shape in shapes]
    if fit_per_shape:
        for i, shape in enumerate(shapes):
            color = colors[i % len(colors)]
            shape_id = list(shapes).index(shape)
            marker_style = marker_styles[shape_id]
            shape_eigvalss = [
                eigvals
                for eigvals, (this_shape, _) in zip(eigvalss, combinations)
                if this_shape == shape
            ]
            shape_areas_tested = np.array(
                [area for this_shape, area in combinations if this_shape == shape]
            )
            shape_N_R_max = np.array(
                [len(eigvals) / np.max(eigvals) for eigvals in shape_eigvalss]
            )

            slope = _calculate_slope(shape_N_R_max, shape_areas_tested)
            r_squared = _calculate_rsquared(shape_N_R_max, shape_areas_tested)
            N_R_sample = np.linspace(np.min(shape_N_R_max), np.max(shape_N_R_max), 100)

            plt.plot(
                shape_N_R_max,
                shape_areas_tested,
                f"{color}{marker_style}",
                markersize=5,
            )
            plt.plot(
                N_R_sample,
                slope * N_R_sample,
                label=f"{shape.title()}, slope={slope:.2f}",
                color=color,
            )

            print(f"{shape.title()} slope: {slope}, R^2: {r_squared}")
    else:
        plt.plot(N_R_max, areas_tested, "ko", markersize=5)

    slope = _calculate_slope(N_R_max, areas_tested)
    r_squared = _calculate_rsquared(N_R_max, areas_tested)
    N_R_sample = np.linspace(np.min(N_R_max), np.max(N_R_max), 100)

    plt.plot(N_R_sample, slope * N_R_sample, "r", label=f"Overall, slope={slope:.2f}")
    plt.xlabel(r"N(R_{max}) / R_{max}")
    plt.ylabel(r"A")
    # plt.title("Linear Relation between Area and N(R_max) / R_max")
    plt.legend()
    plt.savefig(f"{IMAGES_FOLDER}/weyls_law_analog_{test_id}.png", dpi=300)
    plt.show()

    print(f"Overall slope: {slope}, R^2: {r_squared}")


def run_analysis(
    area_sampling,
    shapes,
    SCRIPT_NAME,
    fit_per_shape=True,
    plot_N_R_behavior=True,
    plot_weyls_law_analog=True,
):
    combinations = [(shape, area) for area in area_sampling for shape in shapes]
    areas_tested = np.array([combination[1] for combination in combinations])

    eigvalss = []
    for geometry_type, area in tqdm(combinations, desc="Test"):
        eigvals = calculate_eigenvalues(geometry_type, area)
        eigvalss.append(eigvals)

    if plot_N_R_behavior:
        _plot_N_R_behavior(eigvalss, shapes, area_sampling, test_id=SCRIPT_NAME)

    if plot_weyls_law_analog:
        _plot_weyls_law_analog(
            eigvalss,
            areas_tested,
            shapes,
            area_sampling,
            test_id=SCRIPT_NAME,
            fit_per_shape=fit_per_shape,
        )
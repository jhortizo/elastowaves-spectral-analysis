import matplotlib.pyplot as plt
import numpy as np

import solidspy.postprocesor as pos
from elastowaves_spectral_analysis.fem_solver import retrieve_solution
from elastowaves_spectral_analysis.constants import IMAGES_FOLDER

def plot_eigvec(ax, bc_array, nodes, eigvec, elements, eigval):
    sol = pos.complete_disp(bc_array, nodes, eigvec, ndof_node=2)
    field = np.sqrt(sol[:, 0] ** 2 + sol[:, 1] ** 2)
    tri = pos.mesh2tri(nodes, elements)

    ax.tricontourf(tri, field, levels=12)
    ax.axis("off")
    ax.grid(False)

    ax.set_title(
        rf"$\lambda$ = {round(eigval, 1)}",
        loc="left",
        fontsize=8,
        pad=1,
        color="black",

    )


def plot_eigvecs_array(eigvecs_to_plot, geometry_type, params):
    bc_array, eigvals, eigvecs, nodes, elements = retrieve_solution(
        geometry_type, params, force_reprocess=True
    )

    n = int(eigvecs_to_plot**0.5)
    fig, axs = plt.subplots(n, n)

    for i in range(n):
        for j in range(n):
            plot_eigvec(
                axs[i, j],
                bc_array,
                nodes,
                eigvecs[:, i * n + j],
                elements,
                eigvals[i * n + j],
            )

    plt.savefig(f"{IMAGES_FOLDER}/eigvecs_{geometry_type}.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    eigvecs_to_plot = 25
    # geometry_type = "isospectral_1_1"
    # params = {}

    geometry_type = "triangle"
    params = {"cathetus": 1, "mesh_size": 0.1}

    plot_eigvecs_array(eigvecs_to_plot, geometry_type, params)

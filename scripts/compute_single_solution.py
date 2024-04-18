import warnings

import matplotlib.pyplot as plt
import numpy as np

from elastowaves_spectral_analysis.fem_solver import retrieve_solution

warnings.filterwarnings(
    "ignore", "The following kwargs were not used by contour: 'shading'", UserWarning
)  # ignore unimportant warning from solidspy


def plot_eigenvec(bc_array, nodes, eigvec, elements):
    import solidspy.postprocesor as pos

    sol = pos.complete_disp(bc_array, nodes, eigvec, ndof_node=2)
    pos.plot_node_field(sol[:, 0], nodes, elements)  # x component
    pos.plot_node_field(sol[:, 1], nodes, elements)  # y component
    pos.plot_node_field(
        np.sqrt(sol[:, 0] ** 2 + sol[:, 1] ** 2), nodes, elements
    )  # disp. amplitude
    plt.show()


def main():
    geometry_type = "triangle"
    params = {"cathetus": 1.0, "mesh_size": 0.05}
    force_reprocess = False
    n_eigenvec = 2  # to plot

    bc_array, eigvals, eigvecs, nodes, elements = retrieve_solution(
        geometry_type, params, force_reprocess=force_reprocess
    )

    plot_eigenvec(bc_array, nodes, eigvecs[:, n_eigenvec], elements)


if __name__ == "__main__":
    main()

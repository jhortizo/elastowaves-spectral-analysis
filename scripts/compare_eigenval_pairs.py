import numpy as np
import matplotlib.pyplot as plt
import solidspy.postprocesor as pos # noqa: F401

from elastowaves_spectral_analysis.fem_solver import retrieve_solution
from elastowaves_spectral_analysis.constants import IMAGES_FOLDER


def compare_eigenvals():

    eigval_limit = 1000 # take first 1000 eigenvalues
    geometry_types = ["isospectral_1_1", "isospectral_1_2"]

    paramss = [{}, {}]

    eigvalss = []

    for geometry_type, params in zip(geometry_types, paramss):
        _, eigvals, _, _, _ = retrieve_solution(geometry_type, params)
        eigvalss.append(eigvals[:eigval_limit])

    relative_error = (abs(eigvalss[0] - eigvalss[1]) / eigvalss[0]) * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(np.arange(0, len(eigvalss[0]), 1), eigvalss[0], "r--")
    ax1.plot(np.arange(0, len(eigvalss[1]), 1), eigvalss[1], "b-")
    ax1.set_xlabel("Eigenvalue index")
    ax1.set_ylabel(r"$\lambda$")

    ax2.plot(np.arange(0, len(relative_error), 1), relative_error, "g-")
    ax2.set_xlabel("Eigenvalue index")
    ax2.set_ylabel("Relative Error (%)")

    plt.savefig(
        f'{IMAGES_FOLDER}/eigenvals_comparison_{"-".join(geometry_types)}.png', dpi=300
    )
    plt.show()

    avg_relative_error = np.mean(relative_error)
    print(f"Average relative error: {avg_relative_error}")


if __name__ == "__main__":
    compare_eigenvals()

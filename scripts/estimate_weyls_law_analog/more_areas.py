import os

import numpy as np
from tqdm import tqdm

from utils import calculate_eigenvalues, plot_N_R_behavior, plot_weyls_law_analog


def main():
    SCRIPT_NAME = os.path.basename(__file__).split(".")[0]
    area_sampling = np.linspace(1, 100, 20)
    shapes = ["square", "triangle"]

    combinations = [(shape, area) for area in area_sampling for shape in shapes]
    areas_tested = np.array([combination[1] for combination in combinations])

    eigvalss = []
    for geometry_type, area in tqdm(combinations, desc="Test"):
        eigvals = calculate_eigenvalues(geometry_type, area)
        eigvalss.append(eigvals)

    plot_N_R_behavior(eigvalss, shapes, area_sampling, test_id=SCRIPT_NAME)

    slope, r_squared = plot_weyls_law_analog(
        eigvalss, areas_tested, test_id=SCRIPT_NAME
    )

    print(f"Slope: {slope}")
    print(f"R^2: {r_squared}")


if __name__ == "__main__":
    main()

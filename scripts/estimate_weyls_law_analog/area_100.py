import os

import numpy as np
from utils import run_analysis

SCRIPT_NAME = os.path.basename(__file__).split(".")[0]


def main():
    area_sampling = np.array([100])
    shapes = ["square", "triangle"]

    run_analysis(area_sampling, shapes, SCRIPT_NAME, plot_weyls_law_analog=False)


if __name__ == "__main__":
    main()


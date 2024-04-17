
from elastowaves_spectral_analysis.fem_solver import solver

def main():
    geometry_type = "triangle"
    params = {
        'side': 10.0,
        'mesh_size': 1.0
    }
    solver(geometry_type, params)


if __name__ == '__main__':
    main()
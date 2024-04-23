# elastowaves-spectral-analysis

Spectral analysis of the differential operator for wave propagation in linear elastodynamics, by means of its discretization using FEM.

This was done as final project for the course in Classical Mechanics, Master in Applied Mathematics, Universidad EAFIT, 2024-1. The corresponding written report is also in the repository, I suggest you start by checking it to get an idea of what is this is all about.

Every plot in the report is created by running an specific script in the `scripts` folder. 

The folder `elastowaves_spectral_analysis` is a local library which assists the creation of domains meshes and solution of eigenvalue-eigenvector problems within them. The scripts automatically create a `data` folder where the meshes, solutions and images are saved for (usable) caching and analysis.

## How to install

Using [poetry](https://python-poetry.org/), just run:

```bash
poetry install
```




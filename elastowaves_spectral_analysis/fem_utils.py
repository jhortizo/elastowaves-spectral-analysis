"""
Supporting functions for the FEM solver
"""

import numpy as np
import solidspy.femutil as fem
import solidspy.gaussutil as gau


def acoust_diff(r, s, coord, element):
    """
    Interpolation matrices for elements for acoustics

    Parameters
    ----------
    r : float
        Horizontal coordinate of the evaluation point.
    s : float
        Vertical coordinate of the evaluation point.
    coord : ndarray (float)
        Coordinates of the element.

    Returns
    -------
    H : ndarray (float)
        Array with the shape functions evaluated at the point (r, s)
        for each degree of freedom.
    B : ndarray (float)
        Array with the gradient matrix evaluated
        at the point (r, s).
    det : float
        Determinant of the Jacobian.
    """
    N, dNdr = element(r, s)
    N.shape = 1, N.shape[0]
    det, jaco_inv = fem.jacoper(dNdr, coord)
    dNdx = jaco_inv @ dNdr
    return N, dNdx, det


def acoust_tri6(coord, params):
    """
    Triangular element with 6 nodes for acoustics under
    axisymmetric conditions.

    Parameters
    ----------
    coord : coord
        Coordinates of the element.
    params : list
        List with material parameters in the following order:
        [Speed].

    Returns
    -------
    stiff_mat : ndarray (float)
        Local stifness matrix.
    mass_mat : ndarray (float)
        Local mass matrix.
    """

    speed = params
    stiff_mat = np.zeros((6, 6))
    mass_mat = np.zeros((6, 6))
    gpts, gwts = gau.gauss_tri(order=3)
    for cont in range(gpts.shape[0]):
        r = gpts[cont, 0]
        s = gpts[cont, 1]
        H, B, det = acoust_diff(r, s, coord, fem.shape_tri6)
        factor = det * gwts[cont]
        stiff_mat += 0.5 * speed**2 * factor * (B.T @ B)
        mass_mat += 0.5 * factor * (H.T @ H)
    return stiff_mat, mass_mat

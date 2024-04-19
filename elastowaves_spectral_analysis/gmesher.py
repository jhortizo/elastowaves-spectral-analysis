"""
Create meshes programmatically, using gmsh API for python
"""

import gmsh


def _create_square_mesh(side: float, mesh_size: float, mesh_file: str):
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)  # no output in terminal
    gmsh.model.add("square")

    gmsh.option.setNumber("Mesh.Algorithm", 2)  # Delaunay, triangular mesh
    gmsh.option.setNumber(
        "Mesh.ElementOrder", 2
    )  # Order of the elements, 2 means quadratic

    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)

    lc = mesh_size
    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(side, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(side, side, 0, lc)
    p4 = gmsh.model.geo.addPoint(0, side, 0, lc)

    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p4)
    l4 = gmsh.model.geo.addLine(p4, p1)

    cl = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
    gmsh.model.geo.addPlaneSurface([cl])

    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)  # 2 means 2D mesh

    gmsh.write(mesh_file)

    # dev code, add breakpoint and check mesh
    # gmsh.fltk.run()

    gmsh.finalize()


def _create_triangle_mesh(cathetus: float, mesh_size: float, mesh_file: str):
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

    gmsh.model.add("triangle")

    gmsh.option.setNumber("Mesh.Algorithm", 2)
    gmsh.option.setNumber("Mesh.ElementOrder", 2)

    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)

    lc = mesh_size
    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(cathetus, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(0, cathetus, 0, lc)

    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p1)

    cl = gmsh.model.geo.addCurveLoop([l1, l2, l3])
    gmsh.model.geo.addPlaneSurface([cl])
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write(mesh_file)

    # dev code, add breakpoint and check mesh
    # gmsh.fltk.run()
    gmsh.finalize()


def _create_circle_mesh(radius: float, mesh_size: float, mesh_file: str):
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add("circle")

    gmsh.option.setNumber("Mesh.Algorithm", 2)
    gmsh.option.setNumber("Mesh.ElementOrder", 2)

    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)

    lc = mesh_size
    center = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p1 = gmsh.model.geo.addPoint(radius, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(-radius, 0, 0, lc)

    circle1 = gmsh.model.geo.addCircleArc(p1, center, p2)
    circle2 = gmsh.model.geo.addCircleArc(p2, center, p1)

    cl = gmsh.model.geo.addCurveLoop([circle1, circle2])
    gmsh.model.geo.addPlaneSurface([cl])

    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write(mesh_file)
    gmsh.finalize()


def _create_isospectral_1_1(mesh_file: str):
    """
    Create a mesh for the isospectral domain presented
    in https://en.wikipedia.org/wiki/Hearing_the_shape_of_a_drum#/media/File:Isospectral_drums.svg
    (the left one)
    """
    coords = [
        (2, 0),
        (3, 1),
        (3, 2),
        (1, 2),
        (1, 3),
        (0, 2),
        (1, 1),
        (2, 1),
    ]
    mesh_size = 0.1
    _create_mesh_from_coords(coords, mesh_size, mesh_file)


def _create_isospectral_1_2(mesh_file: str):
    """
    Create a mesh for the isospectral domain presented
    in https://en.wikipedia.org/wiki/Hearing_the_shape_of_a_drum
    (the right one)
    """

    coords = [
        (2, 0),
        (2, 1),
        (3, 1),
        (2, 2),
        (1, 2),
        (1, 3),
        (0, 3),
        (0, 2),
    ]
    mesh_size = 0.1
    _create_mesh_from_coords(coords, mesh_size, mesh_file)


def _create_isospectral_2_1(mesh_file: str):
    """
    Create a mesh for the isospectral domain presented
    in https://doi.org/10.1155/S1073792894000437
    (fig4. 7_3, left one)
    """
    h = (3) ** 0.5 / 2
    coords = [
        (0.5, 0),
        (3.5, 0),
        (2.5, 2 * h),
        (2, h),
        (0, h),
    ]
    mesh_size = 0.1
    _create_mesh_from_coords(coords, mesh_size, mesh_file)


def _create_isospectral_2_2(mesh_file: str):
    """
    Create a mesh for the isospectral domain presented
    in https://doi.org/10.1155/S1073792894000437
    (fig4. 7_3, right one)
    """
    h = (3) ** 0.5 / 2
    coords = [
        (0, 0),
        (1, 0),
        (2.5, 3 * h),
        (0.5, 3 * h),
        (1, 2 * h),
    ]
    mesh_size = 0.1
    _create_mesh_from_coords(coords, mesh_size, mesh_file)


def _create_mesh_from_coords(coords, mesh_size, mesh_file):
    """Create a mesh for a given set of coordinates"""
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add("custom")

    gmsh.option.setNumber("Mesh.Algorithm", 2)
    gmsh.option.setNumber("Mesh.ElementOrder", 2)

    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)

    lc = mesh_size
    ps = []
    for coord in coords:
        ps.append(gmsh.model.geo.addPoint(coord[0], coord[1], 0, lc))

    lines = []
    for i in range(len(ps)):
        lines.append(gmsh.model.geo.addLine(ps[i], ps[(i + 1) % len(ps)]))

    cl = gmsh.model.geo.addCurveLoop(lines)
    gmsh.model.geo.addPlaneSurface([cl])

    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)

    gmsh.write(mesh_file)
    gmsh.finalize()


def create_mesh(geometry_type, params, mesh_file):
    mesh_functions = {
        "square": _create_square_mesh,
        "triangle": _create_triangle_mesh,
        "circle": _create_circle_mesh,
        "isospectral_1_1": _create_isospectral_1_1,
        "isospectral_1_2": _create_isospectral_1_2,
        "isospectral_2_1": _create_isospectral_2_1,
        "isospectral_2_2": _create_isospectral_2_2,
    }
    if geometry_type in mesh_functions:
        mesh_functions[geometry_type](**params, mesh_file=mesh_file)
    else:
        raise ValueError(f"Unknown geometry type: {geometry_type}")

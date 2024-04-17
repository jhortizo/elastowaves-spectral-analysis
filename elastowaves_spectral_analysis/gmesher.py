"""
Create meshes programmatically, using gmsh API for python
"""

import gmsh


def create_square_mesh(side: float, mesh_size: float, mesh_file: str):
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


def create_triangle_mesh(cathethus: float, mesh_size: float, mesh_file: str):
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

    gmsh.model.add("square")

    gmsh.option.setNumber("Mesh.Algorithm", 2)
    gmsh.option.setNumber("Mesh.ElementOrder", 2)

    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)

    lc = mesh_size
    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(cathethus, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(0, cathethus, 0, lc)

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


def create_circle_mesh(radius: float, mesh_size: float, mesh_file: str):
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


def create_mesh(geometry_type, params, mesh_file):
    if geometry_type == "square":
        create_square_mesh(params["side"], params["mesh_size"], mesh_file)
    elif geometry_type == "triangle":
        create_triangle_mesh(params["cathetus"], params["mesh_size"], mesh_file)
    elif geometry_type == "circle":
        create_circle_mesh(params["radius"], params["mesh_size"], mesh_file)
    else:
        raise ValueError(f"Unknown geometry type: {geometry_type}")

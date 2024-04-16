"""Create meshes programmatically, using gmsh API for python"""

import gmsh


def create_square_mesh(square_side: float = 1.0, mesh_size: float = 0.2):
    # Initialize gmsh
    gmsh.initialize()

    # Set up a new model
    gmsh.model.add("square")

    ## To use triangles
    gmsh.option.setNumber("Mesh.Algorithm", 2)  # Delaunay

    # # To use quadrangles
    # gmsh.option.setNumber("Mesh.Algorithm", 8)  # Frontal-Delaunay for quadrangles

    # Global mesh size
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)

    # Create points
    lc = mesh_size  # characteristic length of the mesh elements
    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(1, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(1, 1, 0, lc)
    p4 = gmsh.model.geo.addPoint(0, 1, 0, lc)

    # Create lines
    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p4)
    l4 = gmsh.model.geo.addLine(p4, p1)

    # Create Curve Loop and Plane Surface
    cl = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
    gmsh.model.geo.addPlaneSurface([cl])

    # Synchronize the model
    gmsh.model.geo.synchronize()

    # Mesh the model
    gmsh.model.mesh.generate(2)

    # Save the mesh
    gmsh.write("data/meshes/square.msh")

    # Open the GUI to view the mesh (optional, comment out if not needed)
    # gmsh.fltk.run()

    # Finalize gmsh
    gmsh.finalize()



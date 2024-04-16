"""Create meshes programmatically, using gmsh API for python"""

import gmsh


def create_square_mesh(side: float = 1.0, mesh_size: float = 0.2):
    # Initialize gmsh
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

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
    p2 = gmsh.model.geo.addPoint(side, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(side, side, 0, lc)
    p4 = gmsh.model.geo.addPoint(0, side, 0, lc)

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


def create_triangle_mesh(cathethus: float = 1.0, mesh_size: float = 0.2):
    # Initialize gmsh
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

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
    p2 = gmsh.model.geo.addPoint(cathethus, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(0, cathethus, 0, lc)

    # Create lines
    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p1)

    # Create Curve Loop and Plane Surface
    cl = gmsh.model.geo.addCurveLoop([l1, l2, l3])
    gmsh.model.geo.addPlaneSurface([cl])

    # Synchronize the model
    gmsh.model.geo.synchronize()

    # Mesh the model
    gmsh.model.mesh.generate(2)

    # Save the mesh
    gmsh.write("data/meshes/triangle.msh")

    # Open the GUI to view the mesh (optional, comment out if not needed)
    gmsh.fltk.run()

    # Finalize gmsh
    gmsh.finalize()


def create_circle_mesh(radius: float = 1.0, mesh_size: float = 0.2):
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add("circle")

    ## To use triangles
    gmsh.option.setNumber("Mesh.Algorithm", 2)  # Delaunay

    # # To use quadrangles
    # gmsh.option.setNumber("Mesh.Algorithm", 8)  # Frontal-Delaunay for quadrangles

    # Global mesh size
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)

    # Define points
    lc = 0.1  # Characteristic length
    center = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p1 = gmsh.model.geo.addPoint(radius, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(-radius, 0, 0, lc)

    # Define circular arc
    circle1 = gmsh.model.geo.addCircleArc(p1, center, p2)
    circle2 = gmsh.model.geo.addCircleArc(p2, center, p1)

    # Create Curve Loop and Plane Surface
    cl = gmsh.model.geo.addCurveLoop([circle1, circle2])
    gmsh.model.geo.addPlaneSurface([cl])

    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write("data/meshes/circle.msh")
    gmsh.fltk.run()  # Optional: to view the GUI
    gmsh.finalize()

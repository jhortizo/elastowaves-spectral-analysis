import os

MATERIAL_PARAMETERS = {
    "E": 1.0,
    "NU": 0.3,
    "RHO": 1.0,
}

SIDE_TO_MESH_SIZE_RATIO = 10

MESHES_FOLDER = "data/meshes"
SOLUTIONS_FOLDER = "data/solutions"
IMAGES_FOLDER = "data/images"

# Create the folders if they don't exist
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
abs_meshes_folder = os.path.join(current_dir, MESHES_FOLDER)
abs_solutions_folder = os.path.join(current_dir, SOLUTIONS_FOLDER)
abs_images_folder = os.path.join(current_dir, IMAGES_FOLDER)
os.makedirs(abs_meshes_folder, exist_ok=True)
os.makedirs(abs_solutions_folder, exist_ok=True)
os.makedirs(abs_images_folder, exist_ok=True)

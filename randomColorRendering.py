import os
import bpy
import csv
import random

# Get the current folder path
folder_path = '/Users/naiqixiao/Downloads/ALL VOMETRIC SHAPES - UPDATED'

# Get a list of files in the current folder
file_list = os.listdir(folder_path)

# Filter the file list to include only files ending with .fbx
fbx_files = [file for file in file_list if file.endswith('.fbx')]

# Set the output folder path
output_folder = os.path.join(folder_path, "output")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def create_material(name, color):
    # Create a new material
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    return material

def setup_render_settings(output_path):
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'JPEG'  # Set image format
    scene.render.filepath = output_path  # Set output file path

def setup_camera():
    # Add a new camera
    bpy.ops.object.camera_add()
    camera = bpy.context.object

    # Position the camera
    camera.location = (5, -5, 4)
    camera.rotation_euler = (1.1, 0, 0.785)

    # Set the camera as the active camera for the scene
    bpy.context.scene.camera = camera

def setup_light():
    # Add a new light
    bpy.ops.object.light_add(type='SUN')
    light = bpy.context.object

    # Position the light
    light.location = (-2, -5, 4)
    light.data.energy = 5  # Adjust the energy (brightness) as needed

def set_render_background_color(color):
    # Ensure the world uses node-based settings
    world = bpy.data.worlds['World']  # Assuming 'World' is your world data block name
    world.use_nodes = True

    # Get the world node tree and the background node
    node_tree = world.node_tree
    bg_node = node_tree.nodes.get('Background', None)

    # If the background node exists, set its color
    if bg_node:
        bg_node.inputs['Color'].default_value = color

def assign_materials_to_objects(objects):
    for obj in objects:
        if obj.type == 'MESH':
            # Create a unique color for each object
            color = [random.random() for _ in range(3)] + [1.0]  # RGBA
            mat_name = f"Material_{obj.name}"
            material = create_material(mat_name, color)
            # Assign material to object
            if len(obj.data.materials):
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
                
setup_camera()
setup_light()
set_render_background_color((0.9, 0.9, 0.9, 1)) 

# Process each .fbx file
for fbx_file in fbx_files:
    # Import the current file into Blender
    bpy.ops.import_scene.fbx(filepath=os.path.join(folder_path, fbx_file))

    assign_materials_to_objects(bpy.data.objects)
    
    # Set the file name based on the object name
    export_file_name = fbx_file + ".png"

    # Set the output file path
    output_file = os.path.join(output_folder, export_file_name)

    setup_render_settings(output_file)
    
    # Render the scene and save the image
    bpy.ops.render.render(write_still=True)
    
    # Delete all objects in the scene
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
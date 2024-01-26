import os
import bpy
import csv

# Get the current folder path
folder_path = os.chdir('/Users/naiqixiao/Downloads/ALL VOMETRIC SHAPES - UPDATED')

# Get a list of files in the current folder
file_list = os.listdir(folder_path)

# Filter the file list to include only files ending with .fbx
fbx_files = [file for file in file_list if file.endswith('.fbx')]

# Create a CSV file to store the object names
csv_file = open('object_list.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['FBX File', 'Object Name', 'Location', 'Size', 'Rotation'])

# Process each .fbx file
for fbx_file in fbx_files:
    # Your processing code here
    print(f"Processing file: {fbx_file}")
    
    # Import the current file into Blender
    bpy.ops.import_scene.fbx(filepath=fbx_file)

    # Get all objects in the scene
    objects = bpy.data.objects

    # Print the names of all objects
    for obj in objects:
        object_name = obj.name
        # Skip objects with name 'Cube' or 'Light'
        if object_name == 'Camera':
            continue
        print(object_name)
        
        object_size = obj.dimensions
        object_location = obj.location
        object_rotation = obj.rotation_euler
        
        # Write the FBX file name and object name to the CSV file
        csv_writer.writerow([fbx_file, object_name, [object_location.x, object_location.y, object_location.z], [object_size.x, object_size.y, object_size.z], [object_rotation.x, object_rotation.y, object_rotation.z]])

    # Rest of your code...
    # Delete all objects in the scene
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

# Close the CSV file
csv_file.close()

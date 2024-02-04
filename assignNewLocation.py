import bpy
import csv
import os
import random
from mathutils import Vector
from mathutils import Quaternion
from math import radians
import math


# Path to the updated CSV file
csv_file_path = '/Users/naiqixiao/Downloads/updated_object_names_Pumpkin.csv'

# Get the current folder path
folder_path = os.chdir('/Users/naiqixiao/Downloads/ALL VOMETRIC SHAPES - UPDATED')

# Function to import an FBX file
def import_fbx(fbx_file_path):
    bpy.ops.import_scene.fbx(filepath=fbx_file_path)

# Function to update object locations
def update_object_locations(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            obj_name = row['Object Name']
            if row['ObjectType'] == 'base':
                if int(row['AssociatedBaseIndex']) > 1:
                    # remove other base object
                    bpy.data.objects.remove(bpy.data.objects[obj_name])
                else:
                    # keep one base object
                    baseObject = obj_name
            # Assuming 'Location' column contains updated location values as a list
            new_location = eval(row['newLocation'])  # Using eval to convert string list to actual list
            if obj_name in bpy.data.objects:
                bpy.data.objects[obj_name].location = new_location
        
        # return the name of base object
        return baseObject

# New function to randomly hide 3 "part" objects
def show_random_parts(csv_file_path):
    part_objects = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ObjectType'] == 'part':
                obj = bpy.context.scene.objects.get(row['Object Name'])
                if obj:
                    part_objects.append(row['Object Name'])
                    bpy.data.objects[row['Object Name']].hide_viewport = bpy.data.objects[row['Object Name']].hide_render = True
    
    # Randomly select 3 "part" objects to show
    objects_to_show = random.sample(part_objects, min(5, len(part_objects)))
    
    # Hide the selected objects in Blender
    for obj_name in objects_to_show:
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].hide_viewport = bpy.data.objects[obj_name].hide_render = False

def create_material(name, color):
    # Create a new material
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True

    nodes = material.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfHairPrincipled')

    # bsdf = material.node_tree.nodes["Principled Hair BSDF"]
    bsdf.inputs['Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = .80
    bsdf.inputs['Random Roughness'].default_value = .80

    output = nodes.new(type='ShaderNodeOutputMaterial')
    
    # Link the Principled Hair BSDF node to the Material Output
    links = material.node_tree.links
    link = links.new(bsdf.outputs[0], output.inputs[0])
    return material

# New function to assign unique colors to shown objects
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

def image_export(output_path):
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'JPEG'  # Set image format
    scene.render.filepath = output_path  # Set output file path
    # Render the scene and save the image
    bpy.ops.render.render(write_still=True)

def setup_camera():
    # Add a new camera
    bpy.ops.object.camera_add()
    camera = bpy.context.object

    # Position the camera
    camera.location = (2.5, 0, 2)
    camera.rotation_euler = (1.0360409021377563, 0.04162178188562393, 0.738756000995636)

    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512

    # Ensure the aspect ratio is 1:1 by setting the pixel aspect ratio
    bpy.context.scene.render.pixel_aspect_x = 1
    bpy.context.scene.render.pixel_aspect_y = 1

    # Set the camera as the active camera for the scene
    bpy.context.scene.camera = camera

def setup_light():
    # Add a new light
    bpy.ops.object.light_add(type='AREA')
    light = bpy.context.object

    # Position the light
    light.location = (1.7200278043746948, 2.2876501083374023, 2.0)
    light.rotation_mode = "XYZ"
    light.rotation_euler = (-0.19239047169685364, 0.9672511219978333, 0.6540918946266174)
    light.scale = (3.1999998092651367, 3.999999761581421, 2.119999885559082)
    light.data.energy = 96
    light.data.size = 0.44905954599380493

    # Add a new light
    bpy.ops.object.light_add(type='AREA')
    light = bpy.context.object

    # Position the light
    light.location = (0.0, -2.4204671382904053, 2.4167652130126953)
    light.rotation_mode = "XYZ"
    light.rotation_euler = (0.3550497889518738, -0.7058761715888977, 1.0531928539276123)
    light.scale = (3.1999998092651367, 3.999999761581421, 2.119999885559082)
    light.data.energy = 94
    light.data.size = 0.52
    light.data.volume_factor = 0.77

    # Add a new light
    bpy.ops.object.light_add(type='AREA')
    light = bpy.context.object

    # Position the light
    light.location = (3.8642451763153076, 0.2624208927154541, -2.152742385864258)
    light.rotation_mode = "XYZ"
    light.rotation_euler = (3.4780237674713135, -0.94093257188797, -0.3346114754676819)
    light.scale = (3.1999998092651367, 3.999999761581421, 2.119999885559082)
    light.data.energy = 94
    light.data.size = 1.04
    light.data.volume_factor = 0.47


def set_render_background_color(color):
    # Access the current scene's world settings
    world = bpy.context.scene.world
    world.use_nodes = True

    # Get the world node tree and the background node
    bg_node = world.node_tree.nodes.get('Background')

    # If the background node exists, set its color
    if bg_node:
        bg_node.inputs['Color'].default_value = color

def video_export(obj, export_file_name):

    # Optional: Update the render resolution percentage to 100%
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.fps = 24

    # Animation parameters
    start_frame = 1
    mid_frame = 60  # Mid-point of the animation, end of Z-axis rotation
    end_frame = 120  # End of the animation, and Y-axis rotation
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Clear existing animation data
    obj.animation_data_clear()

    # Z-axis rotation keyframes
    obj.rotation_euler[2] = 0  # Start Z-axis rotation
    obj.keyframe_insert(data_path="rotation_euler", index=2, frame=start_frame)

    obj.rotation_euler[2] = 2 * math.pi  # End Z-axis rotation
    obj.keyframe_insert(data_path="rotation_euler", index=2, frame=end_frame)

    # Set the camera's initial position and insert a keyframe
    camera.location.z = 2
    camera.keyframe_insert(data_path="location", index=2, frame=mid_frame+1)  # index=2 for the Z-axis

    # Set the camera's final position and insert a keyframe
    camera.location.z = -1.5
    camera.keyframe_insert(data_path="location", index=2, frame=end_frame)

    # # Y-axis rotation keyframes
    # obj.rotation_euler[1] = 0  # Start Y-axis rotation (reset to initial if needed)
    # obj.keyframe_insert(data_path="rotation_euler", index=1, frame=mid_frame+1)  # Start just after Z rotation ends

    # obj.rotation_euler[1] = 2 * math.pi  # End Y-axis rotation
    # obj.keyframe_insert(data_path="rotation_euler", index=1, frame=end_frame)

    # # Normalize the axis vector (1,1,0)
    # axis = [1 / math.sqrt(2), 1 / math.sqrt(2), 0]

    # # Angle of rotation in radians
    # angle = math.radians(60)  # Convert 60 degrees to radians

    # # Create the rotation quaternion for 60 degrees around the normalized (1,1,0) axis
    # rotation_quaternion = Quaternion((axis[0] * math.sin(angle / 2), axis[1] * math.sin(angle / 2), axis[2] * math.sin(angle / 2), math.cos(angle / 2)))

    # # Apply the rotation quaternion to the object's rotation_quaternion property
    # obj.rotation_mode = 'QUATERNION'

    # # Insert keyframe at start (ensure the rotation is at its initial state)
    # obj.rotation_quaternion = (1, 0, 0, 0)  # No rotation
    # obj.keyframe_insert(data_path="rotation_quaternion", frame=mid_frame+1)

    # # Insert keyframe at end with the desired rotation
    # obj.rotation_quaternion = rotation_quaternion
    # obj.keyframe_insert(data_path="rotation_quaternion", frame=end_frame)
    # 

    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'  # 'FFMPEG' for video files
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'  # 'MPEG4' for MP4, 'OGG' for OGV; not directly applicable to GIF
    bpy.context.scene.render.ffmpeg.codec = 'H264'

    # transparent background
    # bpy.context.scene.render.ffmpeg.format = 'WEBM'  # 'webm' for WEBM
    # bpy.context.scene.render.ffmpeg.codec = 'WEBM'
    
    # bpy.context.scene.render.film_transparent = True
    
    bpy.context.scene.render.filepath = export_file_name

    # Render the scene and save the video
    bpy.ops.render.render(animation=True)

# Loop through all objects in the scene
for obj in bpy.context.scene.objects:
    # Check if the object is a mesh
    bpy.data.objects.remove(obj, do_unlink=True)
        
def merge_children():
    # Get all objects in the scene
    objects = bpy.data.objects

    # Print the names of all objects
    for obj in objects:
        object_name = obj.name
        if object_name.startswith("Group"):
            # Name of the parent object
            parent_name = object_name  # Replace with your parent object's name

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Get the parent object
            parent_obj = bpy.data.objects.get(parent_name)

            # Ensure the parent object exists and is a mesh
            if parent_obj and parent_obj.type == 'EMPTY':
                # Set the parent object as the active object
                bpy.context.view_layer.objects.active = parent_obj
                
                # Select the parent object
                parent_obj.select_set(True)
                
                # Select all child objects that are meshes
            for child_obj in parent_obj.children:
                if child_obj.type == 'MESH':
                    child_obj.select_set(True)
            else:
                print(f"Parent object named '{parent_name}' not found or is not a mesh.")

            if len(parent_obj.children) > 0:
                # Set the active object to the first child object
                bpy.context.view_layer.objects.active = parent_obj.children[0]

                objectName = parent_obj.children[0].name

                # Join the selected objects into the active object (the parent)
                bpy.ops.object.join()

                bpy.ops.object.select_all(action='DESELECT')
                
                # break parent-child relationship
                obj = bpy.data.objects.get(objectName)
                obj.select_set(True)
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

                bpy.ops.object.select_all(action='DESELECT')

                parent_obj.select_set(True)
                bpy.ops.object.delete()
    
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
            
setup_camera()
setup_light()
set_render_background_color((0.06, 0.06, 0.06, 1)) 

# Distance from the object (change as needed)
distance_from_object = 1.0

# This example positions the camera on the positive Z axis of the object
camera = bpy.data.objects['Camera']


# Assuming all objects are from a single FBX file

with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    first_row = next(reader)
    fbx_file_path = first_row['FBX File']
    if fbx_file_path:
        import_fbx(fbx_file_path)  # Import the FBX file
        baseObjectName = update_object_locations(csv_file_path)  # Update object locations
    
    baseObject = bpy.data.objects[baseObjectName]
    camera_location = baseObject.location + Vector((distance_from_object, distance_from_object, distance_from_object))

    # Update the camera's location
    camera.location = camera_location
        
    # Point the camera towards the target object
    # Create a 'TRACK TO' constraint if not already present
    track_to_constraint = camera.constraints.new(type='TRACK_TO')
    track_to_constraint.target = baseObject
    track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_to_constraint.up_axis = 'UP_Y'

merge_children()

with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
     # creating parent object
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    parent_obj = bpy.context.object

    for row in reader:
        obj_name = row['Object Name']
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.parent = parent_obj
        else:
            print(f"Object named '{obj_name}' not found.")

for i in range(10):
    show_random_parts(csv_file_path)
    assign_materials_to_objects(bpy.data.objects)

    # Set the file name based on the object name
    export_file_name = fbx_file_path + "_" + str(i) + ".mp4"

    video_export(parent_obj, export_file_name)

    # # Set the file name based on the object name
    # export_file_name = fbx_file_path + "_" + str(i) + ".jpg"
    # image_export(export_file_name)


# Delete all objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()
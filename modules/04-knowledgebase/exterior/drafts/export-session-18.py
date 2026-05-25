"""
Balencia City v3 — Module #04 Knowledgebase
Session 18: Export + Screenshots only
(Run after build-session-18.py saved the .blend file)
"""

import bpy
import math
import os

MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
DRAFTS_DIR = os.path.join(MODULE_DIR, "exterior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")
BLEND_FILE = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18.blend")
GLB_OUT = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18.glb")

# Reference dimensions
TOTAL_HEIGHT = 9.8
BEACON_HEIGHT = 1.5

# Load blend
print("=== Loading blend file ===")
bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

from mathutils import Vector


def get_tri_count(obj):
    if obj.type != 'MESH':
        return 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    tris = sum(len(p.vertices) - 2 for p in mesh.polygons)
    eval_obj.to_mesh_clear()
    return tris


mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
total_tris = sum(get_tri_count(obj) for obj in mesh_objects)
print(f"  Mesh objects: {len(mesh_objects)}")
print(f"  Total tris: {total_tris}")


# =====================================================
# GLB EXPORT
# =====================================================
print("\n=== GLB Export ===")

# Remove cameras and lights before export
cameras_lights = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in cameras_lights:
    bpy.data.objects.remove(obj, do_unlink=True)
print(f"  Removed {len(cameras_lights)} cameras/lights")

os.makedirs(os.path.dirname(GLB_OUT), exist_ok=True)

bpy.ops.export_scene.gltf(
    filepath=GLB_OUT,
    export_format='GLB',
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
    export_apply=True,
    export_yup=True,
    export_texcoords=True,
    export_normals=True,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False,
)

file_size_kb = os.path.getsize(GLB_OUT) / 1024
print(f"  Exported: {GLB_OUT}")
print(f"  File size: {file_size_kb:.0f} KB")
print(f"  Size budget check: {'PASS' if file_size_kb <= 400 else 'LARGE'}")
print(f"  Tris budget check: {'PASS' if total_tris <= 20000 else 'OVER BUDGET'}")


# =====================================================
# RENDER SCREENSHOTS
# =====================================================
print("\n=== Rendering Screenshots ===")

# Re-add camera for rendering
cam_data = bpy.data.cameras.new(name="Screenshot_Camera")
cam_data.lens = 50
cam_data.clip_start = 0.1
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Screenshot_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Re-add minimal lighting
key_data = bpy.data.lights.new(name="SS_Key", type='SUN')
key_data.color = (1.0, 0.894, 0.8)
key_data.energy = 0.8
key_obj = bpy.data.objects.new("SS_Key", key_data)
bpy.context.collection.objects.link(key_obj)
key_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

fill_data = bpy.data.lights.new(name="SS_Fill", type='AREA')
fill_data.color = (0.102, 0.102, 0.251)
fill_data.energy = 50
fill_data.size = 20
fill_obj = bpy.data.objects.new("SS_Fill", fill_data)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (5, 15, 10)

# Set world background (ink-blue)
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)

# Render settings
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

target = Vector((0, 0, TOTAL_HEIGHT / 2))
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def set_camera_and_render(cam_ob, position, name):
    cam_ob.location = position
    direction = target - Vector(position)
    cam_ob.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    filepath = os.path.join(SCREENSHOTS_DIR, f"session18-{name}.png")
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {filepath}")


# Screenshot 1: Front elevation
set_camera_and_render(cam_obj, (0, -18, 6), "front-elevation")

# Screenshot 2: 3/4 angle
set_camera_and_render(cam_obj, (12, -14, 8), "three-quarter")

# Screenshot 3: Distance view
set_camera_and_render(cam_obj, (20, -20, 12), "distance-view")

# Screenshot 4: Detail - columns and vault
set_camera_and_render(cam_obj, (3, -8, 2.5), "detail-columns")

# Screenshot 5: Detail - crown
set_camera_and_render(cam_obj, (4, -6, TOTAL_HEIGHT + 1), "detail-crown")


print("\n=== EXPORT + SCREENSHOTS COMPLETE ===")
print(f"  GLB: {GLB_OUT} ({file_size_kb:.0f} KB)")
print(f"  Screenshots: session18-*.png in {SCREENSHOTS_DIR}")

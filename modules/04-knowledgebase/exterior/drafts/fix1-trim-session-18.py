"""
Balencia City v3 -- Module #04 Knowledgebase
Session 18 Fix 1 TRIM: Remove excess tris to fit within 5,000-8,000 target.

Current: 8,684 tris (684 over ceiling).
Strategy: Remove the middle ring band from each of the 6 columns
(ring indices 1, 4, 7, 10, 13, 16 -- the 1/2 height ring on each column).
Each torus = 192 tris, removing 6 = -1,152 tris -> ~7,532 target.
"""

import bpy
import os

MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
DRAFTS_DIR = os.path.join(MODULE_DIR, "exterior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")
BLEND_FILE = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18-fix1.blend")
GLB_OUT = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18-fix1.glb")

import math

print("=== Loading blend file ===")
bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

from mathutils import Vector

TOTAL_HEIGHT = 9.8


def get_tri_count(obj):
    if obj.type != 'MESH':
        return 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    tris = sum(len(p.vertices) - 2 for p in mesh.polygons)
    eval_obj.to_mesh_clear()
    return tris


# Count before
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
before_tris = sum(get_tri_count(obj) for obj in mesh_objects)
print(f"  Before tris: {before_tris}")

# Remove middle ring from each column group (indices 1, 4, 7, 10, 13, 16)
# Rings are named column_ring_0 through column_ring_17
# Per column: indices 0,1,2 then 3,4,5 then 6,7,8 etc.
# Middle of each group is index 1, 4, 7, 10, 13, 16
removed_tris = 0
removed_count = 0
for ring_idx in [1, 4, 7, 10, 13, 16]:
    ring_name = f"column_ring_{ring_idx}"
    ring_obj = bpy.data.objects.get(ring_name)
    if ring_obj:
        removed_tris += get_tri_count(ring_obj)
        bpy.data.objects.remove(ring_obj, do_unlink=True)
        removed_count += 1
        print(f"  Removed {ring_name}")

print(f"  Removed {removed_count} rings, {removed_tris} tris")

# Final count
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
final_tris = sum(get_tri_count(obj) for obj in mesh_objects)
print(f"\n  Final tris: {final_tris}")
print(f"  Target: 5,000-8,000")
print(f"  Budget check: {'PASS' if 5000 <= final_tris <= 8000 else 'REVIEW'}")
print(f"  Total objects: {len(mesh_objects)}")

# Material distribution
mat_dist = {}
for obj in mesh_objects:
    if obj.data.materials:
        mat_name = obj.data.materials[0].name
        mat_dist[mat_name] = mat_dist.get(mat_name, 0) + 1
print(f"\n  Material distribution:")
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    print(f"    {mat_name}: {mat_dist.get(mat_name, 0)} objects")


# =====================================================
# GLB EXPORT
# =====================================================
print("\n=== GLB Export ===")

cameras_lights = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in cameras_lights:
    bpy.data.objects.remove(obj, do_unlink=True)

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


# =====================================================
# SCREENSHOTS
# =====================================================
print("\n=== Rendering Screenshots ===")

cam_data = bpy.data.cameras.new(name="Screenshot_Camera")
cam_data.lens = 50
cam_data.clip_start = 0.1
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Screenshot_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

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

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
if hasattr(world, 'use_nodes'):
    world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)

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
    filepath = os.path.join(SCREENSHOTS_DIR, f"session18-fix1-{name}.png")
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {filepath}")


set_camera_and_render(cam_obj, (0, -18, 6), "front-elevation")
set_camera_and_render(cam_obj, (12, -14, 8), "three-quarter")
set_camera_and_render(cam_obj, (20, -20, 12), "distance-view")


# =====================================================
# SAVE BLEND
# =====================================================
print("\n=== Saving blend file ===")

cameras_lights = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in cameras_lights:
    bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
print(f"  Saved: {BLEND_FILE}")


print("\n" + "=" * 60)
print("SESSION 18 FIX 1 TRIM COMPLETE")
print("=" * 60)
print(f"  Before: {before_tris}")
print(f"  Removed: {removed_tris}")
print(f"  Final: {final_tris}")
print(f"  Objects: {len(mesh_objects)}")
print(f"  GLB: {file_size_kb:.0f} KB")
print("=" * 60)

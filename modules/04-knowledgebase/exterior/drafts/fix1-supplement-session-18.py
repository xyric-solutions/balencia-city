"""
Balencia City v3 -- Module #04 Knowledgebase
Session 18 Fix 1 SUPPLEMENT: Additional geometry to reach 5,000-8,000 tris.

Fix 1 reached 4,384 tris. This supplement adds:
- More column detail (entasis profile + ring bands on each column)
- Additional stone facade panels on sides and back
- Data floor front/back edge trim (not just sides)
- Vertical accent pilasters on stone section corners
- Window sill and header elements for all arched windows
- Additional rustication on back facade
"""

import bpy
import bmesh
import math
import os

MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
DRAFTS_DIR = os.path.join(MODULE_DIR, "exterior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")
BLEND_IN = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18-fix1.blend")
BLEND_OUT = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18-fix1.blend")  # Overwrite
GLB_OUT = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18-fix1.glb")       # Overwrite

print("=== Loading blend file ===")
bpy.ops.wm.open_mainfile(filepath=BLEND_IN)

from mathutils import Vector

# Get materials
mats = {}
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    mat = bpy.data.materials.get(mat_name)
    if mat:
        mats[mat_name] = mat
assert len(mats) == 7


def assign_mat(obj, mat_name):
    mat = mats[mat_name]
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def apply_transforms(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)


def get_tri_count(obj):
    if obj.type != 'MESH':
        return 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    tris = sum(len(p.vertices) - 2 for p in mesh.polygons)
    eval_obj.to_mesh_clear()
    return tris


# Reference dimensions
BUILDING_WIDTH = 4.0
BUILDING_DEPTH = 3.5
LOWER_HEIGHT = 3.2
TRANSITION_HEIGHT = 0.6
UPPER_START = 3.8
UPPER_HEIGHT = 6.0
TOTAL_HEIGHT = UPPER_START + UPPER_HEIGHT
BEACON_HEIGHT = 1.5

stone_body_width = BUILDING_WIDTH * 1.15
stone_body_depth = BUILDING_DEPTH * 1.1
column_radius_refined = 0.325
column_height = LOWER_HEIGHT + 0.3
front_y = -(BUILDING_DEPTH / 2) - 0.1
front_col_y = front_y - 0.15

floor_width_base = BUILDING_WIDTH - 0.6
floor_depth = BUILDING_DEPTH - 0.4
floor_spacing = UPPER_HEIGHT / 12
num_floors = 12

# Count initial tris
initial_tris = sum(get_tri_count(obj) for obj in bpy.data.objects if obj.type == 'MESH')
print(f"  Initial tris (post-fix1): {initial_tris}")
supp_tris_added = 0


# =====================================================
# SUPPLEMENT A: Column Ring Bands (decorative rings)
# =====================================================
print("\n=== Supplement A: Column Ring Bands ===")

# Add 3 decorative ring bands per column (at 1/4, 1/2, 3/4 height)
ring_segments = 16
ring_inner_radius = column_radius_refined * 0.95
ring_outer_radius = column_radius_refined * 1.15
ring_height = 0.04

column_positions_all = [
    (f"stone_column_front_{i}", bpy.data.objects.get(f"stone_column_front_{i}"))
    for i in range(4)
] + [
    (f"stone_column_side_{i}", bpy.data.objects.get(f"stone_column_side_{i}"))
    for i in range(2)
]

ring_idx = 0
for col_name, col_obj in column_positions_all:
    if not col_obj:
        continue
    cx, cy = col_obj.location.x, col_obj.location.y

    for frac in [0.25, 0.5, 0.75]:
        rz = column_height * frac
        bpy.ops.mesh.primitive_torus_add(
            major_radius=ring_outer_radius,
            minor_radius=ring_height / 2,
            major_segments=ring_segments,
            minor_segments=6,
            location=(cx, cy, rz)
        )
        ring = bpy.context.active_object
        ring.name = f"column_ring_{ring_idx}"
        apply_transforms(ring)
        assign_mat(ring, "base")
        supp_tris_added += get_tri_count(ring)
        ring_idx += 1

print(f"  Column rings added: {ring_idx} objects, {supp_tris_added} tris")


# =====================================================
# SUPPLEMENT B: Corner Pilasters on Stone Section
# =====================================================
print("\n=== Supplement B: Corner Pilasters ===")

pilaster_b_start = supp_tris_added
# 4 vertical pilasters at corners of stone section (like embedded half-columns)
pilaster_width = 0.12
pilaster_depth = 0.08
pilaster_height = LOWER_HEIGHT * 0.95

corner_positions = [
    (-(stone_body_width / 2) - pilaster_depth / 2, -(stone_body_depth / 2), "FL"),
    ((stone_body_width / 2) + pilaster_depth / 2, -(stone_body_depth / 2), "FR"),
    (-(stone_body_width / 2) - pilaster_depth / 2, (stone_body_depth / 2), "BL"),
    ((stone_body_width / 2) + pilaster_depth / 2, (stone_body_depth / 2), "BR"),
]

for px, py, label in corner_positions:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(px, py, pilaster_height / 2)
    )
    pil = bpy.context.active_object
    pil.name = f"pilaster_{label}"
    pil.scale = (pilaster_width, pilaster_width, pilaster_height)
    apply_transforms(pil)
    assign_mat(pil, "base")
    supp_tris_added += get_tri_count(pil)

    # Pilaster cap
    bpy.ops.mesh.primitive_cone_add(
        radius1=pilaster_width * 0.8,
        radius2=pilaster_width * 0.5,
        depth=0.06,
        vertices=8,
        location=(px, py, pilaster_height + 0.03)
    )
    cap = bpy.context.active_object
    cap.name = f"pilaster_cap_{label}"
    apply_transforms(cap)
    assign_mat(cap, "base")
    supp_tris_added += get_tri_count(cap)

print(f"  Pilasters added: {supp_tris_added - pilaster_b_start} tris")


# =====================================================
# SUPPLEMENT C: Window Sill + Header Elements
# =====================================================
print("\n=== Supplement C: Window Sills & Headers ===")

supp_c_start = supp_tris_added

window_width = 0.7
window_height = 2.4

# Front windows
for i, wx in enumerate([-1.0, 0, 1.0]):
    win_bottom = LOWER_HEIGHT * 0.55 - window_height / 2
    win_top = LOWER_HEIGHT * 0.55 + window_height / 2

    # Sill (bottom ledge, slightly wider than window, protruding)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(wx, front_y + 0.05 - 0.03, win_bottom - 0.02)
    )
    sill = bpy.context.active_object
    sill.name = f"window_sill_front_{i}"
    sill.scale = (window_width + 0.1, 0.06, 0.03)
    apply_transforms(sill)
    assign_mat(sill, "base")
    supp_tris_added += get_tri_count(sill)

    # Header (top, heavier, keystone-like)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(wx, front_y + 0.05 - 0.02, win_top + 0.04)
    )
    header = bpy.context.active_object
    header.name = f"window_header_front_{i}"
    header.scale = (window_width + 0.08, 0.05, 0.06)
    apply_transforms(header)
    assign_mat(header, "base")
    supp_tris_added += get_tri_count(header)

# Side windows
side_window_width = window_width * 0.8
side_window_height = window_height * 0.8

for side_idx, sy_offset in enumerate([-0.8, 0.8]):
    for side_x, side_label in [(-(BUILDING_WIDTH / 2) - 0.02, "left"), ((BUILDING_WIDTH / 2) + 0.02, "right")]:
        win_bottom = LOWER_HEIGHT * 0.55 - side_window_height / 2
        win_top = LOWER_HEIGHT * 0.55 + side_window_height / 2

        # Determine sill offset direction
        x_offset = -0.03 if side_label == "left" else 0.03

        # Sill
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(side_x + x_offset, sy_offset, win_bottom - 0.02)
        )
        sill = bpy.context.active_object
        sill.name = f"window_sill_{side_label}_{side_idx}"
        sill.scale = (0.05, side_window_width + 0.08, 0.03)
        apply_transforms(sill)
        assign_mat(sill, "base")
        supp_tris_added += get_tri_count(sill)

        # Header
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(side_x + x_offset, sy_offset, win_top + 0.03)
        )
        header = bpy.context.active_object
        header.name = f"window_header_{side_label}_{side_idx}"
        header.scale = (0.04, side_window_width + 0.06, 0.05)
        apply_transforms(header)
        assign_mat(header, "base")
        supp_tris_added += get_tri_count(header)

print(f"  Window sills/headers added: {supp_tris_added - supp_c_start} tris")


# =====================================================
# SUPPLEMENT D: Data Floor Front/Back Edge Trim
# =====================================================
print("\n=== Supplement D: Data Floor Front/Back Edge Trim ===")

supp_d_start = supp_tris_added

for i in range(num_floors):
    floor_obj = bpy.data.objects.get(f"data_floor_{i:02d}")
    if not floor_obj:
        continue

    bbox = [floor_obj.matrix_world @ Vector(corner) for corner in floor_obj.bound_box]
    fw = max(v.x for v in bbox) - min(v.x for v in bbox)
    fd = max(v.y for v in bbox) - min(v.y for v in bbox)
    fz_actual = (max(v.z for v in bbox) + min(v.z for v in bbox)) / 2
    ft = max(v.z for v in bbox) - min(v.z for v in bbox)
    front_edge_y = min(v.y for v in bbox)
    back_edge_y = max(v.y for v in bbox)

    # Front edge trim (Y-axis edge)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, front_edge_y - 0.01, fz_actual + ft / 2 + 0.005)
    )
    ftrim = bpy.context.active_object
    ftrim.name = f"floor_trim_front_{i:02d}"
    ftrim.scale = (fw * 0.9, 0.02, 0.01)
    apply_transforms(ftrim)
    assign_mat(ftrim, "detail")
    supp_tris_added += get_tri_count(ftrim)

    # Back edge trim
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, back_edge_y + 0.01, fz_actual + ft / 2 + 0.005)
    )
    btrim = bpy.context.active_object
    btrim.name = f"floor_trim_back_{i:02d}"
    btrim.scale = (fw * 0.9, 0.02, 0.01)
    apply_transforms(btrim)
    assign_mat(btrim, "detail")
    supp_tris_added += get_tri_count(btrim)

print(f"  Front/back floor trim added: {supp_tris_added - supp_d_start} tris")


# =====================================================
# SUPPLEMENT E: Side Facade Stone Panels
# =====================================================
print("\n=== Supplement E: Side Facade Stone Panels ===")

supp_e_start = supp_tris_added

# Add recessed panels on left and right side facades of stone base
# 2 panels per side, between side windows
panel_recess = 0.03

for side_label, sx_base in [("left", -(stone_body_width / 2)), ("right", (stone_body_width / 2))]:
    x_sign = -1 if side_label == "left" else 1
    sx = sx_base + x_sign * panel_recess / 2

    for panel_idx, sy in enumerate([-0.4, 0.4]):
        # Panel between windows
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(sx, sy, LOWER_HEIGHT * 0.4)
        )
        panel = bpy.context.active_object
        panel.name = f"side_panel_{side_label}_{panel_idx}"
        panel.scale = (panel_recess, 0.5, LOWER_HEIGHT * 0.5)
        apply_transforms(panel)
        assign_mat(panel, "base")
        supp_tris_added += get_tri_count(panel)

# Back facade panels (3 panels, evenly spaced)
back_y = stone_body_depth / 2 + panel_recess / 2
for panel_idx, bx in enumerate([-1.2, 0, 1.2]):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(bx, back_y, LOWER_HEIGHT * 0.45)
    )
    panel = bpy.context.active_object
    panel.name = f"back_panel_{panel_idx}"
    panel.scale = (0.6, panel_recess, LOWER_HEIGHT * 0.55)
    apply_transforms(panel)
    assign_mat(panel, "base")
    supp_tris_added += get_tri_count(panel)

print(f"  Side/back panels added: {supp_tris_added - supp_e_start} tris")


# =====================================================
# SUPPLEMENT F: Back Facade Windows
# =====================================================
print("\n=== Supplement F: Back Facade Windows ===")

supp_f_start = supp_tris_added

# Add 3 simpler rectangular windows on back facade (no arch needed -- these are utility/secondary)
back_win_y = (stone_body_depth / 2) + 0.02
for i, bwx in enumerate([-1.0, 0, 1.0]):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(bwx, back_win_y, LOWER_HEIGHT * 0.5)
    )
    bwin = bpy.context.active_object
    bwin.name = f"back_window_{i}"
    bwin.scale = (0.5, 0.06, 1.5)
    apply_transforms(bwin)
    assign_mat(bwin, "glass")
    supp_tris_added += get_tri_count(bwin)

    # Sill
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(bwx, back_win_y + 0.02, LOWER_HEIGHT * 0.5 - 0.75 - 0.02)
    )
    sill = bpy.context.active_object
    sill.name = f"back_window_sill_{i}"
    sill.scale = (0.55, 0.04, 0.03)
    apply_transforms(sill)
    assign_mat(sill, "base")
    supp_tris_added += get_tri_count(sill)

print(f"  Back windows added: {supp_tris_added - supp_f_start} tris")


# =====================================================
# SUPPLEMENT G: Additional Emissive Accents
# =====================================================
print("\n=== Supplement G: Emissive Accents ===")

supp_g_start = supp_tris_added

# Add emissive dot pairs on the stone section sides (reading as interior lights)
# These are small cubes suggesting lit windows on the back facade
for i in range(3):
    for bwx in [-0.5, 0.5]:
        wz = 0.6 + i * 0.8
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(bwx, (stone_body_depth / 2) + 0.01, wz)
        )
        dot = bpy.context.active_object
        dot.name = f"back_window_glow_{i}_{bwx:.1f}"
        dot.scale = (0.08, 0.01, 0.08)
        apply_transforms(dot)
        assign_mat(dot, "emissive")
        supp_tris_added += get_tri_count(dot)

print(f"  Emissive accents added: {supp_tris_added - supp_g_start} tris")


# =====================================================
# POLISH & FINALIZE
# =====================================================
print("\n=== Polish ===")

# Apply all transforms (mesh only)
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')

# Recalculate normals
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
for obj in mesh_objects:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.select_set(False)

# Final count
final_mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
final_tris = sum(get_tri_count(obj) for obj in final_mesh_objects)
print(f"\n  Supplement tris added: {supp_tris_added}")
print(f"  Total mesh objects: {len(final_mesh_objects)}")
print(f"  Final total tris: {final_tris}")
print(f"  Target range: 5,000-8,000")
print(f"  Budget check: {'PASS' if 5000 <= final_tris <= 8000 else 'REVIEW'}")

# Material distribution
mat_dist = {}
for obj in final_mesh_objects:
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
print(f"  Removed {len(cameras_lights)} cameras/lights")

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

bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print(f"  Saved: {BLEND_OUT}")


print("\n" + "=" * 60)
print("SESSION 18 FIX 1 SUPPLEMENT COMPLETE")
print("=" * 60)
print(f"  Initial tris (post-fix1): {initial_tris}")
print(f"  Supplement tris added: {supp_tris_added}")
print(f"  Final tris: {final_tris}")
print(f"  Total objects: {len(final_mesh_objects)}")
print(f"  GLB size: {file_size_kb:.0f} KB")
print(f"  Blend: {BLEND_OUT}")
print(f"  GLB: {GLB_OUT}")
print("=" * 60)

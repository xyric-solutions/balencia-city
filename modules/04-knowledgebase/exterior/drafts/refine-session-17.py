"""
Balencia City v3 — Module #04 Knowledgebase
Session 17: Silhouette Refinement Pass

After reviewing screenshots, making these targeted adjustments:
1. Widen stone base to create more dramatic taper toward upper section
2. Make columns protrude more from the facade
3. Add width variation to floating floors (wider at bottom, narrower at top)
4. Make vault entrance more imposing
5. Enhance crown beacon
6. Add buttress-like forms at base corners for gravitas
"""

import bpy
import bmesh
import math
import os

MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
DRAFTS_DIR = os.path.join(MODULE_DIR, "exterior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")
BLEND_FILE = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-17.blend")

# Open the saved blend file
bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

from mathutils import Vector

# Reference dimensions from the build
BUILDING_WIDTH = 4.0
BUILDING_DEPTH = 3.5
LOWER_HEIGHT = 3.2
TRANSITION_HEIGHT = 0.6
UPPER_START = 3.8
UPPER_HEIGHT = 6.0
TOTAL_HEIGHT = UPPER_START + UPPER_HEIGHT
BEACON_HEIGHT = 1.5
floor_width_base = BUILDING_WIDTH - 0.6
floor_depth = BUILDING_DEPTH - 0.4

# Get materials dict
mats = {}
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    mat = bpy.data.materials.get(mat_name)
    if mat:
        mats[mat_name] = mat

def assign_mat(obj, mat_name):
    mat = mats[mat_name]
    obj.data.materials.clear()
    obj.data.materials.append(mat)

def apply_transforms(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)


# =====================================================
# REFINEMENT 1: Widen stone base for more taper
# =====================================================
print("=== Refinement 1: Widening stone base ===")

body = bpy.data.objects.get("stone_base_body")
if body:
    # Scale wider and deeper for more imposing base
    body.scale = (1.15, 1.1, 1.0)  # 15% wider, 10% deeper
    bpy.context.view_layer.objects.active = body
    body.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    body.select_set(False)

plinth = bpy.data.objects.get("stone_plinth")
if plinth:
    plinth.scale = (1.15, 1.1, 1.0)
    bpy.context.view_layer.objects.active = plinth
    plinth.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    plinth.select_set(False)


# =====================================================
# REFINEMENT 2: Make columns protrude more
# =====================================================
print("=== Refinement 2: Enhancing columns ===")

for i in range(4):
    col = bpy.data.objects.get(f"stone_column_front_{i}")
    if col:
        # Move columns further forward and make them thicker
        col.location.y -= 0.15
        col.scale = (1.3, 1.3, 1.0)
        bpy.context.view_layer.objects.active = col
        col.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        col.select_set(False)

for i in range(2):
    col = bpy.data.objects.get(f"stone_column_side_{i}")
    if col:
        offset = -0.15 if i == 0 else 0.15
        col.location.x += offset
        col.scale = (1.3, 1.3, 1.0)
        bpy.context.view_layer.objects.active = col
        col.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        col.select_set(False)


# =====================================================
# REFINEMENT 3: Add width variation to floating floors
# =====================================================
print("=== Refinement 3: Varying floating floor widths ===")

num_floors = 12
floor_spacing = UPPER_HEIGHT / num_floors

for i in range(num_floors):
    floor_obj = bpy.data.objects.get(f"data_floor_{i:02d}")
    if floor_obj:
        # Taper: bottom floors wider, top floors narrower
        # Factor goes from 1.1 at bottom to 0.85 at top
        taper_factor = 1.1 - (i / (num_floors - 1)) * 0.25
        floor_obj.scale.x = taper_factor
        floor_obj.scale.y = taper_factor * 0.95
        bpy.context.view_layer.objects.active = floor_obj
        floor_obj.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        floor_obj.select_set(False)


# =====================================================
# REFINEMENT 4: Corner buttresses for gravitas
# =====================================================
print("=== Refinement 4: Adding corner buttresses ===")

buttress_width = 0.35
buttress_depth = 0.35
buttress_height = LOWER_HEIGHT * 0.7
base_half_w = (BUILDING_WIDTH * 1.15) / 2  # Account for widened base
base_half_d = (BUILDING_DEPTH * 1.1) / 2

corner_positions = [
    (-base_half_w, -base_half_d, "FL"),
    (base_half_w, -base_half_d, "FR"),
    (-base_half_w, base_half_d, "BL"),
    (base_half_w, base_half_d, "BR"),
]

for cx, cy, label in corner_positions:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, buttress_height / 2))
    buttress = bpy.context.active_object
    buttress.name = f"corner_buttress_{label}"
    buttress.scale = (buttress_width, buttress_depth, buttress_height)
    apply_transforms(buttress)
    assign_mat(buttress, "base")


# =====================================================
# REFINEMENT 5: Enhance vault entrance
# =====================================================
print("=== Refinement 5: Enhancing vault entrance ===")

# Make vault frame pillars wider and taller
for side in ["left", "right"]:
    frame = bpy.data.objects.get(f"vault_frame_{side}")
    if frame:
        frame.scale = (1.4, 1.3, 1.1)
        bpy.context.view_layer.objects.active = frame
        frame.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        frame.select_set(False)

lintel = bpy.data.objects.get("vault_lintel")
if lintel:
    lintel.scale = (1.2, 1.3, 1.4)
    bpy.context.view_layer.objects.active = lintel
    lintel.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    lintel.select_set(False)

# Add vault accent trim
vault_y = -(BUILDING_DEPTH / 2) - 0.2
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, vault_y - 0.15, 0.9))
vault_accent = bpy.context.active_object
vault_accent.name = "vault_accent_trim"
vault_accent.scale = (2.2, 0.08, 0.06)
apply_transforms(vault_accent)
assign_mat(vault_accent, "accent")


# =====================================================
# REFINEMENT 6: Enhance crown beacon
# =====================================================
print("=== Refinement 6: Enhancing crown ===")

beacon = bpy.data.objects.get("crown_beacon")
if beacon:
    # Make beacon taller and thicker
    beacon.scale = (1.5, 1.5, 1.4)
    bpy.context.view_layer.objects.active = beacon
    beacon.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    beacon.select_set(False)

# Add a wider beacon base flare
bpy.ops.mesh.primitive_cone_add(
    radius1=0.5,
    radius2=0.15,
    depth=0.4,
    vertices=12,
    location=(0, 0, TOTAL_HEIGHT + 0.2)
)
beacon_flare = bpy.context.active_object
beacon_flare.name = "beacon_flare"
apply_transforms(beacon_flare)
assign_mat(beacon_flare, "emissive")

# Add a secondary beacon tip (pointed)
bpy.ops.mesh.primitive_cone_add(
    radius1=0.08,
    radius2=0.0,
    depth=0.6,
    vertices=8,
    location=(0, 0, TOTAL_HEIGHT + BEACON_HEIGHT * 1.4 + 0.3)
)
beacon_tip = bpy.context.active_object
beacon_tip.name = "beacon_tip"
apply_transforms(beacon_tip)
assign_mat(beacon_tip, "emissive")


# =====================================================
# REFINEMENT 7: Add horizontal accent bands on stone section
# =====================================================
print("=== Refinement 7: Accent bands on stone section ===")

band_positions = [0.8, 1.6, 2.4]  # Three horizontal bands
for bz in band_positions:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -(base_half_d) - 0.02, bz))
    band = bpy.context.active_object
    band.name = f"stone_accent_band_{bz:.1f}"
    band.scale = (BUILDING_WIDTH * 1.15 + 0.1, 0.03, 0.05)
    band.rotation_euler = (0, 0, 0)
    apply_transforms(band)
    assign_mat(band, "accent")


# =====================================================
# TRIANGLE COUNT REAUDIT
# =====================================================
print("\n=== Triangle count reaudit ===")

def get_tri_count(obj):
    if obj.type != 'MESH':
        return 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    tris = sum(len(p.vertices) - 2 for p in mesh.polygons)
    eval_obj.to_mesh_clear()
    return tris

total_tris = 0
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
for obj in sorted(mesh_objects, key=lambda o: o.name):
    tris = get_tri_count(obj)
    total_tris += tris
    mat_name = obj.data.materials[0].name if obj.data.materials else "NONE"
    # Only print new/changed objects
    if "buttress" in obj.name or "beacon" in obj.name or "accent_band" in obj.name or "vault_accent" in obj.name:
        print(f"  [NEW] {obj.name}: {tris} tris [{mat_name}]")

print(f"\n  TOTAL TRIANGLES: {total_tris}")
print(f"  Budget: 12,000 (60% of 20K)")
print(f"  Usage: {total_tris / 12000 * 100:.1f}%")

# Material usage summary
print("\n=== Material usage summary ===")
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    users = [obj.name for obj in mesh_objects if obj.data.materials and obj.data.materials[0].name == mat_name]
    print(f"  {mat_name}: {len(users)} objects")


# =====================================================
# SAVE AND RE-RENDER
# =====================================================
print("\n=== Saving and re-rendering ===")
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

# Set up render settings
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

cam = bpy.data.objects.get("Overview_Camera")
if cam:
    cam.data.lens = 50
    bpy.context.scene.camera = cam

target = Vector((0, 0, TOTAL_HEIGHT / 2))

def set_camera_and_render(cam_obj, position, name):
    cam_obj.location = position
    direction = target - Vector(position)
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    filepath = os.path.join(SCREENSHOTS_DIR, f"session17-{name}-v2.png")
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {filepath}")

# Screenshot 1: Front elevation
set_camera_and_render(cam, (0, -18, 6), "front-elevation")

# Screenshot 2: 3/4 angle
set_camera_and_render(cam, (12, -14, 8), "three-quarter")

# Screenshot 3: Distance view
set_camera_and_render(cam, (20, -20, 12), "distance-view")

# Re-save
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

print("\n=== REFINEMENT COMPLETE ===")
print(f"  Total objects: {len(mesh_objects)}")
print(f"  Total triangles: {total_tris}")

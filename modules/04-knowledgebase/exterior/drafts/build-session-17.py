"""
Balencia City v3 — Module #04 Knowledgebase
Session 17: Exterior Major Forms

Grand library cathedral: ancient stone base transitioning to floating tech top.
25 floors, ~10 units tall. Royal Purple #7F24FF district color.
"""

import bpy
import bmesh
import math
import os
import sys

# === PATHS ===
MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
DRAFTS_DIR = os.path.join(MODULE_DIR, "exterior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")
SHARED_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared"
BLEND_FILE = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-17.blend")


# =====================================================
# PHASE 1: CLEAR SCENE
# =====================================================
print("=== Phase 1: Clearing scene ===")
bpy.ops.wm.read_factory_settings(use_empty=True)


# =====================================================
# PHASE 2: LIGHTING RIG (inline from shared/lighting-rig.py)
# =====================================================
print("=== Phase 2: Setting up lighting rig ===")

# Execute the shared lighting rig
lighting_script = os.path.join(SHARED_DIR, "lighting-rig.py")
with open(lighting_script, 'r') as f:
    exec(f.read())

# Verify lights
light_count = sum(1 for obj in bpy.data.objects if obj.type == 'LIGHT')
cam_count = sum(1 for obj in bpy.data.objects if obj.type == 'CAMERA')
print(f"  Lights: {light_count}, Cameras: {cam_count}")
assert light_count == 3, f"Expected 3 lights, got {light_count}"

# Verify world background
world = bpy.context.scene.world
bg = world.node_tree.nodes.get("Background")
bg_color = tuple(bg.inputs["Color"].default_value[:3])
print(f"  World background: {bg_color}")


# =====================================================
# PHASE 3: MATERIAL LIBRARY (inline from shared/material-library.py)
# =====================================================
print("=== Phase 3: Creating material library ===")

mat_script = os.path.join(SHARED_DIR, "material-library.py")
with open(mat_script, 'r') as f:
    mat_code = f.read()
exec(mat_code)

# Create materials with Royal Purple and energy+holo enabled
mats = create_materials("#7F24FF", include_energy=True, include_holo=True)
print(f"  Materials created: {list(mats.keys())}")
assert len(mats) == 7, f"Expected 7 materials, got {len(mats)}"


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def assign_mat(obj, mat_name):
    """Assign a material from the mats dict to an object."""
    mat = mats[mat_name]
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def apply_transforms(obj):
    """Apply all transforms to an object."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)


def get_tri_count(obj):
    """Get triangle count for a mesh object."""
    if obj.type != 'MESH':
        return 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    tris = sum(len(p.vertices) - 2 for p in mesh.polygons)
    eval_obj.to_mesh_clear()
    return tris


# =====================================================
# PHASE 4: BUILD MAJOR FORMS
# =====================================================
print("=== Phase 4: Building major forms ===")

# Building dimensions
# 25 floors, ~10u tall total
# Lower stone section: floors 1-8 = 3.2u
# Transition zone: 0.6u
# Upper floating section: floors 10-25 = 6.0u
# Crown beacon: 1.5u above roofline

BUILDING_WIDTH = 4.0    # X dimension
BUILDING_DEPTH = 3.5    # Y dimension
LOWER_HEIGHT = 3.2      # Stone base
TRANSITION_HEIGHT = 0.6
UPPER_START = 3.8       # Where floating floors begin
UPPER_HEIGHT = 6.0      # Total upper section
TOTAL_HEIGHT = UPPER_START + UPPER_HEIGHT  # ~9.8u
BEACON_HEIGHT = 1.5

# --- 4.1: STONE BASE (lower 8 floors) ---
print("  Building stone base...")

# Main stone body
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, LOWER_HEIGHT / 2))
stone_body = bpy.context.active_object
stone_body.name = "stone_base_body"
stone_body.scale = (BUILDING_WIDTH, BUILDING_DEPTH, LOWER_HEIGHT)
apply_transforms(stone_body)
assign_mat(stone_body, "base")

# Stone base has a slight batter (wider at bottom) for imposing feel
# Add a tapered base plinth
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.15))
plinth = bpy.context.active_object
plinth.name = "stone_plinth"
plinth.scale = (BUILDING_WIDTH + 0.5, BUILDING_DEPTH + 0.5, 0.3)
apply_transforms(plinth)
assign_mat(plinth, "base")

# --- 4.2: STONE COLUMNS (4 front, 2 side) ---
print("  Building stone columns...")

column_radius = 0.25
column_height = LOWER_HEIGHT + 0.3  # Slightly taller than walls
column_segments = 12  # Enough for silhouette, not excessive tris

# Front facade columns - 4 evenly spaced
front_y = -(BUILDING_DEPTH / 2) - 0.1  # Slightly in front of facade
column_positions_front = [
    (-1.5, front_y),
    (-0.5, front_y),
    (0.5, front_y),
    (1.5, front_y),
]

for i, (cx, cy) in enumerate(column_positions_front):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=column_radius,
        depth=column_height,
        vertices=column_segments,
        location=(cx, cy, column_height / 2)
    )
    col = bpy.context.active_object
    col.name = f"stone_column_front_{i}"
    apply_transforms(col)
    assign_mat(col, "base")

# Side columns - 1 per side at midpoint
for i, sx in enumerate([-(BUILDING_WIDTH / 2) - 0.1, (BUILDING_WIDTH / 2) + 0.1]):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=column_radius,
        depth=column_height,
        vertices=column_segments,
        location=(sx, 0, column_height / 2)
    )
    col = bpy.context.active_object
    col.name = f"stone_column_side_{i}"
    apply_transforms(col)
    assign_mat(col, "base")

# --- 4.3: ARCHED WINDOWS (stone section) ---
print("  Building arched windows...")

# Windows as inset rectangles on the front facade
# 8 floors, 2 window openings per floor = 16 windows total, but for major forms
# we represent them as grouped window bands (3 vertical bands on front)
window_width = 0.7
window_height = 2.4
window_depth = 0.08

# Three tall window bays on front facade
for i, wx in enumerate([-1.0, 0, 1.0]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, front_y + 0.05, LOWER_HEIGHT * 0.55))
    win = bpy.context.active_object
    win.name = f"arched_window_front_{i}"
    win.scale = (window_width, window_depth, window_height)
    apply_transforms(win)
    assign_mat(win, "glass")

# Side windows - 2 per side
for side_idx, sy_offset in enumerate([-0.8, 0.8]):
    for side_x, side_label in [(-(BUILDING_WIDTH / 2) - 0.02, "left"), ((BUILDING_WIDTH / 2) + 0.02, "right")]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(side_x, sy_offset, LOWER_HEIGHT * 0.55))
        win = bpy.context.active_object
        win.name = f"arched_window_{side_label}_{side_idx}"
        win.scale = (window_depth, window_width * 0.8, window_height * 0.8)
        apply_transforms(win)
        assign_mat(win, "glass")

# --- 4.4: TRANSITION ZONE ---
print("  Building transition zone...")

# The transition zone is where stone tapers into metal
# Slightly narrower, inset, different material (detail)
tz_bottom = LOWER_HEIGHT
tz_width = BUILDING_WIDTH - 0.3
tz_depth = BUILDING_DEPTH - 0.2

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, tz_bottom + TRANSITION_HEIGHT / 2))
transition = bpy.context.active_object
transition.name = "transition_zone"
transition.scale = (tz_width, tz_depth, TRANSITION_HEIGHT)
apply_transforms(transition)
assign_mat(transition, "detail")

# Transition accent bands (horizontal lines marking the shift)
for band_z in [tz_bottom + 0.1, tz_bottom + TRANSITION_HEIGHT - 0.1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, band_z))
    band = bpy.context.active_object
    band.name = f"transition_band_{band_z:.1f}"
    band.scale = (tz_width + 0.15, tz_depth + 0.15, 0.04)
    apply_transforms(band)
    assign_mat(band, "accent")

# --- 4.5: FLOATING DATA FLOORS (upper section) ---
print("  Building floating data floors...")

# 12 floating glass platforms with visible gaps
num_floors = 12
floor_thickness = 0.12
floor_spacing = UPPER_HEIGHT / num_floors  # ~0.5u per floor
floor_width = BUILDING_WIDTH - 0.6  # Slightly narrower than base
floor_depth = BUILDING_DEPTH - 0.4

for i in range(num_floors):
    fz = UPPER_START + (i * floor_spacing) + floor_spacing / 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, fz))
    floor_obj = bpy.context.active_object
    floor_obj.name = f"data_floor_{i:02d}"
    floor_obj.scale = (floor_width, floor_depth, floor_thickness)
    apply_transforms(floor_obj)
    assign_mat(floor_obj, "glass")

# Thin vertical support columns for floating floors (4 corners)
support_radius = 0.06
support_height = UPPER_HEIGHT
support_positions = [
    (-(floor_width / 2) + 0.15, -(floor_depth / 2) + 0.15),
    ((floor_width / 2) - 0.15, -(floor_depth / 2) + 0.15),
    (-(floor_width / 2) + 0.15, (floor_depth / 2) - 0.15),
    ((floor_width / 2) - 0.15, (floor_depth / 2) - 0.15),
]

for i, (sx, sy) in enumerate(support_positions):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=support_radius,
        depth=support_height,
        vertices=8,
        location=(sx, sy, UPPER_START + support_height / 2)
    )
    support = bpy.context.active_object
    support.name = f"floor_support_{i}"
    apply_transforms(support)
    assign_mat(support, "detail")

# --- 4.6: EMISSIVE GLOW ELEMENTS (purple inner glow) ---
print("  Building emissive glow elements...")

# Emissive panels between floating floors - visible from outside
# These create the "stacked light" appearance
emissive_width = floor_width - 0.3
emissive_depth = floor_depth - 0.2

for i in range(num_floors - 1):
    ez = UPPER_START + (i * floor_spacing) + floor_spacing
    # Front-facing emissive panel
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -(floor_depth / 2) + 0.02, ez))
    em = bpy.context.active_object
    em.name = f"emissive_panel_front_{i:02d}"
    em.scale = (emissive_width, 1, floor_spacing * 0.6)
    em.rotation_euler = (math.radians(90), 0, 0)
    apply_transforms(em)
    assign_mat(em, "emissive")

# Back-facing emissive panels (every other floor for variety)
for i in range(0, num_floors - 1, 2):
    ez = UPPER_START + (i * floor_spacing) + floor_spacing
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, (floor_depth / 2) - 0.02, ez))
    em = bpy.context.active_object
    em.name = f"emissive_panel_back_{i:02d}"
    em.scale = (emissive_width, 1, floor_spacing * 0.6)
    em.rotation_euler = (math.radians(90), 0, 0)
    apply_transforms(em)
    assign_mat(em, "emissive")

# --- 4.7: CASCADING ENERGY WATERFALL ---
print("  Building energy waterfall...")

# A vertical plane on the front facade running from crown to base
waterfall_width = 0.4
waterfall_height = TOTAL_HEIGHT + BEACON_HEIGHT * 0.5
waterfall_z = waterfall_height / 2

bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -(BUILDING_DEPTH / 2) - 0.15, waterfall_z))
waterfall = bpy.context.active_object
waterfall.name = "energy_waterfall"
waterfall.scale = (waterfall_width, 1, waterfall_height)
waterfall.rotation_euler = (math.radians(90), 0, 0)
apply_transforms(waterfall)
assign_mat(waterfall, "energy")

# Waterfall side streaks (thinner, flanking the main stream)
for wx, suffix in [(-0.3, "left"), (0.3, "right")]:
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(wx, -(BUILDING_DEPTH / 2) - 0.13, waterfall_z * 0.7)
    )
    streak = bpy.context.active_object
    streak.name = f"energy_streak_{suffix}"
    streak.scale = (0.08, 1, waterfall_height * 0.6)
    streak.rotation_euler = (math.radians(90), 0, 0)
    apply_transforms(streak)
    assign_mat(streak, "energy")

# --- 4.8: ENERGY RESERVOIR POOL ---
print("  Building energy reservoir pool...")

# A glowing basin at ground level beneath the waterfall
pool_width = 1.2
pool_depth = 0.8
pool_height = 0.1

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -(BUILDING_DEPTH / 2) - 0.5, pool_height / 2))
pool = bpy.context.active_object
pool.name = "energy_reservoir_pool"
pool.scale = (pool_width, pool_depth, pool_height)
apply_transforms(pool)
assign_mat(pool, "energy")

# Pool rim (slightly larger, accent material)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -(BUILDING_DEPTH / 2) - 0.5, 0.02))
pool_rim = bpy.context.active_object
pool_rim.name = "energy_reservoir_rim"
pool_rim.scale = (pool_width + 0.2, pool_depth + 0.2, 0.04)
apply_transforms(pool_rim)
assign_mat(pool_rim, "accent")

# --- 4.9: CROWN KNOWLEDGE BEACON ---
print("  Building crown knowledge beacon...")

# Vertical cylinder of purple light above roofline
beacon_radius = 0.15
bpy.ops.mesh.primitive_cylinder_add(
    radius=beacon_radius,
    depth=BEACON_HEIGHT,
    vertices=12,
    location=(0, 0, TOTAL_HEIGHT + BEACON_HEIGHT / 2)
)
beacon = bpy.context.active_object
beacon.name = "crown_beacon"
apply_transforms(beacon)
assign_mat(beacon, "emissive")

# Beacon base platform (top of building)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, TOTAL_HEIGHT + 0.05))
beacon_base = bpy.context.active_object
beacon_base.name = "crown_platform"
beacon_base.scale = (floor_width + 0.2, floor_depth + 0.2, 0.1)
apply_transforms(beacon_base)
assign_mat(beacon_base, "accent")

# Beacon glow ring
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.35,
    minor_radius=0.04,
    major_segments=16,
    minor_segments=6,
    location=(0, 0, TOTAL_HEIGHT + BEACON_HEIGHT + 0.1)
)
beacon_ring = bpy.context.active_object
beacon_ring.name = "beacon_glow_ring"
apply_transforms(beacon_ring)
assign_mat(beacon_ring, "emissive")

# --- 4.10: ARCHIVE VAULT ENTRANCE ---
print("  Building archive vault entrance...")

# Heavy oversized door frame at ground level, front-center
door_width = 1.4
door_height = 1.8
door_depth = 0.4
frame_thickness = 0.2

# Door frame - left pillar
bpy.ops.mesh.primitive_cube_add(size=1, location=(
    -(door_width / 2) - frame_thickness / 2,
    -(BUILDING_DEPTH / 2) - 0.2,
    door_height / 2
))
frame_left = bpy.context.active_object
frame_left.name = "vault_frame_left"
frame_left.scale = (frame_thickness, door_depth, door_height)
apply_transforms(frame_left)
assign_mat(frame_left, "base")

# Door frame - right pillar
bpy.ops.mesh.primitive_cube_add(size=1, location=(
    (door_width / 2) + frame_thickness / 2,
    -(BUILDING_DEPTH / 2) - 0.2,
    door_height / 2
))
frame_right = bpy.context.active_object
frame_right.name = "vault_frame_right"
frame_right.scale = (frame_thickness, door_depth, door_height)
apply_transforms(frame_right)
assign_mat(frame_right, "base")

# Door frame - lintel (top beam)
bpy.ops.mesh.primitive_cube_add(size=1, location=(
    0,
    -(BUILDING_DEPTH / 2) - 0.2,
    door_height + frame_thickness / 2
))
lintel = bpy.context.active_object
lintel.name = "vault_lintel"
lintel.scale = (door_width + frame_thickness * 2, door_depth, frame_thickness * 1.5)
apply_transforms(lintel)
assign_mat(lintel, "base")

# Vault door surface (recessed, dark)
bpy.ops.mesh.primitive_cube_add(size=1, location=(
    0,
    -(BUILDING_DEPTH / 2) - 0.1,
    door_height / 2
))
vault_door = bpy.context.active_object
vault_door.name = "vault_door"
vault_door.scale = (door_width, 0.05, door_height)
apply_transforms(vault_door)
assign_mat(vault_door, "detail")

# --- 4.11: HOLO DATA PANELS ---
print("  Building holo data panels...")

# Flat translucent rectangles on upper floor edges
panel_width = 0.6
panel_height = 0.35

# Front-facing panels on every 3rd data floor
for i in range(0, num_floors, 3):
    fz = UPPER_START + (i * floor_spacing) + floor_spacing * 0.7
    for px in [-1.2, 1.2]:
        bpy.ops.mesh.primitive_plane_add(size=1, location=(
            px, -(floor_depth / 2) - 0.08, fz
        ))
        panel = bpy.context.active_object
        panel.name = f"holo_panel_{i:02d}_{'L' if px < 0 else 'R'}"
        panel.scale = (panel_width, 1, panel_height)
        panel.rotation_euler = (math.radians(90), 0, 0)
        apply_transforms(panel)
        assign_mat(panel, "holo")

# Side-facing holo panels
for i in range(1, num_floors, 4):
    fz = UPPER_START + (i * floor_spacing) + floor_spacing * 0.7
    for sx, rot in [((floor_width / 2) + 0.08, math.radians(90)), (-(floor_width / 2) - 0.08, math.radians(90))]:
        bpy.ops.mesh.primitive_plane_add(size=1, location=(
            sx, 0, fz
        ))
        panel = bpy.context.active_object
        panel.name = f"holo_panel_side_{i:02d}_{'R' if sx > 0 else 'L'}"
        panel.scale = (panel_height, 1, panel_width)
        panel.rotation_euler = (math.radians(90), 0, rot)
        apply_transforms(panel)
        assign_mat(panel, "holo")


# =====================================================
# PHASE 5: TRIANGLE COUNT AUDIT
# =====================================================
print("\n=== Phase 5: Triangle count audit ===")

total_tris = 0
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
for obj in sorted(mesh_objects, key=lambda o: o.name):
    tris = get_tri_count(obj)
    total_tris += tris
    mat_name = obj.data.materials[0].name if obj.data.materials else "NONE"
    print(f"  {obj.name}: {tris} tris [{mat_name}]")

print(f"\n  TOTAL TRIANGLES: {total_tris}")
print(f"  Budget: 12,000 (60% of 20K)")
print(f"  Usage: {total_tris / 12000 * 100:.1f}%")

if total_tris > 12000:
    print("  WARNING: Over budget! Need to reduce geometry.")
else:
    print("  OK: Within budget.")

# Material usage summary
print("\n=== Material usage summary ===")
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    users = [obj.name for obj in mesh_objects if obj.data.materials and obj.data.materials[0].name == mat_name]
    print(f"  {mat_name}: {len(users)} objects")


# =====================================================
# PHASE 6: SAVE BLEND FILE
# =====================================================
print(f"\n=== Phase 6: Saving blend file ===")
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
print(f"  Saved to: {BLEND_FILE}")


# =====================================================
# PHASE 7: RENDER SCREENSHOTS
# =====================================================
print("\n=== Phase 7: Rendering screenshots ===")

# Set up render settings for screenshots
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# Get or create camera
cam = bpy.data.objects.get("Overview_Camera")
if not cam:
    cam_data = bpy.data.cameras.new(name="Screenshot_Camera")
    cam = bpy.data.objects.new("Screenshot_Camera", cam_data)
    bpy.context.collection.objects.link(cam)

cam.data.lens = 50
cam.data.clip_start = 0.1
cam.data.clip_end = 200
bpy.context.scene.camera = cam

from mathutils import Vector

# Building center for aiming
target = Vector((0, 0, TOTAL_HEIGHT / 2))

def set_camera_and_render(cam_obj, position, name):
    """Position camera, aim at building center, render."""
    cam_obj.location = position
    direction = target - Vector(position)
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    filepath = os.path.join(SCREENSHOTS_DIR, f"session17-{name}.png")
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {filepath}")

# Screenshot 1: Front elevation
set_camera_and_render(cam, (0, -18, 6), "front-elevation")

# Screenshot 2: 3/4 angle (reveals depth and gradient)
set_camera_and_render(cam, (12, -14, 8), "three-quarter")

# Screenshot 3: Distance view (tests recognition at thumbnail)
set_camera_and_render(cam, (20, -20, 12), "distance-view")

# Re-save with camera positions
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

print("\n=== BUILD COMPLETE ===")
print(f"  Total objects: {len(mesh_objects)}")
print(f"  Total triangles: {total_tris}")
print(f"  Blend file: {BLEND_FILE}")
print(f"  Screenshots: {SCREENSHOTS_DIR}/session17-*.png")

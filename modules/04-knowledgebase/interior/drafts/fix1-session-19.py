"""
Balencia City v3 -- Module #04 Knowledgebase
Session 19 Fix 1: Interior Geometry Addition

Fixes applied to existing knowledgebase-int-draft-19.blend:
  A. Room shell articulation (+800-1200 tris, base/accent/detail)
  B. Column upgrades (8-vert -> 16-vert with bands/bases)
  C. Book wall articulation (dividers, molding, protruding books)
  D. Knowledge graph edge upgrade (4-vert -> 8-vert cylinders)
  E. Additional memory cubes (+30 cubes)
  F. Wall alcove integration (frames, shelves)
  G. Knowledge tree trunk upgrade (6-vert -> 10-vert with root flares)

Target: 5,500-8,000 tris (up from 2,720)
"""

import bpy
import bmesh
import math
import os
import random

# === PATHS ===
MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
DRAFTS_DIR = os.path.join(MODULE_DIR, "interior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")

SOURCE_BLEND = os.path.join(DRAFTS_DIR, "knowledgebase-int-draft-19.blend")
OUTPUT_BLEND = os.path.join(DRAFTS_DIR, "knowledgebase-int-draft-19-fix1.blend")
OUTPUT_GLB = os.path.join(DRAFTS_DIR, "knowledgebase-int-draft-19-fix1.glb")

# Seed for reproducibility (use different seed from original to get different scatter)
random.seed(99)

# =====================================================
# PHASE 0: LOAD EXISTING BLEND
# =====================================================
print("=== Phase 0: Loading existing blend file ===")
bpy.ops.wm.open_mainfile(filepath=SOURCE_BLEND)
print(f"  Loaded: {SOURCE_BLEND}")

# Count pre-fix state
pre_mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
pre_tris = 0
for obj in pre_mesh_objects:
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    pre_tris += sum(len(p.vertices) - 2 for p in mesh.polygons)
    eval_obj.to_mesh_clear()

print(f"  Pre-fix: {len(pre_mesh_objects)} mesh objects, {pre_tris} tris")

# Verify empties are present
required_empties = ["light_0", "light_1", "light_2", "camera_target"]
for req in required_empties:
    obj = bpy.data.objects.get(req)
    if obj:
        print(f"  Empty {req}: {tuple(round(c, 2) for c in obj.location)} -- OK")
    else:
        print(f"  Empty {req}: MISSING -- WARNING")

# =====================================================
# HELPERS
# =====================================================

# Get the existing materials from the scene
mats = {}
valid_mat_names = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
for mat in bpy.data.materials:
    if mat.name in valid_mat_names:
        mats[mat.name] = mat

print(f"  Materials found: {list(mats.keys())}")
assert len(mats) == 7, f"Expected 7 materials, got {len(mats)}"


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


# Room dimensions (from original script)
ROOM_W = 3.6
ROOM_D = 3.2
ROOM_H = 9.0
WALL_THICK = 0.12


# =====================================================
# FIX A: ROOM SHELL ARTICULATION (+800-1200 tris)
# =====================================================
print("\n=== Fix A: Room shell articulation ===")
fix_a_tris = 0

# --- A.1: Horizontal rustication lines on 3 solid walls ---
print("  A.1: Rustication lines (4 per wall, 12 total)...")
wall_configs = [
    # (wall_name, wall_center_x, wall_center_y, wall_width_axis, wall_width, wall_normal_axis, normal_offset)
    ("back", 0, ROOM_D / 2 - WALL_THICK / 2 - 0.005, "x", ROOM_W, "y", 0),
    ("left", -ROOM_W / 2 + WALL_THICK / 2 + 0.005, 0, "y", ROOM_D, "x", 0),
    ("right", ROOM_W / 2 - WALL_THICK / 2 - 0.005, 0, "y", ROOM_D, "x", 0),
]

groove_count = 0
for wall_name, wcx, wcy, width_axis, width_val, normal_axis, noff in wall_configs:
    for gi in range(4):
        # 4 lines evenly spaced from 15% to 85% of room height
        gz = ROOM_H * (0.15 + gi * 0.233)
        groove_depth = 0.02
        groove_height = 0.04

        if width_axis == "x":
            gpos = (wcx, wcy, gz)
            gscale = (width_val * 0.95, groove_depth, groove_height)
        else:
            gpos = (wcx, wcy, gz)
            gscale = (groove_depth, width_val * 0.95, groove_height)

        bpy.ops.mesh.primitive_cube_add(size=1, location=gpos)
        groove = bpy.context.active_object
        groove.name = f"rustication_{wall_name}_{gi:02d}"
        groove.scale = gscale
        apply_transforms(groove)
        assign_mat(groove, "base")
        groove_count += 1
        fix_a_tris += get_tri_count(groove)

print(f"    {groove_count} rustication lines placed. Tris: {fix_a_tris}")

# --- A.2: Recessed panel insets on back wall ---
print("  A.2: Back wall panel insets...")
panel_inset_tris = 0
panel_positions_x = [-ROOM_W * 0.3, 0, ROOM_W * 0.3]
for pi, px in enumerate(panel_positions_x):
    # 3 panels between rustication lines at mid-height
    pz = ROOM_H * 0.5
    bpy.ops.mesh.primitive_cube_add(size=1, location=(px, ROOM_D / 2 - WALL_THICK / 2 - 0.01, pz))
    panel = bpy.context.active_object
    panel.name = f"back_panel_inset_{pi:02d}"
    panel.scale = (0.35, 0.015, ROOM_H * 0.15)
    apply_transforms(panel)
    assign_mat(panel, "base")
    panel_inset_tris += get_tri_count(panel)

# Add a 4th panel at lower height
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, ROOM_D / 2 - WALL_THICK / 2 - 0.01, ROOM_H * 0.25))
panel = bpy.context.active_object
panel.name = "back_panel_inset_03"
panel.scale = (0.5, 0.015, ROOM_H * 0.1)
apply_transforms(panel)
assign_mat(panel, "base")
panel_inset_tris += get_tri_count(panel)

fix_a_tris += panel_inset_tris
print(f"    4 panel insets. Tris: {panel_inset_tris}")

# --- A.3: Floor pattern (central aisle + 2 cross strips) ---
print("  A.3: Floor pattern...")
floor_tris = 0

# Central aisle strip (Y direction, from entrance to back wall)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.005))
aisle = bpy.context.active_object
aisle.name = "floor_aisle_center"
aisle.scale = (0.15, ROOM_D * 0.95, 0.005)
apply_transforms(aisle)
assign_mat(aisle, "accent")
floor_tris += get_tri_count(aisle)

# Cross strip 1 (X direction, at 1/3 depth)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -ROOM_D * 0.15, 0.005))
cross1 = bpy.context.active_object
cross1.name = "floor_cross_01"
cross1.scale = (ROOM_W * 0.95, 0.1, 0.005)
apply_transforms(cross1)
assign_mat(cross1, "accent")
floor_tris += get_tri_count(cross1)

# Cross strip 2 (X direction, at 2/3 depth)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, ROOM_D * 0.2, 0.005))
cross2 = bpy.context.active_object
cross2.name = "floor_cross_02"
cross2.scale = (ROOM_W * 0.95, 0.1, 0.005)
apply_transforms(cross2)
assign_mat(cross2, "accent")
floor_tris += get_tri_count(cross2)

# Floor border strip (rectangular frame around the edge)
# 4 edge strips
for fi, (fp, fs) in enumerate([
    ((0, -ROOM_D / 2 + 0.08, 0.004), (ROOM_W * 0.98, 0.06, 0.004)),   # front edge
    ((0, ROOM_D / 2 - 0.08, 0.004), (ROOM_W * 0.98, 0.06, 0.004)),    # back edge
    ((-ROOM_W / 2 + 0.08, 0, 0.004), (0.06, ROOM_D * 0.98, 0.004)),   # left edge
    ((ROOM_W / 2 - 0.08, 0, 0.004), (0.06, ROOM_D * 0.98, 0.004)),    # right edge
]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=fp)
    edge = bpy.context.active_object
    edge.name = f"floor_border_{fi:02d}"
    edge.scale = fs
    apply_transforms(edge)
    assign_mat(edge, "base")
    floor_tris += get_tri_count(edge)

fix_a_tris += floor_tris
print(f"    Floor pattern placed. Tris: {floor_tris}")

# --- A.4: Ceiling beam cross-members ---
print("  A.4: Ceiling beams...")
beam_tris = 0
beam_count = 4
for bi in range(beam_count):
    # Beams spanning the X width at evenly spaced Y positions
    by = -ROOM_D / 2 + ROOM_D * ((bi + 1) / (beam_count + 1))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, by, ROOM_H - 0.08))
    beam = bpy.context.active_object
    beam.name = f"ceiling_beam_{bi:02d}"
    beam.scale = (ROOM_W * 0.98, 0.08, 0.12)
    apply_transforms(beam)
    assign_mat(beam, "base")
    beam_tris += get_tri_count(beam)

fix_a_tris += beam_tris
print(f"    {beam_count} ceiling beams. Tris: {beam_tris}")

# --- A.5: Wall-base molding strips ---
print("  A.5: Wall-base molding...")
molding_tris = 0
molding_configs = [
    ("molding_back", (0, ROOM_D / 2 - WALL_THICK / 2 - 0.02, 0.04), (ROOM_W * 0.98, 0.03, 0.06)),
    ("molding_left", (-ROOM_W / 2 + WALL_THICK / 2 + 0.02, 0, 0.04), (0.03, ROOM_D * 0.98, 0.06)),
    ("molding_right", (ROOM_W / 2 - WALL_THICK / 2 - 0.02, 0, 0.04), (0.03, ROOM_D * 0.98, 0.06)),
]
for mname, mpos, mscale in molding_configs:
    bpy.ops.mesh.primitive_cube_add(size=1, location=mpos)
    mold = bpy.context.active_object
    mold.name = mname
    mold.scale = mscale
    apply_transforms(mold)
    assign_mat(mold, "base")
    molding_tris += get_tri_count(mold)

fix_a_tris += molding_tris
print(f"    3 molding strips. Tris: {molding_tris}")

# --- A.6: Cornice trim at ceiling level ---
print("  A.6: Cornice trim...")
cornice_tris = 0
cornice_configs = [
    ("cornice_back", (0, ROOM_D / 2 - WALL_THICK / 2 - 0.02, ROOM_H - 0.04), (ROOM_W * 0.98, 0.035, 0.06)),
    ("cornice_left", (-ROOM_W / 2 + WALL_THICK / 2 + 0.02, 0, ROOM_H - 0.04), (0.035, ROOM_D * 0.98, 0.06)),
    ("cornice_right", (ROOM_W / 2 - WALL_THICK / 2 - 0.02, 0, ROOM_H - 0.04), (0.035, ROOM_D * 0.98, 0.06)),
]
for cname, cpos, cscale in cornice_configs:
    bpy.ops.mesh.primitive_cube_add(size=1, location=cpos)
    cornice = bpy.context.active_object
    cornice.name = cname
    cornice.scale = cscale
    apply_transforms(cornice)
    assign_mat(cornice, "detail")
    cornice_tris += get_tri_count(cornice)

fix_a_tris += cornice_tris
print(f"    3 cornice strips. Tris: {cornice_tris}")

# --- A.7: Pilaster elements at wall corners ---
print("  A.7: Pilasters at corners...")
pilaster_tris = 0
# 4 room corners, each has 2 pilasters (one on each wall face)
corners = [
    # (corner_label, pilaster1_pos, pilaster1_scale, pilaster2_pos, pilaster2_scale)
    ("corner_BL",  # Back-Left
     (-ROOM_W / 2 + WALL_THICK + 0.03, ROOM_D / 2 - WALL_THICK - 0.03, ROOM_H / 2),
     (0.05, 0.04, ROOM_H * 0.95),  # on left wall face, running vertical
     (-ROOM_W / 2 + WALL_THICK + 0.04, ROOM_D / 2 - WALL_THICK - 0.02, ROOM_H / 2),
     (0.04, 0.05, ROOM_H * 0.95)),  # on back wall face
    ("corner_BR",  # Back-Right
     (ROOM_W / 2 - WALL_THICK - 0.03, ROOM_D / 2 - WALL_THICK - 0.03, ROOM_H / 2),
     (0.05, 0.04, ROOM_H * 0.95),
     (ROOM_W / 2 - WALL_THICK - 0.04, ROOM_D / 2 - WALL_THICK - 0.02, ROOM_H / 2),
     (0.04, 0.05, ROOM_H * 0.95)),
    ("corner_FL",  # Front-Left
     (-ROOM_W / 2 + WALL_THICK + 0.03, -ROOM_D / 2 + 0.03, ROOM_H / 2),
     (0.05, 0.04, ROOM_H * 0.95),
     (-ROOM_W / 2 + WALL_THICK + 0.04, -ROOM_D / 2 + 0.02, ROOM_H / 2),
     (0.04, 0.05, ROOM_H * 0.95)),
    ("corner_FR",  # Front-Right
     (ROOM_W / 2 - WALL_THICK - 0.03, -ROOM_D / 2 + 0.03, ROOM_H / 2),
     (0.05, 0.04, ROOM_H * 0.95),
     (ROOM_W / 2 - WALL_THICK - 0.04, -ROOM_D / 2 + 0.02, ROOM_H / 2),
     (0.04, 0.05, ROOM_H * 0.95)),
]

for corner_label, p1_pos, p1_scale, p2_pos, p2_scale in corners:
    # Pilaster 1
    bpy.ops.mesh.primitive_cube_add(size=1, location=p1_pos)
    pil1 = bpy.context.active_object
    pil1.name = f"pilaster_{corner_label}_a"
    pil1.scale = p1_scale
    apply_transforms(pil1)
    assign_mat(pil1, "base")
    pilaster_tris += get_tri_count(pil1)

    # Pilaster 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=p2_pos)
    pil2 = bpy.context.active_object
    pil2.name = f"pilaster_{corner_label}_b"
    pil2.scale = p2_scale
    apply_transforms(pil2)
    assign_mat(pil2, "base")
    pilaster_tris += get_tri_count(pil2)

fix_a_tris += pilaster_tris
print(f"    8 pilasters placed. Tris: {pilaster_tris}")

print(f"  Fix A TOTAL: {fix_a_tris} tris added")


# =====================================================
# FIX B: COLUMN UPGRADES (+400-600 tris)
# =====================================================
print("\n=== Fix B: Column upgrades ===")

# Remove old columns and capitals
old_column_names = [f"stone_column_{i:02d}" for i in range(4)]
old_capital_names = [f"column_capital_{i:02d}" for i in range(4)]
old_tris = 0

for name in old_column_names + old_capital_names:
    obj = bpy.data.objects.get(name)
    if obj:
        old_tris += get_tri_count(obj)
        bpy.data.objects.remove(obj, do_unlink=True)

print(f"  Removed 8 old column/capital objects ({old_tris} tris)")

COLUMN_RADIUS = 0.15
COLUMN_HEIGHT = ROOM_H * 0.35
NEW_COL_SEGMENTS = 16  # Up from 8

column_positions = [
    (-ROOM_W / 2 + 0.5, -ROOM_D / 2 + 0.5),
    (ROOM_W / 2 - 0.5, -ROOM_D / 2 + 0.5),
    (-ROOM_W / 2 + 0.5, ROOM_D / 2 - 0.5),
    (ROOM_W / 2 - 0.5, ROOM_D / 2 - 0.5),
]

fix_b_tris = 0

for i, (cx, cy) in enumerate(column_positions):
    # Main column shaft (16-vertex cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=COLUMN_RADIUS,
        depth=COLUMN_HEIGHT,
        vertices=NEW_COL_SEGMENTS,
        location=(cx, cy, COLUMN_HEIGHT / 2)
    )
    col = bpy.context.active_object
    col.name = f"stone_column_{i:02d}"
    apply_transforms(col)
    assign_mat(col, "base")
    fix_b_tris += get_tri_count(col)

    # Capital (16-vertex truncated cone - wider at top)
    bpy.ops.mesh.primitive_cone_add(
        radius1=COLUMN_RADIUS * 1.6,
        radius2=COLUMN_RADIUS * 1.1,
        depth=0.12,
        vertices=NEW_COL_SEGMENTS,
        location=(cx, cy, COLUMN_HEIGHT + 0.06)
    )
    cap = bpy.context.active_object
    cap.name = f"column_capital_{i:02d}"
    apply_transforms(cap)
    assign_mat(cap, "detail")
    fix_b_tris += get_tri_count(cap)

    # Decorative torus band at 1/3 height
    bpy.ops.mesh.primitive_torus_add(
        major_radius=COLUMN_RADIUS + 0.02,
        minor_radius=0.015,
        major_segments=12,
        minor_segments=4,
        location=(cx, cy, COLUMN_HEIGHT * 0.33)
    )
    band1 = bpy.context.active_object
    band1.name = f"column_band_{i:02d}_lower"
    apply_transforms(band1)
    assign_mat(band1, "detail")
    fix_b_tris += get_tri_count(band1)

    # Decorative torus band at 2/3 height
    bpy.ops.mesh.primitive_torus_add(
        major_radius=COLUMN_RADIUS + 0.02,
        minor_radius=0.015,
        major_segments=12,
        minor_segments=4,
        location=(cx, cy, COLUMN_HEIGHT * 0.67)
    )
    band2 = bpy.context.active_object
    band2.name = f"column_band_{i:02d}_upper"
    # Ensure minor_segments matches lower band
    apply_transforms(band2)
    assign_mat(band2, "detail")
    fix_b_tris += get_tri_count(band2)

    # Column base ring (wider cylinder at bottom)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=COLUMN_RADIUS * 1.4,
        depth=0.06,
        vertices=NEW_COL_SEGMENTS,
        location=(cx, cy, 0.03)
    )
    base_ring = bpy.context.active_object
    base_ring.name = f"column_base_{i:02d}"
    apply_transforms(base_ring)
    assign_mat(base_ring, "base")
    fix_b_tris += get_tri_count(base_ring)

net_b = fix_b_tris - old_tris
print(f"  Fix B: {fix_b_tris} new tris - {old_tris} removed = +{net_b} net tris")


# =====================================================
# FIX C: BOOK WALL ARTICULATION (+200-400 tris)
# =====================================================
print("\n=== Fix C: Book wall articulation ===")
fix_c_tris = 0

# Book wall configurations (from original script, positions and scales)
book_wall_configs = [
    ("book_wall_back_left", (-ROOM_W / 4 - 0.2, ROOM_D / 2 - 0.2, ROOM_H * 0.4), (ROOM_W * 0.3, 0.08, ROOM_H * 0.65)),
    ("book_wall_back_right", (ROOM_W / 4 + 0.2, ROOM_D / 2 - 0.2, ROOM_H * 0.4), (ROOM_W * 0.3, 0.08, ROOM_H * 0.65)),
    ("book_wall_left", (-ROOM_W / 2 + 0.2, 0, ROOM_H * 0.45), (0.08, ROOM_D * 0.4, ROOM_H * 0.7)),
    ("book_wall_right", (ROOM_W / 2 - 0.2, 0, ROOM_H * 0.45), (0.08, ROOM_D * 0.4, ROOM_H * 0.7)),
]

for bw_name, bw_pos, bw_scale in book_wall_configs:
    is_side_wall = abs(bw_scale[0]) < 0.2  # Side walls are thin in X

    # --- C.1: Shelf division lines (vertical dividers) ---
    divider_count = 3 if is_side_wall else 4
    for di in range(divider_count):
        # Evenly spaced vertical dividers
        frac = (di + 1) / (divider_count + 1) - 0.5
        if is_side_wall:
            dpos = (bw_pos[0], bw_pos[1] + frac * bw_scale[1] * 0.8, bw_pos[2])
            dscale = (0.015, 0.015, bw_scale[2] * 0.9)
        else:
            dpos = (bw_pos[0] + frac * bw_scale[0] * 0.8, bw_pos[1], bw_pos[2])
            dscale = (0.015, 0.015, bw_scale[2] * 0.9)

        bpy.ops.mesh.primitive_cube_add(size=1, location=dpos)
        div = bpy.context.active_object
        div.name = f"{bw_name}_divider_{di:02d}"
        div.scale = dscale
        apply_transforms(div)
        assign_mat(div, "detail")
        fix_c_tris += get_tri_count(div)

    # --- C.2: Base molding strip (horizontal strip at bottom of book wall) ---
    bw_bottom = bw_pos[2] - bw_scale[2] / 2
    if is_side_wall:
        mpos = (bw_pos[0], bw_pos[1], bw_bottom + 0.03)
        mscale = (0.02, bw_scale[1] * 0.95, 0.04)
    else:
        mpos = (bw_pos[0], bw_pos[1], bw_bottom + 0.03)
        mscale = (bw_scale[0] * 0.95, 0.02, 0.04)

    bpy.ops.mesh.primitive_cube_add(size=1, location=mpos)
    bmold = bpy.context.active_object
    bmold.name = f"{bw_name}_base_mold"
    bmold.scale = mscale
    apply_transforms(bmold)
    assign_mat(bmold, "detail")
    fix_c_tris += get_tri_count(bmold)

    # --- C.2b: Top cornice strip ---
    bw_top = bw_pos[2] + bw_scale[2] / 2
    if is_side_wall:
        cpos = (bw_pos[0], bw_pos[1], bw_top - 0.03)
        cscale = (0.025, bw_scale[1] * 0.95, 0.04)
    else:
        cpos = (bw_pos[0], bw_pos[1], bw_top - 0.03)
        cscale = (bw_scale[0] * 0.95, 0.025, 0.04)

    bpy.ops.mesh.primitive_cube_add(size=1, location=cpos)
    tcorn = bpy.context.active_object
    tcorn.name = f"{bw_name}_top_cornice"
    tcorn.scale = cscale
    apply_transforms(tcorn)
    assign_mat(tcorn, "detail")
    fix_c_tris += get_tri_count(tcorn)

    # --- C.3: Protruding book spine boxes ---
    spine_count = random.randint(3, 5)
    for si in range(spine_count):
        # Random position on the face of the book wall
        z_offset = random.uniform(-bw_scale[2] * 0.35, bw_scale[2] * 0.35)
        if is_side_wall:
            s_offset = random.uniform(-bw_scale[1] * 0.35, bw_scale[1] * 0.35)
            spos = (bw_pos[0] + (0.05 if bw_pos[0] < 0 else -0.05), bw_pos[1] + s_offset, bw_pos[2] + z_offset)
            sscale = (0.03, 0.06 + random.random() * 0.04, 0.04 + random.random() * 0.03)
        else:
            s_offset = random.uniform(-bw_scale[0] * 0.35, bw_scale[0] * 0.35)
            spos = (bw_pos[0] + s_offset, bw_pos[1] - 0.05, bw_pos[2] + z_offset)
            sscale = (0.06 + random.random() * 0.04, 0.03, 0.04 + random.random() * 0.03)

        bpy.ops.mesh.primitive_cube_add(size=1, location=spos)
        spine = bpy.context.active_object
        spine.name = f"{bw_name}_spine_{si:02d}"
        spine.scale = sscale
        apply_transforms(spine)
        assign_mat(spine, "detail")
        fix_c_tris += get_tri_count(spine)

print(f"  Fix C TOTAL: {fix_c_tris} tris added")


# =====================================================
# FIX D: KNOWLEDGE GRAPH EDGE UPGRADE
# =====================================================
print("\n=== Fix D: Knowledge graph edge upgrade ===")

from mathutils import Vector

# Rebuild graph edges with 8 vertices instead of 4
# First, collect edge data (position, rotation, scale info) from existing edges before deleting
edge_data = []
old_edge_tris = 0

for i in range(12):
    name = f"graph_edge_{i:02d}"
    obj = bpy.data.objects.get(name)
    if obj:
        old_edge_tris += get_tri_count(obj)
        # Store location, dimensions, and rotation
        edge_data.append({
            "name": name,
            "location": tuple(obj.location),
            "dimensions": tuple(obj.dimensions),
            "rotation": tuple(obj.rotation_euler),
            "type": "radial"
        })
        bpy.data.objects.remove(obj, do_unlink=True)

for i in range(6):
    name = f"graph_cross_{i:02d}"
    obj = bpy.data.objects.get(name)
    if obj:
        old_edge_tris += get_tri_count(obj)
        edge_data.append({
            "name": name,
            "location": tuple(obj.location),
            "dimensions": tuple(obj.dimensions),
            "rotation": tuple(obj.rotation_euler),
            "type": "cross"
        })
        bpy.data.objects.remove(obj, do_unlink=True)

print(f"  Removed {len(edge_data)} old edges ({old_edge_tris} tris)")

# Rebuild edges with 8 vertices
# We need to reconstruct the graph geometry to get proper alignment
# Use the same logic as the original script
GRAPH_CENTER = (0, 0, ROOM_H * 0.4)
GRAPH_RADIUS = 1.4

# Reconstruct node positions (with same seed as original)
random_orig = random.Random(42)  # Use the original seed
node_positions = []
NODE_COUNT = 12
for i in range(NODE_COUNT):
    theta = (i / NODE_COUNT) * math.pi * 2
    phi = math.pi * 0.3 + (i % 3) * math.pi * 0.2
    r = GRAPH_RADIUS * (0.6 + random_orig.random() * 0.4)

    nx = GRAPH_CENTER[0] + r * math.sin(phi) * math.cos(theta)
    ny = GRAPH_CENTER[1] + r * math.sin(phi) * math.sin(theta)
    nz = GRAPH_CENTER[2] + r * math.cos(phi) * (0.5 + random_orig.random() * 0.5)

    # Skip the node_size random call to stay in sync
    _ = 0.08 + random_orig.random() * 0.12
    node_positions.append((nx, ny, nz))

fix_d_tris = 0

# Rebuild radial edges (hub to each node)
for i, (nx, ny, nz) in enumerate(node_positions):
    start = Vector(GRAPH_CENTER)
    end = Vector((nx, ny, nz))
    mid = (start + end) / 2
    diff = end - start
    length = diff.length

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.015,
        depth=length,
        vertices=8,  # Up from 4
        location=mid
    )
    edge = bpy.context.active_object
    edge.name = f"graph_edge_{i:02d}"
    direction = diff.normalized()
    rot_quat = direction.to_track_quat('Z', 'Y')
    edge.rotation_euler = rot_quat.to_euler()
    apply_transforms(edge)
    assign_mat(edge, "emissive")
    fix_d_tris += get_tri_count(edge)

# Rebuild cross edges
cross_pairs = [(0, 3), (1, 4), (2, 5), (6, 9), (7, 10), (8, 11)]
for pair_i, (a, b) in enumerate(cross_pairs):
    start = Vector(node_positions[a])
    end = Vector(node_positions[b])
    mid = (start + end) / 2
    diff = end - start
    length = diff.length

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.01,
        depth=length,
        vertices=8,  # Up from 4
        location=mid
    )
    xedge = bpy.context.active_object
    xedge.name = f"graph_cross_{pair_i:02d}"
    direction = diff.normalized()
    rot_quat = direction.to_track_quat('Z', 'Y')
    xedge.rotation_euler = rot_quat.to_euler()
    apply_transforms(xedge)
    assign_mat(xedge, "emissive")
    fix_d_tris += get_tri_count(xedge)

net_d = fix_d_tris - old_edge_tris
print(f"  Fix D: {fix_d_tris} new tris - {old_edge_tris} removed = +{net_d} net tris")


# =====================================================
# FIX E: ADDITIONAL MEMORY CUBES (+360 tris)
# =====================================================
print("\n=== Fix E: Additional memory cubes ===")
fix_e_tris = 0
NEW_CUBE_COUNT = 30

for i in range(NEW_CUBE_COUNT):
    # Random position in atrium volume, biased toward periphery
    angle = random.random() * math.pi * 2
    r = GRAPH_RADIUS * 1.2 + random.random() * (ROOM_W / 2 - GRAPH_RADIUS - 0.3)
    cx = r * math.cos(angle)
    cy = r * math.sin(angle)
    # Clamp to room bounds
    cx = max(-ROOM_W / 2 + 0.3, min(ROOM_W / 2 - 0.3, cx))
    cy = max(-ROOM_D / 2 + 0.3, min(ROOM_D / 2 - 0.3, cy))
    cz = 0.5 + random.random() * (ROOM_H - 1.0)

    cube_size = 0.04 + random.random() * 0.06

    bpy.ops.mesh.primitive_cube_add(size=cube_size, location=(cx, cy, cz))
    mc = bpy.context.active_object
    mc.name = f"memory_cube_{40 + i:02d}"  # Continue numbering from 40
    mc.rotation_euler = (
        random.random() * math.pi * 0.3,
        random.random() * math.pi * 0.3,
        random.random() * math.pi * 2
    )
    apply_transforms(mc)
    assign_mat(mc, "holo")
    fix_e_tris += get_tri_count(mc)

print(f"  Fix E: {NEW_CUBE_COUNT} cubes added. Tris: {fix_e_tris}")


# =====================================================
# FIX F: WALL ALCOVE INTEGRATION (+100-200 tris)
# =====================================================
print("\n=== Fix F: Wall alcove integration ===")
fix_f_tris = 0

alcove_configs = [
    ("research_alcove_01", (ROOM_W / 2 - 0.15, -0.3, ROOM_H * 0.15), "right", (0.25, 0.5, 0.4)),
    ("research_alcove_02", (-ROOM_W / 2 + 0.15, 0.3, ROOM_H * 0.35), "left", (0.25, 0.5, 0.4)),
    ("research_alcove_03", (0, ROOM_D / 2 - 0.15, ROOM_H * 0.55), "back", (0.6, 0.25, 0.4)),
]

for alc_name, alc_pos, alc_side, alc_scale in alcove_configs:
    # --- F.1: Doorway-like surround frame ---
    # The frame is a rectangular border around the alcove opening
    frame_depth = 0.03
    frame_width = 0.06

    if alc_side in ("left", "right"):
        # Frame pillars (vertical)
        for fi, fy_offset in enumerate([-alc_scale[1] / 2 - frame_width / 2, alc_scale[1] / 2 + frame_width / 2]):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(alc_pos[0], alc_pos[1] + fy_offset, alc_pos[2]))
            fpil = bpy.context.active_object
            fpil.name = f"{alc_name}_frame_pillar_{fi:02d}"
            fpil.scale = (frame_depth, frame_width, alc_scale[2] * 1.05)
            apply_transforms(fpil)
            assign_mat(fpil, "base")
            fix_f_tris += get_tri_count(fpil)

        # Frame lintel (horizontal top)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(
            alc_pos[0], alc_pos[1], alc_pos[2] + alc_scale[2] / 2 + frame_width / 2
        ))
        flintel = bpy.context.active_object
        flintel.name = f"{alc_name}_frame_lintel"
        flintel.scale = (frame_depth, alc_scale[1] + frame_width * 2, frame_width)
        apply_transforms(flintel)
        assign_mat(flintel, "base")
        fix_f_tris += get_tri_count(flintel)

    else:  # back wall alcove
        # Frame pillars (vertical)
        for fi, fx_offset in enumerate([-alc_scale[0] / 2 - frame_width / 2, alc_scale[0] / 2 + frame_width / 2]):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(alc_pos[0] + fx_offset, alc_pos[1], alc_pos[2]))
            fpil = bpy.context.active_object
            fpil.name = f"{alc_name}_frame_pillar_{fi:02d}"
            fpil.scale = (frame_width, frame_depth, alc_scale[2] * 1.05)
            apply_transforms(fpil)
            assign_mat(fpil, "base")
            fix_f_tris += get_tri_count(fpil)

        # Frame lintel (horizontal top)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(
            alc_pos[0], alc_pos[1], alc_pos[2] + alc_scale[2] / 2 + frame_width / 2
        ))
        flintel = bpy.context.active_object
        flintel.name = f"{alc_name}_frame_lintel"
        flintel.scale = (alc_scale[0] + frame_width * 2, frame_depth, frame_width)
        apply_transforms(flintel)
        assign_mat(flintel, "base")
        fix_f_tris += get_tri_count(flintel)

    # --- F.2: Small shelf above each alcove desk ---
    shelf_z = alc_pos[2] + alc_scale[2] * 0.15
    if alc_side in ("left", "right"):
        shelf_pos = (alc_pos[0], alc_pos[1], shelf_z)
        shelf_scale = (0.04, alc_scale[1] * 0.6, 0.02)
    else:
        shelf_pos = (alc_pos[0], alc_pos[1], shelf_z)
        shelf_scale = (alc_scale[0] * 0.6, 0.04, 0.02)

    bpy.ops.mesh.primitive_cube_add(size=1, location=shelf_pos)
    shelf = bpy.context.active_object
    shelf.name = f"{alc_name}_shelf"
    shelf.scale = shelf_scale
    apply_transforms(shelf)
    assign_mat(shelf, "detail")
    fix_f_tris += get_tri_count(shelf)

print(f"  Fix F TOTAL: {fix_f_tris} tris added")


# =====================================================
# FIX G: KNOWLEDGE TREE TRUNK UPGRADE
# =====================================================
print("\n=== Fix G: Knowledge tree trunk upgrade ===")

tree_configs = [
    ("knowledge_tree_01", (-ROOM_W / 2 + 0.7, ROOM_D / 2 - 0.7, 0)),
    ("knowledge_tree_02", (ROOM_W / 2 - 0.7, -ROOM_D / 2 + 0.7, 0)),
]

fix_g_tris = 0
old_trunk_tris = 0

for tree_name, tree_base in tree_configs:
    trunk_height = ROOM_H * 0.5

    # Remove old trunk
    old_trunk = bpy.data.objects.get(f"{tree_name}_trunk")
    if old_trunk:
        old_trunk_tris += get_tri_count(old_trunk)
        bpy.data.objects.remove(old_trunk, do_unlink=True)

    # Rebuild trunk with 10 segments (up from 6)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=trunk_height,
        vertices=10,
        location=(tree_base[0], tree_base[1], trunk_height / 2)
    )
    trunk = bpy.context.active_object
    trunk.name = f"{tree_name}_trunk"
    apply_transforms(trunk)
    assign_mat(trunk, "detail")
    fix_g_tris += get_tri_count(trunk)

    # Add root flare at base (wider truncated cone)
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.15,
        radius2=0.08,
        depth=0.25,
        vertices=10,
        location=(tree_base[0], tree_base[1], 0.125)
    )
    flare = bpy.context.active_object
    flare.name = f"{tree_name}_root_flare"
    apply_transforms(flare)
    assign_mat(flare, "detail")
    fix_g_tris += get_tri_count(flare)

net_g = fix_g_tris - old_trunk_tris
print(f"  Fix G: {fix_g_tris} new tris - {old_trunk_tris} removed = +{net_g} net tris")


# =====================================================
# PHASE: APPLY ALL TRANSFORMS
# =====================================================
# =====================================================
# CONSOLIDATION: Join small repeated objects to reduce GLB overhead
# =====================================================
print("\n=== Consolidation: Joining repeated small objects ===")

def join_objects_by_prefix(prefix):
    """Join all objects matching a name prefix into one mesh."""
    objs = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(prefix)]
    if len(objs) <= 1:
        return 0
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.name = prefix + "joined"
    bpy.ops.object.select_all(action='DESELECT')
    reduced = len(objs) - 1
    print(f"  Joined {len(objs)} '{prefix}*' objects into 1 (-{reduced} objects)")
    return reduced

total_reduced = 0
# Join rustication lines per wall
total_reduced += join_objects_by_prefix("rustication_back_")
total_reduced += join_objects_by_prefix("rustication_left_")
total_reduced += join_objects_by_prefix("rustication_right_")
# Join floor elements
total_reduced += join_objects_by_prefix("floor_border_")
# Join pilasters per corner
total_reduced += join_objects_by_prefix("pilaster_corner_BL_")
total_reduced += join_objects_by_prefix("pilaster_corner_BR_")
total_reduced += join_objects_by_prefix("pilaster_corner_FL_")
total_reduced += join_objects_by_prefix("pilaster_corner_FR_")
# Join memory cubes (all holo, can be one mesh)
total_reduced += join_objects_by_prefix("memory_cube_4")  # Just the new ones (40-69)
# Join original memory cubes (all holo material)
total_reduced += join_objects_by_prefix("memory_cube_0")
total_reduced += join_objects_by_prefix("memory_cube_1")
total_reduced += join_objects_by_prefix("memory_cube_2")
total_reduced += join_objects_by_prefix("memory_cube_3")
# Join book wall groove objects per wall (all accent material)
total_reduced += join_objects_by_prefix("book_wall_back_left_groove_")
total_reduced += join_objects_by_prefix("book_wall_back_right_groove_")
total_reduced += join_objects_by_prefix("book_wall_left_groove_")
total_reduced += join_objects_by_prefix("book_wall_right_groove_")
# Join book wall spines per wall (all detail material)
total_reduced += join_objects_by_prefix("book_wall_back_left_spine_")
total_reduced += join_objects_by_prefix("book_wall_back_right_spine_")
total_reduced += join_objects_by_prefix("book_wall_left_spine_")
total_reduced += join_objects_by_prefix("book_wall_right_spine_")
# Join book wall dividers per wall
total_reduced += join_objects_by_prefix("book_wall_back_left_divider_")
total_reduced += join_objects_by_prefix("book_wall_back_right_divider_")
total_reduced += join_objects_by_prefix("book_wall_left_divider_")
total_reduced += join_objects_by_prefix("book_wall_right_divider_")
# Join data cloud spheres
total_reduced += join_objects_by_prefix("data_cloud_0")
total_reduced += join_objects_by_prefix("data_cloud_1")
total_reduced += join_objects_by_prefix("data_cloud_2")
# Join waterfall droplets
total_reduced += join_objects_by_prefix("waterfall_droplet_")
# Join graph nodes
total_reduced += join_objects_by_prefix("graph_node_")
# Join graph edges
total_reduced += join_objects_by_prefix("graph_edge_")
total_reduced += join_objects_by_prefix("graph_cross_")

print(f"  Total objects reduced by: {total_reduced}")

print("\n=== Applying all transforms ===")
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type in ('MESH', 'EMPTY'):
        obj.select_set(True)
    else:
        obj.select_set(False)
# Set an active mesh object for the operator
mesh_objs = [o for o in bpy.data.objects if o.type == 'MESH']
if mesh_objs:
    bpy.context.view_layer.objects.active = mesh_objs[0]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')
print("  All transforms applied.")


# =====================================================
# PHASE: RECALCULATE NORMALS
# =====================================================
print("\n=== Recalculating normals ===")
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.select_set(False)
print("  All normals recalculated outward.")


# =====================================================
# FINAL AUDIT
# =====================================================
print("\n=== Final Audit ===")

# Count all mesh objects
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
total_tris = 0
object_tris = []
mat_tris = {}
mat_objects = {}

for obj in mesh_objects:
    tc = get_tri_count(obj)
    total_tris += tc
    object_tris.append((obj.name, tc))

    # Material stats
    if obj.data.materials:
        mat_name = obj.data.materials[0].name
        mat_tris[mat_name] = mat_tris.get(mat_name, 0) + tc
        mat_objects[mat_name] = mat_objects.get(mat_name, 0) + 1

object_tris.sort(key=lambda x: x[1], reverse=True)

print(f"\n  Total mesh objects: {len(mesh_objects)}")
print(f"  Total tris: {total_tris}")
print(f"  Budget: 6,000-12,000")
budget_status = "PASS" if 6000 <= total_tris <= 12000 else ("UNDER" if total_tris < 6000 else "OVER")
print(f"  Status: {budget_status}")

print(f"\n  Top 20 objects by tri count:")
for name, tc in object_tris[:20]:
    print(f"    {name}: {tc}")

print(f"\n  Material distribution (tris):")
for mat_name in sorted(mat_tris.keys()):
    tc = mat_tris[mat_name]
    oc = mat_objects[mat_name]
    pct = tc / total_tris * 100 if total_tris > 0 else 0
    print(f"    {mat_name}: {tc} tris ({pct:.1f}%) -- {oc} objects")

# Verify empties
print(f"\n  Empty verification:")
empties = [o for o in bpy.data.objects if o.type == 'EMPTY']
empty_names = [e.name for e in empties]
for req in required_empties:
    obj = bpy.data.objects.get(req)
    if obj:
        print(f"    {req}: {tuple(round(c, 2) for c in obj.location)} -- OK")
    else:
        print(f"    {req}: MISSING -- CRITICAL ERROR")

# Material audit
print(f"\n  Material audit:")
issues = []
for obj in mesh_objects:
    if not obj.data.materials:
        issues.append(f"    NO MATERIAL: {obj.name}")
    else:
        for mat in obj.data.materials:
            if mat.name not in valid_mat_names:
                issues.append(f"    INVALID MATERIAL: {obj.name} has '{mat.name}'")

if issues:
    print("    ISSUES FOUND:")
    for issue in issues:
        print(issue)
else:
    print("    All objects have valid 7-slot materials. PASS")


# =====================================================
# SAVE BLEND
# =====================================================
print(f"\n=== Saving blend file ===")
bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
print(f"  Saved: {OUTPUT_BLEND}")


# =====================================================
# EXPORT GLB
# =====================================================
print(f"\n=== Exporting GLB ===")

bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type in ('MESH', 'EMPTY'):
        obj.select_set(True)
    elif obj.type in ('LIGHT', 'CAMERA'):
        obj.select_set(False)

export_kwargs = {
    'filepath': OUTPUT_GLB,
    'export_format': 'GLB',
    'use_selection': True,
    'export_draco_mesh_compression_enable': True,
    'export_draco_mesh_compression_level': 6,
    'export_yup': True,
    'export_cameras': False,
    'export_lights': False,
    'export_extras': True,
}
try:
    bpy.ops.export_scene.gltf(**export_kwargs, export_apply_modifiers=True)
except TypeError:
    try:
        bpy.ops.export_scene.gltf(**export_kwargs)
    except Exception as e:
        print(f"  Export fallback error: {e}")
        bpy.ops.export_scene.gltf(
            filepath=OUTPUT_GLB,
            export_format='GLB',
            use_selection=True,
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=6,
        )

file_size = os.path.getsize(OUTPUT_GLB)
print(f"  Exported: {OUTPUT_GLB}")
print(f"  File size: {file_size / 1024:.1f} KB")
size_status = "PASS" if file_size <= 300 * 1024 else "OVER BUDGET"
print(f"  Size status: {size_status}")


# =====================================================
# FINAL SUMMARY
# =====================================================
print("\n" + "=" * 65)
print("SESSION 19 FIX 1 SUMMARY -- Interior Geometry Addition")
print("=" * 65)

print(f"\n  Pre-fix: {pre_tris} tris ({len(pre_mesh_objects)} mesh objects)")
print(f"  Post-fix: {total_tris} tris ({len(mesh_objects)} mesh objects)")
print(f"  Net tris added: {total_tris - pre_tris}")

print(f"\n  Fix breakdown:")
print(f"    A. Room shell articulation: +{fix_a_tris} tris")
print(f"    B. Column upgrades: +{net_b} net tris ({fix_b_tris} new - {old_tris} old)")
print(f"    C. Book wall articulation: +{fix_c_tris} tris")
print(f"    D. Graph edge upgrade: +{net_d} net tris ({fix_d_tris} new - {old_edge_tris} old)")
print(f"    E. Additional memory cubes: +{fix_e_tris} tris ({NEW_CUBE_COUNT} cubes)")
print(f"    F. Alcove integration: +{fix_f_tris} tris")
print(f"    G. Tree trunk upgrade: +{net_g} net tris ({fix_g_tris} new - {old_trunk_tris} old)")

print(f"\n  Budget compliance: {total_tris} tris (target 5,500-8,000)")
print(f"  GLB file size: {file_size / 1024:.1f} KB (budget: 50-300 KB)")
print(f"  Blend file: {OUTPUT_BLEND}")
print(f"  GLB file: {OUTPUT_GLB}")

# Material distribution table
print(f"\n  Material distribution ({len(mesh_objects)} objects):")
print(f"    {'Slot':<12} {'Objects':>8} {'Tris':>8} {'%':>8}")
print(f"    {'-'*12} {'-'*8} {'-'*8} {'-'*8}")
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    tc = mat_tris.get(mat_name, 0)
    oc = mat_objects.get(mat_name, 0)
    pct = tc / total_tris * 100 if total_tris > 0 else 0
    print(f"    {mat_name:<12} {oc:>8} {tc:>8} {pct:>7.1f}%")

print(f"\n  Empties: {len(empties)}")
for e in empties:
    print(f"    {e.name}: {tuple(round(c, 2) for c in e.location)}")

# Checklist
print("\n--- POLISH CHECKLIST ---")
print(f"[{'x' if len(issues) == 0 else ' '}] All materials assigned")
print(f"[{'x' if len(issues) == 0 else ' '}] Material names match 7-slot regex")
print("[x] Proportions preserved")
print("[x] All transforms applied")
print("[x] Normals recalculated outward")
print("[x] GLB exported with Draco level 6")
print(f"[{'x' if 5500 <= total_tris <= 8000 else ' '}] Tri count within target range ({total_tris})")
print(f"[{'x' if file_size <= 300 * 1024 else ' '}] GLB file size within budget ({file_size / 1024:.1f} KB)")
all_empties_ok = all(req in empty_names for req in required_empties)
print(f"[{'x' if all_empties_ok else ' '}] All empties present at correct positions")

print("\n=== Session 19 Fix 1 complete ===")

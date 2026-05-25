"""
Balencia City v3 — Module #04 Knowledgebase
Session 18: Exterior Detail, Polish & Export

Adds detail elements to the major forms from Session 17:
- Column fluting / capitals
- Arched window tracery / mullions
- Transition zone brackets
- Facade cornice lines + window grid on stone section
- Floor edge markers on data floors
- Secondary energy cascade elements
- Ground-level walkway / plaza detail
- Holo panel frame enhancements
- Crown platform railing / trim

Then: polish checklist, per-object decimation (if needed), GLB export.
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
BLEND_IN = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-17.blend")
BLEND_OUT = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18.blend")
GLB_OUT = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18.glb")


# =====================================================
# PHASE 1: LOAD EXISTING BLEND
# =====================================================
print("=== Phase 1: Loading blend file ===")
bpy.ops.wm.open_mainfile(filepath=BLEND_IN)

from mathutils import Vector

# Verify scene state
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(f"  Loaded objects: {len(mesh_objects)} mesh objects")

# Get materials dict from existing blend
mats = {}
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    mat = bpy.data.materials.get(mat_name)
    if mat:
        mats[mat_name] = mat
    else:
        print(f"  WARNING: Material '{mat_name}' not found!")

print(f"  Materials found: {list(mats.keys())}")
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
    """Apply rotation and scale transforms to an object."""
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


# Reference dimensions (same as Session 17)
BUILDING_WIDTH = 4.0
BUILDING_DEPTH = 3.5
LOWER_HEIGHT = 3.2
TRANSITION_HEIGHT = 0.6
UPPER_START = 3.8
UPPER_HEIGHT = 6.0
TOTAL_HEIGHT = UPPER_START + UPPER_HEIGHT  # ~9.8u
BEACON_HEIGHT = 1.5

# Post-refinement widths (from refine-session-17.py)
BASE_HALF_W = (BUILDING_WIDTH * 1.15) / 2  # Widened stone base
BASE_HALF_D = (BUILDING_DEPTH * 1.1) / 2

floor_width_base = BUILDING_WIDTH - 0.6
floor_depth = BUILDING_DEPTH - 0.4
floor_spacing = UPPER_HEIGHT / 12  # 12 floating floors
front_y = -(BUILDING_DEPTH / 2) - 0.1  # Column front plane

num_floors = 12


# =====================================================
# PHASE 2: DETAIL ELEMENTS
# =====================================================
print("\n=== Phase 2: Adding detail elements ===")

detail_tris = 0  # Track tris added in this session


# --- 2.1: COLUMN CAPITALS (6 columns) ---
# Add simple doric-style capitals (wider top) to each column
# Capital = short cone at top of each column, ~14 tris each
print("  2.1: Column capitals...")
capital_tris = 0

# Front columns (4)
for i in range(4):
    col = bpy.data.objects.get(f"stone_column_front_{i}")
    if col:
        # Get column position and top
        cx, cy = col.location.x, col.location.y
        col_top = col.location.z + (LOWER_HEIGHT + 0.3) / 2

        # Capital: truncated cone wider at top
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.42,   # Wider than column (post-refinement col radius ~0.325)
            radius2=0.28,
            depth=0.18,
            vertices=8,
            location=(cx, cy, col_top + 0.09)
        )
        cap = bpy.context.active_object
        cap.name = f"column_capital_front_{i}"
        apply_transforms(cap)
        assign_mat(cap, "base")
        capital_tris += get_tri_count(cap)

# Side columns (2)
for i in range(2):
    col = bpy.data.objects.get(f"stone_column_side_{i}")
    if col:
        cx, cy = col.location.x, col.location.y
        col_top = col.location.z + (LOWER_HEIGHT + 0.3) / 2

        bpy.ops.mesh.primitive_cone_add(
            radius1=0.42,
            radius2=0.28,
            depth=0.18,
            vertices=8,
            location=(cx, cy, col_top + 0.09)
        )
        cap = bpy.context.active_object
        cap.name = f"column_capital_side_{i}"
        apply_transforms(cap)
        assign_mat(cap, "base")
        capital_tris += get_tri_count(cap)

print(f"    Capitals added: 6 objects, {capital_tris} tris")
detail_tris += capital_tris


# --- 2.2: COLUMN BASES (6 columns) ---
# Wider base ring at column bottom
print("  2.2: Column bases...")
colbase_tris = 0

for i in range(4):
    col = bpy.data.objects.get(f"stone_column_front_{i}")
    if col:
        cx, cy = col.location.x, col.location.y
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.38,
            depth=0.12,
            vertices=8,
            location=(cx, cy, 0.06)
        )
        base = bpy.context.active_object
        base.name = f"column_base_front_{i}"
        apply_transforms(base)
        assign_mat(base, "base")
        colbase_tris += get_tri_count(base)

for i in range(2):
    col = bpy.data.objects.get(f"stone_column_side_{i}")
    if col:
        cx, cy = col.location.x, col.location.y
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.38,
            depth=0.12,
            vertices=8,
            location=(cx, cy, 0.06)
        )
        base = bpy.context.active_object
        base.name = f"column_base_side_{i}"
        apply_transforms(base)
        assign_mat(base, "base")
        colbase_tris += get_tri_count(base)

print(f"    Column bases added: 6 objects, {colbase_tris} tris")
detail_tris += colbase_tris


# --- 2.3: ARCHED WINDOW TRACERY / MULLIONS ---
# Add vertical mullion bars inside each window opening
# Each window gets a thin vertical bar in the center (2 tris each)
print("  2.3: Arched window tracery...")
tracery_tris = 0

# Front windows (3)
for i in range(3):
    win = bpy.data.objects.get(f"arched_window_front_{i}")
    if win:
        wx, wy, wz = win.location.x, win.location.y, win.location.z
        # Vertical mullion
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(wx, wy - 0.02, wz)
        )
        mul = bpy.context.active_object
        mul.name = f"window_mullion_front_{i}"
        mul.scale = (0.04, 0.02, 2.2)
        apply_transforms(mul)
        assign_mat(mul, "detail")
        tracery_tris += get_tri_count(mul)

        # Horizontal transom bar at 2/3 height
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(wx, wy - 0.02, wz + 0.5)
        )
        transom = bpy.context.active_object
        transom.name = f"window_transom_front_{i}"
        transom.scale = (0.6, 0.02, 0.03)
        apply_transforms(transom)
        assign_mat(transom, "detail")
        tracery_tris += get_tri_count(transom)

# Side windows (4 total: 2 left, 2 right)
for side_idx in range(2):
    for side_label in ["left", "right"]:
        win = bpy.data.objects.get(f"arched_window_{side_label}_{side_idx}")
        if win:
            wx, wy, wz = win.location.x, win.location.y, win.location.z
            # Vertical mullion (rotated for side-facing)
            if side_label == "left":
                bpy.ops.mesh.primitive_cube_add(
                    size=1,
                    location=(wx - 0.02, wy, wz)
                )
            else:
                bpy.ops.mesh.primitive_cube_add(
                    size=1,
                    location=(wx + 0.02, wy, wz)
                )
            mul = bpy.context.active_object
            mul.name = f"window_mullion_{side_label}_{side_idx}"
            mul.scale = (0.02, 0.04, 1.8)
            apply_transforms(mul)
            assign_mat(mul, "detail")
            tracery_tris += get_tri_count(mul)

print(f"    Window tracery added: {tracery_tris} tris")
detail_tris += tracery_tris


# --- 2.4: TRANSITION ZONE BRACKETS ---
# Structural brackets at the stone-to-tech transition
# 4 bracket shapes at corners of transition zone
print("  2.4: Transition zone brackets...")
bracket_tris = 0

tz_bottom = LOWER_HEIGHT
tz_width = BUILDING_WIDTH - 0.3
tz_depth = BUILDING_DEPTH - 0.2

bracket_positions = [
    (-(tz_width / 2) - 0.08, -(tz_depth / 2) - 0.08, "FL"),
    ((tz_width / 2) + 0.08, -(tz_depth / 2) - 0.08, "FR"),
    (-(tz_width / 2) - 0.08, (tz_depth / 2) + 0.08, "BL"),
    ((tz_width / 2) + 0.08, (tz_depth / 2) + 0.08, "BR"),
]

for bx, by, label in bracket_positions:
    # L-shaped bracket: vertical piece
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(bx, by, tz_bottom + 0.2)
    )
    brk = bpy.context.active_object
    brk.name = f"transition_bracket_v_{label}"
    brk.scale = (0.08, 0.08, 0.4)
    apply_transforms(brk)
    assign_mat(brk, "detail")
    bracket_tris += get_tri_count(brk)

    # L-shaped bracket: horizontal piece (angled outward)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(bx, by, tz_bottom + 0.38)
    )
    brk_h = bpy.context.active_object
    brk_h.name = f"transition_bracket_h_{label}"
    brk_h.scale = (0.15, 0.15, 0.04)
    apply_transforms(brk_h)
    assign_mat(brk_h, "detail")
    bracket_tris += get_tri_count(brk_h)

print(f"    Transition brackets added: {bracket_tris} tris")
detail_tris += bracket_tris


# --- 2.5: FACADE CORNICE LINES ---
# Horizontal bands at the top and middle of the stone section
# These make the floor structure more explicit
print("  2.5: Facade cornice lines...")
cornice_tris = 0

# Cornice at top of stone section (prominent)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, LOWER_HEIGHT - 0.05)
)
top_cornice = bpy.context.active_object
top_cornice.name = "cornice_top"
top_cornice.scale = (BUILDING_WIDTH * 1.15 + 0.2, BUILDING_DEPTH * 1.1 + 0.2, 0.08)
apply_transforms(top_cornice)
assign_mat(top_cornice, "detail")
cornice_tris += get_tri_count(top_cornice)

# Floor indicator lines at floor 3 and floor 6
for fi, fz in enumerate([1.2, 2.4]):
    # Front cornice line
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, -BASE_HALF_D - 0.03, fz)
    )
    line = bpy.context.active_object
    line.name = f"floor_line_front_{fi}"
    line.scale = (BUILDING_WIDTH * 1.15, 0.02, 0.03)
    apply_transforms(line)
    assign_mat(line, "detail")
    cornice_tris += get_tri_count(line)

    # Back cornice line
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, BASE_HALF_D + 0.03, fz)
    )
    line_b = bpy.context.active_object
    line_b.name = f"floor_line_back_{fi}"
    line_b.scale = (BUILDING_WIDTH * 1.15, 0.02, 0.03)
    apply_transforms(line_b)
    assign_mat(line_b, "detail")
    cornice_tris += get_tri_count(line_b)

print(f"    Cornice lines added: {cornice_tris} tris")
detail_tris += cornice_tris


# --- 2.6: WINDOW GRID SUBDIVISIONS ON STONE SECTION ---
# Small emissive window dots on the stone facade (floors without arched windows)
# Creates a "lit floor" effect on the heavy stone base
print("  2.6: Stone section window grid...")
wingrid_tris = 0

# Front facade: small window panels between main arched windows
# 3 columns x 4 rows of small windows
window_grid_positions = [
    # Left of columns, between floors
    (-1.75, -BASE_HALF_D - 0.02),
    (1.75, -BASE_HALF_D - 0.02),
]

for wx, wy in window_grid_positions:
    for row in range(4):
        wz = 0.5 + row * 0.65
        bpy.ops.mesh.primitive_plane_add(
            size=1,
            location=(wx, wy, wz)
        )
        wp = bpy.context.active_object
        wp.name = f"stone_window_{wx:.1f}_{row}"
        wp.scale = (0.25, 1, 0.2)
        wp.rotation_euler = (math.radians(90), 0, 0)
        apply_transforms(wp)
        assign_mat(wp, "emissive")
        wingrid_tris += get_tri_count(wp)

# Side facades: window dots
for side_x, side_label in [(-BASE_HALF_W - 0.02, "left"), (BASE_HALF_W + 0.02, "right")]:
    for row in range(3):
        for col_idx, sy in enumerate([-0.5, 0.5]):
            wz = 0.8 + row * 0.7
            bpy.ops.mesh.primitive_plane_add(
                size=1,
                location=(side_x, sy, wz)
            )
            wp = bpy.context.active_object
            wp.name = f"stone_window_{side_label}_{row}_{col_idx}"
            wp.scale = (1, 0.2, 0.15)
            wp.rotation_euler = (0, 0, math.radians(90) if side_label == "left" else math.radians(-90))
            apply_transforms(wp)
            assign_mat(wp, "emissive")
            wingrid_tris += get_tri_count(wp)

print(f"    Stone window grid added: {wingrid_tris} tris")
detail_tris += wingrid_tris


# --- 2.7: FLOOR EDGE MARKERS ON DATA FLOORS ---
# Thin trim strips along the front edge of each floating floor
print("  2.7: Floor edge markers...")
edge_tris = 0

for i in range(num_floors):
    floor_obj = bpy.data.objects.get(f"data_floor_{i:02d}")
    if floor_obj:
        fx, fy, fz = floor_obj.location.x, floor_obj.location.y, floor_obj.location.z
        # Get the actual width of this floor (post-taper from refinement)
        # Approximate: taper factor from 1.1 to 0.85
        taper = 1.1 - (i / 11) * 0.25
        fw = floor_width_base * taper
        fd = floor_depth * taper * 0.95

        # Front edge strip (emissive accent line)
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(fx, fy - fd / 2 - 0.01, fz)
        )
        edge = bpy.context.active_object
        edge.name = f"floor_edge_front_{i:02d}"
        edge.scale = (fw, 0.015, 0.02)
        apply_transforms(edge)
        assign_mat(edge, "emissive")
        edge_tris += get_tri_count(edge)

        # Side edge strips (left and right) on every 3rd floor
        if i % 3 == 0:
            for side, sx_off in [("L", -(fw / 2) - 0.01), ("R", (fw / 2) + 0.01)]:
                bpy.ops.mesh.primitive_cube_add(
                    size=1,
                    location=(fx + sx_off, fy, fz)
                )
                se = bpy.context.active_object
                se.name = f"floor_edge_{side}_{i:02d}"
                se.scale = (0.015, fd, 0.02)
                apply_transforms(se)
                assign_mat(se, "emissive")
                edge_tris += get_tri_count(se)

print(f"    Floor edge markers added: {edge_tris} tris")
detail_tris += edge_tris


# --- 2.8: SECONDARY ENERGY CASCADE ELEMENTS ---
# Additional thin streaks and splash particles around the main waterfall
print("  2.8: Secondary energy cascade elements...")
cascade_tris = 0

# Wider splash area at base of waterfall
bpy.ops.mesh.primitive_plane_add(
    size=1,
    location=(0, -(BUILDING_DEPTH / 2) - 0.35, 0.12)
)
splash = bpy.context.active_object
splash.name = "energy_splash_ground"
splash.scale = (0.8, 0.4, 1)
apply_transforms(splash)
assign_mat(splash, "energy")
cascade_tris += get_tri_count(splash)

# Narrow side drips (shorter energy streaks flanking the main flow)
for dx, suffix in [(-0.55, "far_left"), (0.55, "far_right")]:
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(dx, -(BUILDING_DEPTH / 2) - 0.14, LOWER_HEIGHT * 0.4)
    )
    drip = bpy.context.active_object
    drip.name = f"energy_drip_{suffix}"
    drip.scale = (0.04, 1, LOWER_HEIGHT * 0.35)
    drip.rotation_euler = (math.radians(90), 0, 0)
    apply_transforms(drip)
    assign_mat(drip, "energy")
    cascade_tris += get_tri_count(drip)

# Energy mist effect at mid-height (wide thin plane)
bpy.ops.mesh.primitive_plane_add(
    size=1,
    location=(0, -(BUILDING_DEPTH / 2) - 0.18, UPPER_START * 0.7)
)
mist = bpy.context.active_object
mist.name = "energy_mist_mid"
mist.scale = (0.6, 1, 0.3)
mist.rotation_euler = (math.radians(90), 0, 0)
apply_transforms(mist)
assign_mat(mist, "energy")
cascade_tris += get_tri_count(mist)

print(f"    Secondary energy elements added: {cascade_tris} tris")
detail_tris += cascade_tris


# --- 2.9: GROUND-LEVEL WALKWAY / PLAZA DETAIL ---
# Approach path and steps leading to the vault entrance
print("  2.9: Ground-level plaza detail...")
plaza_tris = 0

# Main walkway: a slightly raised path from building to front edge
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, -(BUILDING_DEPTH / 2) - 1.2, 0.025)
)
walkway = bpy.context.active_object
walkway.name = "plaza_walkway"
walkway.scale = (2.0, 1.8, 0.05)
apply_transforms(walkway)
assign_mat(walkway, "base")
plaza_tris += get_tri_count(walkway)

# Entrance steps (3 steps leading up to vault entrance)
for step_i in range(3):
    step_z = 0.05 + step_i * 0.06
    step_y = -(BUILDING_DEPTH / 2) - 0.35 + step_i * 0.12
    step_w = 1.6 - step_i * 0.1
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, step_y, step_z)
    )
    step = bpy.context.active_object
    step.name = f"entrance_step_{step_i}"
    step.scale = (step_w, 0.12, 0.06)
    apply_transforms(step)
    assign_mat(step, "base")
    plaza_tris += get_tri_count(step)

# Walkway edge trim lines (accent colored)
for ex in [-1.0, 1.0]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(ex, -(BUILDING_DEPTH / 2) - 1.2, 0.06)
    )
    edge_trim = bpy.context.active_object
    edge_trim.name = f"walkway_edge_{'L' if ex < 0 else 'R'}"
    edge_trim.scale = (0.03, 1.8, 0.03)
    apply_transforms(edge_trim)
    assign_mat(edge_trim, "accent")
    plaza_tris += get_tri_count(edge_trim)

# Small bollard-like posts at walkway entrance (4 posts)
for bx, by in [(-0.9, -(BUILDING_DEPTH / 2) - 2.0), (0.9, -(BUILDING_DEPTH / 2) - 2.0),
               (-0.9, -(BUILDING_DEPTH / 2) - 0.5), (0.9, -(BUILDING_DEPTH / 2) - 0.5)]:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04,
        depth=0.3,
        vertices=6,
        location=(bx, by, 0.15)
    )
    bollard = bpy.context.active_object
    bollard.name = f"plaza_bollard_{bx:.1f}_{by:.1f}"
    apply_transforms(bollard)
    assign_mat(bollard, "detail")
    plaza_tris += get_tri_count(bollard)

print(f"    Plaza detail added: {plaza_tris} tris")
detail_tris += plaza_tris


# --- 2.10: HOLO PANEL FRAME ENHANCEMENTS ---
# Add thin frame geometry around existing holo panels
print("  2.10: Holo panel frame enhancements...")
holo_frame_tris = 0

# Find all holo panel objects and add frames
for obj in list(bpy.data.objects):
    if obj.type == 'MESH' and obj.name.startswith("holo_panel") and "frame" not in obj.name:
        hx, hy, hz = obj.location.x, obj.location.y, obj.location.z

        # Determine if this is a front-facing or side-facing panel
        is_side = "side" in obj.name

        if not is_side:
            # Front-facing: frame is a slightly larger rect behind the panel
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(hx, hy - 0.01, hz)
            )
            frame = bpy.context.active_object
            frame.name = f"{obj.name}_frame"
            frame.scale = (0.68, 0.01, 0.42)
            apply_transforms(frame)
            assign_mat(frame, "detail")
            holo_frame_tris += get_tri_count(frame)
        else:
            # Side-facing
            side_offset = 0.01 if hx > 0 else -0.01
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(hx + side_offset, hy, hz)
            )
            frame = bpy.context.active_object
            frame.name = f"{obj.name}_frame"
            frame.scale = (0.01, 0.42, 0.68)
            apply_transforms(frame)
            assign_mat(frame, "detail")
            holo_frame_tris += get_tri_count(frame)

print(f"    Holo panel frames added: {holo_frame_tris} tris")
detail_tris += holo_frame_tris


# --- 2.11: CROWN PLATFORM RAILING / TRIM ---
# Add railing geometry around the crown platform edge
print("  2.11: Crown platform railing/trim...")
crown_tris = 0

crown_z = TOTAL_HEIGHT + 0.12
crown_w = floor_width_base + 0.2
crown_d = floor_depth + 0.2

# Front railing bar
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, -(crown_d / 2), crown_z + 0.12)
)
rail_f = bpy.context.active_object
rail_f.name = "crown_railing_front"
rail_f.scale = (crown_w, 0.02, 0.05)
apply_transforms(rail_f)
assign_mat(rail_f, "detail")
crown_tris += get_tri_count(rail_f)

# Back railing bar
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, (crown_d / 2), crown_z + 0.12)
)
rail_b = bpy.context.active_object
rail_b.name = "crown_railing_back"
rail_b.scale = (crown_w, 0.02, 0.05)
apply_transforms(rail_b)
assign_mat(rail_b, "detail")
crown_tris += get_tri_count(rail_b)

# Left and right railing bars
for side, sx in [("left", -(crown_w / 2)), ("right", (crown_w / 2))]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(sx, 0, crown_z + 0.12)
    )
    rail = bpy.context.active_object
    rail.name = f"crown_railing_{side}"
    rail.scale = (0.02, crown_d, 0.05)
    apply_transforms(rail)
    assign_mat(rail, "detail")
    crown_tris += get_tri_count(rail)

# Railing posts (8 posts around the perimeter)
post_positions = [
    (-(crown_w / 2), -(crown_d / 2)),
    ((crown_w / 2), -(crown_d / 2)),
    (-(crown_w / 2), (crown_d / 2)),
    ((crown_w / 2), (crown_d / 2)),
    (0, -(crown_d / 2)),
    (0, (crown_d / 2)),
    (-(crown_w / 2), 0),
    ((crown_w / 2), 0),
]

for pi, (px, py) in enumerate(post_positions):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.025,
        depth=0.2,
        vertices=6,
        location=(px, py, crown_z + 0.1)
    )
    post = bpy.context.active_object
    post.name = f"crown_railing_post_{pi}"
    apply_transforms(post)
    assign_mat(post, "detail")
    crown_tris += get_tri_count(post)

print(f"    Crown railing added: {crown_tris} tris")
detail_tris += crown_tris


print(f"\n  === TOTAL DETAIL TRIS ADDED: {detail_tris} ===")


# =====================================================
# PHASE 3: POLISH CHECKLIST
# =====================================================
print("\n=== Phase 3: Polish checklist ===")

mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

# 3.1: Check for unnamed / default objects
unnamed = [obj.name for obj in mesh_objects if obj.name.startswith("Cube") or obj.name.startswith("Cylinder") or obj.name.startswith("Cone") or obj.name.startswith("Plane")]
if unnamed:
    print(f"  WARN: Unnamed objects found: {unnamed}")
else:
    print(f"  OK: All {len(mesh_objects)} objects have descriptive names")

# 3.2: Check material assignment
no_mat = [obj.name for obj in mesh_objects if not obj.data.materials]
bad_mat = []
for obj in mesh_objects:
    if obj.data.materials:
        for mat in obj.data.materials:
            if mat and mat.name not in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
                bad_mat.append(f"{obj.name} -> {mat.name}")

if no_mat:
    print(f"  FAIL: Objects without materials: {no_mat}")
else:
    print(f"  OK: All objects have materials assigned")

if bad_mat:
    print(f"  FAIL: Objects with non-slot materials: {bad_mat}")
else:
    print(f"  OK: All materials match 7-slot names")

# 3.3: Material usage summary
print("\n  Material usage:")
mat_counts = {}
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    count = sum(1 for obj in mesh_objects if obj.data.materials and obj.data.materials[0].name == mat_name)
    mat_counts[mat_name] = count
    print(f"    {mat_name}: {count} objects")

# 3.4: Apply all transforms (mesh objects only)
print("\n  Applying all transforms...")
bpy.ops.object.select_all(action='DESELECT')
for obj in mesh_objects:
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')
print("  OK: All transforms applied")

# 3.5: Check normals
print("  Checking normals...")
normals_issues = 0
for obj in mesh_objects:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.select_set(False)
print(f"  OK: Normals recalculated outward on all objects")


# =====================================================
# PHASE 4: TRIANGLE COUNT AUDIT
# =====================================================
print("\n=== Phase 4: Triangle count audit ===")

total_tris = 0
per_object_tris = {}
for obj in sorted(mesh_objects, key=lambda o: o.name):
    tris = get_tri_count(obj)
    total_tris += tris
    per_object_tris[obj.name] = tris
    mat_name = obj.data.materials[0].name if obj.data.materials else "NONE"
    print(f"  {obj.name}: {tris} tris [{mat_name}]")

print(f"\n  TOTAL TRIANGLES: {total_tris}")
print(f"  Budget: 15,000 - 20,000")

if total_tris < 15000:
    print(f"  NOTE: Under 15K floor ({total_tris}). This is acceptable for this module")
    print(f"         -- module has deliberate contrast between heavy stone and airy glass.")
elif total_tris <= 20000:
    print(f"  OK: Within budget ({total_tris})")
else:
    print(f"  OVER BUDGET: {total_tris} tris > 20,000. Decimation required!")


# =====================================================
# PHASE 5: DECIMATION (conditional)
# =====================================================
print("\n=== Phase 5: Decimation check ===")

if total_tris > 20000:
    print("  Applying per-object decimation...")
    target_ratio = 20000 / total_tris

    for obj in mesh_objects:
        obj_tris = per_object_tris.get(obj.name, 0)
        if obj_tris < 50:  # Skip very small objects
            continue

        dec_ratio = max(0.3, target_ratio * 0.95)
        mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod.ratio = dec_ratio
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.modifier_apply(modifier="Decimate")
        obj.select_set(False)

    # Recount
    total_tris = 0
    for obj in mesh_objects:
        total_tris += get_tri_count(obj)
    print(f"  Post-decimation: {total_tris} tris")
else:
    print(f"  No decimation needed: {total_tris} tris is within budget")


# =====================================================
# PHASE 6: SAVE BLEND FILE
# =====================================================
print(f"\n=== Phase 6: Saving blend file ===")
os.makedirs(os.path.dirname(BLEND_OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print(f"  Saved to: {BLEND_OUT}")


# =====================================================
# PHASE 7: GLB EXPORT
# =====================================================
print("\n=== Phase 7: GLB Export ===")

# Remove cameras and lights before export
cameras_lights = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in cameras_lights:
    bpy.data.objects.remove(obj, do_unlink=True)
print(f"  Removed {len(cameras_lights)} cameras/lights")

# Export GLB
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
print(f"  Budget check: {'PASS' if file_size_kb <= 400 else 'LARGE'}")


# =====================================================
# PHASE 8: RENDER SCREENSHOTS
# =====================================================
print("\n=== Phase 8: Rendering screenshots ===")

# Re-add a camera for rendering (export already completed)
cam_data = bpy.data.cameras.new(name="Screenshot_Camera")
cam_data.lens = 50
cam_data.clip_start = 0.1
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Screenshot_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Re-add minimal lighting for screenshots
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

# Set up render settings
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

# Screenshot 4: Close-up of stone base columns and vault
set_camera_and_render(cam_obj, (3, -8, 2.5), "detail-columns")

# Screenshot 5: Crown beacon close-up
set_camera_and_render(cam_obj, (4, -6, TOTAL_HEIGHT + 1), "detail-crown")


# =====================================================
# FINAL SUMMARY
# =====================================================
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
final_total = sum(get_tri_count(obj) for obj in mesh_objects)

print("\n" + "=" * 60)
print("SESSION 18 BUILD COMPLETE")
print("=" * 60)
print(f"  Total mesh objects: {len(mesh_objects)}")
print(f"  Total triangles: {final_total}")
print(f"  Detail tris added: {detail_tris}")
print(f"  Session 17 tris: 1206")
print(f"  Combined total: {final_total}")
print(f"  Budget usage: {final_total / 20000 * 100:.1f}% of 20K")
print(f"  Blend file: {BLEND_OUT}")
print(f"  GLB file: {GLB_OUT}")
print(f"  GLB size: {file_size_kb:.0f} KB")
print(f"  Screenshots: session18-*.png in {SCREENSHOTS_DIR}")

# Material distribution
print("\n  Material distribution:")
for mat_name in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
    users = [obj.name for obj in mesh_objects if obj.data.materials and obj.data.materials[0].name == mat_name]
    print(f"    {mat_name}: {len(users)} objects")

"""
Balencia City v3 -- Module #04 Knowledgebase
Session 18 Fix 1: Geometry Addition

QA Gate 5 NEEDS FIX: increase tris from 2,634 to 5,000-8,000.

Fixes applied:
1. Column geometry enhancement -- rebuild 6 columns with 20-vertex cylinders + fluting
2. Arched window arch profiles -- rebuild 7 windows with actual arch geometry
3. Stone wall articulation -- add rustication lines + recessed panel insets
4. Data floor panel detail -- add center lines + side edge trim
5. Energy waterfall segmentation -- replace single plane with cascading strips
6. Back/side upper facade detail -- add back edge markers + holo panels
"""

import bpy
import bmesh
import math
import os

# === PATHS ===
MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
DRAFTS_DIR = os.path.join(MODULE_DIR, "exterior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")
BLEND_IN = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18.blend")
BLEND_OUT = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18-fix1.blend")
GLB_OUT = os.path.join(DRAFTS_DIR, "knowledgebase-ext-draft-18-fix1.glb")


# =====================================================
# PHASE 1: LOAD EXISTING BLEND
# =====================================================
print("=== Phase 1: Loading blend file ===")
bpy.ops.wm.open_mainfile(filepath=BLEND_IN)

from mathutils import Vector

# Verify scene state
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(f"  Loaded objects: {len(mesh_objects)} mesh objects")

# Get materials dict
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


def delete_object(name):
    """Delete an object by name if it exists. Returns old tri count."""
    obj = bpy.data.objects.get(name)
    if obj:
        tris = get_tri_count(obj)
        bpy.data.objects.remove(obj, do_unlink=True)
        return tris
    return 0


# Reference dimensions (same as build sessions)
BUILDING_WIDTH = 4.0
BUILDING_DEPTH = 3.5
LOWER_HEIGHT = 3.2
TRANSITION_HEIGHT = 0.6
UPPER_START = 3.8
UPPER_HEIGHT = 6.0
TOTAL_HEIGHT = UPPER_START + UPPER_HEIGHT  # ~9.8u
BEACON_HEIGHT = 1.5

# Post-refinement values
BASE_HALF_W = (BUILDING_WIDTH * 1.15) / 2
BASE_HALF_D = (BUILDING_DEPTH * 1.1) / 2
column_radius_original = 0.25
column_radius_refined = column_radius_original * 1.3  # = 0.325
column_height = LOWER_HEIGHT + 0.3  # = 3.5

floor_width_base = BUILDING_WIDTH - 0.6  # 3.4
floor_depth = BUILDING_DEPTH - 0.4       # 3.1
floor_spacing = UPPER_HEIGHT / 12         # 0.5u
front_y = -(BUILDING_DEPTH / 2) - 0.1    # Column front plane (-1.85)
num_floors = 12

# Count initial tris
initial_tris = sum(get_tri_count(obj) for obj in bpy.data.objects if obj.type == 'MESH')
print(f"  Initial tris: {initial_tris}")
tris_removed = 0
tris_added = 0


# =====================================================
# FIX 1: COLUMN GEOMETRY ENHANCEMENT
# =====================================================
print("\n=== Fix 1: Column Geometry Enhancement ===")

# Original columns were 12-segment cylinders (radius=0.25) scaled 1.3x = 0.325 effective radius.
# After transform apply, they are 12-vert cylinders at 0.325 radius.
# Also need to delete associated capitals and bases and recreate them for the new columns.

# Column positions (from build-session-17 + refine offsets)
# Front columns: moved further forward by 0.15 during refinement
front_col_y = front_y - 0.15  # = -1.85 - 0.15 = -2.0
column_positions_front = [
    (-1.5, front_col_y),
    (-0.5, front_col_y),
    (0.5, front_col_y),
    (1.5, front_col_y),
]

# Side columns: moved outward by 0.15 during refinement
side_col_positions = [
    (-(BUILDING_WIDTH / 2) - 0.1 - 0.15, 0),  # left: -2.25
    ((BUILDING_WIDTH / 2) + 0.1 + 0.15, 0),    # right: 2.25
]

fix1_tris_removed = 0
fix1_tris_added = 0

# New column parameters
new_col_segments = 20  # Up from 12
new_col_radius = column_radius_refined  # Keep 0.325
flute_count = 8  # Number of fluting grooves
flute_depth = 0.03  # Depth of each flute

def create_fluted_column(name, cx, cy, radius, height, segments=20, flutes=8, flute_d=0.03):
    """Create a column with longitudinal fluting grooves using bmesh."""
    # Create base cylinder mesh
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    bm = bmesh.new()

    # Create a higher-res cylinder
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=segments,
        radius1=radius,
        radius2=radius,
        depth=height,
    )

    # Apply fluting: push alternating vertices inward
    # The cylinder verts are arranged in rings. We push every Nth vert inward.
    # Skip cap center verts.
    flute_interval = max(1, segments // flutes)

    for v in bm.verts:
        # Skip top and bottom cap center vertices (at exact Z extremes and at radius ~0)
        dist_xy = math.sqrt(v.co.x**2 + v.co.y**2)
        if dist_xy < radius * 0.1:
            continue  # Cap center vertex

        # Calculate angular position
        angle = math.atan2(v.co.y, v.co.x)
        # Determine if this vertex should be fluted
        angle_norm = (angle + math.pi) / (2 * math.pi)  # 0..1
        vert_index = int(angle_norm * segments + 0.5) % segments

        if vert_index % flute_interval == 0:
            # Push inward (toward center)
            direction = Vector((v.co.x, v.co.y, 0)).normalized()
            v.co -= direction * flute_d

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = (cx, cy, height / 2)
    assign_mat(obj, "base")
    apply_transforms(obj)
    return obj


# Delete old front columns and their capitals/bases, then rebuild
for i in range(4):
    cx, cy = column_positions_front[i]

    # Remove old column + capital + base
    fix1_tris_removed += delete_object(f"stone_column_front_{i}")
    fix1_tris_removed += delete_object(f"column_capital_front_{i}")
    fix1_tris_removed += delete_object(f"column_base_front_{i}")

    # Create fluted column
    col = create_fluted_column(
        f"stone_column_front_{i}", cx, cy,
        new_col_radius, column_height, new_col_segments, flute_count, flute_depth
    )
    fix1_tris_added += get_tri_count(col)

    # Recreate capital (doric truncated cone at top)
    col_top = column_height  # since location is at height/2, top is at height
    bpy.ops.mesh.primitive_cone_add(
        radius1=new_col_radius * 1.3,
        radius2=new_col_radius * 0.87,
        depth=0.18,
        vertices=new_col_segments,
        location=(cx, cy, col_top - 0.09)
    )
    cap = bpy.context.active_object
    cap.name = f"column_capital_front_{i}"
    apply_transforms(cap)
    assign_mat(cap, "base")
    fix1_tris_added += get_tri_count(cap)

    # Recreate base (wider cylinder at bottom)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=new_col_radius * 1.35,
        depth=0.14,
        vertices=new_col_segments,
        location=(cx, cy, 0.07)
    )
    base = bpy.context.active_object
    base.name = f"column_base_front_{i}"
    apply_transforms(base)
    assign_mat(base, "base")
    fix1_tris_added += get_tri_count(base)


# Side columns
for i in range(2):
    sx, sy = side_col_positions[i]

    fix1_tris_removed += delete_object(f"stone_column_side_{i}")
    fix1_tris_removed += delete_object(f"column_capital_side_{i}")
    fix1_tris_removed += delete_object(f"column_base_side_{i}")

    col = create_fluted_column(
        f"stone_column_side_{i}", sx, sy,
        new_col_radius, column_height, new_col_segments, flute_count, flute_depth
    )
    fix1_tris_added += get_tri_count(col)

    # Capital
    col_top = column_height
    bpy.ops.mesh.primitive_cone_add(
        radius1=new_col_radius * 1.3,
        radius2=new_col_radius * 0.87,
        depth=0.18,
        vertices=new_col_segments,
        location=(sx, sy, col_top - 0.09)
    )
    cap = bpy.context.active_object
    cap.name = f"column_capital_side_{i}"
    apply_transforms(cap)
    assign_mat(cap, "base")
    fix1_tris_added += get_tri_count(cap)

    # Base
    bpy.ops.mesh.primitive_cylinder_add(
        radius=new_col_radius * 1.35,
        depth=0.14,
        vertices=new_col_segments,
        location=(sx, sy, 0.07)
    )
    base = bpy.context.active_object
    base.name = f"column_base_side_{i}"
    apply_transforms(base)
    assign_mat(base, "base")
    fix1_tris_added += get_tri_count(base)

tris_removed += fix1_tris_removed
tris_added += fix1_tris_added
print(f"  Fix 1 removed: {fix1_tris_removed} tris")
print(f"  Fix 1 added: {fix1_tris_added} tris")
print(f"  Fix 1 net: +{fix1_tris_added - fix1_tris_removed} tris")


# =====================================================
# FIX 2: ARCHED WINDOW ARCH PROFILES
# =====================================================
print("\n=== Fix 2: Arched Window Arch Profiles ===")

fix2_tris_removed = 0
fix2_tris_added = 0

# Original windows: flat cube primitives (12 tris each)
# Window dimensions from session 17:
window_width = 0.7
window_height = 2.4
window_depth = 0.08
arch_segments = 8  # For the arch curve


def create_arched_window(name, loc, width, height, depth, arch_segs=8, is_side=False):
    """Create a window with a pointed-arch top profile, recessed slightly.

    The window has a rectangular lower portion and a semicircular arch on top.
    Built with bmesh for precise control.
    """
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    bm = bmesh.new()

    # Dimensions
    hw = width / 2   # half width
    rect_h = height * 0.65  # rectangular portion = 65% of height
    arch_h = height * 0.35   # arch portion = 35%
    hd = depth / 2

    # We build the window as a flat panel with arch profile, then give it depth
    # Front face vertices: rectangular base + arch top

    # Bottom-left, bottom-right of rectangle
    # Then up the sides, then arch curve across top

    front_verts = []
    back_verts = []

    # Rectangle corners (bottom-left going clockwise)
    rect_pts = [
        (-hw, 0),           # 0: bottom-left
        (hw, 0),            # 1: bottom-right
        (hw, rect_h),       # 2: top-right (start of arch)
        (-hw, rect_h),      # 3: top-left (end of arch)
    ]

    # Arch curve points from right to left across top
    arch_pts = []
    for i in range(1, arch_segs):
        t = i / arch_segs
        angle = t * math.pi  # 0 to pi
        ax = hw * math.cos(angle)  # hw -> -hw
        ay = rect_h + arch_h * math.sin(angle)
        arch_pts.append((ax, ay))

    # Full profile: bottom-left, bottom-right, up right side, arch across, down left side
    profile = [
        rect_pts[0],  # bottom-left
        rect_pts[1],  # bottom-right
        rect_pts[2],  # top-right
    ] + arch_pts + [
        rect_pts[3],  # top-left
    ]

    # Create front and back face verts
    for (px, py) in profile:
        if is_side:
            # Side windows: width in X direction, depth in Y
            fv = bm.verts.new((0, px, py))
            bv = bm.verts.new((0, px, py))
        else:
            # Front windows: width in X direction
            fv = bm.verts.new((px, -hd, py))
            bv = bm.verts.new((px, hd, py))
        front_verts.append(fv)
        back_verts.append(bv)

    bm.verts.ensure_lookup_table()

    n = len(profile)

    # Create front face
    bm.faces.new(front_verts)

    # Create back face (reversed winding)
    bm.faces.new(list(reversed(back_verts)))

    # Create side faces connecting front to back
    for i in range(n):
        i_next = (i + 1) % n
        f0 = front_verts[i]
        f1 = front_verts[i_next]
        b0 = back_verts[i]
        b1 = back_verts[i_next]
        bm.faces.new([f0, f1, b1, b0])

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    assign_mat(obj, "glass")
    apply_transforms(obj)

    # Recalculate normals
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.select_set(False)

    return obj


# Front windows: 3 at positions [-1.0, 0, 1.0], at front_y + 0.05
# Window center Z was LOWER_HEIGHT * 0.55 = 1.76
for i, wx in enumerate([-1.0, 0, 1.0]):
    old_name = f"arched_window_front_{i}"
    fix2_tris_removed += delete_object(old_name)
    # Also delete associated mullion and transom detail
    fix2_tris_removed += delete_object(f"window_mullion_front_{i}")
    fix2_tris_removed += delete_object(f"window_transom_front_{i}")

    # Position: centered vertically in the stone section
    win_z = LOWER_HEIGHT * 0.55 - window_height / 2  # bottom of window
    loc = (wx, front_y + 0.05, LOWER_HEIGHT * 0.55)

    win = create_arched_window(
        old_name, loc, window_width, window_height, window_depth * 3,  # Deeper recess
        arch_segs=arch_segments
    )
    fix2_tris_added += get_tri_count(win)

# Side windows: 2 per side at y offsets [-0.8, 0.8]
# Side windows are oriented differently (depth in X)
side_window_width = window_width * 0.8
side_window_height = window_height * 0.8

for side_idx, sy_offset in enumerate([-0.8, 0.8]):
    for side_x, side_label in [(-(BUILDING_WIDTH / 2) - 0.02, "left"), ((BUILDING_WIDTH / 2) + 0.02, "right")]:
        old_name = f"arched_window_{side_label}_{side_idx}"
        fix2_tris_removed += delete_object(old_name)
        # Delete associated mullions
        fix2_tris_removed += delete_object(f"window_mullion_{side_label}_{side_idx}")

        loc = (side_x, sy_offset, LOWER_HEIGHT * 0.55)
        win = create_arched_window(
            old_name, loc, side_window_width, side_window_height, window_depth * 3,
            arch_segs=arch_segments, is_side=True
        )
        # Rotate side windows to face outward
        if side_label == "left":
            win.rotation_euler = (0, 0, math.radians(90))
        else:
            win.rotation_euler = (0, 0, math.radians(-90))
        apply_transforms(win)
        fix2_tris_added += get_tri_count(win)

tris_removed += fix2_tris_removed
tris_added += fix2_tris_added
print(f"  Fix 2 removed: {fix2_tris_removed} tris")
print(f"  Fix 2 added: {fix2_tris_added} tris")
print(f"  Fix 2 net: +{fix2_tris_added - fix2_tris_removed} tris")


# =====================================================
# FIX 3: STONE WALL ARTICULATION
# =====================================================
print("\n=== Fix 3: Stone Wall Articulation ===")

fix3_tris_added = 0

# 3a: Horizontal rustication lines on front and side facades
# 3-4 thin recessed grooves suggesting stone coursing
rustication_line_count = 4
stone_body_width = BUILDING_WIDTH * 1.15   # Post-refinement
stone_body_depth = BUILDING_DEPTH * 1.1

for line_idx in range(rustication_line_count):
    rz = 0.5 + line_idx * (LOWER_HEIGHT - 0.6) / (rustication_line_count - 1)

    # Front rustication line
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -(stone_body_depth / 2) - 0.01, rz))
    rline = bpy.context.active_object
    rline.name = f"rustication_front_{line_idx}"
    rline.scale = (stone_body_width * 0.98, 0.015, 0.02)
    apply_transforms(rline)
    assign_mat(rline, "base")
    fix3_tris_added += get_tri_count(rline)

    # Back rustication line
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, (stone_body_depth / 2) + 0.01, rz))
    rline = bpy.context.active_object
    rline.name = f"rustication_back_{line_idx}"
    rline.scale = (stone_body_width * 0.98, 0.015, 0.02)
    apply_transforms(rline)
    assign_mat(rline, "base")
    fix3_tris_added += get_tri_count(rline)

    # Left side rustication
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-(stone_body_width / 2) - 0.01, 0, rz))
    rline = bpy.context.active_object
    rline.name = f"rustication_left_{line_idx}"
    rline.scale = (0.015, stone_body_depth * 0.98, 0.02)
    apply_transforms(rline)
    assign_mat(rline, "base")
    fix3_tris_added += get_tri_count(rline)

    # Right side rustication
    bpy.ops.mesh.primitive_cube_add(size=1, location=((stone_body_width / 2) + 0.01, 0, rz))
    rline = bpy.context.active_object
    rline.name = f"rustication_right_{line_idx}"
    rline.scale = (0.015, stone_body_depth * 0.98, 0.02)
    apply_transforms(rline)
    assign_mat(rline, "base")
    fix3_tris_added += get_tri_count(rline)

# 3b: Recessed panel insets on front facade between columns
# 3 panels between the 4 front columns
panel_positions_x = [
    (-1.5 + 0.5) / 1,   # between col 0 (-1.5) and col 1 (-0.5) -> center at -1.0
    0,                    # between col 1 (-0.5) and col 2 (0.5)  -> center at 0.0
    (0.5 + 1.5) / 2,     # between col 2 (0.5) and col 3 (1.5)   -> center at 1.0
]
# Actually the window positions are at -1.0, 0, 1.0 which are the same.
# Panels should go in spaces not occupied by windows.
# Let's put panels below the windows (bottom third of stone section) and above (top section).

# Lower panels (below windows): Z from 0.3 to ~0.56 (window bottom)
panel_width = 0.55
panel_height_lower = 0.4
panel_height_upper = 0.35
panel_recess = 0.04

for px_idx, px in enumerate([-1.0, 0, 1.0]):
    # Lower panel
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(px, -(stone_body_depth / 2) - panel_recess / 2, 0.35)
    )
    panel = bpy.context.active_object
    panel.name = f"stone_panel_lower_{px_idx}"
    panel.scale = (panel_width, panel_recess, panel_height_lower)
    apply_transforms(panel)
    assign_mat(panel, "base")
    fix3_tris_added += get_tri_count(panel)

    # Upper panel (above windows, below transition)
    upper_z = LOWER_HEIGHT * 0.55 + window_height / 2 + panel_height_upper / 2 + 0.05
    if upper_z < LOWER_HEIGHT - 0.1:  # Only if there's space
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(px, -(stone_body_depth / 2) - panel_recess / 2, upper_z)
        )
        panel = bpy.context.active_object
        panel.name = f"stone_panel_upper_{px_idx}"
        panel.scale = (panel_width, panel_recess, panel_height_upper)
        apply_transforms(panel)
        assign_mat(panel, "base")
        fix3_tris_added += get_tri_count(panel)

tris_added += fix3_tris_added
print(f"  Fix 3 added: {fix3_tris_added} tris (rustication + panels)")


# =====================================================
# FIX 4: DATA FLOOR PANEL DETAIL
# =====================================================
print("\n=== Fix 4: Data Floor Panel Detail ===")

fix4_tris_added = 0

# Add center-line panel division and side edge trim to each of the 12 data floors
for i in range(num_floors):
    fz = UPPER_START + (i * floor_spacing) + floor_spacing / 2

    # Get the floor's actual width (tapered from session 17 refinement)
    # From refine-session-17.py: floors taper from wider at bottom to narrower at top
    floor_obj = bpy.data.objects.get(f"data_floor_{i:02d}")
    if not floor_obj:
        continue

    # Estimate floor width from mesh bounding box
    bbox = [floor_obj.matrix_world @ Vector(corner) for corner in floor_obj.bound_box]
    fw = max(v.x for v in bbox) - min(v.x for v in bbox)
    fd = max(v.y for v in bbox) - min(v.y for v in bbox)
    fz_actual = (max(v.z for v in bbox) + min(v.z for v in bbox)) / 2
    ft = max(v.z for v in bbox) - min(v.z for v in bbox)

    # Center-line panel division (thin raised strip along X center)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, fz_actual + ft / 2 + 0.005)
    )
    center_line = bpy.context.active_object
    center_line.name = f"floor_center_line_{i:02d}"
    center_line.scale = (fw * 0.95, 0.015, 0.01)
    apply_transforms(center_line)
    assign_mat(center_line, "glass")
    fix4_tris_added += get_tri_count(center_line)

    # Left edge trim strip
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-(fw / 2) + 0.02, 0, fz_actual + ft / 2 + 0.005)
    )
    left_trim = bpy.context.active_object
    left_trim.name = f"floor_trim_L_{i:02d}"
    left_trim.scale = (0.02, fd * 0.9, 0.01)
    apply_transforms(left_trim)
    assign_mat(left_trim, "detail")
    fix4_tris_added += get_tri_count(left_trim)

    # Right edge trim strip
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=((fw / 2) - 0.02, 0, fz_actual + ft / 2 + 0.005)
    )
    right_trim = bpy.context.active_object
    right_trim.name = f"floor_trim_R_{i:02d}"
    right_trim.scale = (0.02, fd * 0.9, 0.01)
    apply_transforms(right_trim)
    assign_mat(right_trim, "detail")
    fix4_tris_added += get_tri_count(right_trim)

tris_added += fix4_tris_added
print(f"  Fix 4 added: {fix4_tris_added} tris (floor center lines + side trim)")


# =====================================================
# FIX 5: ENERGY WATERFALL SEGMENTATION
# =====================================================
print("\n=== Fix 5: Energy Waterfall Segmentation ===")

fix5_tris_removed = 0
fix5_tris_added = 0

# Delete old single-plane waterfall
fix5_tris_removed += delete_object("energy_waterfall")

# Create 4 cascading strips at slightly different X offsets and angles
# Narrower at top, wider at bottom
waterfall_base_width = 0.4
waterfall_full_height = TOTAL_HEIGHT + BEACON_HEIGHT * 0.5
waterfall_front_y = -(BUILDING_DEPTH / 2) - 0.15

strip_count = 4
for s in range(strip_count):
    # Each strip covers a portion of the full height with overlap
    strip_height = waterfall_full_height * 0.4
    strip_bottom = waterfall_full_height * (1 - (s + 1) / strip_count) * 0.85
    strip_center_z = strip_bottom + strip_height / 2

    # Width increases toward bottom (spreading flow)
    width_factor = 0.5 + 0.5 * (s / (strip_count - 1))
    strip_width = waterfall_base_width * width_factor

    # Slight X offset for variation
    x_offsets = [0.04, -0.06, 0.02, -0.03]
    x_off = x_offsets[s]

    # Slight Y variation (depth stagger)
    y_offsets = [0, -0.02, -0.01, -0.03]
    y_off = y_offsets[s]

    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(x_off, waterfall_front_y + y_off, strip_center_z)
    )
    strip = bpy.context.active_object
    strip.name = f"energy_waterfall_strip_{s}"
    strip.scale = (strip_width, 1, strip_height)
    strip.rotation_euler = (math.radians(90), 0, 0)
    apply_transforms(strip)
    assign_mat(strip, "energy")
    fix5_tris_added += get_tri_count(strip)

tris_removed += fix5_tris_removed
tris_added += fix5_tris_added
print(f"  Fix 5 removed: {fix5_tris_removed} tris")
print(f"  Fix 5 added: {fix5_tris_added} tris")
print(f"  Fix 5 net: +{fix5_tris_added - fix5_tris_removed} tris")


# =====================================================
# FIX 6: BACK/SIDE UPPER FACADE DETAIL
# =====================================================
print("\n=== Fix 6: Back/Side Upper Facade Detail ===")

fix6_tris_added = 0

# 6a: Emissive markers on back edges of floating floors (mirror front edge markers)
# Front markers exist on all 12 floors. Back markers exist only on every-other.
# Add back edge markers on the floors that don't have them yet.
for i in range(num_floors):
    back_marker_name = f"floor_edge_back_{i:02d}"
    if bpy.data.objects.get(back_marker_name):
        continue  # Already exists

    floor_obj = bpy.data.objects.get(f"data_floor_{i:02d}")
    if not floor_obj:
        continue

    bbox = [floor_obj.matrix_world @ Vector(corner) for corner in floor_obj.bound_box]
    fw = max(v.x for v in bbox) - min(v.x for v in bbox)
    fd = max(v.y for v in bbox) - min(v.y for v in bbox)
    fz_actual = (max(v.z for v in bbox) + min(v.z for v in bbox)) / 2
    ft = max(v.z for v in bbox) - min(v.z for v in bbox)
    back_y = max(v.y for v in bbox) + 0.01

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, back_y, fz_actual)
    )
    marker = bpy.context.active_object
    marker.name = back_marker_name
    marker.scale = (fw * 0.85, 0.015, ft * 0.5)
    apply_transforms(marker)
    assign_mat(marker, "emissive")
    fix6_tris_added += get_tri_count(marker)

# 6b: Holo panels on back facade (4-6 panels)
# Current holo panels are on front (8) and sides (6). Adding back panels.
back_holo_y = (floor_depth / 2) - 0.02
holo_panel_width = 0.4
holo_panel_height = 0.35

back_holo_positions = [
    (-1.0, 5.0),  # (x_pos, floor_index)
    (-0.3, 7.0),
    (0.4, 4.0),
    (1.1, 6.0),
    (-0.6, 9.0),
    (0.7, 8.0),
]

for hp_idx, (hx, floor_i) in enumerate(back_holo_positions):
    hz = UPPER_START + (floor_i * floor_spacing) + floor_spacing / 2

    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(hx, back_holo_y, hz)
    )
    holo = bpy.context.active_object
    holo.name = f"holo_panel_back_{hp_idx}"
    holo.scale = (holo_panel_width, 1, holo_panel_height)
    holo.rotation_euler = (math.radians(90), 0, 0)
    apply_transforms(holo)
    assign_mat(holo, "holo")
    fix6_tris_added += get_tri_count(holo)

    # Frame for each back holo panel
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(hx, back_holo_y + 0.01, hz)
    )
    frame = bpy.context.active_object
    frame.name = f"holo_panel_back_{hp_idx}_frame"
    frame.scale = (holo_panel_width + 0.04, 0.01, holo_panel_height + 0.04)
    apply_transforms(frame)
    assign_mat(frame, "detail")
    fix6_tris_added += get_tri_count(frame)

# 6c: Additional side holo panels (2-3 per side)
side_holo_additions = [
    # (side, x_pos, y_pos, floor_index)
    ("left", -(floor_width_base / 2) - 0.02, -0.4, 5.0),
    ("left", -(floor_width_base / 2) - 0.02, 0.5, 8.0),
    ("left", -(floor_width_base / 2) - 0.02, -0.1, 10.0),
    ("right", (floor_width_base / 2) + 0.02, 0.3, 6.0),
    ("right", (floor_width_base / 2) + 0.02, -0.5, 9.0),
    ("right", (floor_width_base / 2) + 0.02, 0.0, 7.0),
]

for sh_idx, (side, sx, sy, floor_i) in enumerate(side_holo_additions):
    hz = UPPER_START + (floor_i * floor_spacing) + floor_spacing / 2

    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(sx, sy, hz)
    )
    holo = bpy.context.active_object
    holo.name = f"holo_panel_{side}_extra_{sh_idx}"
    holo.scale = (1, holo_panel_width * 0.8, holo_panel_height * 0.8)
    holo.rotation_euler = (0, 0, math.radians(90) if side == "left" else math.radians(-90))
    apply_transforms(holo)
    assign_mat(holo, "holo")
    fix6_tris_added += get_tri_count(holo)

tris_added += fix6_tris_added
print(f"  Fix 6 added: {fix6_tris_added} tris (back markers + holo panels)")


# =====================================================
# PHASE 3: POLISH
# =====================================================
print("\n=== Phase 3: Polish ===")

# Apply all transforms (mesh objects only -- lights cannot have all transforms applied)
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')

# Recalculate normals on all mesh objects
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
print(f"\n  Total mesh objects: {len(final_mesh_objects)}")
print(f"  Total tris removed: {tris_removed}")
print(f"  Total tris added: {tris_added}")
print(f"  Net tris change: +{tris_added - tris_removed}")
print(f"  Final total tris: {final_tris}")
print(f"  Target range: 5,000-8,000")
print(f"  Budget check: {'PASS' if 5000 <= final_tris <= 8000 else 'REVIEW' if final_tris <= 15000 else 'OVER'}")

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
# PHASE 4: GLB EXPORT
# =====================================================
print("\n=== Phase 4: GLB Export ===")

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


# =====================================================
# PHASE 5: SCREENSHOTS
# =====================================================
print("\n=== Phase 5: Rendering Screenshots ===")

# Re-add camera
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

# World background (ink-blue)
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
    filepath = os.path.join(SCREENSHOTS_DIR, f"session18-fix1-{name}.png")
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {filepath}")


# Front elevation
set_camera_and_render(cam_obj, (0, -18, 6), "front-elevation")

# 3/4 angle
set_camera_and_render(cam_obj, (12, -14, 8), "three-quarter")

# Distance view
set_camera_and_render(cam_obj, (20, -20, 12), "distance-view")


# =====================================================
# PHASE 6: SAVE BLEND
# =====================================================
print("\n=== Phase 6: Saving blend file ===")

# Remove cameras/lights again before saving (clean file)
cameras_lights = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in cameras_lights:
    bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print(f"  Saved: {BLEND_OUT}")


# =====================================================
# FINAL REPORT
# =====================================================
print("\n" + "=" * 60)
print("SESSION 18 FIX 1 -- GEOMETRY ADDITION COMPLETE")
print("=" * 60)
print(f"  Initial tris: {initial_tris}")
print(f"  Final tris: {final_tris}")
print(f"  Net change: +{final_tris - initial_tris}")
print(f"  Total objects: {len(final_mesh_objects)}")
print(f"  GLB size: {file_size_kb:.0f} KB")
print(f"  Target: 5,000-8,000 tris")
print(f"  Blend: {BLEND_OUT}")
print(f"  GLB: {GLB_OUT}")
print("=" * 60)

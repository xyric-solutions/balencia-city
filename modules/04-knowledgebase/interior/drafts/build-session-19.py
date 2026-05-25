"""
Balencia City v3 -- Module #04 Knowledgebase
Session 19: Interior -- Knowledge Archive

A vast vertical atrium with floating memory cubes, holographic book walls,
a central neural learning network knowledge graph, knowledge trees,
research chamber alcoves, reading platforms, and a cascading waterfall terminus.

District Color: Royal Purple #7F24FF
Budget: 6K-12K tris
Energy: Yes | Holo: Yes
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
SHARED_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared"
BLEND_FILE = os.path.join(DRAFTS_DIR, "knowledgebase-int-draft-19.blend")
GLB_FILE = os.path.join(DRAFTS_DIR, "knowledgebase-int-draft-19.glb")

# Seed for reproducibility
random.seed(42)


# =====================================================
# PHASE 1: CLEAR SCENE
# =====================================================
print("=== Phase 1: Clearing scene ===")
bpy.ops.wm.read_factory_settings(use_empty=True)


# =====================================================
# PHASE 2: LIGHTING RIG
# =====================================================
print("=== Phase 2: Setting up lighting rig ===")

lighting_script = os.path.join(SHARED_DIR, "lighting-rig.py")
with open(lighting_script, 'r') as f:
    exec(f.read())

light_count = sum(1 for obj in bpy.data.objects if obj.type == 'LIGHT')
cam_count = sum(1 for obj in bpy.data.objects if obj.type == 'CAMERA')
print(f"  Lights: {light_count}, Cameras: {cam_count}")

world = bpy.context.scene.world
bg = world.node_tree.nodes.get("Background")
bg_color = tuple(bg.inputs["Color"].default_value[:3])
print(f"  World background: {bg_color}")


# =====================================================
# PHASE 3: MATERIAL LIBRARY
# =====================================================
print("=== Phase 3: Creating material library ===")

mat_script = os.path.join(SHARED_DIR, "material-library.py")
with open(mat_script, 'r') as f:
    mat_code = f.read()
exec(mat_code)

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


def create_empty(name, location, display_size=0.3):
    """Create a plain axes empty at the given location."""
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    empty = bpy.context.active_object
    empty.name = name
    empty.empty_display_size = display_size
    return empty


# =====================================================
# ROOM DIMENSIONS
# =====================================================
# Interior fits within exterior shell (4.0 x 3.5 x 9.8u)
# Walls take ~0.15u each side, so interior space is ~3.7 x 3.2
# Atrium spans most of the building height

ROOM_W = 3.6      # X dimension (interior clear span)
ROOM_D = 3.2      # Y dimension (interior clear span)
ROOM_H = 9.0      # Z dimension (atrium height, floor to ceiling)
WALL_THICK = 0.12  # Wall thickness


# =====================================================
# PHASE 4: BUILD ROOM SHELL
# =====================================================
print("=== Phase 4: Building room shell ===")

# --- 4.1: Floor ---
print("  Floor...")
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "room_floor"
floor.scale = (ROOM_W, ROOM_D, 1)
apply_transforms(floor)
assign_mat(floor, "base")

# --- 4.2: Ceiling ---
print("  Ceiling...")
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, ROOM_H))
ceiling = bpy.context.active_object
ceiling.name = "room_ceiling"
ceiling.scale = (ROOM_W, ROOM_D, 1)
# Flip normal downward
ceiling.rotation_euler = (math.radians(180), 0, 0)
apply_transforms(ceiling)
assign_mat(ceiling, "base")

# --- 4.3: Back wall (Y+) ---
print("  Back wall...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, ROOM_D / 2, ROOM_H / 2))
back_wall = bpy.context.active_object
back_wall.name = "room_wall_back"
back_wall.scale = (ROOM_W, WALL_THICK, ROOM_H)
apply_transforms(back_wall)
assign_mat(back_wall, "base")

# --- 4.4: Left wall (X-) ---
print("  Left wall...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ROOM_W / 2, 0, ROOM_H / 2))
left_wall = bpy.context.active_object
left_wall.name = "room_wall_left"
left_wall.scale = (WALL_THICK, ROOM_D, ROOM_H)
apply_transforms(left_wall)
assign_mat(left_wall, "base")

# --- 4.5: Right wall (X+) ---
print("  Right wall...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(ROOM_W / 2, 0, ROOM_H / 2))
right_wall = bpy.context.active_object
right_wall.name = "room_wall_right"
right_wall.scale = (WALL_THICK, ROOM_D, ROOM_H)
apply_transforms(right_wall)
assign_mat(right_wall, "base")

# --- 4.6: Front wall (Y-) -- WINDOWED (open wall) ---
# The front wall has an arch entrance opening at the bottom (archive vault)
# and large window panels in the upper section. We model the solid portions.
print("  Front wall (windowed)...")

# Front wall: lower solid band at vault entrance sides
# Left pillar of front wall
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ROOM_W / 2 + 0.3, -ROOM_D / 2, ROOM_H * 0.2))
fw_left = bpy.context.active_object
fw_left.name = "front_wall_left_pillar"
fw_left.scale = (0.6, WALL_THICK, ROOM_H * 0.4)
apply_transforms(fw_left)
assign_mat(fw_left, "base")

# Right pillar of front wall
bpy.ops.mesh.primitive_cube_add(size=1, location=(ROOM_W / 2 - 0.3, -ROOM_D / 2, ROOM_H * 0.2))
fw_right = bpy.context.active_object
fw_right.name = "front_wall_right_pillar"
fw_right.scale = (0.6, WALL_THICK, ROOM_H * 0.4)
apply_transforms(fw_right)
assign_mat(fw_right, "base")

# Upper front wall -- glass panel (large window overlooking city)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -ROOM_D / 2, ROOM_H * 0.7))
fw_upper = bpy.context.active_object
fw_upper.name = "front_wall_glass"
fw_upper.scale = (ROOM_W * 0.8, WALL_THICK * 0.5, ROOM_H * 0.55)
apply_transforms(fw_upper)
assign_mat(fw_upper, "glass")

# Lintel above entrance
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -ROOM_D / 2, ROOM_H * 0.4))
lintel = bpy.context.active_object
lintel.name = "front_wall_lintel"
lintel.scale = (ROOM_W, WALL_THICK, 0.15)
apply_transforms(lintel)
assign_mat(lintel, "accent")

print("  Room shell complete.")


# =====================================================
# PHASE 5: STONE COLUMNS (base structural detail)
# =====================================================
print("=== Phase 5: Stone columns ===")

# 4 columns at lower level corners, reaching partway up
COLUMN_RADIUS = 0.15
COLUMN_HEIGHT = ROOM_H * 0.35  # Lower third of atrium
COLUMN_SEGMENTS = 8  # Low poly

column_positions = [
    (-ROOM_W / 2 + 0.5, -ROOM_D / 2 + 0.5),
    (ROOM_W / 2 - 0.5, -ROOM_D / 2 + 0.5),
    (-ROOM_W / 2 + 0.5, ROOM_D / 2 - 0.5),
    (ROOM_W / 2 - 0.5, ROOM_D / 2 - 0.5),
]

for i, (cx, cy) in enumerate(column_positions):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=COLUMN_RADIUS,
        depth=COLUMN_HEIGHT,
        vertices=COLUMN_SEGMENTS,
        location=(cx, cy, COLUMN_HEIGHT / 2)
    )
    col = bpy.context.active_object
    col.name = f"stone_column_{i:02d}"
    apply_transforms(col)
    assign_mat(col, "base")

    # Simple capital (wider top)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=COLUMN_RADIUS * 1.5,
        depth=0.1,
        vertices=COLUMN_SEGMENTS,
        location=(cx, cy, COLUMN_HEIGHT)
    )
    cap = bpy.context.active_object
    cap.name = f"column_capital_{i:02d}"
    apply_transforms(cap)
    assign_mat(cap, "detail")

print(f"  Built {len(column_positions)} columns with capitals.")


# =====================================================
# PHASE 6: FOCAL ELEMENT -- Neural Learning Network
# =====================================================
print("=== Phase 6: Building focal element -- Neural Knowledge Graph ===")

# The knowledge graph: central hub sphere with orbiting nodes connected by edges.
# ~6m (6u) diameter conceptually, but we scale to fit room (~2.5u radius spread).
# This gets ~25-30% of tri budget.

GRAPH_CENTER = (0, 0, ROOM_H * 0.4)  # 40% height
GRAPH_RADIUS = 1.4  # Spread radius

# Central hub node (largest sphere)
bpy.ops.mesh.primitive_ico_sphere_add(
    radius=0.35,
    subdivisions=2,
    location=GRAPH_CENTER
)
hub = bpy.context.active_object
hub.name = "graph_hub_node"
assign_mat(hub, "emissive")

# Orbiting knowledge nodes (12 nodes at various positions)
NODE_COUNT = 12
node_positions = []
for i in range(NODE_COUNT):
    # Distribute in a rough sphere around center
    theta = (i / NODE_COUNT) * math.pi * 2
    phi = math.pi * 0.3 + (i % 3) * math.pi * 0.2  # Vary elevation
    r = GRAPH_RADIUS * (0.6 + random.random() * 0.4)

    nx = GRAPH_CENTER[0] + r * math.sin(phi) * math.cos(theta)
    ny = GRAPH_CENTER[1] + r * math.sin(phi) * math.sin(theta)
    nz = GRAPH_CENTER[2] + r * math.cos(phi) * (0.5 + random.random() * 0.5)

    node_size = 0.08 + random.random() * 0.12

    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=node_size,
        subdivisions=1,
        location=(nx, ny, nz)
    )
    node = bpy.context.active_object
    node.name = f"graph_node_{i:02d}"
    assign_mat(node, "emissive")
    node_positions.append((nx, ny, nz))

# Connections (edges) between hub and each node -- thin cylinders
print("  Building graph connections...")
from mathutils import Vector

for i, (nx, ny, nz) in enumerate(node_positions):
    start = Vector(GRAPH_CENTER)
    end = Vector((nx, ny, nz))
    mid = (start + end) / 2
    diff = end - start
    length = diff.length

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.015,
        depth=length,
        vertices=4,
        location=mid
    )
    edge = bpy.context.active_object
    edge.name = f"graph_edge_{i:02d}"

    # Align cylinder to direction
    direction = diff.normalized()
    up = Vector((0, 0, 1))
    if abs(direction.dot(up)) > 0.999:
        up = Vector((1, 0, 0))
    rot_quat = direction.to_track_quat('Z', 'Y')
    edge.rotation_euler = rot_quat.to_euler()
    apply_transforms(edge)
    assign_mat(edge, "emissive")

# Secondary connections between neighboring nodes (6 cross-links)
print("  Building cross-connections...")
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
        vertices=4,
        location=mid
    )
    xedge = bpy.context.active_object
    xedge.name = f"graph_cross_{pair_i:02d}"
    direction = diff.normalized()
    rot_quat = direction.to_track_quat('Z', 'Y')
    xedge.rotation_euler = rot_quat.to_euler()
    apply_transforms(xedge)
    assign_mat(xedge, "emissive")

# Outer ring -- a torus encircling the graph
bpy.ops.mesh.primitive_torus_add(
    major_radius=GRAPH_RADIUS * 0.85,
    minor_radius=0.02,
    major_segments=16,
    minor_segments=4,
    location=GRAPH_CENTER,
    rotation=(math.radians(15), math.radians(10), 0)
)
ring = bpy.context.active_object
ring.name = "graph_ring_outer"
apply_transforms(ring)
assign_mat(ring, "emissive")

# Second ring at different angle
bpy.ops.mesh.primitive_torus_add(
    major_radius=GRAPH_RADIUS * 0.7,
    minor_radius=0.015,
    major_segments=16,
    minor_segments=4,
    location=GRAPH_CENTER,
    rotation=(math.radians(75), math.radians(30), math.radians(45))
)
ring2 = bpy.context.active_object
ring2.name = "graph_ring_inner"
apply_transforms(ring2)
assign_mat(ring2, "accent")

print(f"  Focal element complete: hub + {NODE_COUNT} nodes + edges + rings.")


# =====================================================
# PHASE 7: PROPS
# =====================================================
print("=== Phase 7: Building props ===")

# --- 7.1: Floating Memory Cubes ---
print("  7.1: Memory cubes...")
# Scatter small cubes throughout the atrium volume, avoiding the center
# where the knowledge graph is. Use holo material.
CUBE_COUNT = 40  # Keep low for tri budget; each cube = 12 tris
for i in range(CUBE_COUNT):
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
    mc.name = f"memory_cube_{i:02d}"
    mc.rotation_euler = (
        random.random() * math.pi * 0.3,
        random.random() * math.pi * 0.3,
        random.random() * math.pi * 2
    )
    apply_transforms(mc)
    assign_mat(mc, "holo")

print(f"    {CUBE_COUNT} memory cubes placed.")

# --- 7.2: Holographic Book Walls ---
print("  7.2: Book walls...")
# 4 tall flat panels along the side and back walls with book-spine patterns
# (geometric grooves via thin boxes stacked vertically)

book_wall_configs = [
    # (name, pos, scale, normal_axis)
    ("book_wall_back_left", (-ROOM_W / 4 - 0.2, ROOM_D / 2 - 0.2, ROOM_H * 0.4), (ROOM_W * 0.3, 0.08, ROOM_H * 0.65)),
    ("book_wall_back_right", (ROOM_W / 4 + 0.2, ROOM_D / 2 - 0.2, ROOM_H * 0.4), (ROOM_W * 0.3, 0.08, ROOM_H * 0.65)),
    ("book_wall_left", (-ROOM_W / 2 + 0.2, 0, ROOM_H * 0.45), (0.08, ROOM_D * 0.4, ROOM_H * 0.7)),
    ("book_wall_right", (ROOM_W / 2 - 0.2, 0, ROOM_H * 0.45), (0.08, ROOM_D * 0.4, ROOM_H * 0.7)),
]

for bw_name, bw_pos, bw_scale in book_wall_configs:
    bpy.ops.mesh.primitive_cube_add(size=1, location=bw_pos)
    bw = bpy.context.active_object
    bw.name = bw_name
    bw.scale = bw_scale
    apply_transforms(bw)
    assign_mat(bw, "detail")

    # Add 5-7 horizontal groove lines on each book wall to suggest spines
    groove_count = random.randint(5, 7)
    for gi in range(groove_count):
        gz_offset = (gi / groove_count - 0.5) * bw_scale[2] * 0.8
        # Determine groove orientation based on wall
        if abs(bw_scale[0]) < 0.2:  # Side wall (thin in X)
            groove_pos = (bw_pos[0], bw_pos[1], bw_pos[2] + gz_offset)
            groove_scale = (0.01, bw_scale[1] * 0.95, 0.015)
        else:  # Back wall (thin in Y)
            groove_pos = (bw_pos[0], bw_pos[1], bw_pos[2] + gz_offset)
            groove_scale = (bw_scale[0] * 0.95, 0.01, 0.015)

        bpy.ops.mesh.primitive_cube_add(size=1, location=groove_pos)
        groove = bpy.context.active_object
        groove.name = f"{bw_name}_groove_{gi:02d}"
        groove.scale = groove_scale
        apply_transforms(groove)
        assign_mat(groove, "accent")

print(f"    {len(book_wall_configs)} book walls with grooves.")

# --- 7.3: Knowledge Trees ---
print("  7.3: Knowledge trees...")
# 2 vertical branching structures from lower floors
# Trunk (cylinder) + 3-4 branches (tilted cylinders) + leaf clusters (ico spheres)

tree_configs = [
    ("knowledge_tree_01", (-ROOM_W / 2 + 0.7, ROOM_D / 2 - 0.7, 0)),
    ("knowledge_tree_02", (ROOM_W / 2 - 0.7, -ROOM_D / 2 + 0.7, 0)),
]

for tree_name, tree_base in tree_configs:
    trunk_height = ROOM_H * 0.5
    # Trunk
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=trunk_height,
        vertices=6,
        location=(tree_base[0], tree_base[1], trunk_height / 2)
    )
    trunk = bpy.context.active_object
    trunk.name = f"{tree_name}_trunk"
    apply_transforms(trunk)
    assign_mat(trunk, "detail")

    # Branches (3 per tree)
    for bi in range(3):
        branch_z = trunk_height * (0.4 + bi * 0.2)
        branch_angle = (bi * 120 + random.randint(-15, 15)) % 360
        branch_len = 0.5 + random.random() * 0.3
        tilt = math.radians(30 + random.random() * 20)

        bx = tree_base[0] + branch_len * 0.5 * math.cos(math.radians(branch_angle))
        by = tree_base[1] + branch_len * 0.5 * math.sin(math.radians(branch_angle))
        bz = branch_z + branch_len * 0.3

        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.03,
            depth=branch_len,
            vertices=4,
            location=(bx, by, bz)
        )
        branch = bpy.context.active_object
        branch.name = f"{tree_name}_branch_{bi:02d}"
        branch.rotation_euler = (tilt, 0, math.radians(branch_angle))
        apply_transforms(branch)
        assign_mat(branch, "emissive")

        # Leaf cluster at branch tip
        leaf_pos = (
            tree_base[0] + branch_len * math.cos(math.radians(branch_angle)) * math.cos(tilt),
            tree_base[1] + branch_len * math.sin(math.radians(branch_angle)) * math.cos(tilt),
            bz + branch_len * 0.4
        )
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=0.1 + random.random() * 0.05,
            subdivisions=1,
            location=leaf_pos
        )
        leaf = bpy.context.active_object
        leaf.name = f"{tree_name}_leaf_{bi:02d}"
        apply_transforms(leaf)
        assign_mat(leaf, "emissive")

print(f"    {len(tree_configs)} knowledge trees built.")

# --- 7.4: Research Chamber Alcoves ---
print("  7.4: Research chamber alcoves...")
# 3 wall-recessed spaces at different levels with desk forms
# Positioned on back wall and side walls

alcove_configs = [
    ("research_alcove_01", (ROOM_W / 2 - 0.15, -0.3, ROOM_H * 0.15), "right"),
    ("research_alcove_02", (-ROOM_W / 2 + 0.15, 0.3, ROOM_H * 0.35), "left"),
    ("research_alcove_03", (0, ROOM_D / 2 - 0.15, ROOM_H * 0.55), "back"),
]

for alc_name, alc_pos, alc_side in alcove_configs:
    # Alcove shell (recessed box in wall)
    if alc_side in ("left", "right"):
        alc_scale = (0.25, 0.5, 0.4)
    else:
        alc_scale = (0.6, 0.25, 0.4)

    bpy.ops.mesh.primitive_cube_add(size=1, location=alc_pos)
    alcove = bpy.context.active_object
    alcove.name = alc_name
    alcove.scale = alc_scale
    apply_transforms(alcove)
    assign_mat(alcove, "base")

    # Desk inside alcove
    desk_z = alc_pos[2] - alc_scale[2] * 0.3
    bpy.ops.mesh.primitive_cube_add(size=1, location=(alc_pos[0], alc_pos[1], desk_z))
    desk = bpy.context.active_object
    desk.name = f"{alc_name}_desk"
    desk.scale = (alc_scale[0] * 0.7, alc_scale[1] * 0.6, 0.03)
    apply_transforms(desk)
    assign_mat(desk, "detail")

print(f"    {len(alcove_configs)} research alcoves with desks.")

# --- 7.5: Holographic Data Clouds in Research Chambers ---
print("  7.5: Data clouds...")
for i, (alc_name, alc_pos, _) in enumerate(alcove_configs):
    # Small cluster of tiny spheres above each desk
    for si in range(4):
        sx = alc_pos[0] + random.uniform(-0.15, 0.15)
        sy = alc_pos[1] + random.uniform(-0.15, 0.15)
        sz = alc_pos[2] + 0.15 + random.random() * 0.2

        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=0.03 + random.random() * 0.02,
            subdivisions=1,
            location=(sx, sy, sz)
        )
        cloud = bpy.context.active_object
        cloud.name = f"data_cloud_{i:02d}_{si:02d}"
        apply_transforms(cloud)
        assign_mat(cloud, "holo")

print("    Data clouds placed in all 3 alcoves.")

# --- 7.6: Reading Platforms ---
print("  7.6: Reading platforms...")
# 2 circular raised platforms at floor level with low seating

platform_configs = [
    ("reading_platform_01", (-0.9, -0.7, 0)),
    ("reading_platform_02", (0.9, 0.5, 0)),
]

for plat_name, plat_pos in platform_configs:
    # Raised circular platform
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.45,
        depth=0.08,
        vertices=12,
        location=(plat_pos[0], plat_pos[1], 0.04)
    )
    plat = bpy.context.active_object
    plat.name = plat_name
    apply_transforms(plat)
    assign_mat(plat, "base")

    # Low seating (2 small cubes on platform)
    for si in range(2):
        seat_angle = si * math.pi + random.random() * 0.5
        seat_x = plat_pos[0] + 0.2 * math.cos(seat_angle)
        seat_y = plat_pos[1] + 0.2 * math.sin(seat_angle)

        bpy.ops.mesh.primitive_cube_add(
            size=0.15,
            location=(seat_x, seat_y, 0.15)
        )
        seat = bpy.context.active_object
        seat.name = f"{plat_name}_seat_{si:02d}"
        apply_transforms(seat)
        assign_mat(seat, "detail")

print(f"    {len(platform_configs)} reading platforms with seating.")

# --- 7.7: Cascading Waterfall Terminus ---
print("  7.7: Waterfall terminus...")
# Where the exterior energy waterfall enters the interior at the front wall
# Vertical stream of energy flowing from ceiling down near front wall center

# Waterfall stream (vertical flat plane with energy material)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, -ROOM_D / 2 + 0.25, ROOM_H * 0.5)
)
waterfall = bpy.context.active_object
waterfall.name = "waterfall_terminus"
waterfall.scale = (0.15, 0.04, ROOM_H * 0.48)
apply_transforms(waterfall)
assign_mat(waterfall, "energy")

# Pool at base of waterfall
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.3,
    depth=0.06,
    vertices=10,
    location=(0, -ROOM_D / 2 + 0.3, 0.03)
)
pool = bpy.context.active_object
pool.name = "waterfall_pool"
apply_transforms(pool)
assign_mat(pool, "energy")

# Splash droplets (small cubes above pool)
for di in range(5):
    dx = random.uniform(-0.2, 0.2)
    dy = random.uniform(-0.15, 0.15)
    dz = 0.1 + random.random() * 0.25

    bpy.ops.mesh.primitive_cube_add(
        size=0.025 + random.random() * 0.015,
        location=(dx, -ROOM_D / 2 + 0.3 + dy, dz)
    )
    drop = bpy.context.active_object
    drop.name = f"waterfall_droplet_{di:02d}"
    drop.rotation_euler = (
        random.random() * 0.5,
        random.random() * 0.5,
        random.random() * math.pi
    )
    apply_transforms(drop)
    assign_mat(drop, "energy")

print("    Waterfall terminus with pool and droplets.")

print("=== Phase 7 complete: All props built ===")


# =====================================================
# PHASE 8: PLACE EMPTIES
# =====================================================
print("=== Phase 8: Placing empties ===")

# light_0: Atrium center at knowledge graph height -- purple key light
light_0 = create_empty("light_0", (0, 0, ROOM_H * 0.42))
print(f"  light_0 at {tuple(light_0.location)}")

# light_1: Upper atrium near crown -- cool fill light
light_1 = create_empty("light_1", (0, 0, ROOM_H * 0.85))
print(f"  light_1 at {tuple(light_1.location)}")

# light_2: Lower atrium near archive entrance -- warm accent
light_2 = create_empty("light_2", (0, -ROOM_D / 2 + 0.5, ROOM_H * 0.1))
print(f"  light_2 at {tuple(light_2.location)}")

# camera_target: Center of knowledge graph at ~40% height
cam_target = create_empty("camera_target", (0, 0, ROOM_H * 0.4), display_size=0.5)
print(f"  camera_target at {tuple(cam_target.location)}")

print("  All 4 empties placed.")


# =====================================================
# PHASE 9: MATERIAL AUDIT
# =====================================================
print("=== Phase 9: Material audit ===")

valid_mat_names = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
issues = []

for obj in mesh_objects:
    if not obj.data.materials:
        issues.append(f"  NO MATERIAL: {obj.name}")
    else:
        for mat in obj.data.materials:
            if mat.name not in valid_mat_names:
                issues.append(f"  INVALID MATERIAL: {obj.name} has '{mat.name}'")

if issues:
    print("  MATERIAL ISSUES FOUND:")
    for issue in issues:
        print(issue)
else:
    print("  All objects have valid 7-slot materials.")


# =====================================================
# PHASE 10: TRI COUNT AUDIT (PRE-DECIMATION)
# =====================================================
print("=== Phase 10: Tri count audit ===")

total_tris = 0
object_tris = []

for obj in mesh_objects:
    tc = get_tri_count(obj)
    total_tris += tc
    object_tris.append((obj.name, tc))

object_tris.sort(key=lambda x: x[1], reverse=True)

print(f"  Total tris: {total_tris}")
print(f"  Budget: 6K-12K")
print(f"  Top 15 objects by tri count:")
for name, tc in object_tris[:15]:
    print(f"    {name}: {tc}")


# =====================================================
# PHASE 11: DECIMATION (if needed)
# =====================================================
print("=== Phase 11: Decimation ===")

TARGET_MAX = 11000  # Stay under 12K with margin

if total_tris > TARGET_MAX:
    print(f"  Over budget ({total_tris} > {TARGET_MAX}). Decimating...")
    # Decimate the largest objects (but protect focal element less)
    # Sort by tri count descending
    for obj_name, tc in object_tris:
        if total_tris <= TARGET_MAX:
            break
        if tc < 50:
            continue  # Skip tiny objects

        obj = bpy.data.objects.get(obj_name)
        if not obj or obj.type != 'MESH':
            continue

        # Focal element gets gentler decimation
        is_focal = "graph_" in obj_name
        ratio = 0.7 if is_focal else 0.5

        # Only decimate if this object is significantly contributing
        if tc > 100:
            mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
            mod.ratio = ratio
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.modifier_apply(modifier="Decimate")
            obj.select_set(False)

            new_tc = get_tri_count(obj)
            saved = tc - new_tc
            total_tris -= saved
            print(f"    {obj_name}: {tc} -> {new_tc} (saved {saved})")

    print(f"  Post-decimation total: {total_tris}")
else:
    print(f"  Within budget ({total_tris} <= {TARGET_MAX}). No decimation needed.")


# Final tri count
total_tris_final = 0
object_tris_final = []
for obj in [o for o in bpy.data.objects if o.type == 'MESH']:
    tc = get_tri_count(obj)
    total_tris_final += tc
    object_tris_final.append((obj.name, tc))

object_tris_final.sort(key=lambda x: x[1], reverse=True)
print(f"\n  FINAL tri count: {total_tris_final}")
for name, tc in object_tris_final[:10]:
    print(f"    {name}: {tc}")


# =====================================================
# PHASE 12: SAVE BLEND FILE
# =====================================================
print(f"=== Phase 12: Saving blend file ===")
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
print(f"  Saved: {BLEND_FILE}")


# =====================================================
# PHASE 13: EXPORT GLB
# =====================================================
print(f"=== Phase 13: Exporting GLB ===")

# Select all mesh objects and empties for export
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type in ('MESH', 'EMPTY'):
        obj.select_set(True)
    elif obj.type in ('LIGHT', 'CAMERA'):
        obj.select_set(False)

# Blender 5.x changed some export parameter names
export_kwargs = {
    'filepath': GLB_FILE,
    'export_format': 'GLB',
    'use_selection': True,
    'export_draco_mesh_compression_enable': True,
    'export_draco_mesh_compression_level': 6,
    'export_yup': True,
    'export_cameras': False,
    'export_lights': False,
    'export_extras': True,
}
# Try both old and new parameter names for apply_modifiers
try:
    bpy.ops.export_scene.gltf(**export_kwargs, export_apply_modifiers=True)
except TypeError:
    try:
        bpy.ops.export_scene.gltf(**export_kwargs)
    except Exception as e:
        print(f"  Export fallback error: {e}")
        # Minimal export
        bpy.ops.export_scene.gltf(
            filepath=GLB_FILE,
            export_format='GLB',
            use_selection=True,
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=6,
        )

# Verify file size
file_size = os.path.getsize(GLB_FILE)
print(f"  Exported: {GLB_FILE}")
print(f"  File size: {file_size / 1024:.1f} KB")


# =====================================================
# PHASE 14: FINAL SUMMARY
# =====================================================
print("\n" + "=" * 60)
print("SESSION 19 SUMMARY -- Knowledgebase Interior")
print("=" * 60)

# Count empties
empties = [o for o in bpy.data.objects if o.type == 'EMPTY']
empty_names = [e.name for e in empties]
print(f"\nEmpties ({len(empties)}):")
for e in empties:
    print(f"  {e.name}: {tuple(round(c, 2) for c in e.location)}")

# Validate required empties
required_empties = ["light_0", "light_1", "light_2", "camera_target"]
for req in required_empties:
    status = "FOUND" if req in empty_names else "MISSING"
    print(f"  {req}: {status}")

# Material usage summary
mat_usage = {}
for obj in [o for o in bpy.data.objects if o.type == 'MESH']:
    for mat in obj.data.materials:
        mat_usage[mat.name] = mat_usage.get(mat.name, 0) + 1

print(f"\nMaterial usage:")
for mat_name, count in sorted(mat_usage.items()):
    print(f"  {mat_name}: {count} objects")

print(f"\nFinal tri count: {total_tris_final}")
print(f"GLB size: {file_size / 1024:.1f} KB")
print(f"Blend file: {BLEND_FILE}")
print(f"GLB file: {GLB_FILE}")

# Checklist
print("\n--- END CRITERIA CHECKLIST ---")
print("[x] Room shell complete")
print("[x] Focal element built")
prop_count = len([o for o in bpy.data.objects if o.type == 'MESH' and any(
    p in o.name for p in ['memory_cube', 'book_wall', 'knowledge_tree',
                          'research_alcove', 'data_cloud', 'reading_platform', 'waterfall']
)])
empties_ok = all(r in empty_names for r in required_empties)
tris_ok = total_tris_final <= 12000
size_ok = file_size <= 300 * 1024
print(f"[{'x' if prop_count >= 4 else ' '}] 4-8 props placed ({prop_count} prop objects)")
print(f"[{'x' if empties_ok else ' '}] All empties placed")
print(f"[{'x' if not issues else ' '}] All materials from 7-slot set")
print(f"[{'x' if tris_ok else ' '}] Within 6K-12K tri budget ({total_tris_final})")
print(f"[{'x' if size_ok else ' '}] GLB under 300 KB ({file_size / 1024:.1f} KB)")

print("\n=== Session 19 build script complete ===")

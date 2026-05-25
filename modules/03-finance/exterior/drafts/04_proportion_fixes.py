"""
Finance Tower (Module #03) — Proportion Fixes
Fix window positioning (must be recessed, not protruding),
entry portal position, and crown panel integration.
"""
import bpy
import math
from mathutils import Vector

# ============================================================
# FIX 1: Recessed Windows
# Windows were positioned at (radius - 0.15) but that puts them
# ON the surface. They need to be deeper inside, and also need
# to face outward properly relative to the faceted body.
# ============================================================

# Delete existing windows and recreate with correct positioning
windows_to_remove = [obj for obj in bpy.data.objects if obj.name.startswith("window_c")]
for obj in windows_to_remove:
    bpy.data.objects.remove(obj, do_unlink=True)

mat_glass = bpy.data.materials.get("glass")

total_height = 14.0
base_radius = 4.0
sides = 8
z_offset = 1.0

# Same section data for radius interpolation
sections = [
    (0.00, 1.00, 0),
    (0.05, 1.02, 0),
    (0.12, 0.95, 3),
    (0.28, 0.88, -2),
    (0.45, 0.82, 4),
    (0.62, 0.76, -3),
    (0.80, 0.72, 2),
    (0.92, 0.70, -1),
    (1.00, 0.68, 0),
]

def get_radius_at_height(h_frac):
    """Interpolate radius at a given height fraction."""
    for i in range(len(sections) - 1):
        if sections[i][0] <= h_frac <= sections[i+1][0]:
            t = (h_frac - sections[i][0]) / (sections[i+1][0] - sections[i][0])
            r = sections[i][1] + t * (sections[i+1][1] - sections[i][1])
            return base_radius * r
    return base_radius * sections[-1][1]

# Floor clusters (3 vertical zones)
clusters = [
    (0.10, 0.35),   # lower third
    (0.38, 0.58),   # middle third
    (0.62, 0.85),   # upper third
]

window_objects = []
for cluster_idx, (h_start, h_end) in enumerate(clusters):
    z_start = h_start * total_height + z_offset
    z_end = h_end * total_height + z_offset
    z_mid = (z_start + z_end) / 2
    z_height = z_end - z_start

    h_mid_frac = (h_start + h_end) / 2
    radius = get_radius_at_height(h_mid_frac)

    # Place windows on alternating faces, RECESSED deeply
    for face_idx in range(0, sides, 2):
        angle = 2 * math.pi * face_idx / sides

        # Position window INSIDE the body surface (recessed by 0.3)
        recess_depth = 0.3
        wx = (radius - recess_depth) * math.cos(angle)
        wy = (radius - recess_depth) * math.sin(angle)

        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(wx, wy, z_mid),
            scale=(0.05, 1.0, z_height * 0.75)
        )
        window = bpy.context.active_object
        window.name = f"window_c{cluster_idx}_f{face_idx}"
        window.rotation_euler.z = angle + math.pi/2
        window.data.materials.append(mat_glass)

        for poly in window.data.polygons:
            poly.use_smooth = False

        window_objects.append(window)

print(f"Windows fixed: {len(window_objects)} recessed panels (deeper inside body)")


# ============================================================
# FIX 2: Entry Portal Position
# Move entry to sit flush with the body surface on the -Y face
# The body at ground level has radius ~4.0 on the -Y face
# ============================================================

mat_detail = bpy.data.materials.get("detail")
mat_emissive = bpy.data.materials.get("emissive")

# The -Y face of the octagon at ground level
# For an 8-sided polygon, the face at -Y spans from vertex at -pi/2 - pi/8 to -pi/2 + pi/8
# The face center is at angle = -pi/2, distance = radius * cos(pi/8)
face_angle = -math.pi / 2
face_dist = base_radius * 1.0 * math.cos(math.pi / 8)  # ~3.7

entry_y = -face_dist
entry_z_base = z_offset  # sits at base of main body

# Delete old entry objects
entry_objects = [obj for obj in bpy.data.objects if obj.name.startswith("entry_")]
for obj in entry_objects:
    bpy.data.objects.remove(obj, do_unlink=True)

entry_width = 2.0
entry_height = 2.5
entry_depth = 0.8

# Left pillar
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-entry_width/2 - 0.15, entry_y - 0.1, entry_z_base + entry_height/2),
    scale=(0.3, entry_depth/2, entry_height/2)
)
lp = bpy.context.active_object
lp.name = "entry_pillar_left"
lp.data.materials.append(mat_detail)
for poly in lp.data.polygons:
    poly.use_smooth = False

# Right pillar
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(entry_width/2 + 0.15, entry_y - 0.1, entry_z_base + entry_height/2),
    scale=(0.3, entry_depth/2, entry_height/2)
)
rp = bpy.context.active_object
rp.name = "entry_pillar_right"
rp.data.materials.append(mat_detail)
for poly in rp.data.polygons:
    poly.use_smooth = False

# Lintel
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, entry_y - 0.1, entry_z_base + entry_height + 0.15),
    scale=(entry_width/2 + 0.45, entry_depth/2, 0.25)
)
lintel = bpy.context.active_object
lintel.name = "entry_lintel"
lintel.data.materials.append(mat_detail)
for poly in lintel.data.polygons:
    poly.use_smooth = False

# Gold edge strips
# Left vertical
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-entry_width/2 - 0.15, entry_y - entry_depth/2 - 0.05, entry_z_base + entry_height/2),
    scale=(0.035, 0.035, entry_height/2 + 0.15)
)
el = bpy.context.active_object
el.name = "entry_edge_left"
el.data.materials.append(mat_emissive)

# Right vertical
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(entry_width/2 + 0.15, entry_y - entry_depth/2 - 0.05, entry_z_base + entry_height/2),
    scale=(0.035, 0.035, entry_height/2 + 0.15)
)
er = bpy.context.active_object
er.name = "entry_edge_right"
er.data.materials.append(mat_emissive)

# Top horizontal
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, entry_y - entry_depth/2 - 0.05, entry_z_base + entry_height + 0.4),
    scale=(entry_width/2 + 0.45, 0.035, 0.035)
)
et = bpy.context.active_object
et.name = "entry_edge_top"
et.data.materials.append(mat_emissive)

print(f"Entry portal repositioned: flush with -Y face at y={entry_y:.2f}")


# ============================================================
# FIX 3: Market Display — move to match new entry position
# ============================================================
market = bpy.data.objects.get("market_display")
if market:
    market.location = (1.5, entry_y - 0.15, entry_z_base + 3.2)
    print(f"Market display repositioned to y={entry_y - 0.15:.2f}")


# ============================================================
# FIX 4: Crown panels — tighten them closer to body
# ============================================================
crown_z = 14.0 + z_offset
crown_radius = base_radius * 0.68
panel_count = 8

for i in range(panel_count):
    panel = bpy.data.objects.get(f"crown_panel_{i}")
    if panel:
        angle = 2 * math.pi * i / panel_count
        # Move panels flush against the body surface (was +0.15, now -0.05)
        px = (crown_radius - 0.05) * math.cos(angle)
        py = (crown_radius - 0.05) * math.sin(angle)
        panel.location = (px, py, crown_z - 0.7)
        panel.rotation_euler.z = angle + math.pi/2

print("Crown panels tightened against body surface")


# ============================================================
# Report updated tri count
# ============================================================
print("\n--- UPDATED OBJECT INVENTORY ---")
total_tris = 0
mesh_objects = []
curve_objects = []

for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type == 'MESH':
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh_eval = obj_eval.to_mesh()
        tris = sum(len(poly.vertices) - 2 for poly in mesh_eval.polygons)
        mat_name = obj.data.materials[0].name if obj.data.materials else 'NONE'
        mesh_objects.append((obj.name, tris, mat_name))
        total_tris += tris
        obj_eval.to_mesh_clear()
    elif obj.type == 'CURVE':
        curve_objects.append(obj.name)

for name, tris, mat_name in mesh_objects:
    print(f"  {name}: {tris} tris [{mat_name}]")

print(f"\nMesh objects: {len(mesh_objects)}, Total mesh tris: {total_tris}")
print(f"Curve objects: {len(curve_objects)} (edge wireframe, convert in detail session)")
print(f"Grand total objects: {len(bpy.data.objects)}")
print(f"Budget check: {total_tris} / 10800 = {total_tris/10800*100:.1f}% of 60% target")

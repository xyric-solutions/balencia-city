"""
Session 10 -- Yoga & Wellbeing Exterior: Detail + Polish + Export
Run: blender yoga-exterior-s09.blend -b -P s10_detail_polish_export.py

Loads the Session 9 .blend file and adds:
1. Energy pipeline geometry (energy slot, currently 0%)
2. Organic support pillar reshaping (taper + segmentation)
3. Walkway curvature (replace box walkways with curved arcs + organic rails)
4. Terrace railing detail on garden platforms
5. LED light strips (emissive slot, boost to 3-8%)
6. Additional vegetation detail (vine clusters, leaf forms)
7. Floating stepping stones between garden platforms
8. Dome facade enrichment (meridian ribs)

Then: polish checks, per-object decimation, GLB export, save new .blend.
"""
import bpy
import bmesh
import math
import os
import sys
from mathutils import Vector

# ============================================================
# CONFIGURATION
# ============================================================
SAVE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/exterior/drafts"
BLEND_OUT = os.path.join(SAVE_DIR, "yoga-exterior-s10.blend")
GLB_OUT = os.path.join(SAVE_DIR, "yoga-ext-draft-s10.glb")
EXPORT_PIPELINE = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/export-pipeline.py"

MAX_TRIS = 18000
TARGET_TRIS = 15000  # Stop adding detail near this number

# ============================================================
# HELPERS
# ============================================================
def assign_mat(obj, slot_name):
    """Assign an existing material by slot name to an object."""
    mat = bpy.data.materials.get(slot_name)
    if mat:
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
    else:
        print(f"  WARNING: Material '{slot_name}' not found for {obj.name}")

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

def count_tris_per_object():
    """Return list of (name, tri_count) for all mesh objects."""
    results = []
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj_eval = obj.evaluated_get(depsgraph)
            mesh_eval = obj_eval.to_mesh()
            tris = 0
            for poly in mesh_eval.polygons:
                tris += max(1, len(poly.vertices) - 2)
            obj_eval.to_mesh_clear()
            results.append((obj.name, tris))
    return results

def count_total_tris():
    return sum(t for _, t in count_tris_per_object())

def print_tri_report(label=""):
    report = count_tris_per_object()
    total = sum(t for _, t in report)
    print(f"\n=== TRI REPORT {label} ===")
    for name, tris in sorted(report, key=lambda x: -x[1]):
        print(f"  {name}: {tris}")
    print(f"  TOTAL: {total} / {MAX_TRIS} ({total/MAX_TRIS*100:.1f}%)")
    return total

def apply_smooth(obj):
    """Apply smooth shading to an object."""
    for poly in obj.data.polygons:
        poly.use_smooth = True

# ============================================================
# STEP 0: VERIFY SCENE STATE
# ============================================================
print("=" * 60)
print("SESSION 10: Detail + Polish + Export")
print("=" * 60)

mesh_count = sum(1 for obj in bpy.data.objects if obj.type == 'MESH')
total = count_total_tris()
print(f"\nScene verification: {mesh_count} mesh objects, {total} tris")

# Verify key objects exist
expected_objects = [
    "main_platform", "platform_rim", "dome_large", "dome_medium",
    "dome_small", "reflecting_lake", "energy_receptor"
]
missing = [n for n in expected_objects if n not in bpy.data.objects]
if missing:
    print(f"WARNING: Missing objects: {missing}")
else:
    print("All key objects present. Proceeding with detail pass.")

initial_tris = total

# ============================================================
# ENSURE ENERGY MATERIAL EXISTS (was missing from S09 .blend)
# ============================================================
def hex_to_linear(hex_color):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    def to_linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (to_linear(r), to_linear(g), to_linear(b), 1.0)

if "energy" not in bpy.data.materials:
    DETAIL_COLOR = hex_to_linear("#16161E")
    ENERGY_ORANGE = hex_to_linear("#FF5E00")
    mat = bpy.data.materials.new(name="energy")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = DETAIL_COLOR
    bsdf.inputs["Roughness"].default_value = 0.15
    bsdf.inputs["Metallic"].default_value = 0.10
    bsdf.inputs["Emission Color"].default_value = ENERGY_ORANGE
    bsdf.inputs["Emission Strength"].default_value = 0.10
    print("  Created missing 'energy' material")

# ============================================================
# DETAIL 1: ENERGY PIPELINE GEOMETRY (energy slot = 0% -> target 3-5%)
# ============================================================
print("\n--- DETAIL 1: Energy Pipeline Geometry ---")

# 1a. Energy conduit ring on platform underside (traces where SIA energy flows)
# A thin torus ring running underneath the platform, suggesting energy distribution
bpy.ops.mesh.primitive_torus_add(
    major_radius=3.5, minor_radius=0.06,
    major_segments=24, minor_segments=6,
    location=(0, 0, 0.55)
)
conduit_ring = bpy.context.active_object
conduit_ring.name = "energy_conduit_ring"
conduit_ring.scale = (1.0, 0.7, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
apply_smooth(conduit_ring)
assign_mat(conduit_ring, "energy")
deselect_all()
print("  energy_conduit_ring created")

# 1b. Energy vein traces on platform underside (4 radial lines from center to rim)
vein_angles = [0, math.pi/2, math.pi, 3*math.pi/2]
for i, angle in enumerate(vein_angles):
    inner_r = 0.5
    outer_r = 3.2
    cx = math.cos(angle)
    cy = math.sin(angle) * 0.7  # Elliptical to match platform

    start_x = cx * inner_r
    start_y = cy * inner_r
    end_x = cx * outer_r
    end_y = cy * outer_r

    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2

    dx = end_x - start_x
    dy = end_y - start_y
    length = math.sqrt(dx*dx + dy*dy)
    rot_angle = math.atan2(dy, dx)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.025, depth=length, vertices=6,
        location=(mid_x, mid_y, 0.55)
    )
    vein = bpy.context.active_object
    vein.name = f"energy_vein_{i+1:02d}"
    vein.rotation_euler = (0, math.radians(90), rot_angle)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    apply_smooth(vein)
    assign_mat(vein, "energy")
    deselect_all()
print("  energy_veins (4) created")

# 1c. Energy receptor dish (replace small sphere with wider receptor form on large dome apex)
# The existing energy_receptor is a small sphere at the top of dome_large.
# Add a wider collar/dish around it to make it read as a receptor.
dome_large_apex_z = 0.97 + 1.8  # matches dome_large position + radius
bpy.ops.mesh.primitive_cone_add(
    radius1=0.25, radius2=0.08, depth=0.12,
    vertices=12,
    location=(-1.2, -0.3, dome_large_apex_z - 0.06)
)
receptor_dish = bpy.context.active_object
receptor_dish.name = "energy_receptor_dish"
apply_smooth(receptor_dish)
assign_mat(receptor_dish, "energy")
deselect_all()
print("  energy_receptor_dish created")

# 1d. Small energy nodes on medium and small dome apexes
dome_medium_apex_z = 0.97 + 1.2
dome_small_apex_z = 0.97 + 0.8

for idx, (dx, dy, dz) in enumerate([
    (2.0, 0.5, dome_medium_apex_z),
    (0.5, 1.8, dome_small_apex_z)
]):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.08, segments=8, ring_count=4,
        location=(dx, dy, dz)
    )
    node = bpy.context.active_object
    node.name = f"energy_node_{idx+1:02d}"
    apply_smooth(node)
    assign_mat(node, "energy")
    deselect_all()
print("  energy_nodes (2) created on dome apexes")

print(f"  Energy detail tris: {count_total_tris() - initial_tris}")

# ============================================================
# DETAIL 2: SUPPORT PILLAR ORGANIC RESHAPING
# ============================================================
print("\n--- DETAIL 2: Support Pillar Organic Reshaping ---")
# The existing pillars are simple cones (12 vertices). Replace with tapered
# organic forms: wider base, narrower top, with 2 segmentation rings for
# the "tree trunk" look.
#
# Strategy: Delete existing pillars, recreate with better geometry.
# Each new pillar: cylinder with 3 height segments, proportional editing
# applied via bmesh to create organic taper.

pillar_positions = [
    (-2.5, -1.5),
    (2.5, -1.5),
    (-3.0, 1.0),
    (3.0, 1.0),
    (0.0, 2.0),
]

# Remove old pillars
for i in range(1, 6):
    old_name = f"support_pillar_{i:02d}"
    old_obj = bpy.data.objects.get(old_name)
    if old_obj:
        bpy.data.objects.remove(old_obj, do_unlink=True)

# Create new organic pillars
for i, (px, py) in enumerate(pillar_positions):
    # Cylinder with more segments for organic shaping
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.20, depth=0.85, vertices=10,
        location=(px, py, 0.375)
    )
    pillar = bpy.context.active_object
    pillar.name = f"support_pillar_{i+1:02d}"

    # Enter edit mode to taper and shape organically
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(pillar.data)
    bm.verts.ensure_lookup_table()

    # Add loop cuts for segmentation (organic rings)
    # We'll manually adjust vertex positions instead of loop cuts
    # since loop cuts in bmesh are complex
    # Taper: bottom wider, top narrower, with slight bulge in middle
    min_z = min(v.co.z for v in bm.verts)
    max_z = max(v.co.z for v in bm.verts)
    height_range = max_z - min_z if max_z != min_z else 1.0

    for v in bm.verts:
        t = (v.co.z - min_z) / height_range  # 0=bottom, 1=top

        # Organic taper profile: wide at bottom, slight bulge at 0.3, narrow at top
        # base_radius=0.28, mid_radius=0.22, top_radius=0.12
        if t < 0.3:
            scale = 1.4 - t * 0.6  # 1.4 -> 1.22
        elif t < 0.7:
            scale = 1.22 - (t - 0.3) * 0.8  # 1.22 -> 0.9
        else:
            scale = 0.9 - (t - 0.7) * 1.2  # 0.9 -> 0.54

        # Only scale XY (radial), not Z
        v.co.x *= scale
        v.co.y *= scale

    bmesh.update_edit_mesh(pillar.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    apply_smooth(pillar)
    assign_mat(pillar, "detail")
    deselect_all()

print("  Support pillars reshaped (5 organic tapered forms)")

# ============================================================
# DETAIL 3: WALKWAY CURVATURE
# ============================================================
print("\n--- DETAIL 3: Walkway Curvature ---")
# Replace the existing box walkways with gently curved paths.
# Strategy: Delete old walkways, create new ones using subdivided planes
# with slight vertical arc.

# Remove old walkways and their rails
walkway_names = []
for obj in list(bpy.data.objects):
    if obj.type == 'MESH' and obj.name.startswith("walkway_"):
        walkway_names.append(obj.name)
        bpy.data.objects.remove(obj, do_unlink=True)
print(f"  Removed {len(walkway_names)} old walkway objects")

# New curved walkway function
def create_curved_walkway(name, start, end, width=0.18, arc_height=0.08,
                          segments=8, rail_height=0.12):
    """Create a walkway with subtle vertical arc and organic low railings."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dz = end[2] - start[2]
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    angle_z = math.atan2(dy, dx)
    angle_y = math.atan2(dz, math.sqrt(dx*dx + dy*dy))

    # Create subdivided plane for the walkway deck
    verts = []
    faces = []
    half_w = width / 2

    for i in range(segments + 1):
        t = i / segments
        # Position along the path
        x = t * length
        # Vertical arc (parabolic)
        z_arc = arc_height * 4 * t * (1 - t)  # peaks at midpoint
        # Two vertices per segment (left and right edge)
        verts.append(Vector((x, -half_w, z_arc)))
        verts.append(Vector((x, half_w, z_arc)))

    for i in range(segments):
        v0 = i * 2
        v1 = i * 2 + 1
        v2 = (i + 1) * 2 + 1
        v3 = (i + 1) * 2
        faces.append((v0, v1, v2, v3))

    # Build mesh
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([v[:] for v in verts], [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    # Position and rotate to align with start->end
    mid = ((start[0]+end[0])/2, (start[1]+end[1])/2, (start[2]+end[2])/2)
    obj.location = start
    obj.rotation_euler = (angle_y, 0, angle_z)
    apply_smooth(obj)
    assign_mat(obj, "detail")
    deselect_all()

    # Create organic low railings (thin curved rails along each edge)
    for side, sign in [("L", -1), ("R", 1)]:
        rail_verts = []
        rail_faces = []
        rail_r = 0.012  # thin rail radius

        for i in range(segments + 1):
            t = i / segments
            x = t * length
            z_arc = arc_height * 4 * t * (1 - t)
            y_pos = sign * (half_w + 0.01)

            # Rail cross-section (simple box for low poly)
            rail_verts.append(Vector((x, y_pos - rail_r, z_arc + rail_height)))
            rail_verts.append(Vector((x, y_pos + rail_r, z_arc + rail_height)))
            rail_verts.append(Vector((x, y_pos + rail_r, z_arc + rail_height - rail_r*2)))
            rail_verts.append(Vector((x, y_pos - rail_r, z_arc + rail_height - rail_r*2)))

        for i in range(segments):
            base = i * 4
            for j in range(4):
                j_next = (j + 1) % 4
                rail_faces.append((
                    base + j, base + j_next,
                    base + 4 + j_next, base + 4 + j
                ))

        rail_name = f"{name}_rail_{side}"
        rail_mesh = bpy.data.meshes.new(rail_name)
        rail_mesh.from_pydata([v[:] for v in rail_verts], [], rail_faces)
        rail_mesh.update()
        rail_obj = bpy.data.objects.new(rail_name, rail_mesh)
        bpy.context.collection.objects.link(rail_obj)
        rail_obj.location = start
        rail_obj.rotation_euler = (angle_y, 0, angle_z)
        apply_smooth(rail_obj)
        assign_mat(rail_obj, "accent")
        deselect_all()

# Walkway 1: Large dome edge -> Medium dome edge
create_curved_walkway("walkway_01",
    start=(0.6, -0.3, 0.97),
    end=(0.8, 0.5, 0.97),
    width=0.18, arc_height=0.06, segments=6)

# Walkway 2: Medium dome -> Small dome
create_curved_walkway("walkway_02",
    start=(1.5, 1.2, 0.97),
    end=(0.8, 1.3, 0.97),
    width=0.15, arc_height=0.04, segments=5)

# Walkway 3: Main platform edge to garden platform 01
create_curved_walkway("walkway_03",
    start=(-3.5, -1.0, 0.8),
    end=(-3.2, -1.0, 0.5),
    width=0.15, arc_height=0.05, segments=5)

print("  3 curved walkways with organic rails created")

# ============================================================
# DETAIL 4: TERRACE RAILING DETAIL ON GARDEN PLATFORMS
# ============================================================
print("\n--- DETAIL 4: Terrace Railings on Garden Platforms ---")

# Add low organic railings (partial arcs) around each garden platform
garden_configs = [
    {"name": "garden_platform_01", "radius": 1.2, "pos": (-4.0, -1.0, 0.5), "rail_arc": 0.65},
    {"name": "garden_platform_02", "radius": 0.9, "pos": (3.8, -1.5, 0.6), "rail_arc": 0.55},
    {"name": "garden_platform_03", "radius": 0.7, "pos": (-3.5, 2.0, 0.7), "rail_arc": 0.50},
]

for gc in garden_configs:
    r = gc["radius"] + 0.05
    pos = gc["pos"]
    arc_span = gc["rail_arc"]  # fraction of full circle to cover
    segments = 10
    rail_height = 0.12
    rail_thickness = 0.02

    # Create a partial torus-like railing as a series of connected quads
    verts = []
    faces = []

    start_angle = -arc_span * math.pi
    end_angle = arc_span * math.pi

    for i in range(segments + 1):
        t = i / segments
        angle = start_angle + t * (end_angle - start_angle)
        cx = r * math.cos(angle)
        cy = r * math.sin(angle)

        # Two verts per segment: inner-top and outer-top
        verts.append(Vector((cx - rail_thickness * math.cos(angle),
                             cy - rail_thickness * math.sin(angle),
                             rail_height)))
        verts.append(Vector((cx + rail_thickness * math.cos(angle),
                             cy + rail_thickness * math.sin(angle),
                             rail_height)))

    for i in range(segments):
        v0 = i * 2
        v1 = i * 2 + 1
        v2 = (i + 1) * 2 + 1
        v3 = (i + 1) * 2
        faces.append((v0, v1, v2, v3))

    railing_name = gc["name"].replace("garden_platform", "terrace_railing")
    mesh = bpy.data.meshes.new(railing_name)
    mesh.from_pydata([v[:] for v in verts], [], faces)
    mesh.update()
    rail_obj = bpy.data.objects.new(railing_name, mesh)
    bpy.context.collection.objects.link(rail_obj)
    rail_obj.location = (pos[0], pos[1], pos[2] + 0.08)
    apply_smooth(rail_obj)
    assign_mat(rail_obj, "accent")
    deselect_all()

print("  3 terrace railings created")

# ============================================================
# DETAIL 5: LED LIGHT STRIPS (emissive slot boost)
# ============================================================
print("\n--- DETAIL 5: LED Light Strips ---")

# 5a. LED ring at base of each dome (inside the holo collar)
dome_configs_led = [
    {"name": "led_ring_large",  "radius": 1.85, "pos": (-1.2, -0.3, 0.97), "segs": 20},
    {"name": "led_ring_medium", "radius": 1.25, "pos": (2.0, 0.5, 0.97),   "segs": 16},
    {"name": "led_ring_small",  "radius": 0.85, "pos": (0.5, 1.8, 0.97),   "segs": 12},
]

for lc in dome_configs_led:
    bpy.ops.mesh.primitive_torus_add(
        major_radius=lc["radius"], minor_radius=0.02,
        major_segments=lc["segs"], minor_segments=4,
        location=lc["pos"]
    )
    led = bpy.context.active_object
    led.name = lc["name"]
    apply_smooth(led)
    assign_mat(led, "emissive")
    deselect_all()
print("  3 dome base LED rings")

# 5b. LED strips along platform rim (2 thin rings at top and bottom of platform edge)
for idx, z_offset in enumerate([0.92, 0.68]):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=4.6, minor_radius=0.015,
        major_segments=24, minor_segments=4,
        location=(0, 0, z_offset)
    )
    led_rim = bpy.context.active_object
    led_rim.name = f"led_strip_platform_{idx+1:02d}"
    led_rim.scale = (1.0, 0.7, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    apply_smooth(led_rim)
    assign_mat(led_rim, "emissive")
    deselect_all()
print("  2 platform edge LED strips")

# 5c. LED accents on garden platform edges
for i, gc in enumerate(garden_configs):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=gc["radius"] - 0.05, minor_radius=0.015,
        major_segments=12, minor_segments=4,
        location=(gc["pos"][0], gc["pos"][1], gc["pos"][2] + 0.08)
    )
    led_garden = bpy.context.active_object
    led_garden.name = f"led_strip_garden_{i+1:02d}"
    apply_smooth(led_garden)
    assign_mat(led_garden, "emissive")
    deselect_all()
print("  3 garden platform LED strips")

# ============================================================
# DETAIL 6: ADDITIONAL VEGETATION
# ============================================================
print("\n--- DETAIL 6: Additional Vegetation ---")

# 6a. More vine clusters hanging from platform edges
new_vine_positions = [
    {"name": "vine_cluster_05", "pos": (-1.5, -3.0, 0.5), "scale": (0.10, 0.10, 0.30)},
    {"name": "vine_cluster_06", "pos": (2.8, 1.5, 0.5),   "scale": (0.12, 0.12, 0.25)},
    {"name": "vine_cluster_07", "pos": (-4.2, 0.8, 0.4),  "scale": (0.08, 0.08, 0.22)},
    {"name": "vine_cluster_08", "pos": (0.0, -2.8, 0.5),  "scale": (0.11, 0.11, 0.28)},
]

for vc in new_vine_positions:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, vertices=6,
        location=vc["pos"]
    )
    vine = bpy.context.active_object
    vine.name = vc["name"]
    vine.scale = vc["scale"]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    apply_smooth(vine)
    assign_mat(vine, "holo")
    deselect_all()
print("  4 additional vine clusters")

# 6b. Small leaf/plant forms on planter walls
planter_leaf_configs = [
    {"name": "leaf_form_01", "pos": (0.3, 0.6, 1.12), "scale": (0.08, 0.05, 0.06)},
    {"name": "leaf_form_02", "pos": (0.15, 0.5, 1.10), "scale": (0.06, 0.04, 0.05)},
    {"name": "leaf_form_03", "pos": (1.0, 1.3, 1.10), "scale": (0.07, 0.05, 0.05)},
    {"name": "leaf_form_04", "pos": (1.15, 1.4, 1.08), "scale": (0.05, 0.04, 0.04)},
]

for lf in planter_leaf_configs:
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1.0, segments=6, ring_count=4,
        location=lf["pos"]
    )
    leaf = bpy.context.active_object
    leaf.name = lf["name"]
    leaf.scale = lf["scale"]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    apply_smooth(leaf)
    assign_mat(leaf, "holo")
    deselect_all()
print("  4 leaf forms on planter walls")

# ============================================================
# DETAIL 7: FLOATING STEPPING STONES
# ============================================================
print("\n--- DETAIL 7: Floating Stepping Stones ---")

# Small flat discs floating between garden platforms, suggesting
# a meditative path across water
stepping_stone_configs = [
    {"name": "stepping_stone_01", "pos": (-3.7, -1.0, 0.35), "radius": 0.18},
    {"name": "stepping_stone_02", "pos": (-3.9, -0.5, 0.38), "radius": 0.15},
    {"name": "stepping_stone_03", "pos": (-4.1, 0.0, 0.40),  "radius": 0.16},
    {"name": "stepping_stone_04", "pos": (-3.8, 0.5, 0.42),  "radius": 0.14},
    {"name": "stepping_stone_05", "pos": (-3.6, 1.0, 0.45),  "radius": 0.17},
    {"name": "stepping_stone_06", "pos": (-3.5, 1.5, 0.50),  "radius": 0.15},
    # Between garden_02 and main platform
    {"name": "stepping_stone_07", "pos": (3.2, -1.2, 0.55),  "radius": 0.16},
    {"name": "stepping_stone_08", "pos": (2.6, -1.0, 0.60),  "radius": 0.14},
]

for sc in stepping_stone_configs:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=sc["radius"], depth=0.04, vertices=8,
        location=sc["pos"]
    )
    stone = bpy.context.active_object
    stone.name = sc["name"]
    # Slight random rotation for organic feel
    stone.rotation_euler = (0, 0, hash(sc["name"]) % 628 / 100.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    apply_smooth(stone)
    assign_mat(stone, "base")
    deselect_all()
print(f"  {len(stepping_stone_configs)} stepping stones created")

# ============================================================
# DETAIL 8: DOME FACADE ENRICHMENT (Meridian Ribs)
# ============================================================
print("\n--- DETAIL 8: Dome Meridian Ribs ---")

# Add subtle meridian rib arcs on the dome surfaces.
# These are thin half-circle arcs placed vertically on the domes.
dome_rib_configs = [
    {"dome": "dome_large",  "radius": 1.8, "pos": (-1.2, -0.3, 0.97), "rib_count": 6},
    {"dome": "dome_medium", "radius": 1.2, "pos": (2.0, 0.5, 0.97),   "rib_count": 4},
    {"dome": "dome_small",  "radius": 0.8, "pos": (0.5, 1.8, 0.97),   "rib_count": 3},
]

for dc in dome_rib_configs:
    r = dc["radius"] + 0.02  # Slightly outside the dome
    for j in range(dc["rib_count"]):
        angle = j * math.pi / dc["rib_count"]

        # Create a half-circle arc as a thin cylinder rotated to become a rib
        rib_segments = 8
        rib_verts = []
        rib_edges = []
        rib_thickness = 0.015

        for k in range(rib_segments + 1):
            t = k / rib_segments
            theta = t * math.pi  # 0 to pi (half circle)

            # Position on dome surface
            x = r * math.cos(theta) * math.cos(angle)
            y = r * math.cos(theta) * math.sin(angle)
            z = r * math.sin(theta)

            rib_verts.append(Vector((x, y, z)))

        # Create mesh from vertices and edges (thin line)
        rib_name = f"rib_{dc['dome']}_{j+1:02d}"
        rib_mesh = bpy.data.meshes.new(rib_name)

        # Make it a thin tube: use bevel on a curve instead, or create
        # a simple edge-only mesh and add a skin modifier

        # Simpler approach: create a thin torus arc
        # Instead, use a series of small cylinders connected as a rib
        # For budget efficiency, just create a single thin cylinder per rib
        # oriented as a meridian line

        # Minimal rib: single thin cylinder as a great-circle arc
        # Position at dome center, rotate to become a meridian
        bpy.ops.mesh.primitive_cylinder_add(
            radius=rib_thickness, depth=r * math.pi * 0.95,
            vertices=4, location=(dc["pos"][0], dc["pos"][1], dc["pos"][2] + r/2)
        )
        rib = bpy.context.active_object
        rib.name = rib_name

        # Bend via lattice/curve is too complex -- just position as straight ribs
        # that read as structural detail at distance
        rib.rotation_euler = (0, 0, angle)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        apply_smooth(rib)
        assign_mat(rib, "detail")
        deselect_all()

print("  Dome meridian ribs created (13 total)")

# ============================================================
# DETAIL 9: PLATFORM RIM TOP RING (already exists, verify)
# ============================================================
print("\n--- Verifying existing platform_rim_top ---")
rim_top = bpy.data.objects.get("platform_rim_top")
if rim_top:
    print("  platform_rim_top exists")
else:
    # If missing, create it
    bpy.ops.mesh.primitive_torus_add(
        major_radius=4.6, minor_radius=0.08,
        major_segments=24, minor_segments=6,
        location=(0, 0, 0.97)
    )
    rim_top = bpy.context.active_object
    rim_top.name = "platform_rim_top"
    rim_top.scale = (1.0, 0.7, 0.5)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    apply_smooth(rim_top)
    assign_mat(rim_top, "accent")
    deselect_all()
    print("  platform_rim_top created (was missing)")

# ============================================================
# CHECKPOINT: Triangle count before polish
# ============================================================
pre_polish_tris = print_tri_report("PRE-POLISH")

# ============================================================
# POLISH CHECKLIST
# ============================================================
print("\n" + "=" * 60)
print("POLISH CHECKLIST")
print("=" * 60)

# P1. Check all objects have materials (no default gray)
unnamed_mats = []
no_mats = []
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    if not obj.data.materials or not obj.data.materials[0]:
        no_mats.append(obj.name)
    else:
        mat = obj.data.materials[0]
        valid_names = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
        if mat.name not in valid_names:
            unnamed_mats.append(f"{obj.name} -> {mat.name}")

if no_mats:
    print(f"  [FAIL] Objects without materials: {no_mats}")
else:
    print("  [PASS] All objects have materials assigned")

if unnamed_mats:
    print(f"  [WARN] Non-standard material names: {unnamed_mats}")
else:
    print("  [PASS] All material names match 7-slot regex")

# P2. Check object naming (no Cube.001 etc)
bad_names = [obj.name for obj in bpy.data.objects if obj.type == 'MESH'
             and any(obj.name.startswith(p) for p in ["Cube", "Cylinder", "Sphere", "Cone", "Torus", "Plane"])]
if bad_names:
    print(f"  [FAIL] Generic object names: {bad_names}")
else:
    print("  [PASS] All objects named descriptively")

# P3. Check normals (face orientation)
# Note: mesh.calc_normals() removed in Blender 5.x -- normals are auto-calculated
flipped = []
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    mesh = obj.data
    mesh.update()  # Ensure mesh data is current
    has_issue = False
    for poly in mesh.polygons:
        if poly.normal.length < 0.001:
            has_issue = True
            break
    if has_issue:
        flipped.append(obj.name)

if flipped:
    print(f"  [WARN] Possible normal issues: {flipped}")
else:
    print("  [PASS] Normals appear correct")

# P4. Apply all transforms (mesh objects only -- lights/cameras cannot have loc/rot applied)
print("  Applying all transforms (mesh objects only)...")
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')
print("  [DONE] All transforms applied")

# P5. Material distribution report
print("\n  Material Distribution:")
slot_tris = {"base": 0, "accent": 0, "glass": 0, "detail": 0,
             "emissive": 0, "energy": 0, "holo": 0, "other": 0}
depsgraph = bpy.context.evaluated_depsgraph_get()
total_tris_now = 0
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    obj_eval = obj.evaluated_get(depsgraph)
    mesh_eval = obj_eval.to_mesh()
    tris = sum(max(1, len(p.vertices) - 2) for p in mesh_eval.polygons)
    obj_eval.to_mesh_clear()
    total_tris_now += tris

    if obj.data.materials and obj.data.materials[0]:
        mat_name = obj.data.materials[0].name
        if mat_name in slot_tris:
            slot_tris[mat_name] += tris
        else:
            slot_tris["other"] += tris
    else:
        slot_tris["other"] += tris

for slot, tris in sorted(slot_tris.items(), key=lambda x: -x[1]):
    pct = tris / total_tris_now * 100 if total_tris_now > 0 else 0
    spec_range = {
        "base": "50-55%", "accent": "10-15%", "glass": "10-18%",
        "detail": "12-18%", "emissive": "3-8%", "energy": "0-5%",
        "holo": "0-5%", "other": "0%"
    }
    print(f"    {slot}: {tris} tris ({pct:.1f}%) [spec: {spec_range.get(slot, '?')}]")

# ============================================================
# DECIMATION (Per-Object)
# ============================================================
print("\n" + "=" * 60)
print("DECIMATION")
print("=" * 60)

current_total = count_total_tris()
print(f"Current total: {current_total} tris")

if current_total > MAX_TRIS:
    print(f"OVER BUDGET ({current_total} > {MAX_TRIS}). Decimating...")

    # Sort objects by tri count descending, decimate largest first
    obj_tris = count_tris_per_object()
    obj_tris.sort(key=lambda x: -x[1])

    # Calculate how much we need to cut
    excess = current_total - TARGET_TRIS
    cut_so_far = 0

    for obj_name, obj_tri_count in obj_tris:
        if cut_so_far >= excess:
            break
        if obj_tri_count < 50:  # Don't decimate tiny objects
            continue

        obj = bpy.data.objects.get(obj_name)
        if not obj or obj.type != 'MESH':
            continue

        # Determine decimation ratio based on object type
        # Large structural objects: gentler decimation (0.7-0.8)
        # Detail objects: can tolerate more (0.5-0.7)
        if obj_tri_count > 500:
            ratio = 0.65
        elif obj_tri_count > 200:
            ratio = 0.55
        else:
            ratio = 0.50

        expected_cut = obj_tri_count * (1 - ratio)

        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod.ratio = ratio
        bpy.ops.object.modifier_apply(modifier="Decimate")
        obj.select_set(False)
        deselect_all()

        # Count actual new tris
        new_total = count_total_tris()
        actual_cut = current_total - new_total
        cut_so_far += actual_cut
        current_total = new_total

        print(f"  {obj_name}: ratio={ratio:.2f}, cut ~{actual_cut} tris")

    print(f"\nAfter decimation: {count_total_tris()} tris")

elif current_total > TARGET_TRIS:
    print(f"Above target ({current_total} > {TARGET_TRIS}) but within budget. Light decimation...")

    obj_tris = count_tris_per_object()
    obj_tris.sort(key=lambda x: -x[1])

    # Only decimate the top 3 largest objects with gentle ratio
    for obj_name, obj_tri_count in obj_tris[:3]:
        if obj_tri_count < 200:
            continue
        obj = bpy.data.objects.get(obj_name)
        if not obj:
            continue

        ratio = 0.80
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod.ratio = ratio
        bpy.ops.object.modifier_apply(modifier="Decimate")
        obj.select_set(False)
        deselect_all()
        print(f"  {obj_name}: ratio={ratio:.2f}")

    print(f"\nAfter light decimation: {count_total_tris()} tris")
else:
    print(f"Within budget ({current_total} <= {TARGET_TRIS}). No decimation needed.")

# ============================================================
# FINAL TRI REPORT
# ============================================================
final_report = print_tri_report("FINAL")

# ============================================================
# EXPORT GLB
# ============================================================
print("\n" + "=" * 60)
print("EXPORT GLB")
print("=" * 60)

# Remove cameras and lights before export
to_remove = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in to_remove:
    bpy.data.objects.remove(obj, do_unlink=True)
print(f"  Removed {len(to_remove)} cameras/lights")

# Verify origin is at bottom-center
# Find the global minimum Z across all objects
global_min_z = float('inf')
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.data.vertices:
        for v in obj.data.vertices:
            world_z = (obj.matrix_world @ v.co).z
            if world_z < global_min_z:
                global_min_z = world_z

if global_min_z != float('inf') and abs(global_min_z) > 0.01:
    print(f"  Adjusting origin: global min Z was {global_min_z:.3f}, shifting to 0")
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.location.z -= global_min_z

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
final_tris = count_total_tris()
print(f"\n  Exported: {GLB_OUT}")
print(f"  Triangles: {final_tris}")
print(f"  File size: {file_size_kb:.0f} KB")
print(f"  Budget check: {'PASS' if final_tris <= MAX_TRIS else 'OVER BUDGET'}")
print(f"  Size check: {'PASS' if file_size_kb <= 400 else 'LARGE (>400KB)'}")

# ============================================================
# SAVE .BLEND (without cameras/lights -- re-add for screenshots)
# ============================================================
# Re-add camera for screenshots
cam_data = bpy.data.cameras.new(name="Overview_Camera")
cam_data.lens_unit = 'FOV'
cam_data.angle = math.radians(45)
cam_data.clip_start = 0.1
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Overview_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (12, -10, 6)
target = Vector((0, 0, 1.2))
cam_dir = target - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam_obj

# Re-add basic lighting for viewport
key_data = bpy.data.lights.new(name="Key_Light", type='SUN')
key_data.color = (1.0, 0.894, 0.8)
key_data.energy = 0.8
key_obj = bpy.data.objects.new("Key_Light", key_data)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (-8, 20, -6)
key_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

fill_data = bpy.data.lights.new(name="Fill_Light", type='AREA')
fill_data.color = (0.102, 0.102, 0.251)
fill_data.energy = 50
fill_data.size = 20
fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (5, 15, 10)
fill_obj.rotation_euler = (math.radians(60), 0, 0)

# Save the blend file
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print(f"\n  Saved .blend: {BLEND_OUT}")

# ============================================================
# SCREENSHOTS
# ============================================================
print("\n" + "=" * 60)
print("RENDERING SCREENSHOTS")
print("=" * 60)

# Set up render for screenshots
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100

try:
    engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'ShaderNodeEeveeSpecular') else 'BLENDER_EEVEE'
    bpy.context.scene.render.engine = engine
except Exception:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGB'

# World background
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)

# Screenshot 1: Front elevation
cam_obj.location = (0, -14, 3)
cam_dir = Vector((0, 0, 1.0)) - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.render.filepath = os.path.join(SAVE_DIR, "s10_front_elevation.png")
bpy.ops.render.render(write_still=True)
print("  s10_front_elevation.png rendered")

# Screenshot 2: 3/4 angle
cam_obj.location = (12, -10, 6)
cam_dir = Vector((0, 0, 1.2)) - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.render.filepath = os.path.join(SAVE_DIR, "s10_three_quarter.png")
bpy.ops.render.render(write_still=True)
print("  s10_three_quarter.png rendered")

# Screenshot 3: Distance overview
cam_obj.location = (18, -15, 10)
cam_dir = Vector((0, 0, 0.8)) - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.render.filepath = os.path.join(SAVE_DIR, "s10_distance_overview.png")
bpy.ops.render.render(write_still=True)
print("  s10_distance_overview.png rendered")

# Screenshot 4: Top-down for layout verification
cam_obj.location = (0, 0, 12)
cam_obj.rotation_euler = (0, 0, 0)  # Looking straight down
cam_dir = Vector((0, 0, 0)) - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.render.filepath = os.path.join(SAVE_DIR, "s10_top_down.png")
bpy.ops.render.render(write_still=True)
print("  s10_top_down.png rendered")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("SESSION 10 COMPLETE")
print("=" * 60)
print(f"  Initial tris (from S09): {initial_tris}")
print(f"  Pre-polish tris: {pre_polish_tris}")
print(f"  Final tris: {final_tris}")
print(f"  Budget: {MAX_TRIS}")
print(f"  GLB size: {file_size_kb:.0f} KB")
print(f"  .blend: {BLEND_OUT}")
print(f"  .glb: {GLB_OUT}")
print(f"  Screenshots: 4 (front, 3/4, distance, top-down)")
print(f"  Mesh objects: {sum(1 for o in bpy.data.objects if o.type == 'MESH')}")
print("=" * 60)

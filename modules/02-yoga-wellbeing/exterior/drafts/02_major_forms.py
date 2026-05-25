"""
Session 9 — Yoga & Wellbeing: Step 2 — Major Form Geometry
Build all primary architectural volumes for the floating sanctuary.

Structure: ~10u wide, ~2.5u tall floating organic platform complex over water.
"""
import bpy
import bmesh
import math
from mathutils import Vector

# Helper: assign material by slot name
def assign_mat(obj, slot_name):
    mat = bpy.data.materials.get(slot_name)
    if mat:
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
    else:
        print(f"WARNING: Material '{slot_name}' not found!")

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

# ============================================================
# ELEMENT 1: REFLECTING LAKE SURFACE
# Flat plane below the building, glass material for mirror effect
# ============================================================
bpy.ops.mesh.primitive_plane_add(size=18, location=(0, 0, -0.05))
lake = bpy.context.active_object
lake.name = "reflecting_lake"
lake.scale = (1.0, 0.7, 1.0)  # slightly elliptical, 18x12.6u
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
assign_mat(lake, "glass")
deselect_all()

print("1/9 reflecting_lake created")

# ============================================================
# ELEMENT 2: MAIN FLOATING PLATFORM
# Large organic curved disc, ~10x7u, elevated ~0.8u above water
# Using a cylinder with low height, then applying subdivision for organic feel
# ============================================================
bpy.ops.mesh.primitive_cylinder_add(
    radius=5.0, depth=0.35, vertices=32,
    location=(0, 0, 0.8)
)
platform = bpy.context.active_object
platform.name = "main_platform"
# Scale to make elliptical (wider than deep)
platform.scale = (1.0, 0.7, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Add subdivision for organic smoothness
mod = platform.modifiers.new(name="Subdivision", type='SUBSURF')
mod.levels = 2
mod.render_levels = 2
bpy.context.view_layer.objects.active = platform
platform.select_set(True)
bpy.ops.object.modifier_apply(modifier="Subdivision")
platform.select_set(False)

assign_mat(platform, "base")
deselect_all()

print("2/9 main_platform created")

# ============================================================
# ELEMENT 3: PLATFORM UNDERSIDE RIM
# A slightly inset ring on the bottom edge to give visual thickness
# ============================================================
bpy.ops.mesh.primitive_torus_add(
    major_radius=4.8, minor_radius=0.12,
    major_segments=32, minor_segments=8,
    location=(0, 0, 0.63)
)
rim = bpy.context.active_object
rim.name = "platform_rim"
rim.scale = (1.0, 0.7, 0.6)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
assign_mat(rim, "accent")
deselect_all()

print("3/9 platform_rim created")

# ============================================================
# ELEMENT 4: SUPPORT PILLARS (5 tapered columns from water to platform)
# Organic tapered forms — wider at bottom, narrower at top
# ============================================================
pillar_positions = [
    (-2.5, -1.5),  # front-left
    (2.5, -1.5),   # front-right
    (-3.0, 1.0),   # mid-left
    (3.0, 1.0),    # mid-right
    (0.0, 2.0),    # back-center
]

for i, (px, py) in enumerate(pillar_positions):
    # Create tapered cylinder using a cone shape
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.28,   # bottom (wider)
        radius2=0.15,   # top (narrower)
        depth=0.85,     # from water surface to platform
        vertices=12,
        location=(px, py, 0.375)  # centered between water (0) and platform (0.8)
    )
    pillar = bpy.context.active_object
    pillar.name = f"support_pillar_{i+1:02d}"

    # Smooth shading
    bpy.ops.object.shade_smooth()

    assign_mat(pillar, "detail")
    deselect_all()

print("4/9 support_pillars created (5 pillars)")

# ============================================================
# ELEMENT 5: GLASS DOMES (3 domes of varying sizes)
# Partial spheres — the main architectural signature
# ============================================================
dome_configs = [
    {"name": "dome_large",  "radius": 1.8, "pos": (-1.2, -0.3, 0.97), "segments": 24},
    {"name": "dome_medium", "radius": 1.2, "pos": (2.0, 0.5, 0.97),   "segments": 20},
    {"name": "dome_small",  "radius": 0.8, "pos": (0.5, 1.8, 0.97),   "segments": 16},
]

for dc in dome_configs:
    # Create UV sphere and cut bottom half to make a dome
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=dc["radius"],
        segments=dc["segments"],
        ring_count=dc["segments"] // 2,
        location=dc["pos"]
    )
    dome = bpy.context.active_object
    dome.name = dc["name"]

    # Remove bottom hemisphere using bmesh
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(dome.data)
    bm.verts.ensure_lookup_table()

    # Select vertices below the dome base (below dome center)
    verts_to_delete = [v for v in bm.verts if v.co.z < -0.05]
    bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')
    bmesh.update_edit_mesh(dome.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Smooth shading
    bpy.ops.object.shade_smooth()

    assign_mat(dome, "glass")
    deselect_all()

print("5/9 glass_domes created (3 domes)")

# ============================================================
# ELEMENT 6: DOME BASES / LIVING WALL BANDS
# Cylindrical collars at the base of each dome — holo material for bioluminescence
# ============================================================
for dc in dome_configs:
    collar_name = dc["name"].replace("dome_", "dome_collar_")
    bpy.ops.mesh.primitive_cylinder_add(
        radius=dc["radius"] + 0.05,
        depth=0.18,
        vertices=dc["segments"],
        location=(dc["pos"][0], dc["pos"][1], dc["pos"][2] - 0.02)
    )
    collar = bpy.context.active_object
    collar.name = collar_name
    bpy.ops.object.shade_smooth()
    assign_mat(collar, "holo")
    deselect_all()

print("6/9 dome_collars created (3 collars, holo)")

# ============================================================
# ELEMENT 7: MEDITATION GARDEN PLATFORMS
# 2 smaller floating discs at varying heights around the main platform
# ============================================================
garden_configs = [
    {"name": "garden_platform_01", "radius": 1.2, "pos": (-4.0, -1.0, 0.5), "depth": 0.15},
    {"name": "garden_platform_02", "radius": 0.9, "pos": (3.8, -1.5, 0.6), "depth": 0.12},
    {"name": "garden_platform_03", "radius": 0.7, "pos": (-3.5, 2.0, 0.7), "depth": 0.10},
]

for gc in garden_configs:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=gc["radius"], depth=gc["depth"], vertices=20,
        location=gc["pos"]
    )
    gp = bpy.context.active_object
    gp.name = gc["name"]

    # Subdivision for organic roundness
    mod = gp.modifiers.new(name="Subdivision", type='SUBSURF')
    mod.levels = 1
    mod.render_levels = 1
    bpy.context.view_layer.objects.active = gp
    gp.select_set(True)
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    gp.select_set(False)

    bpy.ops.object.shade_smooth()
    assign_mat(gp, "base")
    deselect_all()

print("7/9 garden_platforms created (3 platforms)")

# ============================================================
# ELEMENT 8: FLOATING WALKWAYS
# Thin curved paths connecting dome sections — using curved cylinders
# ============================================================

# Walkway 1: Large dome -> Medium dome
def create_walkway(name, start, end, width=0.2, rail_height=0.15):
    """Create a simple walkway bridge between two points."""
    mid = ((start[0]+end[0])/2, (start[1]+end[1])/2, max(start[2], end[2]) + 0.08)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    angle = math.atan2(dy, dx)

    # Walkway deck
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(mid[0], mid[1], mid[2])
    )
    deck = bpy.context.active_object
    deck.name = name
    deck.scale = (length / 2, width, 0.03)
    deck.rotation_euler = (0, 0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_smooth()
    assign_mat(deck, "detail")
    deselect_all()

    # Left railing
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(mid[0] - math.sin(angle) * width,
                  mid[1] + math.cos(angle) * width,
                  mid[2] + rail_height)
    )
    rail_l = bpy.context.active_object
    rail_l.name = name + "_rail_L"
    rail_l.scale = (length / 2, 0.015, rail_height)
    rail_l.rotation_euler = (0, 0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign_mat(rail_l, "accent")
    deselect_all()

    # Right railing
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(mid[0] + math.sin(angle) * width,
                  mid[1] - math.cos(angle) * width,
                  mid[2] + rail_height)
    )
    rail_r = bpy.context.active_object
    rail_r.name = name + "_rail_R"
    rail_r.scale = (length / 2, 0.015, rail_height)
    rail_r.rotation_euler = (0, 0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign_mat(rail_r, "accent")
    deselect_all()

# Walkway between large dome and medium dome
create_walkway("walkway_01",
    start=(-1.2 + 1.8, -0.3, 0.97),   # edge of large dome
    end=(2.0 - 1.2, 0.5, 0.97),       # edge of medium dome
    width=0.18)

# Walkway between medium dome and small dome
create_walkway("walkway_02",
    start=(2.0 - 0.5, 0.5 + 1.0, 0.97),
    end=(0.5 + 0.3, 1.8 - 0.5, 0.97),
    width=0.15)

# Walkway from main platform edge to garden platform 01
create_walkway("walkway_03",
    start=(-3.5, -1.0, 0.8),
    end=(-4.0 + 0.8, -1.0, 0.5),
    width=0.15)

print("8/9 walkways created (3 walkways with railings)")

# ============================================================
# ELEMENT 9: TERRACE PLANTER WALLS + HANGING GARDENS + ENERGY RECEPTOR
# ============================================================

# Terrace planter walls between domes (organic rounded forms)
planter_positions = [
    {"name": "planter_wall_01", "pos": (0.3, 0.6, 0.97), "radius": 0.3, "height": 0.2},
    {"name": "planter_wall_02", "pos": (1.0, 1.3, 0.97), "radius": 0.25, "height": 0.18},
]

for pp in planter_positions:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=pp["radius"], depth=pp["height"], vertices=12,
        location=pp["pos"]
    )
    pw = bpy.context.active_object
    pw.name = pp["name"]
    bpy.ops.object.shade_smooth()
    assign_mat(pw, "base")
    deselect_all()

# Hanging garden vine clusters at platform edges (simplified cylinder clusters, holo)
vine_positions = [
    {"name": "vine_cluster_01", "pos": (-3.8, 0.0, 0.6), "scale": (0.15, 0.15, 0.35)},
    {"name": "vine_cluster_02", "pos": (3.5, -0.8, 0.6), "scale": (0.12, 0.12, 0.30)},
    {"name": "vine_cluster_03", "pos": (-2.0, -2.5, 0.6), "scale": (0.10, 0.10, 0.25)},
    {"name": "vine_cluster_04", "pos": (1.5, -2.2, 0.6), "scale": (0.13, 0.13, 0.28)},
]

for vc in vine_positions:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, vertices=8,
        location=vc["pos"]
    )
    vine = bpy.context.active_object
    vine.name = vc["name"]
    vine.scale = vc["scale"]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_smooth()
    assign_mat(vine, "holo")
    deselect_all()

# Dome apex energy receptor — soft glow point on largest dome apex
# Small sphere at top of large dome
dome_large_top_z = 0.97 + 1.8  # dome center + radius
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, segments=12, ring_count=6,
    location=(-1.2, -0.3, dome_large_top_z)
)
receptor = bpy.context.active_object
receptor.name = "energy_receptor"
bpy.ops.object.shade_smooth()
assign_mat(receptor, "emissive")
deselect_all()

print("9/9 planters, vines, receptor created")

# ============================================================
# FINAL: COUNT ALL MESH TRIS
# ============================================================
total_tris = 0
mesh_report = []
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        # Evaluate depsgraph to count actual tris
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh = obj_eval.to_mesh()
        tris = sum(1 for f in mesh.polygons for _ in range(max(1, len(f.vertices) - 2)))
        obj_eval.to_mesh_clear()
        mesh_report.append(f"  {obj.name}: {tris} tris")
        total_tris += tris

print(f"\n=== MESH OBJECT REPORT ===")
for line in mesh_report:
    print(line)
print(f"=== TOTAL: {total_tris} tris (budget: <10,800) ===")
print(f"Budget usage: {total_tris / 10800 * 100:.1f}%")

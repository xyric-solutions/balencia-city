"""
Session 9 — Yoga & Wellbeing Exterior: Complete Build Script
Run headless: blender -b -P build_yoga_exterior.py

Creates the full scene from scratch:
1. Clear scene
2. Lighting rig (3-point cinematic)
3. Material library (7-slot, Sage #6EE7B7)
4. All major form geometry
5. Save .blend file
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector

SAVE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/exterior/drafts"
BLEND_FILE = os.path.join(SAVE_DIR, "yoga-exterior-s09.blend")

# ============================================================
# STEP 1: CLEAR SCENE
# ============================================================
# Delete everything in the scene
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat)
for cam in list(bpy.data.cameras):
    bpy.data.cameras.remove(cam)
for light in list(bpy.data.lights):
    bpy.data.lights.remove(light)

print("Scene cleared.")

# ============================================================
# STEP 2: LIGHTING RIG
# ============================================================
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)  # #0A0A0F
    bg_node.inputs["Strength"].default_value = 1.0

# Key Light (Sun)
key_data = bpy.data.lights.new(name="Key_Light", type='SUN')
key_data.color = (1.0, 0.894, 0.8)
key_data.energy = 0.8
key_data.use_shadow = True
key_data.shadow_soft_size = 0.5
key_obj = bpy.data.objects.new("Key_Light", key_data)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (-8, 20, -6)
key_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

# Rim Light (Spot)
rim_data = bpy.data.lights.new(name="Rim_Light", type='SPOT')
rim_data.color = (1.0, 0.369, 0.0)
rim_data.energy = 200
rim_data.spot_size = math.radians(45)
rim_data.spot_blend = 0.9
rim_data.use_shadow = True
rim_obj = bpy.data.objects.new("Rim_Light", rim_data)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (10, 18, -14)
direction = Vector((0, 0, -3)) - Vector((10, 18, -14))
rim_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# Fill Light (Area)
fill_data = bpy.data.lights.new(name="Fill_Light", type='AREA')
fill_data.color = (0.102, 0.102, 0.251)
fill_data.energy = 50
fill_data.size = 20
fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (5, 15, 10)
fill_obj.rotation_euler = (math.radians(60), 0, 0)

# Camera — positioned for horizontal low-rise building
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

# Render settings
try:
    engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'ShaderNodeEeveeSpecular') else 'BLENDER_EEVEE'
    bpy.context.scene.render.engine = engine
except Exception:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

eevee = bpy.context.scene.eevee
if hasattr(eevee, 'use_bloom'):
    eevee.use_bloom = True
    eevee.bloom_threshold = 0.4
    eevee.bloom_intensity = 0.6
if hasattr(eevee, 'use_ssr'):
    eevee.use_ssr = True
if hasattr(eevee, 'use_gtao'):
    eevee.use_gtao = True
    eevee.gtao_distance = 0.35

print("Lighting rig loaded.")

# ============================================================
# STEP 3: MATERIAL LIBRARY (7-Slot for Sage #6EE7B7)
# ============================================================
def hex_to_linear(hex_color):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    def to_linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (to_linear(r), to_linear(g), to_linear(b), 1.0)

BASE_COLOR = hex_to_linear("#1E1E28")
ACCENT_INACTIVE = hex_to_linear("#2A2A38")
GLASS_COLOR = hex_to_linear("#0F0F18")
DETAIL_COLOR = hex_to_linear("#16161E")
ENERGY_ORANGE = hex_to_linear("#FF5E00")
DISTRICT_COLOR = hex_to_linear("#6EE7B7")

def make_mat(name, base_color, roughness, metallic, emission_color=None, emission_strength=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission_color and emission_strength > 0:
        bsdf.inputs["Emission Color"].default_value = emission_color
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    if alpha < 1.0:
        if hasattr(mat, 'blend_method'):
            mat.blend_method = 'BLEND'
        bsdf.inputs["Alpha"].default_value = alpha
    return mat

mats = {}
mats["base"] = make_mat("base", BASE_COLOR, 0.80, 0.05)
mats["accent"] = make_mat("accent", ACCENT_INACTIVE, 0.55, 0.16, DISTRICT_COLOR, 0.24)
mats["glass"] = make_mat("glass", GLASS_COLOR, 0.10, 0.30, hex_to_linear("#FEF3C7"), 0.08, alpha=0.86)
mats["detail"] = make_mat("detail", DETAIL_COLOR, 0.60, 0.15)
mats["emissive"] = make_mat("emissive", DETAIL_COLOR, 0.22, 0.00, DISTRICT_COLOR, 0.06)
mats["energy"] = make_mat("energy", DETAIL_COLOR, 0.15, 0.10, ENERGY_ORANGE, 0.10)
mats["holo"] = make_mat("holo", DETAIL_COLOR, 0.20, 0.05, DISTRICT_COLOR, 0.15, alpha=0.40)

print(f"Materials created: {len(mats)} ({', '.join(mats.keys())})")

# ============================================================
# HELPERS
# ============================================================
def assign_mat(obj, slot_name):
    mat = bpy.data.materials.get(slot_name)
    if mat:
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

# ============================================================
# ELEMENT 1: REFLECTING LAKE SURFACE
# ============================================================
bpy.ops.mesh.primitive_plane_add(size=18, location=(0, 0, -0.05))
lake = bpy.context.active_object
lake.name = "reflecting_lake"
lake.scale = (1.0, 0.7, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
assign_mat(lake, "glass")
deselect_all()
print("  1/10 reflecting_lake")

# ============================================================
# ELEMENT 2: MAIN FLOATING PLATFORM
# Large organic curved disc ~10x7u, elevated ~0.8u above water
# ============================================================
bpy.ops.mesh.primitive_cylinder_add(
    radius=5.0, depth=0.35, vertices=32,
    location=(0, 0, 0.8)
)
platform = bpy.context.active_object
platform.name = "main_platform"
platform.scale = (1.0, 0.7, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Subdivision for organic smoothness
mod = platform.modifiers.new(name="Subdivision", type='SUBSURF')
mod.levels = 2
mod.render_levels = 2
bpy.context.view_layer.objects.active = platform
platform.select_set(True)
bpy.ops.object.modifier_apply(modifier="Subdivision")
platform.select_set(False)

assign_mat(platform, "base")
deselect_all()
print("  2/10 main_platform")

# ============================================================
# ELEMENT 3: PLATFORM UNDERSIDE RIM (accent ring for visual definition)
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
print("  3/10 platform_rim")

# ============================================================
# ELEMENT 4: SUPPORT PILLARS (5 tapered columns from water to platform)
# ============================================================
pillar_positions = [
    (-2.5, -1.5),
    (2.5, -1.5),
    (-3.0, 1.0),
    (3.0, 1.0),
    (0.0, 2.0),
]

for i, (px, py) in enumerate(pillar_positions):
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.28, radius2=0.15, depth=0.85,
        vertices=12,
        location=(px, py, 0.375)
    )
    pillar = bpy.context.active_object
    pillar.name = f"support_pillar_{i+1:02d}"
    bpy.ops.object.shade_smooth()
    assign_mat(pillar, "detail")
    deselect_all()
print("  4/10 support_pillars (5)")

# ============================================================
# ELEMENT 5: GLASS DOMES (3 domes, varying sizes)
# Hemisphere geometry — the architectural signature
# ============================================================
dome_configs = [
    {"name": "dome_large",  "radius": 1.8, "pos": (-1.2, -0.3, 0.97), "segments": 24},
    {"name": "dome_medium", "radius": 1.2, "pos": (2.0, 0.5, 0.97),   "segments": 20},
    {"name": "dome_small",  "radius": 0.8, "pos": (0.5, 1.8, 0.97),   "segments": 16},
]

for dc in dome_configs:
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=dc["radius"],
        segments=dc["segments"],
        ring_count=dc["segments"] // 2,
        location=dc["pos"]
    )
    dome = bpy.context.active_object
    dome.name = dc["name"]

    # Remove bottom hemisphere
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(dome.data)
    bm.verts.ensure_lookup_table()
    verts_to_delete = [v for v in bm.verts if v.co.z < -0.05]
    bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')
    bmesh.update_edit_mesh(dome.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.shade_smooth()
    assign_mat(dome, "glass")
    deselect_all()
print("  5/10 glass_domes (3)")

# ============================================================
# ELEMENT 6: DOME BASE COLLARS (holo bioluminescent bands)
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
print("  6/10 dome_collars (3, holo)")

# ============================================================
# ELEMENT 7: MEDITATION GARDEN PLATFORMS (3 floating discs)
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
print("  7/10 garden_platforms (3)")

# ============================================================
# ELEMENT 8: FLOATING WALKWAYS (3 walkways with railings)
# ============================================================
def create_walkway(name, start, end, width=0.2, rail_height=0.15):
    mid = ((start[0]+end[0])/2, (start[1]+end[1])/2, max(start[2], end[2]) + 0.08)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    angle = math.atan2(dy, dx)

    # Deck
    bpy.ops.mesh.primitive_cube_add(size=1, location=mid)
    deck = bpy.context.active_object
    deck.name = name
    deck.scale = (length / 2, width, 0.03)
    deck.rotation_euler = (0, 0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_smooth()
    assign_mat(deck, "detail")
    deselect_all()

    # Left railing
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        mid[0] - math.sin(angle) * width,
        mid[1] + math.cos(angle) * width,
        mid[2] + rail_height
    ))
    rail_l = bpy.context.active_object
    rail_l.name = name + "_rail_L"
    rail_l.scale = (length / 2, 0.015, rail_height)
    rail_l.rotation_euler = (0, 0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign_mat(rail_l, "accent")
    deselect_all()

    # Right railing
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        mid[0] + math.sin(angle) * width,
        mid[1] - math.cos(angle) * width,
        mid[2] + rail_height
    ))
    rail_r = bpy.context.active_object
    rail_r.name = name + "_rail_R"
    rail_r.scale = (length / 2, 0.015, rail_height)
    rail_r.rotation_euler = (0, 0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign_mat(rail_r, "accent")
    deselect_all()

# Large dome edge -> Medium dome edge
create_walkway("walkway_01",
    start=(0.6, -0.3, 0.97),
    end=(0.8, 0.5, 0.97),
    width=0.18)

# Medium dome -> Small dome
create_walkway("walkway_02",
    start=(1.5, 1.2, 0.97),
    end=(0.8, 1.3, 0.97),
    width=0.15)

# Main platform edge to garden platform 01
create_walkway("walkway_03",
    start=(-3.5, -1.0, 0.8),
    end=(-3.2, -1.0, 0.5),
    width=0.15)

print("  8/10 walkways (3 with railings)")

# ============================================================
# ELEMENT 9: TERRACE PLANTER WALLS
# ============================================================
planter_configs = [
    {"name": "planter_wall_01", "pos": (0.3, 0.6, 0.97), "radius": 0.3, "height": 0.2},
    {"name": "planter_wall_02", "pos": (1.0, 1.3, 0.97), "radius": 0.25, "height": 0.18},
]

for pp in planter_configs:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=pp["radius"], depth=pp["height"], vertices=12,
        location=pp["pos"]
    )
    pw = bpy.context.active_object
    pw.name = pp["name"]
    bpy.ops.object.shade_smooth()
    assign_mat(pw, "base")
    deselect_all()
print("  9a/10 planter_walls (2)")

# ============================================================
# ELEMENT 10: HANGING GARDENS + ENERGY RECEPTOR
# ============================================================
# Vine clusters (holo)
vine_positions = [
    {"name": "vine_cluster_01", "pos": (-3.8, 0.0, 0.5), "scale": (0.15, 0.15, 0.35)},
    {"name": "vine_cluster_02", "pos": (3.5, -0.8, 0.5), "scale": (0.12, 0.12, 0.30)},
    {"name": "vine_cluster_03", "pos": (-2.0, -2.5, 0.5), "scale": (0.10, 0.10, 0.25)},
    {"name": "vine_cluster_04", "pos": (1.5, -2.2, 0.5), "scale": (0.13, 0.13, 0.28)},
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
print("  9b/10 vine_clusters (4, holo)")

# Energy receptor sphere on largest dome apex
dome_large_top_z = 0.97 + 1.8
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, segments=12, ring_count=6,
    location=(-1.2, -0.3, dome_large_top_z)
)
receptor = bpy.context.active_object
receptor.name = "energy_receptor"
bpy.ops.object.shade_smooth()
assign_mat(receptor, "emissive")
deselect_all()
print("  10/10 energy_receptor")

# ============================================================
# TRIANGLE COUNT REPORT
# ============================================================
total_tris = 0
mesh_report = []
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh_eval = obj_eval.to_mesh()
        tris = 0
        for poly in mesh_eval.polygons:
            # Each polygon with N verts = N-2 triangles
            tris += max(1, len(poly.vertices) - 2)
        obj_eval.to_mesh_clear()
        mesh_report.append((obj.name, tris))
        total_tris += tris

print("\n=== TRIANGLE COUNT REPORT ===")
for name, count in sorted(mesh_report, key=lambda x: -x[1]):
    print(f"  {name}: {count}")
print(f"\n  TOTAL: {total_tris} tris")
print(f"  Budget: 10,800 tris (60% of 18K)")
print(f"  Usage: {total_tris / 10800 * 100:.1f}%")

# ============================================================
# SAVE .blend FILE
# ============================================================
os.makedirs(SAVE_DIR, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
print(f"\nSaved: {BLEND_FILE}")
print("Build complete. Open in Blender to take viewport screenshots.")

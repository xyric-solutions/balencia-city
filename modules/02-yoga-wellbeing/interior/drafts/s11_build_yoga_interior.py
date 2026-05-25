"""
Session 11 -- Yoga & Wellbeing Interior
Balencia City v3

Build order:
  1. Clear scene
  2. Lighting rig + material library (inline, matching shared scripts)
  3. Room shell (floor, dome ceiling, walls, open windowed section)
  4. Focal element (breathing energy rings)
  5. Props (yoga mats, pools, lanterns, pods, sub-dome, stones)
  6. Empties (light_0, light_1, light_2, camera_target)
  7. Material audit
  8. Tri count + distribution report
  9. Apply transforms
 10. Export GLB + save .blend

Run via Blender MCP or:
  blender -b -P s11_build_yoga_interior.py
"""

import bpy
import bmesh
import math
import os

# ---------------------------------------------------------------------------
# 0. CONFIGURATION
# ---------------------------------------------------------------------------

DOME_RADIUS = 5.5        # Interior dome radius (~11m diameter)
FLOOR_RADIUS = 5.6       # Floor slightly larger than dome
DOME_HEIGHT = 4.5         # Apex height of dome interior
YOGA_CIRCLE_RADIUS = 3.0 # Radius of the yoga mat circle
DISTRICT_COLOR_HEX = "#6EE7B7"

PROJECT_ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "modules/02-yoga-wellbeing/interior/drafts")
BLEND_PATH = os.path.join(OUTPUT_DIR, "yoga-interior-s11.blend")
GLB_PATH = os.path.join(OUTPUT_DIR, "yoga-int-draft-s11.glb")

# ---------------------------------------------------------------------------
# 1. CLEAR SCENE
# ---------------------------------------------------------------------------

bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------------------------------------------------------------------------
# 2. MATERIALS (7-slot system)
# ---------------------------------------------------------------------------

def hex_to_linear(hex_color):
    """Convert hex color string to linear RGBA tuple."""
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
district_color = hex_to_linear(DISTRICT_COLOR_HEX)

def make_material(name, base_color, roughness, metallic,
                  emission_color=None, emission_strength=0.0, alpha=1.0):
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

materials = {
    "base": make_material("base", BASE_COLOR, 0.80, 0.05),
    "accent": make_material("accent", ACCENT_INACTIVE, 0.55, 0.16,
                            emission_color=district_color, emission_strength=0.24),
    "glass": make_material("glass", GLASS_COLOR, 0.10, 0.30,
                           emission_color=hex_to_linear("#FEF3C7"),
                           emission_strength=0.08, alpha=0.86),
    "detail": make_material("detail", DETAIL_COLOR, 0.60, 0.15),
    "emissive": make_material("emissive", DETAIL_COLOR, 0.22, 0.00,
                              emission_color=district_color, emission_strength=0.06),
    "energy": make_material("energy", DETAIL_COLOR, 0.15, 0.10,
                            emission_color=ENERGY_ORANGE, emission_strength=0.10),
    "holo": make_material("holo", DETAIL_COLOR, 0.20, 0.05,
                          emission_color=district_color, emission_strength=0.15,
                          alpha=0.40),
}

def assign_mat(obj, slot_name):
    mat = materials[slot_name]
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# ---------------------------------------------------------------------------
# LIGHTING RIG (viewport preview only -- excluded from GLB export)
# ---------------------------------------------------------------------------

world = bpy.data.worlds.new("BalenciaWorld")
bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)
    bg_node.inputs["Strength"].default_value = 1.0

key_data = bpy.data.lights.new(name="Key_Light", type='SUN')
key_data.color = (1.0, 0.894, 0.8)
key_data.energy = 0.8
key_data.use_shadow = True
key_obj = bpy.data.objects.new("Key_Light", key_data)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (0, 0, 8)

fill_data = bpy.data.lights.new(name="Fill_Light", type='AREA')
fill_data.color = (0.102, 0.102, 0.251)
fill_data.energy = 50
fill_data.size = 12
fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (5, 5, 4)
fill_obj.rotation_euler = (math.radians(60), 0, math.radians(-45))

rim_data = bpy.data.lights.new(name="Rim_Light", type='SPOT')
rim_data.color = (1.0, 0.369, 0.0)
rim_data.energy = 150
rim_data.spot_size = math.radians(60)
rim_data.spot_blend = 0.9
rim_obj = bpy.data.objects.new("Rim_Light", rim_data)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (0, 6, 3)
rim_obj.rotation_euler = (math.radians(120), 0, math.radians(180))

cam_data = bpy.data.cameras.new(name="Overview_Camera")
cam_data.lens_unit = 'FOV'
cam_data.angle = math.radians(50)
cam_data.clip_start = 0.1
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Overview_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (0, -8, 4)
from mathutils import Vector
target_pt = Vector((0, 0, 1.0))
direction = target_pt - cam_obj.location
cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam_obj

try:
    engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'ShaderNodeEeveeSpecular') else 'BLENDER_EEVEE'
    bpy.context.scene.render.engine = engine
except Exception:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

print("[S11] Scene cleared, lighting rig + materials created.")

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def select_only(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def apply_transforms(obj):
    select_only(obj)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

def get_tri_count(obj):
    if obj.type != 'MESH':
        return 0
    dg = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(dg)
    mesh = eval_obj.to_mesh()
    mesh.calc_loop_triangles()
    count = len(mesh.loop_triangles)
    eval_obj.to_mesh_clear()
    return count

def cut_below_z(obj, z_threshold=-0.05):
    """Delete vertices below z_threshold in edit mode."""
    select_only(obj)
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    below = [v for v in bm.verts if v.co.z < z_threshold]
    if below:
        bmesh.ops.delete(bm, geom=below, context='VERTS')
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

# ---------------------------------------------------------------------------
# 3. ROOM SHELL
# ---------------------------------------------------------------------------
print("[S11] Building room shell...")

# -- Floor: main circular disc (high vertex count for base domination) --
bpy.ops.mesh.primitive_cylinder_add(
    radius=FLOOR_RADIUS, depth=0.15, vertices=64,
    location=(0, 0, -0.075)
)
floor = bpy.context.active_object
floor.name = "floor"
assign_mat(floor, "base")
apply_transforms(floor)

# -- Floor: secondary structural layer underneath --
bpy.ops.mesh.primitive_cylinder_add(
    radius=FLOOR_RADIUS - 0.3, depth=0.08, vertices=48,
    location=(0, 0, -0.19)
)
floor_under = bpy.context.active_object
floor_under.name = "floor_underside"
assign_mat(floor_under, "base")
apply_transforms(floor_under)

# -- Floor: border ring --
bpy.ops.mesh.primitive_torus_add(
    major_radius=FLOOR_RADIUS - 0.1,
    minor_radius=0.08,
    major_segments=48,
    minor_segments=6,
    location=(0, 0, 0.0)
)
floor_border = bpy.context.active_object
floor_border.name = "floor_border_ring"
assign_mat(floor_border, "base")
apply_transforms(floor_border)

# -- Floor: inner border ring --
bpy.ops.mesh.primitive_torus_add(
    major_radius=FLOOR_RADIUS - 1.2,
    minor_radius=0.05,
    major_segments=48,
    minor_segments=4,
    location=(0, 0, 0.005)
)
floor_inner_border = bpy.context.active_object
floor_inner_border.name = "floor_inner_border"
assign_mat(floor_inner_border, "base")
apply_transforms(floor_inner_border)

# -- Floor ribs (8 radial ribs under floor) --
for i in range(8):
    angle = math.radians(i * 45)
    cx = math.cos(angle) * (FLOOR_RADIUS * 0.45)
    cy = math.sin(angle) * (FLOOR_RADIUS * 0.45)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(cx, cy, -0.2),
        scale=(FLOOR_RADIUS * 0.85, 0.06, 0.06)
    )
    rib = bpy.context.active_object
    rib.name = f"floor_rib_{i+1:02d}"
    rib.rotation_euler = (0, 0, angle)
    assign_mat(rib, "base")
    apply_transforms(rib)

# -- Floor panels (6 sectors) --
for i in range(6):
    angle = math.radians(i * 60 + 30)
    r = FLOOR_RADIUS * 0.55
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=0.03, vertices=16,
        location=(math.cos(angle) * r, math.sin(angle) * r, 0.015)
    )
    panel = bpy.context.active_object
    panel.name = f"floor_panel_{i+1:02d}"
    assign_mat(panel, "base")
    apply_transforms(panel)

# -- Wall panels (base material, partial enclosure along back arc) --
for i in range(10):
    angle = math.radians(150 + i * 24)  # 240-degree arc from +Y opening
    x = math.cos(angle) * (DOME_RADIUS - 0.1)
    y = math.sin(angle) * (DOME_RADIUS - 0.1)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, y, 0.9),
        scale=(0.6, 0.12, 0.9)
    )
    wp = bpy.context.active_object
    wp.name = f"wall_panel_{i+1:02d}"
    wp.rotation_euler = (0, 0, angle)
    assign_mat(wp, "base")
    apply_transforms(wp)

# -- Wall: lower ring (partial cylinder, 270 degrees) --
bpy.ops.mesh.primitive_cylinder_add(
    radius=DOME_RADIUS + 0.05, depth=1.8, vertices=48,
    location=(0, 0, 0.9)
)
wall_ring = bpy.context.active_object
wall_ring.name = "wall_lower_temp"

select_only(wall_ring)
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(wall_ring.data)
bm.verts.ensure_lookup_table()
# Remove 60-degree arc facing +Y (the window opening)
verts_to_remove = [v for v in bm.verts if abs(math.atan2(v.co.x, v.co.y)) < math.radians(30)]
if verts_to_remove:
    bmesh.ops.delete(bm, geom=verts_to_remove, context='VERTS')
# Remove cap faces
faces_to_remove = [f for f in bm.faces if abs(f.normal.z) > 0.9]
if faces_to_remove:
    bmesh.ops.delete(bm, geom=faces_to_remove, context='FACES')
bmesh.update_edit_mesh(wall_ring.data)
bpy.ops.object.mode_set(mode='OBJECT')
wall_ring.name = "wall_lower"
assign_mat(wall_ring, "base")
apply_transforms(wall_ring)

# -- Dome ceiling (hemisphere, glass) --
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=DOME_RADIUS, segments=24, ring_count=12,
    location=(0, 0, 0)
)
dome_ceiling = bpy.context.active_object
dome_ceiling.name = "dome_ceiling"
cut_below_z(dome_ceiling, -0.01)
assign_mat(dome_ceiling, "glass")
apply_transforms(dome_ceiling)

# -- Window wall (glass panel in 60-deg opening) --
bpy.ops.mesh.primitive_cylinder_add(
    radius=DOME_RADIUS + 0.02, depth=2.8, vertices=48,
    location=(0, 0, 1.4)
)
window_wall = bpy.context.active_object
window_wall.name = "window_wall_temp"

select_only(window_wall)
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(window_wall.data)
bm.verts.ensure_lookup_table()
outside = [v for v in bm.verts if abs(math.atan2(v.co.x, v.co.y)) >= math.radians(30)]
if outside:
    bmesh.ops.delete(bm, geom=outside, context='VERTS')
faces_to_remove = [f for f in bm.faces if abs(f.normal.z) > 0.9]
if faces_to_remove:
    bmesh.ops.delete(bm, geom=faces_to_remove, context='FACES')
bmesh.update_edit_mesh(window_wall.data)
bpy.ops.object.mode_set(mode='OBJECT')
window_wall.name = "window_wall"
assign_mat(window_wall, "glass")
apply_transforms(window_wall)

# -- Dome structural ribs (4 meridian arcs, accent) --
for i in range(4):
    angle = math.radians(i * 45 + 22.5)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=DOME_RADIUS - 0.05,
        minor_radius=0.05,
        major_segments=20,
        minor_segments=4,
        location=(0, 0, 0)
    )
    rib = bpy.context.active_object
    rib.name = f"dome_rib_{i+1:02d}"
    rib.rotation_euler = (0, math.radians(90), angle)
    assign_mat(rib, "accent")
    apply_transforms(rib)
    cut_below_z(rib, -0.05)

# -- Dome horizontal ring ribs (detail) --
for idx, (frac, r_factor) in enumerate([(0.35, 0.85), (0.65, 0.60)]):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=DOME_RADIUS * r_factor,
        minor_radius=0.035,
        major_segments=20,
        minor_segments=4,
        location=(0, 0, DOME_HEIGHT * frac)
    )
    ring = bpy.context.active_object
    ring.name = f"dome_inner_ring_{idx+1:02d}"
    assign_mat(ring, "detail")
    apply_transforms(ring)

print("[S11] Room shell complete.")

# ---------------------------------------------------------------------------
# 4. FOCAL ELEMENT -- Breathing Energy Rings (budget-controlled)
# ---------------------------------------------------------------------------
print("[S11] Building focal element (breathing energy rings)...")

# 4 concentric torus rings -- minimal tessellation to stay within 0-5% energy budget
ring_configs = [
    (0.8,  0.04, 0.05, 12, 4),   # inner ring
    (1.4,  0.05, 0.08, 14, 4),
    (2.0,  0.06, 0.12, 16, 4),
    (2.6,  0.07, 0.15, 18, 4),   # outer ring
]

for i, (major_r, minor_r, h, maj_seg, min_seg) in enumerate(ring_configs):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_r,
        minor_radius=minor_r,
        major_segments=maj_seg,
        minor_segments=min_seg,
        location=(0, 0, h)
    )
    ring = bpy.context.active_object
    ring.name = f"breathing_ring_{i+1:02d}"
    assign_mat(ring, "energy")
    apply_transforms(ring)

# Center emitter disc
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.3, depth=0.02, vertices=10,
    location=(0, 0, 0.02)
)
emitter = bpy.context.active_object
emitter.name = "breathing_emitter_disc"
assign_mat(emitter, "energy")
apply_transforms(emitter)

print("[S11] Focal element complete.")

# ---------------------------------------------------------------------------
# 5. PROPS
# ---------------------------------------------------------------------------
print("[S11] Building props...")

# 5a. Yoga mats (12 positions in circle) + glow rings
for i in range(12):
    angle = math.radians(i * 30)
    x = math.cos(angle) * YOGA_CIRCLE_RADIUS
    y = math.sin(angle) * YOGA_CIRCLE_RADIUS

    # Mat body (flat, base material)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.35, depth=0.02, vertices=8,
        location=(x, y, 0.01)
    )
    mat_obj = bpy.context.active_object
    mat_obj.name = f"yoga_mat_{i+1:02d}"
    mat_obj.scale = (1.0, 1.6, 1.0)
    mat_obj.rotation_euler = (0, 0, angle + math.radians(90))
    assign_mat(mat_obj, "base")
    apply_transforms(mat_obj)

    # Glow ring (minimal tessellation for emissive budget)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.45,
        minor_radius=0.012,
        major_segments=8,
        minor_segments=3,
        location=(x, y, 0.005)
    )
    glow = bpy.context.active_object
    glow.name = f"mat_glow_ring_{i+1:02d}"
    assign_mat(glow, "emissive")
    apply_transforms(glow)

# 5b. Water meditation pools (2 at edges)
pool_positions = [(-3.8, -2.5), (3.8, -2.5)]
for i, (px, py) in enumerate(pool_positions):
    # Pool surface
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.2, depth=0.03, vertices=16,
        location=(px, py, -0.01)
    )
    pool = bpy.context.active_object
    pool.name = f"water_pool_{i+1:02d}"
    assign_mat(pool, "glass")
    apply_transforms(pool)

    # Pool rim
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.2,
        minor_radius=0.05,
        major_segments=16,
        minor_segments=4,
        location=(px, py, 0.0)
    )
    rim = bpy.context.active_object
    rim.name = f"pool_rim_{i+1:02d}"
    assign_mat(rim, "detail")
    apply_transforms(rim)

    # Stones in pool (3 per pool, lower than before)
    for j in range(3):
        s_angle = math.radians(j * 120 + 60)
        sx = px + math.cos(s_angle) * 0.6
        sy = py + math.sin(s_angle) * 0.6
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=0.08 + j * 0.02, subdivisions=2,
            location=(sx, sy, 0.02)
        )
        stone = bpy.context.active_object
        stone.name = f"stone_pool{i+1:02d}_{j+1:02d}"
        stone.scale = (1.0, 1.0, 0.5)
        assign_mat(stone, "detail")
        apply_transforms(stone)

# 5c. Floating amber lanterns (4 total)
lantern_positions = [
    (-3.5, -2.2, 1.5), (-4.1, -2.8, 1.3),
    (3.5, -2.2, 1.5),  (4.1, -2.8, 1.3),
]
for i, pos in enumerate(lantern_positions):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.1, segments=6, ring_count=4,
        location=pos
    )
    lantern = bpy.context.active_object
    lantern.name = f"amber_lantern_{i+1:02d}"
    assign_mat(lantern, "emissive")
    apply_transforms(lantern)

# 5d. Mindfulness pods (3 along back wall)
pod_y = -4.5
for i in range(3):
    pod_x = (i - 1) * 2.5
    # Pod body (capsule)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.5, segments=10, ring_count=6,
        location=(pod_x, pod_y, 0.6)
    )
    pod = bpy.context.active_object
    pod.name = f"mindfulness_pod_{i+1:02d}"
    pod.scale = (0.7, 1.5, 0.8)
    assign_mat(pod, "glass")
    apply_transforms(pod)

    # Pod cradle
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.35, depth=0.12, vertices=10,
        location=(pod_x, pod_y, 0.1)
    )
    cradle = bpy.context.active_object
    cradle.name = f"pod_cradle_{i+1:02d}"
    cradle.scale = (0.7, 1.3, 1.0)
    assign_mat(cradle, "detail")
    apply_transforms(cradle)

# 5e. Healing gathering sub-dome at far end (near windowed wall, +Y)
sdc = (0, 3.8, 0)  # subdome center

# Sub-dome frame (accent)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1.8, segments=14, ring_count=7,
    location=sdc
)
subdome = bpy.context.active_object
subdome.name = "healing_subdome"
cut_below_z(subdome, sdc[2] - 0.05)
assign_mat(subdome, "accent")
apply_transforms(subdome)

# Sub-dome interior holo surface
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1.6, segments=14, ring_count=7,
    location=sdc
)
subdome_holo = bpy.context.active_object
subdome_holo.name = "healing_subdome_holo"
cut_below_z(subdome_holo, sdc[2] - 0.05)
assign_mat(subdome_holo, "holo")
apply_transforms(subdome_holo)

# Sub-dome base ring
bpy.ops.mesh.primitive_torus_add(
    major_radius=1.8,
    minor_radius=0.05,
    major_segments=14,
    minor_segments=4,
    location=(sdc[0], sdc[1], 0.0)
)
subdome_ring = bpy.context.active_object
subdome_ring.name = "healing_subdome_ring"
assign_mat(subdome_ring, "accent")
apply_transforms(subdome_ring)

# Sub-dome structural ribs (3)
for i in range(3):
    angle = math.radians(i * 60 + 30)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.75,
        minor_radius=0.025,
        major_segments=14,
        minor_segments=4,
        location=sdc
    )
    srib = bpy.context.active_object
    srib.name = f"subdome_rib_{i+1:02d}"
    srib.rotation_euler = (0, math.radians(90), angle)
    assign_mat(srib, "accent")
    apply_transforms(srib)
    cut_below_z(srib, -0.05)

# 5f. Floor path markers (6 radial lines toward center, detail)
for i in range(6):
    angle = math.radians(i * 60)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(math.cos(angle) * 1.5, math.sin(angle) * 1.5, 0.005),
        scale=(YOGA_CIRCLE_RADIUS - 0.5, 0.025, 0.004)
    )
    path = bpy.context.active_object
    path.name = f"floor_path_{i+1:02d}"
    path.rotation_euler = (0, 0, angle)
    assign_mat(path, "detail")
    apply_transforms(path)

# 5g. Additional base geometry to hit 50%+ target

# Yoga circle outer ring (marks the practice area boundary)
bpy.ops.mesh.primitive_torus_add(
    major_radius=YOGA_CIRCLE_RADIUS + 0.5,
    minor_radius=0.06,
    major_segments=36,
    minor_segments=4,
    location=(0, 0, 0.005)
)
circle_ring = bpy.context.active_object
circle_ring.name = "yoga_circle_ring"
assign_mat(circle_ring, "base")
apply_transforms(circle_ring)

# Platform edge lip
bpy.ops.mesh.primitive_torus_add(
    major_radius=FLOOR_RADIUS,
    minor_radius=0.12,
    major_segments=48,
    minor_segments=6,
    location=(0, 0, 0.0)
)
edge_lip = bpy.context.active_object
edge_lip.name = "floor_edge_lip"
assign_mat(edge_lip, "base")
apply_transforms(edge_lip)

# Additional floor sector panels (inner ring, 4 more)
for i in range(4):
    angle = math.radians(i * 90 + 45)
    r = FLOOR_RADIUS * 0.35
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.7, depth=0.025, vertices=12,
        location=(math.cos(angle) * r, math.sin(angle) * r, 0.012)
    )
    sp = bpy.context.active_object
    sp.name = f"floor_sector_{i+1:02d}"
    assign_mat(sp, "base")
    apply_transforms(sp)

# Meditation alcove benches (base, along walls, 4 small benches)
bench_angles = [math.radians(a) for a in [200, 240, 280, 320]]
for i, ba in enumerate(bench_angles):
    bx = math.cos(ba) * (DOME_RADIUS - 0.8)
    by = math.sin(ba) * (DOME_RADIUS - 0.8)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(bx, by, 0.2),
        scale=(0.8, 0.3, 0.2)
    )
    bench = bpy.context.active_object
    bench.name = f"meditation_bench_{i+1:02d}"
    bench.rotation_euler = (0, 0, ba)
    assign_mat(bench, "base")
    apply_transforms(bench)

# 5h. Additional base geometry for 50%+ target

# Wall base molding (thick torus along wall base, follows wall arc)
bpy.ops.mesh.primitive_torus_add(
    major_radius=DOME_RADIUS + 0.05,
    minor_radius=0.1,
    major_segments=48,
    minor_segments=6,
    location=(0, 0, 0.0)
)
wall_molding = bpy.context.active_object
wall_molding.name = "wall_base_molding"
# Cut the window opening section
select_only(wall_molding)
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(wall_molding.data)
bm.verts.ensure_lookup_table()
window_verts = [v for v in bm.verts if abs(math.atan2(v.co.x, v.co.y)) < math.radians(35)]
if window_verts:
    bmesh.ops.delete(bm, geom=window_verts, context='VERTS')
bmesh.update_edit_mesh(wall_molding.data)
bpy.ops.object.mode_set(mode='OBJECT')
assign_mat(wall_molding, "base")
apply_transforms(wall_molding)

# Mid-height wall band (structural horizontal ring on walls)
bpy.ops.mesh.primitive_torus_add(
    major_radius=DOME_RADIUS + 0.03,
    minor_radius=0.06,
    major_segments=48,
    minor_segments=4,
    location=(0, 0, 1.0)
)
wall_band = bpy.context.active_object
wall_band.name = "wall_mid_band"
select_only(wall_band)
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(wall_band.data)
bm.verts.ensure_lookup_table()
window_verts = [v for v in bm.verts if abs(math.atan2(v.co.x, v.co.y)) < math.radians(35)]
if window_verts:
    bmesh.ops.delete(bm, geom=window_verts, context='VERTS')
bmesh.update_edit_mesh(wall_band.data)
bpy.ops.object.mode_set(mode='OBJECT')
assign_mat(wall_band, "base")
apply_transforms(wall_band)

# Floor center platform (raised circular area under yoga circle)
bpy.ops.mesh.primitive_cylinder_add(
    radius=YOGA_CIRCLE_RADIUS + 0.8, depth=0.04, vertices=48,
    location=(0, 0, -0.005)
)
center_platform = bpy.context.active_object
center_platform.name = "center_platform"
assign_mat(center_platform, "base")
apply_transforms(center_platform)

# Transition steps (2 rings between center platform and floor edge)
for idx, r in enumerate([YOGA_CIRCLE_RADIUS + 1.2, YOGA_CIRCLE_RADIUS + 1.8]):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=r,
        minor_radius=0.04,
        major_segments=36,
        minor_segments=4,
        location=(0, 0, -0.005 - idx * 0.015)
    )
    step = bpy.context.active_object
    step.name = f"floor_step_ring_{idx+1:02d}"
    assign_mat(step, "base")
    apply_transforms(step)

print("[S11] All props complete.")

# ---------------------------------------------------------------------------
# 6. EMPTIES
# ---------------------------------------------------------------------------
print("[S11] Placing empties...")

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, DOME_HEIGHT - 0.3))
bpy.context.active_object.name = "light_0"

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(-3.8, -2.5, 2.0))
bpy.context.active_object.name = "light_1"

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 3.8, 1.2))
bpy.context.active_object.name = "light_2"

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0.6))
bpy.context.active_object.name = "camera_target"

print("[S11] Empties placed: light_0, light_1, light_2, camera_target")

# ---------------------------------------------------------------------------
# 7. MATERIAL AUDIT
# ---------------------------------------------------------------------------
print("[S11] Running material audit...")

mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
valid_slots = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
audit_errors = []

for obj in mesh_objects:
    if not obj.data.materials:
        audit_errors.append(f"  NO MATERIAL: {obj.name}")
    else:
        mat_name = obj.data.materials[0].name if obj.data.materials[0] else "None"
        if mat_name not in valid_slots:
            audit_errors.append(f"  INVALID MATERIAL '{mat_name}' on {obj.name}")

if audit_errors:
    print("[S11] MATERIAL AUDIT FAILURES:")
    for e in audit_errors:
        print(e)
else:
    print("[S11] Material audit PASSED -- all objects have valid 7-slot materials.")

# ---------------------------------------------------------------------------
# 8. TRI COUNT + MATERIAL DISTRIBUTION
# ---------------------------------------------------------------------------

# Apply all transforms first
print("\n[S11] Applying all transforms...")
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        select_only(obj)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

print("\n[S11] Triangle count report:")

slot_tris = {s: 0 for s in valid_slots}
object_report = []
total_tris = 0

for obj in sorted(mesh_objects, key=lambda o: o.name):
    tc = get_tri_count(obj)
    total_tris += tc
    mat_name = obj.data.materials[0].name if obj.data.materials and obj.data.materials[0] else "unknown"
    slot_tris[mat_name] = slot_tris.get(mat_name, 0) + tc
    object_report.append((obj.name, tc, mat_name))

print(f"\n  Total mesh objects: {len(mesh_objects)}")
print(f"  Total triangles: {total_tris}")
print(f"  Budget: 5K-10K tris")
in_budget = 5000 <= total_tris <= 10000
print(f"  Status: {'PASS' if in_budget else 'NEEDS ADJUSTMENT'}")

print("\n  Material distribution:")
for slot in ["base", "detail", "glass", "accent", "energy", "emissive", "holo"]:
    count = slot_tris.get(slot, 0)
    pct = (count / total_tris * 100) if total_tris > 0 else 0
    print(f"    {slot:10s}: {count:5d} tris ({pct:5.1f}%)")

print("\n  Per-object breakdown (sorted by tris desc):")
for name, tc, mat in sorted(object_report, key=lambda x: -x[1]):
    print(f"    {name:35s} {tc:5d} tris  [{mat}]")

# ---------------------------------------------------------------------------
# 9. DECIMATION IF NEEDED
# ---------------------------------------------------------------------------
if total_tris > 10000:
    print(f"\n[S11] Over budget ({total_tris} > 10000). Applying decimation...")
    for obj in mesh_objects:
        tc = get_tri_count(obj)
        if "breathing_ring" in obj.name:
            continue  # preserve focal element
        if tc > 120:
            ratio = max(0.5, 100.0 / tc)
            select_only(obj)
            mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
            mod.ratio = ratio
            bpy.ops.object.modifier_apply(modifier="Decimate")
    total_after = sum(get_tri_count(obj) for obj in mesh_objects)
    print(f"[S11] Tri count after decimation: {total_after}")
    total_tris = total_after

# ---------------------------------------------------------------------------
# 10. SAVE + EXPORT
# ---------------------------------------------------------------------------
print(f"\n[S11] Saving .blend to: {BLEND_PATH}")
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)

print(f"[S11] Exporting GLB to: {GLB_PATH}")

# Hide lights/camera, select only mesh + empties
for obj in bpy.data.objects:
    if obj.type in ('LIGHT', 'CAMERA'):
        obj.select_set(False)
        obj.hide_set(True)
    else:
        obj.select_set(True)

# Determine available export parameters for this Blender version
export_kwargs = {
    'filepath': GLB_PATH,
    'export_format': 'GLB',
    'use_selection': True,
    'export_draco_mesh_compression_enable': True,
    'export_draco_mesh_compression_level': 6,
    'export_cameras': False,
    'export_lights': False,
    'export_yup': True,
}
try:
    bpy.ops.export_scene.gltf(**export_kwargs)
except TypeError as e:
    # Fall back: remove unrecognized kwargs one at a time
    print(f"[S11] Export retry due to: {e}")
    # Try minimal set
    bpy.ops.export_scene.gltf(
        filepath=GLB_PATH,
        export_format='GLB',
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_cameras=False,
        export_lights=False,
    )

# Verify empties in export
empty_names = sorted([obj.name for obj in bpy.data.objects if obj.type == 'EMPTY'])

print(f"\n[S11] === SESSION 11 SUMMARY ===")
print(f"  Mesh objects: {len(mesh_objects)}")
print(f"  Empties exported: {empty_names}")
print(f"  Total tris: {total_tris}")
print(f"  .blend: {BLEND_PATH}")
print(f"  .glb: {GLB_PATH}")
print(f"  Material slots: {sorted(materials.keys())}")
print(f"[S11] === DONE ===")

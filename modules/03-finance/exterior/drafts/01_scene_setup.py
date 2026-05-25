"""
Finance Tower (Module #03) — Scene Setup
Step 1: Clear scene, set up lighting rig and material library.
"""
import bpy
import math

# ============================================================
# STEP 1: Clear the entire scene
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Remove orphan data
for block in bpy.data.meshes:
    if not block.users:
        bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    if not block.users:
        bpy.data.materials.remove(block)
for block in bpy.data.cameras:
    if not block.users:
        bpy.data.cameras.remove(block)
for block in bpy.data.lights:
    if not block.users:
        bpy.data.lights.remove(block)

print(f"Scene cleared. Objects remaining: {len(bpy.data.objects)}")

# ============================================================
# STEP 2: Lighting Rig (from shared/lighting-rig.py)
# ============================================================
# World background: #0A0A0F
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)  # #0A0A0F
    bg_node.inputs["Strength"].default_value = 1.0

# Key Light — Sun
key_data = bpy.data.lights.new(name="Key_Light", type='SUN')
key_data.color = (1.0, 0.894, 0.8)  # #FFE4CC warm
key_data.energy = 0.8
key_data.use_shadow = True
key_data.shadow_soft_size = 0.5
key_obj = bpy.data.objects.new("Key_Light", key_data)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (-8, 20, -6)
key_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

# Rim Light — Spot (Burnt Orange)
rim_data = bpy.data.lights.new(name="Rim_Light", type='SPOT')
rim_data.color = (1.0, 0.369, 0.0)  # #FF5E00
rim_data.energy = 200
rim_data.spot_size = math.radians(45)
rim_data.spot_blend = 0.9
rim_data.use_shadow = True
rim_obj = bpy.data.objects.new("Rim_Light", rim_data)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (10, 18, -14)
from mathutils import Vector
direction = Vector((0, 0, -3)) - Vector((10, 18, -14))
rim_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# Fill Light — Area (cool ambient)
fill_data = bpy.data.lights.new(name="Fill_Light", type='AREA')
fill_data.color = (0.102, 0.102, 0.251)  # #1a1a40
fill_data.energy = 50
fill_data.size = 20
fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (5, 15, 10)
fill_obj.rotation_euler = (math.radians(60), 0, 0)

# Camera
cam_data = bpy.data.cameras.new(name="Overview_Camera")
cam_data.lens_unit = 'FOV'
cam_data.angle = math.radians(45)
cam_data.clip_start = 0.1
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Overview_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (0, 25, 18)
target = Vector((0, -2, -1))
cam_dir = target - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam_obj

# Render engine
try:
    engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'ShaderNodeEeveeSpecular') else 'BLENDER_EEVEE'
    bpy.context.scene.render.engine = engine
except Exception:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# EEVEE settings
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

print("Lighting rig loaded: 3 lights + camera.")

# ============================================================
# STEP 3: Material Library (from shared/material-library.py)
# District color: #F59E0B (Rich Gold), energy=True, holo=False
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
DISTRICT_COLOR = hex_to_linear("#F59E0B")

def _make_material(name, base_color, roughness, metallic, emission_color=None, emission_strength=0.0, alpha=1.0):
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

materials = {}
materials["base"] = _make_material("base", BASE_COLOR, 0.80, 0.05)
materials["accent"] = _make_material("accent", ACCENT_INACTIVE, 0.55, 0.16,
                                      emission_color=DISTRICT_COLOR, emission_strength=0.24)
materials["glass"] = _make_material("glass", GLASS_COLOR, 0.10, 0.30,
                                     emission_color=hex_to_linear("#FEF3C7"), emission_strength=0.08, alpha=0.86)
materials["detail"] = _make_material("detail", DETAIL_COLOR, 0.60, 0.15)
materials["emissive"] = _make_material("emissive", DETAIL_COLOR, 0.22, 0.00,
                                        emission_color=DISTRICT_COLOR, emission_strength=0.06)
materials["energy"] = _make_material("energy", DETAIL_COLOR, 0.15, 0.10,
                                      emission_color=ENERGY_ORANGE, emission_strength=0.10)

print(f"Materials created: {list(materials.keys())} ({len(materials)} total)")

# ============================================================
# VERIFICATION
# ============================================================
light_count = sum(1 for obj in bpy.data.objects if obj.type == 'LIGHT')
mat_count = len([m for m in bpy.data.materials if m.name in ['base','accent','glass','detail','emissive','energy']])
print(f"Verification: {light_count} lights, {mat_count} materials")
print(f"World background set to #0A0A0F: {bg_node.inputs['Color'].default_value[0]:.4f}")
print("Scene setup complete.")

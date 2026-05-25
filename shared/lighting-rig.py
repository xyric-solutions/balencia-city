"""
Balencia City v3 — Viewport Lighting Rig
Run in Blender at the start of every building session.
Matches the R3F app's cinematic aesthetic: ink-blue zenith to warm amber horizon.
"""
import bpy
import math


def setup_viewport_lighting():
    """Configure Blender scene to match Balencia City v3 dark premium aesthetic."""

    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("BalenciaWorld")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)  # #0A0A0F
        bg_node.inputs["Strength"].default_value = 1.0

    key_data = bpy.data.lights.new(name="Key_Light", type='SUN')
    key_data.color = (1.0, 0.894, 0.8)  # #FFE4CC warm
    key_data.energy = 0.8
    key_data.use_shadow = True
    key_data.shadow_soft_size = 0.5
    key_obj = bpy.data.objects.new("Key_Light", key_data)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (-8, 20, -6)
    key_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

    rim_data = bpy.data.lights.new(name="Rim_Light", type='SPOT')
    rim_data.color = (1.0, 0.369, 0.0)  # #FF5E00 Burnt Orange (brand primary)
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

    fill_data = bpy.data.lights.new(name="Fill_Light", type='AREA')
    fill_data.color = (0.102, 0.102, 0.251)  # #1a1a40 cool ambient
    fill_data.energy = 50
    fill_data.size = 20
    fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (5, 15, 10)
    fill_obj.rotation_euler = (math.radians(60), 0, 0)

    cam_data = bpy.data.cameras.new(name="Overview_Camera")
    cam_data.lens_unit = 'FOV'
    cam_data.angle = math.radians(45)
    cam_data.clip_start = 0.1
    cam_data.clip_end = 200
    cam_obj = bpy.data.objects.new("Overview_Camera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = (0, 25, 18)

    from mathutils import Vector as V
    target = V((0, -2, -1))
    direction = target - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    bpy.context.scene.camera = cam_obj

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

    print("Balencia v3 viewport lighting rig loaded.")


def clear_lighting():
    """Remove all lights and cameras added by this rig."""
    names = ["Key_Light", "Rim_Light", "Fill_Light", "Overview_Camera"]
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)


if __name__ == "__main__":
    clear_lighting()
    setup_viewport_lighting()

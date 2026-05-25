"""
Balencia City v3 — Interior Lighting Rig
Run in Blender for interior preview renders. NOT exported to GLB.

Designed to illuminate enclosed cylindrical interiors where the exterior
rig's lights can't penetrate. Adds:
- Key point light at the focal point (city model / hero element)
- Fill area light near ceiling pointing down
- Wall-wash point lights to reveal cylindrical walls
- Ground-level accent spots for corridor/entrance illumination

Materials also get boosted emissions for preview (inactive-to-preview values).
The R3F runtime overrides all material properties, so preview values don't
affect production.

Usage:
    import interior_lighting_rig
    interior_lighting_rig.setup_interior_lighting(
        focal_point=(0, 0, 19.2),
        floor_z=4.0,
        ceiling_z=42.0,
        radius=3.0,
    )
"""
import bpy
import math
from mathutils import Vector


def clear_interior_lighting():
    """Remove all interior preview lights."""
    prefixes = ["Interior_", "Wall_Wash_", "Mid_Fill", "Corridor_Light"]
    for obj in list(bpy.data.objects):
        if obj.type == 'LIGHT' and any(obj.name.startswith(p) for p in prefixes):
            bpy.data.objects.remove(obj, do_unlink=True)


def setup_interior_lighting(focal_point=(0, 0, 19.2), floor_z=4.0, ceiling_z=42.0, radius=3.0):
    """
    Set up interior-specific preview lighting for a cylindrical atrium.

    Args:
        focal_point: (x, y, z) of the hero element / room focal point
        floor_z: Z height of the floor
        ceiling_z: Z height of the ceiling
        radius: Radius of the cylindrical room
    """
    clear_interior_lighting()

    fx, fy, fz = focal_point
    room_height = ceiling_z - floor_z

    # Key light at focal point — illuminates the hero element
    key_data = bpy.data.lights.new(name="Interior_Key", type='POINT')
    key_data.color = (1.0, 0.85, 0.65)
    key_data.energy = 1500
    key_data.shadow_soft_size = 2.0
    key_data.use_shadow = True
    key_obj = bpy.data.objects.new("Interior_Key", key_data)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (fx, fy, fz)

    # Fill light near ceiling — soft downward illumination
    fill_data = bpy.data.lights.new(name="Interior_Fill", type='AREA')
    fill_data.color = (0.7, 0.75, 0.9)
    fill_data.energy = 200
    fill_data.size = radius * 1.5
    fill_obj = bpy.data.objects.new("Interior_Fill", fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (fx, fy, ceiling_z - room_height * 0.1)
    fill_obj.rotation_euler = (math.radians(180), 0, 0)

    # Mid-height fill
    mid_data = bpy.data.lights.new(name="Mid_Fill", type='AREA')
    mid_data.color = (0.8, 0.65, 0.45)
    mid_data.energy = 100
    mid_data.size = radius
    mid_obj = bpy.data.objects.new("Mid_Fill", mid_data)
    bpy.context.collection.objects.link(mid_obj)
    mid_obj.location = (fx, fy, floor_z + room_height * 0.2)
    mid_obj.rotation_euler = (math.radians(180), 0, 0)

    # Wall-wash lights — 2 point lights near the walls
    wall_r = radius * 0.67
    for i, angle in enumerate([math.radians(90), math.radians(270)]):
        wash_data = bpy.data.lights.new(name=f"Wall_Wash_{i}", type='POINT')
        wash_data.color = (0.9, 0.75, 0.55)
        wash_data.energy = 200
        wash_data.shadow_soft_size = 3.0
        wash_obj = bpy.data.objects.new(f"Wall_Wash_{i}", wash_data)
        bpy.context.collection.objects.link(wash_obj)
        wash_obj.location = (math.cos(angle) * wall_r, math.sin(angle) * wall_r, fz)

    # Ground-level accent spots (pointing upward)
    accent_data = bpy.data.lights.new(name="Interior_Accent", type='SPOT')
    accent_data.color = (1.0, 0.369, 0.0)
    accent_data.energy = 400
    accent_data.spot_size = math.radians(90)
    accent_data.spot_blend = 0.8
    accent_data.use_shadow = True
    accent_obj = bpy.data.objects.new("Interior_Accent", accent_data)
    bpy.context.collection.objects.link(accent_obj)
    accent_obj.location = (0, -radius * 0.67, floor_z + 0.5)
    accent_obj.rotation_euler = (math.radians(-90), 0, 0)

    accent2_data = bpy.data.lights.new(name="Interior_Accent_2", type='SPOT')
    accent2_data.color = (1.0, 0.5, 0.2)
    accent2_data.energy = 100
    accent2_data.spot_size = math.radians(70)
    accent2_data.spot_blend = 0.9
    accent2_obj = bpy.data.objects.new("Interior_Accent_2", accent2_data)
    bpy.context.collection.objects.link(accent2_obj)
    accent2_obj.location = (radius * 0.5, radius * 0.5, floor_z + 0.5)
    accent2_obj.rotation_euler = (math.radians(-80), 0, 0)

    print(f"Interior lighting rig loaded (focal={focal_point}, floor={floor_z}, ceiling={ceiling_z}, r={radius})")


def boost_emissions_for_preview():
    """
    Boost material emissions from inactive to preview values.
    Preview values sit between inactive (production default) and active (scroll-focused).
    Safe to apply — the R3F runtime overrides all material properties by slot name.
    """
    preview = {
        'base': 0.03,
        'detail': 0.04,
        'emissive': 0.25,
        'holo': 0.50,
        'glass': 0.15,
        'accent': 0.30,
        'energy': 0.15,
    }

    emission_colors = {
        'base': (0.04, 0.03, 0.025, 1.0),
        'detail': (0.15, 0.08, 0.02, 1.0),
    }

    for mat in bpy.data.materials:
        if mat.use_nodes and mat.name in preview:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                if mat.name in emission_colors:
                    bsdf.inputs["Emission Color"].default_value = emission_colors[mat.name]
                bsdf.inputs["Emission Strength"].default_value = preview[mat.name]

    print("Emissions boosted to preview values")


if __name__ == "__main__":
    clear_interior_lighting()
    setup_interior_lighting()
    boost_emissions_for_preview()

"""
Balencia City v3 — Energy Pipeline Utilities
Helpers for generating arced tube geometry connecting SIA Tower to districts.

Usage:
    import energy_pipeline_utils as epu
    epu.create_pipeline(
        start=(0, 0, 30),      # SIA Tower crown
        end=(-15, 0, 8),       # District connection point
        arc_height=40,          # Peak height of arc
        tube_radius=0.08,
        segments=64,
        name="pipeline_fitness"
    )
"""
import bpy
import math
from mathutils import Vector


def create_arc_curve(start, end, arc_height, segments=64, name="pipeline_curve"):
    """Create a bezier curve following an arc from start to end."""
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = segments

    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(1)  # 2 points total

    p0 = spline.bezier_points[0]
    p1 = spline.bezier_points[1]

    p0.co = Vector(start)
    p1.co = Vector(end)

    mid = (Vector(start) + Vector(end)) / 2
    mid.z = arc_height

    p0.handle_right_type = 'FREE'
    p0.handle_right = mid + (Vector(start) - mid) * 0.3
    p0.handle_right.z = arc_height * 0.7

    p1.handle_left_type = 'FREE'
    p1.handle_left = mid + (Vector(end) - mid) * 0.3
    p1.handle_left.z = arc_height * 0.7

    curve_obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(curve_obj)
    return curve_obj


def create_pipeline(start, end, arc_height=40, tube_radius=0.08, segments=64, name="pipeline"):
    """
    Create a complete energy pipeline tube from SIA Tower to a district.
    Returns the mesh object ready for material assignment.
    """
    curve_obj = create_arc_curve(start, end, arc_height, segments, f"{name}_curve")

    curve_obj.data.bevel_depth = tube_radius
    curve_obj.data.bevel_resolution = 4
    curve_obj.data.use_fill_caps = True

    bpy.context.view_layer.objects.active = curve_obj
    curve_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')

    curve_obj.name = name

    return curve_obj


def create_ground_veins(center, radius=3.0, vein_count=8, name="ground_veins"):
    """
    Create ground-level energy veins radiating from a pipeline endpoint.
    Flat geometry at Y=0.05 (just above ground).
    """
    veins = []
    for i in range(vein_count):
        angle = (2 * math.pi * i) / vein_count
        end_x = center[0] + radius * math.cos(angle)
        end_y = center[1] + radius * math.sin(angle)

        curve_data = bpy.data.curves.new(f"{name}_{i}", type='CURVE')
        curve_data.dimensions = '3D'
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(1)

        p0 = spline.bezier_points[0]
        p1 = spline.bezier_points[1]
        p0.co = Vector((center[0], center[1], 0.05))
        p1.co = Vector((end_x, end_y, 0.05))

        curve_data.bevel_depth = 0.02
        curve_data.bevel_resolution = 2

        vein_obj = bpy.data.objects.new(f"{name}_{i}", curve_data)
        bpy.context.collection.objects.link(vein_obj)

        bpy.context.view_layer.objects.active = vein_obj
        vein_obj.select_set(True)
        bpy.ops.object.convert(target='MESH')

        veins.append(vein_obj)

    return veins

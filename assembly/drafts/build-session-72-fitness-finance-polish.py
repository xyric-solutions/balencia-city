"""
Balencia City v3 - Session 72
Phase 8.4 Fitness + Finance exterior polish wave.

This script upgrades the already-approved Fitness and Finance exterior GLBs
without changing district origins, layout positions, or baked energy routes.
"""

import json
import math
import os
import shutil
from collections import defaultdict
from datetime import date

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Desktop/balencia-city-v3"
ASSEMBLY_AUDIT = os.path.join(ROOT, "assembly/audit")
ASSEMBLY_SCREENSHOTS = os.path.join(ROOT, "assembly/screenshots")
ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}

MODULES = [
    {
        "id": "fitness",
        "label": "Fitness",
        "root_name": "fitness-ext",
        "accent_hex": "#34A853",
        "source_blend": "modules/01-fitness/exterior/drafts/fitness-session07.blend",
        "output_blend": "modules/01-fitness/exterior/drafts/fitness-session72-v2-polish.blend",
        "draft_glb": "modules/01-fitness/exterior/drafts/fitness-ext-v2-draft-s72.glb",
        "approved_glb": "modules/01-fitness/exterior/approved/fitness-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/01-fitness/fitness-ext.glb",
        "metrics": "modules/01-fitness/exterior/drafts/session72-v2-metrics.json",
        "qa_import": "modules/01-fitness/exterior/drafts/session72-qa-import.json",
        "screenshots": "modules/01-fitness/screenshots",
        "tri_min": 12000,
        "tri_max": 18000,
        "size_min_kb": 100,
        "size_max_kb": 350,
    },
    {
        "id": "finance",
        "label": "Finance",
        "root_name": "finance-ext",
        "accent_hex": "#F59E0B",
        "source_blend": "modules/03-finance/exterior/drafts/finance-exterior-s14.blend",
        "output_blend": "modules/03-finance/exterior/drafts/finance-session72-v2-polish.blend",
        "draft_glb": "modules/03-finance/exterior/drafts/finance-ext-v2-draft-s72.glb",
        "approved_glb": "modules/03-finance/exterior/approved/finance-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/03-finance/finance-ext.glb",
        "metrics": "modules/03-finance/exterior/drafts/session72-v2-metrics.json",
        "qa_import": "modules/03-finance/exterior/drafts/session72-qa-import.json",
        "screenshots": "modules/03-finance/screenshots",
        "tri_min": 12000,
        "tri_max": 18000,
        "size_min_kb": 100,
        "size_max_kb": 350,
    },
]

EXTERIOR_MODULES = [
    ("SIA Tower", "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb", "sia-tower"),
    ("Fitness", "modules/01-fitness/exterior/approved/fitness-ext.glb", "fitness"),
    ("Yoga & Wellbeing", "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb", "yoga"),
    ("Finance", "modules/03-finance/exterior/approved/finance-ext.glb", "finance"),
    ("Knowledgebase", "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb", "knowledgebase"),
    ("Chat & Communication", "modules/05-chat-communication/exterior/approved/chat-ext.glb", "chat"),
    ("Leaderboard", "modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb", "leaderboard"),
    ("Relationships", "modules/07-relationships/exterior/approved/relationships-ext.glb", "relationships"),
    ("Career", "modules/08-career/exterior/approved/career-ext.glb", "career"),
    ("Recovery & Sleep", "modules/09-recovery-sleep/exterior/approved/recovery-ext.glb", "recovery"),
    ("AI Analytics", "modules/10-ai-analytics/exterior/approved/analytics-ext.glb", "analytics"),
    ("Nutrition", "modules/11-nutrition/exterior/approved/nutrition-ext.glb", "nutrition"),
]

for module in MODULES:
    for key in ("output_blend", "draft_glb", "approved_glb", "app_glb", "metrics", "qa_import"):
        os.makedirs(os.path.dirname(os.path.join(ROOT, module[key])), exist_ok=True)
    os.makedirs(os.path.join(ROOT, module["screenshots"]), exist_ok=True)
for path in (ASSEMBLY_AUDIT, ASSEMBLY_SCREENSHOTS):
    os.makedirs(path, exist_ok=True)

created_categories = {}


def rel(path):
    return os.path.relpath(path, ROOT)


def material_base_name(material):
    return material.name.split(".")[0] if material else ""


def mesh_objects():
    return [obj for obj in bpy.data.objects if obj.type == "MESH"]


def count_tris(objects=None):
    total = 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in objects or mesh_objects():
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        mesh.calc_loop_triangles()
        total += len(mesh.loop_triangles)
        eval_obj.to_mesh_clear()
    return total


def world_bbox(objects=None):
    points = []
    for obj in objects or mesh_objects():
        for corner in obj.bound_box:
            points.append(obj.matrix_world @ Vector(corner))
    if not points:
        return {"min": [0, 0, 0], "max": [0, 0, 0], "size": [0, 0, 0], "center": [0, 0, 0]}
    mins = [min(point[i] for point in points) for i in range(3)]
    maxs = [max(point[i] for point in points) for i in range(3)]
    size = [maxs[i] - mins[i] for i in range(3)]
    center = [(mins[i] + maxs[i]) / 2 for i in range(3)]
    return {
        "min": [round(value, 4) for value in mins],
        "max": [round(value, 4) for value in maxs],
        "size": [round(value, 4) for value in size],
        "center": [round(value, 4) for value in center],
    }


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for collection in list(bpy.data.collections):
        if not collection.users:
            bpy.data.collections.remove(collection)
    for mesh in list(bpy.data.meshes):
        if not mesh.users:
            bpy.data.meshes.remove(mesh)
    for material in list(bpy.data.materials):
        if not material.users:
            bpy.data.materials.remove(material)


def current_object():
    obj = bpy.context.view_layer.objects.active
    if obj is not None:
        return obj
    selected = bpy.context.selected_objects
    if selected:
        return selected[-1]
    raise RuntimeError("No active object after primitive creation")


def assign(obj, material):
    obj.data.materials.clear()
    obj.data.materials.append(material)
    return obj


def shade_smooth(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def apply_transform(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    return obj


def register(obj, category):
    created_categories[obj.name] = category
    return obj


def hex_to_linear(hex_color):
    hex_color = hex_color.lstrip("#")
    rgb = [int(hex_color[index:index + 2], 16) / 255.0 for index in (0, 2, 4)]

    def convert(channel):
        if channel <= 0.04045:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    return tuple(convert(channel) for channel in rgb) + (1.0,)


def ensure_material(name, base, emission=None, strength=0.0, alpha=1.0, roughness=0.6, metallic=0.1):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.name = name
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = base
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if emission:
            bsdf.inputs["Emission Color"].default_value = emission
            bsdf.inputs["Emission Strength"].default_value = strength
        if alpha < 1.0:
            bsdf.inputs["Alpha"].default_value = alpha
            mat.blend_method = "BLEND"
            mat.use_screen_refraction = True
    return mat


def normalize_materials(accent_hex):
    accent = hex_to_linear(accent_hex)
    orange = hex_to_linear("#FF5E00")
    material_defs = {
        "base": ((0.012, 0.013, 0.018, 1.0), None, 0.0, 1.0, 0.82, 0.06),
        "accent": ((0.024, 0.027, 0.022, 1.0), accent, 0.14, 1.0, 0.48, 0.22),
        "glass": ((0.006, 0.009, 0.014, 1.0), accent, 0.025, 0.82, 0.16, 0.18),
        "detail": ((0.008, 0.009, 0.012, 1.0), None, 0.0, 1.0, 0.56, 0.30),
        "emissive": ((0.018, 0.018, 0.012, 1.0), accent, 0.28, 1.0, 0.24, 0.0),
        "energy": ((0.045, 0.018, 0.004, 1.0), orange, 0.24, 1.0, 0.20, 0.04),
        "holo": ((0.018, 0.024, 0.020, 1.0), accent, 0.22, 0.42, 0.18, 0.02),
    }
    mats = {name: ensure_material(name, *args) for name, args in material_defs.items()}
    fallback = mats["detail"]
    for obj in mesh_objects():
        if not obj.data.materials:
            obj.data.materials.append(fallback)
        for index, material in enumerate(obj.data.materials):
            base = material_base_name(material)
            obj.data.materials[index] = mats[base] if base in mats else fallback
    return mats


def box(name, loc, dims, material, category, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    obj.scale = dims
    assign(obj, material)
    apply_transform(obj)
    return register(obj, category)


def cylinder(name, loc, radius, depth, material, category, vertices=8, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, material)
    shade_smooth(obj)
    apply_transform(obj)
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, material, category, vertices=8, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    assign(obj, material)
    shade_smooth(obj)
    apply_transform(obj)
    return register(obj, category)


def torus(name, loc, major, minor, material, category, seg=32, minor_seg=6, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=seg,
        minor_segments=minor_seg,
        major_radius=major,
        minor_radius=minor,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    assign(obj, material)
    shade_smooth(obj)
    apply_transform(obj)
    return register(obj, category)


def cylinder_between(name, start, end, radius, material, category, vertices=6):
    start = Vector(start)
    end = Vector(end)
    direction = end - start
    length = direction.length
    if length <= 0.001:
        return None
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=(start + end) / 2)
    obj = current_object()
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign(obj, material)
    shade_smooth(obj)
    apply_transform(obj)
    return register(obj, category)


def add_fitness_polish(mats, bbox):
    category = "session72 fitness facade bands, windows, and muscular frame"
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    front_y = min_y - 0.08
    back_y = max_y + 0.08
    left_x = min_x - 0.08
    right_x = max_x + 0.08
    body_bottom = min_z + max(0.85, height * 0.08)
    body_top = max_z - max(0.8, height * 0.09)

    for level in range(30):
        z = body_bottom + (body_top - body_bottom) * (level / 29)
        band_name = f"Fitness_v2_floor_edge_band_{level + 1:02d}"
        box(f"{band_name}_front", (cx, front_y, z), (width * 0.48, 0.045, 0.035), mats["emissive"], category)
        box(f"{band_name}_back", (cx, back_y, z), (width * 0.48, 0.045, 0.035), mats["emissive"], category)
        box(f"{band_name}_left", (left_x, cy, z), (0.045, depth * 0.48, 0.035), mats["emissive"], category)
        box(f"{band_name}_right", (right_x, cy, z), (0.045, depth * 0.48, 0.035), mats["emissive"], category)

    row_count = 8
    front_cols = [-0.34, -0.17, 0.0, 0.17, 0.34]
    side_cols = [-0.28, -0.09, 0.09, 0.28]
    for row in range(row_count):
        z = body_bottom + (body_top - body_bottom) * ((row + 0.5) / row_count)
        for column_index, frac in enumerate(front_cols):
            x = cx + frac * width
            box(f"Fitness_v2_front_activity_glass_{row:02d}_{column_index:02d}", (x, front_y - 0.012, z), (width * 0.048, 0.028, 0.24), mats["glass"], category)
            box(f"Fitness_v2_back_activity_glass_{row:02d}_{column_index:02d}", (x, back_y + 0.012, z), (width * 0.048, 0.028, 0.24), mats["glass"], category)
        for column_index, frac in enumerate(side_cols):
            y = cy + frac * depth
            box(f"Fitness_v2_left_activity_glass_{row:02d}_{column_index:02d}", (left_x - 0.012, y, z), (0.028, depth * 0.052, 0.24), mats["glass"], category)
            box(f"Fitness_v2_right_activity_glass_{row:02d}_{column_index:02d}", (right_x + 0.012, y, z), (0.028, depth * 0.052, 0.24), mats["glass"], category)

    frame_category = "session72 fitness exposed frame, cantilevers, and entry depth"
    for x in (left_x, right_x):
        for y in (front_y, back_y):
            cylinder_between(f"Fitness_v2_corner_power_column_{x:.1f}_{y:.1f}", (x, y, min_z + 0.35), (x, y, max_z - 0.55), 0.06, mats["detail"], frame_category, vertices=8)
    for level, z in enumerate((body_bottom + height * 0.28, body_bottom + height * 0.50, body_bottom + height * 0.72)):
        band_width = width * (0.60 + 0.035 * level)
        band_depth = depth * (0.60 + 0.035 * level)
        box(f"Fitness_v2_cantilever_power_lip_front_{level}", (cx, front_y - 0.18, z), (band_width, 0.16, 0.16), mats["accent"], frame_category)
        box(f"Fitness_v2_cantilever_power_lip_back_{level}", (cx, back_y + 0.18, z), (band_width, 0.16, 0.16), mats["accent"], frame_category)
        box(f"Fitness_v2_cantilever_power_lip_left_{level}", (left_x - 0.18, cy, z), (0.16, band_depth, 0.16), mats["accent"], frame_category)
        box(f"Fitness_v2_cantilever_power_lip_right_{level}", (right_x + 0.18, cy, z), (0.16, band_depth, 0.16), mats["accent"], frame_category)
    for side_index, x in enumerate((left_x, right_x)):
        for brace_index, z in enumerate((body_bottom + 1.4, body_bottom + 4.2, body_bottom + 7.0, body_bottom + 9.8)):
            cylinder_between(
                f"Fitness_v2_diagonal_brace_front_{side_index}_{brace_index}",
                (x, front_y - 0.05, z),
                (cx + (x - cx) * 0.72, front_y - 0.05, z + 1.35),
                0.038,
                mats["detail"],
                frame_category,
                vertices=5,
            )

    portal_z = min_z + 1.95
    left_entry = (cx - width * 0.18, front_y - 0.34, min_z + 0.35)
    right_entry = (cx + width * 0.18, front_y - 0.34, min_z + 0.35)
    apex = (cx, front_y - 0.34, min_z + 3.9)
    cylinder_between("Fitness_v2_triangular_entry_beam_left", left_entry, apex, 0.12, mats["accent"], frame_category, vertices=6)
    cylinder_between("Fitness_v2_triangular_entry_beam_right", right_entry, apex, 0.12, mats["accent"], frame_category, vertices=6)
    box("Fitness_v2_deep_entry_shadow", (cx, front_y - 0.4, portal_z), (width * 0.20, 0.07, 1.25), mats["detail"], frame_category)
    box("Fitness_v2_entry_threshold_green_scan", (cx, front_y - 0.48, min_z + 0.78), (width * 0.18, 0.04, 0.08), mats["emissive"], frame_category)

    for panel in range(5):
        x = cx + (panel - 2) * width * 0.075
        box(f"Fitness_v2_trophy_display_panel_{panel}", (x, front_y - 0.52, min_z + 2.7), (width * 0.035, 0.035, 0.38), mats["emissive"], frame_category)

    track_category = "session72 fitness athletic track and rooftop mechanical finish"
    track_x = width * 0.70
    track_y = depth * 0.70
    for lane in range(3):
        inset = lane * 0.42
        x0, x1 = cx - track_x + inset, cx + track_x - inset
        y0, y1 = cy - track_y + inset, cy + track_y - inset
        z = min_z + 0.08 + lane * 0.015
        cylinder_between(f"Fitness_v2_track_lane_front_{lane}", (x0, y0, z), (x1, y0, z), 0.035, mats["energy"], track_category, vertices=5)
        cylinder_between(f"Fitness_v2_track_lane_back_{lane}", (x0, y1, z), (x1, y1, z), 0.035, mats["energy"], track_category, vertices=5)
        cylinder_between(f"Fitness_v2_track_lane_left_{lane}", (x0, y0, z), (x0, y1, z), 0.035, mats["energy"], track_category, vertices=5)
        cylinder_between(f"Fitness_v2_track_lane_right_{lane}", (x1, y0, z), (x1, y1, z), 0.035, mats["energy"], track_category, vertices=5)

    roof_z = max_z + 0.15
    for index, x in enumerate((cx - width * 0.26, cx, cx + width * 0.26)):
        box(f"Fitness_v2_roof_mech_housing_{index}", (x, cy + depth * 0.10, roof_z), (width * 0.085, depth * 0.10, 0.28), mats["detail"], track_category)
        box(f"Fitness_v2_roof_green_status_strip_{index}", (x, cy + depth * 0.22, roof_z + 0.24), (width * 0.07, 0.025, 0.035), mats["emissive"], track_category)
    torus("Fitness_v2_roof_pipeline_hardpoint_collar", (cx, cy, max_z + 0.28), max(width, depth) * 0.15, 0.035, mats["energy"], track_category, seg=36, minor_seg=5)
    cylinder("Fitness_v2_roof_pipeline_socket_core", (cx, cy, max_z + 0.36), 0.16, 0.18, mats["energy"], track_category, vertices=10)


def polygon_points(radius, z, sides=8, rotation=math.pi / 8):
    return [
        (math.cos(rotation + i * math.tau / sides) * radius, math.sin(rotation + i * math.tau / sides) * radius, z)
        for i in range(sides)
    ]


def add_finance_polish(mats, bbox):
    category = "session72 finance crystalline floor edges and recessed windows"
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    radius = max(width, depth) * 0.48
    body_bottom = min_z + max(0.9, height * 0.08)
    body_top = max_z - max(1.15, height * 0.13)

    for floor in range(35):
        z = body_bottom + (body_top - body_bottom) * (floor / 34)
        local_radius = radius * (1.0 - 0.18 * ((z - body_bottom) / max(body_top - body_bottom, 0.001)))
        points = polygon_points(local_radius, z)
        for side in range(8):
            start = points[side]
            end = points[(side + 1) % 8]
            cylinder_between(
                f"Finance_v2_gold_floor_edge_{floor + 1:02d}_{side}",
                (start[0] + cx, start[1] + cy, z),
                (end[0] + cx, end[1] + cy, z),
                0.018,
                mats["emissive"],
                category,
                vertices=5,
            )

    row_count = 8
    for face in range(8):
        angle = math.pi / 8 + face * math.tau / 8
        normal = Vector((math.cos(angle), math.sin(angle), 0))
        tangent = Vector((-math.sin(angle), math.cos(angle), 0))
        for row in range(row_count):
            z = body_bottom + (body_top - body_bottom) * ((row + 0.55) / row_count)
            face_radius = radius * (1.0 - 0.18 * ((z - body_bottom) / max(body_top - body_bottom, 0.001)))
            center = Vector((cx, cy, z)) + normal * (face_radius + 0.045)
            for slot, offset in enumerate((-0.42, 0.42)):
                loc = center + tangent * (offset * radius * 0.35)
                box(
                    f"Finance_v2_recessed_plate_glass_{face}_{row}_{slot}",
                    (loc.x, loc.y, loc.z),
                    (radius * 0.045, 0.028, 0.18),
                    mats["glass"],
                    category,
                    rot=(0.0, 0.0, angle + math.pi / 2),
                )
                box(
                    f"Finance_v2_gold_window_frame_{face}_{row}_{slot}",
                    (loc.x, loc.y, loc.z + 0.23),
                    (radius * 0.050, 0.022, 0.018),
                    mats["emissive"],
                    category,
                    rot=(0.0, 0.0, angle + math.pi / 2),
                )
                box(
                    f"Finance_v2_shadow_reveal_{face}_{row}_{slot}",
                    (loc.x, loc.y, loc.z - 0.23),
                    (radius * 0.052, 0.018, 0.022),
                    mats["detail"],
                    category,
                    rot=(0.0, 0.0, angle + math.pi / 2),
                )

    base_category = "session72 finance stable base, entry, and market display finish"
    for step, scale in enumerate((1.20, 1.02, 0.84)):
        cone(
            f"Finance_v2_octagonal_weighted_base_step_{step}",
            (cx, cy, min_z + 0.18 + step * 0.23),
            radius * scale,
            radius * (scale * 0.92),
            0.22,
            mats["base"],
            base_category,
            vertices=8,
            rot=(0.0, 0.0, math.pi / 8),
        )
    for face in range(8):
        angle = math.pi / 8 + face * math.tau / 8
        normal = Vector((math.cos(angle), math.sin(angle), 0))
        tangent_rot = angle + math.pi / 2
        loc = Vector((cx, cy, min_z + 1.25)) + normal * (radius * 1.03)
        box(f"Finance_v2_base_facet_pilaster_{face}", (loc.x, loc.y, loc.z), (0.10, 0.18, 0.92), mats["detail"], base_category, rot=(0.0, 0.0, tangent_rot))
        glow = Vector((cx, cy, min_z + 1.90)) + normal * (radius * 1.05)
        box(f"Finance_v2_gold_base_index_marker_{face}", (glow.x, glow.y, glow.z), (0.18, 0.025, 0.18), mats["emissive"], base_category, rot=(0.0, 0.0, tangent_rot))

    entry_y = min_y - 0.22
    box("Finance_v2_deep_geometric_entry_shadow", (cx, entry_y - 0.05, min_z + 1.55), (width * 0.16, 0.045, 0.95), mats["detail"], base_category)
    cylinder_between("Finance_v2_entry_left_gold_edge", (cx - width * 0.18, entry_y, min_z + 0.55), (cx - width * 0.08, entry_y, min_z + 2.75), 0.035, mats["emissive"], base_category, vertices=5)
    cylinder_between("Finance_v2_entry_right_gold_edge", (cx + width * 0.18, entry_y, min_z + 0.55), (cx + width * 0.08, entry_y, min_z + 2.75), 0.035, mats["emissive"], base_category, vertices=5)
    box("Finance_v2_market_ticker_panel", (cx, entry_y - 0.05, min_z + 2.15), (width * 0.18, 0.026, 0.18), mats["emissive"], base_category)
    for tick in range(9):
        x = cx + (tick - 4) * width * 0.035
        box(f"Finance_v2_market_ticker_glyph_{tick}", (x, entry_y - 0.08, min_z + 2.17 + (tick % 3) * 0.055), (0.035, 0.018, 0.04), mats["accent"], base_category)

    crown_category = "session72 finance crown data ring and observation deck polish"
    crown_z = body_top + height * 0.055
    for ring_index, z in enumerate((crown_z, crown_z + 0.34, crown_z + 0.72)):
        torus(f"Finance_v2_crown_financial_data_ring_{ring_index}", (cx, cy, z), radius * (0.50 - ring_index * 0.035), 0.026, mats["emissive"], crown_category, seg=64, minor_seg=4)
    for panel in range(16):
        angle = panel * math.tau / 16
        loc = Vector((cx, cy, crown_z + 0.44)) + Vector((math.cos(angle), math.sin(angle), 0)) * (radius * 0.55)
        box(f"Finance_v2_crown_market_panel_{panel}", (loc.x, loc.y, loc.z), (0.18, 0.025, 0.24), mats["accent"], crown_category, rot=(0.0, 0.0, angle + math.pi / 2))
        if panel % 2 == 0:
            cylinder_between(
                f"Finance_v2_crown_gold_data_pin_{panel}",
                (cx, cy, crown_z + 0.04),
                (loc.x, loc.y, loc.z + 0.10),
                0.016,
                mats["emissive"],
                crown_category,
                vertices=5,
            )
    deck_y = max_y + 0.30
    box("Finance_v2_cantilevered_observation_glass_floor", (cx, deck_y + depth * 0.06, crown_z + 0.18), (width * 0.20, depth * 0.085, 0.035), mats["glass"], crown_category)
    for offset in (-0.22, 0.0, 0.22):
        cylinder_between(
            f"Finance_v2_observation_deck_underbrace_{offset:+.2f}",
            (cx + offset * width, deck_y, crown_z - 0.22),
            (cx + offset * width * 0.6, max_y, crown_z - 0.70),
            0.024,
            mats["detail"],
            crown_category,
            vertices=5,
        )
    torus("Finance_v2_roof_pipeline_hardpoint_collar", (cx, cy, max_z + 0.22), radius * 0.20, 0.028, mats["energy"], crown_category, seg=36, minor_seg=4)
    cylinder("Finance_v2_roof_pipeline_socket_core", (cx, cy, max_z + 0.30), 0.13, 0.16, mats["energy"], crown_category, vertices=10)


def summarize_created_categories():
    summary = defaultdict(lambda: {"objects": 0, "tris": 0})
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in mesh_objects():
        category = created_categories.get(obj.name)
        if not category:
            continue
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        mesh.calc_loop_triangles()
        summary[category]["objects"] += 1
        summary[category]["tris"] += len(mesh.loop_triangles)
        eval_obj.to_mesh_clear()
    return dict(sorted(summary.items()))


def merge_created_by_material(module_id):
    grouped = defaultdict(list)
    for obj in mesh_objects():
        if obj.name not in created_categories:
            continue
        slot = material_base_name(obj.data.materials[0]) if obj.data.materials else "detail"
        grouped[slot].append(obj)

    for slot, objects in grouped.items():
        if len(objects) < 2:
            continue
        bpy.ops.object.select_all(action="DESELECT")
        active = objects[0]
        for obj in objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = active
        bpy.ops.object.join()
        active.name = f"{module_id}_s72_{slot}_polish_mesh"
        created_categories[active.name] = f"session72 merged {slot} polish geometry"


def remove_cameras_lights():
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)


def parent_under_root(root_name):
    existing = bpy.data.objects.get(root_name)
    if existing:
        bpy.data.objects.remove(existing, do_unlink=True)
    root = bpy.data.objects.new(root_name, None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in list(bpy.data.objects):
        if obj == root:
            continue
        if obj.type == "MESH" and obj.parent is None:
            obj.parent = root
    return root


def export_glb(module):
    remove_cameras_lights()
    parent_under_root(module["root_name"])
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(ROOT, module["draft_glb"]),
        export_format="GLB",
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_yup=True,
        export_apply=True,
        export_texcoords=True,
        export_normals=True,
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
    )


def validate_glb(module):
    path = os.path.join(ROOT, module["draft_glb"])
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=path)
    objects = mesh_objects()
    material_slots = sorted({material_base_name(mat) for obj in objects for mat in obj.data.materials if mat})
    invalid = sorted(slot for slot in material_slots if slot not in ALLOWED_MATERIALS)
    bbox = world_bbox(objects)
    tris = count_tris(objects)
    size_bytes = os.path.getsize(path)
    cameras_lights = [obj.name for obj in bpy.data.objects if obj.type in {"CAMERA", "LIGHT"}]
    roots = [obj.name for obj in bpy.data.objects if obj.parent is None]
    qa = {
        "path": module["draft_glb"],
        "object_count": len(objects),
        "tris": tris,
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "bbox": bbox,
        "materials": material_slots,
        "invalid_materials": invalid,
        "cameras_lights": cameras_lights,
        "roots": roots,
        "passed": (
            len(objects) > 0
            and module["tri_min"] <= tris <= module["tri_max"]
            and module["size_min_kb"] * 1024 <= size_bytes <= module["size_max_kb"] * 1024
            and not invalid
            and not cameras_lights
            and bbox["min"][2] >= -0.02
        ),
    }
    with open(os.path.join(ROOT, module["qa_import"]), "w", encoding="utf-8") as handle:
        json.dump(qa, handle, indent=2)
    return qa


def look_at(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_render(width=1400, height=1100):
    scene = bpy.context.scene
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 48
    scene.world.color = (0.002, 0.002, 0.006)
    return scene


def add_light_rig(bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    height = max_z - min_z
    bpy.ops.object.light_add(type="AREA", location=(cx, min_y - 10, min_z + height * 0.78))
    key = current_object()
    key.name = "S72_Key_Area"
    key.data.energy = 420
    key.data.size = 7
    bpy.ops.object.light_add(type="POINT", location=(min_x - 4, min_y - 5, min_z + height * 0.28))
    fill = current_object()
    fill.name = "S72_Warm_Fill"
    fill.data.energy = 120
    bpy.ops.object.light_add(type="POINT", location=(max_x + 4, max_y + 4, max_z + 2))
    crown = current_object()
    crown.name = "S72_Crown_Glint"
    crown.data.energy = 160


def render_current(path, camera_loc, target, bbox, focal=44, ortho=None, width=1400, height=1100):
    setup_render(width, height)
    add_light_rig(bbox)
    bpy.ops.object.camera_add(location=camera_loc)
    camera = current_object()
    look_at(camera, target)
    camera.data.lens = focal
    if ortho:
        camera.data.type = "ORTHO"
        camera.data.ortho_scale = ortho
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)


def emission_strengths():
    values = []
    for material in bpy.data.materials:
        if not material.use_nodes:
            continue
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if not bsdf or "Emission Strength" not in bsdf.inputs:
            continue
        values.append((material, bsdf.inputs["Emission Strength"].default_value))
    return values


def render_evidence(module, bbox):
    prefix = "session72-fitness-v2" if module["id"] == "fitness" else "session72-finance-v2"
    directory = os.path.join(ROOT, module["screenshots"])
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, cz = bbox["center"]
    height = max_z - min_z
    span = max(max_x - min_x, max_y - min_y, height)
    target = (cx, cy, min_z + height * 0.52)
    render_current(
        os.path.join(directory, f"{prefix}-front.png"),
        (cx, min_y - span * 1.65, min_z + height * 0.54),
        target,
        bbox,
        focal=48,
    )
    render_current(
        os.path.join(directory, f"{prefix}-threequarter.png"),
        (max_x + span * 1.1, min_y - span * 1.35, min_z + height * 0.58),
        target,
        bbox,
        focal=44,
    )
    saved = emission_strengths()
    for material, _value in saved:
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Emission Strength"].default_value = 0
    render_current(
        os.path.join(directory, f"{prefix}-dark-first.png"),
        (max_x + span * 0.9, min_y - span * 1.45, min_z + height * 0.50),
        target,
        bbox,
        focal=48,
    )
    for material, value in saved:
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Emission Strength"].default_value = value


def build_module(module):
    print(f"--- Building Session 72 v2 polish: {module['label']} ---")
    global created_categories
    created_categories = {}
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, module["source_blend"]))
    mats = normalize_materials(module["accent_hex"])
    pre_tris = count_tris()
    pre_objects = len(mesh_objects())
    pre_bbox = world_bbox()

    if module["id"] == "fitness":
        add_fitness_polish(mats, pre_bbox)
    elif module["id"] == "finance":
        add_finance_polish(mats, pre_bbox)
    else:
        raise RuntimeError(f"Unhandled module: {module['id']}")

    bbox = world_bbox()
    if bbox["min"][2] < -0.001:
        dz = -bbox["min"][2]
        for obj in mesh_objects():
            obj.location.z += dz
        bbox = world_bbox()

    category_summary = summarize_created_categories()
    merge_created_by_material(module["id"])
    bbox = world_bbox()
    final_live_tris = count_tris()
    final_live_objects = len(mesh_objects())
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, module["output_blend"]))

    render_evidence(module, bbox)
    export_glb(module)
    qa = validate_glb(module)
    if not qa["passed"]:
        raise RuntimeError(f"{module['label']} Session 72 QA failed: {qa}")

    shutil.copy2(os.path.join(ROOT, module["draft_glb"]), os.path.join(ROOT, module["approved_glb"]))
    shutil.copy2(os.path.join(ROOT, module["draft_glb"]), os.path.join(ROOT, module["app_glb"]))

    metrics = {
        "session": 72,
        "date": str(date.today()),
        "module": module["label"],
        "source_blend": module["source_blend"],
        "output_blend": module["output_blend"],
        "draft_glb": module["draft_glb"],
        "approved_glb": module["approved_glb"],
        "app_public_glb": module["app_glb"],
        "pre_tris": pre_tris,
        "pre_objects": pre_objects,
        "pre_bbox": pre_bbox,
        "final_live_tris": final_live_tris,
        "final_live_objects": final_live_objects,
        "final_tris": qa["tris"],
        "final_objects": qa["object_count"],
        "final_size_bytes": qa["size_bytes"],
        "final_size_kb": qa["size_kb"],
        "bbox": qa["bbox"],
        "material_slots": qa["materials"],
        "created_categories": category_summary,
        "budget": {
            "tri_min": module["tri_min"],
            "tri_max": module["tri_max"],
            "size_min_kb": module["size_min_kb"],
            "size_max_kb": module["size_max_kb"],
            "status": "APPROVED",
        },
        "qa": qa,
    }
    with open(os.path.join(ROOT, module["metrics"]), "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
    return metrics


def audit_one(label, path, module_id):
    full_path = os.path.join(ROOT, path)
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=full_path)
    objects = mesh_objects()
    tris = count_tris(objects)
    bbox = world_bbox(objects)
    size_bytes = os.path.getsize(full_path)
    slots = sorted({material_base_name(mat) for obj in objects for mat in obj.data.materials if mat})
    invalid = sorted(slot for slot in slots if slot not in ALLOWED_MATERIALS)
    return {
        "id": module_id,
        "label": label,
        "path": path,
        "tris": tris,
        "object_count": len(objects),
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "bbox": bbox,
        "materials": slots,
        "invalid_materials": invalid,
    }


def audit_all():
    return [audit_one(label, path, module_id) for label, path, module_id in EXTERIOR_MODULES]


def write_wave_report(pre_audit, post_audit, metrics_by_id):
    json_path = os.path.join(ASSEMBLY_AUDIT, "session-72-fitness-finance-polish.json")
    md_path = os.path.join(ASSEMBLY_AUDIT, "session-72-fitness-finance-polish.md")
    report = {
        "session": 72,
        "date": str(date.today()),
        "scope": "Phase 8.4 Fitness + Finance exterior polish wave",
        "pre_audit": pre_audit,
        "post_audit": post_audit,
        "polished_modules": metrics_by_id,
        "verdict": "APPROVED - Fitness and Finance v2 exterior polish complete; origins and runtime paths preserved.",
    }
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    lines = [
        "# Session 72 Fitness + Finance Exterior Polish",
        "",
        f"Date: {date.today()}",
        "Status: Approved",
        "",
        "## Summary",
        "",
        "Session 72 completed the Phase 8.4 polish wave for the Fitness and Finance approved exteriors while preserving layout origins, city-layout-v2 positions, and baked energy route assumptions.",
        "",
        "## V2 Results",
        "",
        "| Module | Previous Tris | Session 72 Tris | Objects | Size | Verdict |",
        "|--------|---------------|-----------------|---------|------|---------|",
    ]
    for module in MODULES:
        metrics = metrics_by_id[module["id"]]
        lines.append(
            f"| {module['label']} | {metrics['pre_tris']:,} | {metrics['final_tris']:,} | "
            f"{metrics['final_objects']} | {metrics['final_size_kb']:.1f} KB | Approved |"
        )
    lines.extend(
        [
            "",
            "## Added Finish Signals",
            "",
            "- Fitness: 30 green floor-edge bands, activity glass, exposed corner steel, cantilever power lips, triangular entry depth, trophy panels, track energy lanes, rooftop mechanical detail, and roof pipeline collar.",
            "- Finance: 35 octagonal gold floor-edge rings, recessed plate-glass facets, window frames, weighted base steps, entry ticker, crown data rings, observation deck underbracing, and roof pipeline collar.",
            "",
            "## QA",
            "",
            "- Both draft GLBs reimport cleanly.",
            "- Both exports use only approved material slot names.",
            "- No cameras or lights exported.",
            "- Both assets remain within their 12K-18K exterior triangle budgets and 100-350 KB file budgets.",
            "",
            "## Evidence",
            "",
            "- `modules/01-fitness/screenshots/session72-fitness-v2-front.png`",
            "- `modules/01-fitness/screenshots/session72-fitness-v2-threequarter.png`",
            "- `modules/01-fitness/screenshots/session72-fitness-v2-dark-first.png`",
            "- `modules/03-finance/screenshots/session72-finance-v2-front.png`",
            "- `modules/03-finance/screenshots/session72-finance-v2-threequarter.png`",
            "- `modules/03-finance/screenshots/session72-finance-v2-dark-first.png`",
            "- `assembly/screenshots/s72-exterior-finish-contact-sheet.png`",
        ]
    )
    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return {"json": rel(json_path), "md": rel(md_path)}


def import_group(path, offset, target_height=None):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    imported = [obj for obj in bpy.data.objects if obj not in before]
    meshes = [obj for obj in imported if obj.type == "MESH"]
    bbox = world_bbox(meshes)
    center = Vector(bbox["center"])
    roots = [obj for obj in imported if obj.parent is None or obj.parent not in imported]
    group = bpy.data.objects.new(f"contact_{os.path.basename(path).replace('.glb', '')}", None)
    bpy.context.collection.objects.link(group)
    group.location = (center.x, center.y, bbox["min"][2])
    for root in roots:
        root.parent = group
        root.matrix_parent_inverse = group.matrix_world.inverted()
    if target_height and bbox["size"][2] > 0.001:
        scale = target_height / bbox["size"][2]
        group.scale = (scale, scale, scale)
    group.location = offset
    return imported


def render_contact_sheet():
    clear_scene()
    cols = 4
    x_spacing = 38
    z_spacing = 37
    for index, (_label, path, module_id) in enumerate(EXTERIOR_MODULES):
        row = index // cols
        col = index % cols
        x = (col - 1.5) * x_spacing
        z = (2 - row) * z_spacing
        target_height = 42 if module_id == "sia-tower" else 26
        import_group(os.path.join(ROOT, path), (x, 0, z), target_height=target_height)

    bbox = world_bbox()
    render_current(
        os.path.join(ASSEMBLY_SCREENSHOTS, "s72-exterior-finish-contact-sheet.png"),
        (0, -190, 62),
        (0, 0, 54),
        bbox,
        focal=70,
        ortho=160,
        width=1800,
        height=1500,
    )


def main():
    print("=== Session 72: Fitness + Finance exterior polish wave ===")
    pre_audit = audit_all()
    metrics_by_id = {}
    for module in MODULES:
        metrics_by_id[module["id"]] = build_module(module)
    post_audit = audit_all()
    report_paths = write_wave_report(pre_audit, post_audit, metrics_by_id)
    render_contact_sheet()
    print(f"Report written: {report_paths['md']}")
    for module in MODULES:
        print(f"{module['label']} approved GLB updated: {module['approved_glb']}")


if __name__ == "__main__":
    main()

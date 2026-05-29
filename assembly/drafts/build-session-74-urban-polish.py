"""
Balencia City v3 - Session 74
Phase 8.6 Knowledgebase + Chat + Career urban exterior polish wave.

This upgrades already-approved urban/civic exterior GLBs while preserving
origins, city-layout-v2 positions, app paths, and baked energy route assumptions.
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
        "id": "knowledgebase",
        "label": "Knowledgebase",
        "root_name": "knowledgebase-ext",
        "accent_hex": "#7F24FF",
        "source_glb": "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb",
        "output_blend": "modules/04-knowledgebase/exterior/drafts/knowledgebase-session74-v2-polish.blend",
        "draft_glb": "modules/04-knowledgebase/exterior/drafts/knowledgebase-ext-v2-draft-s74.glb",
        "approved_glb": "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/04-knowledgebase/knowledgebase-ext.glb",
        "metrics": "modules/04-knowledgebase/exterior/drafts/session74-v2-metrics.json",
        "qa_import": "modules/04-knowledgebase/exterior/drafts/session74-qa-import.json",
        "screenshots": "modules/04-knowledgebase/screenshots",
        "tri_min": 15000,
        "tri_max": 20000,
        "size_min_kb": 100,
        "size_max_kb": 400,
    },
    {
        "id": "chat",
        "label": "Chat & Communication",
        "root_name": "chat-ext",
        "accent_hex": "#FF5E00",
        "source_glb": "modules/05-chat-communication/exterior/approved/chat-ext.glb",
        "output_blend": "modules/05-chat-communication/exterior/drafts/chat-session74-v2-polish.blend",
        "draft_glb": "modules/05-chat-communication/exterior/drafts/chat-ext-v2-draft-s74.glb",
        "approved_glb": "modules/05-chat-communication/exterior/approved/chat-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/05-chat-communication/chat-ext.glb",
        "metrics": "modules/05-chat-communication/exterior/drafts/session74-v2-metrics.json",
        "qa_import": "modules/05-chat-communication/exterior/drafts/session74-qa-import.json",
        "screenshots": "modules/05-chat-communication/screenshots",
        "tri_min": 15000,
        "tri_max": 20500,
        "size_min_kb": 120,
        "size_max_kb": 400,
    },
    {
        "id": "career",
        "label": "Career",
        "root_name": "career-ext",
        "accent_hex": "#3B82F6",
        "source_glb": "modules/08-career/exterior/approved/career-ext.glb",
        "output_blend": "modules/08-career/exterior/drafts/career-session74-v2-polish.blend",
        "draft_glb": "modules/08-career/exterior/drafts/career-ext-v2-draft-s74.glb",
        "approved_glb": "modules/08-career/exterior/approved/career-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/08-career/career-ext.glb",
        "metrics": "modules/08-career/exterior/drafts/session74-v2-metrics.json",
        "qa_import": "modules/08-career/exterior/drafts/session74-qa-import.json",
        "screenshots": "modules/08-career/screenshots",
        "tri_min": 15000,
        "tri_max": 20500,
        "size_min_kb": 100,
        "size_max_kb": 400,
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
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
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
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
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
        "accent": ((0.024, 0.027, 0.030, 1.0), accent, 0.12, 1.0, 0.48, 0.18),
        "glass": ((0.006, 0.009, 0.014, 1.0), accent, 0.025, 0.82, 0.16, 0.18),
        "detail": ((0.008, 0.009, 0.012, 1.0), None, 0.0, 1.0, 0.56, 0.30),
        "emissive": ((0.018, 0.018, 0.012, 1.0), accent, 0.24, 1.0, 0.24, 0.0),
        "energy": ((0.045, 0.018, 0.004, 1.0), orange, 0.22, 1.0, 0.20, 0.04),
        "holo": ((0.018, 0.024, 0.020, 1.0), accent, 0.20, 0.42, 0.18, 0.02),
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
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, material)
    shade_smooth(obj)
    apply_transform(obj)
    return register(obj, category)


def torus(name, loc, major, minor, material, category, seg=32, minor_seg=4, rot=(0.0, 0.0, 0.0)):
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


def cylinder_between(name, start, end, radius, material, category, vertices=5):
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


def linked_mesh_instance(name, source, loc, category, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)):
    obj = bpy.data.objects.new(name, source.data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = rot
    obj.scale = scale
    if source.data.materials:
        obj.data.materials.clear()
        for material in source.data.materials:
            obj.data.materials.append(material)
    return register(obj, category)


def add_knowledgebase_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    category = "session74 knowledgebase archive civic finish"

    # Classical base: stronger column fluting, arch depth, and archive stair mass.
    for col in range(6):
        x = cx + (col - 2.5) * width * 0.115
        y = min_y - depth * 0.075
        cylinder(f"Knowledge_v2_monument_column_sleeve_{col}", (x, y, min_z + height * 0.16), width * 0.030, height * 0.30, mats["base"], category, vertices=12)
        for flute in range(6):
            angle = flute * math.tau / 6
            cylinder_between(
                f"Knowledge_v2_column_shadow_flute_{col}_{flute}",
                (x + math.cos(angle) * width * 0.033, y + math.sin(angle) * width * 0.033, min_z + height * 0.035),
                (x + math.cos(angle) * width * 0.033, y + math.sin(angle) * width * 0.033, min_z + height * 0.285),
                width * 0.004,
                mats["detail"],
                category,
                vertices=4,
            )
        torus(f"Knowledge_v2_column_cap_shadow_{col}", (x, y, min_z + height * 0.315), width * 0.038, width * 0.004, mats["detail"], category, seg=20, minor_seg=3)

    for tier in range(5):
        z = min_z + height * (0.10 + tier * 0.047)
        box(f"Knowledge_v2_deep_archive_band_{tier}", (cx, min_y - depth * 0.105, z), (width * 0.42, depth * 0.012, height * 0.006), mats["base"], category)
        for arch in range(5):
            x = cx + (arch - 2) * width * 0.095
            cylinder(f"Knowledge_v2_recessed_arch_glass_{tier}_{arch}", (x, min_y - depth * 0.121, z + height * 0.015), width * 0.020, depth * 0.018, mats["glass"], category, vertices=12, rot=(math.pi / 2, 0, 0))

    for step in range(5):
        box(f"Knowledge_v2_archive_vault_step_{step}", (cx, min_y - depth * (0.19 + step * 0.020), min_z + 0.035 + step * 0.020), (width * (0.26 - step * 0.025), depth * 0.020, 0.020), mats["base"], category)

    # Floating data floors: visible civic-library stack, purple reading glow, and screen panels.
    floor_count = 11
    for floor in range(floor_count):
        z = min_z + height * (0.44 + floor * 0.040)
        scale = 0.78 - (floor % 3) * 0.020
        box(f"Knowledge_v2_floating_data_floor_glass_{floor:02d}", (cx, cy, z), (width * scale * 0.28, depth * scale * 0.25, height * 0.0045), mats["glass"], category, rot=(0, 0, 0.035 * (floor % 2)))
        box(f"Knowledge_v2_purple_reading_core_{floor:02d}", (cx, cy, z + height * 0.006), (width * scale * 0.20, depth * scale * 0.18, height * 0.003), mats["emissive"], category, rot=(0, 0, 0.035 * (floor % 2)))
        for side in (-1, 1):
            box(f"Knowledge_v2_holo_catalog_panel_{floor:02d}_{side}", (cx + side * width * 0.235, cy, z + height * 0.010), (width * 0.006, depth * 0.13, height * 0.026), mats["holo"], category)

    for stream in range(9):
        x = cx + (stream - 4) * width * 0.032
        cylinder_between(
            f"Knowledge_v2_waterfall_strand_{stream:02d}",
            (x, min_y - depth * 0.145, max_z - height * 0.09),
            (x + math.sin(stream) * width * 0.010, min_y - depth * 0.155, min_z + height * 0.07),
            width * 0.0045,
            mats["energy"],
            category,
            vertices=5,
        )
    torus(f"Knowledge_v2_reservoir_basin_outer", (cx, min_y - depth * 0.155, min_z + height * 0.045), width * 0.135, width * 0.006, mats["energy"], category, seg=36, minor_seg=4, rot=(math.pi / 2, 0, 0))
    cylinder(f"Knowledge_v2_crown_beacon_core", (cx, cy, max_z + height * 0.035), width * 0.020, height * 0.13, mats["emissive"], category, vertices=12)

    glyph_master = cylinder("Knowledge_v2_reusable_archive_glyph_master", (cx, cy, min_z + height * 0.40), width * 0.010, depth * 0.004, mats["holo"], category, vertices=8, rot=(math.pi / 2, 0, 0))
    glyph_master.hide_viewport = True
    glyph_master.hide_render = True
    for floor in range(12):
        z = min_z + height * (0.39 + floor * 0.038)
        for glyph in range(12):
            side = -1 if glyph < 6 else 1
            row = glyph if glyph < 6 else glyph - 6
            x = cx + side * width * (0.125 + row * 0.017)
            y = min_y - depth * 0.132
            linked_mesh_instance(
                f"Knowledge_v2_instanced_archive_glyph_{floor:02d}_{glyph:02d}",
                glyph_master,
                (x, y, z + (row % 2) * height * 0.006),
                category,
                rot=(math.pi / 2, 0, row * 0.24),
                scale=(0.72 + (row % 3) * 0.10, 1.0, 1.0),
            )


def add_chat_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    category = "session74 chat communication signal finish"

    pod_positions = [
        (cx - width * 0.22, cy - depth * 0.16, height * 0.64),
        (cx + width * 0.12, cy - depth * 0.09, height * 0.74),
        (cx + width * 0.25, cy + depth * 0.18, height * 0.56),
        (cx - width * 0.09, cy + depth * 0.19, height * 0.51),
    ]
    for pod, (x, y, top) in enumerate(pod_positions):
        for band in range(5):
            z = min_z + top * (0.24 + band * 0.125)
            box(f"Chat_v2_live_floor_signal_band_{pod}_{band}", (x, y - depth * 0.050, z), (width * 0.055, depth * 0.006, height * 0.0035), mats["emissive"], category)
            if band % 2 == 0:
                box(f"Chat_v2_outward_message_screen_{pod}_{band}", (x + width * 0.042, y, z + height * 0.016), (width * 0.005, depth * 0.030, height * 0.022), mats["holo"], category)
        for spike in range(3):
            angle = spike * math.tau / 3
            base = (x + math.cos(angle) * width * 0.027, y + math.sin(angle) * depth * 0.027, min_z + top + height * 0.025)
            tip = (base[0], base[1], base[2] + height * (0.075 - spike * 0.010))
            cylinder_between(f"Chat_v2_broadcast_antenna_{pod}_{spike}", base, tip, width * 0.0038, mats["detail"], category, vertices=5)
        torus(f"Chat_v2_rooftop_signal_halo_{pod}", (x, y, min_z + top + height * 0.020), width * 0.052, width * 0.0035, mats["energy"], category, seg=24, minor_seg=3)

    for link, (a, b) in enumerate(((0, 1), (1, 2), (0, 3), (3, 2))):
        start = Vector((pod_positions[a][0], pod_positions[a][1], min_z + pod_positions[a][2] * 0.62))
        end = Vector((pod_positions[b][0], pod_positions[b][1], min_z + pod_positions[b][2] * 0.62))
        cylinder_between(f"Chat_v2_glass_bridge_outer_sleeve_{link}", start, end, width * 0.010, mats["glass"], category, vertices=8)
        cylinder_between(f"Chat_v2_inner_signal_thread_{link}", start + Vector((0, 0, height * 0.012)), end + Vector((0, 0, height * 0.012)), width * 0.004, mats["energy"], category, vertices=5)
        midpoint = (start + end) / 2
        box(f"Chat_v2_bridge_status_node_{link}", midpoint, (width * 0.022, depth * 0.012, height * 0.012), mats["emissive"], category)

    for plaza in range(8):
        angle = plaza * math.tau / 8
        x = cx + math.cos(angle) * width * 0.28
        y = cy + math.sin(angle) * depth * 0.27
        box(f"Chat_v2_plaza_conversation_tile_{plaza:02d}", (x, y, min_z + 0.020), (width * 0.035, depth * 0.018, 0.012), mats["base"], category, rot=(0, 0, angle))


def add_career_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    category = "session74 career ascent tower finish"

    tower_positions = [
        (cx, cy - depth * 0.08, height * 0.92),
        (cx - width * 0.23, cy + depth * 0.13, height * 0.72),
        (cx + width * 0.20, cy + depth * 0.15, height * 0.66),
        (cx + width * 0.06, cy - depth * 0.28, height * 0.58),
    ]
    for tower, (x, y, top) in enumerate(tower_positions):
        for band in range(6):
            z = min_z + top * (0.18 + band * 0.120)
            box(f"Career_v2_crisp_blue_floor_joint_{tower}_{band}", (x, y - depth * 0.055, z), (width * 0.060, depth * 0.005, height * 0.0028), mats["emissive"], category)
        for fin in (-1, 1):
            cylinder_between(
                f"Career_v2_upward_corner_fin_{tower}_{fin}",
                (x + fin * width * 0.045, y + depth * 0.035, min_z + top * 0.74),
                (x + fin * width * 0.060, y + depth * 0.045, min_z + top + height * 0.045),
                width * 0.004,
                mats["accent"],
                category,
                vertices=4,
            )

    for lift, tower_index in enumerate((0, 1)):
        x, y, top = tower_positions[tower_index]
        cylinder(f"Career_v2_visible_elevator_tube_{lift}", (x - width * 0.065, y - depth * 0.020, min_z + top * 0.49), width * 0.014, top * 0.68, mats["glass"], category, vertices=8)
        for car in range(2):
            z = min_z + top * (0.28 + car * 0.30)
            box(f"Career_v2_elevator_car_glow_{lift}_{car}", (x - width * 0.065, y - depth * 0.020, z), (width * 0.015, width * 0.015, height * 0.012), mats["emissive"], category)

    deck_z = min_z + tower_positions[0][2] + height * 0.010
    box("Career_v2_executive_deck_glass_floor", (cx + width * 0.095, cy - depth * 0.10, deck_z), (width * 0.090, depth * 0.040, height * 0.004), mats["glass"], category)
    for rail in (-1, 1):
        box(f"Career_v2_observation_deck_rail_{rail}", (cx + width * 0.095, cy - depth * (0.10 + rail * 0.044), deck_z + height * 0.014), (width * 0.090, depth * 0.004, height * 0.010), mats["detail"], category)

    for path in range(6):
        angle = -math.pi * 0.85 + path * math.pi * 1.70 / 5
        box(f"Career_v2_networking_plaza_path_{path}", (cx + math.cos(angle) * width * 0.22, cy + math.sin(angle) * depth * 0.24, min_z + 0.018), (width * 0.045, depth * 0.010, 0.010), mats["base"], category, rot=(0, 0, angle))


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
        active.name = f"{module_id}_s74_{slot}_polish_mesh"
        created_categories[active.name] = f"session74 merged {slot} polish geometry"


def merge_all_meshes_by_material(module_id):
    grouped = defaultdict(list)
    for obj in mesh_objects():
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
        active.name = f"{module_id}_s74_{slot}_combined_mesh"


def remove_cameras_lights():
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"} or "reusable_archive_glyph_master" in obj.name:
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
        "roots": [obj.name for obj in bpy.data.objects if obj.parent is None],
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
    key.name = "S74_Key_Area"
    key.data.energy = 420
    key.data.size = 7
    bpy.ops.object.light_add(type="POINT", location=(min_x - 4, min_y - 5, min_z + height * 0.28))
    fill = current_object()
    fill.name = "S74_Warm_Fill"
    fill.data.energy = 120
    bpy.ops.object.light_add(type="POINT", location=(max_x + 4, max_y + 4, max_z + 2))
    crown = current_object()
    crown.name = "S74_Crown_Glint"
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
    prefix = f"session74-{module['id']}-v2"
    directory = os.path.join(ROOT, module["screenshots"])
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    height = max_z - min_z
    span = max(max_x - min_x, max_y - min_y, height)
    target = (cx, cy, min_z + height * 0.52)
    render_current(os.path.join(directory, f"{prefix}-front.png"), (cx, min_y - span * 1.65, min_z + height * 0.54), target, bbox, focal=48)
    render_current(os.path.join(directory, f"{prefix}-threequarter.png"), (max_x + span * 1.1, min_y - span * 1.35, min_z + height * 0.58), target, bbox, focal=44)
    saved = emission_strengths()
    for material, _value in saved:
        material.node_tree.nodes.get("Principled BSDF").inputs["Emission Strength"].default_value = 0
    render_current(os.path.join(directory, f"{prefix}-dark-first.png"), (max_x + span * 0.9, min_y - span * 1.45, min_z + height * 0.50), target, bbox, focal=48)
    for material, value in saved:
        material.node_tree.nodes.get("Principled BSDF").inputs["Emission Strength"].default_value = value


def build_module(module):
    print(f"--- Building Session 74 v2 polish: {module['label']} ---")
    global created_categories
    created_categories = {}
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, module["source_glb"]))
    mats = normalize_materials(module["accent_hex"])
    pre_tris = count_tris()
    pre_objects = len(mesh_objects())
    pre_bbox = world_bbox()

    if module["id"] == "knowledgebase":
        add_knowledgebase_polish(mats, pre_bbox)
    elif module["id"] == "chat":
        add_chat_polish(mats, pre_bbox)
    elif module["id"] == "career":
        add_career_polish(mats, pre_bbox)
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
    merge_all_meshes_by_material(module["id"])
    bbox = world_bbox()
    final_live_tris = count_tris()
    final_live_objects = len(mesh_objects())
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, module["output_blend"]))
    render_evidence(module, bbox)
    export_glb(module)
    qa = validate_glb(module)
    if not qa["passed"]:
        raise RuntimeError(f"{module['label']} Session 74 QA failed: {qa}")

    shutil.copy2(os.path.join(ROOT, module["draft_glb"]), os.path.join(ROOT, module["approved_glb"]))
    shutil.copy2(os.path.join(ROOT, module["draft_glb"]), os.path.join(ROOT, module["app_glb"]))
    metrics = {
        "session": 74,
        "date": str(date.today()),
        "module": module["label"],
        "source_glb": module["source_glb"],
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
    clear_scene()
    full_path = os.path.join(ROOT, path)
    bpy.ops.import_scene.gltf(filepath=full_path)
    objects = mesh_objects()
    slots = sorted({material_base_name(mat) for obj in objects for mat in obj.data.materials if mat})
    return {
        "id": module_id,
        "label": label,
        "path": path,
        "tris": count_tris(objects),
        "object_count": len(objects),
        "size_bytes": os.path.getsize(full_path),
        "size_kb": round(os.path.getsize(full_path) / 1024, 1),
        "bbox": world_bbox(objects),
        "materials": slots,
        "invalid_materials": sorted(slot for slot in slots if slot not in ALLOWED_MATERIALS),
    }


def audit_all():
    return [audit_one(label, path, module_id) for label, path, module_id in EXTERIOR_MODULES]


def write_wave_report(pre_audit, post_audit, metrics_by_id):
    json_path = os.path.join(ASSEMBLY_AUDIT, "session-74-urban-polish.json")
    md_path = os.path.join(ASSEMBLY_AUDIT, "session-74-urban-polish.md")
    report = {
        "session": 74,
        "date": str(date.today()),
        "scope": "Phase 8.6 Knowledgebase + Chat + Career urban exterior polish wave",
        "pre_audit": pre_audit,
        "post_audit": post_audit,
        "polished_modules": metrics_by_id,
        "verdict": "APPROVED - urban v2 exterior polish complete; origins and runtime paths preserved.",
    }
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    lines = [
        "# Session 74 Urban Exterior Polish",
        "",
        f"Date: {date.today()}",
        "Status: Approved",
        "",
        "## Summary",
        "",
        "Session 74 completed the Phase 8.6 urban polish wave for Knowledgebase, Chat, and Career while preserving layout origins, city-layout-v2 positions, and baked energy route assumptions.",
        "",
        "## V2 Results",
        "",
        "| Module | Previous Tris | Session 74 Tris | Objects | Size | Verdict |",
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
            "- Knowledgebase: stronger classical column sleeves/fluting, recessed archive arches, vault steps, floating data floors, holo catalog panels, waterfall strands, reservoir basin, and crown beacon.",
            "- Chat: live floor signal bands, outward holo screens, antenna crowns, rooftop signal halos, glass bridge sleeves, inner signal threads, bridge status nodes, and plaza conversation tiles.",
            "- Career: crisp blue floor joints, upward corner fins, visible elevator tubes/cars, executive observation deck glass/rails, and networking plaza paths.",
            "",
            "## QA",
            "",
            "- All three draft GLBs reimport cleanly.",
            "- All three exports use only approved material slot names.",
            "- No cameras or lights exported.",
            "- All three assets remain within their Phase 8 exterior triangle/file budgets.",
            "",
            "## Evidence",
            "",
            "- `modules/04-knowledgebase/screenshots/session74-knowledgebase-v2-front.png`",
            "- `modules/04-knowledgebase/screenshots/session74-knowledgebase-v2-threequarter.png`",
            "- `modules/04-knowledgebase/screenshots/session74-knowledgebase-v2-dark-first.png`",
            "- `modules/05-chat-communication/screenshots/session74-chat-v2-front.png`",
            "- `modules/05-chat-communication/screenshots/session74-chat-v2-threequarter.png`",
            "- `modules/05-chat-communication/screenshots/session74-chat-v2-dark-first.png`",
            "- `modules/08-career/screenshots/session74-career-v2-front.png`",
            "- `modules/08-career/screenshots/session74-career-v2-threequarter.png`",
            "- `modules/08-career/screenshots/session74-career-v2-dark-first.png`",
            "- `assembly/screenshots/s74-exterior-finish-contact-sheet.png`",
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
    render_current(os.path.join(ASSEMBLY_SCREENSHOTS, "s74-exterior-finish-contact-sheet.png"), (0, -190, 62), (0, 0, 54), bbox, focal=70, ortho=160, width=1800, height=1500)


def main():
    print("=== Session 74: Knowledgebase + Chat + Career urban polish wave ===")
    for module in MODULES:
        for key in ("output_blend", "draft_glb", "approved_glb", "app_glb", "metrics", "qa_import"):
            os.makedirs(os.path.dirname(os.path.join(ROOT, module[key])), exist_ok=True)
        os.makedirs(os.path.join(ROOT, module["screenshots"]), exist_ok=True)
    for path in (ASSEMBLY_AUDIT, ASSEMBLY_SCREENSHOTS):
        os.makedirs(path, exist_ok=True)

    pre_audit = audit_all()
    metrics_by_id = {}
    for module in MODULES:
        metrics_path = os.path.join(ROOT, module["metrics"])
        if os.path.exists(metrics_path):
            with open(metrics_path, "r", encoding="utf-8") as handle:
                metrics = json.load(handle)
            if (
                metrics.get("session") == 74
                and metrics.get("budget", {}).get("status") == "APPROVED"
                and len(metrics.get("qa", {}).get("roots", [])) == 1
            ):
                print(f"--- Reusing approved Session 74 metrics: {module['label']} ---")
                metrics_by_id[module["id"]] = metrics
                continue
        metrics_by_id[module["id"]] = build_module(module)
    post_audit = audit_all()
    report_paths = write_wave_report(pre_audit, post_audit, metrics_by_id)
    render_contact_sheet()
    print(f"Report written: {report_paths['md']}")
    for module in MODULES:
        print(f"{module['label']} approved GLB updated: {module['approved_glb']}")


if __name__ == "__main__":
    main()

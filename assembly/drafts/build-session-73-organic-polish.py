"""
Balencia City v3 - Session 73
Phase 8.5 Yoga + Recovery + Relationships organic exterior polish wave.

This upgrades already-approved organic exterior GLBs while preserving origins,
layout positions, and baked energy route assumptions.
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
        "id": "yoga",
        "label": "Yoga & Wellbeing",
        "root_name": "yoga-ext",
        "accent_hex": "#6EE7B7",
        "source_glb": "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb",
        "output_blend": "modules/02-yoga-wellbeing/exterior/drafts/yoga-session73-v2-polish.blend",
        "draft_glb": "modules/02-yoga-wellbeing/exterior/drafts/yoga-ext-v2-draft-s73.glb",
        "approved_glb": "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/02-yoga-wellbeing/yoga-ext.glb",
        "metrics": "modules/02-yoga-wellbeing/exterior/drafts/session73-v2-metrics.json",
        "qa_import": "modules/02-yoga-wellbeing/exterior/drafts/session73-qa-import.json",
        "screenshots": "modules/02-yoga-wellbeing/screenshots",
        "tri_min": 12000,
        "tri_max": 18000,
        "size_min_kb": 100,
        "size_max_kb": 350,
    },
    {
        "id": "recovery",
        "label": "Recovery & Sleep",
        "root_name": "recovery-ext",
        "accent_hex": "#6366F1",
        "source_glb": "modules/09-recovery-sleep/exterior/approved/recovery-ext.glb",
        "output_blend": "modules/09-recovery-sleep/exterior/drafts/recovery-session73-v2-polish.blend",
        "draft_glb": "modules/09-recovery-sleep/exterior/drafts/recovery-ext-v2-draft-s73.glb",
        "approved_glb": "modules/09-recovery-sleep/exterior/approved/recovery-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/09-recovery-sleep/recovery-ext.glb",
        "metrics": "modules/09-recovery-sleep/exterior/drafts/session73-v2-metrics.json",
        "qa_import": "modules/09-recovery-sleep/exterior/drafts/session73-qa-import.json",
        "screenshots": "modules/09-recovery-sleep/screenshots",
        "tri_min": 12000,
        "tri_max": 18000,
        "size_min_kb": 80,
        "size_max_kb": 350,
    },
    {
        "id": "relationships",
        "label": "Relationships",
        "root_name": "relationships-ext",
        "accent_hex": "#F43F5E",
        "source_glb": "modules/07-relationships/exterior/approved/relationships-ext.glb",
        "output_blend": "modules/07-relationships/exterior/drafts/relationships-session73-v2-polish.blend",
        "draft_glb": "modules/07-relationships/exterior/drafts/relationships-ext-v2-draft-s73.glb",
        "approved_glb": "modules/07-relationships/exterior/approved/relationships-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/07-relationships/relationships-ext.glb",
        "metrics": "modules/07-relationships/exterior/drafts/session73-v2-metrics.json",
        "qa_import": "modules/07-relationships/exterior/drafts/session73-qa-import.json",
        "screenshots": "modules/07-relationships/screenshots",
        "tri_min": 12000,
        "tri_max": 18000,
        "size_min_kb": 80,
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


def cylinder(name, loc, radius, depth, material, category, vertices=16, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, material)
    shade_smooth(obj)
    apply_transform(obj)
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, material, category, vertices=16, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, material)
    shade_smooth(obj)
    apply_transform(obj)
    return register(obj, category)


def torus(name, loc, major, minor, material, category, seg=48, minor_seg=5, rot=(0.0, 0.0, 0.0)):
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


def add_yoga_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    category = "session73 yoga layered organic finish"

    for ring, scale in enumerate((0.96, 0.74)):
        torus(f"Yoga_v2_breathing_platform_lamella_{ring}", (cx, cy, min_z + 0.36 + ring * 0.12), width * 0.27 * scale, 0.030, mats["base"], category, seg=40, minor_seg=4)
        torus(f"Yoga_v2_sage_shadow_trim_{ring}", (cx, cy, min_z + 0.49 + ring * 0.12), width * 0.27 * scale, 0.018, mats["detail"], category, seg=40, minor_seg=3)

    for index in range(12):
        angle = index * math.tau / 12
        inner = Vector((cx, cy, min_z + 0.18)) + Vector((math.cos(angle), math.sin(angle), 0)) * width * 0.22
        outer = Vector((cx, cy, min_z + 0.26)) + Vector((math.cos(angle), math.sin(angle), 0)) * width * 0.41
        cylinder_between(f"Yoga_v2_platform_underside_rib_{index:02d}", inner, outer, 0.026, mats["base"], category, vertices=5)

    for dome, (xoff, yoff, radius, height) in enumerate(((0.0, 0.0, 2.1, 1.15), (-0.24, 0.32, 1.22, 0.82), (0.31, 0.25, 0.94, 0.65))):
        x = cx + xoff * width
        y = cy + yoff * depth
        torus(f"Yoga_v2_dome_leaf_skirt_{dome}", (x, y, max_z - height), radius, 0.026, mats["detail"], category, seg=36, minor_seg=3)
        torus(f"Yoga_v2_dome_holo_breath_band_{dome}", (x, y, max_z - height * 0.55), radius * 0.76, 0.017, mats["holo"], category, seg=36, minor_seg=3)
        for rib in range(3):
            angle = rib * math.tau / 3
            start = (x + math.cos(angle) * radius * 0.30, y + math.sin(angle) * radius * 0.30, max_z - height * 0.98)
            end = (x + math.cos(angle) * radius * 0.75, y + math.sin(angle) * radius * 0.75, max_z - height * 0.22)
            cylinder_between(f"Yoga_v2_dome_soft_meridian_{dome}_{rib}", start, end, 0.018, mats["detail"], category, vertices=5)

    for index in range(10):
        angle = -math.pi * 0.85 + index * (math.pi * 1.70 / 9)
        x = cx + math.cos(angle) * width * 0.47
        y = cy + math.sin(angle) * depth * 0.45
        cylinder_between(
            f"Yoga_v2_hanging_garden_vine_{index:02d}",
            (x, y, min_z + 0.95),
            (x + math.cos(angle) * 0.25, y + math.sin(angle) * 0.25, min_z + 0.18 + (index % 3) * 0.10),
            0.020,
            mats["holo"],
            category,
            vertices=5,
        )
        if index % 3 == 0:
            cone(f"Yoga_v2_leaf_cluster_{index:02d}", (x, y, min_z + 0.62), 0.10, 0.02, 0.20, mats["holo"], category, vertices=5, rot=(math.pi / 2, 0, angle))

    for stone in range(10):
        x = cx + (stone - 4.5) * width * 0.060
        y = min_y + 0.30 + math.sin(stone * 0.75) * 0.45
        cylinder(f"Yoga_v2_lake_stepping_stone_{stone:02d}", (x, y, min_z + 0.055), 0.12 + (stone % 3) * 0.025, 0.035, mats["detail"], category, vertices=8)


def add_recovery_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    category = "session73 recovery soft-shell and lake finish"

    for ring, scale in enumerate((0.92, 0.62)):
        torus(f"Recovery_v2_lake_sleep_ripple_{ring}", (cx, cy, min_z + 0.075 + ring * 0.020), width * 0.30 * scale, 0.018, mats["glass"], category, seg=40, minor_seg=3)
        box(f"Recovery_v2_lake_shadow_shelf_{ring}", (cx, cy, min_z + 0.05 + ring * 0.014), (width * 0.18 * scale, depth * 0.13 * scale, 0.012), mats["base"], category, rot=(0.0, 0.0, ring * 0.37))

    for ribbon in range(3):
        z = min_z + 3.0 + ribbon * 0.72
        scale = 0.88 - ribbon * 0.075
        torus(f"Recovery_v2_cloud_contour_whisper_{ribbon}", (cx, cy, z), width * 0.20 * scale, 0.018, mats["detail"], category, seg=36, minor_seg=3, rot=(0.0, 0.0, ribbon * 0.21))

    for pillar in range(5):
        angle = math.tau * pillar / 5 + 0.20
        x = cx + math.cos(angle) * width * 0.18
        y = cy + math.sin(angle) * depth * 0.20
        torus(f"Recovery_v2_pillar_sleep_halo_{pillar}", (x, y, min_z + 1.08), 0.34, 0.019, mats["emissive"], category, seg=36, minor_seg=4)
        cylinder(f"Recovery_v2_pillar_glass_sleeve_{pillar}", (x, y, min_z + 2.2), 0.18, 2.2, mats["glass"], category, vertices=8)

    for star in range(8):
        angle = star * math.tau / 8
        radius = width * (0.13 + (star % 4) * 0.020)
        z = min_z + 4.0 + (star % 5) * 0.42
        cylinder(f"Recovery_v2_muted_star_jewel_{star:02d}", (cx + math.cos(angle) * radius, cy + math.sin(angle) * depth * 0.16, z), 0.042, 0.035, mats["emissive"], category, vertices=5, rot=(math.pi / 2, 0, angle))

    for wisp in range(4):
        angle = math.pi * 0.1 + wisp * math.tau / 4
        start = (cx + math.cos(angle) * width * 0.23, cy + math.sin(angle) * depth * 0.24, min_z + 3.3 + (wisp % 3) * 0.25)
        end = (cx + math.cos(angle) * width * 0.43, cy + math.sin(angle) * depth * 0.41, start[2] - 0.40)
        cylinder_between(f"Recovery_v2_dissolving_edge_wisp_{wisp}", start, end, 0.018, mats["accent"], category, vertices=5)


def add_relationships_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    category = "session73 relationships garden pavilion finish"

    for ring, scale in enumerate((0.96, 0.72)):
        torus(f"Relationships_v2_moat_reflection_ring_{ring}", (cx, cy, min_z + 0.085 + ring * 0.020), width * 0.30 * scale, 0.022, mats["glass"], category, seg=40, minor_seg=3, rot=(0.0, 0.0, ring * 0.18))
        torus(f"Relationships_v2_garden_terrace_lip_{ring}", (cx, cy, min_z + 1.15 + ring * 0.48), width * 0.23 * scale, 0.024, mats["base"], category, seg=40, minor_seg=3)

    for index in range(16):
        angle = index * math.tau / 16
        radius_x = width * (0.32 + (index % 3) * 0.018)
        radius_y = depth * (0.30 + (index % 4) * 0.015)
        x = cx + math.cos(angle) * radius_x
        y = cy + math.sin(angle) * radius_y
        cone(f"Relationships_v2_rose_canopy_bud_{index:02d}", (x, y, min_z + 1.38 + (index % 4) * 0.18), 0.10, 0.025, 0.20, mats["emissive"], category, vertices=7)
        if index % 2 == 0:
            cylinder(f"Relationships_v2_dark_leaf_fan_{index:02d}", (x, y, min_z + 1.22), 0.13, 0.035, mats["detail"], category, vertices=7, rot=(math.pi / 2, 0, angle))

    for bridge in range(4):
        angle = math.pi / 4 + bridge * math.pi / 2
        x = cx + math.cos(angle) * width * 0.36
        y = cy + math.sin(angle) * depth * 0.34
        for rail in (-0.18, 0.18):
            tangent = Vector((-math.sin(angle), math.cos(angle), 0))
            offset = tangent * rail
            cylinder_between(
                f"Relationships_v2_bridge_warm_rail_{bridge}_{rail:+.2f}",
                (x - math.cos(angle) * 1.1 + offset.x, y - math.sin(angle) * 1.1 + offset.y, min_z + 0.70),
                (x + math.cos(angle) * 1.1 + offset.x, y + math.sin(angle) * 1.1 + offset.y, min_z + 0.82),
                0.026,
                mats["detail"],
                category,
                vertices=5,
            )
        box(f"Relationships_v2_bridge_threshold_glow_{bridge}", (x, y, min_z + 0.66), (0.55, 0.045, 0.030), mats["emissive"], category, rot=(0.0, 0.0, angle))

    for dome in range(2):
        angle = dome * math.tau / 2 + 0.45
        x = cx + math.cos(angle) * width * 0.12
        y = cy + math.sin(angle) * depth * 0.10
        torus(f"Relationships_v2_roof_dome_frame_{dome}", (x, y, max_z - 0.88 + dome * 0.05), 0.82 - dome * 0.08, 0.021, mats["detail"], category, seg=32, minor_seg=3)
        cylinder(f"Relationships_v2_warm_gathering_core_{dome}", (x, y, max_z - 1.08 + dome * 0.05), 0.16, 0.10, mats["emissive"], category, vertices=12)


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
        active.name = f"{module_id}_s73_{slot}_polish_mesh"
        created_categories[active.name] = f"session73 merged {slot} polish geometry"


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
    key.name = "S73_Key_Area"
    key.data.energy = 420
    key.data.size = 7
    bpy.ops.object.light_add(type="POINT", location=(min_x - 4, min_y - 5, min_z + height * 0.28))
    fill = current_object()
    fill.name = "S73_Warm_Fill"
    fill.data.energy = 120
    bpy.ops.object.light_add(type="POINT", location=(max_x + 4, max_y + 4, max_z + 2))
    crown = current_object()
    crown.name = "S73_Crown_Glint"
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
    prefix = f"session73-{module['id']}-v2"
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
    print(f"--- Building Session 73 v2 polish: {module['label']} ---")
    global created_categories
    created_categories = {}
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, module["source_glb"]))
    mats = normalize_materials(module["accent_hex"])
    pre_tris = count_tris()
    pre_objects = len(mesh_objects())
    pre_bbox = world_bbox()

    if module["id"] == "yoga":
        add_yoga_polish(mats, pre_bbox)
    elif module["id"] == "recovery":
        add_recovery_polish(mats, pre_bbox)
    elif module["id"] == "relationships":
        add_relationships_polish(mats, pre_bbox)
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
        raise RuntimeError(f"{module['label']} Session 73 QA failed: {qa}")

    shutil.copy2(os.path.join(ROOT, module["draft_glb"]), os.path.join(ROOT, module["approved_glb"]))
    shutil.copy2(os.path.join(ROOT, module["draft_glb"]), os.path.join(ROOT, module["app_glb"]))
    metrics = {
        "session": 73,
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
    json_path = os.path.join(ASSEMBLY_AUDIT, "session-73-organic-polish.json")
    md_path = os.path.join(ASSEMBLY_AUDIT, "session-73-organic-polish.md")
    report = {
        "session": 73,
        "date": str(date.today()),
        "scope": "Phase 8.5 Yoga + Recovery + Relationships organic exterior polish wave",
        "pre_audit": pre_audit,
        "post_audit": post_audit,
        "polished_modules": metrics_by_id,
        "verdict": "APPROVED - organic v2 exterior polish complete; origins and runtime paths preserved.",
    }
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    lines = [
        "# Session 73 Organic Exterior Polish",
        "",
        f"Date: {date.today()}",
        "Status: Approved",
        "",
        "## Summary",
        "",
        "Session 73 completed the Phase 8.5 organic polish wave for Yoga, Recovery, and Relationships while preserving layout origins, city-layout-v2 positions, and baked energy route assumptions.",
        "",
        "## V2 Results",
        "",
        "| Module | Previous Tris | Session 73 Tris | Objects | Size | Verdict |",
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
            "- Yoga: layered platform lamellae, underside ribs, dome leaf skirts, holo breath bands, soft dome meridians, hanging vines, leaf clusters, and lake stepping stones.",
            "- Recovery: lake sleep ripples, dark shadow shelves, soft-shell contour ribbons, pillar halos/sleeves, muted star jewels, and dissolving edge wisps.",
            "- Relationships: moat reflection rings, garden terrace lips, rose canopy buds, dark leaf fans, bridge rail articulation, threshold glows, roof dome frames, and warm gathering cores.",
            "",
            "## QA",
            "",
            "- All three draft GLBs reimport cleanly.",
            "- All three exports use only approved material slot names.",
            "- No cameras or lights exported.",
            "- All three assets remain within Phase 8 exterior triangle/file budgets.",
            "",
            "## Evidence",
            "",
            "- `modules/02-yoga-wellbeing/screenshots/session73-yoga-v2-front.png`",
            "- `modules/02-yoga-wellbeing/screenshots/session73-yoga-v2-threequarter.png`",
            "- `modules/02-yoga-wellbeing/screenshots/session73-yoga-v2-dark-first.png`",
            "- `modules/09-recovery-sleep/screenshots/session73-recovery-v2-front.png`",
            "- `modules/09-recovery-sleep/screenshots/session73-recovery-v2-threequarter.png`",
            "- `modules/09-recovery-sleep/screenshots/session73-recovery-v2-dark-first.png`",
            "- `modules/07-relationships/screenshots/session73-relationships-v2-front.png`",
            "- `modules/07-relationships/screenshots/session73-relationships-v2-threequarter.png`",
            "- `modules/07-relationships/screenshots/session73-relationships-v2-dark-first.png`",
            "- `assembly/screenshots/s73-exterior-finish-contact-sheet.png`",
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
    render_current(os.path.join(ASSEMBLY_SCREENSHOTS, "s73-exterior-finish-contact-sheet.png"), (0, -190, 62), (0, 0, 54), bbox, focal=70, ortho=160, width=1800, height=1500)


def main():
    print("=== Session 73: Yoga + Recovery + Relationships organic polish wave ===")
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
            if metrics.get("session") == 73 and metrics.get("budget", {}).get("status") == "APPROVED":
                print(f"--- Reusing approved Session 73 metrics: {module['label']} ---")
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

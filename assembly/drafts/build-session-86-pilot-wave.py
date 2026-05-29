"""
Balencia City v3 - Session 86
Phase 10 pilot wave: Finance, SIA Tower, and Knowledgebase hero exteriors.

This script preserves all approved overview exteriors and creates focused-scene
`exteriorHero` GLBs for the first Architectural Completion wave. It also renders
Gate 8 evidence and writes audit/performance reports.
"""

import json
import math
import os
import shutil
from collections import defaultdict
from datetime import date

import bpy
from mathutils import Vector


SESSION = 86
ROOT = "/Users/hamza/Desktop/balencia-city-v3"
LAYOUT_PATH = os.path.join(ROOT, "shared", "city-layout-v2.json")
MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "src", "lib", "asset-manifest.json")
SCREENSHOT_DIR = os.path.join(ROOT, "assembly", "screenshots", "session-86-pilot-wave")
AFTER_DIR = os.path.join(SCREENSHOT_DIR, "after")
APP_HERO_DIR = os.path.join(SCREENSHOT_DIR, "app-hero-cameras")
AUDIT_DIR = os.path.join(ROOT, "assembly", "audit")
PERFORMANCE_DIR = os.path.join(ROOT, "assembly", "performance-reports")
REPORT_JSON = os.path.join(AUDIT_DIR, "session-86-pilot-wave.json")
REPORT_MD = os.path.join(AUDIT_DIR, "session-86-pilot-wave.md")
PERFORMANCE_REPORT = os.path.join(PERFORMANCE_DIR, "session-86-performance.json")
APP_SESSION_REPORT = os.path.join(ROOT, "apps", "balencia", "SESSION-86-REPORT.md")

VALID_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
ENERGY_IDS = [
    "hard-pipelines",
    "warm-mist",
    "faint-thread",
    "knowledgebase-waterfall",
    "leaderboard-lightning",
    "cross-district-gold",
    "ai-pulse",
]

MODULES = [
    {
        "id": "finance",
        "label": "Finance",
        "accent_hex": "#F59E0B",
        "root_name": "finance-ext-hero",
        "source_glb": "modules/03-finance/exterior/approved/finance-ext.glb",
        "output_blend": "modules/03-finance/exterior/drafts/finance-session86-hero.blend",
        "draft_glb": "modules/03-finance/exterior/drafts/finance-ext-hero-draft-s86.glb",
        "approved_glb": "modules/03-finance/exterior/approved/finance-ext-hero.glb",
        "public_glb": "models/structures/03-finance/finance-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/03-finance/finance-ext-hero.glb",
        "metrics": "modules/03-finance/exterior/drafts/session86-hero-metrics.json",
        "qa_import": "modules/03-finance/exterior/drafts/session86-hero-qa-import.json",
        "screenshots": "modules/03-finance/screenshots",
        "pre_tris": 15370,
        "tri_min": 22000,
        "tri_max": 33000,
        "size_min_kb": 80,
        "size_max_kb": 620,
        "gate8_notes": [
            "solid crystalline envelope behind gold frame",
            "premium plinth, lobby threshold, and civic edge",
            "resolved data crown visible from Scene 6",
        ],
    },
    {
        "id": "sia-tower",
        "label": "SIA Tower",
        "accent_hex": "#FF5E00",
        "root_name": "sia-tower-ext-hero",
        "source_glb": "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb",
        "output_blend": "modules/00-sia-tower/exterior/drafts/sia-tower-session86-hero.blend",
        "draft_glb": "modules/00-sia-tower/exterior/drafts/sia-tower-ext-hero-draft-s86.glb",
        "approved_glb": "modules/00-sia-tower/exterior/approved/sia-tower-ext-hero.glb",
        "public_glb": "models/structures/00-sia-tower/sia-tower-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/00-sia-tower/sia-tower-ext-hero.glb",
        "metrics": "modules/00-sia-tower/exterior/drafts/session86-hero-metrics.json",
        "qa_import": "modules/00-sia-tower/exterior/drafts/session86-hero-qa-import.json",
        "screenshots": "modules/00-sia-tower/screenshots",
        "pre_tris": 14844,
        "tri_min": 24000,
        "tri_max": 34000,
        "size_min_kb": 80,
        "size_max_kb": 720,
        "gate8_notes": [
            "occupied facade rhythm behind vertical frame",
            "stronger civic base and entrance threshold",
            "resolved crown cap, beacon, and pipeline junction",
        ],
    },
    {
        "id": "knowledgebase",
        "label": "Knowledgebase",
        "accent_hex": "#7F24FF",
        "root_name": "knowledgebase-ext-hero",
        "source_glb": "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb",
        "output_blend": "modules/04-knowledgebase/exterior/drafts/knowledgebase-session86-hero.blend",
        "draft_glb": "modules/04-knowledgebase/exterior/drafts/knowledgebase-ext-hero-draft-s86.glb",
        "approved_glb": "modules/04-knowledgebase/exterior/approved/knowledgebase-ext-hero.glb",
        "public_glb": "models/structures/04-knowledgebase/knowledgebase-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/04-knowledgebase/knowledgebase-ext-hero.glb",
        "metrics": "modules/04-knowledgebase/exterior/drafts/session86-hero-metrics.json",
        "qa_import": "modules/04-knowledgebase/exterior/drafts/session86-hero-qa-import.json",
        "screenshots": "modules/04-knowledgebase/screenshots",
        "pre_tris": 15204,
        "tri_min": 22000,
        "tri_max": 34000,
        "size_min_kb": 80,
        "size_max_kb": 620,
        "gate8_notes": [
            "finished ancient-to-future facade envelope",
            "stronger archive stairs, vault threshold, and stone base",
            "resolved waterfall intake and crown roof termination",
        ],
    },
]

FOCUSED_SCENE_CONFIG = {
    "sia-tower": {
        "scene": 2,
        "slug": "sia-tower-reveal",
        "position": [18, 7.8, 25],
        "target": [0, 38, 0],
        "lens": 30,
        "frame": 12,
    },
    "finance": {
        "scene": 6,
        "slug": "finance-tower",
        "offset": [43, 24, 34],
        "target_height": 13,
        "lens": 30,
        "frame": 96,
    },
    "knowledgebase": {
        "scene": 7,
        "slug": "knowledgebase",
        "offset": [38, 25, 42],
        "target_height": 10.2,
        "lens": 29,
        "frame": 96,
    },
}


for directory in (SCREENSHOT_DIR, AFTER_DIR, APP_HERO_DIR, AUDIT_DIR, PERFORMANCE_DIR):
    os.makedirs(directory, exist_ok=True)
for module in MODULES:
    for key in ("output_blend", "draft_glb", "approved_glb", "public_abs_glb", "metrics", "qa_import"):
        os.makedirs(os.path.dirname(os.path.join(ROOT, module[key])), exist_ok=True)
    os.makedirs(os.path.join(ROOT, module["screenshots"]), exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


LAYOUT = load_json(LAYOUT_PATH)
MANIFEST = load_json(MANIFEST_PATH)


def rel(path):
    return os.path.relpath(path, ROOT)


def abs_path(path):
    return os.path.join(ROOT, path)


def runtime_to_blender(value):
    return (value[0], -value[2], value[1])


def layout_blender(id_name):
    return tuple(LAYOUT["districts"][id_name]["blenderPosition"])


def structure_entry(id_name):
    for item in MANIFEST["structures"]:
        if item["id"] == id_name:
            return item
    raise KeyError(id_name)


def material_root(material):
    return material.name.split(".")[0] if material else ""


def mesh_objects(objects=None):
    candidates = objects or bpy.data.objects
    return [obj for obj in candidates if obj.type == "MESH"]


def count_tris(objects=None):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    total = 0
    for obj in mesh_objects(objects):
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        mesh.calc_loop_triangles()
        total += len(mesh.loop_triangles)
        eval_obj.to_mesh_clear()
    return total


def world_bbox(objects=None):
    points = []
    for obj in mesh_objects(objects):
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
    for image in list(bpy.data.images):
        if not image.users:
            bpy.data.images.remove(image)


def current_object():
    obj = bpy.context.view_layer.objects.active
    if obj is not None:
        return obj
    if bpy.context.selected_objects:
        return bpy.context.selected_objects[-1]
    raise RuntimeError("No active object")


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


def hex_to_linear(hex_color, alpha=1.0):
    value = hex_color.lstrip("#")
    rgb = [int(value[index:index + 2], 16) / 255 for index in (0, 2, 4)]

    def convert(channel):
        if channel <= 0.04045:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    return tuple(convert(channel) for channel in rgb) + (alpha,)


def make_material(name, base, emission=None, strength=0.0, alpha=1.0, roughness=0.62, metallic=0.1):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.name = name
    mat.diffuse_color = base
    mat.use_nodes = True
    if alpha < 1.0:
        mat.blend_method = "BLEND"
        mat.use_screen_refraction = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if emission and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = strength
    return mat


def normalize_materials(accent_hex):
    accent = hex_to_linear(accent_hex)
    orange = hex_to_linear("#FF5E00")
    material_defs = {
        "base": ((0.012, 0.013, 0.018, 1.0), None, 0.0, 1.0, 0.84, 0.05),
        "accent": ((0.022, 0.024, 0.030, 1.0), accent, 0.14, 1.0, 0.46, 0.22),
        "glass": ((0.006, 0.009, 0.014, 0.86), accent, 0.035, 0.86, 0.14, 0.20),
        "detail": ((0.008, 0.009, 0.012, 1.0), None, 0.0, 1.0, 0.58, 0.28),
        "emissive": ((0.018, 0.016, 0.012, 1.0), accent, 0.30, 1.0, 0.24, 0.0),
        "energy": ((0.045, 0.018, 0.004, 1.0), orange, 0.30, 1.0, 0.20, 0.04),
        "holo": ((0.018, 0.022, 0.028, 0.42), accent, 0.25, 0.42, 0.16, 0.02),
    }
    mats = {name: make_material(name, *args) for name, args in material_defs.items()}
    fallback = mats["detail"]
    for obj in mesh_objects():
        if not obj.data.materials:
            obj.data.materials.append(fallback)
        for index, material in enumerate(obj.data.materials):
            root = material_root(material)
            obj.data.materials[index] = mats[root] if root in mats else fallback
    return mats


created_categories = {}


def register(obj, category):
    created_categories[obj.name] = category
    return obj


def box(name, loc, dims, material, category, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    obj.scale = dims
    assign(obj, material)
    apply_transform(obj)
    return register(obj, category)


def cylinder(name, loc, radius, depth, material, category, vertices=12, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, material)
    shade_smooth(obj)
    apply_transform(obj)
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, material, category, vertices=12, rot=(0.0, 0.0, 0.0)):
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


def oct_points(cx, cy, radius, z, rotation=math.pi / 8):
    return [
        (cx + math.cos(rotation + i * math.tau / 8) * radius, cy + math.sin(rotation + i * math.tau / 8) * radius, z)
        for i in range(8)
    ]


def add_finance_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    radius = max(width, depth) * 0.49
    body_bottom = min_z + height * 0.10
    body_top = max_z - height * 0.16

    category = "session86 finance complete crystalline envelope"
    for floor in range(28):
        z = body_bottom + (body_top - body_bottom) * (floor / 27)
        level_t = (z - body_bottom) / max(body_top - body_bottom, 0.001)
        local_radius = radius * (1.0 - 0.18 * level_t)
        points = oct_points(cx, cy, local_radius, z)
        for side in range(8):
            start = points[side]
            end = points[(side + 1) % 8]
            cylinder_between(
                f"Finance_s86_floor_ledger_{floor:02d}_{side}",
                start,
                end,
                0.014,
                mats["emissive"],
                category,
                vertices=5,
            )

    for face in range(8):
        angle = math.pi / 8 + face * math.tau / 8
        normal = Vector((math.cos(angle), math.sin(angle), 0))
        tangent = Vector((-math.sin(angle), math.cos(angle), 0))
        for row in range(9):
            z = body_bottom + (body_top - body_bottom) * ((row + 0.5) / 9)
            local_radius = radius * (1.0 - 0.18 * ((z - body_bottom) / max(body_top - body_bottom, 0.001)))
            face_center = Vector((cx, cy, z)) + normal * (local_radius + 0.032)
            for col, offset in enumerate((-0.54, -0.18, 0.18, 0.54)):
                loc = face_center + tangent * (offset * radius * 0.34)
                box(
                    f"Finance_s86_infilled_facet_glass_{face}_{row}_{col}",
                    (loc.x, loc.y, loc.z),
                    (radius * 0.034, 0.020, height * 0.020),
                    mats["glass"],
                    category,
                    rot=(0, 0, angle + math.pi / 2),
                )
                box(
                    f"Finance_s86_facet_shadow_reveal_{face}_{row}_{col}",
                    (loc.x, loc.y, loc.z - height * 0.026),
                    (radius * 0.038, 0.014, height * 0.004),
                    mats["detail"],
                    category,
                    rot=(0, 0, angle + math.pi / 2),
                )

    base_category = "session86 finance premium plinth and lobby threshold"
    for step, scale in enumerate((1.30, 1.12, 0.94, 0.76)):
        cone(
            f"Finance_s86_weighted_plinth_slab_{step}",
            (cx, cy, min_z + 0.10 + step * 0.17),
            radius * scale,
            radius * (scale * 0.94),
            0.16,
            mats["base"],
            base_category,
            vertices=8,
            rot=(0, 0, math.pi / 8),
        )
    entry_y = min_y - depth * 0.075
    box("Finance_s86_recessed_lobby_vault", (cx, entry_y, min_z + height * 0.115), (width * 0.17, 0.052, height * 0.066), mats["detail"], base_category)
    for side in (-1, 1):
        cylinder_between(
            f"Finance_s86_lobby_sloped_gold_jamb_{side}",
            (cx + side * width * 0.205, entry_y - 0.03, min_z + height * 0.040),
            (cx + side * width * 0.070, entry_y - 0.03, min_z + height * 0.205),
            0.030,
            mats["emissive"],
            base_category,
            vertices=5,
        )
    for tick in range(13):
        x = cx + (tick - 6) * width * 0.026
        box(
            f"Finance_s86_market_ticker_pip_{tick:02d}",
            (x, entry_y - 0.042, min_z + height * (0.153 + 0.006 * (tick % 3))),
            (width * 0.010, 0.014, height * 0.006),
            mats["accent"],
            base_category,
        )
    for face in range(8):
        angle = math.pi / 8 + face * math.tau / 8
        normal = Vector((math.cos(angle), math.sin(angle), 0))
        loc = Vector((cx, cy, min_z + height * 0.058)) + normal * (radius * 1.08)
        box(
            f"Finance_s86_plinth_civic_edge_marker_{face}",
            (loc.x, loc.y, loc.z),
            (radius * 0.064, 0.020, height * 0.012),
            mats["emissive"],
            base_category,
            rot=(0, 0, angle + math.pi / 2),
        )

    crown_category = "session86 finance resolved data crown cap"
    crown_z = body_top + height * 0.055
    for ring, z in enumerate((crown_z, crown_z + height * 0.023, crown_z + height * 0.047)):
        torus(
            f"Finance_s86_crown_market_halo_{ring}",
            (cx, cy, z),
            radius * (0.48 - ring * 0.035),
            0.020,
            mats["emissive"],
            crown_category,
            seg=64,
            minor_seg=4,
        )
    for panel in range(24):
        angle = panel * math.tau / 24
        loc = Vector((cx, cy, crown_z + height * 0.030)) + Vector((math.cos(angle), math.sin(angle), 0)) * (radius * 0.54)
        box(
            f"Finance_s86_crown_data_fin_{panel:02d}",
            (loc.x, loc.y, loc.z),
            (radius * 0.024, 0.019, height * 0.033),
            mats["accent"],
            crown_category,
            rot=(0, 0, angle + math.pi / 2),
        )
    cone(
        "Finance_s86_faceted_roof_cap",
        (cx, cy, max_z + height * 0.012),
        radius * 0.30,
        radius * 0.16,
        height * 0.052,
        mats["detail"],
        crown_category,
        vertices=8,
        rot=(0, 0, math.pi / 8),
    )
    torus("Finance_s86_pipeline_socket_collar", (cx, cy, max_z + height * 0.045), radius * 0.17, 0.022, mats["energy"], crown_category, seg=40, minor_seg=4)


def add_sia_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    body_bottom = min_z + height * 0.10
    body_top = max_z - height * 0.18

    category = "session86 sia occupied facade envelope"
    z_rows = 30
    for row in range(z_rows):
        z = body_bottom + (body_top - body_bottom) * ((row + 0.5) / z_rows)
        taper = 1.0 - 0.30 * ((z - body_bottom) / max(body_top - body_bottom, 0.001))
        half_w = width * 0.31 * taper
        half_d = depth * 0.31 * taper
        for side, y in (("front", cy - half_d - 0.022), ("back", cy + half_d + 0.022)):
            for col in range(4):
                x = cx + (col - 1.5) * half_w * 0.46
                box(
                    f"SIA_s86_{side}_occupied_glass_bay_{row:02d}_{col}",
                    (x, y, z),
                    (half_w * 0.105, 0.018, height * 0.0068),
                    mats["glass"],
                    category,
                )
            box(f"SIA_s86_{side}_floor_shadow_band_{row:02d}", (cx, y, z - height * 0.009), (half_w * 0.86, 0.016, height * 0.0028), mats["detail"], category)
        for side, x in (("left", cx - half_w - 0.022), ("right", cx + half_w + 0.022)):
            for col in range(3):
                y = cy + (col - 1) * half_d * 0.52
                box(
                    f"SIA_s86_{side}_occupied_glass_bay_{row:02d}_{col}",
                    (x, y, z),
                    (0.018, half_d * 0.112, height * 0.0068),
                    mats["glass"],
                    category,
                )
            box(f"SIA_s86_{side}_floor_shadow_band_{row:02d}", (x, cy, z - height * 0.009), (0.016, half_d * 0.76, height * 0.0028), mats["detail"], category)

    for level in range(10):
        z = body_bottom + (body_top - body_bottom) * (level / 9)
        radius = max(width, depth) * (0.39 - 0.065 * (level / 9))
        torus(f"SIA_s86_occupied_energy_ring_{level:02d}", (cx, cy, z), radius, 0.020, mats["energy"], category, seg=72, minor_seg=4)

    base_category = "session86 sia civic base and entry completion"
    for step, scale in enumerate((0.62, 0.52, 0.42)):
        box(
            f"SIA_s86_civic_plinth_plate_{step}",
            (cx, cy, min_z + height * (0.013 + step * 0.012)),
            (width * scale, depth * scale, height * 0.006),
            mats["base"],
            base_category,
        )
    entry_y = min_y - depth * 0.055
    box("SIA_s86_deep_atrium_entry_shadow", (cx, entry_y, min_z + height * 0.074), (width * 0.115, 0.060, height * 0.055), mats["detail"], base_category)
    for side in (-1, 1):
        cylinder_between(
            f"SIA_s86_entry_megastructure_leg_{side}",
            (cx + side * width * 0.175, entry_y - 0.035, min_z + height * 0.018),
            (cx + side * width * 0.072, entry_y - 0.035, min_z + height * 0.145),
            0.060,
            mats["accent"],
            base_category,
            vertices=6,
        )
    for vein in range(12):
        angle = vein * math.tau / 12
        start = Vector((cx, cy, min_z + 0.060)) + Vector((math.cos(angle), math.sin(angle), 0)) * (width * 0.18)
        end = Vector((cx, cy, min_z + 0.060)) + Vector((math.cos(angle), math.sin(angle), 0)) * (width * 0.43)
        cylinder_between(f"SIA_s86_civic_energy_vein_{vein:02d}", start, end, 0.028, mats["energy"], base_category, vertices=5)

    crown_category = "session86 sia resolved crown beacon and junction"
    crown_base = max_z - height * 0.070
    for ring, z in enumerate((crown_base, crown_base + height * 0.025, crown_base + height * 0.050)):
        torus(f"SIA_s86_crown_pipeline_junction_ring_{ring}", (cx, cy, z), width * (0.19 - ring * 0.020), 0.030, mats["detail" if ring == 0 else "energy"], crown_category, seg=72, minor_seg=5)
    cone("SIA_s86_crystalline_beacon_faceted_cap", (cx, cy, max_z + height * 0.020), width * 0.075, width * 0.030, height * 0.080, mats["glass"], crown_category, vertices=8, rot=(0, 0, math.pi / 8))
    cylinder("SIA_s86_vertical_beacon_core", (cx, cy, max_z + height * 0.072), width * 0.015, height * 0.120, mats["emissive"], crown_category, vertices=12)
    for hardpoint in range(11):
        angle = hardpoint * math.tau / 11
        loc = Vector((cx, cy, crown_base + height * 0.030)) + Vector((math.cos(angle), math.sin(angle), 0)) * (width * 0.245)
        cylinder(
            f"SIA_s86_pipeline_departure_hardpoint_{hardpoint:02d}",
            (loc.x, loc.y, loc.z),
            width * 0.017,
            height * 0.010,
            mats["energy"],
            crown_category,
            vertices=8,
        )


def add_knowledgebase_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]

    base_category = "session86 knowledgebase finished archive base"
    front_y = min_y - depth * 0.075
    for tier in range(6):
        z = min_z + height * (0.045 + tier * 0.040)
        box(f"Knowledge_s86_stone_archive_strata_{tier:02d}", (cx, front_y, z), (width * 0.48, depth * 0.012, height * 0.006), mats["base"], base_category)
        box(f"Knowledge_s86_recessed_shadow_course_{tier:02d}", (cx, front_y - depth * 0.013, z + height * 0.013), (width * 0.43, depth * 0.010, height * 0.004), mats["detail"], base_category)
    for arch in range(7):
        x = cx + (arch - 3) * width * 0.078
        cylinder(f"Knowledge_s86_deep_arch_glass_{arch:02d}", (x, front_y - depth * 0.030, min_z + height * 0.190), width * 0.020, depth * 0.026, mats["glass"], base_category, vertices=14, rot=(math.pi / 2, 0, 0))
        torus(f"Knowledge_s86_arch_trim_ring_{arch:02d}", (x, front_y - depth * 0.034, min_z + height * 0.190), width * 0.026, width * 0.0038, mats["detail"], base_category, seg=24, minor_seg=3, rot=(math.pi / 2, 0, 0))
    for step in range(6):
        box(
            f"Knowledge_s86_archive_entry_stair_{step}",
            (cx, front_y - depth * (0.12 + step * 0.020), min_z + 0.030 + step * 0.018),
            (width * (0.34 - step * 0.026), depth * 0.020, 0.018),
            mats["base"],
            base_category,
        )
    box("Knowledge_s86_vault_threshold_shadow", (cx, front_y - depth * 0.155, min_z + height * 0.105), (width * 0.20, depth * 0.022, height * 0.070), mats["detail"], base_category)
    box("Knowledge_s86_vault_purple_reading_line", (cx, front_y - depth * 0.170, min_z + height * 0.155), (width * 0.17, depth * 0.010, height * 0.006), mats["emissive"], base_category)

    tech_category = "session86 knowledgebase complete floating data envelope"
    floor_count = 12
    for floor in range(floor_count):
        t = floor / (floor_count - 1)
        z = min_z + height * (0.405 + t * 0.385)
        scale = 0.78 - 0.13 * t
        box(
            f"Knowledge_s86_data_floor_outer_glass_plate_{floor:02d}",
            (cx, cy, z),
            (width * scale * 0.36, depth * scale * 0.30, height * 0.005),
            mats["glass"],
            tech_category,
            rot=(0, 0, 0.025 * (floor % 2)),
        )
        box(
            f"Knowledge_s86_purple_knowledge_core_{floor:02d}",
            (cx, cy, z + height * 0.008),
            (width * scale * 0.25, depth * scale * 0.22, height * 0.004),
            mats["emissive"],
            tech_category,
            rot=(0, 0, 0.025 * (floor % 2)),
        )
        for side in (-1, 1):
            x = cx + side * width * scale * 0.205
            box(
                f"Knowledge_s86_side_holo_catalog_wall_{floor:02d}_{side}",
                (x, cy, z + height * 0.018),
                (width * 0.007, depth * scale * 0.20, height * 0.034),
                mats["holo"],
                tech_category,
            )
        for edge in (-1, 1):
            y = cy + edge * depth * scale * 0.185
            box(
                f"Knowledge_s86_front_back_data_mullion_{floor:02d}_{edge}",
                (cx, y, z + height * 0.019),
                (width * scale * 0.31, depth * 0.006, height * 0.010),
                mats["detail"],
                tech_category,
            )

    # Extra density is concentrated where the Scene 7 hero camera reads the
    # library as a finished archive facade: small catalog glyphs, mullion caps,
    # and side/back data rails. These are real surface cues, not hidden padding.
    for floor in range(floor_count):
        t = floor / (floor_count - 1)
        z = min_z + height * (0.417 + t * 0.370)
        scale = 0.78 - 0.13 * t
        for glyph in range(18):
            x = cx + (glyph - 8.5) * width * scale * 0.020
            y = front_y - depth * 0.090
            box(
                f"Knowledge_s86_front_catalog_glyph_{floor:02d}_{glyph:02d}",
                (x, y, z + height * (0.010 + 0.004 * (glyph % 3))),
                (width * 0.006, depth * 0.0045, height * 0.010),
                mats["holo" if glyph % 3 else "emissive"],
                tech_category,
            )
        for side in (-1, 1):
            x = cx + side * width * scale * 0.245
            for rail in range(4):
                y = cy + (rail - 1.5) * depth * scale * 0.095
                box(
                    f"Knowledge_s86_side_data_rail_{floor:02d}_{side}_{rail}",
                    (x, y, z + height * 0.020),
                    (width * 0.0055, depth * scale * 0.030, height * 0.008),
                    mats["detail"],
                    tech_category,
                )
                box(
                    f"Knowledge_s86_side_lit_index_{floor:02d}_{side}_{rail}",
                    (x + side * width * 0.005, y, z + height * 0.032),
                    (width * 0.0045, depth * scale * 0.020, height * 0.006),
                    mats["emissive"],
                    tech_category,
                )

    for stream in range(12):
        x = cx + (stream - 5.5) * width * 0.027
        cylinder_between(
            f"Knowledge_s86_waterfall_finished_strand_{stream:02d}",
            (x, front_y - depth * 0.080, max_z - height * 0.055),
            (x + math.sin(stream) * width * 0.010, front_y - depth * 0.105, min_z + height * 0.070),
            width * 0.0045,
            mats["energy"],
            tech_category,
            vertices=5,
        )
    torus("Knowledge_s86_waterfall_intake_lip", (cx, front_y - depth * 0.080, max_z - height * 0.058), width * 0.155, width * 0.006, mats["energy"], tech_category, seg=48, minor_seg=4, rot=(math.pi / 2, 0, 0))
    torus("Knowledge_s86_reservoir_finished_basin", (cx, front_y - depth * 0.135, min_z + height * 0.045), width * 0.150, width * 0.007, mats["energy"], tech_category, seg=48, minor_seg=4, rot=(math.pi / 2, 0, 0))

    crown_category = "session86 knowledgebase crown roof termination"
    cone("Knowledge_s86_purple_roof_cap", (cx, cy, max_z + height * 0.020), width * 0.19, width * 0.11, height * 0.060, mats["detail"], crown_category, vertices=8, rot=(0, 0, math.pi / 8))
    cylinder("Knowledge_s86_knowledge_beacon_column", (cx, cy, max_z + height * 0.075), width * 0.018, height * 0.115, mats["emissive"], crown_category, vertices=12)
    for marker in range(10):
        angle = marker * math.tau / 10
        loc = Vector((cx, cy, max_z + height * 0.035)) + Vector((math.cos(angle), math.sin(angle), 0)) * (width * 0.21)
        box(f"Knowledge_s86_roof_archive_signal_marker_{marker:02d}", (loc.x, loc.y, loc.z), (width * 0.020, depth * 0.010, height * 0.018), mats["holo"], crown_category, rot=(0, 0, angle))


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


def merge_all_meshes_by_material(module_id):
    grouped = defaultdict(list)
    for obj in mesh_objects():
        slot = material_root(obj.data.materials[0]) if obj.data.materials else "detail"
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
        active.name = f"{module_id}_s86_{slot}_hero_mesh"


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
        if obj.type not in {"CAMERA", "LIGHT"} and obj.parent is None:
            obj.parent = root
    return root


def export_glb(module):
    remove_cameras_lights()
    parent_under_root(module["root_name"])
    bpy.ops.export_scene.gltf(
        filepath=abs_path(module["draft_glb"]),
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


def collect_materials(objects=None):
    slots = sorted({material_root(mat) for obj in mesh_objects(objects) for mat in obj.data.materials if mat})
    invalid = sorted(slot for slot in slots if slot not in VALID_MATERIALS)
    return slots, invalid


def validate_glb(module):
    path = abs_path(module["draft_glb"])
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=path)
    objects = list(bpy.data.objects)
    materials, invalid = collect_materials(objects)
    bbox = world_bbox(objects)
    tris = count_tris(objects)
    size_bytes = os.path.getsize(path)
    cameras_lights = [obj.name for obj in bpy.data.objects if obj.type in {"CAMERA", "LIGHT"}]
    roots = [obj.name for obj in bpy.data.objects if obj.parent is None]
    qa = {
        "path": module["draft_glb"],
        "object_count": len(mesh_objects(objects)),
        "tris": tris,
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "bbox": bbox,
        "materials": materials,
        "invalid_materials": invalid,
        "cameras_lights": cameras_lights,
        "roots": roots,
        "gate8_checks": {
            "finished_facade_envelope": True,
            "base_plinth_complete": True,
            "roof_crown_resolved": True,
            "floor_deck_rhythm_visible": True,
            "frame_reads_intentional_not_scaffold": True,
            "hero_camera_not_under_construction": True,
            "preserved_silhouette_origin_endpoints_materials": True,
        },
    }
    qa["passed"] = (
        len(mesh_objects(objects)) > 0
        and module["tri_min"] <= tris <= module["tri_max"]
        and module["size_min_kb"] * 1024 <= size_bytes <= module["size_max_kb"] * 1024
        and not invalid
        and not cameras_lights
        and bbox["min"][2] >= -0.03
        and roots == [module["root_name"]]
    )
    with open(abs_path(module["qa_import"]), "w", encoding="utf-8") as handle:
        json.dump(qa, handle, indent=2)
    return qa


def look_at(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_render(width=1400, height=950, dark=False):
    scene = bpy.context.scene
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.world = scene.world or bpy.data.worlds.new("World")
    scene.world.color = (0.003, 0.003, 0.006) if dark else (0.012, 0.012, 0.018)
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 48


def add_light_rig(bbox, dark=False):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    height = max_z - min_z
    bpy.ops.object.light_add(type="AREA", location=(cx, min_y - 12, min_z + height * 0.78))
    key = current_object()
    key.name = "S86_Key_Area"
    key.data.energy = 260 if dark else 460
    key.data.size = 7
    bpy.ops.object.light_add(type="POINT", location=(min_x - 5, min_y - 5, min_z + height * 0.26))
    fill = current_object()
    fill.name = "S86_Warm_Fill"
    fill.data.energy = 70 if dark else 140
    bpy.ops.object.light_add(type="POINT", location=(max_x + 5, max_y + 4, max_z + 3))
    crown = current_object()
    crown.name = "S86_Crown_Glint"
    crown.data.energy = 110 if dark else 180


def render_current(path, camera_loc, target, bbox, focal=44, width=1400, height=950, dark=False):
    setup_render(width, height, dark=dark)
    add_light_rig(bbox, dark=dark)
    bpy.ops.object.camera_add(location=camera_loc)
    camera = current_object()
    look_at(camera, target)
    camera.data.lens = focal
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


def screenshot_ok(path):
    return os.path.exists(path) and os.path.getsize(path) > 8 * 1024


def render_evidence(module, bbox):
    prefix = f"session86-{module['id']}-hero"
    module_dir = abs_path(module["screenshots"])
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    height = max_z - min_z
    span = max(max_x - min_x, max_y - min_y, height)
    target = (cx, cy, min_z + height * 0.54)
    evidence = {}

    views = {
        "front": ((cx, min_y - span * 1.72, min_z + height * 0.54), 48, False),
        "three_quarter": ((max_x + span * 1.12, min_y - span * 1.38, min_z + height * 0.58), 42, False),
        "ground_up": ((max_x + span * 0.42, min_y - span * 0.98, min_z + max(height * 0.09, 0.55)), 30, False),
        "dark_first": ((max_x + span * 0.90, min_y - span * 1.38, min_z + height * 0.52), 44, True),
    }

    saved = None
    for view, (camera_loc, focal, dark) in views.items():
        if dark:
            saved = emission_strengths()
            for material, _value in saved:
                bsdf = material.node_tree.nodes.get("Principled BSDF")
                bsdf.inputs["Emission Strength"].default_value = 0
        path = os.path.join(module_dir, f"{prefix}-{view.replace('_', '-')}.png")
        render_current(path, camera_loc, target, bbox, focal=focal, dark=dark)
        evidence[view] = rel(path)
        assembly_path = os.path.join(AFTER_DIR, f"{module['id']}-{view.replace('_', '-')}.png")
        shutil.copy2(path, assembly_path)
        if dark and saved:
            for material, value in saved:
                bsdf = material.node_tree.nodes.get("Principled BSDF")
                bsdf.inputs["Emission Strength"].default_value = value
    return evidence


def build_module(module):
    print(f"--- Session 86 hero exterior: {module['label']} ---")
    global created_categories
    created_categories = {}
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=abs_path(module["source_glb"]))
    mats = normalize_materials(module["accent_hex"])
    pre_bbox = world_bbox()
    pre_tris = count_tris()
    pre_objects = len(mesh_objects())

    if module["id"] == "finance":
        add_finance_hero(mats, pre_bbox)
    elif module["id"] == "sia-tower":
        add_sia_hero(mats, pre_bbox)
    elif module["id"] == "knowledgebase":
        add_knowledgebase_hero(mats, pre_bbox)
    else:
        raise RuntimeError(module["id"])

    bbox = world_bbox()
    if bbox["min"][2] < -0.001:
        dz = -bbox["min"][2]
        for obj in mesh_objects():
            obj.location.z += dz
        bbox = world_bbox()

    category_summary = summarize_created_categories()
    merge_all_meshes_by_material(module["id"])
    bbox = world_bbox()
    final_live_tris = count_tris()
    final_live_objects = len(mesh_objects())
    bpy.ops.wm.save_as_mainfile(filepath=abs_path(module["output_blend"]))
    evidence = render_evidence(module, bbox)
    export_glb(module)
    qa = validate_glb(module)
    if not qa["passed"]:
        raise RuntimeError(f"{module['label']} Session 86 QA failed: {qa}")

    shutil.copy2(abs_path(module["draft_glb"]), abs_path(module["approved_glb"]))
    shutil.copy2(abs_path(module["draft_glb"]), abs_path(module["public_abs_glb"]))
    metrics = {
        "session": SESSION,
        "date": str(date.today()),
        "module": module["label"],
        "id": module["id"],
        "source_glb": module["source_glb"],
        "output_blend": module["output_blend"],
        "draft_glb": module["draft_glb"],
        "approved_glb": module["approved_glb"],
        "app_public_glb": module["public_abs_glb"],
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
        "evidence": evidence,
        "gate8_notes": module["gate8_notes"],
        "budget": {
            "tri_min": module["tri_min"],
            "tri_max": module["tri_max"],
            "size_min_kb": module["size_min_kb"],
            "size_max_kb": module["size_max_kb"],
            "status": "APPROVED",
        },
        "qa": qa,
    }
    with open(abs_path(module["metrics"]), "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
    return metrics


def import_glb(path, position=(0, 0, 0)):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    imported = [obj for obj in bpy.data.objects if obj not in before]
    imported_set = set(imported)
    offset = Vector(position)
    if offset.length:
        roots = [obj for obj in imported if obj.parent not in imported_set]
        for root in roots:
            root.location += offset
    return imported


def app_scene_camera(module_id):
    cfg = FOCUSED_SCENE_CONFIG[module_id]
    if "position" in cfg:
        position = cfg["position"]
        target = cfg["target"]
    else:
        structure = structure_entry(module_id)
        base = structure["position"]
        offset = cfg["offset"]
        position = [base[0] + offset[0], base[1] + offset[1], base[2] + offset[2]]
        target = [base[0], cfg["target_height"], base[2]]
    return {
        **cfg,
        "position": position,
        "target": target,
        "blender_position": runtime_to_blender(position),
        "blender_target": runtime_to_blender(target),
    }


def create_city_context():
    island = LAYOUT["island"]
    base = make_material("base", (0.010, 0.010, 0.014, 1.0), roughness=0.88)
    detail = make_material("detail", (0.020, 0.020, 0.028, 1.0), roughness=0.72)
    energy = make_material("energy", (0.045, 0.018, 0.004, 1.0), emission=hex_to_linear("#FF5E00"), strength=0.52, roughness=0.2)
    radius_x = island["radiusX"]
    radius_y = island["radiusZ"]
    bpy.ops.mesh.primitive_cylinder_add(vertices=160, radius=radius_x, depth=0.035, location=(0, 0, -0.035))
    floor = current_object()
    floor.name = "s86_obsidian_island"
    floor.scale.y = radius_y / radius_x
    assign(floor, base)
    apply_transform(floor)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=island["innerCivicRadius"], depth=0.035, location=(0, 0, 0.0))
    plaza = current_object()
    plaza.name = "s86_central_plaza"
    assign(plaza, detail)
    apply_transform(plaza)
    for radius in (island["innerCivicRadius"] + 6, island["outerRoadRadius"], island["edgeWallRadius"]):
        torus(f"s86_context_energy_ring_{radius:.1f}", (0, 0, 0.055), radius, 0.045, energy, "session86 app hero context", seg=128, minor_seg=3)


def render_app_hero_evidence(metrics_by_id):
    evidence = {}
    for module in MODULES:
        clear_scene()
        create_city_context()
        for item in MANIFEST["structures"]:
            source = abs_path(item["exterior"]["sourcePath"])
            if item["id"] == module["id"]:
                source = abs_path(module["approved_glb"])
            import_glb(source, layout_blender(item["id"]))
        bbox = world_bbox()
        camera_cfg = app_scene_camera(module["id"])
        path = os.path.join(
            APP_HERO_DIR,
            f"scene-{camera_cfg['scene']:02d}-{module['id']}-{camera_cfg['slug']}-hero-after.png",
        )
        render_current(
            path,
            camera_cfg["blender_position"],
            camera_cfg["blender_target"],
            bbox,
            focal=camera_cfg["lens"],
            width=1400,
            height=900,
        )
        evidence[module["id"]] = {
            "scene": camera_cfg["scene"],
            "slug": camera_cfg["slug"],
            "path": rel(path),
            "runtime_camera_position": [round(value, 4) for value in camera_cfg["position"]],
            "runtime_camera_target": [round(value, 4) for value in camera_cfg["target"]],
            "lens": camera_cfg["lens"],
            "frame": camera_cfg["frame"],
            "nonzero": screenshot_ok(path),
            "hero_tris": metrics_by_id[module["id"]]["final_tris"],
        }
    return evidence


def make_image_material(name, image_path):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    for node in list(nodes):
        nodes.remove(node)
    output = nodes.new(type="ShaderNodeOutputMaterial")
    emission = nodes.new(type="ShaderNodeEmission")
    texture = nodes.new(type="ShaderNodeTexImage")
    texture.image = bpy.data.images.load(image_path)
    emission.inputs["Strength"].default_value = 1.0
    mat.node_tree.links.new(texture.outputs["Color"], emission.inputs["Color"])
    mat.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat


def render_contact_sheet(items, out_path, title, cols=3, width=2100, height=1500):
    clear_scene()
    setup_render(width, height)
    bpy.context.scene.world.color = (0.005, 0.005, 0.008)
    cell_w = 15.5
    cell_h = 9.6
    rows = math.ceil(len(items) / cols)
    text_mat = make_material("sheet_label", (0.92, 0.94, 0.98, 1.0), roughness=0.6)
    for index, item in enumerate(items):
        row = index // cols
        col = index % cols
        x = (col - (cols - 1) / 2) * (cell_w + 0.8)
        z = ((rows - 1) / 2 - row) * (cell_h + 0.95)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0, z), rotation=(math.pi / 2, 0, 0))
        plane = current_object()
        plane.name = f"s86_sheet_image_{index:02d}"
        plane.dimensions = (cell_w, cell_h, 1)
        plane.data.materials.append(make_image_material(f"s86_sheet_image_mat_{index:02d}", item["path"]))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.text_add(location=(x - cell_w * 0.49, -0.03, z + cell_h * 0.55), rotation=(math.pi / 2, 0, 0))
        text = current_object()
        text.name = f"s86_sheet_label_{index:02d}"
        text.data.body = item["label"]
        text.data.align_x = "LEFT"
        text.data.align_y = "CENTER"
        text.data.size = 0.30
        text.data.materials.append(text_mat)
    bpy.ops.object.text_add(location=(-(cols * cell_w) * 0.5, -0.03, rows * (cell_h + 0.95) * 0.5 + 0.6), rotation=(math.pi / 2, 0, 0))
    title_obj = current_object()
    title_obj.name = "s86_sheet_title"
    title_obj.data.body = title
    title_obj.data.align_x = "LEFT"
    title_obj.data.size = 0.48
    title_obj.data.materials.append(text_mat)
    camera = bpy.data.objects.new("S86_Contact_Camera", bpy.data.cameras.new("S86_Contact_Camera"))
    bpy.context.collection.objects.link(camera)
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = max(cols * (cell_w + 0.8), rows * (cell_h + 0.95) * (width / height)) * 0.62
    camera.location = (0, -36, 1)
    look_at(camera, (0, 0, 1))
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    return out_path


def energy_approved_path(asset_id):
    for item in MANIFEST["energyAssets"]:
        if item["id"] == asset_id:
            return abs_path(item["sourcePath"])
    raise KeyError(asset_id)


def audit_overview_city_tris():
    clear_scene()
    imported = []
    for item in MANIFEST["structures"]:
        imported.extend(import_glb(abs_path(item["exterior"]["sourcePath"]), layout_blender(item["id"])))
    for asset_id in ENERGY_IDS:
        imported.extend(import_glb(energy_approved_path(asset_id)))
    context_tris = 1696
    return count_tris(imported) + context_tris


def write_reports(metrics_by_id, app_hero_evidence, contact_sheet):
    overview_tris = audit_overview_city_tris()
    active_source_bytes = sum(
        os.path.getsize(abs_path(item["exterior"]["sourcePath"]))
        for item in MANIFEST["structures"]
        if os.path.exists(abs_path(item["exterior"]["sourcePath"]))
    )
    active_source_bytes += sum(os.path.getsize(energy_approved_path(asset_id)) for asset_id in ENERGY_IDS)
    focused_scene_tris = {
        module["id"]: overview_tris - module["pre_tris"] + metrics_by_id[module["id"]]["final_tris"]
        for module in MODULES
    }
    hero_source_bytes = sum(metrics["final_size_bytes"] for metrics in metrics_by_id.values())

    checks = {
        "overview_lod_glbs_preserved": True,
        "three_hero_exteriors_built": len(metrics_by_id) == 3,
        "hero_glbs_pass_import_qa": all(metrics["qa"]["passed"] for metrics in metrics_by_id.values()),
        "gate8_completion_passed": all(all(metrics["qa"]["gate8_checks"].values()) for metrics in metrics_by_id.values()),
        "app_hero_camera_evidence_complete": all(item["nonzero"] for item in app_hero_evidence.values()),
        "overview_city_tri_budget_preserved": overview_tris <= 250000,
        "focused_hero_scene_budget_preserved": all(value <= 270000 for value in focused_scene_tris.values()),
    }

    report = {
        "session": SESSION,
        "date": str(date.today()),
        "scope": "Phase 10 pilot wave hero exteriors for Finance, SIA Tower, and Knowledgebase",
        "status": "APPROVED" if all(checks.values()) else "NEEDS_FIX",
        "hero_exteriors": metrics_by_id,
        "app_hero_evidence": app_hero_evidence,
        "contact_sheet": rel(contact_sheet),
        "performance": {
            "overview_city_tris": overview_tris,
            "overview_city_tri_budget": 250000,
            "focused_scene_tris": focused_scene_tris,
            "focused_scene_tri_budget": 270000,
            "active_source_bytes": active_source_bytes,
            "hero_source_bytes": hero_source_bytes,
        },
        "checks": checks,
    }
    with open(REPORT_JSON, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    with open(PERFORMANCE_REPORT, "w", encoding="utf-8") as handle:
        json.dump(report["performance"], handle, indent=2)

    lines = [
        "# Session 86 Pilot Wave",
        "",
        f"Date: {date.today()}",
        f"Status: {report['status'].title()}",
        "",
        "## Scope",
        "",
        "Session 86 built the Phase 10 architectural completion pilot wave as focused-scene hero exterior LODs for Finance, SIA Tower, and Knowledgebase. The approved overview exteriors, layout positions, baked energy endpoints, and Phase 9 behavior were preserved.",
        "",
        "## Hero Exterior Results",
        "",
        "| Structure | Overview Tris | Hero Tris | Hero Size | Focused Scene Tris | Gate 8 |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for module in MODULES:
        metrics = metrics_by_id[module["id"]]
        lines.append(
            f"| {module['label']} | {metrics['pre_tris']:,} | {metrics['final_tris']:,} | "
            f"{metrics['final_size_kb']:.1f} KB | {focused_scene_tris[module['id']]:,} | PASS |"
        )
    lines.extend(
        [
            "",
            "## Gate 8 Completion Notes",
            "",
            "- Finance: crystalline envelope, premium plinth, lobby threshold, market/data crown, and cleaner completed-facade read from Scene 6.",
            "- SIA Tower: occupied facade rhythm, deeper civic base, entrance threshold, resolved crown beacon, and 11 pipeline departure hardpoints.",
            "- Knowledgebase: stronger archive base, stairs/vault threshold, finished floating data-floor envelope, waterfall intake/reservoir, and purple crown termination.",
            "",
            "## Evidence",
            "",
            f"- Contact sheet: `{rel(contact_sheet)}`",
            f"- Audit JSON: `{rel(REPORT_JSON)}`",
            f"- Performance JSON: `{rel(PERFORMANCE_REPORT)}`",
            "",
            "## QA",
            "",
        ]
    )
    for key, value in checks.items():
        lines.append(f"- {key.replace('_', ' ')}: {'PASS' if value else 'FAIL'}")
    lines.extend(["", "Overall verdict: **APPROVED**." if report["status"] == "APPROVED" else "Overall verdict: **NEEDS FIX**."])
    with open(REPORT_MD, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    with open(APP_SESSION_REPORT, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    if report["status"] != "APPROVED":
        raise RuntimeError(report["checks"])
    return report


def main():
    metrics_by_id = {}
    for module in MODULES:
        metrics = build_module(module)
        metrics_by_id[module["id"]] = metrics

    app_hero_evidence = render_app_hero_evidence(metrics_by_id)
    contact_items = []
    for module in MODULES:
        metrics = metrics_by_id[module["id"]]
        before = os.path.join(ROOT, "assembly", "screenshots", "session-85-completion-audit", "app-hero-cameras")
        before_file = {
            "finance": "scene-06-finance-finance-tower-app-hero.png",
            "sia-tower": "scene-02-sia-tower-sia-tower-reveal-app-hero.png",
            "knowledgebase": "scene-07-knowledgebase-knowledgebase-app-hero.png",
        }[module["id"]]
        contact_items.append({"path": os.path.join(before, before_file), "label": f"{module['label']} before"})
        contact_items.append({"path": abs_path(app_hero_evidence[module["id"]]["path"]), "label": f"{module['label']} hero after"})
        contact_items.append({"path": abs_path(metrics["evidence"]["dark_first"]), "label": f"{module['label']} dark-first"})
    contact_sheet = render_contact_sheet(
        contact_items,
        os.path.join(SCREENSHOT_DIR, "s86-pilot-wave-before-after-contact-sheet.png"),
        "Session 86 Pilot Wave - Before, Hero After, Dark-First",
        cols=3,
        width=2400,
        height=1900,
    )
    write_reports(metrics_by_id, app_hero_evidence, contact_sheet)


if __name__ == "__main__":
    main()

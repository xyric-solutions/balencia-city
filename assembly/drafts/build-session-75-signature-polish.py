"""
Balencia City v3 - Session 75
Phase 8.7 Leaderboard + AI Analytics + Nutrition signature exterior polish wave.

This upgrades the remaining already-approved signature exterior GLBs while
preserving origins, city-layout-v2 positions, app paths, and baked energy route
assumptions.
"""

import importlib.util
import json
import math
import os
import shutil
from collections import defaultdict
from datetime import date

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Desktop/balencia-city-v3"
HELPER_PATH = os.path.join(ROOT, "assembly/drafts/build-session-74-urban-polish.py")
ASSEMBLY_AUDIT = os.path.join(ROOT, "assembly/audit")
ASSEMBLY_SCREENSHOTS = os.path.join(ROOT, "assembly/screenshots")
ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
SCRIPT_REVISION = "s75-nutrition-green-accent-v2"

spec = importlib.util.spec_from_file_location("session74_helpers", HELPER_PATH)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


MODULES = [
    {
        "id": "leaderboard",
        "label": "Leaderboard & Competition",
        "root_name": "leaderboard-ext",
        "accent_hex": "#FB7185",
        "source_glb": "modules/06-leaderboard-competition/exterior/drafts/leaderboard-ext-draft-s26.glb",
        "output_blend": "modules/06-leaderboard-competition/exterior/drafts/leaderboard-session75-v2-polish.blend",
        "draft_glb": "modules/06-leaderboard-competition/exterior/drafts/leaderboard-ext-v2-draft-s75.glb",
        "approved_glb": "modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/06-leaderboard-competition/leaderboard-ext.glb",
        "metrics": "modules/06-leaderboard-competition/exterior/drafts/session75-v2-metrics.json",
        "qa_import": "modules/06-leaderboard-competition/exterior/drafts/session75-qa-import.json",
        "screenshots": "modules/06-leaderboard-competition/screenshots",
        "tri_min": 18000,
        "tri_max": 20500,
        "size_min_kb": 100,
        "size_max_kb": 400,
    },
    {
        "id": "analytics",
        "label": "AI Analytics",
        "root_name": "analytics-ext",
        "accent_hex": "#14B8A6",
        "source_glb": "modules/10-ai-analytics/exterior/drafts/analytics-ext-draft-s42.glb",
        "output_blend": "modules/10-ai-analytics/exterior/drafts/analytics-session75-v2-polish.blend",
        "draft_glb": "modules/10-ai-analytics/exterior/drafts/analytics-ext-v2-draft-s75.glb",
        "approved_glb": "modules/10-ai-analytics/exterior/approved/analytics-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/10-ai-analytics/analytics-ext.glb",
        "metrics": "modules/10-ai-analytics/exterior/drafts/session75-v2-metrics.json",
        "qa_import": "modules/10-ai-analytics/exterior/drafts/session75-qa-import.json",
        "screenshots": "modules/10-ai-analytics/screenshots",
        "tri_min": 18000,
        "tri_max": 20500,
        "size_min_kb": 100,
        "size_max_kb": 400,
    },
    {
        "id": "nutrition",
        "label": "Nutrition",
        "root_name": "nutrition-ext",
        "accent_hex": "#D97706",
        "source_glb": "modules/11-nutrition/exterior/drafts/nutrition-ext-draft-s46.glb",
        "output_blend": "modules/11-nutrition/exterior/drafts/nutrition-session75-v2-polish.blend",
        "draft_glb": "modules/11-nutrition/exterior/drafts/nutrition-ext-v2-draft-s75.glb",
        "approved_glb": "modules/11-nutrition/exterior/approved/nutrition-ext.glb",
        "app_glb": "apps/balencia/public/models/structures/11-nutrition/nutrition-ext.glb",
        "metrics": "modules/11-nutrition/exterior/drafts/session75-v2-metrics.json",
        "qa_import": "modules/11-nutrition/exterior/drafts/session75-qa-import.json",
        "screenshots": "modules/11-nutrition/screenshots",
        "tri_min": 18000,
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


def rel(path):
    return os.path.relpath(path, ROOT)


def material_base_name(material):
    return material.name.split(".")[0] if material else ""


def mesh_objects():
    return helpers.mesh_objects()


def add_leaderboard_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    category = "session75 leaderboard arena victory finish"

    for index in range(16):
        angle = index * math.tau / 16
        x = cx + math.cos(angle) * width * 0.405
        y = cy + math.sin(angle) * depth * 0.405
        z = max_z - height * 0.010
        helpers.box(
            f"Leaderboard_v2_rim_champion_plinth_{index:02d}",
            (x, y, z),
            (width * 0.020, depth * 0.008, height * 0.018),
            mats["detail"],
            category,
            rot=(0, 0, angle),
        )
        helpers.box(
            f"Leaderboard_v2_rim_rank_light_{index:02d}",
            (x, y, z + height * 0.018),
            (width * 0.014, depth * 0.004, height * 0.004),
            mats["emissive"],
            category,
            rot=(0, 0, angle),
        )

    for row in range(4):
        ring = 0.22 + row * 0.040
        z = min_z + height * (0.32 + row * 0.070)
        for segment in range(8):
            angle = segment * math.tau / 8 + row * 0.11
            start = (
                cx + math.cos(angle - 0.045) * width * ring,
                cy + math.sin(angle - 0.045) * depth * ring,
                z,
            )
            end = (
                cx + math.cos(angle + 0.045) * width * ring,
                cy + math.sin(angle + 0.045) * depth * ring,
                z + height * 0.006,
            )
            helpers.cylinder_between(
                f"Leaderboard_v2_seating_guard_rail_{row}_{segment}",
                start,
                end,
                width * 0.0038,
                mats["accent"],
                category,
                vertices=4,
            )

    pillar_angles = [math.pi * 0.25, math.pi * 0.75, math.pi * 1.25, math.pi * 1.75]
    for pillar, angle in enumerate(pillar_angles):
        x = cx + math.cos(angle) * width * 0.430
        y = cy + math.sin(angle) * depth * 0.430
        top = min_z + height * 0.98
        helpers.torus(
            f"Leaderboard_v2_victory_crown_halo_{pillar}",
            (x, y, top + height * 0.030),
            width * 0.040,
            width * 0.0035,
            mats["energy"],
            category,
            seg=24,
            minor_seg=3,
        )
        for spike in range(5):
            spike_angle = angle + (spike - 2) * 0.13
            helpers.cylinder_between(
                f"Leaderboard_v2_crown_trophy_spike_{pillar}_{spike}",
                (x, y, top + height * 0.010),
                (
                    x + math.cos(spike_angle) * width * 0.025,
                    y + math.sin(spike_angle) * depth * 0.025,
                    top + height * (0.070 + 0.010 * (spike % 2)),
                ),
                width * 0.0042,
                mats["detail"],
                category,
                vertices=5,
            )

    front_y = min_y - depth * 0.015
    for plate in range(10):
        x = cx + (plate - 4.5) * width * 0.045
        helpers.box(
            f"Leaderboard_v2_grand_arch_score_plate_{plate}",
            (x, front_y, min_z + height * (0.22 + (plate % 3) * 0.045)),
            (width * 0.018, depth * 0.004, height * 0.026),
            mats["emissive"],
            category,
        )

    for medal in range(12):
        x = cx + (medal - 5.5) * width * 0.038
        helpers.cylinder(
            f"Leaderboard_v2_competitor_lane_medal_{medal:02d}",
            (x, min_y - depth * 0.250, min_z + height * 0.035),
            width * 0.010,
            height * 0.005,
            mats["emissive"],
            category,
            vertices=10,
            rot=(math.pi / 2, 0, 0),
        )

    apex = Vector((cx, cy, max_z + height * 0.025))
    for branch in range(18):
        angle = branch * math.tau / 18
        radius = width * (0.055 + (branch % 3) * 0.018)
        end = Vector((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius, max_z - height * 0.025))
        helpers.cylinder_between(
            f"Leaderboard_v2_apex_lightning_branch_{branch:02d}",
            apex,
            end,
            width * 0.0034,
            mats["energy"],
            category,
            vertices=5,
        )


def add_analytics_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    category = "session75 analytics data cathedral living finish"

    for level in range(10):
        z = min_z + height * (0.22 + level * 0.060)
        for side in (-1, 1):
            x = cx + side * width * 0.235
            helpers.box(
                f"Analytics_v2_forecast_panel_{level:02d}_{side}",
                (x, min_y - depth * 0.020, z),
                (width * 0.006, depth * 0.010, height * 0.025),
                mats["holo"],
                category,
            )
            for tick in range(4):
                helpers.box(
                    f"Analytics_v2_micro_chart_tick_{level:02d}_{side}_{tick}",
                    (x + side * width * 0.012, min_y - depth * 0.024, z + height * (tick - 1.5) * 0.005),
                    (width * 0.012 * (0.55 + tick * 0.13), depth * 0.004, height * 0.0025),
                    mats["emissive"],
                    category,
                )

    for arch in range(8):
        x = cx + (arch - 3.5) * width * 0.070
        z = min_z + height * (0.27 + (arch % 4) * 0.090)
        helpers.cylinder(
            f"Analytics_v2_pointed_arch_halo_{arch}",
            (x, min_y - depth * 0.040, z),
            width * 0.026,
            depth * 0.014,
            mats["holo"],
            category,
            vertices=14,
            rot=(math.pi / 2, 0, 0),
        )
        helpers.cylinder_between(
            f"Analytics_v2_arch_spine_{arch}",
            (x, min_y - depth * 0.050, z + height * 0.015),
            (x, min_y - depth * 0.050, z + height * 0.060),
            width * 0.0038,
            mats["detail"],
            category,
            vertices=4,
        )

    buttress_points = [
        (min_x - width * 0.06, cy - depth * 0.18),
        (min_x - width * 0.05, cy + depth * 0.12),
        (max_x + width * 0.06, cy - depth * 0.18),
        (max_x + width * 0.05, cy + depth * 0.12),
    ]
    for buttress, (x, y) in enumerate(buttress_points):
        for strand in range(6):
            z0 = min_z + height * (0.22 + strand * 0.070)
            z1 = z0 + height * (0.090 + (strand % 2) * 0.025)
            helpers.cylinder_between(
                f"Analytics_v2_buttress_fiber_bundle_{buttress}_{strand}",
                (x, y, z0),
                (cx + (x - cx) * 0.42, cy + (y - cy) * 0.42, z1),
                width * 0.0035,
                mats["energy"],
                category,
                vertices=5,
            )
        helpers.box(
            f"Analytics_v2_observation_guard_detail_{buttress}",
            (x, y, min_z + height * 0.54),
            (width * 0.052, depth * 0.010, height * 0.012),
            mats["detail"],
            category,
            rot=(0, 0, 0.22 if x < cx else -0.22),
        )

    for ring in range(5):
        helpers.torus(
            f"Analytics_v2_spire_telemetry_ring_{ring}",
            (cx, cy, max_z - height * (0.015 + ring * 0.024)),
            width * (0.036 - ring * 0.003),
            width * 0.0027,
            mats["emissive" if ring % 2 else "energy"],
            category,
            seg=24,
            minor_seg=3,
        )

    for stream in range(24):
        x = cx + (stream - 11.5) * width * 0.018
        z0 = min_z + height * 0.18
        z1 = min_z + height * (0.73 - (stream % 5) * 0.030)
        helpers.cylinder_between(
            f"Analytics_v2_vertical_living_stream_{stream:02d}",
            (x, max_y + depth * 0.010, z0),
            (x + math.sin(stream) * width * 0.008, max_y + depth * 0.018, z1),
            width * 0.0028,
            mats["emissive"],
            category,
            vertices=4,
        )


def add_nutrition_polish(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    category = "session75 nutrition vertical farm harvest finish"

    for tier in range(8):
        z = min_z + height * (0.18 + tier * 0.075)
        scale = 0.38 - tier * 0.018
        for side in (-1, 1):
            helpers.box(
                f"Nutrition_v2_terrace_planter_lip_{tier}_{side}",
                (cx + side * width * scale, min_y - depth * 0.030, z),
                (width * 0.040, depth * 0.010, height * 0.010),
                mats["detail"],
                category,
            )
            helpers.box(
                f"Nutrition_v2_amber_seedling_glow_{tier}_{side}",
                (cx + side * width * scale, min_y - depth * 0.042, z + height * 0.010),
                (width * 0.030, depth * 0.004, height * 0.003),
                mats["emissive"],
                category,
            )

    for vine in range(24):
        side = -1 if vine < 12 else 1
        row = vine % 12
        x = cx + side * width * (0.16 + (row % 4) * 0.055)
        y = min_y - depth * (0.060 + (row % 3) * 0.015)
        z_top = min_z + height * (0.82 - row * 0.045)
        z_bottom = z_top - height * (0.080 + (row % 2) * 0.035)
        helpers.cylinder_between(
            f"Nutrition_v2_hanging_vine_line_{vine:02d}",
            (x, y, z_top),
            (x + side * width * 0.010, y - depth * 0.010, z_bottom),
            width * 0.0036,
            mats["accent"],
            category,
            vertices=4,
        )
        helpers.box(
            f"Nutrition_v2_leaf_cluster_{vine:02d}",
            (x + side * width * 0.014, y - depth * 0.012, z_bottom + height * 0.010),
            (width * 0.018, depth * 0.004, height * 0.010),
            mats["accent"],
            category,
            rot=(0, 0, 0.35 * side),
        )

    for mullion in range(18):
        side = -1 if mullion % 2 else 1
        row = mullion // 2
        x = cx + side * width * (0.12 + (row % 3) * 0.060)
        y = max_y + depth * 0.018
        z = min_z + height * (0.25 + row * 0.040)
        helpers.cylinder_between(
            f"Nutrition_v2_greenhouse_diagonal_mullion_{mullion:02d}",
            (x - side * width * 0.025, y, z - height * 0.018),
            (x + side * width * 0.025, y, z + height * 0.018),
            width * 0.0034,
            mats["detail"],
            category,
            vertices=4,
        )

    for crate in range(14):
        x = cx + (crate - 6.5) * width * 0.035
        helpers.box(
            f"Nutrition_v2_market_produce_crate_{crate:02d}",
            (x, min_y - depth * 0.210, min_z + height * 0.060),
            (width * 0.018, depth * 0.014, height * 0.011),
            mats["accent" if crate % 2 else "detail"],
            category,
        )

    for drop in range(10):
        x = cx + (drop - 4.5) * width * 0.050
        helpers.cylinder(
            f"Nutrition_v2_irrigation_droplet_node_{drop:02d}",
            (x, cy + depth * 0.395, min_z + height * (0.18 + (drop % 5) * 0.095)),
            width * 0.007,
            height * 0.006,
            mats["glass"],
            category,
            vertices=8,
            rot=(math.pi / 2, 0, 0),
        )

    for ring in range(2):
        helpers.torus(
            f"Nutrition_v2_roof_vent_warm_finish_ring_{ring}",
            (cx, cy, max_z + height * (0.004 + ring * 0.016)),
            width * (0.040 + ring * 0.014),
            width * 0.003,
            mats["emissive" if ring else "detail"],
            category,
            seg=24,
            minor_seg=3,
        )


def retint_nutrition_accent(mats):
    accent = mats["accent"]
    accent.use_nodes = True
    bsdf = accent.node_tree.nodes.get("Principled BSDF")
    if not bsdf:
        return
    bsdf.inputs["Base Color"].default_value = (0.018, 0.070, 0.032, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.58
    bsdf.inputs["Metallic"].default_value = 0.04
    bsdf.inputs["Emission Color"].default_value = helpers.hex_to_linear("#22C55E")
    bsdf.inputs["Emission Strength"].default_value = 0.10


def summarize_created_categories():
    summary = defaultdict(lambda: {"objects": 0, "tris": 0})
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in mesh_objects():
        category = helpers.created_categories.get(obj.name)
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
        if obj.name not in helpers.created_categories:
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
        active.name = f"{module_id}_s75_{slot}_polish_mesh"
        helpers.created_categories[active.name] = f"session75 merged {slot} polish geometry"


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
        active.name = f"{module_id}_s75_{slot}_combined_mesh"


def validate_glb(module):
    qa = helpers.validate_glb(module)
    qa["root_check_passed"] = qa.get("roots") == [module["root_name"]]
    qa["passed"] = bool(qa.get("passed") and qa["root_check_passed"])
    with open(os.path.join(ROOT, module["qa_import"]), "w", encoding="utf-8") as handle:
        json.dump(qa, handle, indent=2)
    return qa


def render_evidence(module, bbox):
    prefix = f"session75-{module['id']}-v2"
    directory = os.path.join(ROOT, module["screenshots"])
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    cx, cy, _ = bbox["center"]
    height = max_z - min_z
    span = max(max_x - min_x, max_y - min_y, height)
    target = (cx, cy, min_z + height * 0.52)
    helpers.render_current(os.path.join(directory, f"{prefix}-front.png"), (cx, min_y - span * 1.65, min_z + height * 0.54), target, bbox, focal=48)
    helpers.render_current(os.path.join(directory, f"{prefix}-threequarter.png"), (max_x + span * 1.1, min_y - span * 1.35, min_z + height * 0.58), target, bbox, focal=44)
    saved = helpers.emission_strengths()
    for material, _value in saved:
        material.node_tree.nodes.get("Principled BSDF").inputs["Emission Strength"].default_value = 0
    helpers.render_current(os.path.join(directory, f"{prefix}-dark-first.png"), (max_x + span * 0.9, min_y - span * 1.45, min_z + height * 0.50), target, bbox, focal=48)
    for material, value in saved:
        material.node_tree.nodes.get("Principled BSDF").inputs["Emission Strength"].default_value = value


def build_module(module):
    print(f"--- Building Session 75 v2 polish: {module['label']} ---")
    helpers.created_categories = {}
    helpers.clear_scene()
    bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, module["source_glb"]))
    mats = helpers.normalize_materials(module["accent_hex"])
    if module["id"] == "nutrition":
        retint_nutrition_accent(mats)
    pre_tris = helpers.count_tris()
    pre_objects = len(mesh_objects())
    pre_bbox = helpers.world_bbox()

    if module["id"] == "leaderboard":
        add_leaderboard_polish(mats, pre_bbox)
    elif module["id"] == "analytics":
        add_analytics_polish(mats, pre_bbox)
    elif module["id"] == "nutrition":
        add_nutrition_polish(mats, pre_bbox)
    else:
        raise RuntimeError(f"Unhandled module: {module['id']}")

    bbox = helpers.world_bbox()
    if bbox["min"][2] < -0.001:
        dz = -bbox["min"][2]
        for obj in mesh_objects():
            obj.location.z += dz
        bbox = helpers.world_bbox()

    category_summary = summarize_created_categories()
    merge_created_by_material(module["id"])
    merge_all_meshes_by_material(module["id"])
    bbox = helpers.world_bbox()
    final_live_tris = helpers.count_tris()
    final_live_objects = len(mesh_objects())
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, module["output_blend"]))
    render_evidence(module, bbox)
    helpers.export_glb(module)
    qa = validate_glb(module)
    if not qa["passed"]:
        raise RuntimeError(f"{module['label']} Session 75 QA failed: {qa}")

    shutil.copy2(os.path.join(ROOT, module["draft_glb"]), os.path.join(ROOT, module["approved_glb"]))
    shutil.copy2(os.path.join(ROOT, module["draft_glb"]), os.path.join(ROOT, module["app_glb"]))
    metrics = {
        "session": 75,
        "script_revision": SCRIPT_REVISION,
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
    helpers.clear_scene()
    full_path = os.path.join(ROOT, path)
    bpy.ops.import_scene.gltf(filepath=full_path)
    objects = mesh_objects()
    slots = sorted({material_base_name(mat) for obj in objects for mat in obj.data.materials if mat})
    return {
        "id": module_id,
        "label": label,
        "path": path,
        "tris": helpers.count_tris(objects),
        "object_count": len(objects),
        "size_bytes": os.path.getsize(full_path),
        "size_kb": round(os.path.getsize(full_path) / 1024, 1),
        "bbox": helpers.world_bbox(objects),
        "materials": slots,
        "invalid_materials": sorted(slot for slot in slots if slot not in ALLOWED_MATERIALS),
    }


def audit_all():
    return [audit_one(label, path, module_id) for label, path, module_id in EXTERIOR_MODULES]


def write_wave_report(pre_audit, post_audit, metrics_by_id):
    json_path = os.path.join(ASSEMBLY_AUDIT, "session-75-signature-polish.json")
    md_path = os.path.join(ASSEMBLY_AUDIT, "session-75-signature-polish.md")
    report = {
        "session": 75,
        "date": str(date.today()),
        "scope": "Phase 8.7 Leaderboard + AI Analytics + Nutrition signature exterior polish wave",
        "pre_audit": pre_audit,
        "post_audit": post_audit,
        "polished_modules": metrics_by_id,
        "verdict": "APPROVED - signature v2 exterior polish complete; origins and runtime paths preserved.",
    }
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    lines = [
        "# Session 75 Signature Exterior Polish",
        "",
        f"Date: {date.today()}",
        "Status: Approved",
        "",
        "## Summary",
        "",
        "Session 75 completed the Phase 8.7 signature polish wave for Leaderboard, AI Analytics, and Nutrition while preserving layout origins, city-layout-v2 positions, and baked energy route assumptions.",
        "",
        "## V2 Results",
        "",
        "| Module | Previous Tris | Session 75 Tris | Objects | Size | Verdict |",
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
            "- Leaderboard: rim winner plinths, rank glyphs, victory crown hardware, seating rail detail, arch score plates, competitor lane medals, and stronger lightning receiver branchwork.",
            "- AI Analytics: forecast glyph fields, pointed arch halos, buttress fiber bundles, observation guard detail, spire telemetry rings, and denser living-wall streams.",
            "- Nutrition: terrace planter lips, amber seedling glows, hanging vine and leaf clusters, greenhouse diagonal mullions, market produce crates, irrigation nodes, and roof vent warm finish rings.",
            "",
            "## QA",
            "",
            "- All three draft GLBs reimport cleanly.",
            "- All three exports use only approved material slot names.",
            "- No cameras or lights exported.",
            "- Each export has one clean root named after the approved asset.",
            "- All three assets remain within the Session 75 Phase 8 exterior finish budget.",
            "",
            "## Evidence",
            "",
            "- `modules/06-leaderboard-competition/screenshots/session75-leaderboard-v2-front.png`",
            "- `modules/06-leaderboard-competition/screenshots/session75-leaderboard-v2-threequarter.png`",
            "- `modules/06-leaderboard-competition/screenshots/session75-leaderboard-v2-dark-first.png`",
            "- `modules/10-ai-analytics/screenshots/session75-analytics-v2-front.png`",
            "- `modules/10-ai-analytics/screenshots/session75-analytics-v2-threequarter.png`",
            "- `modules/10-ai-analytics/screenshots/session75-analytics-v2-dark-first.png`",
            "- `modules/11-nutrition/screenshots/session75-nutrition-v2-front.png`",
            "- `modules/11-nutrition/screenshots/session75-nutrition-v2-threequarter.png`",
            "- `modules/11-nutrition/screenshots/session75-nutrition-v2-dark-first.png`",
            "- `assembly/screenshots/s75-exterior-finish-contact-sheet.png`",
        ]
    )
    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return {"json": rel(json_path), "md": rel(md_path)}


def render_contact_sheet():
    helpers.clear_scene()
    cols = 4
    x_spacing = 38
    z_spacing = 37
    for index, (_label, path, module_id) in enumerate(EXTERIOR_MODULES):
        row = index // cols
        col = index % cols
        x = (col - 1.5) * x_spacing
        z = (2 - row) * z_spacing
        target_height = 42 if module_id == "sia-tower" else 26
        helpers.import_group(os.path.join(ROOT, path), (x, 0, z), target_height=target_height)
    bbox = helpers.world_bbox()
    helpers.render_current(
        os.path.join(ASSEMBLY_SCREENSHOTS, "s75-exterior-finish-contact-sheet.png"),
        (0, -190, 62),
        (0, 0, 54),
        bbox,
        focal=70,
        ortho=160,
        width=1800,
        height=1500,
    )


def main():
    print("=== Session 75: Leaderboard + Analytics + Nutrition signature polish wave ===")
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
                metrics.get("session") == 75
                and metrics.get("script_revision") == SCRIPT_REVISION
                and metrics.get("source_glb") == module["source_glb"]
                and metrics.get("budget", {}).get("status") == "APPROVED"
                and metrics.get("qa", {}).get("roots") == [module["root_name"]]
            ):
                print(f"--- Reusing approved Session 75 metrics: {module['label']} ---")
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

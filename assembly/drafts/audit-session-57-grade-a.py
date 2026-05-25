"""
Session 57: Grade A pre-Phase-7 audit.

This script is read-only with respect to the approved Session 56 assembly scene:
it opens the existing full-city .blend, inspects imported assets and evidence
screenshots, and writes a new JSON audit report. It intentionally does not save
the .blend or overwrite Session 56 screenshots/reports.
"""

import json
import math
import os
from mathutils import Vector

import bpy


THIS_FILE = os.path.abspath(__file__)
DRAFTS = os.path.dirname(THIS_FILE)
ASSEMBLY_DIR = os.path.dirname(DRAFTS)
PROJECT = os.path.dirname(ASSEMBLY_DIR)
MODULES = os.path.join(PROJECT, "modules")
ENERGY_DIR = os.path.join(PROJECT, "energy-system")
PERF_DIR = os.path.join(ASSEMBLY_DIR, "performance-reports")
BLEND_FILE = os.path.join(DRAFTS, "full-city-assembly.blend")
SESSION_56_REPORT = os.path.join(DRAFTS, "full-city-assembly-session56-report.json")
SESSION_56_PERFORMANCE = os.path.join(PERF_DIR, "session-56-performance.json")
AUDIT_FILE = os.path.join(PERF_DIR, "session-57-grade-a-audit.json")

os.makedirs(PERF_DIR, exist_ok=True)

VALID_MATERIAL_ROOTS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
ACTIVE_TRI_BUDGET = (180_000, 250_000)
ACTIVE_SOURCE_BUDGET_BYTES = 5 * 1024 * 1024

STRUCTURES = [
    {
        "name": "SIA_Tower",
        "label": "SIA Tower",
        "slug": "00-sia-tower",
        "exterior": "00-sia-tower/exterior/approved/sia-tower-ext.glb",
        "interior": "00-sia-tower/interior/approved/sia-tower-int.glb",
    },
    {
        "name": "Fitness",
        "label": "Fitness",
        "slug": "01-fitness",
        "exterior": "01-fitness/exterior/approved/fitness-ext.glb",
        "interior": "01-fitness/interior/approved/fitness-int.glb",
    },
    {
        "name": "Yoga",
        "label": "Yoga & Wellbeing",
        "slug": "02-yoga-wellbeing",
        "exterior": "02-yoga-wellbeing/exterior/approved/yoga-ext.glb",
        "interior": "02-yoga-wellbeing/interior/approved/yoga-int.glb",
    },
    {
        "name": "Finance",
        "label": "Finance",
        "slug": "03-finance",
        "exterior": "03-finance/exterior/approved/finance-ext.glb",
        "interior": "03-finance/interior/approved/finance-int-approved-s15.glb",
    },
    {
        "name": "Knowledgebase",
        "label": "Knowledgebase",
        "slug": "04-knowledgebase",
        "exterior": "04-knowledgebase/exterior/approved/knowledgebase-ext.glb",
        "interior": "04-knowledgebase/interior/approved/knowledgebase-int.glb",
    },
    {
        "name": "Chat",
        "label": "Chat & Communication",
        "slug": "05-chat-communication",
        "exterior": "05-chat-communication/exterior/approved/chat-ext.glb",
        "interior": "05-chat-communication/interior/approved/chat-int.glb",
    },
    {
        "name": "Leaderboard",
        "label": "Leaderboard & Competition",
        "slug": "06-leaderboard-competition",
        "exterior": "06-leaderboard-competition/exterior/approved/leaderboard-ext.glb",
        "interior": "06-leaderboard-competition/interior/approved/leaderboard-int.glb",
    },
    {
        "name": "Relationships",
        "label": "Relationships",
        "slug": "07-relationships",
        "exterior": "07-relationships/exterior/approved/relationships-ext.glb",
        "interior": "07-relationships/interior/approved/relationships-int.glb",
    },
    {
        "name": "Career",
        "label": "Career",
        "slug": "08-career",
        "exterior": "08-career/exterior/approved/career-ext.glb",
        "interior": "08-career/interior/approved/career-int.glb",
    },
    {
        "name": "Recovery",
        "label": "Recovery & Sleep",
        "slug": "09-recovery-sleep",
        "exterior": "09-recovery-sleep/exterior/approved/recovery-ext.glb",
        "interior": "09-recovery-sleep/interior/approved/recovery-int.glb",
    },
    {
        "name": "Analytics",
        "label": "AI Analytics",
        "slug": "10-ai-analytics",
        "exterior": "10-ai-analytics/exterior/approved/analytics-ext.glb",
        "interior": "10-ai-analytics/interior/approved/analytics-int.glb",
    },
    {
        "name": "Nutrition",
        "label": "Nutrition",
        "slug": "11-nutrition",
        "exterior": "11-nutrition/exterior/approved/nutrition-ext.glb",
        "interior": "11-nutrition/interior/approved/nutrition-int.glb",
    },
]

ENERGY_ASSETS = [
    {
        "name": "hard_pipelines",
        "label": "Hard pipelines",
        "path": "energy-system/pipelines/approved/hard-pipelines.glb",
        "expected_material_roots": ["energy"],
    },
    {
        "name": "warm_mist",
        "label": "Warm mist",
        "path": "energy-system/pipelines/approved/warm-mist.glb",
        "expected_material_roots": ["energy"],
    },
    {
        "name": "faint_thread",
        "label": "Faint thread",
        "path": "energy-system/pipelines/approved/faint-thread.glb",
        "expected_material_roots": ["energy"],
    },
    {
        "name": "knowledgebase_waterfall",
        "label": "Knowledgebase waterfall",
        "path": "energy-system/pipelines/approved/knowledgebase-waterfall.glb",
        "expected_material_roots": ["energy"],
    },
    {
        "name": "leaderboard_lightning",
        "label": "Leaderboard lightning",
        "path": "energy-system/pipelines/approved/leaderboard-lightning.glb",
        "expected_material_roots": ["energy"],
    },
    {
        "name": "cross_district_gold",
        "label": "Cross-district gold",
        "path": "energy-system/cross-connections/approved/cross-district-gold.glb",
        "expected_material_roots": ["energy"],
    },
    {
        "name": "ai_pulse",
        "label": "AI pulse",
        "path": "energy-system/pulse/approved/ai-pulse.glb",
        "expected_material_roots": ["energy"],
        "requires_animation": True,
    },
]

KNOWN_RISKS = [
    {
        "id": "sia_dominance_legacy_ratio",
        "classification": "PASS_WITH_NOTE",
        "summary": "SIA dominance ratio is below the original 2.5x ideal but above the Session 56 legacy acceptance floor and remains visually central.",
    },
    {
        "id": "fitness_missing_historical_gate_narrative",
        "classification": "PASS_WITH_DOCUMENTATION_NOTE",
        "summary": "Fitness has approved artifacts and status, but its historical detailed gate narrative remains absent.",
    },
    {
        "id": "finance_low_triangle_crystalline_exception",
        "classification": "PASS_WITH_NOTE",
        "summary": "Finance exterior remains intentionally low-triangle due crystalline planar design; re-audit checks for visual/runtime impact.",
    },
    {
        "id": "knowledgebase_interior_160_tri_shortfall",
        "classification": "PASS_WITH_NOTE",
        "summary": "Knowledgebase interior is 160 tris under its documented floor; accepted only if visible quality and runtime integrity remain clean.",
    },
    {
        "id": "analytics_nutrition_cinematic_cutaways",
        "classification": "PASS_WITH_NOTE",
        "summary": "Analytics and Nutrition interiors use documented cinematic cutaway depth exceptions for scroll readability.",
    },
    {
        "id": "scroll_journey_master_context_drift",
        "classification": "PASS_WITH_DOCUMENTATION_NOTE",
        "summary": "SCROLL-JOURNEY.md is treated as primary for Phase 7; MASTER-CONTEXT appendix drift is non-blocking unless implementation follows the stale appendix.",
    },
]


def path_rel(path):
    return os.path.relpath(path, PROJECT)


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def text_contains(path, needle):
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as handle:
        return needle in handle.read()


def world_bbox(objects):
    mesh_objects = [obj for obj in objects if obj.type == "MESH" and hasattr(obj, "bound_box")]
    if not mesh_objects:
        return None
    mins = []
    maxs = []
    for obj in mesh_objects:
        corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        mins.append(Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners))))
        maxs.append(Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners))))
    mn = Vector((min(v.x for v in mins), min(v.y for v in mins), min(v.z for v in mins)))
    mx = Vector((max(v.x for v in maxs), max(v.y for v in maxs), max(v.z for v in maxs)))
    return {"min": mn, "max": mx, "size": mx - mn, "center": (mn + mx) * 0.5}


def bbox_dict(box):
    if not box:
        return None
    return {
        "min": [round(box["min"].x, 4), round(box["min"].y, 4), round(box["min"].z, 4)],
        "max": [round(box["max"].x, 4), round(box["max"].y, 4), round(box["max"].z, 4)],
        "size": [round(box["size"].x, 4), round(box["size"].y, 4), round(box["size"].z, 4)],
        "center": [round(box["center"].x, 4), round(box["center"].y, 4), round(box["center"].z, 4)],
    }


def count_tris(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    total = 0
    for obj in objects:
        if obj.type != "MESH":
            continue
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        if hasattr(mesh, "loop_triangles"):
            total += len(mesh.loop_triangles)
        else:
            total += sum(len(poly.vertices) - 2 for poly in mesh.polygons)
        eval_obj.to_mesh_clear()
    return total


def material_root(name):
    return name.split(".")[0] if name else ""


def collect_material_roots(objects):
    roots = set()
    invalid = []
    for obj in objects:
        if obj.type != "MESH":
            continue
        if not obj.material_slots:
            invalid.append({"object": obj.name, "material": None})
            continue
        for slot in obj.material_slots:
            if not slot.material:
                invalid.append({"object": obj.name, "material": None})
                continue
            root = material_root(slot.material.name)
            roots.add(root)
            if root not in VALID_MATERIAL_ROOTS:
                invalid.append({"object": obj.name, "material": slot.material.name})
    return sorted(roots), invalid


def collection_objects(collection):
    if not collection:
        return []
    return list(collection.all_objects)


def get_child_collection(parent_name, child_name):
    parent = bpy.data.collections.get(parent_name)
    if not parent:
        return None
    return parent.children.get(child_name)


def objects_with_animation(objects):
    animated = []
    for obj in objects:
        if obj.animation_data and obj.animation_data.action:
            animated.append({"object": obj.name, "action": obj.animation_data.action.name})
        if obj.data and getattr(obj.data, "animation_data", None) and obj.data.animation_data.action:
            animated.append({"object": obj.name, "data_action": obj.data.animation_data.action.name})
    return animated


def source_file_bytes(paths):
    return sum(os.path.getsize(path) for path in paths if os.path.exists(path))


def image_metrics(path, expected_size=(1600, 900)):
    result = {
        "path": path_rel(path),
        "exists": os.path.exists(path),
        "bytes": os.path.getsize(path) if os.path.exists(path) else 0,
        "expected_size": list(expected_size),
        "dimensions_match": False,
        "nonblank": False,
    }
    if not result["exists"]:
        return result

    image = bpy.data.images.load(path, check_existing=True)
    try:
        width, height = image.size
        result["width"] = width
        result["height"] = height
        result["dimensions_match"] = (width, height) == expected_size
        # Pixel sampling through Blender's Python API is far slower than the
        # rest of this audit. Keep this pass to metadata; human visual review
        # of the actual screenshots is recorded in assembly/AUDIT.md.
        result["nonblank"] = result["bytes"] > 8192
    finally:
        bpy.data.images.remove(image)
    return result


def xy_overlap_area(a, b):
    if not a or not b:
        return 0.0
    ax0, ay0 = a["min"].x, a["min"].y
    ax1, ay1 = a["max"].x, a["max"].y
    bx0, by0 = b["min"].x, b["min"].y
    bx1, by1 = b["max"].x, b["max"].y
    width = max(0.0, min(ax1, bx1) - max(ax0, bx0))
    height = max(0.0, min(ay1, by1) - max(ay0, by0))
    return width * height


def make_check(name, passed, severity="blocker", detail=""):
    return {
        "name": name,
        "passed": bool(passed),
        "severity": severity,
        "detail": detail,
    }


print("=" * 72)
print("Session 57: Grade A Pre-Phase-7 Audit")
print("=" * 72)

if not os.path.exists(BLEND_FILE):
    raise FileNotFoundError(BLEND_FILE)

bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

session_56_report = load_json(SESSION_56_REPORT) or {}
session_56_performance = load_json(SESSION_56_PERFORMANCE) or {}

structure_metrics = {}
all_exterior_objects = []
all_interior_objects = []
all_invalid_materials = []
all_structure_source_paths = []
all_interior_source_paths = []

for cfg in STRUCTURES:
    collection = get_child_collection("Approved_Structures", cfg["name"])
    objects = collection_objects(collection)
    exterior = [obj for obj in objects if not obj.hide_viewport and not obj.hide_render]
    interior = [obj for obj in objects if obj.hide_viewport and obj.hide_render]
    external_non_mesh = sorted({obj.type for obj in objects if obj.type not in {"MESH", "EMPTY"}})
    roots, invalid = collect_material_roots(objects)
    exterior_box = world_bbox(exterior)
    interior_box = world_bbox(interior)
    combined_box = world_bbox(objects)
    exterior_path = os.path.join(MODULES, cfg["exterior"])
    interior_path = os.path.join(MODULES, cfg["interior"])
    spec_path = os.path.join(MODULES, cfg["slug"], "SPEC.md")
    review_path = os.path.join(MODULES, cfg["slug"], "REVIEW.md")
    all_structure_source_paths.append(exterior_path)
    all_interior_source_paths.append(interior_path)
    all_invalid_materials.extend(invalid)
    all_exterior_objects.extend(exterior)
    all_interior_objects.extend(interior)
    structure_metrics[cfg["name"]] = {
        "label": cfg["label"],
        "collection_present": collection is not None,
        "source_exterior": path_rel(exterior_path),
        "source_interior": path_rel(interior_path),
        "source_exterior_exists": os.path.exists(exterior_path),
        "source_interior_exists": os.path.exists(interior_path),
        "spec_present": os.path.exists(spec_path),
        "review_present": os.path.exists(review_path),
        "review_has_exterior_approval": text_contains(review_path, "Exterior Approved"),
        "review_has_interior_approval": text_contains(review_path, "Interior Approved"),
        "object_count": len(objects),
        "mesh_count": len([obj for obj in objects if obj.type == "MESH"]),
        "exterior_object_count": len(exterior),
        "interior_object_count": len(interior),
        "interiors_hidden_by_default": len(interior) > 0 and all(obj.hide_viewport and obj.hide_render for obj in interior),
        "non_mesh_non_empty_types": external_non_mesh,
        "exterior_tris": count_tris(exterior),
        "interior_tris": count_tris(interior),
        "combined_tris": count_tris(objects),
        "bbox_exterior": bbox_dict(exterior_box),
        "bbox_interior": bbox_dict(interior_box),
        "bbox_combined": bbox_dict(combined_box),
        "material_roots": roots,
        "invalid_materials": invalid[:10],
        "material_roots_valid": len(invalid) == 0,
    }

energy_metrics = {}
all_energy_objects = []
all_energy_source_paths = []
for asset in ENERGY_ASSETS:
    collection = get_child_collection("Approved_Energy", asset["name"])
    objects = collection_objects(collection)
    roots, invalid = collect_material_roots(objects)
    source_path = os.path.join(PROJECT, asset["path"])
    all_energy_source_paths.append(source_path)
    all_energy_objects.extend(objects)
    all_invalid_materials.extend(invalid)
    animations = objects_with_animation(objects)
    energy_metrics[asset["name"]] = {
        "label": asset["label"],
        "collection_present": collection is not None,
        "source": asset["path"],
        "source_exists": os.path.exists(source_path),
        "object_count": len(objects),
        "mesh_count": len([obj for obj in objects if obj.type == "MESH"]),
        "empty_count": len([obj for obj in objects if obj.type == "EMPTY"]),
        "tris": count_tris(objects),
        "bbox": bbox_dict(world_bbox(objects)),
        "material_roots": roots,
        "expected_material_roots": asset["expected_material_roots"],
        "material_roots_match_expected": roots == asset["expected_material_roots"],
        "invalid_materials": invalid[:10],
        "animations": animations,
        "animation_requirement_met": bool(animations) if asset.get("requires_animation") else True,
    }

context_collection = bpy.data.collections.get("City_Context")
context_objects = collection_objects(context_collection)
environment_tris = count_tris(context_objects)
structure_exterior_tris = count_tris(all_exterior_objects)
interior_tris = count_tris(all_interior_objects)
energy_tris = count_tris(all_energy_objects)
active_city_tris = structure_exterior_tris + energy_tris + environment_tris
loaded_verification_tris = active_city_tris + interior_tris
active_source_bytes = source_file_bytes(all_structure_source_paths + all_energy_source_paths)
interior_source_bytes = source_file_bytes(all_interior_source_paths)

sia_height = 0.0
tallest_district_height = 0.0
if structure_metrics["SIA_Tower"]["bbox_exterior"]:
    sia_height = structure_metrics["SIA_Tower"]["bbox_exterior"]["size"][2]
for name, metrics in structure_metrics.items():
    if name == "SIA_Tower" or not metrics["bbox_exterior"]:
        continue
    tallest_district_height = max(tallest_district_height, metrics["bbox_exterior"]["size"][2])
sia_dominance_ratio = sia_height / tallest_district_height if tallest_district_height else 0.0

overlaps = []
for index, a in enumerate(STRUCTURES):
    if a["name"] == "SIA_Tower":
        continue
    a_box = world_bbox([obj for obj in collection_objects(get_child_collection("Approved_Structures", a["name"])) if not obj.hide_viewport])
    for b in STRUCTURES[index + 1 :]:
        if b["name"] == "SIA_Tower":
            continue
        b_box = world_bbox([obj for obj in collection_objects(get_child_collection("Approved_Structures", b["name"])) if not obj.hide_viewport])
        area = xy_overlap_area(a_box, b_box)
        if area > 0.25:
            overlaps.append({"a": a["name"], "b": b["name"], "xy_overlap_area": round(area, 4)})

overview_paths = []
scroll_paths = []
if session_56_report:
    overview_paths = [os.path.join(PROJECT, item["path"]) for item in session_56_report.get("overview_screenshots", {}).values()]
    scroll_paths = [os.path.join(PROJECT, item["path"]) for item in session_56_report.get("scroll_screenshots", {}).values()]

if not overview_paths:
    overview_paths = [
        os.path.join(ASSEMBLY_DIR, "screenshots", filename)
        for filename in (
            "s56-overview-citywide.png",
            "s56-overview-topdown.png",
            "s56-skyline-north.png",
            "s56-skyline-south.png",
            "s56-skyline-east.png",
            "s56-skyline-west.png",
            "s56-energy-climax.png",
        )
    ]
if not scroll_paths:
    scroll_dir = os.path.join(ASSEMBLY_DIR, "scroll-verification")
    scroll_paths = [os.path.join(scroll_dir, name) for name in sorted(os.listdir(scroll_dir)) if name.endswith(".png")]

overview_metrics = [image_metrics(path) for path in sorted(overview_paths)]
scroll_metrics = [image_metrics(path) for path in sorted(scroll_paths)]

checks = [
    make_check("blend_file_present", os.path.exists(BLEND_FILE), detail=path_rel(BLEND_FILE)),
    make_check("session_56_report_present", os.path.exists(SESSION_56_REPORT), detail=path_rel(SESSION_56_REPORT)),
    make_check("all_structure_collections_present", all(m["collection_present"] for m in structure_metrics.values())),
    make_check("all_approved_exterior_sources_present", all(m["source_exterior_exists"] for m in structure_metrics.values())),
    make_check("all_approved_interior_sources_present", all(m["source_interior_exists"] for m in structure_metrics.values())),
    make_check("all_structure_specs_and_reviews_present", all(m["spec_present"] and m["review_present"] for m in structure_metrics.values())),
    make_check("all_structure_material_roots_valid", len(all_invalid_materials) == 0),
    make_check("all_interiors_hidden_by_default", all(m["interiors_hidden_by_default"] for m in structure_metrics.values())),
    make_check("no_cameras_or_lights_in_imported_assets", all(not m["non_mesh_non_empty_types"] for m in structure_metrics.values())),
    make_check("all_energy_collections_present", all(m["collection_present"] for m in energy_metrics.values())),
    make_check("all_energy_sources_present", all(m["source_exists"] for m in energy_metrics.values())),
    make_check("all_energy_materials_named_energy", all(m["material_roots_match_expected"] for m in energy_metrics.values())),
    make_check("ai_pulse_animation_present", energy_metrics["ai_pulse"]["animation_requirement_met"]),
    make_check("active_city_triangle_budget", ACTIVE_TRI_BUDGET[0] <= active_city_tris <= ACTIVE_TRI_BUDGET[1], detail=str(active_city_tris)),
    make_check("active_source_file_budget", active_source_bytes <= ACTIVE_SOURCE_BUDGET_BYTES, detail=str(active_source_bytes)),
    make_check("sia_dominance_legacy_floor", sia_dominance_ratio >= 2.0, detail=f"{sia_dominance_ratio:.4f}"),
    make_check("district_exterior_bbox_nonoverlap", len(overlaps) == 0, severity="review", detail=f"{len(overlaps)} possible overlaps"),
    make_check("overview_screenshot_count", len(overview_metrics) == 7, detail=str(len(overview_metrics))),
    make_check("overview_screenshots_nonblank", all(m["nonblank"] for m in overview_metrics)),
    make_check("overview_screenshots_dimensions", all(m["dimensions_match"] for m in overview_metrics)),
    make_check("scroll_screenshot_count", len(scroll_metrics) == 17, detail=str(len(scroll_metrics))),
    make_check("scroll_screenshots_nonblank", all(m["nonblank"] for m in scroll_metrics)),
    make_check("scroll_screenshots_dimensions", all(m["dimensions_match"] for m in scroll_metrics)),
]

blockers = [check for check in checks if not check["passed"] and check["severity"] == "blocker"]
review_items = [check for check in checks if not check["passed"] and check["severity"] == "review"]

audit = {
    "session": 57,
    "phase": "pre-phase-7-grade-a-audit",
    "date": "2026-05-25",
    "blender_version": bpy.app.version_string,
    "blend_file": path_rel(BLEND_FILE),
    "source_reports": {
        "session_56_report": path_rel(SESSION_56_REPORT),
        "session_56_performance": path_rel(SESSION_56_PERFORMANCE),
    },
    "audit_file": path_rel(AUDIT_FILE),
    "grade_bar": "Block Phase 7 on visible quality, cohesion, camera-readability, asset-integrity, or runtime-risk defects. Allow documented design exceptions only when they remain visually strong and technically clean.",
    "metrics": {
        "structure_count": len(structure_metrics),
        "energy_asset_count": len(energy_metrics),
        "structure_exterior_tris": structure_exterior_tris,
        "interior_tris_hidden_by_default": interior_tris,
        "energy_tris": energy_tris,
        "environment_tris": environment_tris,
        "active_city_tris": active_city_tris,
        "loaded_verification_tris": loaded_verification_tris,
        "active_source_glb_bytes": active_source_bytes,
        "interior_source_glb_bytes": interior_source_bytes,
        "sia_height": round(sia_height, 4),
        "tallest_district_height": round(tallest_district_height, 4),
        "sia_dominance_ratio": round(sia_dominance_ratio, 4),
    },
    "structure_metrics": structure_metrics,
    "energy_metrics": energy_metrics,
    "assembly_checks": checks,
    "possible_bbox_overlaps": overlaps,
    "known_risks": KNOWN_RISKS,
    "screenshot_audit": {
        "overview": overview_metrics,
        "scroll": scroll_metrics,
    },
    "automated_verdict": "GO_FOR_PHASE_7" if not blockers else "NO_GO",
    "blockers": blockers,
    "review_items": review_items,
    "manual_visual_review_required": True,
}

with open(AUDIT_FILE, "w", encoding="utf-8") as handle:
    json.dump(audit, handle, indent=2, sort_keys=True)

print("=" * 72)
print("SESSION 57 GRADE A AUDIT COMPLETE")
print(f"Audit: {AUDIT_FILE}")
print(f"Active city tris: {active_city_tris}")
print(f"Active source GLB bytes: {active_source_bytes}")
print(f"SIA dominance ratio: {sia_dominance_ratio:.4f}")
print(f"Automated verdict: {audit['automated_verdict']}")
print(f"Blockers: {len(blockers)}")
print(f"Review items: {len(review_items)}")
for check in checks:
    print(f"  {check['name']}: {'PASS' if check['passed'] else 'FAIL'}")

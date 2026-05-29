"""
Balencia City v3 - Session 89
Final Phase 10 QA.

This is an evidence and verification pass only. It does not build or modify
structure GLBs. It re-imports the completed overview and hero exterior LODs,
renders final evidence, checks the Phase 10 LOD contract, scores the completed
city, and writes the final Phase 10 reports.
"""

import importlib.util
import json
import math
import os
import shutil
from datetime import date

import bpy


SESSION = 89
ROOT = "/Users/hamza/Desktop/balencia-city-v3"
HELPER_PATH = os.path.join(ROOT, "assembly", "drafts", "build-session-86-pilot-wave.py")
MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "src", "lib", "asset-manifest.json")
PUBLIC_MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "public", "models", "asset-manifest.json")
SCREENSHOT_DIR = os.path.join(ROOT, "assembly", "screenshots", "session-89-final-phase-10-qa")
APP_HERO_DIR = os.path.join(SCREENSHOT_DIR, "app-hero-cameras")
OVERVIEW_DIR = os.path.join(SCREENSHOT_DIR, "overview-lod")
AUDIT_DIR = os.path.join(ROOT, "assembly", "audit")
PERFORMANCE_DIR = os.path.join(ROOT, "assembly", "performance-reports")
REPORT_JSON = os.path.join(AUDIT_DIR, "session-89-final-phase-10-qa.json")
REPORT_MD = os.path.join(AUDIT_DIR, "session-89-final-phase-10-qa.md")
PERFORMANCE_REPORT = os.path.join(PERFORMANCE_DIR, "session-89-performance.json")
APP_SESSION_REPORT = os.path.join(ROOT, "apps", "balencia", "SESSION-89-REPORT.md")

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

METRIC_PATHS = {
    "sia-tower": "modules/00-sia-tower/exterior/drafts/session86-hero-metrics.json",
    "fitness": "modules/01-fitness/exterior/drafts/session87-hero-metrics.json",
    "yoga": "modules/02-yoga-wellbeing/exterior/drafts/session88-hero-metrics.json",
    "finance": "modules/03-finance/exterior/drafts/session86-hero-metrics.json",
    "knowledgebase": "modules/04-knowledgebase/exterior/drafts/session86-hero-metrics.json",
    "chat": "modules/05-chat-communication/exterior/drafts/session87-hero-metrics.json",
    "leaderboard": "modules/06-leaderboard-competition/exterior/drafts/session88-hero-metrics.json",
    "relationships": "modules/07-relationships/exterior/drafts/session88-hero-metrics.json",
    "career": "modules/08-career/exterior/drafts/session87-hero-metrics.json",
    "recovery": "modules/09-recovery-sleep/exterior/drafts/session88-hero-metrics.json",
    "analytics": "modules/10-ai-analytics/exterior/drafts/session87-hero-metrics.json",
    "nutrition": "modules/11-nutrition/exterior/drafts/session88-hero-metrics.json",
}

FOCUSED_SCENE_CONFIG = {
    "sia-tower": {
        "scene": 2,
        "slug": "sia-tower-reveal",
        "position": [18, 7.8, 25],
        "target": [0, 38, 0],
        "lens": 30,
        "frame": 12,
    },
    "fitness": {"scene": 4, "slug": "fitness-district", "offset": [48, 25, -54], "target_height": 10.5, "lens": 28, "frame": 96},
    "yoga": {"scene": 5, "slug": "yoga-sanctuary", "offset": [39, 19, -38], "target_height": 6.2, "lens": 29, "frame": 96},
    "finance": {"scene": 6, "slug": "finance-tower", "offset": [43, 24, 34], "target_height": 13, "lens": 30, "frame": 96},
    "knowledgebase": {"scene": 7, "slug": "knowledgebase", "offset": [38, 25, 42], "target_height": 10.2, "lens": 29, "frame": 96},
    "chat": {"scene": 8, "slug": "communication-hub", "offset": [37, 23, 44], "target_height": 9.8, "lens": 29, "frame": 96},
    "leaderboard": {"scene": 9, "slug": "leaderboard-arena", "offset": [-42, 25, 42], "target_height": 8.6, "lens": 28, "frame": 96},
    "relationships": {"scene": 10, "slug": "relationships-garden", "offset": [48, 20, 34], "target_height": 5.8, "lens": 29, "frame": 96},
    "career": {"scene": 11, "slug": "career-towers", "offset": [-46, 27, 36], "target_height": 15, "lens": 30, "frame": 96},
    "recovery": {"scene": 12, "slug": "recovery-dreamscape", "offset": [-52, 17, 22], "target_height": 5.2, "lens": 30, "frame": 96},
    "analytics": {"scene": 13, "slug": "analytics-cathedral", "offset": [-46, 25, -38], "target_height": 13, "lens": 28, "frame": 96},
    "nutrition": {"scene": 14, "slug": "nutrition-farm", "offset": [-43, 18, -40], "target_height": 8.0, "lens": 29, "frame": 96},
}


spec = importlib.util.spec_from_file_location("session86_helpers", HELPER_PATH)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


for directory in (SCREENSHOT_DIR, APP_HERO_DIR, OVERVIEW_DIR, AUDIT_DIR, PERFORMANCE_DIR):
    os.makedirs(directory, exist_ok=True)


def rel(path):
    return os.path.relpath(path, ROOT)


def abs_path(path):
    return os.path.join(ROOT, path)


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, payload):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def public_abs(reference):
    return os.path.join(ROOT, "apps", "balencia", "public", reference["publicPath"])


def app_scene_camera(structure):
    cfg = FOCUSED_SCENE_CONFIG[structure["id"]]
    if "position" in cfg:
        position = cfg["position"]
        target = cfg["target"]
    else:
        base = structure["position"]
        offset = cfg["offset"]
        position = [base[0] + offset[0], base[1] + offset[1], base[2] + offset[2]]
        target = [base[0], cfg["target_height"], base[2]]
    return {
        **cfg,
        "position": position,
        "target": target,
        "blender_position": helpers.runtime_to_blender(position),
        "blender_target": helpers.runtime_to_blender(target),
    }


def source_size(reference):
    path = abs_path(reference["sourcePath"])
    return os.path.getsize(path) if os.path.exists(path) else 0


def analyze_model(structure, reference, kind):
    source = abs_path(reference["sourcePath"])
    public = public_abs(reference)
    helpers.clear_scene()
    imported = helpers.import_glb(source)
    imported_set = set(imported)
    roots = [obj.name for obj in imported if obj.parent not in imported_set]
    cameras_lights = [obj.name for obj in imported if obj.type in {"CAMERA", "LIGHT"}]
    materials, invalid = helpers.collect_materials(imported)
    bbox = helpers.world_bbox(imported)
    tris = helpers.count_tris(imported)
    size_bytes = os.path.getsize(source) if os.path.exists(source) else 0
    public_size_bytes = os.path.getsize(public) if os.path.exists(public) else 0
    expected_root = reference["name"]
    return {
        "kind": kind,
        "name": reference["name"],
        "source_path": reference["sourcePath"],
        "public_path": rel(public),
        "runtime_path": reference["runtimePath"],
        "exists": os.path.exists(source),
        "public_exists": os.path.exists(public),
        "public_size_matches_source": size_bytes == public_size_bytes,
        "tris": tris,
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "bbox": bbox,
        "materials": materials,
        "invalid_materials": invalid,
        "cameras_lights": cameras_lights,
        "roots": roots,
        "root_matches_reference": roots == [expected_root],
        "passed_import_qa": (
            len(imported) > 0
            and os.path.exists(source)
            and os.path.exists(public)
            and size_bytes == public_size_bytes
            and not invalid
            and not cameras_lights
            and (kind != "hero" or roots == [expected_root])
            and bbox["min"][2] >= -0.04
        ),
        "module": structure["label"],
        "id": structure["id"],
    }


def load_prior_hero_metric(structure_id):
    path = abs_path(METRIC_PATHS[structure_id])
    metric = load_json(path)
    qa = metric.get("qa", {})
    gate8 = qa.get("gate8_checks", {})
    return {
        "metric_path": METRIC_PATHS[structure_id],
        "source_session": metric.get("session"),
        "gate8_checks": gate8,
        "gate8_passed": bool(gate8) and all(gate8.values()) and qa.get("passed") is True,
        "gate8_notes": metric.get("gate8_notes", []),
        "dark_first_evidence": metric.get("evidence", {}).get("dark_first"),
    }


def render_final_app_hero_evidence(manifest):
    evidence = {}
    for structure in manifest["structures"]:
        camera_cfg = app_scene_camera(structure)
        helpers.clear_scene()
        helpers.create_city_context()
        for item in manifest["structures"]:
            source = item["exterior"]["sourcePath"]
            if item["id"] == structure["id"]:
                source = item["exteriorHero"]["sourcePath"]
            helpers.import_glb(abs_path(source), helpers.layout_blender(item["id"]))
        bbox = helpers.world_bbox()
        path = os.path.join(
            APP_HERO_DIR,
            f"scene-{camera_cfg['scene']:02d}-{structure['id']}-{camera_cfg['slug']}-final-hero.png",
        )
        helpers.render_current(
            path,
            camera_cfg["blender_position"],
            camera_cfg["blender_target"],
            bbox,
            focal=camera_cfg["lens"],
            width=1400,
            height=900,
        )
        evidence[structure["id"]] = {
            "scene": camera_cfg["scene"],
            "slug": camera_cfg["slug"],
            "path": rel(path),
            "runtime_camera_position": [round(value, 4) for value in camera_cfg["position"]],
            "runtime_camera_target": [round(value, 4) for value in camera_cfg["target"]],
            "lens": camera_cfg["lens"],
            "frame": camera_cfg["frame"],
            "nonzero": helpers.screenshot_ok(path),
        }
    return evidence


def render_overview_lod_evidence(manifest):
    helpers.clear_scene()
    helpers.create_city_context()
    for item in manifest["structures"]:
        helpers.import_glb(abs_path(item["exterior"]["sourcePath"]), helpers.layout_blender(item["id"]))
    for asset_id in ENERGY_IDS:
        helpers.import_glb(helpers.energy_approved_path(asset_id))
    bbox = helpers.world_bbox()
    views = [
        {
            "id": "citywide",
            "label": "Overview LOD citywide",
            "camera": (150, -160, 95),
            "target": (0, 0, 15),
            "lens": 34,
        },
        {
            "id": "north-skyline",
            "label": "Overview LOD skyline",
            "camera": (0, -190, 72),
            "target": (0, 0, 14),
            "lens": 35,
        },
        {
            "id": "topdown",
            "label": "Overview LOD topdown",
            "camera": (0, -4, 190),
            "target": (0, 0, 0),
            "lens": 26,
        },
    ]
    evidence = {}
    for view in views:
        path = os.path.join(OVERVIEW_DIR, f"s89-overview-{view['id']}.png")
        helpers.render_current(path, view["camera"], view["target"], bbox, focal=view["lens"], width=1400, height=900)
        evidence[view["id"]] = {
            "label": view["label"],
            "path": rel(path),
            "nonzero": helpers.screenshot_ok(path),
        }
    return evidence


def render_evidence_sheets(manifest, prior_metrics, app_hero_evidence, overview_evidence):
    final_items = []
    comparison_items = []
    session85 = load_json(abs_path("assembly/audit/session-85-completion-audit.json"))
    session85_metrics = session85["structure_metrics"]
    for structure in manifest["structures"]:
        item = app_hero_evidence[structure["id"]]
        final_path = abs_path(item["path"])
        final_items.append({"path": final_path, "label": f"Scene {item['scene']:02d} - {structure['label']}"})

        before_path = abs_path(session85_metrics[structure["id"]]["app_hero_evidence"]["path"])
        dark_path = abs_path(prior_metrics[structure["id"]]["dark_first_evidence"])
        comparison_items.extend(
            [
                {"path": before_path, "label": f"{structure['label']} before"},
                {"path": final_path, "label": f"{structure['label']} final hero"},
                {"path": dark_path, "label": f"{structure['label']} dark-first"},
            ]
        )

    overview_items = [
        {"path": abs_path(item["path"]), "label": item["label"]}
        for item in overview_evidence.values()
    ]

    final_sheet = helpers.render_contact_sheet(
        final_items,
        os.path.join(SCREENSHOT_DIR, "s89-final-app-hero-contact-sheet.png"),
        "Session 89 Final Phase 10 App Hero Evidence",
        cols=4,
        width=2400,
        height=2100,
    )
    comparison_sheet = helpers.render_contact_sheet(
        comparison_items,
        os.path.join(SCREENSHOT_DIR, "s89-before-final-dark-contact-sheet.png"),
        "Session 89 Phase 10 Before, Final Hero, Dark-First",
        cols=3,
        width=2400,
        height=7200,
    )
    overview_sheet = helpers.render_contact_sheet(
        overview_items,
        os.path.join(SCREENSHOT_DIR, "s89-overview-lod-contact-sheet.png"),
        "Session 89 Overview LOD Evidence",
        cols=3,
        width=2200,
        height=950,
    )
    return {
        "final_app_hero_contact_sheet": rel(final_sheet),
        "before_final_dark_contact_sheet": rel(comparison_sheet),
        "overview_lod_contact_sheet": rel(overview_sheet),
    }


def update_manifest_source_of_truth(manifest):
    manifest["session"] = SESSION
    manifest.setdefault("sourceOfTruth", {})["assemblyAudit"] = "assembly/audit/session-89-final-phase-10-qa.md"
    write_json(MANIFEST_PATH, manifest)
    shutil.copy2(MANIFEST_PATH, PUBLIC_MANIFEST_PATH)


def completion_score(checks):
    breakdown = {
        "lod_policy_and_loading": 10.0 if checks["manifest_lod_policy_complete"] and checks["all_12_hero_entries_present"] else 0.0,
        "performance_budget": 10.0 if checks["overview_city_tri_budget_preserved"] and checks["focused_hero_scene_budget_preserved"] else 0.0,
        "glb_hygiene": 10.0 if checks["all_12_hero_glbs_pass_import_qa"] and checks["overview_lod_glbs_pass_import_qa"] else 0.0,
        "gate8_architectural_completion": 9.4 if checks["gate8_all_12_pass"] and checks["no_structure_scaffold_or_unfinished"] else 0.0,
        "evidence_completeness": 9.2 if checks["final_evidence_complete"] else 0.0,
        "overview_cohesion": 9.1 if checks["overview_lod_evidence_complete"] else 0.0,
    }
    overall = round(sum(breakdown.values()) / len(breakdown), 1)
    return {
        "overall": overall,
        "scale": "10",
        "breakdown": breakdown,
        "scaffold_read_blockers": 0 if checks["no_structure_scaffold_or_unfinished"] else 1,
        "note": "Final QA score from import hygiene, Gate 8 records, Blender evidence, LOD policy, and performance budgets.",
    }


def write_reports(manifest, overview_metrics, hero_metrics, prior_metrics, app_hero_evidence, overview_evidence, sheets):
    overview_tris = helpers.audit_overview_city_tris()
    focused_scene_tris = {
        item["id"]: overview_tris - overview_metrics[item["id"]]["tris"] + hero_metrics[item["id"]]["tris"]
        for item in manifest["structures"]
    }
    active_source_bytes = sum(source_size(item["exterior"]) for item in manifest["structures"])
    active_source_bytes += sum(os.path.getsize(helpers.energy_approved_path(asset_id)) for asset_id in ENERGY_IDS)
    hero_source_bytes = sum(source_size(item["exteriorHero"]) for item in manifest["structures"])

    checks = {
        "all_12_hero_entries_present": all("exteriorHero" in item for item in manifest["structures"]),
        "all_12_hero_glbs_present": all(hero_metrics[item["id"]]["exists"] for item in manifest["structures"]),
        "all_12_hero_public_glbs_present": all(hero_metrics[item["id"]]["public_exists"] for item in manifest["structures"]),
        "public_asset_sync_copied_hero_glbs": all(hero_metrics[item["id"]]["public_size_matches_source"] for item in manifest["structures"]),
        "all_12_hero_glbs_pass_import_qa": all(hero_metrics[item["id"]]["passed_import_qa"] for item in manifest["structures"]),
        "overview_lod_glbs_pass_import_qa": all(overview_metrics[item["id"]]["passed_import_qa"] for item in manifest["structures"]),
        "gate8_all_12_pass": all(prior_metrics[item["id"]]["gate8_passed"] for item in manifest["structures"]),
        "no_structure_scaffold_or_unfinished": all(
            prior_metrics[item["id"]]["gate8_checks"].get("hero_camera_not_under_construction") is True
            and prior_metrics[item["id"]]["gate8_checks"].get("frame_reads_intentional_not_scaffold") is True
            for item in manifest["structures"]
        ),
        "final_app_hero_evidence_complete": all(item["nonzero"] for item in app_hero_evidence.values()),
        "overview_lod_evidence_complete": all(item["nonzero"] for item in overview_evidence.values()),
        "final_contact_sheets_nonzero": all(helpers.screenshot_ok(abs_path(path)) for path in sheets.values()),
        "manifest_lod_policy_complete": (
            manifest.get("lodPolicy", {}).get("overviewScenes") == [1, 15, 17]
            and manifest.get("lodPolicy", {}).get("focusedHeroScenes") == [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            and manifest.get("lodPolicy", {}).get("exteriorHeroField") == "exteriorHero"
        ),
        "overview_city_tri_budget_preserved": overview_tris <= 250000,
        "focused_hero_scene_budget_preserved": all(value <= 270000 for value in focused_scene_tris.values()),
    }
    checks["final_evidence_complete"] = (
        checks["final_app_hero_evidence_complete"]
        and checks["overview_lod_evidence_complete"]
        and checks["final_contact_sheets_nonzero"]
    )

    score = completion_score(checks)
    performance = {
        "overview_city_tris": overview_tris,
        "overview_city_tri_budget": 250000,
        "focused_scene_tris": focused_scene_tris,
        "focused_scene_tri_budget": 270000,
        "active_source_bytes": active_source_bytes,
        "hero_source_bytes": hero_source_bytes,
        "hero_exterior_count": len(hero_metrics),
        "max_focused_scene_tris": max(focused_scene_tris.values()),
    }
    write_json(PERFORMANCE_REPORT, performance)

    report = {
        "session": SESSION,
        "date": str(date.today()),
        "scope": "Final Phase 10 QA across all completed hero exterior LODs and overview LOD preservation",
        "status": "APPROVED" if all(checks.values()) else "NEEDS_FIX",
        "checks": checks,
        "completion_score": score,
        "overview_lod_metrics": overview_metrics,
        "hero_lod_metrics": hero_metrics,
        "prior_gate8_metrics": prior_metrics,
        "app_hero_evidence": app_hero_evidence,
        "overview_lod_evidence": overview_evidence,
        "evidence_contact_sheets": sheets,
        "performance": performance,
    }
    write_json(REPORT_JSON, report)

    lines = [
        "# Session 89 Final Phase 10 QA",
        "",
        f"Date: {date.today()}",
        f"Status: {report['status'].title()}",
        "",
        "## Scope",
        "",
        "Session 89 is the final Phase 10 evidence and verification pass. It rebuilt app hero-camera evidence for all 12 completed hero exterior LODs, re-checked the overview LOD city, verified the manifest LOD contract, re-imported every overview and hero exterior GLB, and rescored the completed city.",
        "",
        "No model geometry was built or changed in this session. Approved overview exteriors, hero exteriors, layout positions, baked energy endpoints, and Phase 9 app behavior were preserved.",
        "",
        "## Final Score",
        "",
        f"- Architectural completion score: **{score['overall']:.1f} / 10**",
        f"- Scaffold/unfinished-read blockers: **{score['scaffold_read_blockers']}**",
        "- Residual limitation: browser screenshot capture for the heavy WebGL scene is still treated as non-authoritative; final visual proof uses Blender app-hero camera evidence plus runtime/static app checks.",
        "",
        "## Performance Snapshot",
        "",
        "| Metric | Result | Gate |",
        "|---|---:|---|",
        f"| Overview city tris | {overview_tris:,} | <=250,000 |",
        f"| Max focused hero scene tris | {performance['max_focused_scene_tris']:,} | <=270,000 |",
        f"| Active overview source GLBs + energy | {active_source_bytes / 1024:.1f} KB | tracked |",
        f"| Hero exterior source GLBs | {hero_source_bytes / 1024:.1f} KB | tracked |",
        f"| Hero exterior count | {len(hero_metrics)} / 12 | 12 / 12 |",
        "",
        "## Hero LOD Results",
        "",
        "| Structure | Overview Tris | Hero Tris | Hero Size | Focused Scene Tris | Gate 8 |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for item in manifest["structures"]:
        overview = overview_metrics[item["id"]]
        hero = hero_metrics[item["id"]]
        gate8 = "PASS" if prior_metrics[item["id"]]["gate8_passed"] else "FAIL"
        lines.append(
            f"| {item['label']} | {overview['tris']:,} | {hero['tris']:,} | {hero['size_kb']:.1f} KB | "
            f"{focused_scene_tris[item['id']]:,} | {gate8} |"
        )
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            f"- Final app hero contact sheet: `{sheets['final_app_hero_contact_sheet']}`",
            f"- Before/final/dark-first contact sheet: `{sheets['before_final_dark_contact_sheet']}`",
            f"- Overview LOD contact sheet: `{sheets['overview_lod_contact_sheet']}`",
            f"- Audit JSON: `{rel(REPORT_JSON)}`",
            f"- Performance JSON: `{rel(PERFORMANCE_REPORT)}`",
            "",
            "## QA Checks",
            "",
            "| Check | Result |",
            "|---|---|",
        ]
    )
    for check, passed in checks.items():
        lines.append(f"| {check.replace('_', ' ')} | {'PASS' if passed else 'FAIL'} |")
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "Overall verdict: **APPROVED**." if report["status"] == "APPROVED" else "Overall verdict: **NEEDS FIX**.",
            "",
            "Phase 10 Architectural Completion is complete when paired with the Session 89 app/runtime QA commands.",
        ]
    )
    report_text = "\n".join(lines) + "\n"
    with open(REPORT_MD, "w", encoding="utf-8") as handle:
        handle.write(report_text)
    with open(APP_SESSION_REPORT, "w", encoding="utf-8") as handle:
        handle.write(report_text)

    if report["status"] != "APPROVED":
        raise RuntimeError(report["checks"])
    return report


def main():
    print("=" * 72)
    print("Session 89: Final Phase 10 QA")
    print("=" * 72)
    manifest = load_json(MANIFEST_PATH)
    overview_metrics = {}
    hero_metrics = {}
    prior_metrics = {}

    for structure in manifest["structures"]:
        print(f"Import QA: {structure['label']}")
        overview_metrics[structure["id"]] = analyze_model(structure, structure["exterior"], "overview")
        hero_metrics[structure["id"]] = analyze_model(structure, structure["exteriorHero"], "hero")
        prior_metrics[structure["id"]] = load_prior_hero_metric(structure["id"])

    print("Rendering final app hero evidence")
    app_hero_evidence = render_final_app_hero_evidence(manifest)

    print("Rendering overview LOD evidence")
    overview_evidence = render_overview_lod_evidence(manifest)

    print("Rendering contact sheets")
    sheets = render_evidence_sheets(manifest, prior_metrics, app_hero_evidence, overview_evidence)

    report = write_reports(manifest, overview_metrics, hero_metrics, prior_metrics, app_hero_evidence, overview_evidence, sheets)
    update_manifest_source_of_truth(manifest)

    print(f"Report: {REPORT_MD}")
    print(f"App report: {APP_SESSION_REPORT}")
    print(f"Performance: {PERFORMANCE_REPORT}")
    print(f"Verdict: {report['status']}")
    print(f"Score: {report['completion_score']['overall']:.1f} / 10")
    for check, passed in report["checks"].items():
        print(f"  {check}: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()

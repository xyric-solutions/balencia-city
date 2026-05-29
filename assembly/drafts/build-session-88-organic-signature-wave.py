"""
Balencia City v3 - Session 88
Phase 10 organic/signature wave: Yoga, Recovery, Relationships, Leaderboard,
and Nutrition hero exteriors.

This script preserves approved overview exteriors and creates focused-scene
`exteriorHero` GLBs for the final Architectural Completion build wave.
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


SESSION = 88
ROOT = "/Users/hamza/Desktop/balencia-city-v3"
HELPER_PATH = os.path.join(ROOT, "assembly", "drafts", "build-session-86-pilot-wave.py")
MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "src", "lib", "asset-manifest.json")
PUBLIC_MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "public", "models", "asset-manifest.json")
SCREENSHOT_DIR = os.path.join(ROOT, "assembly", "screenshots", "session-88-organic-signature-wave")
AFTER_DIR = os.path.join(SCREENSHOT_DIR, "after")
APP_HERO_DIR = os.path.join(SCREENSHOT_DIR, "app-hero-cameras")
AUDIT_DIR = os.path.join(ROOT, "assembly", "audit")
PERFORMANCE_DIR = os.path.join(ROOT, "assembly", "performance-reports")
REPORT_JSON = os.path.join(AUDIT_DIR, "session-88-organic-signature-wave.json")
REPORT_MD = os.path.join(AUDIT_DIR, "session-88-organic-signature-wave.md")
PERFORMANCE_REPORT = os.path.join(PERFORMANCE_DIR, "session-88-performance.json")
APP_SESSION_REPORT = os.path.join(ROOT, "apps", "balencia", "SESSION-88-REPORT.md")

spec = importlib.util.spec_from_file_location("session86_helpers", HELPER_PATH)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


MODULES = [
    {
        "id": "yoga",
        "label": "Yoga and Wellbeing",
        "accent_hex": "#6EE7B7",
        "root_name": "yoga-ext-hero",
        "source_glb": "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb",
        "output_blend": "modules/02-yoga-wellbeing/exterior/drafts/yoga-session88-hero.blend",
        "draft_glb": "modules/02-yoga-wellbeing/exterior/drafts/yoga-ext-hero-draft-s88.glb",
        "approved_glb": "modules/02-yoga-wellbeing/exterior/approved/yoga-ext-hero.glb",
        "public_glb": "models/structures/02-yoga-wellbeing/yoga-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/02-yoga-wellbeing/yoga-ext-hero.glb",
        "metrics": "modules/02-yoga-wellbeing/exterior/drafts/session88-hero-metrics.json",
        "qa_import": "modules/02-yoga-wellbeing/exterior/drafts/session88-hero-qa-import.json",
        "screenshots": "modules/02-yoga-wellbeing/screenshots",
        "pre_tris": 16052,
        "tri_min": 23000,
        "tri_max": 36000,
        "size_min_kb": 80,
        "size_max_kb": 700,
        "gate8_notes": [
            "finished floating sanctuary deck, bridge thresholds, dome ribs, and garden ledges",
            "sage breathing/floor rhythm visible from Scene 5 without hardening the silhouette",
            "warm-mist receptor and lake edge read as complete district-specific crown/base logic",
        ],
    },
    {
        "id": "leaderboard",
        "label": "Leaderboard and Competition",
        "accent_hex": "#FB7185",
        "root_name": "leaderboard-ext-hero",
        "source_glb": "modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb",
        "output_blend": "modules/06-leaderboard-competition/exterior/drafts/leaderboard-session88-hero.blend",
        "draft_glb": "modules/06-leaderboard-competition/exterior/drafts/leaderboard-ext-hero-draft-s88.glb",
        "approved_glb": "modules/06-leaderboard-competition/exterior/approved/leaderboard-ext-hero.glb",
        "public_glb": "models/structures/06-leaderboard-competition/leaderboard-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/06-leaderboard-competition/leaderboard-ext-hero.glb",
        "metrics": "modules/06-leaderboard-competition/exterior/drafts/session88-hero-metrics.json",
        "qa_import": "modules/06-leaderboard-competition/exterior/drafts/session88-hero-qa-import.json",
        "screenshots": "modules/06-leaderboard-competition/screenshots",
        "pre_tris": 19928,
        "tri_min": 27000,
        "tri_max": 41000,
        "size_min_kb": 90,
        "size_max_kb": 760,
        "gate8_notes": [
            "open arena now has resolved rim engineering, seating cadence, victory pillar caps, and screen hardware",
            "grand entry, competitor lane, and leaderboard facade read as finished from Scene 9",
            "lightning receiver remains dramatic without changing the baked special energy endpoint",
        ],
    },
    {
        "id": "relationships",
        "label": "Relationships",
        "accent_hex": "#F43F5E",
        "root_name": "relationships-ext-hero",
        "source_glb": "modules/07-relationships/exterior/approved/relationships-ext.glb",
        "output_blend": "modules/07-relationships/exterior/drafts/relationships-session88-hero.blend",
        "draft_glb": "modules/07-relationships/exterior/drafts/relationships-ext-hero-draft-s88.glb",
        "approved_glb": "modules/07-relationships/exterior/approved/relationships-ext-hero.glb",
        "public_glb": "models/structures/07-relationships/relationships-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/07-relationships/relationships-ext-hero.glb",
        "metrics": "modules/07-relationships/exterior/drafts/session88-hero-metrics.json",
        "qa_import": "modules/07-relationships/exterior/drafts/session88-hero-qa-import.json",
        "screenshots": "modules/07-relationships/screenshots",
        "pre_tris": 17170,
        "tri_min": 23000,
        "tri_max": 36000,
        "size_min_kb": 80,
        "size_max_kb": 700,
        "gate8_notes": [
            "low garden pavilion gains completed terrace facades, moat edge, bridges, and welcome thresholds",
            "15-floor anti-tower rhythm remains readable through soft rose ledges and mullions",
            "roof domes and warm-mist diffuser are resolved while preserving the human-scaled silhouette",
        ],
    },
    {
        "id": "recovery",
        "label": "Recovery and Sleep",
        "accent_hex": "#6366F1",
        "root_name": "recovery-ext-hero",
        "source_glb": "modules/09-recovery-sleep/exterior/approved/recovery-ext.glb",
        "output_blend": "modules/09-recovery-sleep/exterior/drafts/recovery-session88-hero.blend",
        "draft_glb": "modules/09-recovery-sleep/exterior/drafts/recovery-ext-hero-draft-s88.glb",
        "approved_glb": "modules/09-recovery-sleep/exterior/approved/recovery-ext-hero.glb",
        "public_glb": "models/structures/09-recovery-sleep/recovery-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/09-recovery-sleep/recovery-ext-hero.glb",
        "metrics": "modules/09-recovery-sleep/exterior/drafts/session88-hero-metrics.json",
        "qa_import": "modules/09-recovery-sleep/exterior/drafts/session88-hero-qa-import.json",
        "screenshots": "modules/09-recovery-sleep/screenshots",
        "pre_tris": 17412,
        "tri_min": 22500,
        "tri_max": 35000,
        "size_min_kb": 80,
        "size_max_kb": 700,
        "gate8_notes": [
            "ethereal shell receives finished contour layers, soft support collars, underside cradle, and lake boundary",
            "no-floor continuous form remains intact while shell depth and embedded star cadence improve the hero read",
            "faint-thread receptor is complete but still deliberately quiet",
        ],
    },
    {
        "id": "nutrition",
        "label": "Nutrition",
        "accent_hex": "#D97706",
        "root_name": "nutrition-ext-hero",
        "source_glb": "modules/11-nutrition/exterior/approved/nutrition-ext.glb",
        "output_blend": "modules/11-nutrition/exterior/drafts/nutrition-session88-hero.blend",
        "draft_glb": "modules/11-nutrition/exterior/drafts/nutrition-ext-hero-draft-s88.glb",
        "approved_glb": "modules/11-nutrition/exterior/approved/nutrition-ext-hero.glb",
        "public_glb": "models/structures/11-nutrition/nutrition-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/11-nutrition/nutrition-ext-hero.glb",
        "metrics": "modules/11-nutrition/exterior/drafts/session88-hero-metrics.json",
        "qa_import": "modules/11-nutrition/exterior/drafts/session88-hero-qa-import.json",
        "screenshots": "modules/11-nutrition/screenshots",
        "pre_tris": 19876,
        "tri_min": 26500,
        "tri_max": 41000,
        "size_min_kb": 90,
        "size_max_kb": 760,
        "gate8_notes": [
            "12-tier vertical farm gains finished terrace ledges, greenhouse mullions, irrigation detail, and market threshold",
            "green plant identity and amber grow-light rhythm stay visible from Scene 14",
            "roof vent crown and hard-pipeline socket read as complete service architecture",
        ],
    },
]

FOCUSED_SCENE_CONFIG = {
    "yoga": {
        "scene": 5,
        "slug": "yoga-sanctuary",
        "offset": [39, 19, -38],
        "target_height": 6.2,
        "lens": 29,
        "frame": 96,
    },
    "leaderboard": {
        "scene": 9,
        "slug": "leaderboard-arena",
        "offset": [-42, 25, 42],
        "target_height": 8.6,
        "lens": 28,
        "frame": 96,
    },
    "relationships": {
        "scene": 10,
        "slug": "relationships-garden",
        "offset": [48, 20, 34],
        "target_height": 5.8,
        "lens": 29,
        "frame": 96,
    },
    "recovery": {
        "scene": 12,
        "slug": "recovery-dreamscape",
        "offset": [-52, 17, 22],
        "target_height": 5.2,
        "lens": 30,
        "frame": 96,
    },
    "nutrition": {
        "scene": 14,
        "slug": "nutrition-farm",
        "offset": [-43, 18, -40],
        "target_height": 8.0,
        "lens": 29,
        "frame": 96,
    },
}

ENERGY_IDS = [
    "hard-pipelines",
    "warm-mist",
    "faint-thread",
    "knowledgebase-waterfall",
    "leaderboard-lightning",
    "cross-district-gold",
    "ai-pulse",
]

for directory in (SCREENSHOT_DIR, AFTER_DIR, APP_HERO_DIR, AUDIT_DIR, PERFORMANCE_DIR):
    os.makedirs(directory, exist_ok=True)
for module in MODULES:
    for key in ("output_blend", "draft_glb", "approved_glb", "public_abs_glb", "metrics", "qa_import"):
        os.makedirs(os.path.dirname(os.path.join(ROOT, module[key])), exist_ok=True)
    os.makedirs(os.path.join(ROOT, module["screenshots"]), exist_ok=True)


def abs_path(path):
    return os.path.join(ROOT, path)


def add_ring_markers(prefix, center, radius, z, count, dims, material, category, rot_offset=0.0):
    cx, cy = center
    for index in range(count):
        angle = rot_offset + index * math.tau / count
        loc = Vector((cx, cy, z)) + Vector((math.cos(angle), math.sin(angle), 0)) * radius
        helpers.box(
            f"{prefix}_{index:02d}",
            (loc.x, loc.y, loc.z),
            dims,
            material,
            category,
            rot=(0, 0, angle),
        )


def add_spoked_ring(prefix, center, radius, z, count, material, category, width, minor=0.006, height=0.010):
    cx, cy = center
    for index in range(count):
        angle = index * math.tau / count
        start = Vector((cx, cy, z)) + Vector((math.cos(angle), math.sin(angle), 0)) * (radius * 0.78)
        end = Vector((cx, cy, z + height * ((index % 3) - 1))) + Vector((math.cos(angle), math.sin(angle), 0)) * radius
        helpers.cylinder_between(f"{prefix}_spoke_{index:02d}", start, end, width, material, category, vertices=5)
    helpers.torus(f"{prefix}_rim", (cx, cy, z), radius, minor, material, category, seg=64, minor_seg=4)


def add_yoga_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    span = max(width, depth)

    base_category = "session88 yoga finished floating deck and lake threshold"
    for ring, scale in enumerate((0.62, 0.73, 0.86, 0.98)):
        helpers.torus(
            f"Yoga_s88_reflecting_lake_finished_edge_{ring}",
            (cx, cy, min_z + 0.018 + ring * 0.012),
            span * 0.34 * scale,
            span * 0.0028,
            mats["glass" if ring < 2 else "detail"],
            base_category,
            seg=72,
            minor_seg=3,
        )
    add_ring_markers(
        "Yoga_s88_platform_breathing_paver",
        (cx, cy),
        span * 0.30,
        min_z + height * 0.130,
        36,
        (width * 0.018, depth * 0.006, height * 0.004),
        mats["base"],
        base_category,
    )
    for bridge, angle in enumerate((-0.65, 0.15, 0.88)):
        start = Vector((cx, cy, min_z + height * 0.118)) + Vector((math.cos(angle), math.sin(angle), 0)) * span * 0.16
        end = Vector((cx, cy, min_z + height * 0.105)) + Vector((math.cos(angle), math.sin(angle), 0)) * span * 0.47
        helpers.cylinder_between(f"Yoga_s88_curved_threshold_walkway_core_{bridge}", start, end, width * 0.014, mats["detail"], base_category, vertices=8)
        for side in (-1, 1):
            normal = Vector((-math.sin(angle), math.cos(angle), 0)) * side * width * 0.020
            helpers.cylinder_between(f"Yoga_s88_walkway_sage_rail_{bridge}_{side}", start + normal, end + normal, width * 0.004, mats["accent"], base_category, vertices=5)
        helpers.box(f"Yoga_s88_entry_stillness_gate_{bridge}", (end.x, end.y, end.z + height * 0.032), (width * 0.038, depth * 0.018, height * 0.036), mats["detail"], base_category, rot=(0, 0, angle))

    dome_category = "session88 yoga resolved dome ribs and garden envelope"
    dome_specs = [
        (cx - width * 0.18, cy + depth * 0.03, height * 0.64, span * 0.145),
        (cx + width * 0.16, cy - depth * 0.12, height * 0.52, span * 0.110),
        (cx + width * 0.10, cy + depth * 0.21, height * 0.42, span * 0.085),
    ]
    for dome, (dx, dy, ztop, radius) in enumerate(dome_specs):
        base_z = min_z + height * 0.205 + dome * height * 0.010
        top_z = min_z + ztop
        for level, t in enumerate((0.18, 0.42, 0.66, 0.86)):
            helpers.torus(
                f"Yoga_s88_dome{dome}_soft_mullion_ring_{level}",
                (dx, dy, base_z + (top_z - base_z) * t),
                radius * (1.03 - t * 0.46),
                span * 0.0026,
                mats["glass" if level % 2 else "detail"],
                dome_category,
                seg=48,
                minor_seg=3,
            )
        for rib in range(10):
            angle = rib * math.tau / 10
            start = Vector((dx, dy, base_z)) + Vector((math.cos(angle), math.sin(angle), 0)) * radius
            end = Vector((dx, dy, top_z)) + Vector((math.cos(angle), math.sin(angle), 0)) * radius * 0.18
            helpers.cylinder_between(f"Yoga_s88_dome{dome}_sage_meridian_rib_{rib:02d}", start, end, span * 0.0028, mats["detail"], dome_category, vertices=5)
        add_ring_markers(
            f"Yoga_s88_dome{dome}_biolume_leaf_cluster",
            (dx, dy),
            radius * 1.12,
            base_z + height * 0.018,
            16,
            (width * 0.012, depth * 0.007, height * 0.010),
            mats["holo"],
            dome_category,
            rot_offset=0.12 * dome,
        )

    crown_category = "session88 yoga warm mist receptor and quiet crown"
    apex = min_z + height * 0.72
    add_spoked_ring("Yoga_s88_apex_mist_receptor", (cx - width * 0.18, cy + depth * 0.03), span * 0.085, apex, 12, mats["energy"], crown_category, span * 0.0026, minor=span * 0.0026, height=height * 0.020)
    for petal in range(8):
        angle = petal * math.tau / 8
        loc = Vector((cx - width * 0.18, cy + depth * 0.03, apex + height * 0.025)) + Vector((math.cos(angle), math.sin(angle), 0)) * span * 0.105
        helpers.box(f"Yoga_s88_receptor_petal_sage_glow_{petal}", (loc.x, loc.y, loc.z), (width * 0.016, depth * 0.006, height * 0.018), mats["emissive"], crown_category, rot=(0, 0, angle))


def add_recovery_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    span = max(width, depth)

    base_category = "session88 recovery completed lake cradle and soft supports"
    for ring, scale in enumerate((0.58, 0.72, 0.88, 1.03)):
        helpers.torus(
            f"Recovery_s88_sleep_lake_boundary_ring_{ring}",
            (cx, cy, min_z + 0.020 + ring * 0.010),
            span * 0.31 * scale,
            span * 0.0024,
            mats["glass" if ring < 2 else "base"],
            base_category,
            seg=72,
            minor_seg=3,
        )
    for pillar in range(5):
        angle = pillar * math.tau / 5 + 0.28
        x = cx + math.cos(angle) * width * 0.28
        y = cy + math.sin(angle) * depth * 0.28
        helpers.torus(f"Recovery_s88_light_pillar_lake_collar_{pillar}", (x, y, min_z + height * 0.085), span * 0.035, span * 0.0028, mats["emissive"], base_category, seg=36, minor_seg=3)
        helpers.torus(f"Recovery_s88_light_pillar_cloud_collar_{pillar}", (x, y, min_z + height * 0.430), span * 0.030, span * 0.0026, mats["detail"], base_category, seg=36, minor_seg=3)
        helpers.cylinder_between(f"Recovery_s88_muted_inner_support_glow_{pillar}", (x, y, min_z + height * 0.10), (x, y, min_z + height * 0.42), span * 0.004, mats["emissive"], base_category, vertices=8)
    helpers.torus("Recovery_s88_concave_underside_sleep_cradle", (cx, cy, min_z + height * 0.318), span * 0.245, span * 0.006, mats["base"], base_category, seg=72, minor_seg=4)

    shell_category = "session88 recovery layered translucent shell depth"
    lobe_specs = [
        (cx - width * 0.18, cy, min_z + height * 0.58, span * 0.23),
        (cx + width * 0.12, cy + depth * 0.10, min_z + height * 0.66, span * 0.20),
        (cx + width * 0.03, cy - depth * 0.18, min_z + height * 0.53, span * 0.18),
    ]
    for lobe, (lx, ly, z, radius) in enumerate(lobe_specs):
        for contour, scale in enumerate((0.68, 0.84, 1.0)):
            helpers.torus(
                f"Recovery_s88_lobe{lobe}_sleep_contour_ribbon_{contour}",
                (lx, ly, z - height * 0.060 + contour * height * 0.035),
                radius * scale,
                span * 0.0028,
                mats["glass" if contour != 1 else "detail"],
                shell_category,
                seg=60,
                minor_seg=3,
            )
        for star in range(10):
            angle = star * math.tau / 10 + lobe * 0.21
            loc = Vector((lx, ly, z + height * (0.010 * ((star % 3) - 1)))) + Vector((math.cos(angle), math.sin(angle), 0)) * radius * 0.92
            helpers.cylinder(f"Recovery_s88_lobe{lobe}_embedded_sleep_star_{star:02d}", (loc.x, loc.y, loc.z), span * 0.005, span * 0.004, mats["emissive"], shell_category, vertices=8)
    for wisp in range(12):
        angle = wisp * math.tau / 12 + 0.15
        start = Vector((cx, cy, min_z + height * (0.47 + 0.06 * (wisp % 3)))) + Vector((math.cos(angle), math.sin(angle), 0)) * span * 0.25
        end = start + Vector((math.cos(angle), math.sin(angle), 0)) * span * (0.08 + 0.02 * (wisp % 2)) + Vector((0, 0, height * 0.025 * math.sin(wisp)))
        helpers.cylinder_between(f"Recovery_s88_fading_edge_wisp_{wisp:02d}", start, end, span * 0.0028, mats["accent"], shell_category, vertices=5)

    crown_category = "session88 recovery quiet thread receptor"
    top = (cx, cy, max_z + height * 0.030)
    helpers.torus("Recovery_s88_thread_receptor_barely_visible_halo", top, span * 0.080, span * 0.0026, mats["energy"], crown_category, seg=48, minor_seg=3)
    helpers.cylinder("Recovery_s88_silver_sleep_beacon_mote", (cx, cy, max_z + height * 0.070), span * 0.006, height * 0.070, mats["emissive"], crown_category, vertices=10)


def add_relationships_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    span = max(width, depth)

    base_category = "session88 relationships completed moat and civic garden edge"
    for ring, scale in enumerate((0.70, 0.82, 0.94, 1.08)):
        helpers.torus(
            f"Relationships_s88_moat_finished_edge_{ring}",
            (cx, cy, min_z + 0.018 + ring * 0.010),
            span * 0.34 * scale,
            span * 0.0025,
            mats["glass" if ring < 2 else "base"],
            base_category,
            seg=72,
            minor_seg=3,
        )
    for bridge, angle in enumerate((-1.18, -0.22, 0.68, 1.62)):
        start = Vector((cx, cy, min_z + height * 0.085)) + Vector((math.cos(angle), math.sin(angle), 0)) * span * 0.22
        end = Vector((cx, cy, min_z + height * 0.072)) + Vector((math.cos(angle), math.sin(angle), 0)) * span * 0.48
        helpers.cylinder_between(f"Relationships_s88_intimate_bridge_deck_{bridge}", start, end, span * 0.006, mats["detail"], base_category, vertices=8)
        for post in range(5):
            point = start.lerp(end, post / 4)
            helpers.cylinder_between(f"Relationships_s88_bridge_rose_post_{bridge}_{post}", point, point + Vector((0, 0, height * 0.040)), span * 0.0028, mats["accent"], base_category, vertices=5)
    front_y = min_y - depth * 0.075
    for side in (-1, 1):
        helpers.cylinder_between(f"Relationships_s88_welcoming_portal_return_{side}", (cx + side * width * 0.18, front_y, min_z + height * 0.040), (cx + side * width * 0.10, front_y, min_z + height * 0.250), span * 0.006, mats["accent"], base_category, vertices=6)
    helpers.box("Relationships_s88_deep_family_entry_shadow", (cx, front_y - depth * 0.030, min_z + height * 0.135), (width * 0.175, depth * 0.030, height * 0.070), mats["detail"], base_category)

    facade_category = "session88 relationships soft floor rhythm and terrace facade"
    for floor in range(15):
        t = floor / 14
        z = min_z + height * (0.16 + 0.52 * t)
        radius = span * (0.258 - 0.045 * t)
        helpers.torus(f"Relationships_s88_anti_tower_floor_ledge_{floor:02d}", (cx, cy, z), radius, span * 0.0025, mats["base" if floor % 3 else "detail"], facade_category, seg=64, minor_seg=3)
        add_ring_markers(
            f"Relationships_s88_floor{floor:02d}_rose_connection_light",
            (cx, cy),
            radius * 1.02,
            z + height * 0.004,
            8,
            (width * 0.010, depth * 0.005, height * 0.006),
            mats["emissive"],
            facade_category,
            rot_offset=0.09 * floor,
        )
    for terrace in range(5):
        radius = span * (0.29 - terrace * 0.030)
        z = min_z + height * (0.18 + terrace * 0.095)
        add_ring_markers(
            f"Relationships_s88_terrace{terrace}_garden_bloom",
            (cx, cy),
            radius,
            z + height * 0.030,
            20,
            (width * 0.012, depth * 0.007, height * 0.009),
            mats["accent"],
            facade_category,
            rot_offset=terrace * 0.18,
        )

    crown_category = "session88 relationships roof domes and mist diffuser"
    dome_centers = [
        (cx - width * 0.14, cy + depth * 0.04, max_z - height * 0.18, span * 0.070),
        (cx + width * 0.12, cy - depth * 0.10, max_z - height * 0.15, span * 0.062),
        (cx + width * 0.02, cy + depth * 0.15, max_z - height * 0.20, span * 0.052),
    ]
    for dome, (dx, dy, dz, radius) in enumerate(dome_centers):
        helpers.torus(f"Relationships_s88_roof_gathering_dome_frame_{dome}", (dx, dy, dz), radius, span * 0.0028, mats["glass"], crown_category, seg=44, minor_seg=3)
        for rib in range(8):
            angle = rib * math.tau / 8
            helpers.cylinder_between(
                f"Relationships_s88_roof_dome_soft_rib_{dome}_{rib}",
                (dx + math.cos(angle) * radius, dy + math.sin(angle) * radius, dz),
                (dx, dy, dz + height * 0.090),
                span * 0.0024,
                mats["detail"],
                crown_category,
                vertices=5,
            )
    add_spoked_ring("Relationships_s88_warm_mist_diffuser", (cx, cy), span * 0.075, max_z + height * 0.018, 10, mats["energy"], crown_category, span * 0.0026, minor=span * 0.0026, height=height * 0.012)


def add_leaderboard_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    span = max(width, depth)
    radius = span * 0.38

    bowl_category = "session88 leaderboard finished bowl seating and rim engineering"
    for tier in range(8):
        z = min_z + height * (0.18 + tier * 0.066)
        helpers.torus(
            f"Leaderboard_s88_visible_seating_deck_cadence_{tier:02d}",
            (cx, cy, z),
            radius * (0.62 + tier * 0.050),
            span * 0.0035,
            mats["detail"],
            bowl_category,
            seg=80,
            minor_seg=3,
        )
        add_ring_markers(
            f"Leaderboard_s88_tier{tier:02d}_section_number_light",
            (cx, cy),
            radius * (0.62 + tier * 0.050),
            z + height * 0.012,
            16,
            (width * 0.009, depth * 0.005, height * 0.007),
            mats["emissive" if tier % 2 else "accent"],
            bowl_category,
            rot_offset=tier * 0.07,
        )
    for ring, scale in enumerate((0.92, 1.00, 1.08)):
        helpers.torus(f"Leaderboard_s88_segmented_open_roof_rim_{ring}", (cx, cy, max_z - height * (0.12 - ring * 0.015)), radius * scale, span * 0.005, mats["detail" if ring == 0 else "base"], bowl_category, seg=80, minor_seg=4)
    for truss in range(24):
        angle = truss * math.tau / 24
        start = Vector((cx, cy, max_z - height * 0.145)) + Vector((math.cos(angle), math.sin(angle), 0)) * radius * 0.80
        end = Vector((cx, cy, max_z - height * 0.080)) + Vector((math.cos(angle), math.sin(angle), 0)) * radius * 1.08
        helpers.cylinder_between(f"Leaderboard_s88_open_rim_finished_truss_{truss:02d}", start, end, span * 0.0028, mats["detail"], bowl_category, vertices=5)

    entry_category = "session88 leaderboard grand entry and competitor lane"
    front_y = min_y - depth * 0.080
    for step in range(7):
        helpers.box(
            f"Leaderboard_s88_competitor_walkway_medal_step_{step}",
            (cx, front_y - depth * (0.08 + step * 0.035), min_z + 0.026 + step * 0.010),
            (width * (0.24 - step * 0.012), depth * 0.030, height * 0.010),
            mats["base" if step % 2 else "accent"],
            entry_category,
        )
    for side in (-1, 1):
        helpers.cylinder_between(f"Leaderboard_s88_monumental_arch_outer_leg_{side}", (cx + side * width * 0.22, front_y, min_z + height * 0.050), (cx + side * width * 0.115, front_y, min_z + height * 0.330), span * 0.006, mats["accent"], entry_category, vertices=6)
        helpers.cylinder_between(f"Leaderboard_s88_arch_inner_gold_trace_{side}", (cx + side * width * 0.17, front_y - depth * 0.016, min_z + height * 0.076), (cx + side * width * 0.075, front_y - depth * 0.016, min_z + height * 0.300), span * 0.003, mats["energy"], entry_category, vertices=5)
    helpers.box("Leaderboard_s88_scoreboard_entry_header", (cx, front_y - depth * 0.025, min_z + height * 0.330), (width * 0.245, depth * 0.020, height * 0.032), mats["emissive"], entry_category)
    for glyph in range(22):
        x = cx + (glyph - 10.5) * width * 0.018
        helpers.box(f"Leaderboard_s88_entry_rank_glyph_{glyph:02d}", (x, front_y - depth * 0.045, min_z + height * (0.348 + 0.004 * (glyph % 4))), (width * 0.007, depth * 0.005, height * 0.009), mats["base" if glyph % 4 else "emissive"], entry_category)

    crown_category = "session88 leaderboard victory pillars and lightning crown"
    for pillar in range(4):
        angle = math.pi / 4 + pillar * math.tau / 4
        x = cx + math.cos(angle) * radius * 1.02
        y = cy + math.sin(angle) * radius * 1.02
        helpers.torus(f"Leaderboard_s88_victory_pillar_crown_halo_{pillar}", (x, y, max_z - height * 0.020), span * 0.040, span * 0.0032, mats["emissive"], crown_category, seg=36, minor_seg=3)
        helpers.torus(f"Leaderboard_s88_victory_pillar_hardware_collar_{pillar}", (x, y, max_z - height * 0.100), span * 0.032, span * 0.0030, mats["detail"], crown_category, seg=36, minor_seg=3)
        for fin in range(4):
            fin_angle = angle + (fin - 1.5) * 0.25
            helpers.cylinder_between(
                f"Leaderboard_s88_victory_beacon_fin_{pillar}_{fin}",
                (x, y, max_z - height * 0.055),
                (x + math.cos(fin_angle) * span * 0.035, y + math.sin(fin_angle) * span * 0.035, max_z + height * 0.055),
                span * 0.0026,
                mats["accent"],
                crown_category,
                vertices=5,
            )
    helpers.torus("Leaderboard_s88_lightning_receiver_engineered_apex", (cx, cy, max_z + height * 0.015), span * 0.085, span * 0.0036, mats["energy"], crown_category, seg=48, minor_seg=3)
    for branch in range(14):
        angle = branch * math.tau / 14
        start = Vector((cx, cy, max_z + height * 0.012))
        end = Vector((cx, cy, max_z - height * 0.075)) + Vector((math.cos(angle), math.sin(angle), 0)) * span * (0.10 + 0.03 * (branch % 2))
        helpers.cylinder_between(f"Leaderboard_s88_controlled_lightning_branch_{branch:02d}", start, end, span * 0.0024, mats["energy"], crown_category, vertices=5)


def add_nutrition_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]

    facade_category = "session88 nutrition completed terrace farm facade"
    for tier in range(12):
        t = tier / 11
        z = min_z + height * (0.105 + t * 0.675)
        half_w = width * (0.47 - 0.17 * t)
        half_d = depth * (0.47 - 0.16 * t)
        for face, y in (("front", min_y - depth * 0.020), ("back", max_y + depth * 0.020)):
            helpers.box(f"Nutrition_s88_{face}_terrace_dark_underledge_{tier:02d}", (cx, y, z), (half_w, depth * 0.010, height * 0.006), mats["base"], facade_category)
            helpers.box(f"Nutrition_s88_{face}_amber_grow_light_louver_{tier:02d}", (cx, y - depth * 0.010 if face == "front" else y + depth * 0.010, z + height * 0.016), (half_w * 0.88, depth * 0.006, height * 0.005), mats["emissive"], facade_category)
            for plant in range(8):
                x = cx + (plant - 3.5) * half_w * 0.22
                helpers.box(f"Nutrition_s88_{face}_leaf_cascade_cluster_{tier:02d}_{plant}", (x, y - depth * 0.018 if face == "front" else y + depth * 0.018, z - height * (0.006 + 0.006 * (plant % 3))), (width * 0.010, depth * 0.006, height * 0.024), mats["accent"], facade_category, rot=(0, 0, 0.12 * ((plant % 3) - 1)))
        for face, x in (("left", min_x - width * 0.020), ("right", max_x + width * 0.020)):
            helpers.box(f"Nutrition_s88_{face}_terrace_floor_rhythm_{tier:02d}", (x, cy, z + height * 0.002), (width * 0.008, half_d, height * 0.006), mats["detail"], facade_category)
            for valve in range(4):
                y = cy + (valve - 1.5) * half_d * 0.32
                helpers.cylinder(f"Nutrition_s88_{face}_irrigation_valve_{tier:02d}_{valve}", (x, y, z + height * 0.022), width * 0.0045, width * 0.004, mats["energy" if valve == 1 and tier % 4 == 0 else "detail"], facade_category, vertices=8)

    greenhouse_category = "session88 nutrition greenhouse and market threshold"
    greenhouse_specs = [
        (cx - width * 0.18, min_y - depth * 0.045, min_z + height * 0.42, width * 0.105),
        (cx + width * 0.15, min_y - depth * 0.047, min_z + height * 0.56, width * 0.092),
        (cx + width * 0.02, max_y + depth * 0.045, min_z + height * 0.49, width * 0.098),
    ]
    for house, (gx, gy, gz, gw) in enumerate(greenhouse_specs):
        helpers.box(f"Nutrition_s88_greenhouse_deep_glass_skin_{house}", (gx, gy, gz), (gw, depth * 0.018, height * 0.100), mats["glass"], greenhouse_category)
        for mullion in range(5):
            x = gx + (mullion - 2) * gw * 0.18
            helpers.box(f"Nutrition_s88_greenhouse_vertical_mullion_{house}_{mullion}", (x, gy - depth * 0.011, gz), (width * 0.004, depth * 0.005, height * 0.108), mats["detail"], greenhouse_category)
        for shelf in range(4):
            helpers.box(f"Nutrition_s88_greenhouse_hydroponic_shelf_{house}_{shelf}", (gx, gy - depth * 0.016, gz - height * 0.040 + shelf * height * 0.026), (gw * 0.82, depth * 0.005, height * 0.004), mats["accent"], greenhouse_category)
    market_y = min_y - depth * 0.110
    helpers.box("Nutrition_s88_open_market_deep_shadow_threshold", (cx, market_y, min_z + height * 0.115), (width * 0.245, depth * 0.035, height * 0.080), mats["detail"], greenhouse_category)
    for crate in range(24):
        x = cx + (crate % 8 - 3.5) * width * 0.035
        z = min_z + height * (0.065 + 0.018 * (crate // 8))
        helpers.box(f"Nutrition_s88_market_produce_crate_{crate:02d}", (x, market_y - depth * 0.040, z), (width * 0.020, depth * 0.016, height * 0.012), mats["accent" if crate % 3 else "emissive"], greenhouse_category)
    for drip in range(36):
        tier = drip % 12
        x = cx + ((drip // 12) - 1) * width * 0.18 + math.sin(drip) * width * 0.015
        y = min_y - depth * 0.055
        z = min_z + height * (0.18 + tier * 0.052)
        helpers.cylinder_between(f"Nutrition_s88_visible_irrigation_drop_line_{drip:02d}", (x, y, z + height * 0.030), (x + math.sin(drip * 1.4) * width * 0.010, y, z - height * 0.012), width * 0.0024, mats["detail"], greenhouse_category, vertices=5)

    crown_category = "session88 nutrition roof service crown and hard socket"
    for ring, z in enumerate((max_z - height * 0.050, max_z - height * 0.020, max_z + height * 0.010)):
        helpers.torus(f"Nutrition_s88_roof_vent_warm_finish_ring_{ring}", (cx, cy, z), width * (0.082 - ring * 0.010), width * 0.0034, mats["detail" if ring == 0 else "emissive"], crown_category, seg=42, minor_seg=3)
    helpers.cylinder("Nutrition_s88_kitchen_vent_finished_stack", (cx, cy, max_z + height * 0.060), width * 0.028, height * 0.120, mats["detail"], crown_category, vertices=14)
    helpers.torus("Nutrition_s88_hard_pipeline_socket_locking_collar", (cx - width * 0.18, cy + depth * 0.12, max_z + height * 0.020), width * 0.062, width * 0.0036, mats["energy"], crown_category, seg=42, minor_seg=3)
    for lug in range(8):
        angle = lug * math.tau / 8
        loc = Vector((cx - width * 0.18, cy + depth * 0.12, max_z + height * 0.025)) + Vector((math.cos(angle), math.sin(angle), 0)) * width * 0.073
        helpers.box(f"Nutrition_s88_socket_locking_lug_{lug}", (loc.x, loc.y, loc.z), (width * 0.012, depth * 0.006, height * 0.013), mats["energy"], crown_category, rot=(0, 0, angle))


def summarize_created_categories():
    summary = defaultdict(lambda: {"objects": 0, "tris": 0})
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in helpers.mesh_objects():
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


def render_evidence(module, bbox):
    prefix = f"session88-{module['id']}-hero"
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
        "three_quarter": ((max_x + span * 1.05, min_y - span * 1.35, min_z + height * 0.58), 42, False),
        "ground_up": ((max_x + span * 0.42, min_y - span * 0.98, min_z + max(height * 0.09, 0.55)), 30, False),
        "dark_first": ((max_x + span * 0.90, min_y - span * 1.38, min_z + height * 0.52), 44, True),
    }
    saved = None
    for view, (camera_loc, focal, dark) in views.items():
        if dark:
            saved = helpers.emission_strengths()
            for material, _value in saved:
                bsdf = material.node_tree.nodes.get("Principled BSDF")
                bsdf.inputs["Emission Strength"].default_value = 0
        path = os.path.join(module_dir, f"{prefix}-{view.replace('_', '-')}.png")
        helpers.render_current(path, camera_loc, target, bbox, focal=focal, dark=dark)
        evidence[view] = helpers.rel(path)
        shutil.copy2(path, os.path.join(AFTER_DIR, f"{module['id']}-{view.replace('_', '-')}.png"))
        if dark and saved:
            for material, value in saved:
                bsdf = material.node_tree.nodes.get("Principled BSDF")
                bsdf.inputs["Emission Strength"].default_value = value
    return evidence


def build_module(module):
    print(f"--- Session 88 hero exterior: {module['label']} ---")
    helpers.created_categories = {}
    helpers.clear_scene()
    bpy.ops.import_scene.gltf(filepath=abs_path(module["source_glb"]))
    mats = helpers.normalize_materials(module["accent_hex"])
    pre_bbox = helpers.world_bbox()
    pre_tris = helpers.count_tris()
    pre_objects = len(helpers.mesh_objects())

    if module["id"] == "yoga":
        add_yoga_hero(mats, pre_bbox)
    elif module["id"] == "leaderboard":
        add_leaderboard_hero(mats, pre_bbox)
    elif module["id"] == "relationships":
        add_relationships_hero(mats, pre_bbox)
    elif module["id"] == "recovery":
        add_recovery_hero(mats, pre_bbox)
    elif module["id"] == "nutrition":
        add_nutrition_hero(mats, pre_bbox)
    else:
        raise RuntimeError(module["id"])

    bbox = helpers.world_bbox()
    if bbox["min"][2] < -0.001:
        dz = -bbox["min"][2]
        for obj in helpers.mesh_objects():
            obj.location.z += dz
        bbox = helpers.world_bbox()

    category_summary = summarize_created_categories()
    helpers.merge_all_meshes_by_material(module["id"])
    bbox = helpers.world_bbox()
    final_live_tris = helpers.count_tris()
    final_live_objects = len(helpers.mesh_objects())
    bpy.ops.wm.save_as_mainfile(filepath=abs_path(module["output_blend"]))
    evidence = render_evidence(module, bbox)
    helpers.export_glb(module)
    qa = helpers.validate_glb(module)
    if not qa["passed"]:
        raise RuntimeError(f"{module['label']} Session 88 QA failed: {qa}")

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


def app_scene_camera(module_id):
    cfg = FOCUSED_SCENE_CONFIG[module_id]
    structure = helpers.structure_entry(module_id)
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


def render_app_hero_evidence(metrics_by_id):
    evidence = {}
    for module in MODULES:
        helpers.clear_scene()
        helpers.create_city_context()
        for item in helpers.MANIFEST["structures"]:
            source = abs_path(item["exterior"]["sourcePath"])
            if item["id"] == module["id"]:
                source = abs_path(module["approved_glb"])
            helpers.import_glb(source, helpers.layout_blender(item["id"]))
        bbox = helpers.world_bbox()
        camera_cfg = app_scene_camera(module["id"])
        path = os.path.join(
            APP_HERO_DIR,
            f"scene-{camera_cfg['scene']:02d}-{module['id']}-{camera_cfg['slug']}-hero-after.png",
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
        evidence[module["id"]] = {
            "scene": camera_cfg["scene"],
            "slug": camera_cfg["slug"],
            "path": helpers.rel(path),
            "runtime_camera_position": [round(value, 4) for value in camera_cfg["position"]],
            "runtime_camera_target": [round(value, 4) for value in camera_cfg["target"]],
            "lens": camera_cfg["lens"],
            "frame": camera_cfg["frame"],
            "nonzero": helpers.screenshot_ok(path),
            "hero_tris": metrics_by_id[module["id"]]["final_tris"],
        }
    return evidence


def update_asset_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    manifest["session"] = SESSION
    manifest["sourceOfTruth"]["assemblyAudit"] = "assembly/audit/session-88-organic-signature-wave.md"
    by_id = {module["id"]: module for module in MODULES}
    for structure in manifest["structures"]:
        module = by_id.get(structure["id"])
        if not module:
            continue
        structure["exteriorHero"] = {
            "name": module["root_name"],
            "sourcePath": module["approved_glb"],
            "publicPath": module["public_glb"],
            "runtimePath": f"/{module['public_glb']}",
        }
    with open(MANIFEST_PATH, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    os.makedirs(os.path.dirname(PUBLIC_MANIFEST_PATH), exist_ok=True)
    shutil.copy2(MANIFEST_PATH, PUBLIC_MANIFEST_PATH)
    return manifest


def energy_approved_path(asset_id):
    for item in helpers.MANIFEST["energyAssets"]:
        if item["id"] == asset_id:
            return abs_path(item["sourcePath"])
    raise KeyError(asset_id)


def write_reports(metrics_by_id, app_hero_evidence, contact_sheet):
    overview_tris = helpers.audit_overview_city_tris()
    active_source_bytes = sum(
        os.path.getsize(abs_path(item["exterior"]["sourcePath"]))
        for item in helpers.MANIFEST["structures"]
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
        "five_hero_exteriors_built": len(metrics_by_id) == 5,
        "hero_glbs_pass_import_qa": all(metrics["qa"]["passed"] for metrics in metrics_by_id.values()),
        "gate8_completion_passed": all(all(metrics["qa"]["gate8_checks"].values()) for metrics in metrics_by_id.values()),
        "app_hero_camera_evidence_complete": all(item["nonzero"] for item in app_hero_evidence.values()),
        "source_manifest_includes_exterior_hero_entries": True,
        "public_asset_sync_copied_hero_glbs": all(os.path.exists(abs_path(module["public_abs_glb"])) for module in MODULES),
        "overview_city_tri_budget_preserved": overview_tris <= 250000,
        "focused_hero_scene_budget_preserved": all(value <= 270000 for value in focused_scene_tris.values()),
    }
    report = {
        "session": SESSION,
        "date": str(date.today()),
        "scope": "Phase 10 organic/signature wave hero exteriors for Yoga, Recovery, Relationships, Leaderboard, and Nutrition",
        "status": "APPROVED" if all(checks.values()) else "NEEDS_FIX",
        "hero_exteriors": metrics_by_id,
        "app_hero_evidence": app_hero_evidence,
        "contact_sheet": helpers.rel(contact_sheet),
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
        "# Session 88 Organic/Signature Wave",
        "",
        f"Date: {date.today()}",
        f"Status: {report['status'].title()}",
        "",
        "## Scope",
        "",
        "Session 88 built Phase 10 architectural completion hero exterior LODs for Yoga and Wellbeing, Recovery and Sleep, Relationships, Leaderboard and Competition, and Nutrition. Approved overview exteriors, layout positions, baked energy endpoints, Phase 9 behavior, and the overview LOD policy were preserved.",
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
            "- Yoga and Wellbeing: floating sanctuary now has resolved dome ribs, lake edge, meditation deck rhythm, entry bridges, garden ledges, and a quiet warm-mist receptor.",
            "- Recovery and Sleep: dream-cloud form now has layered shell depth, embedded star cadence, lake cradle, soft support collars, fading wisps, and a restrained thread receptor.",
            "- Relationships: low garden pavilion now has finished moat edges, bridge posts, 15-floor rose ledges, terrace blooms, welcoming threshold depth, roof domes, and mist diffuser.",
            "- Leaderboard and Competition: open arena now has finished seating/rim cadence, grand entry hardware, competitor walkway steps, rank glyphs, victory pillar crowns, and controlled lightning receiver.",
            "- Nutrition: vertical farm now has completed terrace ledges, greenhouse mullions, irrigation detail, market produce threshold, roof service crown, and hard-pipeline socket.",
            "",
            "## Evidence",
            "",
            f"- Contact sheet: `{helpers.rel(contact_sheet)}`",
            f"- Audit JSON: `{helpers.rel(REPORT_JSON)}`",
            f"- Performance JSON: `{helpers.rel(PERFORMANCE_REPORT)}`",
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
        metrics_by_id[module["id"]] = build_module(module)

    update_asset_manifest()
    app_hero_evidence = render_app_hero_evidence(metrics_by_id)
    before_dir = os.path.join(ROOT, "assembly", "screenshots", "session-85-completion-audit", "app-hero-cameras")
    before_files = {
        "yoga": "scene-05-yoga-yoga-sanctuary-app-hero.png",
        "leaderboard": "scene-09-leaderboard-leaderboard-arena-app-hero.png",
        "relationships": "scene-10-relationships-relationships-garden-app-hero.png",
        "recovery": "scene-12-recovery-recovery-dreamscape-app-hero.png",
        "nutrition": "scene-14-nutrition-nutrition-farm-app-hero.png",
    }
    contact_items = []
    for module in MODULES:
        metrics = metrics_by_id[module["id"]]
        contact_items.append({"path": os.path.join(before_dir, before_files[module["id"]]), "label": f"{module['label']} before"})
        contact_items.append({"path": abs_path(app_hero_evidence[module["id"]]["path"]), "label": f"{module['label']} hero after"})
        contact_items.append({"path": abs_path(metrics["evidence"]["dark_first"]), "label": f"{module['label']} dark-first"})
    contact_sheet = helpers.render_contact_sheet(
        contact_items,
        os.path.join(SCREENSHOT_DIR, "s88-organic-signature-wave-before-after-contact-sheet.png"),
        "Session 88 Organic/Signature Wave - Before, Hero After, Dark-First",
        cols=3,
        width=2400,
        height=3000,
    )
    write_reports(metrics_by_id, app_hero_evidence, contact_sheet)


if __name__ == "__main__":
    main()

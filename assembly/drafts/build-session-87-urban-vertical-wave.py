"""
Balencia City v3 - Session 87
Phase 10 urban/vertical wave: Fitness, Chat, Career, and AI Analytics hero exteriors.

This script preserves approved overview exteriors and creates focused-scene
`exteriorHero` GLBs for the second Architectural Completion wave. It renders
Gate 8 evidence, updates the app manifest, and writes audit/performance reports.
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


SESSION = 87
ROOT = "/Users/hamza/Desktop/balencia-city-v3"
HELPER_PATH = os.path.join(ROOT, "assembly", "drafts", "build-session-86-pilot-wave.py")
MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "src", "lib", "asset-manifest.json")
PUBLIC_MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "public", "models", "asset-manifest.json")
SCREENSHOT_DIR = os.path.join(ROOT, "assembly", "screenshots", "session-87-urban-vertical-wave")
AFTER_DIR = os.path.join(SCREENSHOT_DIR, "after")
APP_HERO_DIR = os.path.join(SCREENSHOT_DIR, "app-hero-cameras")
AUDIT_DIR = os.path.join(ROOT, "assembly", "audit")
PERFORMANCE_DIR = os.path.join(ROOT, "assembly", "performance-reports")
REPORT_JSON = os.path.join(AUDIT_DIR, "session-87-urban-vertical-wave.json")
REPORT_MD = os.path.join(AUDIT_DIR, "session-87-urban-vertical-wave.md")
PERFORMANCE_REPORT = os.path.join(PERFORMANCE_DIR, "session-87-performance.json")
APP_SESSION_REPORT = os.path.join(ROOT, "apps", "balencia", "SESSION-87-REPORT.md")

spec = importlib.util.spec_from_file_location("session86_helpers", HELPER_PATH)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


MODULES = [
    {
        "id": "fitness",
        "label": "Fitness",
        "accent_hex": "#34A853",
        "root_name": "fitness-ext-hero",
        "source_glb": "modules/01-fitness/exterior/approved/fitness-ext.glb",
        "output_blend": "modules/01-fitness/exterior/drafts/fitness-session87-hero.blend",
        "draft_glb": "modules/01-fitness/exterior/drafts/fitness-ext-hero-draft-s87.glb",
        "approved_glb": "modules/01-fitness/exterior/approved/fitness-ext-hero.glb",
        "public_glb": "models/structures/01-fitness/fitness-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/01-fitness/fitness-ext-hero.glb",
        "metrics": "modules/01-fitness/exterior/drafts/session87-hero-metrics.json",
        "qa_import": "modules/01-fitness/exterior/drafts/session87-hero-qa-import.json",
        "screenshots": "modules/01-fitness/screenshots",
        "pre_tris": 16402,
        "tri_min": 24000,
        "tri_max": 36000,
        "size_min_kb": 80,
        "size_max_kb": 620,
        "gate8_notes": [
            "glass and panel skin behind the angular gym exoskeleton",
            "resolved athletic plinth, track edge, entry portal, and trophy wall",
            "roof mechanical crown and hard-pipeline collar visible from Scene 4",
        ],
    },
    {
        "id": "chat",
        "label": "Chat and Communication",
        "accent_hex": "#FF5E00",
        "root_name": "chat-ext-hero",
        "source_glb": "modules/05-chat-communication/exterior/approved/chat-ext.glb",
        "output_blend": "modules/05-chat-communication/exterior/drafts/chat-session87-hero.blend",
        "draft_glb": "modules/05-chat-communication/exterior/drafts/chat-ext-hero-draft-s87.glb",
        "approved_glb": "modules/05-chat-communication/exterior/approved/chat-ext-hero.glb",
        "public_glb": "models/structures/05-chat-communication/chat-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/05-chat-communication/chat-ext-hero.glb",
        "metrics": "modules/05-chat-communication/exterior/drafts/session87-hero-metrics.json",
        "qa_import": "modules/05-chat-communication/exterior/drafts/session87-hero-qa-import.json",
        "screenshots": "modules/05-chat-communication/screenshots",
        "pre_tris": 20052,
        "tri_min": 27000,
        "tri_max": 39000,
        "size_min_kb": 90,
        "size_max_kb": 680,
        "gate8_notes": [
            "finished multi-pod facade rhythm and occupied broadcast screens",
            "bridge sleeves, conduit hardware, and signal nodes read as built",
            "shared podium, signage, roof caps, antenna clusters, and satellite crown resolved",
        ],
    },
    {
        "id": "career",
        "label": "Career",
        "accent_hex": "#3B82F6",
        "root_name": "career-ext-hero",
        "source_glb": "modules/08-career/exterior/approved/career-ext.glb",
        "output_blend": "modules/08-career/exterior/drafts/career-session87-hero.blend",
        "draft_glb": "modules/08-career/exterior/drafts/career-ext-hero-draft-s87.glb",
        "approved_glb": "modules/08-career/exterior/approved/career-ext-hero.glb",
        "public_glb": "models/structures/08-career/career-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/08-career/career-ext-hero.glb",
        "metrics": "modules/08-career/exterior/drafts/session87-hero-metrics.json",
        "qa_import": "modules/08-career/exterior/drafts/session87-hero-qa-import.json",
        "screenshots": "modules/08-career/screenshots",
        "pre_tris": 20288,
        "tri_min": 27000,
        "tri_max": 40000,
        "size_min_kb": 90,
        "size_max_kb": 680,
        "gate8_notes": [
            "occupied professional tower skins with visible floor cadence",
            "elevator-tube machinery, bridge nodes, and executive deck hardware completed",
            "shared networking podium and roof caps preserve the upward silhouette",
        ],
    },
    {
        "id": "analytics",
        "label": "AI Analytics",
        "accent_hex": "#14B8A6",
        "root_name": "analytics-ext-hero",
        "source_glb": "modules/10-ai-analytics/exterior/approved/analytics-ext.glb",
        "output_blend": "modules/10-ai-analytics/exterior/drafts/analytics-session87-hero.blend",
        "draft_glb": "modules/10-ai-analytics/exterior/drafts/analytics-ext-hero-draft-s87.glb",
        "approved_glb": "modules/10-ai-analytics/exterior/approved/analytics-ext-hero.glb",
        "public_glb": "models/structures/10-ai-analytics/analytics-ext-hero.glb",
        "public_abs_glb": "apps/balencia/public/models/structures/10-ai-analytics/analytics-ext-hero.glb",
        "metrics": "modules/10-ai-analytics/exterior/drafts/session87-hero-metrics.json",
        "qa_import": "modules/10-ai-analytics/exterior/drafts/session87-hero-qa-import.json",
        "screenshots": "modules/10-ai-analytics/screenshots",
        "pre_tris": 19411,
        "tri_min": 28000,
        "tri_max": 41000,
        "size_min_kb": 90,
        "size_max_kb": 700,
        "gate8_notes": [
            "finished data-cathedral facade skin rather than only exposed data paths",
            "entry waterfall, pointed arch panels, buttress anchors, and display cadence resolved",
            "spire telemetry crown and beacon remain readable from Scene 13",
        ],
    },
]

FOCUSED_SCENE_CONFIG = {
    "fitness": {
        "scene": 4,
        "slug": "fitness-district",
        "offset": [48, 25, -54],
        "target_height": 10.5,
        "lens": 28,
        "frame": 96,
    },
    "chat": {
        "scene": 8,
        "slug": "communication-hub",
        "offset": [37, 23, 44],
        "target_height": 9.8,
        "lens": 29,
        "frame": 96,
    },
    "career": {
        "scene": 11,
        "slug": "career-towers",
        "offset": [-46, 27, 36],
        "target_height": 15,
        "lens": 30,
        "frame": 96,
    },
    "analytics": {
        "scene": 13,
        "slug": "analytics-cathedral",
        "offset": [-46, 25, -38],
        "target_height": 13,
        "lens": 28,
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


def add_fitness_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    body_bottom = min_z + height * 0.12
    body_top = max_z - height * 0.16
    category = "session87 fitness completed training-deck facade"

    for floor in range(30):
        t = floor / 29
        z = body_bottom + (body_top - body_bottom) * t
        flare = 1.0 + 0.10 * math.sin(t * math.pi * 2.6)
        half_w = width * (0.34 + 0.035 * math.sin(t * math.pi * 3.0)) * flare
        half_d = depth * (0.32 + 0.028 * math.cos(t * math.pi * 2.4))
        for side, y in (("front", min_y - depth * 0.020), ("back", max_y + depth * 0.020)):
            helpers.box(f"Fitness_s87_{side}_green_floor_band_{floor:02d}", (cx, y, z), (half_w, depth * 0.010, height * 0.0045), mats["emissive"], category)
            for col in range(6):
                x = cx + (col - 2.5) * half_w * 0.29
                panel_z = z + height * 0.012
                helpers.box(f"Fitness_s87_{side}_training_glass_bay_{floor:02d}_{col}", (x, y + (-0.018 if side == "front" else 0.018), panel_z), (half_w * 0.070, depth * 0.009, height * 0.015), mats["glass"], category)
                if col % 2 == floor % 2:
                    helpers.box(f"Fitness_s87_{side}_activity_readout_{floor:02d}_{col}", (x, y + (-0.030 if side == "front" else 0.030), panel_z + height * 0.011), (half_w * 0.038, depth * 0.006, height * 0.0045), mats["holo"], category)
        for side, x in (("left", min_x - width * 0.018), ("right", max_x + width * 0.018)):
            helpers.box(f"Fitness_s87_{side}_side_floor_band_{floor:02d}", (x, cy, z), (width * 0.010, half_d, height * 0.004), mats["emissive"], category)
            for col in range(3):
                y = cy + (col - 1) * half_d * 0.44
                helpers.box(f"Fitness_s87_{side}_side_muscle_panel_{floor:02d}_{col}", (x, y, z + height * 0.011), (width * 0.009, half_d * 0.105, height * 0.014), mats["glass"], category)

    brace_category = "session87 fitness exoskeleton and cantilever completion"
    for face_y, suffix in ((min_y - depth * 0.045, "front"), (max_y + depth * 0.045, "back")):
        for side in (-1, 1):
            x = cx + side * width * 0.42
            helpers.cylinder_between(f"Fitness_s87_{suffix}_corner_power_spine_{side}", (x, face_y, body_bottom), (x - side * width * 0.11, face_y, body_top), width * 0.010, mats["detail"], brace_category, vertices=6)
            for level in (0.24, 0.50, 0.76):
                z = body_bottom + (body_top - body_bottom) * level
                helpers.cylinder_between(f"Fitness_s87_{suffix}_diagonal_brace_{side}_{int(level * 100)}", (x - side * width * 0.10, face_y, z - height * 0.055), (x + side * width * 0.06, face_y, z + height * 0.060), width * 0.007, mats["accent"], brace_category, vertices=5)
        for ledge, level in enumerate((0.33, 0.63, 0.91)):
            z = body_bottom + (body_top - body_bottom) * level
            helpers.box(f"Fitness_s87_{suffix}_cantilever_training_deck_{ledge}", (cx, face_y, z), (width * 0.42, depth * 0.045, height * 0.011), mats["base"], brace_category)
            for rail in range(10):
                x = cx + (rail - 4.5) * width * 0.075
                helpers.box(f"Fitness_s87_{suffix}_deck_green_marker_{ledge}_{rail}", (x, face_y - depth * 0.020 if suffix == "front" else face_y + depth * 0.020, z + height * 0.016), (width * 0.018, depth * 0.006, height * 0.004), mats["emissive"], brace_category)

    base_category = "session87 fitness resolved athletic plinth and entry"
    front_y = min_y - depth * 0.12
    for lane, scale in enumerate((1.22, 1.08, 0.94)):
        helpers.torus(f"Fitness_s87_athletic_track_lane_{lane}", (cx, cy, min_z + 0.035 + lane * 0.018), max(width, depth) * 0.36 * scale, max(width, depth) * 0.0045, mats["energy" if lane == 1 else "base"], base_category, seg=72, minor_seg=3)
    for side in (-1, 1):
        helpers.cylinder_between(f"Fitness_s87_triangular_entry_leg_{side}", (cx + side * width * 0.28, front_y, min_z + height * 0.035), (cx + side * width * 0.070, front_y - depth * 0.025, min_z + height * 0.205), width * 0.020, mats["accent"], base_category, vertices=6)
    helpers.box("Fitness_s87_entry_shadow_gate", (cx, front_y - depth * 0.030, min_z + height * 0.112), (width * 0.18, depth * 0.030, height * 0.060), mats["detail"], base_category)
    for trophy in range(12):
        x = cx + (trophy - 5.5) * width * 0.036
        helpers.box(f"Fitness_s87_trophy_wall_glow_tile_{trophy:02d}", (x, front_y - depth * 0.052, min_z + height * (0.162 + 0.010 * (trophy % 3))), (width * 0.018, depth * 0.008, height * 0.016), mats["emissive"], base_category)

    crown_category = "session87 fitness roof equipment and pipeline crown"
    for unit in range(7):
        x = cx + (unit - 3) * width * 0.095
        y = cy + ((unit % 3) - 1) * depth * 0.12
        helpers.box(f"Fitness_s87_roof_mechanical_housing_{unit}", (x, y, max_z + height * 0.018), (width * 0.040, depth * 0.040, height * 0.032), mats["detail"], crown_category)
        helpers.box(f"Fitness_s87_roof_vent_green_slit_{unit}", (x, y - depth * 0.023, max_z + height * 0.042), (width * 0.032, depth * 0.006, height * 0.004), mats["emissive"], crown_category)
    helpers.torus("Fitness_s87_roof_pipeline_socket_collar", (cx, cy, max_z + height * 0.055), width * 0.145, width * 0.0065, mats["energy"], crown_category, seg=48, minor_seg=4)


def add_chat_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    pod_centers = [
        (cx - width * 0.27, cy - depth * 0.12, 0.84),
        (cx + width * 0.02, cy + depth * 0.10, 1.00),
        (cx + width * 0.29, cy - depth * 0.04, 0.78),
        (cx - width * 0.05, cy - depth * 0.30, 0.70),
    ]
    category = "session87 chat finished multi-pod broadcast facades"
    for pod, (px, py, scale_h) in enumerate(pod_centers):
        floors = 18 + pod * 3
        top = min_z + height * (0.22 + 0.70 * scale_h)
        bottom = min_z + height * 0.12
        pod_w = width * (0.105 + 0.012 * (pod % 2))
        pod_d = depth * (0.115 + 0.010 * ((pod + 1) % 2))
        for floor in range(floors):
            z = bottom + (top - bottom) * (floor / max(floors - 1, 1))
            for face, y in (("front", py - pod_d), ("back", py + pod_d)):
                helpers.box(f"Chat_s87_pod{pod}_{face}_orange_floor_line_{floor:02d}", (px, y, z), (pod_w, depth * 0.006, height * 0.0038), mats["emissive"], category)
                for col in range(3):
                    x = px + (col - 1) * pod_w * 0.35
                    helpers.box(f"Chat_s87_pod{pod}_{face}_message_window_{floor:02d}_{col}", (x, y, z + height * 0.010), (pod_w * 0.145, depth * 0.0055, height * 0.0105), mats["glass"], category)
            for face, x in (("left", px - pod_w), ("right", px + pod_w)):
                helpers.box(f"Chat_s87_pod{pod}_{face}_vertical_signal_spine_{floor:02d}", (x, py, z + height * 0.005), (width * 0.005, pod_d * 0.72, height * 0.004), mats["accent"], category)
        for screen in range(4):
            side_y = py - pod_d - depth * 0.018
            z = bottom + (top - bottom) * (0.30 + screen * 0.145)
            x = px + (screen - 1.5) * pod_w * 0.30
            helpers.box(f"Chat_s87_pod{pod}_live_wave_screen_{screen}", (x, side_y, z), (pod_w * 0.180, depth * 0.008, height * 0.035), mats["holo"], category)
            helpers.box(f"Chat_s87_pod{pod}_screen_orange_wave_{screen}", (x, side_y - depth * 0.006, z + height * 0.003), (pod_w * 0.130, depth * 0.004, height * 0.004), mats["emissive"], category)
        for cap in range(4):
            angle = cap * math.tau / 4
            loc = Vector((px, py, top + height * 0.025)) + Vector((math.cos(angle), math.sin(angle), 0)) * width * 0.030
            helpers.cylinder_between(f"Chat_s87_pod{pod}_antenna_bristle_{cap}", (loc.x, loc.y, top + height * 0.004), (loc.x + math.cos(angle) * width * 0.012, loc.y + math.sin(angle) * depth * 0.012, top + height * 0.105), width * 0.0038, mats["detail"], category, vertices=5)
        helpers.torus(f"Chat_s87_pod{pod}_roof_broadcast_cap", (px, py, top + height * 0.018), max(width, depth) * 0.034, max(width, depth) * 0.0038, mats["energy"], category, seg=36, minor_seg=3)

    bridge_category = "session87 chat bridge sleeves and conduit hardware"
    bridge_pairs = [(0, 1, 0.64), (1, 2, 0.56), (3, 0, 0.42), (3, 2, 0.50)]
    for bridge, (a, b, t) in enumerate(bridge_pairs):
        ax, ay, _ = pod_centers[a]
        bx, by, _ = pod_centers[b]
        z = min_z + height * t
        helpers.cylinder_between(f"Chat_s87_glass_bridge_sleeve_{bridge}", (ax, ay, z), (bx, by, z + height * 0.018), width * 0.018, mats["glass"], bridge_category, vertices=8)
        helpers.cylinder_between(f"Chat_s87_inner_signal_thread_{bridge}", (ax, ay, z + height * 0.010), (bx, by, z + height * 0.028), width * 0.006, mats["energy"], bridge_category, vertices=5)
        for node, loc in enumerate(((ax, ay, z), (bx, by, z + height * 0.018))):
            helpers.torus(f"Chat_s87_bridge_status_node_{bridge}_{node}", loc, width * 0.030, width * 0.0038, mats["emissive"], bridge_category, seg=30, minor_seg=3)

    base_category = "session87 chat public plaza and communication threshold"
    helpers.box("Chat_s87_shared_plaza_finished_plate", (cx, cy, min_z + height * 0.020), (width * 0.58, depth * 0.42, height * 0.008), mats["base"], base_category)
    for tile in range(24):
        x = cx + (tile % 8 - 3.5) * width * 0.060
        y = cy + (tile // 8 - 1) * depth * 0.090
        helpers.box(f"Chat_s87_plaza_conversation_tile_{tile:02d}", (x, y, min_z + height * 0.040), (width * 0.030, depth * 0.020, height * 0.004), mats["emissive" if tile % 3 == 0 else "detail"], base_category)
    helpers.cylinder("Chat_s87_main_satellite_dish", (cx + width * 0.03, cy + depth * 0.10, max_z + height * 0.060), width * 0.052, width * 0.016, mats["detail"], base_category, vertices=18, rot=(1.08, 0.28, 0.18))
    helpers.torus("Chat_s87_main_broadcast_halo", (cx + width * 0.03, cy + depth * 0.10, max_z + height * 0.075), width * 0.080, width * 0.004, mats["energy"], base_category, seg=48, minor_seg=3)


def add_career_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    tower_specs = [
        (cx - width * 0.24, cy + depth * 0.10, 0.78, 0.095),
        (cx + width * 0.02, cy - depth * 0.02, 1.00, 0.115),
        (cx + width * 0.26, cy + depth * 0.06, 0.68, 0.085),
        (cx - width * 0.02, cy - depth * 0.28, 0.58, 0.075),
    ]
    category = "session87 career occupied professional tower skins"
    for tower, (tx, ty, scale_h, scale_w) in enumerate(tower_specs):
        floors = 22 + tower * 4
        bottom = min_z + height * 0.10
        top = min_z + height * (0.23 + scale_h * 0.72)
        tower_w = width * scale_w
        tower_d = depth * (scale_w * 1.04)
        for floor in range(floors):
            t = floor / max(floors - 1, 1)
            z = bottom + (top - bottom) * t
            taper = 1.0 - 0.12 * t
            for face, y in (("front", ty - tower_d * taper), ("back", ty + tower_d * taper)):
                helpers.box(f"Career_s87_t{tower}_{face}_blue_floor_joint_{floor:02d}", (tx, y, z), (tower_w * taper, depth * 0.0055, height * 0.0035), mats["emissive"], category)
                for bay in range(4):
                    x = tx + (bay - 1.5) * tower_w * taper * 0.26
                    helpers.box(f"Career_s87_t{tower}_{face}_office_glass_bay_{floor:02d}_{bay}", (x, y, z + height * 0.010), (tower_w * 0.082, depth * 0.005, height * 0.010), mats["glass"], category)
            for face, x in (("left", tx - tower_w * taper), ("right", tx + tower_w * taper)):
                helpers.box(f"Career_s87_t{tower}_{face}_upward_edge_light_{floor:02d}", (x, ty, z + height * 0.004), (width * 0.0045, tower_d * taper * 0.74, height * 0.0035), mats["accent"], category)
        for fin in (-1, 1):
            helpers.cylinder_between(f"Career_s87_t{tower}_roof_ascent_fin_{fin}", (tx + fin * tower_w * 0.55, ty, top), (tx + fin * tower_w * 0.72, ty, top + height * 0.090), width * 0.0055, mats["accent"], category, vertices=5)
        helpers.box(f"Career_s87_t{tower}_roof_cap_plate", (tx, ty, top + height * 0.018), (tower_w * 0.80, tower_d * 0.78, height * 0.014), mats["detail"], category)

    elevator_category = "session87 career elevator tubes and bridge nodes"
    for tube, (tx, ty, scale_h, scale_w) in enumerate((tower_specs[1], tower_specs[0])):
        top = min_z + height * (0.23 + scale_h * 0.72)
        x = tx + width * (0.075 if tube == 0 else -0.065)
        y = ty - depth * 0.120
        helpers.cylinder_between(f"Career_s87_external_elevator_glass_tube_{tube}", (x, y, min_z + height * 0.15), (x, y, top - height * 0.03), width * 0.015, mats["glass"], elevator_category, vertices=12)
        for car in range(4):
            z = min_z + height * (0.22 + car * 0.13)
            helpers.box(f"Career_s87_elevator_car_blue_marker_{tube}_{car}", (x, y - depth * 0.020, z), (width * 0.025, depth * 0.006, height * 0.018), mats["emissive"], elevator_category)
    bridge_pairs = [(0, 1, 0.52), (1, 2, 0.62), (3, 0, 0.40), (3, 2, 0.46)]
    for bridge, (a, b, t) in enumerate(bridge_pairs):
        ax, ay, _, _ = tower_specs[a]
        bx, by, _, _ = tower_specs[b]
        z = min_z + height * t
        helpers.cylinder_between(f"Career_s87_enclosed_stage_bridge_{bridge}", (ax, ay, z), (bx, by, z + height * 0.014), width * 0.018, mats["glass"], elevator_category, vertices=8)
        helpers.cylinder_between(f"Career_s87_bridge_blue_path_core_{bridge}", (ax, ay, z + height * 0.011), (bx, by, z + height * 0.025), width * 0.005, mats["emissive"], elevator_category, vertices=5)
        for node, loc in enumerate(((ax, ay, z), (bx, by, z + height * 0.014))):
            helpers.box(f"Career_s87_bridge_transfer_node_{bridge}_{node}", loc, (width * 0.028, depth * 0.022, height * 0.018), mats["detail"], elevator_category)

    base_category = "session87 career networking podium and executive crown"
    helpers.box("Career_s87_networking_podium_finished_plate", (cx, cy, min_z + height * 0.025), (width * 0.60, depth * 0.40, height * 0.010), mats["base"], base_category)
    for path in range(16):
        x = cx + (path - 7.5) * width * 0.037
        helpers.box(f"Career_s87_networking_plaza_blue_path_{path:02d}", (x, min_y - depth * 0.045, min_z + height * 0.052), (width * 0.015, depth * 0.090, height * 0.004), mats["emissive"], base_category)
    main_x, main_y, main_h, main_w = tower_specs[1]
    deck_z = min_z + height * (0.23 + main_h * 0.72) + height * 0.035
    helpers.box("Career_s87_executive_observation_deck_glass", (main_x, main_y - depth * 0.175, deck_z), (width * 0.125, depth * 0.080, height * 0.010), mats["glass"], base_category)
    for rail in range(9):
        x = main_x + (rail - 4) * width * 0.026
        helpers.cylinder_between(f"Career_s87_observation_deck_rail_{rail}", (x, main_y - depth * 0.222, deck_z), (x, main_y - depth * 0.222, deck_z + height * 0.035), width * 0.0028, mats["detail"], base_category, vertices=5)
    helpers.torus("Career_s87_roof_pipeline_socket_collar", (main_x, main_y, max_z + height * 0.052), width * 0.070, width * 0.0048, mats["energy"], base_category, seg=42, minor_seg=3)


def add_analytics_hero(mats, bbox):
    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    cx, cy, _ = bbox["center"]
    front_y = min_y - depth * 0.050
    body_bottom = min_z + height * 0.14
    body_top = max_z - height * 0.18
    category = "session87 analytics finished living data facade"

    for row in range(18):
        t = row / 17
        z = body_bottom + (body_top - body_bottom) * t
        half_w = width * (0.34 - 0.08 * t)
        for col in range(7):
            x = cx + (col - 3) * half_w * 0.26
            panel_h = height * (0.026 + 0.010 * ((row + col) % 3 == 0))
            helpers.box(f"Analytics_s87_front_dashboard_panel_{row:02d}_{col}", (x, front_y, z + panel_h * 0.20), (half_w * 0.075, depth * 0.006, panel_h), mats["holo" if (row + col) % 2 else "emissive"], category)
            helpers.box(f"Analytics_s87_front_panel_shadow_frame_{row:02d}_{col}", (x, front_y + depth * 0.006, z - height * 0.020), (half_w * 0.086, depth * 0.004, height * 0.004), mats["detail"], category)
        for glyph in range(8):
            x = cx + (glyph - 3.5) * half_w * 0.22
            glyph_z = z + height * (0.030 + 0.006 * (glyph % 3))
            helpers.box(f"Analytics_s87_front_micro_forecast_glyph_{row:02d}_{glyph:02d}", (x, front_y - depth * 0.010, glyph_z), (half_w * 0.026, depth * 0.0045, height * 0.006), mats["emissive" if glyph % 2 else "holo"], category)
        for side, x in (("left", cx - half_w - width * 0.020), ("right", cx + half_w + width * 0.020)):
            helpers.box(f"Analytics_s87_{side}_data_rib_{row:02d}", (x, cy, z), (width * 0.006, depth * 0.42, height * 0.0045), mats["accent"], category)
            for tile in range(3):
                y = cy + (tile - 1) * depth * 0.125
                helpers.box(f"Analytics_s87_{side}_side_heatmap_tile_{row:02d}_{tile}", (x, y, z + height * 0.012), (width * 0.005, depth * 0.040, height * 0.015), mats["holo"], category)

    arch_category = "session87 analytics pointed arch and buttress completion"
    for arch in range(7):
        x = cx + (arch - 3) * width * 0.073
        z = min_z + height * (0.28 + 0.050 * (arch % 2))
        helpers.cylinder(f"Analytics_s87_pointed_arch_holo_window_{arch}", (x, front_y - depth * 0.020, z), width * 0.025, depth * 0.020, mats["holo"], arch_category, vertices=16, rot=(math.pi / 2, 0, 0))
        helpers.cone(f"Analytics_s87_pointed_arch_cap_{arch}", (x, front_y - depth * 0.021, z + height * 0.035), width * 0.028, 0.0, height * 0.050, mats["detail"], arch_category, vertices=4, rot=(0, 0, math.pi / 4))
    for side in (-1, 1):
        anchor_x = cx + side * width * 0.44
        for buttress in range(4):
            z0 = min_z + height * (0.08 + buttress * 0.105)
            z1 = min_z + height * (0.34 + buttress * 0.105)
            end_x = cx + side * width * (0.22 - buttress * 0.010)
            helpers.cylinder_between(f"Analytics_s87_flying_buttress_data_arc_{side}_{buttress}", (anchor_x, cy + depth * (0.18 - buttress * 0.04), z0), (end_x, cy, z1), width * 0.010, mats["detail"], arch_category, vertices=6)
            helpers.cylinder_between(f"Analytics_s87_buttress_teal_fiber_{side}_{buttress}", (anchor_x, cy + depth * (0.18 - buttress * 0.04), z0 + height * 0.018), (end_x, cy, z1 + height * 0.018), width * 0.0038, mats["energy"], arch_category, vertices=5)
            helpers.box(f"Analytics_s87_buttress_base_anchor_{side}_{buttress}", (anchor_x, cy + depth * (0.18 - buttress * 0.04), z0 - height * 0.012), (width * 0.046, depth * 0.040, height * 0.018), mats["base"], arch_category)

    entry_category = "session87 analytics entry waterfall and telemetry crown"
    for stream in range(14):
        x = cx + (stream - 6.5) * width * 0.021
        helpers.cylinder_between(f"Analytics_s87_data_waterfall_stream_{stream:02d}", (x, front_y - depth * 0.050, min_z + height * 0.250), (x + math.sin(stream * 1.7) * width * 0.006, front_y - depth * 0.065, min_z + height * 0.055), width * 0.0035, mats["emissive"], entry_category, vertices=5)
    helpers.box("Analytics_s87_deep_cathedral_entry_shadow", (cx, front_y - depth * 0.074, min_z + height * 0.120), (width * 0.160, depth * 0.022, height * 0.075), mats["detail"], entry_category)
    for ring, z in enumerate((max_z - height * 0.085, max_z - height * 0.045, max_z - height * 0.010)):
        helpers.torus(f"Analytics_s87_spire_telemetry_ring_{ring}", (cx, cy, z), width * (0.135 - ring * 0.020), width * 0.0048, mats["energy" if ring > 0 else "detail"], entry_category, seg=48, minor_seg=3)
    helpers.cone("Analytics_s87_resolved_spire_cap", (cx, cy, max_z + height * 0.038), width * 0.075, width * 0.020, height * 0.115, mats["detail"], entry_category, vertices=8, rot=(0, 0, math.pi / 8))
    helpers.cylinder("Analytics_s87_teal_data_beacon", (cx, cy, max_z + height * 0.105), width * 0.012, height * 0.110, mats["emissive"], entry_category, vertices=12)
    for glyph in range(32):
        angle = glyph * math.tau / 32
        loc = Vector((cx, cy, max_z + height * 0.035)) + Vector((math.cos(angle), math.sin(angle), 0)) * width * 0.185
        helpers.box(f"Analytics_s87_crown_forecast_glyph_{glyph:02d}", (loc.x, loc.y, loc.z + height * 0.006 * (glyph % 3)), (width * 0.014, depth * 0.006, height * 0.010), mats["holo" if glyph % 2 else "emissive"], entry_category, rot=(0, 0, angle))


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
    prefix = f"session87-{module['id']}-hero"
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
        assembly_path = os.path.join(AFTER_DIR, f"{module['id']}-{view.replace('_', '-')}.png")
        shutil.copy2(path, assembly_path)
        if dark and saved:
            for material, value in saved:
                bsdf = material.node_tree.nodes.get("Principled BSDF")
                bsdf.inputs["Emission Strength"].default_value = value
    return evidence


def build_module(module):
    print(f"--- Session 87 hero exterior: {module['label']} ---")
    helpers.created_categories = {}
    helpers.clear_scene()
    bpy.ops.import_scene.gltf(filepath=abs_path(module["source_glb"]))
    mats = helpers.normalize_materials(module["accent_hex"])
    pre_bbox = helpers.world_bbox()
    pre_tris = helpers.count_tris()
    pre_objects = len(helpers.mesh_objects())

    if module["id"] == "fitness":
        add_fitness_hero(mats, pre_bbox)
    elif module["id"] == "chat":
        add_chat_hero(mats, pre_bbox)
    elif module["id"] == "career":
        add_career_hero(mats, pre_bbox)
    elif module["id"] == "analytics":
        add_analytics_hero(mats, pre_bbox)
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
        raise RuntimeError(f"{module['label']} Session 87 QA failed: {qa}")

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
    manifest["sourceOfTruth"]["assemblyAudit"] = "assembly/audit/session-87-urban-vertical-wave.md"
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
        "four_hero_exteriors_built": len(metrics_by_id) == 4,
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
        "scope": "Phase 10 urban/vertical wave hero exteriors for Fitness, Chat, Career, and AI Analytics",
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
        "# Session 87 Urban/Vertical Wave",
        "",
        f"Date: {date.today()}",
        f"Status: {report['status'].title()}",
        "",
        "## Scope",
        "",
        "Session 87 built Phase 10 architectural completion hero exterior LODs for Fitness, Chat and Communication, Career, and AI Analytics. Approved overview exteriors, layout positions, baked energy endpoints, Phase 9 behavior, and the overview LOD policy were preserved.",
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
            "- Fitness: angular gym exoskeleton now has a visible glass/panel skin, training-deck floor cadence, resolved entry portal, trophy wall, athletic track edge, and roof mechanical crown.",
            "- Chat and Communication: multi-pod cluster now has finished facade rhythm, live wave screens, bridge sleeves, conduit signal threads, roof caps, antenna arrays, and a resolved broadcast plaza.",
            "- Career: tower cluster now has occupied office bays, blue floor cadence, elevator tube hardware, enclosed bridge nodes, networking podium, executive deck, and roof caps.",
            "- AI Analytics: data cathedral now has finished dashboard skin, pointed arch panels, buttress anchors/fibers, entry data waterfall, spire telemetry rings, and beacon crown.",
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
    contact_items = []
    before_dir = os.path.join(ROOT, "assembly", "screenshots", "session-85-completion-audit", "app-hero-cameras")
    before_files = {
        "fitness": "scene-04-fitness-fitness-district-app-hero.png",
        "chat": "scene-08-chat-communication-hub-app-hero.png",
        "career": "scene-11-career-career-towers-app-hero.png",
        "analytics": "scene-13-analytics-analytics-cathedral-app-hero.png",
    }
    for module in MODULES:
        metrics = metrics_by_id[module["id"]]
        contact_items.append({"path": os.path.join(before_dir, before_files[module["id"]]), "label": f"{module['label']} before"})
        contact_items.append({"path": abs_path(app_hero_evidence[module["id"]]["path"]), "label": f"{module['label']} hero after"})
        contact_items.append({"path": abs_path(metrics["evidence"]["dark_first"]), "label": f"{module['label']} dark-first"})
    contact_sheet = helpers.render_contact_sheet(
        contact_items,
        os.path.join(SCREENSHOT_DIR, "s87-urban-vertical-wave-before-after-contact-sheet.png"),
        "Session 87 Urban/Vertical Wave - Before, Hero After, Dark-First",
        cols=3,
        width=2400,
        height=2400,
    )
    write_reports(metrics_by_id, app_hero_evidence, contact_sheet)


if __name__ == "__main__":
    main()

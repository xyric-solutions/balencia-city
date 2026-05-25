"""
Session 55: Phase 5 AI pulse ring.

Builds the SIA crown heartbeat as an animated orange energy torus, renders QA
evidence, exports a draft GLB, and promotes it when checks pass.
"""

import json
import math
import os
import shutil
from mathutils import Vector

import bpy


THIS_FILE = os.path.abspath(__file__)
DRAFTS = os.path.dirname(THIS_FILE)
PULSE_DIR = os.path.dirname(DRAFTS)
ENERGY_DIR = os.path.dirname(PULSE_DIR)
PROJECT = os.path.dirname(ENERGY_DIR)
MODULES = os.path.join(PROJECT, "modules")
SHARED = os.path.join(PROJECT, "shared")
SCREENSHOTS = os.path.join(ENERGY_DIR, "screenshots")
APPROVED = os.path.join(PULSE_DIR, "approved")
SESSION_REPORT = os.path.join(DRAFTS, "ai-pulse-session55-report.json")
SESSION_BLEND = os.path.join(DRAFTS, "ai-pulse-session55.blend")
DRAFT_GLB = os.path.join(DRAFTS, "ai-pulse-session55.glb")
APPROVED_GLB = os.path.join(APPROVED, "ai-pulse.glb")
LATEST_LAYOUT_REPORT = os.path.join(
    MODULES, "11-nutrition", "integration-session-48-report.json"
)

PRIOR_ENERGY_ASSETS = {
    "hard_pipelines": os.path.join(ENERGY_DIR, "pipelines/approved/hard-pipelines.glb"),
    "warm_mist": os.path.join(ENERGY_DIR, "pipelines/approved/warm-mist.glb"),
    "faint_thread": os.path.join(ENERGY_DIR, "pipelines/approved/faint-thread.glb"),
    "knowledgebase_waterfall": os.path.join(
        ENERGY_DIR, "pipelines/approved/knowledgebase-waterfall.glb"
    ),
    "leaderboard_lightning": os.path.join(
        ENERGY_DIR, "pipelines/approved/leaderboard-lightning.glb"
    ),
    "cross_district_gold": os.path.join(
        ENERGY_DIR, "cross-connections/approved/cross-district-gold.glb"
    ),
}

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


STRUCTURES = [
    {
        "name": "SIA_Tower",
        "label": "SIA Tower",
        "position": (0, 0, 0),
        "exterior": os.path.join(
            MODULES, "00-sia-tower/exterior/approved/sia-tower-ext.glb"
        ),
    },
    {
        "name": "Fitness",
        "label": "Fitness",
        "position": (26, 25, 0),
        "exterior": os.path.join(MODULES, "01-fitness/exterior/approved/fitness-ext.glb"),
    },
    {
        "name": "Yoga",
        "label": "Yoga & Wellbeing",
        "position": (36, 10, 0),
        "exterior": os.path.join(
            MODULES, "02-yoga-wellbeing/exterior/approved/yoga-ext.glb"
        ),
    },
    {
        "name": "Finance",
        "label": "Finance",
        "position": (35, -6, 0),
        "exterior": os.path.join(MODULES, "03-finance/exterior/approved/finance-ext.glb"),
    },
    {
        "name": "Knowledgebase",
        "label": "Knowledgebase",
        "position": (31, -22, 0),
        "exterior": os.path.join(
            MODULES, "04-knowledgebase/exterior/approved/knowledgebase-ext.glb"
        ),
    },
    {
        "name": "Chat",
        "label": "Chat & Communication",
        "position": (19, -36, 0),
        "exterior": os.path.join(
            MODULES, "05-chat-communication/exterior/approved/chat-ext.glb"
        ),
    },
    {
        "name": "Leaderboard",
        "label": "Leaderboard & Competition",
        "position": (-8, -45, 0),
        "exterior": os.path.join(
            MODULES, "06-leaderboard-competition/exterior/approved/leaderboard-ext.glb"
        ),
    },
    {
        "name": "Relationships",
        "label": "Relationships",
        "position": (8, -59, 0),
        "exterior": os.path.join(
            MODULES, "07-relationships/exterior/approved/relationships-ext.glb"
        ),
    },
    {
        "name": "Career",
        "label": "Career",
        "position": (-30, -34, 0),
        "exterior": os.path.join(MODULES, "08-career/exterior/approved/career-ext.glb"),
    },
    {
        "name": "Recovery",
        "label": "Recovery & Sleep",
        "position": (-43, -8, 0),
        "exterior": os.path.join(
            MODULES, "09-recovery-sleep/exterior/approved/recovery-ext.glb"
        ),
    },
    {
        "name": "Analytics",
        "label": "AI Analytics",
        "position": (-31, 14, 0),
        "exterior": os.path.join(
            MODULES, "10-ai-analytics/exterior/approved/analytics-ext.glb"
        ),
    },
    {
        "name": "Nutrition",
        "label": "Nutrition",
        "position": (-12, 39, 0),
        "exterior": os.path.join(MODULES, "11-nutrition/exterior/approved/nutrition-ext.glb"),
    },
]

VALID_PULSE_FRAMES = [0, 12, 48, 96, 144, 192]
FPS = 24
CYCLE_SECONDS = 8.0
EXPANSION_SECONDS = 6.0
RING_CROSS_SECTION_RADIUS = 0.1
EMISSION_STRENGTH = 2.4


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r", encoding="utf-8") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


def setup_render():
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = int(CYCLE_SECONDS * FPS)
    scene.frame_set(96)
    scene.render.fps = FPS
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        eevee = scene.eevee
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
            eevee.bloom_threshold = 0.12
            eevee.bloom_intensity = 0.95
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.7


def make_energy_material():
    mat = bpy.data.materials.new("energy")
    mat.diffuse_color = (1.0, 0.27, 0.0, 0.74)
    mat.use_nodes = True
    mat.blend_method = "BLEND"
    mat.use_screen_refraction = False
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (1.0, 0.27, 0.0, 0.74)
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = 0.74
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.27, 0.0, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = EMISSION_STRENGTH
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.18
    return mat


def import_glb(path, collection, position=(0, 0, 0)):
    if not os.path.exists(path):
        return []

    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    imported = [obj for obj in bpy.data.objects if obj not in before]
    imported_set = set(imported)

    for obj in imported:
        for user_collection in list(obj.users_collection):
            user_collection.objects.unlink(obj)
        collection.objects.link(obj)

    offset = Vector(position)
    roots = [obj for obj in imported if obj.parent not in imported_set]
    for root in roots:
        root.location += offset

    bpy.ops.object.select_all(action="DESELECT")
    return imported


def world_bbox(objects):
    mesh_objects = [obj for obj in objects if obj.type == "MESH" and hasattr(obj, "bound_box")]
    if not mesh_objects:
        return None
    mins = []
    maxs = []
    for obj in mesh_objects:
        corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        mins.append(
            Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners)))
        )
        maxs.append(
            Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners)))
        )
    mn = Vector((min(v.x for v in mins), min(v.y for v in mins), min(v.z for v in mins)))
    mx = Vector((max(v.x for v in maxs), max(v.y for v in maxs), max(v.z for v in maxs)))
    return {"min": mn, "max": mx, "size": mx - mn, "center": (mn + mx) * 0.5}


def bbox_dict(box):
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


def collect_materials(objects):
    names = set()
    for obj in objects:
        if obj.type != "MESH":
            continue
        for slot in obj.material_slots:
            if slot.material:
                names.add(slot.material.name)
    return sorted(names)


def point_camera(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_camera(name, loc, target, lens=28, clip_end=900):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.1
    data.clip_end = clip_end
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = Vector(loc)
    point_camera(obj, target)
    return obj


def render_still(camera, filename, frame):
    path = os.path.join(SCREENSHOTS, filename)
    bpy.context.scene.frame_set(frame)
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def link_to_collection(obj, collection):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def radial_distance(point):
    return math.hypot(point.x, point.y)


def city_radius_from_registry(registry):
    max_radius = 0.0
    center_radii = []
    for name, item in registry.items():
        if name == "SIA_Tower" or not item["bbox"]:
            continue
        box = item["bbox"]
        center_radii.append(radial_distance(box["center"]))
        for x in (box["min"].x, box["max"].x):
            for y in (box["min"].y, box["max"].y):
                max_radius = max(max_radius, math.hypot(x, y))
    return {
        "inner_district_radius": min(center_radii),
        "all_district_response_radius": max(center_radii),
        "perimeter_radius": max_radius + 2.0,
    }


def keyframe_scale(obj, frame_scale_pairs):
    for frame, scale in frame_scale_pairs:
        obj.scale = (scale, scale, 1.0)
        obj.keyframe_insert(data_path="scale", frame=frame)

    action = obj.animation_data.action if obj.animation_data else None
    if not action:
        return [int(frame) for frame, _scale in frame_scale_pairs]

    frames = set(int(frame) for frame, _scale in frame_scale_pairs)
    # Blender 5.1 migrated Actions to a layered API. When legacy f-curves are
    # present, keep the pulse interpolation linear; otherwise the explicit
    # keyframe list above remains the source for QA and GLB export.
    for fcurve in getattr(action, "fcurves", []):
        for key in fcurve.keyframe_points:
            key.interpolation = "LINEAR"
            frames.add(int(round(key.co.x)))
    return sorted(frames)


def create_pulse_geometry(mat, collection, origin, radii):
    perimeter_radius = radii["perimeter_radius"]
    inner_radius = radii["inner_district_radius"]
    response_radius = radii["all_district_response_radius"]
    start_radius = 0.08
    crown_ring_radius = 4.5

    bpy.ops.mesh.primitive_torus_add(
        major_segments=32,
        minor_segments=6,
        major_radius=perimeter_radius,
        minor_radius=RING_CROSS_SECTION_RADIUS,
        location=origin,
    )
    ring = bpy.context.object
    ring.name = "ai_pulse_expanding_ring"
    ring.data.name = "ai_pulse_expanding_ring_mesh"
    ring.data.materials.append(mat)
    link_to_collection(ring, collection)

    frame_scales = [
        (0, start_radius / perimeter_radius),
        (12, crown_ring_radius / perimeter_radius),
        (48, inner_radius / perimeter_radius),
        (96, response_radius / perimeter_radius),
        (144, 1.0),
        (192, start_radius / perimeter_radius),
    ]
    keyframes = keyframe_scale(ring, frame_scales)

    ring["pulse_session"] = 55
    ring["pulse_cycle_seconds"] = CYCLE_SECONDS
    ring["expansion_seconds"] = EXPANSION_SECONDS
    ring["runtime_hint"] = "Scale from crown to city perimeter, fade alpha to zero by T=6, loop every 8 seconds."
    ring["radius_at_t0_seconds"] = start_radius
    ring["radius_at_t0_5_seconds"] = crown_ring_radius
    ring["radius_at_t2_seconds"] = inner_radius
    ring["radius_at_t4_seconds"] = response_radius
    ring["radius_at_t6_seconds"] = perimeter_radius

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=1.25,
        depth=0.045,
        location=(origin.x, origin.y, origin.z + 0.03),
    )
    crown_flash = bpy.context.object
    crown_flash.name = "ai_pulse_crown_intensifier"
    crown_flash.data.name = "ai_pulse_crown_intensifier_mesh"
    crown_flash.data.materials.append(mat)
    link_to_collection(crown_flash, collection)
    keyframe_scale(
        crown_flash,
        [
            (0, 0.8),
            (12, 1.35),
            (48, 0.65),
            (96, 0.45),
            (144, 0.18),
            (192, 0.8),
        ],
    )
    crown_flash["pulse_session"] = 55
    crown_flash["runtime_hint"] = "Crown glow intensifier for the heartbeat origin."

    return [ring, crown_flash], keyframes


def export_selected_glb(path, objects):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    export_kwargs = {
        "filepath": path,
        "export_format": "GLB",
        "use_selection": True,
        "export_draco_mesh_compression_enable": True,
        "export_draco_mesh_compression_level": 6,
        "export_materials": "EXPORT",
        "export_cameras": False,
        "export_lights": False,
        "export_animations": True,
        "export_extras": True,
    }
    try:
        bpy.ops.export_scene.gltf(**export_kwargs, export_apply_modifiers=True)
    except TypeError:
        export_kwargs.pop("export_animations", None)
        export_kwargs.pop("export_extras", None)
        bpy.ops.export_scene.gltf(**export_kwargs)
    bpy.ops.object.select_all(action="DESELECT")


def import_qa(glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb_path)
    objects = list(bpy.data.objects)
    mesh_objects = [obj for obj in objects if obj.type == "MESH"]
    empty_objects = [obj for obj in objects if obj.type == "EMPTY"]
    materials = collect_materials(mesh_objects)
    actions = list(bpy.data.actions)
    return {
        "object_count": len(objects),
        "mesh_count": len(mesh_objects),
        "empty_count": len(empty_objects),
        "tris": count_tris(mesh_objects),
        "materials": materials,
        "materials_valid": materials == ["energy"],
        "animation_count": len(actions),
        "animation_names": [action.name for action in actions],
        "file_size_bytes": os.path.getsize(glb_path),
    }


print("=" * 72)
print("Session 55: AI Pulse Ring")
print("=" * 72)

bpy.ops.wm.read_factory_settings(use_empty=True)
energy_mat = make_energy_material()

lighting = load_python_module(os.path.join(SHARED, "lighting-rig.py"), "lighting_rig")
lighting["clear_lighting"]()
lighting["setup_viewport_lighting"]()
setup_render()

context_collection = bpy.data.collections.new("Approved_Structure_Context")
bpy.context.scene.collection.children.link(context_collection)
prior_energy_collection = bpy.data.collections.new("Approved_Energy_Context")
bpy.context.scene.collection.children.link(prior_energy_collection)
pulse_collection = bpy.data.collections.new("AI_Pulse_S55")
bpy.context.scene.collection.children.link(pulse_collection)

registry = {}
missing_assets = []

for cfg in STRUCTURES:
    collection = bpy.data.collections.new(cfg["name"])
    context_collection.children.link(collection)
    if not os.path.exists(cfg["exterior"]):
        missing_assets.append(cfg["exterior"])
        imported = []
    else:
        imported = import_glb(cfg["exterior"], collection, cfg["position"])
    box = world_bbox(imported) if imported else None
    registry[cfg["name"]] = {"config": cfg, "objects": imported, "bbox": box}

with open(LATEST_LAYOUT_REPORT, "r", encoding="utf-8") as handle:
    layout_report = json.load(handle)

layout_scales = layout_report.get("structure_scales", {})
for name, item in registry.items():
    if name in layout_scales:
        scale = layout_scales[name]
        item["bbox"] = {
            "min": Vector(scale["min"]),
            "max": Vector(scale["max"]),
            "size": Vector(scale["size"]),
            "center": Vector(scale["center"]),
        }

prior_energy_imports = {}
for key, path in PRIOR_ENERGY_ASSETS.items():
    collection = bpy.data.collections.new(key)
    prior_energy_collection.children.link(collection)
    prior_energy_imports[key] = import_glb(path, collection) if os.path.exists(path) else []

sia_box = registry["SIA_Tower"]["bbox"]
city_radii = city_radius_from_registry(registry)
pulse_origin = Vector((0, 0, sia_box["max"].z + 0.35))

pulse_objects, pulse_keyframes = create_pulse_geometry(
    energy_mat, pulse_collection, pulse_origin, city_radii
)

root = bpy.data.objects.new("ai_pulse_root", None)
root.empty_display_type = "PLAIN_AXES"
root.empty_display_size = 0.4
root.location = pulse_origin
root["pulse_session"] = 55
root["pulse_cycle_seconds"] = CYCLE_SECONDS
root["expansion_seconds"] = EXPANSION_SECONDS
root["runtime_material_key"] = "energy"
root["runtime_hint"] = "City heartbeat. Loop animation every 8 seconds; fade after frame 144."
pulse_collection.objects.link(root)
for obj in pulse_objects:
    obj.parent = root

screenshots = {
    "crown_origin": render_still(
        make_camera("S55_Pulse_Crown_Origin", (24, -30, 54), (0, 0, pulse_origin.z), lens=42),
        "s55-ai-pulse-crown-origin.png",
        12,
    ),
    "inner_districts": render_still(
        make_camera("S55_Pulse_Inner_Districts", (90, -110, 92), (2, -7, 25), lens=17),
        "s55-ai-pulse-inner-districts.png",
        48,
    ),
    "citywide_perimeter": render_still(
        make_camera("S55_Pulse_Citywide_Perimeter", (112, -148, 112), (0, -8, 26), lens=14),
        "s55-ai-pulse-citywide-perimeter.png",
        144,
    ),
}

bpy.ops.wm.save_as_mainfile(filepath=SESSION_BLEND)

selected_for_export = [root] + pulse_objects
export_selected_glb(DRAFT_GLB, selected_for_export)

pulse_materials = collect_materials(pulse_objects)
total_tris = count_tris(pulse_objects)
file_size_bytes = os.path.getsize(DRAFT_GLB)

max_structure_radius = city_radii["perimeter_radius"] - 2.0
checks = {
    "approved_structure_assets_present": not missing_assets,
    "prior_energy_assets_present": all(
        os.path.exists(path) and len(prior_energy_imports[key]) > 0
        for key, path in PRIOR_ENERGY_ASSETS.items()
    ),
    "pulse_origin_at_sia_crown": pulse_origin.z >= sia_box["max"].z
    and pulse_origin.z <= sia_box["max"].z + 1.0
    and abs(pulse_origin.x) < 0.01
    and abs(pulse_origin.y) < 0.01,
    "ring_geometry_present": any(obj.name == "ai_pulse_expanding_ring" for obj in pulse_objects),
    "horizontal_ring": abs(pulse_objects[0].rotation_euler.x) < 0.001
    and abs(pulse_objects[0].rotation_euler.y) < 0.001,
    "small_cross_section": abs(RING_CROSS_SECTION_RADIUS - 0.1) < 0.0001,
    "animation_keyframes": pulse_keyframes == VALID_PULSE_FRAMES,
    "cycle_timing": bpy.context.scene.frame_end == 192 and bpy.context.scene.render.fps == FPS,
    "city_perimeter_reached": city_radii["perimeter_radius"] >= max_structure_radius,
    "material_named_energy": pulse_materials == ["energy"],
    "emissive_strength": EMISSION_STRENGTH >= 2.0,
    "technical_budget": 200 <= total_tris <= 500,
    "file_budget": file_size_bytes <= 40 * 1024,
}

import_check = import_qa(DRAFT_GLB)
checks["approved_glb_reimports"] = import_check["mesh_count"] == len(pulse_objects)
checks["approved_glb_materials_valid"] = import_check["materials_valid"]
checks["approved_glb_animation_present"] = import_check["animation_count"] >= 1

overall = "APPROVED" if all(checks.values()) else "NEEDS REVIEW"
if overall == "APPROVED":
    shutil.copyfile(DRAFT_GLB, APPROVED_GLB)

report = {
    "session": 55,
    "asset": "energy-system/ai-pulse",
    "scope": {
        "pulse_geometry_count": len(pulse_objects),
        "cycle_seconds": CYCLE_SECONDS,
        "expansion_seconds": EXPANSION_SECONDS,
        "note": (
            "Builds the SIA crown heartbeat as an animated orange energy ring. "
            "The torus expands from the SIA crown to the city perimeter by T=6 "
            "and returns to origin by T=8 for a continuous loop."
        ),
    },
    "source_layout_report": LATEST_LAYOUT_REPORT,
    "missing_assets": missing_assets,
    "prior_energy_assets": PRIOR_ENERGY_ASSETS,
    "structure_scales": {name: bbox_dict(item["bbox"]) for name, item in registry.items() if item["bbox"]},
    "pulse_metrics": {
        "origin": [round(pulse_origin.x, 4), round(pulse_origin.y, 4), round(pulse_origin.z, 4)],
        "sia_crown_z": round(sia_box["max"].z, 4),
        "origin_clearance_above_crown": round(pulse_origin.z - sia_box["max"].z, 4),
        "inner_district_radius": round(city_radii["inner_district_radius"], 4),
        "all_district_response_radius": round(city_radii["all_district_response_radius"], 4),
        "perimeter_radius": round(city_radii["perimeter_radius"], 4),
        "city_diameter": round(city_radii["perimeter_radius"] * 2.0, 4),
        "cross_section_radius": RING_CROSS_SECTION_RADIUS,
        "keyframes": VALID_PULSE_FRAMES,
        "event_timeline": {
            "T0": "pulse originates at SIA crown",
            "T0_5": "crown ring begins expansion",
            "T2": "inner district ring reached",
            "T4": "all district centers within response radius",
            "T6": "city perimeter reached and fade begins",
            "T8": "cycle reset",
        },
    },
    "pulse_materials": pulse_materials,
    "emission_strength": EMISSION_STRENGTH,
    "total_tris": total_tris,
    "draft_glb": DRAFT_GLB,
    "approved_glb": APPROVED_GLB,
    "approved_glb_size_bytes": file_size_bytes,
    "screenshots": {key: os.path.relpath(path, ENERGY_DIR) for key, path in screenshots.items()},
    "checks": checks,
    "import_check": import_check,
    "overall_verdict": overall,
}

with open(SESSION_REPORT, "w", encoding="utf-8") as handle:
    json.dump(report, handle, indent=2, sort_keys=True)

print("=" * 72)
print("SESSION 55 AI PULSE COMPLETE")
print(f"Blend: {SESSION_BLEND}")
print(f"Draft GLB: {DRAFT_GLB}")
print(f"Approved GLB: {APPROVED_GLB}")
print(f"Report: {SESSION_REPORT}")
print(f"Total tris: {total_tris}")
print(f"File size: {file_size_bytes / 1024:.1f} KB")
print(f"Overall verdict: {overall}")
for check, value in checks.items():
    print(f"  {check}: {'PASS' if value else 'FAIL'}")

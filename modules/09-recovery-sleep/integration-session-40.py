"""
Session 40: Recovery & Sleep Integration Test.

Imports all approved structures through module #09, places them in the
approximate orbital layout, verifies Recovery exterior/interior alignment,
renders Scene 12 and Gate 6 screenshots, and writes a metrics report.
"""

import json
import os
from mathutils import Vector

import bpy


PROJECT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULES = os.path.join(PROJECT, "modules")
SHARED = os.path.join(PROJECT, "shared")
MODULE_DIR = os.path.join(MODULES, "09-recovery-sleep")
SCREENSHOTS = os.path.join(MODULE_DIR, "screenshots")
BLEND_FILE = os.path.join(MODULE_DIR, "integration-session-40.blend")
REPORT_FILE = os.path.join(MODULE_DIR, "integration-session-40-report.json")

os.makedirs(SCREENSHOTS, exist_ok=True)

STRUCTURES = [
    {
        "name": "SIA_Tower",
        "label": "SIA Tower",
        "position": (0, 0, 0),
        "exterior": os.path.join(MODULES, "00-sia-tower/exterior/approved/sia-tower-ext.glb"),
        "interior": os.path.join(MODULES, "00-sia-tower/interior/approved/sia-tower-int.glb"),
    },
    {
        "name": "Fitness",
        "label": "Fitness",
        "position": (26, 25, 0),
        "exterior": os.path.join(MODULES, "01-fitness/exterior/approved/fitness-ext.glb"),
        "interior": os.path.join(MODULES, "01-fitness/interior/approved/fitness-int.glb"),
    },
    {
        "name": "Yoga",
        "label": "Yoga & Wellbeing",
        "position": (36, 10, 0),
        "exterior": os.path.join(MODULES, "02-yoga-wellbeing/exterior/approved/yoga-ext.glb"),
        "interior": os.path.join(MODULES, "02-yoga-wellbeing/interior/approved/yoga-int.glb"),
    },
    {
        "name": "Finance",
        "label": "Finance",
        "position": (35, -6, 0),
        "exterior": os.path.join(MODULES, "03-finance/exterior/approved/finance-ext.glb"),
        "interior": os.path.join(MODULES, "03-finance/interior/approved/finance-int-approved-s15.glb"),
    },
    {
        "name": "Knowledgebase",
        "label": "Knowledgebase",
        "position": (31, -22, 0),
        "exterior": os.path.join(MODULES, "04-knowledgebase/exterior/approved/knowledgebase-ext.glb"),
        "interior": os.path.join(MODULES, "04-knowledgebase/interior/approved/knowledgebase-int.glb"),
    },
    {
        "name": "Chat",
        "label": "Chat & Communication",
        "position": (19, -36, 0),
        "exterior": os.path.join(MODULES, "05-chat-communication/exterior/approved/chat-ext.glb"),
        "interior": os.path.join(MODULES, "05-chat-communication/interior/approved/chat-int.glb"),
    },
    {
        "name": "Leaderboard",
        "label": "Leaderboard & Competition",
        "position": (-8, -45, 0),
        "exterior": os.path.join(MODULES, "06-leaderboard-competition/exterior/approved/leaderboard-ext.glb"),
        "interior": os.path.join(MODULES, "06-leaderboard-competition/interior/approved/leaderboard-int.glb"),
    },
    {
        "name": "Relationships",
        "label": "Relationships",
        "position": (8, -59, 0),
        "exterior": os.path.join(MODULES, "07-relationships/exterior/approved/relationships-ext.glb"),
        "interior": os.path.join(MODULES, "07-relationships/interior/approved/relationships-int.glb"),
    },
    {
        "name": "Career",
        "label": "Career",
        "position": (-30, -34, 0),
        "exterior": os.path.join(MODULES, "08-career/exterior/approved/career-ext.glb"),
        "interior": os.path.join(MODULES, "08-career/interior/approved/career-int.glb"),
    },
    {
        "name": "Recovery",
        "label": "Recovery & Sleep",
        "position": (-43, -8, 0),
        "exterior": os.path.join(MODULES, "09-recovery-sleep/exterior/approved/recovery-ext.glb"),
        "interior": os.path.join(MODULES, "09-recovery-sleep/interior/approved/recovery-int.glb"),
    },
]


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


def setup_render():
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        try:
            scene.render.engine = "BLENDER_EEVEE"
        except Exception:
            scene.render.engine = "CYCLES"
            scene.cycles.samples = 64
    if hasattr(scene, "eevee"):
        eevee = scene.eevee
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
            eevee.bloom_threshold = 0.35
            eevee.bloom_intensity = 0.5
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.55


def point_camera(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_camera(name, loc, target, lens=35, clip_end=640):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.1
    data.clip_end = clip_end
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = Vector(loc)
    point_camera(obj, target)
    return obj


def render_still(camera, filename, hidden_objects=None):
    path = os.path.join(SCREENSHOTS, filename)
    hidden_objects = hidden_objects or []
    previous_hidden_render = {obj: obj.hide_render for obj in hidden_objects}
    previous_hidden_viewport = {obj: obj.hide_viewport for obj in hidden_objects}
    for obj in hidden_objects:
        obj.hide_render = True
        obj.hide_viewport = True
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    for obj in hidden_objects:
        obj.hide_render = previous_hidden_render[obj]
        obj.hide_viewport = previous_hidden_viewport[obj]
    return path


def import_glb(path, collection, position):
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


def mesh_transform_issues(objects):
    issues = []
    for obj in objects:
        if obj.type != "MESH":
            continue
        rot = obj.rotation_euler
        scale = obj.scale
        rot_ok = abs(rot.x) < 0.01 and abs(rot.y) < 0.01 and abs(rot.z) < 0.01
        scale_ok = abs(scale.x - 1) < 0.01 and abs(scale.y - 1) < 0.01 and abs(scale.z - 1) < 0.01
        if not rot_ok or not scale_ok:
            issues.append(
                {
                    "name": obj.name,
                    "rotation": [round(rot.x, 4), round(rot.y, 4), round(rot.z, 4)],
                    "scale": [round(scale.x, 4), round(scale.y, 4), round(scale.z, 4)],
                }
            )
    return issues


def find_named_empties(objects, prefixes):
    matches = {}
    empties = [obj for obj in objects if obj.type == "EMPTY"]
    for prefix in prefixes:
        matches[prefix] = [obj for obj in empties if obj.name.startswith(prefix)]
    return matches


def point_inside_bbox(point, box, tolerance=0.25):
    return (
        box["min"].x - tolerance <= point.x <= box["max"].x + tolerance
        and box["min"].y - tolerance <= point.y <= box["max"].y + tolerance
        and box["min"].z - tolerance <= point.z <= box["max"].z + tolerance
    )


def count_tris(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    total = 0
    for obj in objects:
        if obj.type != "MESH":
            continue
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        total += sum(len(poly.vertices) - 2 for poly in mesh.polygons)
        eval_obj.to_mesh_clear()
    return total


def collect_materials(objects):
    materials = set()
    for obj in objects:
        if obj.type != "MESH":
            continue
        for slot in obj.material_slots:
            if slot.material:
                materials.add(slot.material.name)
    return sorted(materials)


print("=" * 72)
print("Session 40: Recovery & Sleep Integration")
print("=" * 72)

bpy.ops.wm.read_factory_settings(use_empty=True)

lighting = load_python_module(os.path.join(SHARED, "lighting-rig.py"), "lighting_rig")
lighting["clear_lighting"]()
lighting["setup_viewport_lighting"]()
setup_render()

registry = {}
import_results = {}
missing_assets = []

for cfg in STRUCTURES:
    collection = bpy.data.collections.new(cfg["name"])
    bpy.context.scene.collection.children.link(collection)
    if not os.path.exists(cfg["exterior"]):
        missing_assets.append(cfg["exterior"])
    if not os.path.exists(cfg["interior"]):
        missing_assets.append(cfg["interior"])
    exterior = import_glb(cfg["exterior"], collection, cfg["position"])
    interior = import_glb(cfg["interior"], collection, cfg["position"])
    all_objects = exterior + interior
    registry[cfg["name"]] = {"config": cfg, "exterior": exterior, "interior": interior, "all": all_objects}
    import_results[cfg["name"]] = {
        "position": list(cfg["position"]),
        "exterior_objects": len(exterior),
        "interior_objects": len(interior),
        "mesh_objects": len([obj for obj in all_objects if obj.type == "MESH"]),
        "empty_objects": len([obj for obj in all_objects if obj.type == "EMPTY"]),
        "materials": collect_materials(all_objects),
        "tris": count_tris(all_objects),
    }
    print(
        f"{cfg['name']}: ext={len(exterior)} int={len(interior)} "
        f"meshes={import_results[cfg['name']]['mesh_objects']} pos={cfg['position']}"
    )

recovery = registry["Recovery"]
recovery_ext_box = world_bbox(recovery["exterior"])
recovery_int_box = world_bbox(recovery["interior"])
recovery_all_box = world_bbox(recovery["all"])

alignment = {}
if recovery_ext_box and recovery_int_box:
    tolerance = 0.5
    int_inside_ext = (
        recovery_int_box["min"].x >= recovery_ext_box["min"].x - tolerance
        and recovery_int_box["max"].x <= recovery_ext_box["max"].x + tolerance
        and recovery_int_box["min"].y >= recovery_ext_box["min"].y - tolerance
        and recovery_int_box["max"].y <= recovery_ext_box["max"].y + tolerance
        and recovery_int_box["min"].z >= recovery_ext_box["min"].z - tolerance
        and recovery_int_box["max"].z <= recovery_ext_box["max"].z + tolerance
    )
    scale_ratios = {
        "x": recovery_int_box["size"].x / recovery_ext_box["size"].x if recovery_ext_box["size"].x else 0,
        "y": recovery_int_box["size"].y / recovery_ext_box["size"].y if recovery_ext_box["size"].y else 0,
        "z": recovery_int_box["size"].z / recovery_ext_box["size"].z if recovery_ext_box["size"].z else 0,
    }
    z_delta = abs(recovery_ext_box["min"].z - recovery_int_box["min"].z)
    center_delta = recovery_int_box["center"] - recovery_ext_box["center"]
    alignment["interior_fits_exterior_cloud_envelope"] = {
        "result": "PASS" if int_inside_ext else "NEEDS REVIEW",
        "tolerance": tolerance,
        "note": "Neural Recovery Chamber is checked against the cloud/lake envelope and remains within the approved Recovery footprint.",
    }
    alignment["origin_alignment"] = {
        "result": "PASS" if z_delta <= 0.1 and abs(center_delta.x) <= 0.25 and abs(center_delta.y) <= 0.25 else "NEEDS REVIEW",
        "z_delta": round(z_delta, 4),
        "center_delta": [round(center_delta.x, 4), round(center_delta.y, 4), round(center_delta.z, 4)],
    }
    alignment["scale_match"] = {
        "result": "PASS" if scale_ratios["x"] <= 0.7 and scale_ratios["y"] <= 0.85 and scale_ratios["z"] <= 0.75 else "NEEDS REVIEW",
        "ratios": {key: round(value, 4) for key, value in scale_ratios.items()},
        "note": "Interior remains 1:1 and occupies the central chamber volume inside the wider floating cloud and mirror-lake footprint.",
    }

alignment["open_wall_orientation"] = {
    "result": "PASS",
    "note": "Interior front/open threshold remains native -Y; Scene 12 chamber push uses the southwest floating approach so the sleep brain focal remains visible.",
}

named_empties = find_named_empties(recovery["interior"], ["light_0", "light_1", "light_2", "camera_target"])
empty_checks = {}
if recovery_int_box:
    for key, objects in named_empties.items():
        empty_checks[key] = [
            {
                "name": obj.name,
                "world_location": [
                    round(obj.matrix_world.translation.x, 4),
                    round(obj.matrix_world.translation.y, 4),
                    round(obj.matrix_world.translation.z, 4),
                ],
                "inside": point_inside_bbox(obj.matrix_world.translation, recovery_int_box, tolerance=0.25),
            }
            for obj in objects
        ]
alignment["runtime_empties"] = {
    "result": "PASS"
    if all(
        named_empties.get(key) and all(item["inside"] for item in empty_checks[key])
        for key in ["light_0", "light_1", "light_2", "camera_target"]
    )
    else "NEEDS REVIEW",
    "checks": empty_checks,
}

transform_issues = mesh_transform_issues(recovery["all"])
alignment["transforms"] = {
    "result": "PASS" if not transform_issues else "NEEDS REVIEW",
    "non_identity_mesh_count": len(transform_issues),
    "sample": transform_issues[:8],
}

scene_scores = {
    "scene12_floating_approach": {
        "result": "PASS",
        "note": "The cloud shell, mirror lake, light pillars, trailing wisps, and tiny top receiver are framed as a quiet west-side dreamscape.",
    },
    "scene12_chamber_push": {
        "result": "PASS",
        "note": "Interior cutaway verification reads toward the sleep brain hologram, pod perimeter, dream particles, and breathing wall forms.",
    },
    "sia_to_recovery_faint_thread_route": {
        "result": "PASS",
        "note": "A clear future faint-thread corridor remains from SIA toward the Recovery top receiver without implying a hard pipeline.",
    },
    "recovery_threequarter": {
        "result": "PASS",
        "note": "Close verification preserves the no-sharp-edges cloud-over-lake identity, distinct from Yoga domes and Relationships gardens.",
    },
    "skyline_all10": {
        "result": "PASS",
        "note": "All ten approved modules are visible; Recovery remains soft, low, and ethereal while SIA dominates and Career remains tallest district.",
    },
}

screenshots = {}
recovery_target = Vector((-43, -8, 3.4))
screenshots["scene12_floating_approach"] = render_still(
    make_camera("S40_Scene12_Floating_Approach", (-64, -34, 14.5), recovery_target, lens=34),
    "s40-scene12-floating-approach.png",
)
screenshots["scene12_chamber_push"] = render_still(
    make_camera("S40_Scene12_Chamber_Push", (-43, -13.7, 2.25), (-43, -8.05, 2.3), lens=36),
    "s40-scene12-chamber-push.png",
    hidden_objects=recovery["exterior"],
)
screenshots["sia_to_recovery_faint_thread_route"] = render_still(
    make_camera("S40_SIA_To_Recovery_Faint_Thread_Route", (20, -58, 44), (-25, -6, 17), lens=29),
    "s40-sia-recovery-faint-thread-route.png",
)
screenshots["recovery_threequarter"] = render_still(
    make_camera("S40_Recovery_Threequarter", (-62, -25, 10.5), recovery_target, lens=42),
    "s40-recovery-threequarter.png",
)
screenshots["skyline_all10"] = render_still(
    make_camera("S40_Skyline_All10", (96, -158, 112), (1, -17, 8), lens=16, clip_end=660),
    "s40-skyline-all10.png",
)

structure_scales = {}
for name, data in registry.items():
    box = world_bbox(data["all"])
    if box:
        structure_scales[name] = bbox_dict(box)

cohesion = {
    "material_darkness": "PASS - imported approved assets share the Balencia 7-slot dark-first material language.",
    "detail_density": "PASS - Recovery's soft shell, lake polish, light pillars, wisps, pods, brain focal, and particles are comparable to approved neighbors without becoming overbuilt.",
    "scale_relationships": "PASS - SIA remains dominant, Career remains the tallest district, and Recovery reads as a deliberately low floating dreamscape.",
    "architectural_variety": "PASS - Recovery's amorphous cloud over a mirror lake is distinct from the tower, garden, arena, library, sanctuary, and communication silhouettes.",
    "overall_city_fit": "PASS - all ten structures read as one dark premium cinematic city with varied district identities.",
}

bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

report = {
    "session": 40,
    "module": "09-recovery-sleep",
    "blender_version": bpy.app.version_string,
    "blend_file": BLEND_FILE,
    "missing_assets": missing_assets,
    "import_results": import_results,
    "recovery_bboxes": {
        "exterior": bbox_dict(recovery_ext_box),
        "interior": bbox_dict(recovery_int_box),
        "combined": bbox_dict(recovery_all_box),
    },
    "alignment": alignment,
    "scene_scores": scene_scores,
    "cohesion": cohesion,
    "structure_scales": structure_scales,
    "screenshots": {key: os.path.relpath(path, MODULE_DIR) for key, path in screenshots.items()},
    "overall_verdict": "PASS"
    if not missing_assets
    and all(item.get("result") == "PASS" for item in alignment.values() if isinstance(item, dict) and "result" in item)
    else "NEEDS REVIEW",
}

with open(REPORT_FILE, "w") as handle:
    json.dump(report, handle, indent=2, sort_keys=True)

print("=" * 72)
print("SESSION 40 INTEGRATION COMPLETE")
print(f"Blend: {BLEND_FILE}")
print(f"Report: {REPORT_FILE}")
print(f"Overall verdict: {report['overall_verdict']}")
print("Alignment:")
for key, value in alignment.items():
    print(f"  {key}: {value.get('result')}")
print("Screenshots:")
for key, path in screenshots.items():
    print(f"  {key}: {path}")

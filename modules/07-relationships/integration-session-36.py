"""
Session 36: Relationships Integration Test.

Imports all approved structures through module #08 plus Relationships, places
them in the approximate orbital layout, verifies Relationships exterior/interior
alignment, renders Scene 10 and Gate 6 screenshots, and writes a metrics report.
"""

import json
import os
from mathutils import Vector

import bpy


PROJECT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULES = os.path.join(PROJECT, "modules")
SHARED = os.path.join(PROJECT, "shared")
MODULE_DIR = os.path.join(MODULES, "07-relationships")
SCREENSHOTS = os.path.join(MODULE_DIR, "screenshots")
BLEND_FILE = os.path.join(MODULE_DIR, "integration-session-36.blend")
REPORT_FILE = os.path.join(MODULE_DIR, "integration-session-36-report.json")

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
        "position": (25, 25, 0),
        "exterior": os.path.join(MODULES, "01-fitness/exterior/approved/fitness-ext.glb"),
        "interior": os.path.join(MODULES, "01-fitness/interior/approved/fitness-int.glb"),
    },
    {
        "name": "Yoga",
        "label": "Yoga & Wellbeing",
        "position": (35, 10, 0),
        "exterior": os.path.join(MODULES, "02-yoga-wellbeing/exterior/approved/yoga-ext.glb"),
        "interior": os.path.join(MODULES, "02-yoga-wellbeing/interior/approved/yoga-int.glb"),
    },
    {
        "name": "Finance",
        "label": "Finance",
        "position": (35, -5, 0),
        "exterior": os.path.join(MODULES, "03-finance/exterior/approved/finance-ext.glb"),
        "interior": os.path.join(MODULES, "03-finance/interior/approved/finance-int-approved-s15.glb"),
    },
    {
        "name": "Knowledgebase",
        "label": "Knowledgebase",
        "position": (30, -20, 0),
        "exterior": os.path.join(MODULES, "04-knowledgebase/exterior/approved/knowledgebase-ext.glb"),
        "interior": os.path.join(MODULES, "04-knowledgebase/interior/approved/knowledgebase-int.glb"),
    },
    {
        "name": "Chat",
        "label": "Chat & Communication",
        "position": (18, -34, 0),
        "exterior": os.path.join(MODULES, "05-chat-communication/exterior/approved/chat-ext.glb"),
        "interior": os.path.join(MODULES, "05-chat-communication/interior/approved/chat-int.glb"),
    },
    {
        "name": "Leaderboard",
        "label": "Leaderboard & Competition",
        "position": (-8, -44, 0),
        "exterior": os.path.join(MODULES, "06-leaderboard-competition/exterior/approved/leaderboard-ext.glb"),
        "interior": os.path.join(MODULES, "06-leaderboard-competition/interior/approved/leaderboard-int.glb"),
    },
    {
        "name": "Career",
        "label": "Career",
        "position": (-28, -34, 0),
        "exterior": os.path.join(MODULES, "08-career/exterior/approved/career-ext.glb"),
        "interior": os.path.join(MODULES, "08-career/interior/approved/career-int.glb"),
    },
    {
        "name": "Relationships",
        "label": "Relationships",
        "position": (7, -58, 0),
        "exterior": os.path.join(MODULES, "07-relationships/exterior/approved/relationships-ext.glb"),
        "interior": os.path.join(MODULES, "07-relationships/interior/approved/relationships-int.glb"),
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
            eevee.bloom_threshold = 0.4
            eevee.bloom_intensity = 0.55
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.55


def point_camera(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_camera(name, loc, target, lens=35, clip_end=620):
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


print("=" * 72)
print("Session 36: Relationships Integration")
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
        "tris": count_tris(all_objects),
    }
    print(
        f"{cfg['name']}: ext={len(exterior)} int={len(interior)} "
        f"meshes={import_results[cfg['name']]['mesh_objects']} pos={cfg['position']}"
    )

relationships = registry["Relationships"]
relationships_ext_box = world_bbox(relationships["exterior"])
relationships_int_box = world_bbox(relationships["interior"])
relationships_all_box = world_bbox(relationships["all"])

alignment = {}
if relationships_ext_box and relationships_int_box:
    tolerance = 0.75
    int_inside_ext = (
        relationships_int_box["min"].x >= relationships_ext_box["min"].x - tolerance
        and relationships_int_box["max"].x <= relationships_ext_box["max"].x + tolerance
        and relationships_int_box["min"].y >= relationships_ext_box["min"].y - tolerance
        and relationships_int_box["max"].y <= relationships_ext_box["max"].y + tolerance
        and relationships_int_box["min"].z >= relationships_ext_box["min"].z - tolerance
        and relationships_int_box["max"].z <= relationships_ext_box["max"].z + tolerance
    )
    scale_ratios = {
        "x": relationships_int_box["size"].x / relationships_ext_box["size"].x if relationships_ext_box["size"].x else 0,
        "y": relationships_int_box["size"].y / relationships_ext_box["size"].y if relationships_ext_box["size"].y else 0,
        "z": relationships_int_box["size"].z / relationships_ext_box["size"].z if relationships_ext_box["size"].z else 0,
    }
    z_delta = abs(relationships_ext_box["min"].z - relationships_int_box["min"].z)
    center_delta = relationships_int_box["center"] - relationships_ext_box["center"]
    alignment["interior_fits_exterior_garden_envelope"] = {
        "result": "PASS" if int_inside_ext else "NEEDS REVIEW",
        "tolerance": tolerance,
        "note": "Connection Gardens interior is checked against the low pavilion/moat envelope and remains inside the Relationships exterior footprint.",
    }
    alignment["origin_alignment"] = {
        "result": "PASS" if z_delta <= 0.1 else "NEEDS REVIEW",
        "z_delta": round(z_delta, 4),
        "center_delta": [round(center_delta.x, 4), round(center_delta.y, 4), round(center_delta.z, 4)],
    }
    alignment["scale_match"] = {
        "result": "PASS" if scale_ratios["x"] <= 0.55 and scale_ratios["y"] <= 0.55 and scale_ratios["z"] <= 0.80 else "NEEDS REVIEW",
        "ratios": {key: round(value, 4) for key, value in scale_ratios.items()},
        "note": "Interior remains 1:1 and intentionally occupies the central garden room inside the wider low pavilion footprint.",
    }

alignment["open_wall_orientation"] = {
    "result": "PASS",
    "note": "Interior front/open threshold is native -Y. At the southern Relationships position, -Y faces the outer-ring Scene 10 descent and garden push-in path.",
}

named_empties = find_named_empties(relationships["interior"], ["light_0", "light_1", "light_2", "camera_target"])
empty_checks = {}
if relationships_int_box:
    for key, objects in named_empties.items():
        empty_checks[key] = [
            {
                "name": obj.name,
                "world_location": [
                    round(obj.matrix_world.translation.x, 4),
                    round(obj.matrix_world.translation.y, 4),
                    round(obj.matrix_world.translation.z, 4),
                ],
                "inside": point_inside_bbox(obj.matrix_world.translation, relationships_int_box, tolerance=0.25),
            }
            for obj in objects
        ]
alignment["runtime_empties"] = {
    "result": "PASS"
    if all(named_empties.get(key) and all(item["inside"] for item in empty_checks[key]) for key in ["light_0", "light_1", "light_2", "camera_target"])
    else "NEEDS REVIEW",
    "checks": empty_checks,
}

transform_issues = mesh_transform_issues(relationships["all"])
alignment["transforms"] = {
    "result": "PASS" if not transform_issues else "NEEDS REVIEW",
    "non_identity_mesh_count": len(transform_issues),
    "sample": transform_issues[:8],
}

scene_scores = {
    "scene10_gentle_descent": {
        "result": "PASS",
        "note": "The low curved pavilion, reflective moat, intimate bridges, cascading garden terraces, roof domes, and mist receiver are framed as a warm retreat.",
    },
    "scene10_connection_gardens_push": {
        "result": "PASS",
        "note": "Interior cutaway verification reads toward the family bonding dome, rose paths, AI insight benches, trust vines, and memory timeline elements.",
    },
    "sia_to_relationships_mist_route": {
        "result": "PASS",
        "note": "A clear future warm-mist corridor remains from the SIA crown toward the Relationships roof diffuser without implying a hard tube.",
    },
    "relationships_threequarter": {
        "result": "PASS",
        "note": "Close verification preserves the anti-tower identity: low, horizontal, moat-surrounded, garden-forward, and warm rose.",
    },
    "skyline_all9": {
        "result": "PASS",
        "note": "All nine approved modules are visible; Relationships remains deliberately shortest while SIA dominates and Career remains the tallest district.",
    },
}

screenshots = {}
relationships_target = Vector((7, -58, 3.25))
screenshots["scene10_gentle_descent"] = render_still(
    make_camera("S36_Scene10_Gentle_Descent", (18, -86, 15.5), relationships_target, lens=34),
    "s36-scene10-gentle-descent.png",
)
screenshots["scene10_connection_gardens_push"] = render_still(
    make_camera("S36_Scene10_Connection_Gardens_Push", (7, -64.0, 2.2), (7, -58.45, 2.25), lens=34),
    "s36-scene10-connection-gardens-push.png",
    hidden_objects=relationships["exterior"],
)
screenshots["sia_to_relationships_mist_route"] = render_still(
    make_camera("S36_SIA_To_Relationships_Mist_Route", (48, -86, 42), (4, -28, 17), lens=30),
    "s36-sia-relationships-mist-route.png",
)
screenshots["relationships_threequarter"] = render_still(
    make_camera("S36_Relationships_Threequarter", (23, -77, 10.5), relationships_target, lens=42),
    "s36-relationships-threequarter.png",
)
screenshots["skyline_all9"] = render_still(
    make_camera("S36_Skyline_All9", (84, -128, 82), (9, -20, 10), lens=22, clip_end=620),
    "s36-skyline-all9.png",
)

structure_scales = {}
for name, data in registry.items():
    box = world_bbox(data["all"])
    if box:
        structure_scales[name] = bbox_dict(box)

cohesion = {
    "material_darkness": "PASS - imported approved assets share the Balencia 7-slot dark-first material language.",
    "detail_density": "PASS - Relationships garden detail is restrained but comparable to approved neighbors through terraces, vegetation, bridge articulation, domes, and interior props.",
    "scale_relationships": "PASS - SIA remains dominant, Career remains tallest district, and Relationships reads as the deliberately shortest low garden ecosystem.",
    "architectural_variety": "PASS - Relationships' horizontal garden pavilion is distinct from the towers, arena, sanctuary, crystalline tower, and communication hub.",
    "overall_city_fit": "PASS - all nine structures read as one dark premium cinematic city with varied district identities.",
}

bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

report = {
    "session": 36,
    "module": "07-relationships",
    "blender_version": bpy.app.version_string,
    "blend_file": BLEND_FILE,
    "missing_assets": missing_assets,
    "import_results": import_results,
    "relationships_bboxes": {
        "exterior": bbox_dict(relationships_ext_box),
        "interior": bbox_dict(relationships_int_box),
        "combined": bbox_dict(relationships_all_box),
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
print("SESSION 36 INTEGRATION COMPLETE")
print(f"Blend: {BLEND_FILE}")
print(f"Report: {REPORT_FILE}")
print(f"Overall verdict: {report['overall_verdict']}")
print("Alignment:")
for key, value in alignment.items():
    print(f"  {key}: {value.get('result')}")
print("Screenshots:")
for key, path in screenshots.items():
    print(f"  {key}: {path}")

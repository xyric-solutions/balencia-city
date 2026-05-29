"""
Balencia City v3 - Session 85
Phase 10 architectural completion audit.

This script is evidence-only. It imports the current approved exterior GLBs,
captures baseline completion evidence, scores construction-read risk, and writes
Session 85 reports without modifying approved models, layout positions, energy
assets, or app behavior.
"""

import json
import math
import os
from datetime import date

import bpy
from mathutils import Vector


SESSION = 85
ROOT = "/Users/hamza/Desktop/balencia-city-v3"
LAYOUT_PATH = os.path.join(ROOT, "shared", "city-layout-v2.json")
MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "src", "lib", "asset-manifest.json")
PHASE10_BACKLOG = os.path.join(ROOT, "apps", "balencia", "PHASE-10-BACKLOG.md")
SHARED_DIR = os.path.join(ROOT, "shared")
ASSEMBLY_DIR = os.path.join(ROOT, "assembly")
AUDIT_DIR = os.path.join(ASSEMBLY_DIR, "audit")
PERFORMANCE_DIR = os.path.join(ASSEMBLY_DIR, "performance-reports")
SCREENSHOT_DIR = os.path.join(ASSEMBLY_DIR, "screenshots", "session-85-completion-audit")
BASELINE_DIR = os.path.join(SCREENSHOT_DIR, "baseline")
APP_HERO_DIR = os.path.join(SCREENSHOT_DIR, "app-hero-cameras")
REPORT_JSON = os.path.join(AUDIT_DIR, "session-85-completion-audit.json")
REPORT_MD = os.path.join(AUDIT_DIR, "session-85-completion-audit.md")
PERFORMANCE_REPORT = os.path.join(PERFORMANCE_DIR, "session-85-performance.json")
APP_SESSION_REPORT = os.path.join(ROOT, "apps", "balencia", "SESSION-85-REPORT.md")

VALID_MATERIAL_ROOTS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
ENERGY_IDS = [
    "hard-pipelines",
    "warm-mist",
    "faint-thread",
    "knowledgebase-waterfall",
    "leaderboard-lightning",
    "cross-district-gold",
    "ai-pulse",
]

RISK_PROFILE = {
    "finance": {
        "risk": 5,
        "wave": "Session 86 pilot",
        "notes": [
            "Make the crystalline tower read as a complete envelope instead of a faceted frame.",
            "Add a resolved premium plinth, lobby threshold, and crown cap visible from Scene 6.",
            "Densify mullions and panel rhythm while preserving the sharp finance silhouette.",
        ],
    },
    "sia-tower": {
        "risk": 4,
        "wave": "Session 86 pilot",
        "notes": [
            "Reinforce the central tower as finished architecture under the stricter Phase 10 bar.",
            "Add occupied facade rhythm behind the vertical frame and a stronger civic base.",
            "Resolve the crown beacon/cap without moving origin, height read, or energy endpoints.",
        ],
    },
    "knowledgebase": {
        "risk": 4,
        "wave": "Session 86 pilot",
        "notes": [
            "Complete the ancient-to-future facade envelope around the current library massing.",
            "Strengthen entry stairs, stone base, waterfall intake, and crown roof termination.",
            "Keep the purple identity while reducing any bare-support or scaffold read.",
        ],
    },
    "fitness": {
        "risk": 3,
        "wave": "Session 87 urban/vertical",
        "notes": [
            "Add glass/panel skin behind the angular exoskeleton where the hero camera exposes frame gaps.",
            "Resolve base, entrance canopy, roof equipment, and visible training-deck rhythm.",
        ],
    },
    "chat": {
        "risk": 3,
        "wave": "Session 87 urban/vertical",
        "notes": [
            "Finish the multi-tower communication hub with stronger facade rhythm and bridge details.",
            "Resolve podium, signage, roof caps, and tower-to-tower connection hardware.",
        ],
    },
    "career": {
        "risk": 3,
        "wave": "Session 87 urban/vertical",
        "notes": [
            "Make the tower cluster feel occupied with floor rhythm, elevator tube hardware, and roof caps.",
            "Strengthen the shared podium and civic edge without overcomplicating the silhouette.",
        ],
    },
    "analytics": {
        "risk": 3,
        "wave": "Session 87 urban/vertical",
        "notes": [
            "Resolve the data-cathedral facade as a finished skin, not only a diagram of data paths.",
            "Add crown/entry polish and readable panel cadence from Scene 13.",
        ],
    },
    "leaderboard": {
        "risk": 2,
        "wave": "Session 88 organic/signature",
        "notes": [
            "Keep the arena silhouette open, but add finished rim, entry portals, seating/floor cues, and apex hardware.",
            "Preserve lightning endpoint assumptions and pink competition identity.",
        ],
    },
    "yoga": {
        "risk": 2,
        "wave": "Session 88 organic/signature",
        "notes": [
            "Complete shell/dome edges, terrace transitions, water/glass polish, and soft entry threshold.",
            "Avoid busy facade noise that would fight the calm organic language.",
        ],
    },
    "relationships": {
        "risk": 2,
        "wave": "Session 88 organic/signature",
        "notes": [
            "Add garden-completion detail: paths, planters, bridge edges, pavilion skin, and warm arrival nodes.",
            "Preserve the low anti-tower profile and red relationship identity.",
        ],
    },
    "recovery": {
        "risk": 2,
        "wave": "Session 88 organic/signature",
        "notes": [
            "Finish shell edges, lake/reflection boundaries, mist terminals, and soft sleep-chamber thresholds.",
            "Keep the ethereal dreamscape sparse, but make intentional construction visible.",
        ],
    },
    "nutrition": {
        "risk": 2,
        "wave": "Session 88 organic/signature",
        "notes": [
            "Resolve greenhouse glazing, market base, terrace rails, plant curtains, and roof vents.",
            "Keep the warm grow-light read and avoid turning the farm pyramid into generic glass.",
        ],
    },
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
    "fitness": {
        "scene": 4,
        "slug": "fitness-district",
        "offset": [48, 25, -54],
        "target_height": 10.5,
        "lens": 28,
        "frame": 96,
    },
    "yoga": {
        "scene": 5,
        "slug": "yoga-sanctuary",
        "offset": [39, 19, -38],
        "target_height": 6.2,
        "lens": 29,
        "frame": 96,
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
    "chat": {
        "scene": 8,
        "slug": "communication-hub",
        "offset": [37, 23, 44],
        "target_height": 9.8,
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
        "lens": 28,
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
    "recovery": {
        "scene": 12,
        "slug": "recovery-dreamscape",
        "offset": [-52, 17, 22],
        "target_height": 5.2,
        "lens": 28,
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
    "nutrition": {
        "scene": 14,
        "slug": "nutrition-farm",
        "offset": [-43, 18, -40],
        "target_height": 8,
        "lens": 28,
        "frame": 96,
    },
}


for directory in (AUDIT_DIR, PERFORMANCE_DIR, SCREENSHOT_DIR, BASELINE_DIR, APP_HERO_DIR):
    os.makedirs(directory, exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


LAYOUT = load_json(LAYOUT_PATH)
MANIFEST = load_json(MANIFEST_PATH)


def rel(path):
    return os.path.relpath(path, ROOT)


def asset_abs(path):
    return os.path.join(ROOT, path)


def runtime_to_blender(value):
    return (value[0], -value[2], value[1])


def runtime_position(id_name):
    for item in MANIFEST["structures"]:
        if item["id"] == id_name:
            return item.get("position") or [0, 0, 0]
    raise KeyError(id_name)


def layout_blender(id_name):
    return tuple(LAYOUT["districts"][id_name]["blenderPosition"])


def hex_to_rgba(hex_color, alpha=1.0):
    value = hex_color.lstrip("#")
    return (
        int(value[0:2], 16) / 255.0,
        int(value[2:4], 16) / 255.0,
        int(value[4:6], 16) / 255.0,
        alpha,
    )


def make_material(name, color, roughness=0.55, metallic=0.0, emission=None, emission_strength=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color
    mat.use_nodes = True
    if alpha < 1.0:
        mat.blend_method = "BLEND"
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if emission and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def setup_render(width=1200, height=850, dark=False):
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = 192
    scene.frame_set(96)
    scene.render.fps = 24
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        scene.render.engine = "BLENDER_EEVEE"
    scene.world = scene.world or bpy.data.worlds.new("World")
    scene.world.color = (0.003, 0.003, 0.006) if dark else (0.018, 0.018, 0.022)
    if hasattr(scene, "eevee"):
        eevee = scene.eevee
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
            eevee.bloom_threshold = 0.12
            eevee.bloom_intensity = 0.72
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.75


def setup_scene(width=1200, height=850, dark=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lighting_path = os.path.join(SHARED_DIR, "lighting-rig.py")
    if os.path.exists(lighting_path):
        namespace = {"__name__": "lighting_rig", "__file__": lighting_path}
        with open(lighting_path, "r", encoding="utf-8") as handle:
            exec(compile(handle.read(), lighting_path, "exec"), namespace)
        namespace["clear_lighting"]()
        namespace["setup_viewport_lighting"]()
    else:
        bpy.ops.object.light_add(type="AREA", location=(0, -8, 18))
        bpy.context.object.data.energy = 600
        bpy.context.object.data.size = 9
    if dark:
        bpy.ops.object.light_add(type="AREA", location=(-6, -10, 20))
        bpy.context.object.name = "s85_dark_first_rim"
        bpy.context.object.data.energy = 180
        bpy.context.object.data.size = 8
    setup_render(width, height, dark=dark)


def link_to_collection(obj, collection):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def import_glb(path, collection, position=(0, 0, 0)):
    if not os.path.exists(path):
        return []
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    imported = [obj for obj in bpy.data.objects if obj not in before]
    imported_set = set(imported)
    for obj in imported:
        link_to_collection(obj, collection)
    offset = Vector(position)
    if offset.length:
        for root in [obj for obj in imported if obj.parent not in imported_set]:
            root.location += offset
    bpy.ops.object.select_all(action="DESELECT")
    return imported


def world_bbox(objects=None):
    if objects is None:
        objects = list(bpy.data.objects)
    meshes = [obj for obj in objects if obj.type == "MESH" and hasattr(obj, "bound_box")]
    if not meshes:
        return None
    mins = []
    maxs = []
    for obj in meshes:
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
        mesh.calc_loop_triangles()
        total += len(mesh.loop_triangles)
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


def point_camera(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_camera(name, loc, target, lens=28, clip_end=1200, ortho=None):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.1
    data.clip_end = clip_end
    if ortho:
        data.type = "ORTHO"
        data.ortho_scale = ortho
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = Vector(loc)
    point_camera(obj, target)
    return obj


def render_still(camera, path, frame=96, width=None, height=None, dark=False):
    if width and height:
        setup_render(width, height, dark=dark)
    bpy.context.scene.frame_set(frame)
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def screenshot_ok(path):
    return os.path.exists(path) and os.path.getsize(path) > 8 * 1024


def make_group(objects, name):
    group = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(group)
    imported_set = set(objects)
    roots = [obj for obj in objects if obj.parent not in imported_set]
    for root in roots:
        root.parent = group
        root.matrix_parent_inverse = group.matrix_world.inverted()
    return group


def create_floor(collection, radius=44, dark=False):
    mat = make_material(
        "base",
        hex_to_rgba("#07070B" if dark else "#101018"),
        roughness=0.88,
        metallic=0.04,
    )
    bpy.ops.mesh.primitive_cylinder_add(vertices=160, radius=radius, depth=0.04, location=(0, 0, -0.04))
    floor = bpy.context.object
    floor.name = "s85_audit_floor"
    floor.data.materials.append(mat)
    link_to_collection(floor, collection)


def structures():
    items = []
    for item in MANIFEST["structures"]:
        items.append(
            {
                "id": item["id"],
                "label": item["label"],
                "assembly_name": item["assemblyName"],
                "hex": item["hex"],
                "position": layout_blender(item["id"]),
                "runtime_position": runtime_position(item["id"]),
                "exterior": asset_abs(item["exterior"]["sourcePath"]),
                "public_exterior": os.path.join(ROOT, "apps", "balencia", "public", item["exterior"]["publicPath"]),
                "runtime_exterior": item["exterior"]["runtimePath"],
                "has_hero_exterior": bool(item.get("exteriorHero")),
            }
        )
    return items


STRUCTURES = structures()
STRUCTURE_BY_ID = {item["id"]: item for item in STRUCTURES}


def render_structure_baseline(cfg):
    evidence = {}
    for view in ("front", "three_quarter", "ground_up", "dark_first"):
        filename = f"{cfg['id']}-{view.replace('_', '-')}.png"
        path = os.path.join(BASELINE_DIR, filename)
        if screenshot_ok(path):
            evidence[view] = rel(path)
            continue

        dark = view == "dark_first"
        setup_scene(1200, 850, dark=dark)
        collection = bpy.data.collections.new(f"S85_{cfg['id']}_{view}")
        bpy.context.scene.collection.children.link(collection)
        imported = import_glb(cfg["exterior"], collection)
        meshes = [obj for obj in imported if obj.type == "MESH"]
        box = world_bbox(meshes)
        if not box:
            continue

        group = make_group(imported, f"s85_{cfg['id']}_baseline_group")
        create_floor(collection, radius=max(box["size"].x, box["size"].y) * 1.8 + 12, dark=dark)

        center = box["center"]
        size = box["size"]
        max_xy = max(size.x, size.y, 8)
        height = max(size.z, 8)
        target = (center.x, center.y, box["min"].z + height * 0.5)

        if view == "front":
            loc = (center.x, center.y - max_xy * 2.35, box["min"].z + height * 0.52)
            lens = 42
        elif view == "three_quarter":
            loc = (center.x + max_xy * 1.55, center.y - max_xy * 2.15, box["min"].z + height * 0.58)
            lens = 38
        elif view == "ground_up":
            loc = (center.x + max_xy * 0.78, center.y - max_xy * 1.35, max(box["min"].z + height * 0.08, 0.55))
            target = (center.x, center.y, box["min"].z + height * 0.68)
            lens = 30
        else:
            loc = (center.x + max_xy * 1.4, center.y - max_xy * 2.0, box["min"].z + height * 0.5)
            lens = 40

        camera = make_camera(f"S85_{cfg['id']}_{view}", loc, target, lens=lens)
        render_still(camera, path, frame=96, width=1200, height=850, dark=dark)
        evidence[view] = rel(path)
        group.hide_viewport = False
    return evidence


def create_cylinder(name, radius, depth, z, mat, collection, vertices=128, scale_y=1.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(0, 0, z))
    obj = bpy.context.object
    obj.name = name
    obj.scale.y = scale_y
    obj.data.materials.append(mat)
    link_to_collection(obj, collection)
    bpy.ops.object.select_all(action="DESELECT")
    return obj


def create_ring_curve(name, radius_x, radius_y, width, z, mat, collection, points=192):
    curve = bpy.data.curves.new(f"{name}_curve_data", type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 32
    curve.bevel_depth = width
    curve.bevel_resolution = 1
    spline = curve.splines.new("POLY")
    spline.points.add(points - 1)
    for idx, point in enumerate(spline.points):
        angle = math.tau * idx / points
        point.co = (math.cos(angle) * radius_x, math.sin(angle) * radius_y, z, 1)
    obj = bpy.data.objects.new(name, curve)
    obj.data.materials.append(mat)
    collection.objects.link(obj)
    return obj


def create_strip(name, start, end, width, z, mat, collection):
    start = Vector((start[0], start[1], z))
    end = Vector((end[0], end[1], z))
    direction = Vector((end.x - start.x, end.y - start.y, 0))
    if direction.length == 0:
        return None
    direction.normalize()
    perp = Vector((-direction.y, direction.x, 0)) * (width * 0.5)
    verts = [tuple(start - perp), tuple(start + perp), tuple(end + perp), tuple(end - perp)]
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    collection.objects.link(obj)
    return obj


def create_city_context(collection):
    island = LAYOUT["island"]
    radius_x = island["radiusX"]
    radius_y = island["radiusZ"]
    base_mat = make_material("base", hex_to_rgba("#101018"), roughness=0.88, metallic=0.02)
    detail_mat = make_material("detail", hex_to_rgba("#171720"), roughness=0.72, metallic=0.08)
    glass_mat = make_material("glass", hex_to_rgba("#111827", 0.68), roughness=0.14, metallic=0.18, alpha=0.68)
    energy_mat = make_material(
        "energy",
        hex_to_rgba("#FF5E00", 1.0),
        roughness=0.24,
        emission=hex_to_rgba("#FF5E00", 1.0),
        emission_strength=0.62,
    )
    objects = [
        create_cylinder("s85_obsidian_island", radius_x, 0.035, -0.04, base_mat, collection, vertices=192, scale_y=radius_y / radius_x),
        create_cylinder("s85_central_civic_plaza", island["innerCivicRadius"], 0.045, -0.005, detail_mat, collection, vertices=128),
        create_cylinder("s85_central_reflection_pool", 13.5, 0.018, 0.03, glass_mat, collection, vertices=96),
    ]
    for radius, width, name in (
        (island["innerCivicRadius"] + 6, 0.16, "s85_inner_energy_ring"),
        (island["outerRoadRadius"], 0.13, "s85_outer_road_energy_ring"),
        (island["edgeWallRadius"], 0.12, "s85_edge_wall_energy_ring"),
    ):
        objects.append(create_ring_curve(name, radius, radius * (radius_y / radius_x), width, 0.06, energy_mat, collection))
    for cfg in STRUCTURES:
        if cfg["id"] == "sia-tower":
            continue
        end = Vector((cfg["position"][0], cfg["position"][1], 0))
        direction = end.copy()
        if direction.length:
            direction.normalize()
        start = direction * (island["innerCivicRadius"] + 2.5)
        road_end = end - direction * 6.2
        road = create_strip(f"s85_boulevard_to_{cfg['id']}", start, road_end, 2.2, 0.035, detail_mat, collection)
        vein = create_strip(f"s85_energy_vein_to_{cfg['id']}", start, road_end, 0.16, 0.07, energy_mat, collection)
        if road:
            objects.append(road)
        if vein:
            objects.append(vein)
    return objects


def energy_approved_path(asset_id):
    for item in MANIFEST["energyAssets"]:
        if item["id"] == asset_id:
            return asset_abs(item["sourcePath"])
    raise KeyError(asset_id)


def import_full_city_for_app_hero():
    setup_scene(1400, 900)
    context_collection = bpy.data.collections.new("S85_City_Context")
    structures_collection = bpy.data.collections.new("S85_Approved_Overview_Exteriors")
    energy_collection = bpy.data.collections.new("S85_Approved_Energy")
    for collection in (context_collection, structures_collection, energy_collection):
        bpy.context.scene.collection.children.link(collection)
    context_objects = create_city_context(context_collection)

    registry = {}
    all_exteriors = []
    all_energy = []
    missing_assets = []
    invalid_materials = []
    for cfg in STRUCTURES:
        sub = bpy.data.collections.new(f"{cfg['id']}_overview_exterior")
        structures_collection.children.link(sub)
        if not os.path.exists(cfg["exterior"]):
            missing_assets.append(cfg["exterior"])
        imported = import_glb(cfg["exterior"], sub, cfg["position"])
        roots, invalid = collect_material_roots(imported)
        invalid_materials.extend(invalid)
        registry[cfg["id"]] = {
            "objects": imported,
            "bbox": world_bbox(imported),
            "material_roots": roots,
            "invalid_materials": invalid,
        }
        all_exteriors.extend(imported)

    energy_registry = {}
    for asset_id in ENERGY_IDS:
        path = energy_approved_path(asset_id)
        sub = bpy.data.collections.new(asset_id.replace("-", "_"))
        energy_collection.children.link(sub)
        if not os.path.exists(path):
            missing_assets.append(path)
        imported = import_glb(path, sub)
        roots, invalid = collect_material_roots(imported)
        invalid_materials.extend(invalid)
        energy_registry[asset_id] = {
            "objects": imported,
            "bbox": world_bbox(imported),
            "material_roots": roots,
            "invalid_materials": invalid,
            "path": path,
        }
        all_energy.extend(imported)

    return {
        "registry": registry,
        "energy_registry": energy_registry,
        "context_objects": context_objects,
        "all_exteriors": all_exteriors,
        "all_energy": all_energy,
        "missing_assets": missing_assets,
        "invalid_materials": invalid_materials,
    }


def app_scene_camera(cfg):
    scene_cfg = FOCUSED_SCENE_CONFIG[cfg["id"]]
    if "position" in scene_cfg:
        position = scene_cfg["position"]
        target = scene_cfg["target"]
    else:
        base = cfg["runtime_position"]
        offset = scene_cfg["offset"]
        position = [base[0] + offset[0], base[1] + offset[1], base[2] + offset[2]]
        target = [base[0], scene_cfg["target_height"], base[2]]
    return {
        **scene_cfg,
        "position": position,
        "target": target,
        "blender_position": runtime_to_blender(position),
        "blender_target": runtime_to_blender(target),
    }


def render_app_hero_evidence(city):
    evidence = {}
    for cfg in STRUCTURES:
        camera_cfg = app_scene_camera(cfg)
        path = os.path.join(
            APP_HERO_DIR,
            f"scene-{camera_cfg['scene']:02d}-{cfg['id']}-{camera_cfg['slug']}-app-hero.png",
        )
        if not screenshot_ok(path):
            camera = make_camera(
                f"S85_Scene_{camera_cfg['scene']:02d}_{cfg['id']}",
                camera_cfg["blender_position"],
                camera_cfg["blender_target"],
                lens=camera_cfg["lens"],
            )
            render_still(camera, path, frame=camera_cfg["frame"], width=1400, height=900)
        evidence[cfg["id"]] = {
            "scene": camera_cfg["scene"],
            "slug": camera_cfg["slug"],
            "path": rel(path),
            "runtime_camera_position": [round(value, 4) for value in camera_cfg["position"]],
            "runtime_camera_target": [round(value, 4) for value in camera_cfg["target"]],
            "lens": camera_cfg["lens"],
            "frame": camera_cfg["frame"],
            "nonzero": screenshot_ok(path),
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


def render_image_contact_sheet(image_items, out_path, title, cols=4, width=2200, height=1700):
    if screenshot_ok(out_path):
        return out_path

    setup_scene(width, height)
    bpy.context.scene.world.color = (0.005, 0.005, 0.007)
    cell_w = 16.0
    cell_h = 10.0
    pad_x = 0.95
    pad_z = 1.05
    rows = math.ceil(len(image_items) / cols)
    text_mat = make_material("sheet_label", hex_to_rgba("#F8FAFC"), roughness=0.6)
    for index, item in enumerate(image_items):
        row = index // cols
        col = index % cols
        x = (col - (cols - 1) / 2) * (cell_w + pad_x)
        z = ((rows - 1) / 2 - row) * (cell_h + pad_z)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0, z), rotation=(math.pi / 2, 0, 0))
        plane = bpy.context.object
        plane.name = f"s85_sheet_image_{index:02d}"
        plane.dimensions = (cell_w, cell_h, 1)
        plane.data.materials.append(make_image_material(f"s85_sheet_image_mat_{index:02d}", item["path"]))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.text_add(location=(x - cell_w * 0.49, -0.03, z + cell_h * 0.55), rotation=(math.pi / 2, 0, 0))
        text = bpy.context.object
        text.name = f"s85_sheet_label_{index:02d}"
        text.data.body = item["label"]
        text.data.align_x = "LEFT"
        text.data.align_y = "CENTER"
        text.data.size = 0.28
        text.data.materials.append(text_mat)

    title_z = rows * (cell_h + pad_z) * 0.5 + 0.8
    bpy.ops.object.text_add(location=(-(cols * cell_w) * 0.5, -0.03, title_z), rotation=(math.pi / 2, 0, 0))
    title_obj = bpy.context.object
    title_obj.name = "s85_sheet_title"
    title_obj.data.body = title
    title_obj.data.align_x = "LEFT"
    title_obj.data.align_y = "CENTER"
    title_obj.data.size = 0.48
    title_obj.data.materials.append(text_mat)

    ortho = max(cols * (cell_w + pad_x), rows * (cell_h + pad_z) * (width / height)) * 0.62
    camera = make_camera("S85_Image_Contact_Camera", (0, -36, 1), (0, 0, 1), lens=70, ortho=ortho)
    render_still(camera, out_path, frame=1, width=width, height=height)
    return out_path


def audit_asset_metrics(city, baseline_evidence, app_hero_evidence):
    metrics = {}
    for cfg in STRUCTURES:
        item = city["registry"][cfg["id"]]
        profile = RISK_PROFILE[cfg["id"]]
        exterior_size = os.path.getsize(cfg["exterior"]) if os.path.exists(cfg["exterior"]) else 0
        public_size = os.path.getsize(cfg["public_exterior"]) if os.path.exists(cfg["public_exterior"]) else 0
        risk = profile["risk"]
        metrics[cfg["id"]] = {
            "label": cfg["label"],
            "approved_exterior": rel(cfg["exterior"]),
            "public_exterior": rel(cfg["public_exterior"]),
            "runtime_exterior": cfg["runtime_exterior"],
            "overview_lod_preserved": os.path.exists(cfg["exterior"]) and os.path.exists(cfg["public_exterior"]),
            "has_hero_exterior": cfg["has_hero_exterior"],
            "tris": count_tris(item["objects"]),
            "mesh_objects": len([obj for obj in item["objects"] if obj.type == "MESH"]),
            "source_size_bytes": exterior_size,
            "public_size_bytes": public_size,
            "bbox": bbox_dict(item["bbox"]),
            "material_roots": item["material_roots"],
            "invalid_materials": item["invalid_materials"],
            "baseline_evidence": baseline_evidence.get(cfg["id"], {}),
            "app_hero_evidence": app_hero_evidence.get(cfg["id"], {}),
            "construction_read_risk": risk,
            "construction_read_label": "high" if risk >= 4 else "medium" if risk == 3 else "low-medium",
            "completion_wave": profile["wave"],
            "target_notes": profile["notes"],
        }
    return metrics


def source_file_bytes(paths):
    return sum(os.path.getsize(path) for path in paths if os.path.exists(path))


def summarize_city(city, metrics):
    active_structure_tris = sum(item["tris"] for item in metrics.values())
    energy_tris = sum(count_tris(item["objects"]) for item in city["energy_registry"].values())
    environment_tris = count_tris(city["context_objects"])
    active_city_tris = active_structure_tris + energy_tris + environment_tris
    active_source_bytes = source_file_bytes([cfg["exterior"] for cfg in STRUCTURES] + [energy_approved_path(asset_id) for asset_id in ENERGY_IDS])
    hero_count = sum(1 for cfg in STRUCTURES if cfg["has_hero_exterior"])
    return {
        "active_structure_tris": active_structure_tris,
        "energy_tris": energy_tris,
        "environment_tris": environment_tris,
        "active_city_tris": active_city_tris,
        "active_source_bytes": active_source_bytes,
        "hero_count": hero_count,
        "missing_assets": [rel(path) for path in city["missing_assets"]],
        "invalid_materials": city["invalid_materials"],
    }


def write_reports(metrics, city_summary, baseline_sheet, app_hero_sheet):
    active_structure_tris = city_summary["active_structure_tris"]
    energy_tris = city_summary["energy_tris"]
    environment_tris = city_summary["environment_tris"]
    active_city_tris = city_summary["active_city_tris"]
    active_source_bytes = city_summary["active_source_bytes"]
    hero_count = city_summary["hero_count"]

    baseline_complete = all(
        all(view in item["baseline_evidence"] for view in ("front", "three_quarter", "ground_up", "dark_first"))
        and all(screenshot_ok(os.path.join(ROOT, path)) for path in item["baseline_evidence"].values())
        for item in metrics.values()
    )
    app_hero_complete = all(item["app_hero_evidence"].get("nonzero") for item in metrics.values())
    checks = {
        "all_approved_overview_exteriors_present": all(item["overview_lod_preserved"] for item in metrics.values()),
        "no_hero_exteriors_built_during_audit": hero_count == 0,
        "material_roots_valid": all(len(item["invalid_materials"]) == 0 for item in metrics.values()) and len(city_summary["invalid_materials"]) == 0,
        "baseline_front_threequarter_groundup_darkfirst_complete": baseline_complete,
        "app_hero_camera_evidence_complete": app_hero_complete,
        "baseline_contact_sheet_nonzero": screenshot_ok(baseline_sheet),
        "app_hero_contact_sheet_nonzero": screenshot_ok(app_hero_sheet),
        "overview_city_tri_budget_preserved": active_city_tris <= 250000,
        "active_source_file_budget_preserved": active_source_bytes <= 5 * 1024 * 1024,
        "phase10_lod_policy_present": MANIFEST.get("lodPolicy", {}).get("exteriorHeroField") == "exteriorHero",
    }

    performance = {
        "session": SESSION,
        "date": str(date.today()),
        "active_scene": {
            "structure_exterior_tris": active_structure_tris,
            "energy_tris": energy_tris,
            "environment_tris": environment_tris,
            "total_tris": active_city_tris,
            "budget": "<=250K",
            "result": "PASS" if checks["overview_city_tri_budget_preserved"] else "NEEDS REVIEW",
        },
        "source_glb_bytes": {
            "active_exteriors_plus_energy": active_source_bytes,
            "active_exteriors_plus_energy_kb": round(active_source_bytes / 1024, 1),
        },
        "hero_exterior_count": hero_count,
    }
    with open(PERFORMANCE_REPORT, "w", encoding="utf-8") as handle:
        json.dump(performance, handle, indent=2, sort_keys=True)

    risk_order = sorted(metrics.values(), key=lambda item: (-item["construction_read_risk"], item["label"]))
    wave_targets = {}
    for item in risk_order:
        wave_targets.setdefault(item["completion_wave"], []).append(item["label"])

    report = {
        "session": SESSION,
        "date": str(date.today()),
        "scope": "Phase 10 architectural completion audit and baseline evidence capture",
        "phase10_backlog": rel(PHASE10_BACKLOG),
        "checks": checks,
        "overall_verdict": "APPROVED" if not city_summary["missing_assets"] and all(checks.values()) else "NEEDS REVIEW",
        "missing_assets": city_summary["missing_assets"],
        "invalid_materials": city_summary["invalid_materials"],
        "structure_metrics": metrics,
        "risk_order": [
            {
                "label": item["label"],
                "construction_read_risk": item["construction_read_risk"],
                "completion_wave": item["completion_wave"],
            }
            for item in risk_order
        ],
        "wave_targets": wave_targets,
        "baseline_contact_sheet": rel(baseline_sheet),
        "app_hero_contact_sheet": rel(app_hero_sheet),
        "performance_report": rel(PERFORMANCE_REPORT),
        "active_city_tris": active_city_tris,
        "active_source_bytes": active_source_bytes,
    }
    with open(REPORT_JSON, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)

    lines = [
        "# Session 85 Completion Audit",
        "",
        f"Date: {date.today()}",
        f"Status: {'Approved' if report['overall_verdict'] == 'APPROVED' else 'Needs review'}",
        "",
        "## Scope",
        "",
        "Session 85 entered Phase 10 Architectural Completion as an evidence-only audit. It captured baseline front, 3/4, ground-up, dark-first, and app hero-camera evidence for all 12 approved exteriors, scored construction-read risk, and recorded target notes for the completion waves.",
        "",
        "Approved overview exteriors, layout positions, baked energy endpoints, Phase 9 app behavior, and the current overview LOD policy were preserved. No hero exteriors were built in this session.",
        "",
        "## Performance Snapshot",
        "",
        "| Metric | Result | Gate |",
        "|---|---:|---|",
        f"| Active city tris | {active_city_tris:,} | <=250,000 |",
        f"| Structure exterior tris | {active_structure_tris:,} | tracked |",
        f"| Energy tris | {energy_tris:,} | tracked |",
        f"| City context tris | {environment_tris:,} | tracked |",
        f"| Active source GLB size | {active_source_bytes / 1024:.1f} KB | <=5,120 KB |",
        f"| Hero exterior count | {hero_count} | 0 for audit-only Session 85 |",
        "",
        "## Construction-Read Risk",
        "",
        "| Structure | Risk | Completion Wave | Target Notes |",
        "|---|---:|---|---|",
    ]
    for item in risk_order:
        notes = " ".join(item["target_notes"])
        lines.append(
            f"| {item['label']} | {item['construction_read_risk']} / 5 | {item['completion_wave']} | {notes} |"
        )
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            f"- `{rel(baseline_sheet)}`",
            f"- `{rel(app_hero_sheet)}`",
            f"- `{rel(REPORT_JSON)}`",
            f"- `{rel(PERFORMANCE_REPORT)}`",
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
            f"Overall verdict: **{report['overall_verdict']}**.",
            "",
            "Next recommended session: **Session 86 Pilot Wave: Finance, SIA Tower, and Knowledgebase**.",
        ]
    )

    report_text = "\n".join(lines) + "\n"
    with open(REPORT_MD, "w", encoding="utf-8") as handle:
        handle.write(report_text)
    with open(APP_SESSION_REPORT, "w", encoding="utf-8") as handle:
        handle.write(report_text.replace("# Session 85 Completion Audit", "# Session 85 Report - Completion Audit", 1))

    return report


def main():
    print("=" * 72)
    print("Session 85: Phase 10 architectural completion audit")
    print("=" * 72)

    baseline_evidence = {}
    for cfg in STRUCTURES:
        print(f"Rendering baseline evidence: {cfg['label']}")
        baseline_evidence[cfg["id"]] = render_structure_baseline(cfg)

    print("Rendering app hero-camera evidence from current focused-scene cameras")
    city = import_full_city_for_app_hero()
    app_hero_evidence = render_app_hero_evidence(city)

    metrics = audit_asset_metrics(city, baseline_evidence, app_hero_evidence)
    city_summary = summarize_city(city, metrics)

    baseline_items = []
    for cfg in STRUCTURES:
        for view in ("front", "three_quarter", "ground_up", "dark_first"):
            path = os.path.join(ROOT, baseline_evidence[cfg["id"]][view])
            baseline_items.append({"path": path, "label": f"{cfg['label']} - {view.replace('_', ' ')}"})
    baseline_sheet = render_image_contact_sheet(
        baseline_items,
        os.path.join(SCREENSHOT_DIR, "s85-completion-baseline-contact-sheet.png"),
        "Session 85 Completion Baseline: Front, 3/4, Ground-Up, Dark-First",
        cols=4,
        width=2400,
        height=3400,
    )

    app_items = [
        {
            "path": os.path.join(ROOT, app_hero_evidence[cfg["id"]]["path"]),
            "label": f"Scene {app_hero_evidence[cfg['id']]['scene']:02d} - {cfg['label']}",
        }
        for cfg in STRUCTURES
    ]
    app_hero_sheet = render_image_contact_sheet(
        app_items,
        os.path.join(SCREENSHOT_DIR, "s85-app-hero-camera-contact-sheet.png"),
        "Session 85 App Hero-Camera Baseline",
        cols=4,
        width=2200,
        height=1700,
    )

    report = write_reports(metrics, city_summary, baseline_sheet, app_hero_sheet)

    print(f"Report: {REPORT_MD}")
    print(f"App report: {APP_SESSION_REPORT}")
    print(f"Performance: {PERFORMANCE_REPORT}")
    print(f"Verdict: {report['overall_verdict']}")
    for check, passed in report["checks"].items():
        print(f"  {check}: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()

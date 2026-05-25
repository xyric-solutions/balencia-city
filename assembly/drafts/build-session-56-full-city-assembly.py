"""
Session 56: Phase 6 full-city assembly.

Imports every approved exterior/interior and approved energy asset, places the
city in the finalized orbital layout, renders overview/cardinal/scroll
verification screenshots, saves the assembly .blend, and writes QA reports.
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
SHARED = os.path.join(PROJECT, "shared")
SCREENSHOTS = os.path.join(ASSEMBLY_DIR, "screenshots")
SCROLL_SHOTS = os.path.join(ASSEMBLY_DIR, "scroll-verification")
PERF_DIR = os.path.join(ASSEMBLY_DIR, "performance-reports")
BLEND_FILE = os.path.join(DRAFTS, "full-city-assembly.blend")
REPORT_FILE = os.path.join(DRAFTS, "full-city-assembly-session56-report.json")
PERFORMANCE_FILE = os.path.join(PERF_DIR, "session-56-performance.json")

for path in (DRAFTS, SCREENSHOTS, SCROLL_SHOTS, PERF_DIR):
    os.makedirs(path, exist_ok=True)


STRUCTURES = [
    {
        "name": "SIA_Tower",
        "label": "SIA Tower",
        "position": (0, 0, 0),
        "hex": "#FF5E00",
        "exterior": os.path.join(MODULES, "00-sia-tower/exterior/approved/sia-tower-ext.glb"),
        "interior": os.path.join(MODULES, "00-sia-tower/interior/approved/sia-tower-int.glb"),
    },
    {
        "name": "Fitness",
        "label": "Fitness",
        "position": (26, 25, 0),
        "hex": "#34A853",
        "exterior": os.path.join(MODULES, "01-fitness/exterior/approved/fitness-ext.glb"),
        "interior": os.path.join(MODULES, "01-fitness/interior/approved/fitness-int.glb"),
    },
    {
        "name": "Yoga",
        "label": "Yoga & Wellbeing",
        "position": (36, 10, 0),
        "hex": "#6EE7B7",
        "exterior": os.path.join(MODULES, "02-yoga-wellbeing/exterior/approved/yoga-ext.glb"),
        "interior": os.path.join(MODULES, "02-yoga-wellbeing/interior/approved/yoga-int.glb"),
    },
    {
        "name": "Finance",
        "label": "Finance",
        "position": (35, -6, 0),
        "hex": "#F59E0B",
        "exterior": os.path.join(MODULES, "03-finance/exterior/approved/finance-ext.glb"),
        "interior": os.path.join(MODULES, "03-finance/interior/approved/finance-int-approved-s15.glb"),
    },
    {
        "name": "Knowledgebase",
        "label": "Knowledgebase",
        "position": (31, -22, 0),
        "hex": "#7F24FF",
        "exterior": os.path.join(MODULES, "04-knowledgebase/exterior/approved/knowledgebase-ext.glb"),
        "interior": os.path.join(MODULES, "04-knowledgebase/interior/approved/knowledgebase-int.glb"),
    },
    {
        "name": "Chat",
        "label": "Chat & Communication",
        "position": (19, -36, 0),
        "hex": "#FF5E00",
        "exterior": os.path.join(MODULES, "05-chat-communication/exterior/approved/chat-ext.glb"),
        "interior": os.path.join(MODULES, "05-chat-communication/interior/approved/chat-int.glb"),
    },
    {
        "name": "Leaderboard",
        "label": "Leaderboard & Competition",
        "position": (-8, -45, 0),
        "hex": "#FB7185",
        "exterior": os.path.join(MODULES, "06-leaderboard-competition/exterior/approved/leaderboard-ext.glb"),
        "interior": os.path.join(MODULES, "06-leaderboard-competition/interior/approved/leaderboard-int.glb"),
    },
    {
        "name": "Relationships",
        "label": "Relationships",
        "position": (8, -59, 0),
        "hex": "#F43F5E",
        "exterior": os.path.join(MODULES, "07-relationships/exterior/approved/relationships-ext.glb"),
        "interior": os.path.join(MODULES, "07-relationships/interior/approved/relationships-int.glb"),
    },
    {
        "name": "Career",
        "label": "Career",
        "position": (-30, -34, 0),
        "hex": "#3B82F6",
        "exterior": os.path.join(MODULES, "08-career/exterior/approved/career-ext.glb"),
        "interior": os.path.join(MODULES, "08-career/interior/approved/career-int.glb"),
    },
    {
        "name": "Recovery",
        "label": "Recovery & Sleep",
        "position": (-43, -8, 0),
        "hex": "#6366F1",
        "exterior": os.path.join(MODULES, "09-recovery-sleep/exterior/approved/recovery-ext.glb"),
        "interior": os.path.join(MODULES, "09-recovery-sleep/interior/approved/recovery-int.glb"),
    },
    {
        "name": "Analytics",
        "label": "AI Analytics",
        "position": (-31, 14, 0),
        "hex": "#14B8A6",
        "exterior": os.path.join(MODULES, "10-ai-analytics/exterior/approved/analytics-ext.glb"),
        "interior": os.path.join(MODULES, "10-ai-analytics/interior/approved/analytics-int.glb"),
    },
    {
        "name": "Nutrition",
        "label": "Nutrition",
        "position": (-12, 39, 0),
        "hex": "#D97706",
        "exterior": os.path.join(MODULES, "11-nutrition/exterior/approved/nutrition-ext.glb"),
        "interior": os.path.join(MODULES, "11-nutrition/interior/approved/nutrition-int.glb"),
    },
]


ENERGY_ASSETS = [
    {
        "name": "hard_pipelines",
        "label": "Hard pipelines",
        "path": os.path.join(ENERGY_DIR, "pipelines/approved/hard-pipelines.glb"),
    },
    {
        "name": "warm_mist",
        "label": "Warm mist",
        "path": os.path.join(ENERGY_DIR, "pipelines/approved/warm-mist.glb"),
    },
    {
        "name": "faint_thread",
        "label": "Faint thread",
        "path": os.path.join(ENERGY_DIR, "pipelines/approved/faint-thread.glb"),
    },
    {
        "name": "knowledgebase_waterfall",
        "label": "Knowledgebase waterfall",
        "path": os.path.join(ENERGY_DIR, "pipelines/approved/knowledgebase-waterfall.glb"),
    },
    {
        "name": "leaderboard_lightning",
        "label": "Leaderboard lightning",
        "path": os.path.join(ENERGY_DIR, "pipelines/approved/leaderboard-lightning.glb"),
    },
    {
        "name": "cross_district_gold",
        "label": "Cross-district gold",
        "path": os.path.join(ENERGY_DIR, "cross-connections/approved/cross-district-gold.glb"),
    },
    {
        "name": "ai_pulse",
        "label": "AI pulse",
        "path": os.path.join(ENERGY_DIR, "pulse/approved/ai-pulse.glb"),
    },
]

VALID_MATERIAL_ROOTS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r", encoding="utf-8") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16) / 255.0,
        int(hex_color[2:4], 16) / 255.0,
        int(hex_color[4:6], 16) / 255.0,
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


def setup_render():
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = 192
    scene.frame_set(96)
    scene.render.fps = 24
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        eevee = scene.eevee
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
            eevee.bloom_threshold = 0.18
            eevee.bloom_intensity = 0.72
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.75


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


def set_objects_hidden(objects, hidden):
    for obj in objects:
        obj.hide_render = hidden
        obj.hide_viewport = hidden


def render_still(camera, path, frame=96, show_objects=None, hide_objects=None):
    show_objects = show_objects or []
    hide_objects = hide_objects or []
    touched = list(dict.fromkeys(show_objects + hide_objects))
    previous = {obj: (obj.hide_render, obj.hide_viewport) for obj in touched}
    set_objects_hidden(show_objects, False)
    set_objects_hidden(hide_objects, True)
    bpy.context.scene.frame_set(frame)
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    for obj, (hide_render, hide_viewport) in previous.items():
        obj.hide_render = hide_render
        obj.hide_viewport = hide_viewport
    return path


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


def source_file_bytes(paths):
    return sum(os.path.getsize(path) for path in paths if os.path.exists(path))


def create_strip(name, start, end, width, z, mat, collection):
    start = Vector(start)
    end = Vector(end)
    direction = Vector((end.x - start.x, end.y - start.y, 0))
    if direction.length == 0:
        return None
    direction.normalize()
    perp = Vector((-direction.y, direction.x, 0)) * (width * 0.5)
    verts = [
        (start.x - perp.x, start.y - perp.y, z),
        (start.x + perp.x, start.y + perp.y, z),
        (end.x + perp.x, end.y + perp.y, z),
        (end.x - perp.x, end.y - perp.y, z),
    ]
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    collection.objects.link(obj)
    return obj


def create_cylinder(name, radius, depth, z, mat, collection, vertices=128):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(0, 0, z))
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"{name}_mesh"
    obj.data.materials.append(mat)
    link_to_collection(obj, collection)
    bpy.ops.object.select_all(action="DESELECT")
    return obj


def create_city_context(collection, structures):
    base_mat = make_material("base", hex_to_rgba("#101018"), roughness=0.88, metallic=0.02)
    detail_mat = make_material("detail", hex_to_rgba("#16161E"), roughness=0.7, metallic=0.08)
    energy_mat = make_material(
        "energy",
        hex_to_rgba("#FF5E00", 1.0),
        roughness=0.24,
        emission=hex_to_rgba("#FF5E00", 1.0),
        emission_strength=0.55,
    )
    glass_mat = make_material("glass", hex_to_rgba("#0F0F18", 0.72), roughness=0.12, metallic=0.18, alpha=0.72)

    objects = [
        create_cylinder("city_obsidian_ground", 82.0, 0.035, -0.035, base_mat, collection, vertices=160),
        create_cylinder("central_plaza_polished_stone", 22.0, 0.045, -0.005, detail_mat, collection, vertices=128),
        create_cylinder("central_reflection_pool_dark_glass", 13.5, 0.018, 0.028, glass_mat, collection, vertices=96),
    ]

    for radius, width, name in ((24.0, 0.18, "plaza_orange_energy_ring"), (46.0, 0.14, "midcity_orange_energy_ring"), (71.0, 0.12, "perimeter_orange_energy_ring")):
        curve = bpy.data.curves.new(f"{name}_curve_data", type="CURVE")
        curve.dimensions = "3D"
        curve.resolution_u = 64
        curve.bevel_depth = width
        curve.bevel_resolution = 1
        spline = curve.splines.new("POLY")
        spline.points.add(143)
        for idx, point in enumerate(spline.points):
            angle = math.tau * idx / 144
            point.co = (math.cos(angle) * radius, math.sin(angle) * radius, 0.055, 1)
        obj = bpy.data.objects.new(name, curve)
        obj.data.materials.append(energy_mat)
        collection.objects.link(obj)
        objects.append(obj)

    for cfg in structures:
        if cfg["name"] == "SIA_Tower":
            continue
        end = Vector(cfg["position"])
        direction = Vector((end.x, end.y, 0))
        if direction.length:
            direction.normalize()
        start = direction * 15.0
        road_end = Vector((end.x, end.y, 0)) - direction * 5.0
        road = create_strip(f"boulevard_to_{cfg['name'].lower()}", start, road_end, 2.25, 0.035, detail_mat, collection)
        vein = create_strip(f"energy_vein_to_{cfg['name'].lower()}", start, road_end, 0.18, 0.07, energy_mat, collection)
        if road:
            objects.append(road)
        if vein:
            objects.append(vein)

    return objects


def screenshot_ok(path):
    return os.path.exists(path) and os.path.getsize(path) > 8 * 1024


def path_rel(path):
    return os.path.relpath(path, PROJECT)


print("=" * 72)
print("Session 56: Full-City Assembly")
print("=" * 72)

bpy.ops.wm.read_factory_settings(use_empty=True)

lighting = load_python_module(os.path.join(SHARED, "lighting-rig.py"), "lighting_rig")
lighting["clear_lighting"]()
lighting["setup_viewport_lighting"]()
setup_render()

context_collection = bpy.data.collections.new("City_Context")
bpy.context.scene.collection.children.link(context_collection)
structures_collection = bpy.data.collections.new("Approved_Structures")
bpy.context.scene.collection.children.link(structures_collection)
energy_collection = bpy.data.collections.new("Approved_Energy")
bpy.context.scene.collection.children.link(energy_collection)

environment_objects = create_city_context(context_collection, STRUCTURES)

registry = {}
missing_assets = []
all_exteriors = []
all_interiors = []

for cfg in STRUCTURES:
    collection = bpy.data.collections.new(cfg["name"])
    structures_collection.children.link(collection)
    if not os.path.exists(cfg["exterior"]):
        missing_assets.append(cfg["exterior"])
    if not os.path.exists(cfg["interior"]):
        missing_assets.append(cfg["interior"])

    exterior = import_glb(cfg["exterior"], collection, cfg["position"])
    interior = import_glb(cfg["interior"], collection, cfg["position"])
    set_objects_hidden(interior, True)

    ext_box = world_bbox(exterior)
    int_box = world_bbox(interior)
    combined_box = world_bbox(exterior + interior)
    roots, invalid = collect_material_roots(exterior + interior)
    registry[cfg["name"]] = {
        "config": cfg,
        "collection": collection,
        "exterior": exterior,
        "interior": interior,
        "bbox_exterior": ext_box,
        "bbox_interior": int_box,
        "bbox_combined": combined_box,
        "material_roots": roots,
        "invalid_materials": invalid,
    }
    all_exteriors.extend(exterior)
    all_interiors.extend(interior)
    print(f"{cfg['name']}: ext={len(exterior)} int={len(interior)} pos={cfg['position']}")

energy_registry = {}
all_energy = []
for asset in ENERGY_ASSETS:
    collection = bpy.data.collections.new(asset["name"])
    energy_collection.children.link(collection)
    if not os.path.exists(asset["path"]):
        missing_assets.append(asset["path"])
        imported = []
    else:
        imported = import_glb(asset["path"], collection)
    roots, invalid = collect_material_roots(imported)
    energy_registry[asset["name"]] = {
        "config": asset,
        "objects": imported,
        "bbox": world_bbox(imported),
        "material_roots": roots,
        "invalid_materials": invalid,
    }
    all_energy.extend(imported)
    print(f"{asset['name']}: objects={len(imported)}")

scene_objects = all_exteriors + all_energy + environment_objects
all_loaded_objects = scene_objects + all_interiors
invalid_materials = []
for item in registry.values():
    invalid_materials.extend(item["invalid_materials"])
for item in energy_registry.values():
    invalid_materials.extend(item["invalid_materials"])

structure_metrics = {}
for name, item in registry.items():
    cfg = item["config"]
    ext_tris = count_tris(item["exterior"])
    int_tris = count_tris(item["interior"])
    box = item["bbox_combined"]
    center = box["center"] if box else Vector(cfg["position"])
    structure_metrics[name] = {
        "label": cfg["label"],
        "position": list(cfg["position"]),
        "exterior_objects": len(item["exterior"]),
        "interior_objects": len(item["interior"]),
        "exterior_tris": ext_tris,
        "interior_tris": int_tris,
        "combined_tris": ext_tris + int_tris,
        "bbox_exterior": bbox_dict(item["bbox_exterior"]),
        "bbox_interior": bbox_dict(item["bbox_interior"]),
        "bbox_combined": bbox_dict(item["bbox_combined"]),
        "radial_center_distance": round(math.hypot(center.x, center.y), 4),
        "material_roots": item["material_roots"],
        "approved_exterior_present": os.path.exists(cfg["exterior"]) and len(item["exterior"]) > 0,
        "approved_interior_present": os.path.exists(cfg["interior"]) and len(item["interior"]) > 0,
    }

energy_metrics = {}
for name, item in energy_registry.items():
    cfg = item["config"]
    energy_metrics[name] = {
        "label": cfg["label"],
        "objects": len(item["objects"]),
        "mesh_objects": len([obj for obj in item["objects"] if obj.type == "MESH"]),
        "tris": count_tris(item["objects"]),
        "bbox": bbox_dict(item["bbox"]),
        "file_size_bytes": os.path.getsize(cfg["path"]) if os.path.exists(cfg["path"]) else 0,
        "material_roots": item["material_roots"],
        "approved_asset_present": os.path.exists(cfg["path"]) and len(item["objects"]) > 0,
    }

sia_height = structure_metrics["SIA_Tower"]["bbox_exterior"]["size"][2]
tallest_district = max(
    value["bbox_exterior"]["size"][2]
    for key, value in structure_metrics.items()
    if key != "SIA_Tower" and value["bbox_exterior"]
)
sia_dominance_ratio = sia_height / tallest_district if tallest_district else 0

active_structure_tris = sum(item["exterior_tris"] for item in structure_metrics.values())
interior_tris = sum(item["interior_tris"] for item in structure_metrics.values())
energy_tris = sum(item["tris"] for item in energy_metrics.values())
environment_tris = count_tris(environment_objects)
active_city_tris = active_structure_tris + energy_tris + environment_tris
loaded_verification_tris = active_city_tris + interior_tris

approved_exterior_paths = [cfg["exterior"] for cfg in STRUCTURES]
approved_interior_paths = [cfg["interior"] for cfg in STRUCTURES]
approved_energy_paths = [asset["path"] for asset in ENERGY_ASSETS]
active_source_bytes = source_file_bytes(approved_exterior_paths + approved_energy_paths)
interior_source_bytes = source_file_bytes(approved_interior_paths)

overview_screenshots = {}
overview_configs = [
    ("overview_citywide", "s56-overview-citywide.png", (108, -154, 112), (0, -8, 22), 14, 144),
    ("overview_topdown", "s56-overview-topdown.png", (0, 0, 145), (0, 0, 0), 34, 144),
    ("skyline_north", "s56-skyline-north.png", (0, 118, 42), (0, 0, 19), 24, 96),
    ("skyline_south", "s56-skyline-south.png", (0, -126, 45), (0, -8, 18), 24, 96),
    ("skyline_east", "s56-skyline-east.png", (122, 0, 45), (0, -3, 18), 24, 96),
    ("skyline_west", "s56-skyline-west.png", (-122, 0, 45), (0, -3, 18), 24, 96),
    ("energy_climax", "s56-energy-climax.png", (92, -118, 92), (0, -10, 24), 16, 144),
]

for key, filename, loc, target, lens, frame in overview_configs:
    path = os.path.join(SCREENSHOTS, filename)
    camera = make_camera(f"S56_{key}", loc, target, lens=lens, clip_end=950)
    overview_screenshots[key] = render_still(camera, path, frame=frame)

scroll_configs = [
    {
        "scene": 1,
        "slug": "arrival",
        "focus": "City Aerial",
        "loc": (112, -148, 112),
        "target": (0, -8, 20),
        "lens": 14,
        "frame": 144,
    },
    {
        "scene": 2,
        "slug": "sia-tower-reveal",
        "focus": "SIA Tower Exterior",
        "loc": (18, -25, 7.8),
        "target": (0, 0, 38),
        "lens": 30,
        "frame": 12,
    },
    {
        "scene": 3,
        "slug": "sia-neural-core",
        "focus": "SIA Tower Interior",
        "loc": (0, -3.05, 7.2),
        "target": (0, 0, 25),
        "lens": 24,
        "frame": 48,
        "show_interior": "SIA_Tower",
        "hide_exterior": "SIA_Tower",
        "hide_city_context": True,
        "hide_sia_shell": True,
    },
    {
        "scene": 4,
        "slug": "fitness-district",
        "focus": "Fitness District",
        "loc": (47, 51, 15.5),
        "target": (26, 25, 7.5),
        "lens": 34,
        "frame": 96,
    },
    {
        "scene": 5,
        "slug": "yoga-sanctuary",
        "focus": "Yoga & Wellbeing",
        "loc": (56, 30, 12),
        "target": (36, 10, 4.5),
        "lens": 34,
        "frame": 96,
    },
    {
        "scene": 6,
        "slug": "finance-tower",
        "focus": "Finance",
        "loc": (58, -18, 16),
        "target": (35, -6, 10),
        "lens": 36,
        "frame": 96,
    },
    {
        "scene": 7,
        "slug": "knowledgebase",
        "focus": "Knowledgebase",
        "loc": (49, -42, 19),
        "target": (31, -22, 8),
        "lens": 34,
        "frame": 96,
    },
    {
        "scene": 8,
        "slug": "communication-hub",
        "focus": "Chat & Communication",
        "loc": (44, -62, 17),
        "target": (19, -36, 8),
        "lens": 32,
        "frame": 96,
    },
    {
        "scene": 9,
        "slug": "leaderboard-arena",
        "focus": "Leaderboard & Competition",
        "loc": (-24, -79, 19),
        "target": (-8, -45, 6.4),
        "lens": 32,
        "frame": 96,
    },
    {
        "scene": 10,
        "slug": "relationships-garden",
        "focus": "Relationships",
        "loc": (18, -88, 13),
        "target": (8, -59, 4.3),
        "lens": 32,
        "frame": 96,
    },
    {
        "scene": 11,
        "slug": "career-towers",
        "focus": "Career",
        "loc": (-58, -62, 24),
        "target": (-30, -34, 11.5),
        "lens": 35,
        "frame": 96,
    },
    {
        "scene": 12,
        "slug": "recovery-dreamscape",
        "focus": "Recovery & Sleep",
        "loc": (-75, -20, 13),
        "target": (-43, -8, 5),
        "lens": 35,
        "frame": 96,
    },
    {
        "scene": 13,
        "slug": "analytics-cathedral",
        "focus": "AI Analytics",
        "loc": (-62, 34, 21),
        "target": (-31, 14, 10.5),
        "lens": 34,
        "frame": 96,
    },
    {
        "scene": 14,
        "slug": "nutrition-farm",
        "focus": "Nutrition",
        "loc": (-32, 62, 14),
        "target": (-12, 39, 6),
        "lens": 35,
        "frame": 96,
    },
    {
        "scene": 15,
        "slug": "cross-pillar-revelation",
        "focus": "Cross-Pillar Revelation",
        "loc": (90, -120, 102),
        "target": (0, -12, 24),
        "lens": 16,
        "frame": 144,
    },
    {
        "scene": 16,
        "slug": "today-screen-street",
        "focus": "Today Screen Street Corridor",
        "loc": (31, -26, 2.9),
        "target": (19, -36, 8),
        "lens": 32,
        "frame": 96,
    },
    {
        "scene": 17,
        "slug": "sia-tower-return",
        "focus": "SIA Tower Return",
        "loc": (0, -150, 80),
        "target": (0, 0, 30),
        "lens": 18,
        "frame": 144,
    },
]

scroll_screenshots = {}
for cfg in scroll_configs:
    filename = f"scene-{cfg['scene']:02d}-{cfg['slug']}.png"
    path = os.path.join(SCROLL_SHOTS, filename)
    show_objects = []
    hide_objects = []
    if cfg.get("show_interior"):
        show_objects.extend(registry[cfg["show_interior"]]["interior"])
    if cfg.get("hide_exterior"):
        hide_objects.extend(registry[cfg["hide_exterior"]]["exterior"])
    if cfg.get("hide_city_context"):
        hide_objects.extend(all_energy)
        hide_objects.extend(environment_objects)
    if cfg.get("hide_sia_shell"):
        hide_objects.extend(
            obj
            for obj in registry["SIA_Tower"]["interior"]
            if obj.name.startswith(("INT_Wall", "INT_Ceiling", "INT_Floor"))
        )
    camera = make_camera(f"S56_Scene_{cfg['scene']:02d}_{cfg['slug']}", cfg["loc"], cfg["target"], lens=cfg["lens"], clip_end=950)
    rendered = render_still(camera, path, frame=cfg["frame"], show_objects=show_objects, hide_objects=hide_objects)
    scroll_screenshots[f"scene_{cfg['scene']:02d}"] = {
        "focus": cfg["focus"],
        "path": path_rel(rendered),
        "camera_location": list(cfg["loc"]),
        "camera_target": list(cfg["target"]),
        "lens": cfg["lens"],
        "frame": cfg["frame"],
        "nonzero": screenshot_ok(rendered),
    }

bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
blend_size = os.path.getsize(BLEND_FILE)

overview_screen_report = {
    key: {"path": path_rel(path), "nonzero": screenshot_ok(path)}
    for key, path in overview_screenshots.items()
}

checks = {
    "all_approved_structure_exteriors_present": all(item["approved_exterior_present"] for item in structure_metrics.values()),
    "all_approved_structure_interiors_present": all(item["approved_interior_present"] for item in structure_metrics.values()),
    "all_approved_energy_assets_present": all(item["approved_asset_present"] for item in energy_metrics.values()),
    "material_roots_valid": len(invalid_materials) == 0,
    "active_city_triangle_budget": 180000 <= active_city_tris <= 250000,
    "active_source_file_budget": active_source_bytes <= 5 * 1024 * 1024,
    "scroll_screenshot_count": len(scroll_screenshots) == 17,
    "scroll_screenshots_nonzero": all(item["nonzero"] for item in scroll_screenshots.values()),
    "overview_screenshots_nonzero": all(item["nonzero"] for item in overview_screen_report.values()),
    "sia_dominance_preserved": sia_dominance_ratio >= 2.0,
    "energy_layer_visible": count_tris(all_energy) > 0,
}

performance = {
    "session": 56,
    "blend_file": path_rel(BLEND_FILE),
    "blend_file_size_bytes": blend_size,
    "active_scene": {
        "structure_exterior_tris": active_structure_tris,
        "energy_tris": energy_tris,
        "environment_tris": environment_tris,
        "total_tris": active_city_tris,
        "budget": "180K-250K",
        "result": "PASS" if checks["active_city_triangle_budget"] else "NEEDS REVIEW",
    },
    "loaded_for_verification": {
        "interior_tris_hidden_by_default": interior_tris,
        "total_tris_with_all_interiors": loaded_verification_tris,
        "note": "Interiors are imported for scroll verification and hidden by default; app phase should load interiors on demand.",
    },
    "source_glb_bytes": {
        "active_exteriors_and_energy": active_source_bytes,
        "interiors_on_demand": interior_source_bytes,
        "active_budget_bytes": 5 * 1024 * 1024,
        "result": "PASS" if checks["active_source_file_budget"] else "NEEDS REVIEW",
    },
    "structure_tris": {
        name: {
            "exterior": item["exterior_tris"],
            "interior": item["interior_tris"],
            "combined": item["combined_tris"],
        }
        for name, item in structure_metrics.items()
    },
    "energy_tris": {name: item["tris"] for name, item in energy_metrics.items()},
}

report = {
    "session": 56,
    "phase": "assembly/full-city-layout",
    "blender_version": bpy.app.version_string,
    "blend_file": path_rel(BLEND_FILE),
    "report_file": path_rel(REPORT_FILE),
    "performance_report": path_rel(PERFORMANCE_FILE),
    "missing_assets": [path_rel(path) for path in missing_assets],
    "structure_metrics": structure_metrics,
    "energy_metrics": energy_metrics,
    "scale_and_layout": {
        "sia_height": round(sia_height, 4),
        "tallest_district_height": round(tallest_district, 4),
        "sia_dominance_ratio": round(sia_dominance_ratio, 4),
        "city_perimeter_radius": round(max(math.hypot(box["center"][0], box["center"][1]) for box in [m["bbox_combined"] for m in structure_metrics.values()] if box), 4),
        "note": "SIA remains the dominant central landmark. Ratio uses the legacy approved SIA source-of-truth noted in PROGRESS.md.",
    },
    "performance": performance,
    "checks": checks,
    "invalid_materials": invalid_materials[:25],
    "overview_screenshots": overview_screen_report,
    "scroll_screenshots": scroll_screenshots,
    "verdict": "APPROVED" if all(checks.values()) else "NEEDS REVIEW",
}

with open(PERFORMANCE_FILE, "w", encoding="utf-8") as handle:
    json.dump(performance, handle, indent=2, sort_keys=True)

with open(REPORT_FILE, "w", encoding="utf-8") as handle:
    json.dump(report, handle, indent=2, sort_keys=True)

print("=" * 72)
print("SESSION 56 FULL-CITY ASSEMBLY COMPLETE")
print(f"Blend: {BLEND_FILE}")
print(f"Report: {REPORT_FILE}")
print(f"Performance: {PERFORMANCE_FILE}")
print(f"Active city tris: {active_city_tris}")
print(f"Loaded verification tris: {loaded_verification_tris}")
print(f"SIA dominance ratio: {sia_dominance_ratio:.3f}")
print(f"Verdict: {report['verdict']}")
for key, value in checks.items():
    print(f"  {key}: {'PASS' if value else 'FAIL'}")

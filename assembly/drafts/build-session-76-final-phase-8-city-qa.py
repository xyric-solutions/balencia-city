"""
Balencia City v3 - Session 76
Final Phase 8 city QA, refreshed contact sheets, and performance review.

This script is intentionally evidence-only: it imports current approved assets,
renders final QA sheets/stills, checks material/layout/performance gates, and
writes audit artifacts without changing approved GLBs.
"""

import json
import math
import os
from datetime import date

import bpy
from mathutils import Vector


SESSION = 76
ROOT = "/Users/hamza/Desktop/balencia-city-v3"
LAYOUT_PATH = os.path.join(ROOT, "shared", "city-layout-v2.json")
MANIFEST_PATH = os.path.join(ROOT, "apps", "balencia", "src", "lib", "asset-manifest.json")
BASELINE_AUDIT_PATH = os.path.join(ROOT, "assembly", "audit", "session-71-exterior-finish-audit.json")
SHARED_DIR = os.path.join(ROOT, "shared")
ASSEMBLY_DIR = os.path.join(ROOT, "assembly")
ASSEMBLY_AUDIT = os.path.join(ASSEMBLY_DIR, "audit")
ASSEMBLY_SCREENSHOTS = os.path.join(ASSEMBLY_DIR, "screenshots")
SCROLL_SCREENSHOTS = os.path.join(ASSEMBLY_DIR, "scroll-verification", "session-76")
PERFORMANCE_DIR = os.path.join(ASSEMBLY_DIR, "performance-reports")
REPORT_JSON = os.path.join(ASSEMBLY_AUDIT, "session-76-final-phase-8-city-qa.json")
REPORT_MD = os.path.join(ASSEMBLY_AUDIT, "session-76-final-phase-8-city-qa.md")
PERFORMANCE_REPORT = os.path.join(PERFORMANCE_DIR, "session-76-performance.json")

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
TARGET_SCROLL_SCENES = {1, 4, 6, 11, 15, 16, 17}


for path in (ASSEMBLY_AUDIT, ASSEMBLY_SCREENSHOTS, SCROLL_SCREENSHOTS, PERFORMANCE_DIR):
    os.makedirs(path, exist_ok=True)


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


def layout_runtime(id_name, height=0):
    position = LAYOUT["districts"][id_name]["runtimePosition"]
    return (position[0], height, position[2])


def layout_offset_runtime(id_name, offset):
    base = LAYOUT["districts"][id_name]["runtimePosition"]
    return (base[0] + offset[0], offset[1], base[2] + offset[2])


def layout_blender(id_name):
    return tuple(LAYOUT["districts"][id_name]["blenderPosition"])


def structure_defs():
    items = []
    for item in MANIFEST["structures"]:
        items.append(
            {
                "id": item["id"],
                "name": item["assemblyName"],
                "label": item["label"],
                "hex": item["hex"],
                "position": layout_blender(item["id"]),
                "exterior": asset_abs(item["exterior"]["sourcePath"]),
                "interior": asset_abs(item["interior"]["sourcePath"]),
                "public_exterior": os.path.join(ROOT, "apps", "balencia", "public", item["exterior"]["publicPath"]),
                "runtime_exterior": item["exterior"]["runtimePath"],
            }
        )
    return items


STRUCTURES = structure_defs()
STRUCTURE_BY_ID = {item["id"]: item for item in STRUCTURES}


def energy_approved_path(asset_id):
    for item in MANIFEST["energyAssets"]:
        if item["id"] == asset_id:
            return asset_abs(item["sourcePath"])
    raise KeyError(asset_id)


ENERGY_ASSETS = {asset_id: energy_approved_path(asset_id) for asset_id in ENERGY_IDS}


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r", encoding="utf-8") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


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
        if hasattr(mat, "use_screen_refraction"):
            mat.use_screen_refraction = False
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


def setup_render(width=1600, height=900):
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
    if hasattr(scene, "eevee"):
        eevee = scene.eevee
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
            eevee.bloom_threshold = 0.16
            eevee.bloom_intensity = 0.82
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.72


def setup_scene(width=1600, height=900):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lighting = load_python_module(os.path.join(SHARED_DIR, "lighting-rig.py"), "lighting_rig")
    lighting["clear_lighting"]()
    lighting["setup_viewport_lighting"]()
    setup_render(width, height)


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


def render_still(camera, path, frame=96, width=None, height=None):
    if width and height:
        setup_render(width, height)
    bpy.context.scene.frame_set(frame)
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def screenshot_ok(path):
    return os.path.exists(path) and os.path.getsize(path) > 8 * 1024


def source_file_bytes(paths):
    return sum(os.path.getsize(path) for path in paths if os.path.exists(path))


def create_cylinder(name, radius, depth, z, mat, collection, vertices=128, scale_y=1.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(0, 0, z))
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"{name}_mesh"
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
    glass_mat = make_material("glass", hex_to_rgba("#111827", 0.72), roughness=0.14, metallic=0.18, alpha=0.72)
    energy_mat = make_material(
        "energy",
        hex_to_rgba("#FF5E00", 1.0),
        roughness=0.24,
        emission=hex_to_rgba("#FF5E00", 1.0),
        emission_strength=0.62,
    )
    objects = [
        create_cylinder("s76_obsidian_island", radius_x, 0.035, -0.04, base_mat, collection, vertices=192, scale_y=radius_y / radius_x),
        create_cylinder("s76_central_civic_plaza", island["innerCivicRadius"], 0.045, -0.005, detail_mat, collection, vertices=128),
        create_cylinder("s76_central_reflection_pool", 13.5, 0.018, 0.03, glass_mat, collection, vertices=96),
    ]
    for radius, width, name in (
        (island["innerCivicRadius"] + 6, 0.16, "s76_inner_energy_ring"),
        (island["outerRoadRadius"], 0.13, "s76_outer_road_energy_ring"),
        (island["edgeWallRadius"], 0.12, "s76_edge_wall_energy_ring"),
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
        road = create_strip(f"s76_boulevard_to_{cfg['id']}", start, road_end, 2.2, 0.035, detail_mat, collection)
        vein = create_strip(f"s76_energy_vein_to_{cfg['id']}", start, road_end, 0.16, 0.07, energy_mat, collection)
        if road:
            objects.append(road)
        if vein:
            objects.append(vein)
    return objects


def render_exterior_contact_sheet():
    setup_scene(1800, 1500)
    cols = 4
    x_spacing = 38
    z_spacing = 37
    collection = bpy.data.collections.new("S76_Current_Exterior_Contact_Sheet")
    bpy.context.scene.collection.children.link(collection)
    for index, cfg in enumerate(STRUCTURES):
        row = index // cols
        col = index % cols
        x = (col - 1.5) * x_spacing
        z = (2 - row) * z_spacing
        imported = import_glb(cfg["exterior"], collection)
        meshes = [obj for obj in imported if obj.type == "MESH"]
        box = world_bbox(meshes)
        if not box:
            continue
        center = box["center"]
        roots = [obj for obj in imported if obj.parent is None or obj.parent not in imported]
        group = bpy.data.objects.new(f"s76_contact_{cfg['id']}", None)
        collection.objects.link(group)
        group.location = (center.x, center.y, box["min"].z)
        for root in roots:
            root.parent = group
            root.matrix_parent_inverse = group.matrix_world.inverted()
        target_height = 42 if cfg["id"] == "sia-tower" else 26
        if box["size"].z > 0.001:
            scale = target_height / box["size"].z
            group.scale = (scale, scale, scale)
        group.location = (x, 0, z)
    box = world_bbox()
    camera = make_camera("S76_Exterior_Contact", (0, -190, 62), (0, 0, 54), lens=70, ortho=160)
    path = os.path.join(ASSEMBLY_SCREENSHOTS, "s76-exterior-finish-contact-sheet.png")
    render_still(camera, path, frame=96, width=1800, height=1500)
    return path


def import_full_city():
    setup_scene(1600, 900)
    context_collection = bpy.data.collections.new("S76_City_Context")
    structures_collection = bpy.data.collections.new("S76_Approved_Structures")
    interiors_collection = bpy.data.collections.new("S76_Hidden_Interiors")
    energy_collection = bpy.data.collections.new("S76_Approved_Energy")
    for collection in (context_collection, structures_collection, interiors_collection, energy_collection):
        bpy.context.scene.collection.children.link(collection)

    context_objects = create_city_context(context_collection)
    registry = {}
    all_exteriors = []
    all_interiors = []
    missing_assets = []
    invalid_materials = []

    for cfg in STRUCTURES:
        exterior_sub = bpy.data.collections.new(f"{cfg['id']}_exterior")
        interior_sub = bpy.data.collections.new(f"{cfg['id']}_interior")
        structures_collection.children.link(exterior_sub)
        interiors_collection.children.link(interior_sub)
        for key in ("exterior", "interior", "public_exterior"):
            if not os.path.exists(cfg[key]):
                missing_assets.append(cfg[key])
        exterior = import_glb(cfg["exterior"], exterior_sub, cfg["position"])
        interior = import_glb(cfg["interior"], interior_sub, cfg["position"])
        for obj in interior:
            obj.hide_render = True
            obj.hide_viewport = True
        roots, invalid = collect_material_roots(exterior + interior)
        invalid_materials.extend(invalid)
        registry[cfg["id"]] = {
            "config": cfg,
            "exterior": exterior,
            "interior": interior,
            "bbox_exterior": world_bbox(exterior),
            "bbox_interior": world_bbox(interior),
            "material_roots": roots,
            "invalid_materials": invalid,
        }
        all_exteriors.extend(exterior)
        all_interiors.extend(interior)

    energy_registry = {}
    all_energy = []
    for asset_id, path in ENERGY_ASSETS.items():
        sub = bpy.data.collections.new(asset_id.replace("-", "_"))
        energy_collection.children.link(sub)
        if not os.path.exists(path):
            missing_assets.append(path)
        objects = import_glb(path, sub)
        roots, invalid = collect_material_roots(objects)
        invalid_materials.extend(invalid)
        energy_registry[asset_id] = {
            "path": path,
            "objects": objects,
            "bbox": world_bbox(objects),
            "material_roots": roots,
            "invalid_materials": invalid,
        }
        all_energy.extend(objects)

    return {
        "registry": registry,
        "energy_registry": energy_registry,
        "context_objects": context_objects,
        "all_exteriors": all_exteriors,
        "all_interiors": all_interiors,
        "all_energy": all_energy,
        "missing_assets": missing_assets,
        "invalid_materials": invalid_materials,
    }


def overview_configs():
    return [
        ("citywide", "s76-overview-citywide.png", runtime_to_blender((155, 128, 185)), runtime_to_blender((0, 22, 4)), 14, 144),
        ("topdown", "s76-overview-topdown.png", (0, 0, 190), (0, 0, 0), 36, 144),
        ("skyline_north", "s76-skyline-north.png", (0, 150, 58), (0, 0, 18), 24, 96),
        ("skyline_south", "s76-skyline-south.png", (0, -150, 58), (0, 0, 18), 24, 96),
        ("skyline_east", "s76-skyline-east.png", (150, 0, 58), (0, 0, 18), 24, 96),
        ("skyline_west", "s76-skyline-west.png", (-150, 0, 58), (0, 0, 18), 24, 96),
        ("energy_climax", "s76-energy-climax.png", runtime_to_blender((138, 124, 172)), runtime_to_blender((0, 25, 5)), 16, 144),
    ]


def scroll_configs():
    configs = [
        (1, "arrival", "City aerial", (155, 128, 185), (0, 22, 4), 14, 144),
        (4, "fitness-district", "Fitness district", layout_offset_runtime("fitness", (33, 17, -34)), layout_runtime("fitness", 8), 34, 96),
        (6, "finance-tower", "Finance district", layout_offset_runtime("finance", (32, 17, 20)), layout_runtime("finance", 10), 36, 96),
        (11, "career-towers", "Career district", layout_offset_runtime("career", (-31, 25, 32)), layout_runtime("career", 11.5), 35, 96),
        (15, "cross-pillar-revelation", "Cross-pillar revelation", (138, 124, 172), (0, 25, 5), 16, 144),
        (16, "today-screen-street", "Today screen street corridor", layout_offset_runtime("chat", (22, 2.9, -14)), layout_runtime("chat", 8), 32, 96),
        (17, "sia-tower-return", "SIA tower return", (0, 96, 198), (0, 30, 0), 18, 144),
    ]
    return [
        {
            "scene": scene,
            "slug": slug,
            "focus": focus,
            "loc": runtime_to_blender(loc),
            "target": runtime_to_blender(target),
            "lens": lens,
            "frame": frame,
        }
        for scene, slug, focus, loc, target, lens, frame in configs
        if scene in TARGET_SCROLL_SCENES
    ]


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


def render_image_contact_sheet(image_paths, out_path, title):
    setup_scene(1800, 1200)
    bpy.context.scene.world.color = (0.005, 0.005, 0.007)
    cols = 2
    cell_w = 16.0
    cell_h = 9.0
    pad_x = 1.2
    pad_z = 1.45
    rows = math.ceil(len(image_paths) / cols)
    text_mat = make_material("sheet_label", hex_to_rgba("#F8FAFC"), roughness=0.6)
    for index, item in enumerate(image_paths):
        row = index // cols
        col = index % cols
        x = (col - (cols - 1) / 2) * (cell_w + pad_x)
        z = ((rows - 1) / 2 - row) * (cell_h + pad_z)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0, z), rotation=(math.pi / 2, 0, 0))
        plane = bpy.context.object
        plane.name = f"s76_sheet_image_{index:02d}"
        plane.dimensions = (cell_w, cell_h, 1)
        plane.data.materials.append(make_image_material(f"s76_sheet_image_mat_{index:02d}", item["path"]))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.text_add(location=(x - cell_w * 0.49, -0.03, z + cell_h * 0.56), rotation=(math.pi / 2, 0, 0))
        text = bpy.context.object
        text.name = f"s76_sheet_label_{index:02d}"
        text.data.body = item["label"]
        text.data.align_x = "LEFT"
        text.data.align_y = "CENTER"
        text.data.size = 0.32
        text.data.materials.append(text_mat)

    bpy.ops.object.text_add(location=(-16.7, -0.03, rows * (cell_h + pad_z) * 0.5 + 0.8), rotation=(math.pi / 2, 0, 0))
    title_obj = bpy.context.object
    title_obj.name = "s76_sheet_title"
    title_obj.data.body = title
    title_obj.data.align_x = "LEFT"
    title_obj.data.align_y = "CENTER"
    title_obj.data.size = 0.48
    title_obj.data.materials.append(text_mat)

    camera = make_camera("S76_Image_Contact_Camera", (0, -31, 1), (0, 0, 1), lens=70, ortho=31)
    render_still(camera, out_path, frame=1, width=1800, height=1200)
    return out_path


def render_city_evidence():
    city = import_full_city()
    overview_paths = {}
    for key, filename, loc, target, lens, frame in overview_configs():
        path = os.path.join(ASSEMBLY_SCREENSHOTS, filename)
        camera = make_camera(f"S76_{key}", loc, target, lens=lens)
        overview_paths[key] = render_still(camera, path, frame=frame, width=1600, height=900)

    scroll_paths = {}
    for cfg in scroll_configs():
        path = os.path.join(SCROLL_SCREENSHOTS, f"scene-{cfg['scene']:02d}-{cfg['slug']}.png")
        camera = make_camera(f"S76_Scene_{cfg['scene']:02d}_{cfg['slug']}", cfg["loc"], cfg["target"], lens=cfg["lens"])
        scroll_paths[f"scene_{cfg['scene']:02d}"] = {
            "focus": cfg["focus"],
            "path": render_still(camera, path, frame=cfg["frame"], width=1600, height=900),
            "camera_location": [round(value, 4) for value in cfg["loc"]],
            "camera_target": [round(value, 4) for value in cfg["target"]],
            "lens": cfg["lens"],
            "frame": cfg["frame"],
        }

    return city, overview_paths, scroll_paths


def audit_current_assets(city):
    structure_metrics = {}
    invalid_materials = list(city["invalid_materials"])
    for cfg in STRUCTURES:
        item = city["registry"][cfg["id"]]
        layout_position = layout_blender(cfg["id"])
        structure_metrics[cfg["id"]] = {
            "label": cfg["label"],
            "exterior_path": rel(cfg["exterior"]),
            "interior_path": rel(cfg["interior"]),
            "public_exterior_path": rel(cfg["public_exterior"]),
            "runtime_exterior_path": cfg["runtime_exterior"],
            "position": [round(value, 4) for value in cfg["position"]],
            "layout_position": [round(value, 4) for value in layout_position],
            "position_matches_layout_v2": tuple(round(value, 4) for value in cfg["position"]) == tuple(round(value, 4) for value in layout_position),
            "exterior_tris": count_tris(item["exterior"]),
            "interior_tris": count_tris(item["interior"]),
            "exterior_mesh_objects": len([obj for obj in item["exterior"] if obj.type == "MESH"]),
            "interior_mesh_objects": len([obj for obj in item["interior"] if obj.type == "MESH"]),
            "exterior_size_bytes": os.path.getsize(cfg["exterior"]) if os.path.exists(cfg["exterior"]) else 0,
            "public_exterior_size_bytes": os.path.getsize(cfg["public_exterior"]) if os.path.exists(cfg["public_exterior"]) else 0,
            "bbox_exterior": bbox_dict(item["bbox_exterior"]),
            "bbox_interior": bbox_dict(item["bbox_interior"]),
            "material_roots": item["material_roots"],
            "invalid_materials": item["invalid_materials"],
            "approved_exterior_present": os.path.exists(cfg["exterior"]) and len(item["exterior"]) > 0,
            "approved_interior_present": os.path.exists(cfg["interior"]) and len(item["interior"]) > 0,
            "app_exterior_present": os.path.exists(cfg["public_exterior"]),
        }

    energy_metrics = {}
    for asset_id, item in city["energy_registry"].items():
        path = item["path"]
        energy_metrics[asset_id] = {
            "path": rel(path),
            "tris": count_tris(item["objects"]),
            "mesh_objects": len([obj for obj in item["objects"] if obj.type == "MESH"]),
            "size_bytes": os.path.getsize(path) if os.path.exists(path) else 0,
            "bbox": bbox_dict(item["bbox"]),
            "material_roots": item["material_roots"],
            "invalid_materials": item["invalid_materials"],
            "approved_asset_present": os.path.exists(path) and len(item["objects"]) > 0,
        }

    active_structure_tris = sum(item["exterior_tris"] for item in structure_metrics.values())
    interior_tris = sum(item["interior_tris"] for item in structure_metrics.values())
    energy_tris = sum(item["tris"] for item in energy_metrics.values())
    environment_tris = count_tris(city["context_objects"])
    active_city_tris = active_structure_tris + energy_tris + environment_tris
    loaded_verification_tris = active_city_tris + interior_tris

    exterior_paths = [cfg["exterior"] for cfg in STRUCTURES]
    interior_paths = [cfg["interior"] for cfg in STRUCTURES]
    energy_paths = [ENERGY_ASSETS[asset_id] for asset_id in ENERGY_IDS]
    active_source_bytes = source_file_bytes(exterior_paths + energy_paths)
    interior_source_bytes = source_file_bytes(interior_paths)

    center_positions = [Vector(layout_blender(item["id"])) for item in STRUCTURES if item["id"] != "sia-tower"]
    spacings = []
    for i, first in enumerate(center_positions):
        for second in center_positions[i + 1 :]:
            spacings.append((first - second).length)
    min_spacing = min(spacings)

    sia_height = structure_metrics["sia-tower"]["bbox_exterior"]["size"][2]
    tallest_district = max(
        value["bbox_exterior"]["size"][2]
        for key, value in structure_metrics.items()
        if key != "sia-tower" and value["bbox_exterior"]
    )
    sia_dominance_ratio = sia_height / tallest_district if tallest_district else 0

    return {
        "structure_metrics": structure_metrics,
        "energy_metrics": energy_metrics,
        "missing_assets": [rel(path) for path in city["missing_assets"]],
        "invalid_materials": invalid_materials,
        "active_structure_tris": active_structure_tris,
        "interior_tris": interior_tris,
        "energy_tris": energy_tris,
        "environment_tris": environment_tris,
        "active_city_tris": active_city_tris,
        "loaded_verification_tris": loaded_verification_tris,
        "active_source_bytes": active_source_bytes,
        "interior_source_bytes": interior_source_bytes,
        "min_spacing": min_spacing,
        "sia_dominance_ratio": sia_dominance_ratio,
    }


def baseline_metrics():
    if not os.path.exists(BASELINE_AUDIT_PATH):
        return {}
    data = load_json(BASELINE_AUDIT_PATH)
    return {item["id"]: item for item in data.get("pre_pilot_audit", [])}


def format_kb(value):
    return round(value / 1024, 1)


def write_reports(asset_audit, exterior_sheet, overview_paths, scroll_paths, overview_sheet):
    overview_report = {
        key: {"path": rel(path), "nonzero": screenshot_ok(path)}
        for key, path in overview_paths.items()
    }
    scroll_report = {
        key: {**item, "path": rel(item["path"]), "nonzero": screenshot_ok(item["path"])}
        for key, item in scroll_paths.items()
    }
    checks = {
        "all_approved_structure_exteriors_present": all(item["approved_exterior_present"] for item in asset_audit["structure_metrics"].values()),
        "all_approved_structure_interiors_present": all(item["approved_interior_present"] for item in asset_audit["structure_metrics"].values()),
        "all_app_exteriors_present": all(item["app_exterior_present"] for item in asset_audit["structure_metrics"].values()),
        "all_approved_energy_assets_present": all(item["approved_asset_present"] for item in asset_audit["energy_metrics"].values()),
        "all_positions_match_layout_v2": all(item["position_matches_layout_v2"] for item in asset_audit["structure_metrics"].values()),
        "minimum_spacing_layout_v2": asset_audit["min_spacing"] >= LAYOUT["minimumDistrictSpacing"],
        "material_roots_valid": len(asset_audit["invalid_materials"]) == 0,
        "active_city_triangle_budget": asset_audit["active_city_tris"] <= 250000,
        "active_source_file_budget": asset_audit["active_source_bytes"] <= 5 * 1024 * 1024,
        "sia_dominance_preserved": asset_audit["sia_dominance_ratio"] >= 2.0,
        "exterior_contact_sheet_nonzero": screenshot_ok(exterior_sheet),
        "city_overview_contact_sheet_nonzero": screenshot_ok(overview_sheet),
        "overview_screenshots_nonzero": all(item["nonzero"] for item in overview_report.values()),
        "scroll_screenshots_nonzero": all(item["nonzero"] for item in scroll_report.values()),
    }

    performance = {
        "session": SESSION,
        "date": str(date.today()),
        "active_scene": {
            "structure_exterior_tris": asset_audit["active_structure_tris"],
            "energy_tris": asset_audit["energy_tris"],
            "environment_tris": asset_audit["environment_tris"],
            "total_tris": asset_audit["active_city_tris"],
            "budget": "<=250K",
            "result": "PASS" if checks["active_city_triangle_budget"] else "NEEDS REVIEW",
        },
        "loaded_for_verification": {
            "interior_tris_hidden_by_default": asset_audit["interior_tris"],
            "total_tris_with_all_interiors": asset_audit["loaded_verification_tris"],
        },
        "source_glb_bytes": {
            "active_exteriors_plus_energy": asset_audit["active_source_bytes"],
            "interiors": asset_audit["interior_source_bytes"],
            "active_exteriors_plus_energy_kb": format_kb(asset_audit["active_source_bytes"]),
            "interiors_kb": format_kb(asset_audit["interior_source_bytes"]),
        },
        "layout": {
            "minimum_spacing": round(asset_audit["min_spacing"], 4),
            "budget": f">={LAYOUT['minimumDistrictSpacing']}u",
        },
        "sia_dominance_ratio": round(asset_audit["sia_dominance_ratio"], 4),
    }
    with open(PERFORMANCE_REPORT, "w", encoding="utf-8") as handle:
        json.dump(performance, handle, indent=2, sort_keys=True)

    baseline = baseline_metrics()
    comparison = {}
    for id_name, current in asset_audit["structure_metrics"].items():
        before = baseline.get(id_name)
        comparison[id_name] = {
            "label": current["label"],
            "before_tris": before.get("tris") if before else None,
            "current_tris": current["exterior_tris"],
            "tri_delta": current["exterior_tris"] - before.get("tris", current["exterior_tris"]) if before else None,
            "before_size_kb": before.get("size_kb") if before else None,
            "current_size_kb": format_kb(current["exterior_size_bytes"]),
            "before_objects": before.get("object_count") if before else None,
            "current_objects": current["exterior_mesh_objects"],
        }

    report = {
        "session": SESSION,
        "date": str(date.today()),
        "scope": "Phase 8.8 final city QA contact sheets and performance review",
        "layout_source": rel(LAYOUT_PATH),
        "layout_version": LAYOUT["version"],
        "checks": checks,
        "overall_verdict": "APPROVED" if not asset_audit["missing_assets"] and all(checks.values()) else "NEEDS REVIEW",
        "missing_assets": asset_audit["missing_assets"],
        "invalid_materials": asset_audit["invalid_materials"],
        "structure_metrics": asset_audit["structure_metrics"],
        "energy_metrics": asset_audit["energy_metrics"],
        "phase8_before_after": comparison,
        "performance_report": rel(PERFORMANCE_REPORT),
        "exterior_contact_sheet": rel(exterior_sheet),
        "city_overview_contact_sheet": rel(overview_sheet),
        "overview_screenshots": overview_report,
        "scroll_screenshots": scroll_report,
        "active_city_tris": asset_audit["active_city_tris"],
        "active_source_bytes": asset_audit["active_source_bytes"],
        "minimum_spacing": round(asset_audit["min_spacing"], 4),
        "sia_dominance_ratio": round(asset_audit["sia_dominance_ratio"], 4),
    }
    with open(REPORT_JSON, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)

    lines = [
        "# Session 76 Final Phase 8 City QA",
        "",
        f"Date: {date.today()}",
        f"Status: {'Approved' if report['overall_verdict'] == 'APPROVED' else 'Needs review'}",
        "",
        "## Summary",
        "",
        "Session 76 completed the final Phase 8 evidence pass across current approved exteriors, hidden interiors, approved energy assets, layout-v2 spacing, refreshed contact sheets, and active-city performance budgets.",
        "",
        "## Performance",
        "",
        "| Metric | Result | Gate |",
        "|--------|--------|------|",
        f"| Active city tris | {asset_audit['active_city_tris']:,} | <=250,000 |",
        f"| Structure exterior tris | {asset_audit['active_structure_tris']:,} | tracked |",
        f"| Energy tris | {asset_audit['energy_tris']:,} | tracked |",
        f"| City context tris | {asset_audit['environment_tris']:,} | tracked |",
        f"| Hidden interior tris | {asset_audit['interior_tris']:,} | on-demand only |",
        f"| Active source GLB size | {format_kb(asset_audit['active_source_bytes']):.1f} KB | <=5,120 KB |",
        f"| Minimum district spacing | {asset_audit['min_spacing']:.4f}u | >={LAYOUT['minimumDistrictSpacing']}u |",
        f"| SIA dominance ratio | {asset_audit['sia_dominance_ratio']:.4f}x | >=2.0x |",
        "",
        "## Current Exterior Results",
        "",
        "| Module | Pre-Phase-8 Tris | Session 76 Tris | Objects | Size |",
        "|--------|------------------|-----------------|---------|------|",
    ]
    for cfg in STRUCTURES:
        item = comparison[cfg["id"]]
        before = f"{item['before_tris']:,}" if item["before_tris"] is not None else "n/a"
        lines.append(
            f"| {item['label']} | {before} | {item['current_tris']:,} | "
            f"{item['current_objects']} | {item['current_size_kb']:.1f} KB |"
        )
    lines.extend(
        [
            "",
            "## QA Checks",
            "",
            "| Check | Result |",
            "|-------|--------|",
        ]
    )
    for check, passed in checks.items():
        lines.append(f"| {check.replace('_', ' ')} | {'PASS' if passed else 'FAIL'} |")
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            f"- `{rel(exterior_sheet)}`",
            f"- `{rel(overview_sheet)}`",
        ]
    )
    for key, item in overview_report.items():
        lines.append(f"- `{item['path']}`")
    for key, item in scroll_report.items():
        lines.append(f"- `{item['path']}`")
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"Overall verdict: **{report['overall_verdict']}**.",
        ]
    )
    with open(REPORT_MD, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")

    return report


def main():
    print("=" * 72)
    print("Session 76: Final Phase 8 city QA")
    print("=" * 72)
    exterior_sheet = render_exterior_contact_sheet()
    city, overview_paths, scroll_paths = render_city_evidence()
    asset_audit = audit_current_assets(city)
    sheet_items = [{"path": path, "label": key.replace("_", " ").title()} for key, path in overview_paths.items()]
    overview_sheet = render_image_contact_sheet(
        sheet_items,
        os.path.join(ASSEMBLY_SCREENSHOTS, "s76-city-overview-contact-sheet.png"),
        "Session 76 City Overview QA",
    )
    report = write_reports(asset_audit, exterior_sheet, overview_paths, scroll_paths, overview_sheet)
    print(f"Report: {REPORT_MD}")
    print(f"Performance: {PERFORMANCE_REPORT}")
    print(f"Verdict: {report['overall_verdict']}")
    for check, passed in report["checks"].items():
        print(f"  {check}: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()

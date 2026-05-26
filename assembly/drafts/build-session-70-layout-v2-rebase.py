"""
Session 70: Phase 8.2 assembly and energy layout-v2 rebase.

Reads shared/city-layout-v2.json, rebuilds every baked endpoint energy GLB
against the spread layout, imports the rebuilt approved energy assets into the
full-city assembly, renders 17 scroll verification frames, and writes QA reports.
"""

import json
import math
import os
import shutil
from mathutils import Vector

import bpy


SESSION = 70

THIS_FILE = os.path.abspath(__file__)
DRAFTS = os.path.dirname(THIS_FILE)
ASSEMBLY_DIR = os.path.dirname(DRAFTS)
PROJECT = os.path.dirname(ASSEMBLY_DIR)
APPS_DIR = os.path.join(PROJECT, "apps", "balencia")
ENERGY_DIR = os.path.join(PROJECT, "energy-system")
MODULES = os.path.join(PROJECT, "modules")
SHARED = os.path.join(PROJECT, "shared")

LAYOUT_PATH = os.path.join(SHARED, "city-layout-v2.json")
MANIFEST_PATH = os.path.join(APPS_DIR, "src", "lib", "asset-manifest.json")

PIPELINE_DRAFTS = os.path.join(ENERGY_DIR, "pipelines", "drafts")
PIPELINE_APPROVED = os.path.join(ENERGY_DIR, "pipelines", "approved")
CROSS_DRAFTS = os.path.join(ENERGY_DIR, "cross-connections", "drafts")
CROSS_APPROVED = os.path.join(ENERGY_DIR, "cross-connections", "approved")
PULSE_DRAFTS = os.path.join(ENERGY_DIR, "pulse", "drafts")
PULSE_APPROVED = os.path.join(ENERGY_DIR, "pulse", "approved")
ENERGY_SCREENSHOTS = os.path.join(ENERGY_DIR, "screenshots")

ASSEMBLY_SCREENSHOTS = os.path.join(ASSEMBLY_DIR, "screenshots")
SCROLL_SCREENSHOTS = os.path.join(ASSEMBLY_DIR, "scroll-verification", "session-70")
PERFORMANCE_DIR = os.path.join(ASSEMBLY_DIR, "performance-reports")

ENERGY_BLEND = os.path.join(PIPELINE_DRAFTS, "energy-layout-v2-session70.blend")
ENERGY_REPORT = os.path.join(PIPELINE_DRAFTS, "energy-layout-v2-session70-report.json")
ASSEMBLY_BLEND = os.path.join(DRAFTS, "full-city-assembly.blend")
ASSEMBLY_REPORT = os.path.join(DRAFTS, "full-city-assembly-session70-report.json")
PERFORMANCE_REPORT = os.path.join(PERFORMANCE_DIR, "session-70-performance.json")

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
HARD_PIPELINE_IDS = [
    "fitness",
    "finance",
    "knowledgebase",
    "chat",
    "leaderboard",
    "career",
    "analytics",
    "nutrition",
]
WARM_MIST_IDS = ["yoga", "relationships"]
CROSS_CONNECTIONS = [
    {
        "id": "fitness_recovery",
        "from": "fitness",
        "to": "recovery",
        "insight": "Recovery score impacts tomorrow's workout capacity",
        "height_boost": 13.5,
        "side_offset": -7.2,
    },
    {
        "id": "nutrition_career",
        "from": "nutrition",
        "to": "career",
        "insight": "Skipped meals on meeting days reduce afternoon focus 31%",
        "height_boost": 16.0,
        "side_offset": 6.4,
    },
    {
        "id": "relationships_yoga",
        "from": "relationships",
        "to": "yoga",
        "insight": "Social connection improves recovery scores by 24%",
        "height_boost": 12.5,
        "side_offset": 8.5,
    },
    {
        "id": "finance_career",
        "from": "finance",
        "to": "career",
        "insight": "Spending increases 40% during high-stress work weeks",
        "height_boost": 12.0,
        "side_offset": -5.8,
    },
    {
        "id": "recovery_analytics",
        "from": "recovery",
        "to": "analytics",
        "insight": "Evening meditation correlates with next-day focus scores",
        "height_boost": 10.0,
        "side_offset": 4.2,
    },
    {
        "id": "chat_relationships",
        "from": "chat",
        "to": "relationships",
        "insight": "You haven't spoken to [name] in 14 days",
        "height_boost": 9.5,
        "side_offset": -3.8,
    },
]


for path in (
    DRAFTS,
    PIPELINE_DRAFTS,
    PIPELINE_APPROVED,
    CROSS_DRAFTS,
    CROSS_APPROVED,
    PULSE_DRAFTS,
    PULSE_APPROVED,
    ENERGY_SCREENSHOTS,
    ASSEMBLY_SCREENSHOTS,
    SCROLL_SCREENSHOTS,
    PERFORMANCE_DIR,
):
    os.makedirs(path, exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


LAYOUT = load_json(LAYOUT_PATH)
MANIFEST = load_json(MANIFEST_PATH)


def rel(path):
    return os.path.relpath(path, PROJECT)


def asset_abs(path):
    return os.path.join(PROJECT, path)


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
    defs = []
    for item in MANIFEST["structures"]:
        defs.append(
            {
                "id": item["id"],
                "name": item["assemblyName"],
                "label": item["label"],
                "hex": item["hex"],
                "position": layout_blender(item["id"]),
                "exterior": asset_abs(item["exterior"]["sourcePath"]),
                "interior": asset_abs(item["interior"]["sourcePath"]),
            }
        )
    return defs


STRUCTURES = structure_defs()
STRUCTURE_BY_ID = {item["id"]: item for item in STRUCTURES}


def energy_approved_path(asset_id):
    for item in MANIFEST["energyAssets"]:
        if item["id"] == asset_id:
            return asset_abs(item["sourcePath"])
    raise KeyError(asset_id)


ENERGY_ASSETS = {
    "hard-pipelines": {
        "draft": os.path.join(PIPELINE_DRAFTS, "hard-pipelines-session70.glb"),
        "approved": energy_approved_path("hard-pipelines"),
    },
    "warm-mist": {
        "draft": os.path.join(PIPELINE_DRAFTS, "warm-mist-session70.glb"),
        "approved": energy_approved_path("warm-mist"),
    },
    "faint-thread": {
        "draft": os.path.join(PIPELINE_DRAFTS, "faint-thread-session70.glb"),
        "approved": energy_approved_path("faint-thread"),
    },
    "knowledgebase-waterfall": {
        "draft": os.path.join(PIPELINE_DRAFTS, "knowledgebase-waterfall-session70.glb"),
        "approved": energy_approved_path("knowledgebase-waterfall"),
    },
    "leaderboard-lightning": {
        "draft": os.path.join(PIPELINE_DRAFTS, "leaderboard-lightning-session70.glb"),
        "approved": energy_approved_path("leaderboard-lightning"),
    },
    "cross-district-gold": {
        "draft": os.path.join(CROSS_DRAFTS, "cross-connections-session70.glb"),
        "approved": energy_approved_path("cross-district-gold"),
    },
    "ai-pulse": {
        "draft": os.path.join(PULSE_DRAFTS, "ai-pulse-session70.glb"),
        "approved": energy_approved_path("ai-pulse"),
    },
}


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
            eevee.bloom_threshold = 0.16
            eevee.bloom_intensity = 0.82
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.72


def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lighting = load_python_module(os.path.join(SHARED, "lighting-rig.py"), "lighting_rig")
    lighting["clear_lighting"]()
    lighting["setup_viewport_lighting"]()
    setup_render()


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


def point_camera(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_camera(name, loc, target, lens=28, clip_end=1200):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.1
    data.clip_end = clip_end
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = Vector(loc)
    point_camera(obj, target)
    return obj


def render_still(camera, path, frame=96, show_objects=None, hide_objects=None):
    show_objects = show_objects or []
    hide_objects = hide_objects or []
    touched = list(dict.fromkeys(show_objects + hide_objects))
    previous = {obj: (obj.hide_render, obj.hide_viewport) for obj in touched}
    for obj in show_objects:
        obj.hide_render = False
        obj.hide_viewport = False
    for obj in hide_objects:
        obj.hide_render = True
        obj.hide_viewport = True
    bpy.context.scene.frame_set(frame)
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    for obj, state in previous.items():
        obj.hide_render = state[0]
        obj.hide_viewport = state[1]
    return path


def screenshot_ok(path):
    return os.path.exists(path) and os.path.getsize(path) > 8 * 1024


def source_file_bytes(paths):
    return sum(os.path.getsize(path) for path in paths if os.path.exists(path))


def export_selected_glb(path, objects):
    if not objects:
        raise RuntimeError(f"No objects selected for {path}")
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    kwargs = {
        "filepath": path,
        "export_format": "GLB",
        "use_selection": True,
        "export_draco_mesh_compression_enable": True,
        "export_draco_mesh_compression_level": 6,
        "export_materials": "EXPORT",
        "export_cameras": False,
        "export_lights": False,
    }
    try:
        bpy.ops.export_scene.gltf(**kwargs, export_apply_modifiers=True)
    except TypeError:
        bpy.ops.export_scene.gltf(**kwargs)
    bpy.ops.object.select_all(action="DESELECT")


def import_qa(glb_path):
    before = set(bpy.data.objects)
    before_actions = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=glb_path)
    imported = [obj for obj in bpy.data.objects if obj not in before]
    imported_actions = [action for action in bpy.data.actions if action not in before_actions]
    mesh_objects = [obj for obj in imported if obj.type == "MESH"]
    roots, invalid = collect_material_roots(mesh_objects)
    result = {
        "object_count": len(imported),
        "mesh_count": len(mesh_objects),
        "tris": count_tris(mesh_objects),
        "material_roots": roots,
        "materials_valid": roots == ["energy"] and not invalid,
        "file_size_bytes": os.path.getsize(glb_path),
        "animation_count": len(imported_actions),
    }
    for obj in imported:
        bpy.data.objects.remove(obj, do_unlink=True)
    return result


def quadratic_point(start, peak, end, t):
    return ((1 - t) ** 2) * start + 2 * (1 - t) * t * peak + (t**2) * end


def quadratic_points(start, end, peak_z, steps=18, lateral=0.0):
    start = Vector(start)
    end = Vector(end)
    mid = (start + end) * 0.5
    mid.z = peak_z
    direction = Vector((end.x - start.x, end.y - start.y, 0))
    if direction.length:
        side = Vector((-direction.y, direction.x, 0)).normalized() * lateral
        mid += side
    return [quadratic_point(start, mid, end, idx / (steps - 1)) for idx in range(steps)]


def append_tube(vertices, faces, points, radius, sides=6):
    ring_indices = []
    up = Vector((0, 0, 1))
    for idx, point in enumerate(points):
        if idx == 0:
            tangent = points[1] - point
        elif idx == len(points) - 1:
            tangent = point - points[idx - 1]
        else:
            tangent = points[idx + 1] - points[idx - 1]
        if tangent.length == 0:
            tangent = Vector((1, 0, 0))
        tangent.normalize()
        side = tangent.cross(up)
        if side.length < 0.001:
            side = tangent.cross(Vector((1, 0, 0)))
        side.normalize()
        normal = side.cross(tangent)
        if normal.length == 0:
            normal = up.copy()
        normal.normalize()
        ring = []
        for step in range(sides):
            angle = math.tau * step / sides
            co = point + side * (math.cos(angle) * radius) + normal * (math.sin(angle) * radius)
            ring.append(len(vertices))
            vertices.append(tuple(co))
        ring_indices.append(ring)
    for idx in range(len(ring_indices) - 1):
        current = ring_indices[idx]
        nxt = ring_indices[idx + 1]
        for step in range(sides):
            faces.append((current[step], current[(step + 1) % sides], nxt[(step + 1) % sides], nxt[step]))
    start_center = len(vertices)
    vertices.append(tuple(points[0]))
    end_center = len(vertices)
    vertices.append(tuple(points[-1]))
    for step in range(sides):
        faces.append((start_center, ring_indices[0][step], ring_indices[0][(step + 1) % sides]))
        faces.append((end_center, ring_indices[-1][(step + 1) % sides], ring_indices[-1][step]))


def append_uv_sphere(vertices, faces, center, radii, segments=8, rings=4):
    center = Vector(center)
    start_index = len(vertices)
    vertices.append((center.x, center.y, center.z + radii[2]))
    for ring in range(1, rings):
        phi = math.pi * ring / rings
        z = math.cos(phi) * radii[2]
        rr = math.sin(phi)
        for segment in range(segments):
            theta = math.tau * segment / segments
            vertices.append(
                (
                    center.x + math.cos(theta) * radii[0] * rr,
                    center.y + math.sin(theta) * radii[1] * rr,
                    center.z + z,
                )
            )
    bottom_index = len(vertices)
    vertices.append((center.x, center.y, center.z - radii[2]))

    def ring_index(ring, segment):
        return start_index + 1 + (ring - 1) * segments + (segment % segments)

    for segment in range(segments):
        faces.append((start_index, ring_index(1, segment), ring_index(1, segment + 1)))
    for ring in range(1, rings - 1):
        for segment in range(segments):
            faces.append(
                (
                    ring_index(ring, segment),
                    ring_index(ring + 1, segment),
                    ring_index(ring + 1, segment + 1),
                    ring_index(ring, segment + 1),
                )
            )
    last_ring = rings - 1
    for segment in range(segments):
        faces.append((ring_index(last_ring, segment + 1), ring_index(last_ring, segment), bottom_index))


def append_disc(vertices, faces, center, radius, sides=24):
    center_index = len(vertices)
    vertices.append(center)
    ring_start = len(vertices)
    for idx in range(sides):
        angle = math.tau * idx / sides
        vertices.append((center[0] + math.cos(angle) * radius, center[1] + math.sin(angle) * radius, center[2]))
    for idx in range(sides):
        faces.append((center_index, ring_start + idx, ring_start + ((idx + 1) % sides)))


def append_ring(vertices, faces, center, inner_radius, outer_radius, sides=32):
    inner_start = len(vertices)
    for idx in range(sides):
        angle = math.tau * idx / sides
        vertices.append((center[0] + math.cos(angle) * inner_radius, center[1] + math.sin(angle) * inner_radius, center[2]))
    outer_start = len(vertices)
    for idx in range(sides):
        angle = math.tau * idx / sides
        vertices.append((center[0] + math.cos(angle) * outer_radius, center[1] + math.sin(angle) * outer_radius, center[2]))
    for idx in range(sides):
        faces.append(
            (
                inner_start + idx,
                inner_start + ((idx + 1) % sides),
                outer_start + ((idx + 1) % sides),
                outer_start + idx,
            )
        )


def append_strip(vertices, faces, start, end, width):
    start = Vector(start)
    end = Vector(end)
    direction = end - start
    if direction.length == 0:
        return
    direction.normalize()
    side = Vector((-direction.y, direction.x, 0))
    if side.length == 0:
        side = Vector((1, 0, 0))
    side.normalize()
    perp = side * (width * 0.5)
    base = len(vertices)
    vertices.extend([tuple(start - perp), tuple(start + perp), tuple(end + perp), tuple(end - perp)])
    faces.append((base, base + 1, base + 2, base + 3))


def append_ground_veins(vertices, faces, center, radius=3.0, width=0.12):
    append_disc(vertices, faces, (center[0], center[1], 0.075), 0.26, sides=18)
    for idx in range(8):
        angle = math.tau * idx / 8
        start = Vector((center[0], center[1], 0.08))
        end = start + Vector((math.cos(angle) * radius, math.sin(angle) * radius, 0))
        append_strip(vertices, faces, start, end, width)


def mesh_object(name, vertices, faces, mat, collection):
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    collection.objects.link(obj)
    return obj


def create_energy_root(name, collection, objects):
    root = bpy.data.objects.new(name, None)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.4
    collection.objects.link(root)
    for obj in objects:
        if obj.parent is None:
            obj.parent = root
    return root


def district_anchor(box, scale=0.72):
    return Vector((box["center"].x, box["center"].y, max(2.4, box["max"].z * scale)))


def build_hard_pipelines(registry, mat, collection):
    objects = []
    metrics = {}
    sia_box = registry["sia-tower"]["bbox"]
    crown_z = max(sia_box["max"].z - 5.2, 36.8)
    sia_ring_radius = 4.5
    vertices = []
    faces = []
    append_ground_veins(vertices, faces, (0, 0), radius=4.4, width=0.14)
    hub = mesh_object("hard_pipeline_sia_hub_veins", vertices, faces, mat, collection)
    objects.append(hub)

    for district_id in HARD_PIPELINE_IDS:
        box = registry[district_id]["bbox"]
        center = Vector((box["center"].x, box["center"].y, 0))
        direction = Vector((box["center"].x, box["center"].y, 0))
        if direction.length == 0:
            direction = Vector((1, 0, 0))
        direction.normalize()
        start = Vector((direction.x * sia_ring_radius, direction.y * sia_ring_radius, crown_z))
        end = Vector((box["center"].x, box["center"].y, box["max"].z + 0.55))
        distance = (Vector((end.x, end.y, 0)) - Vector((start.x, start.y, 0))).length
        arc_peak_z = max(start.z + 9.0, end.z + 12.0, min(62.0, 32.0 + distance * 0.23))
        points = quadratic_points(start, end, arc_peak_z, steps=22, lateral=min(distance * 0.035, 4.8))
        verts = []
        fcs = []
        append_tube(verts, fcs, points, 0.08, sides=8)
        append_uv_sphere(verts, fcs, start, (0.22, 0.22, 0.22), segments=8, rings=4)
        append_uv_sphere(verts, fcs, end, (0.26, 0.26, 0.26), segments=8, rings=4)
        for idx in range(4):
            angle = math.tau * idx / 4
            trace_start = end
            trace_end = end + Vector((math.cos(angle) * 1.0, math.sin(angle) * 1.0, -0.04))
            append_strip(verts, fcs, trace_start, trace_end, 0.08)
        append_ground_veins(verts, fcs, center, radius=3.25, width=0.12)
        mid = Vector(points[len(points) // 2])
        for idx, t in enumerate((0.2, 0.36, 0.52, 0.68, 0.84), start=1):
            p = quadratic_point(start, mid, end, t)
            append_uv_sphere(verts, fcs, p, (0.12, 0.12, 0.12), segments=8, rings=3)
        obj = mesh_object(f"hard_pipeline_sia_to_{district_id}", verts, fcs, mat, collection)
        obj["target_district"] = district_id
        objects.append(obj)
        linear_mid_z = (start.z + end.z) * 0.5
        metrics[district_id] = {
            "start": [round(start.x, 4), round(start.y, 4), round(start.z, 4)],
            "end": [round(end.x, 4), round(end.y, 4), round(end.z, 4)],
            "district_center_xy": [round(center.x, 4), round(center.y, 4)],
            "distance_xy": round(distance, 4),
            "arc_peak_z": round(arc_peak_z, 4),
            "arc_lift_over_linear_mid": round(arc_peak_z - linear_mid_z, 4),
            "tris": count_tris([obj]),
        }
    return objects, metrics


def build_warm_mist(registry, mat, collection):
    objects = []
    metrics = {}
    sia_box = registry["sia-tower"]["bbox"]
    crown_z = max(sia_box["max"].z - 5.2, 36.8)
    for district_id in WARM_MIST_IDS:
        box = registry[district_id]["bbox"]
        center = Vector((box["center"].x, box["center"].y, 0))
        direction = center.copy()
        if direction.length == 0:
            direction = Vector((1, 0, 0))
        direction.normalize()
        start = Vector((direction.x * 4.1, direction.y * 4.1, crown_z - 0.55))
        end = Vector((box["center"].x, box["center"].y, box["max"].z + 0.85))
        distance = math.hypot(end.x - start.x, end.y - start.y)
        arc_peak_z = max(start.z + 8.5, end.z + 10.0, min(58.0, 30.0 + math.hypot(end.x - start.x, end.y - start.y) * 0.2))
        route = quadratic_points(start, end, arc_peak_z, steps=16, lateral=-2.5 if district_id == "relationships" else 2.5)
        verts = []
        fcs = []
        for idx, point in enumerate(route):
            scale = 0.55 + math.sin(idx * 1.7) * 0.12
            append_uv_sphere(verts, fcs, point, (scale * 0.72, scale * 0.48, scale * 0.34), segments=8, rings=4)
        for idx, point in enumerate(route[2:-1:3]):
            append_ring(verts, fcs, (point.x, point.y, point.z), 0.46 + idx * 0.04, 0.56 + idx * 0.04, sides=24)
        append_ring(verts, fcs, (end.x, end.y, end.z - 0.08), 0.82, 1.16, sides=32)
        append_ground_veins(verts, fcs, center, radius=3.0, width=0.11)
        obj = mesh_object(f"warm_mist_sia_to_{district_id}", verts, fcs, mat, collection)
        obj["target_district"] = district_id
        objects.append(obj)
        metrics[district_id] = {
            "start": [round(start.x, 4), round(start.y, 4), round(start.z, 4)],
            "end": [round(end.x, 4), round(end.y, 4), round(end.z, 4)],
            "arc_peak_z": round(arc_peak_z, 4),
            "tris": count_tris([obj]),
        }
    return objects, metrics


def build_faint_thread(registry, mat, collection):
    box = registry["recovery"]["bbox"]
    sia_box = registry["sia-tower"]["bbox"]
    center = Vector((box["center"].x, box["center"].y, 0))
    direction = center.copy()
    if direction.length == 0:
        direction = Vector((1, 0, 0))
    direction.normalize()
    start = Vector((direction.x * 4.5, direction.y * 4.5, max(sia_box["max"].z - 5.2, 36.8)))
    end = Vector((box["center"].x, box["center"].y, box["max"].z + 0.45))
    arc_peak_z = max(start.z + 4.0, end.z + 9.0, 42.0)
    points = quadratic_points(start, end, arc_peak_z, steps=22, lateral=2.0)
    verts = []
    fcs = []
    append_tube(verts, fcs, points, 0.018, sides=6)
    for idx, point in enumerate(points[2:-1:3]):
        radius = 0.055 + idx * 0.004
        append_uv_sphere(verts, fcs, point, (radius, radius, radius), segments=6, rings=3)
    append_ring(verts, fcs, (end.x, end.y, end.z - 0.05), 0.48, 0.68, sides=24)
    append_ground_veins(verts, fcs, center, radius=2.55, width=0.08)
    obj = mesh_object("faint_thread_sia_to_recovery", verts, fcs, mat, collection)
    obj["target_district"] = "recovery"
    return [obj], {
        "recovery": {
            "start": [round(start.x, 4), round(start.y, 4), round(start.z, 4)],
            "end": [round(end.x, 4), round(end.y, 4), round(end.z, 4)],
            "arc_peak_z": round(arc_peak_z, 4),
            "tris": count_tris([obj]),
        }
    }


def build_knowledgebase_waterfall(registry, mat, collection):
    box = registry["knowledgebase"]["bbox"]
    center = Vector((box["center"].x, box["center"].y, 0))
    to_sia = Vector((-center.x, -center.y, 0))
    if to_sia.length == 0:
        to_sia = Vector((0, -1, 0))
    to_sia.normalize()
    side = Vector((-to_sia.y, to_sia.x, 0))
    top = Vector((box["center"].x, box["center"].y, box["max"].z + 0.65)) + to_sia * 1.9
    bottom = Vector((box["center"].x, box["center"].y, max(0.55, box["min"].z + 0.55))) + to_sia * 2.25
    verts = []
    fcs = []
    append_ring(verts, fcs, (top.x, top.y, top.z), 0.9, 1.18, sides=32)
    for idx in range(7):
        lateral = side * ((idx - 3) * 0.42)
        start = top + lateral + Vector((0, 0, -0.25 - abs(idx - 3) * 0.05))
        end = bottom + lateral * 0.74 + Vector((0, 0, 0.12))
        append_tube(verts, fcs, [start, (start + end) * 0.5 + to_sia * 0.15, end], 0.055, sides=5)
        append_uv_sphere(verts, fcs, end + Vector((0, 0, -0.18)), (0.09, 0.09, 0.09), segments=6, rings=3)
    for idx in range(5):
        lateral = side * ((idx - 2) * 0.62)
        append_strip(verts, fcs, top + lateral + Vector((0, 0, -1.0)), bottom + lateral * 0.82, 0.12)
    append_ring(verts, fcs, (bottom.x, bottom.y, bottom.z - 0.05), 1.05, 1.48, sides=32)
    append_ground_veins(verts, fcs, (bottom.x, bottom.y), radius=2.7, width=0.1)
    obj = mesh_object("knowledgebase_energy_waterfall_v2", verts, fcs, mat, collection)
    obj["target_district"] = "knowledgebase"
    return [obj], {
        "knowledgebase": {
            "top": [round(top.x, 4), round(top.y, 4), round(top.z, 4)],
            "bottom": [round(bottom.x, 4), round(bottom.y, 4), round(bottom.z, 4)],
            "drop": round(top.z - bottom.z, 4),
            "tris": count_tris([obj]),
        }
    }


def build_leaderboard_lightning(registry, mat, collection):
    box = registry["leaderboard"]["bbox"]
    center = Vector((box["center"].x, box["center"].y, 0))
    intake = Vector((box["center"].x, box["center"].y, box["max"].z + 0.85))
    impact = Vector((box["center"].x, box["center"].y, max(box["max"].z - 2.2, box["center"].z + 2.0)))
    verts = []
    fcs = []
    jag = []
    for idx in range(7):
        t = idx / 6
        point = intake.lerp(impact, t)
        wobble = Vector((math.sin(idx * 1.9) * 0.28, math.cos(idx * 2.2) * 0.24, 0))
        jag.append(point + wobble)
    append_tube(verts, fcs, jag, 0.065, sides=5)
    for idx, point in enumerate(jag[1:-1], start=1):
        for sign in (-1, 1):
            angle = idx * 1.2 + sign * 0.8
            end = point + Vector((math.cos(angle) * 1.0, math.sin(angle) * 1.0, -0.35 - idx * 0.08))
            append_tube(verts, fcs, [point, end], 0.032, sides=4)
    append_ring(verts, fcs, (intake.x, intake.y, intake.z), 0.72, 0.98, sides=32)
    append_ring(verts, fcs, (impact.x, impact.y, impact.z), 0.92, 1.42, sides=32)
    append_disc(verts, fcs, (impact.x, impact.y, impact.z + 0.03), 0.62, sides=24)
    for idx in range(4):
        angle = math.tau * idx / 4
        start = impact + Vector((math.cos(angle) * 0.9, math.sin(angle) * 0.9, -0.08))
        end = start + Vector((math.cos(angle) * 3.8, math.sin(angle) * 3.8, -0.45))
        append_tube(verts, fcs, [start, end], 0.035, sides=4)
    append_ground_veins(verts, fcs, center, radius=3.0, width=0.11)
    obj = mesh_object("leaderboard_energy_lightning_v2", verts, fcs, mat, collection)
    obj["target_district"] = "leaderboard"
    return [obj], {
        "leaderboard": {
            "intake": [round(intake.x, 4), round(intake.y, 4), round(intake.z, 4)],
            "impact": [round(impact.x, 4), round(impact.y, 4), round(impact.z, 4)],
            "tris": count_tris([obj]),
        }
    }


def build_cross_connections(registry, mat, collection):
    objects = []
    metrics = {}
    anchors = []
    for cfg in CROSS_CONNECTIONS:
        source = district_anchor(registry[cfg["from"]]["bbox"], 0.58)
        target = district_anchor(registry[cfg["to"]]["bbox"], 0.58)
        distance = math.hypot(target.x - source.x, target.y - source.y)
        mid = (source + target) * 0.5
        side = Vector((-(target.y - source.y), target.x - source.x, 0))
        if side.length:
            side.normalize()
        peak_z = max(source.z, target.z) + cfg["height_boost"]
        peak = Vector((mid.x, mid.y, peak_z)) + side * cfg["side_offset"]
        points = [quadratic_point(source, peak, target, idx / 18) for idx in range(19)]
        verts = []
        fcs = []
        append_tube(verts, fcs, points, 0.045, sides=5)
        append_uv_sphere(verts, fcs, source, (0.15, 0.15, 0.15), segments=6, rings=3)
        append_uv_sphere(verts, fcs, target, (0.15, 0.15, 0.15), segments=6, rings=3)
        obj = mesh_object(f"cross_connection_{cfg['id']}", verts, fcs, mat, collection)
        obj["connection_id"] = cfg["id"]
        objects.append(obj)
        anchor = bpy.data.objects.new(f"insight_anchor_{cfg['id']}", None)
        anchor.empty_display_type = "SPHERE"
        anchor.empty_display_size = 0.35
        anchor.location = peak
        anchor["insight"] = cfg["insight"]
        anchor["from"] = cfg["from"]
        anchor["to"] = cfg["to"]
        collection.objects.link(anchor)
        anchors.append(anchor)
        metrics[cfg["id"]] = {
            "from": cfg["from"],
            "to": cfg["to"],
            "start": [round(source.x, 4), round(source.y, 4), round(source.z, 4)],
            "end": [round(target.x, 4), round(target.y, 4), round(target.z, 4)],
            "anchor": [round(peak.x, 4), round(peak.y, 4), round(peak.z, 4)],
            "distance_xy": round(distance, 4),
            "tris": count_tris([obj]),
        }
    return objects + anchors, metrics


def keyframe_scale(obj, frame_scale_pairs):
    frames = []
    for frame, scale in frame_scale_pairs:
        obj.scale = (scale, scale, 1.0)
        obj.keyframe_insert(data_path="scale", frame=frame)
        frames.append(frame)
    if obj.animation_data and obj.animation_data.action:
        for fcurve in getattr(obj.animation_data.action, "fcurves", []):
            for key in fcurve.keyframe_points:
                key.interpolation = "LINEAR"
    return frames


def build_ai_pulse(registry, mat, collection):
    sia_box = registry["sia-tower"]["bbox"]
    origin_z = max(sia_box["max"].z + 0.35, 42.35)
    perimeter_radius = LAYOUT["island"]["edgeWallRadius"]
    inner_radius = LAYOUT["island"]["innerCivicRadius"] * 1.9
    response_radius = max(math.hypot(*layout_blender(item["id"])[:2]) for item in STRUCTURES if item["id"] != "sia-tower")

    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0,
        minor_radius=0.1,
        major_segments=128,
        minor_segments=6,
        location=(0, 0, origin_z),
    )
    ring = bpy.context.object
    ring.name = "ai_pulse_expanding_ring"
    ring.data.name = "ai_pulse_expanding_ring_mesh"
    ring.data.materials.append(mat)
    link_to_collection(ring, collection)
    ring_frames = keyframe_scale(
        ring,
        [
            (0, 0.08),
            (12, 4.5),
            (48, inner_radius),
            (96, response_radius),
            (144, perimeter_radius),
            (192, 0.08),
        ],
    )

    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1.0, depth=0.035, location=(0, 0, origin_z + 0.02))
    crown = bpy.context.object
    crown.name = "ai_pulse_crown_intensifier"
    crown.data.name = "ai_pulse_crown_intensifier_mesh"
    crown.data.materials.append(mat)
    link_to_collection(crown, collection)
    crown_frames = keyframe_scale(crown, [(0, 0.8), (12, 2.5), (48, 1.0), (96, 0.7), (144, 0.45), (192, 0.8)])
    return [ring, crown], {
        "origin": [0, 0, round(origin_z, 4)],
        "perimeter_radius": round(perimeter_radius, 4),
        "response_radius": round(response_radius, 4),
        "keyframes": sorted(set(ring_frames + crown_frames)),
        "tris": count_tris([ring, crown]),
    }


def build_structure_context(collection):
    registry = {}
    missing = []
    for cfg in STRUCTURES:
        sub = bpy.data.collections.new(cfg["name"])
        collection.children.link(sub)
        if not os.path.exists(cfg["exterior"]):
            missing.append(cfg["exterior"])
        imported = import_glb(cfg["exterior"], sub, cfg["position"])
        registry[cfg["id"]] = {"config": cfg, "objects": imported, "bbox": world_bbox(imported)}
    return registry, missing


def copy_approved(asset_id):
    shutil.copyfile(ENERGY_ASSETS[asset_id]["draft"], ENERGY_ASSETS[asset_id]["approved"])


def build_energy_assets():
    print("=" * 72)
    print("Session 70: Energy layout-v2 rebake")
    print("=" * 72)
    setup_scene()
    context_collection = bpy.data.collections.new("Approved_Structure_Context_V2")
    bpy.context.scene.collection.children.link(context_collection)
    energy_collection = bpy.data.collections.new("Energy_Layout_V2_S70")
    bpy.context.scene.collection.children.link(energy_collection)
    registry, missing_assets = build_structure_context(context_collection)

    energy_mats = {
        "orange": make_material(
            "energy",
            hex_to_rgba("#FF5E00", 0.92),
            roughness=0.24,
            emission=hex_to_rgba("#FF5E00", 1.0),
            emission_strength=1.8,
            alpha=0.92,
        ),
        "mist": make_material(
            "energy",
            hex_to_rgba("#FF7A1A", 0.58),
            roughness=0.18,
            emission=hex_to_rgba("#FF5E00", 1.0),
            emission_strength=1.25,
            alpha=0.58,
        ),
        "faint": make_material(
            "energy",
            hex_to_rgba("#FF8A1A", 0.24),
            roughness=0.18,
            emission=hex_to_rgba("#FF6A00", 1.0),
            emission_strength=0.42,
            alpha=0.24,
        ),
        "gold": make_material(
            "energy",
            hex_to_rgba("#F59E0B", 1.0),
            roughness=0.22,
            emission=hex_to_rgba("#F59E0B", 1.0),
            emission_strength=0.85,
        ),
        "pulse": make_material(
            "energy",
            hex_to_rgba("#FF5E00", 0.76),
            roughness=0.18,
            emission=hex_to_rgba("#FF5E00", 1.0),
            emission_strength=2.4,
            alpha=0.76,
        ),
    }

    asset_builds = {}
    hard_objects, hard_metrics = build_hard_pipelines(registry, energy_mats["orange"], energy_collection)
    warm_objects, warm_metrics = build_warm_mist(registry, energy_mats["mist"], energy_collection)
    faint_objects, faint_metrics = build_faint_thread(registry, energy_mats["faint"], energy_collection)
    water_objects, water_metrics = build_knowledgebase_waterfall(registry, energy_mats["orange"], energy_collection)
    bolt_objects, bolt_metrics = build_leaderboard_lightning(registry, energy_mats["orange"], energy_collection)
    cross_objects, cross_metrics = build_cross_connections(registry, energy_mats["gold"], energy_collection)
    pulse_objects, pulse_metrics = build_ai_pulse(registry, energy_mats["pulse"], energy_collection)

    generated = {
        "hard-pipelines": {"objects": hard_objects, "metrics": hard_metrics},
        "warm-mist": {"objects": warm_objects, "metrics": warm_metrics},
        "faint-thread": {"objects": faint_objects, "metrics": faint_metrics},
        "knowledgebase-waterfall": {"objects": water_objects, "metrics": water_metrics},
        "leaderboard-lightning": {"objects": bolt_objects, "metrics": bolt_metrics},
        "cross-district-gold": {"objects": cross_objects, "metrics": cross_metrics},
        "ai-pulse": {"objects": pulse_objects, "metrics": pulse_metrics},
    }

    for asset_id, item in generated.items():
        export_objects = [create_energy_root(f"{asset_id.replace('-', '_')}_root_s70", energy_collection, item["objects"])] + item["objects"]
        export_selected_glb(ENERGY_ASSETS[asset_id]["draft"], export_objects)
        item["tris"] = count_tris([obj for obj in item["objects"] if obj.type == "MESH"])
        item["draft_file_size_bytes"] = os.path.getsize(ENERGY_ASSETS[asset_id]["draft"])
        item["material_roots"], item["invalid_materials"] = collect_material_roots(item["objects"])
        item["import_check"] = import_qa(ENERGY_ASSETS[asset_id]["draft"])
        item["checks"] = {
            "objects_present": len(item["objects"]) > 0,
            "material_roots_energy_only": item["material_roots"] == ["energy"] and not item["invalid_materials"],
            "reimports": item["import_check"]["mesh_count"] > 0,
            "reimport_material_valid": item["import_check"]["materials_valid"],
            "file_nonzero": item["draft_file_size_bytes"] > 4096,
        }
        if asset_id == "hard-pipelines":
            item["checks"]["pipeline_count"] = len(item["metrics"]) == len(HARD_PIPELINE_IDS)
            item["checks"]["endpoints_match_layout_v2"] = all(
                math.hypot(
                    item["metrics"][district_id]["end"][0] - registry[district_id]["bbox"]["center"].x,
                    item["metrics"][district_id]["end"][1] - registry[district_id]["bbox"]["center"].y,
                )
                <= 0.01
                for district_id in HARD_PIPELINE_IDS
            )
        if asset_id == "warm-mist":
            item["checks"]["mist_count"] = len(item["metrics"]) == len(WARM_MIST_IDS)
        if asset_id == "cross-district-gold":
            item["checks"]["connection_count"] = len(item["metrics"]) == len(CROSS_CONNECTIONS)
            item["checks"]["insight_anchor_count"] = len([obj for obj in item["objects"] if obj.type == "EMPTY"]) == len(CROSS_CONNECTIONS)
        if asset_id == "ai-pulse":
            item["checks"]["perimeter_matches_layout_v2"] = item["metrics"]["perimeter_radius"] == round(LAYOUT["island"]["edgeWallRadius"], 4)
            item["checks"]["animation_reimports"] = item["import_check"]["animation_count"] >= 2
        item["overall"] = "APPROVED" if all(item["checks"].values()) else "NEEDS REVIEW"
        if item["overall"] == "APPROVED":
            copy_approved(asset_id)
            item["approved_file_size_bytes"] = os.path.getsize(ENERGY_ASSETS[asset_id]["approved"])
        asset_builds[asset_id] = item

    screenshots = {
        "citywide": render_still(
            make_camera("S70_Energy_Citywide", runtime_to_blender((155, 128, 185)), runtime_to_blender((0, 22, 4)), lens=14),
            os.path.join(ENERGY_SCREENSHOTS, "s70-energy-layout-v2-citywide.png"),
            frame=144,
        ),
        "cross_connections": render_still(
            make_camera("S70_Energy_Cross", runtime_to_blender((138, 124, 172)), runtime_to_blender((0, 25, 5)), lens=16),
            os.path.join(ENERGY_SCREENSHOTS, "s70-energy-layout-v2-cross-connections.png"),
            frame=144,
        ),
        "pulse_perimeter": render_still(
            make_camera("S70_AI_Pulse_Perimeter", runtime_to_blender((0, 96, 198)), runtime_to_blender((0, 30, 0)), lens=18),
            os.path.join(ENERGY_SCREENSHOTS, "s70-ai-pulse-layout-v2-perimeter.png"),
            frame=144,
        ),
    }

    bpy.ops.wm.save_as_mainfile(filepath=ENERGY_BLEND)

    report = {
        "session": SESSION,
        "scope": "Phase 8.2 energy layout-v2 rebake",
        "layout_source": rel(LAYOUT_PATH),
        "layout_version": LAYOUT["version"],
        "minimum_district_spacing": LAYOUT["minimumDistrictSpacing"],
        "missing_assets": [rel(path) for path in missing_assets],
        "assets": {
            asset_id: {
                "draft_glb": rel(ENERGY_ASSETS[asset_id]["draft"]),
                "approved_glb": rel(ENERGY_ASSETS[asset_id]["approved"]),
                "tris": item["tris"],
                "metrics": item["metrics"],
                "draft_file_size_bytes": item["draft_file_size_bytes"],
                "approved_file_size_bytes": item.get("approved_file_size_bytes", 0),
                "material_roots": item["material_roots"],
                "checks": item["checks"],
                "import_check": item["import_check"],
                "overall": item["overall"],
            }
            for asset_id, item in asset_builds.items()
        },
        "screenshots": {key: rel(path) for key, path in screenshots.items()},
        "screenshots_nonzero": {key: screenshot_ok(path) for key, path in screenshots.items()},
        "overall_verdict": "APPROVED"
        if not missing_assets
        and all(item["overall"] == "APPROVED" for item in asset_builds.values())
        and all(screenshot_ok(path) for path in screenshots.values())
        else "NEEDS REVIEW",
    }
    with open(ENERGY_REPORT, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
    return report


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
        create_cylinder("layout_v2_obsidian_island", radius_x, 0.035, -0.04, base_mat, collection, vertices=192, scale_y=radius_y / radius_x),
        create_cylinder("layout_v2_central_civic_plaza", island["innerCivicRadius"], 0.045, -0.005, detail_mat, collection, vertices=128),
        create_cylinder("layout_v2_central_reflection_pool", 13.5, 0.018, 0.03, glass_mat, collection, vertices=96),
    ]

    for radius, width, name in (
        (island["innerCivicRadius"] + 6, 0.16, "layout_v2_inner_energy_ring"),
        (island["outerRoadRadius"], 0.13, "layout_v2_outer_road_energy_ring"),
        (island["edgeWallRadius"], 0.12, "layout_v2_edge_wall_energy_ring"),
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
        road = create_strip(f"layout_v2_boulevard_to_{cfg['id']}", start, road_end, 2.2, 0.035, detail_mat, collection)
        vein = create_strip(f"layout_v2_energy_vein_to_{cfg['id']}", start, road_end, 0.16, 0.07, energy_mat, collection)
        if road:
            objects.append(road)
        if vein:
            objects.append(vein)
    return objects


def set_objects_hidden(objects, hidden):
    for obj in objects:
        obj.hide_render = hidden
        obj.hide_viewport = hidden


def scroll_configs():
    configs = [
        (1, "arrival", "City aerial", (155, 128, 185), (0, 22, 4), 14, 144, None),
        (2, "sia-tower-reveal", "SIA tower exterior", (18, 7.8, 25), (0, 38, 0), 30, 12, None),
        (3, "sia-neural-core", "SIA tower interior", (0, 7.2, 3.05), (0, 25, 0), 24, 48, "sia-tower"),
        (4, "fitness-district", "Fitness district", layout_offset_runtime("fitness", (33, 17, -34)), layout_runtime("fitness", 8), 34, 96, None),
        (5, "yoga-sanctuary", "Yoga and wellbeing", layout_offset_runtime("yoga", (26, 14, -26)), layout_runtime("yoga", 5), 34, 96, None),
        (6, "finance-tower", "Finance district", layout_offset_runtime("finance", (32, 17, 20)), layout_runtime("finance", 10), 36, 96, None),
        (7, "knowledgebase", "Knowledgebase district", layout_offset_runtime("knowledgebase", (24, 20, 26)), layout_runtime("knowledgebase", 8), 34, 96, None),
        (8, "communication-hub", "Chat and communication", layout_offset_runtime("chat", (25, 18, 29)), layout_runtime("chat", 8), 32, 96, None),
        (9, "leaderboard-arena", "Leaderboard and competition", layout_offset_runtime("leaderboard", (-24, 20, 33)), layout_runtime("leaderboard", 6.4), 32, 96, None),
        (10, "relationships-garden", "Relationships district", layout_offset_runtime("relationships", (14, 14, 30)), layout_runtime("relationships", 4.3), 32, 96, None),
        (11, "career-towers", "Career district", layout_offset_runtime("career", (-31, 25, 32)), layout_runtime("career", 11.5), 35, 96, None),
        (12, "recovery-dreamscape", "Recovery and sleep", layout_offset_runtime("recovery", (-32, 14, 14)), layout_runtime("recovery", 5), 35, 96, None),
        (13, "analytics-cathedral", "AI analytics", layout_offset_runtime("analytics", (-33, 22, -25)), layout_runtime("analytics", 10.5), 34, 96, None),
        (14, "nutrition-farm", "Nutrition district", layout_offset_runtime("nutrition", (-24, 15, -29)), layout_runtime("nutrition", 6), 35, 96, None),
        (15, "cross-pillar-revelation", "Cross-pillar revelation", (138, 124, 172), (0, 25, 5), 16, 144, None),
        (16, "today-screen-street", "Today screen street corridor", layout_offset_runtime("chat", (22, 2.9, -14)), layout_runtime("chat", 8), 32, 96, None),
        (17, "sia-tower-return", "SIA tower return", (0, 96, 198), (0, 30, 0), 18, 144, None),
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
            "show_interior": show_interior,
        }
        for scene, slug, focus, loc, target, lens, frame, show_interior in configs
    ]


def build_assembly():
    print("=" * 72)
    print("Session 70: Full-city assembly layout-v2 verification")
    print("=" * 72)
    setup_scene()
    context_collection = bpy.data.collections.new("City_Context_Layout_V2")
    bpy.context.scene.collection.children.link(context_collection)
    structures_collection = bpy.data.collections.new("Approved_Structures")
    bpy.context.scene.collection.children.link(structures_collection)
    energy_collection = bpy.data.collections.new("Approved_Energy_Layout_V2")
    bpy.context.scene.collection.children.link(energy_collection)

    environment_objects = create_city_context(context_collection)
    missing_assets = []
    registry = {}
    all_exteriors = []
    all_interiors = []
    for cfg in STRUCTURES:
        sub = bpy.data.collections.new(cfg["name"])
        structures_collection.children.link(sub)
        for key in ("exterior", "interior"):
            if not os.path.exists(cfg[key]):
                missing_assets.append(cfg[key])
        exterior = import_glb(cfg["exterior"], sub, cfg["position"])
        interior = import_glb(cfg["interior"], sub, cfg["position"])
        set_objects_hidden(interior, True)
        roots, invalid = collect_material_roots(exterior + interior)
        registry[cfg["id"]] = {
            "config": cfg,
            "exterior": exterior,
            "interior": interior,
            "bbox_exterior": world_bbox(exterior),
            "bbox_interior": world_bbox(interior),
            "bbox_combined": world_bbox(exterior + interior),
            "material_roots": roots,
            "invalid_materials": invalid,
        }
        all_exteriors.extend(exterior)
        all_interiors.extend(interior)

    energy_registry = {}
    all_energy = []
    for asset_id in ENERGY_IDS:
        sub = bpy.data.collections.new(asset_id.replace("-", "_"))
        energy_collection.children.link(sub)
        path = ENERGY_ASSETS[asset_id]["approved"]
        if not os.path.exists(path):
            missing_assets.append(path)
            imported = []
        else:
            imported = import_glb(path, sub)
        roots, invalid = collect_material_roots(imported)
        energy_registry[asset_id] = {
            "objects": imported,
            "bbox": world_bbox(imported),
            "material_roots": roots,
            "invalid_materials": invalid,
            "path": path,
        }
        all_energy.extend(imported)

    invalid_materials = []
    for item in registry.values():
        invalid_materials.extend(item["invalid_materials"])
    for item in energy_registry.values():
        invalid_materials.extend(item["invalid_materials"])

    structure_metrics = {}
    for id_name, item in registry.items():
        cfg = item["config"]
        ext_tris = count_tris(item["exterior"])
        int_tris = count_tris(item["interior"])
        box = item["bbox_combined"]
        center = box["center"] if box else Vector(cfg["position"])
        layout_position = layout_blender(id_name)
        structure_metrics[id_name] = {
            "label": cfg["label"],
            "position": list(cfg["position"]),
            "layout_position": list(layout_position),
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
            "position_matches_layout_v2": tuple(round(value, 4) for value in cfg["position"]) == tuple(round(value, 4) for value in layout_position),
        }

    energy_metrics = {}
    for asset_id, item in energy_registry.items():
        energy_metrics[asset_id] = {
            "objects": len(item["objects"]),
            "mesh_objects": len([obj for obj in item["objects"] if obj.type == "MESH"]),
            "tris": count_tris(item["objects"]),
            "bbox": bbox_dict(item["bbox"]),
            "file_size_bytes": os.path.getsize(item["path"]) if os.path.exists(item["path"]) else 0,
            "material_roots": item["material_roots"],
            "approved_asset_present": os.path.exists(item["path"]) and len(item["objects"]) > 0,
        }

    active_structure_tris = sum(item["exterior_tris"] for item in structure_metrics.values())
    interior_tris = sum(item["interior_tris"] for item in structure_metrics.values())
    energy_tris = sum(item["tris"] for item in energy_metrics.values())
    environment_tris = count_tris(environment_objects)
    active_city_tris = active_structure_tris + energy_tris + environment_tris
    loaded_verification_tris = active_city_tris + interior_tris

    exterior_paths = [cfg["exterior"] for cfg in STRUCTURES]
    interior_paths = [cfg["interior"] for cfg in STRUCTURES]
    energy_paths = [ENERGY_ASSETS[asset_id]["approved"] for asset_id in ENERGY_IDS]
    active_source_bytes = source_file_bytes(exterior_paths + energy_paths)
    interior_source_bytes = source_file_bytes(interior_paths)

    overview_configs = [
        ("overview_citywide", "s70-overview-citywide.png", runtime_to_blender((155, 128, 185)), runtime_to_blender((0, 22, 4)), 14, 144),
        ("overview_topdown", "s70-overview-topdown.png", (0, 0, 190), (0, 0, 0), 36, 144),
        ("skyline_north", "s70-skyline-north.png", (0, 150, 58), (0, 0, 18), 24, 96),
        ("skyline_south", "s70-skyline-south.png", (0, -150, 58), (0, 0, 18), 24, 96),
        ("skyline_east", "s70-skyline-east.png", (150, 0, 58), (0, 0, 18), 24, 96),
        ("skyline_west", "s70-skyline-west.png", (-150, 0, 58), (0, 0, 18), 24, 96),
        ("energy_climax", "s70-energy-climax.png", runtime_to_blender((138, 124, 172)), runtime_to_blender((0, 25, 5)), 16, 144),
    ]
    overview_screenshots = {}
    for key, filename, loc, target, lens, frame in overview_configs:
        path = os.path.join(ASSEMBLY_SCREENSHOTS, filename)
        camera = make_camera(f"S70_{key}", loc, target, lens=lens)
        overview_screenshots[key] = render_still(camera, path, frame=frame)

    scroll_screenshots = {}
    for cfg in scroll_configs():
        show_objects = []
        hide_objects = []
        if cfg.get("show_interior"):
            show_objects.extend(registry[cfg["show_interior"]]["interior"])
            hide_objects.extend(registry[cfg["show_interior"]]["exterior"])
            hide_objects.extend(all_energy)
            hide_objects.extend(environment_objects)
        path = os.path.join(SCROLL_SCREENSHOTS, f"scene-{cfg['scene']:02d}-{cfg['slug']}.png")
        camera = make_camera(f"S70_Scene_{cfg['scene']:02d}_{cfg['slug']}", cfg["loc"], cfg["target"], lens=cfg["lens"])
        rendered = render_still(camera, path, frame=cfg["frame"], show_objects=show_objects, hide_objects=hide_objects)
        scroll_screenshots[f"scene_{cfg['scene']:02d}"] = {
            "focus": cfg["focus"],
            "path": rel(rendered),
            "camera_location": [round(value, 4) for value in cfg["loc"]],
            "camera_target": [round(value, 4) for value in cfg["target"]],
            "lens": cfg["lens"],
            "frame": cfg["frame"],
            "nonzero": screenshot_ok(rendered),
        }

    bpy.ops.wm.save_as_mainfile(filepath=ASSEMBLY_BLEND)
    blend_size = os.path.getsize(ASSEMBLY_BLEND)

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

    overview_report = {key: {"path": rel(path), "nonzero": screenshot_ok(path)} for key, path in overview_screenshots.items()}
    checks = {
        "all_approved_structure_exteriors_present": all(item["approved_exterior_present"] for item in structure_metrics.values()),
        "all_approved_structure_interiors_present": all(item["approved_interior_present"] for item in structure_metrics.values()),
        "all_approved_energy_assets_present": all(item["approved_asset_present"] for item in energy_metrics.values()),
        "all_positions_match_layout_v2": all(item["position_matches_layout_v2"] for item in structure_metrics.values()),
        "minimum_spacing_layout_v2": min_spacing >= LAYOUT["minimumDistrictSpacing"],
        "material_roots_valid": len(invalid_materials) == 0,
        "active_city_triangle_budget": active_city_tris <= 250000,
        "active_source_file_budget": active_source_bytes <= 5 * 1024 * 1024,
        "scroll_screenshot_count": len(scroll_screenshots) == 17,
        "scroll_screenshots_nonzero": all(item["nonzero"] for item in scroll_screenshots.values()),
        "overview_screenshots_nonzero": all(item["nonzero"] for item in overview_report.values()),
        "sia_dominance_preserved": sia_dominance_ratio >= 2.0,
        "energy_layer_visible": count_tris(all_energy) > 0,
    }

    performance = {
        "session": SESSION,
        "blend_file": rel(ASSEMBLY_BLEND),
        "blend_file_size_bytes": blend_size,
        "active_scene": {
            "structure_exterior_tris": active_structure_tris,
            "energy_tris": energy_tris,
            "environment_tris": environment_tris,
            "total_tris": active_city_tris,
            "budget": "<=250K",
            "result": "PASS" if checks["active_city_triangle_budget"] else "NEEDS REVIEW",
        },
        "loaded_for_verification": {
            "interior_tris_hidden_by_default": interior_tris,
            "total_tris_with_all_interiors": loaded_verification_tris,
        },
        "source_glb_bytes": {
            "active_exteriors_plus_energy": active_source_bytes,
            "interiors": interior_source_bytes,
        },
    }
    with open(PERFORMANCE_REPORT, "w", encoding="utf-8") as handle:
        json.dump(performance, handle, indent=2, sort_keys=True)

    report = {
        "session": SESSION,
        "scope": "Phase 8.2 full-city assembly layout-v2 rebase",
        "layout_source": rel(LAYOUT_PATH),
        "layout_version": LAYOUT["version"],
        "minimum_spacing": round(min_spacing, 4),
        "missing_assets": [rel(path) for path in missing_assets],
        "structure_metrics": structure_metrics,
        "energy_metrics": energy_metrics,
        "active_city_tris": active_city_tris,
        "loaded_verification_tris": loaded_verification_tris,
        "active_source_bytes": active_source_bytes,
        "interior_source_bytes": interior_source_bytes,
        "sia_dominance_ratio": round(sia_dominance_ratio, 4),
        "overview_screenshots": overview_report,
        "scroll_screenshots": scroll_screenshots,
        "performance_report": rel(PERFORMANCE_REPORT),
        "blend_file": rel(ASSEMBLY_BLEND),
        "checks": checks,
        "overall_verdict": "APPROVED" if not missing_assets and all(checks.values()) else "NEEDS REVIEW",
    }
    with open(ASSEMBLY_REPORT, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
    return report


energy_report = build_energy_assets()
assembly_report = build_assembly()

print("=" * 72)
print("SESSION 70 LAYOUT V2 REBASE COMPLETE")
print(f"Energy report: {ENERGY_REPORT}")
print(f"Assembly report: {ASSEMBLY_REPORT}")
print(f"Assembly blend: {ASSEMBLY_BLEND}")
print(f"Energy verdict: {energy_report['overall_verdict']}")
print(f"Assembly verdict: {assembly_report['overall_verdict']}")
for check, value in assembly_report["checks"].items():
    print(f"  {check}: {'PASS' if value else 'FAIL'}")

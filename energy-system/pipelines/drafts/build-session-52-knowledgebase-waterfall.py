"""
Session 52: Phase 5 Knowledgebase waterfall special delivery.

Builds the downward SIA energy cascade on the Knowledgebase facade, renders
QA evidence, exports a draft GLB, and promotes it when checks pass.
"""

import json
import math
import os
import shutil
from mathutils import Vector

import bpy


THIS_FILE = os.path.abspath(__file__)
DRAFTS = os.path.dirname(THIS_FILE)
PIPELINES_DIR = os.path.dirname(DRAFTS)
ENERGY_DIR = os.path.dirname(PIPELINES_DIR)
PROJECT = os.path.dirname(ENERGY_DIR)
MODULES = os.path.join(PROJECT, "modules")
SHARED = os.path.join(PROJECT, "shared")
SCREENSHOTS = os.path.join(ENERGY_DIR, "screenshots")
APPROVED = os.path.join(PIPELINES_DIR, "approved")
SESSION_REPORT = os.path.join(DRAFTS, "knowledgebase-waterfall-session52-report.json")
SESSION_BLEND = os.path.join(DRAFTS, "knowledgebase-waterfall-session52.blend")
DRAFT_GLB = os.path.join(DRAFTS, "knowledgebase-waterfall-session52.glb")
APPROVED_GLB = os.path.join(APPROVED, "knowledgebase-waterfall.glb")
HARD_PIPELINES_GLB = os.path.join(APPROVED, "hard-pipelines.glb")
WARM_MIST_GLB = os.path.join(APPROVED, "warm-mist.glb")
FAINT_THREAD_GLB = os.path.join(APPROVED, "faint-thread.glb")
LATEST_LAYOUT_REPORT = os.path.join(
    MODULES, "11-nutrition", "integration-session-48-report.json"
)

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
        "exterior": os.path.join(MODULES, "02-yoga-wellbeing/exterior/approved/yoga-ext.glb"),
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
        "receptor": "SIA-facing crown lip feeding a facade energy waterfall",
    },
    {
        "name": "Chat",
        "label": "Chat & Communication",
        "position": (19, -36, 0),
        "exterior": os.path.join(MODULES, "05-chat-communication/exterior/approved/chat-ext.glb"),
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


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r", encoding="utf-8") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


def setup_render():
    scene = bpy.context.scene
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
            eevee.bloom_threshold = 0.16
            eevee.bloom_intensity = 0.78
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.6


def make_energy_material():
    mat = bpy.data.materials.new("energy")
    mat.diffuse_color = (1.0, 0.25, 0.0, 0.82)
    mat.use_nodes = True
    mat.blend_method = "BLEND"
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (1.0, 0.24, 0.0, 0.82)
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = 0.82
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.28, 0.02, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 1.9
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.22
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
        mins.append(Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners))))
        maxs.append(Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners))))
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


def make_camera(name, loc, target, lens=28, clip_end=800):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.1
    data.clip_end = clip_end
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = Vector(loc)
    point_camera(obj, target)
    return obj


def render_still(camera, filename):
    path = os.path.join(SCREENSHOTS, filename)
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def append_tube(vertices, faces, points, radius, sides=5):
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


def append_uv_sphere(vertices, faces, center, radii, segments=6, rings=3):
    start_index = len(vertices)
    vertices.append((center.x, center.y, center.z + radii.z))

    for ring in range(1, rings):
        phi = math.pi * ring / rings
        z = math.cos(phi) * radii.z
        rr = math.sin(phi)
        for segment in range(segments):
            theta = math.tau * segment / segments
            vertices.append(
                (
                    center.x + math.cos(theta) * radii.x * rr,
                    center.y + math.sin(theta) * radii.y * rr,
                    center.z + z,
                )
            )

    bottom_index = len(vertices)
    vertices.append((center.x, center.y, center.z - radii.z))

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


def append_ring(vertices, faces, center, inner_radius, outer_radius, sides=24):
    inner_start = len(vertices)
    for idx in range(sides):
        angle = math.tau * idx / sides
        vertices.append((center.x + math.cos(angle) * inner_radius, center.y + math.sin(angle) * inner_radius, center.z))
    outer_start = len(vertices)
    for idx in range(sides):
        angle = math.tau * idx / sides
        vertices.append((center.x + math.cos(angle) * outer_radius, center.y + math.sin(angle) * outer_radius, center.z))
    for idx in range(sides):
        faces.append(
            (
                inner_start + idx,
                inner_start + ((idx + 1) % sides),
                outer_start + ((idx + 1) % sides),
                outer_start + idx,
            )
        )


def append_disc(vertices, faces, center, radius, sides=20):
    center_index = len(vertices)
    vertices.append(center)
    ring_start = len(vertices)
    for idx in range(sides):
        angle = math.tau * idx / sides
        vertices.append((center[0] + math.cos(angle) * radius, center[1] + math.sin(angle) * radius, center[2]))
    for idx in range(sides):
        faces.append((center_index, ring_start + idx, ring_start + ((idx + 1) % sides)))


def append_vein_strip(vertices, faces, center, angle, length, width):
    start = Vector(center)
    direction = Vector((math.cos(angle), math.sin(angle), 0))
    perp = Vector((-direction.y, direction.x, 0)) * (width * 0.5)
    end = start + direction * length
    taper = width * 0.16
    end_perp = Vector((-direction.y, direction.x, 0)) * (taper * 0.5)
    start_index = len(vertices)
    vertices.extend(
        [
            tuple(start - perp),
            tuple(start + perp),
            tuple(end + end_perp),
            tuple(end - end_perp),
        ]
    )
    faces.append((start_index, start_index + 1, start_index + 2, start_index + 3))


def append_curtain_strip(vertices, faces, top_center, bottom_center, side, half_width, index, count):
    t0 = index / count
    t1 = (index + 1) / count
    o0 = -half_width + t0 * half_width * 2
    o1 = -half_width + t1 * half_width * 2
    start_index = len(vertices)
    vertices.extend(
        [
            tuple(top_center + side * o0),
            tuple(top_center + side * o1),
            tuple(bottom_center + side * (o1 * 0.72)),
            tuple(bottom_center + side * (o0 * 0.72)),
        ]
    )
    faces.append((start_index, start_index + 1, start_index + 2, start_index + 3))


def create_waterfall_mesh(prefix, knowledge_box, mat, collection):
    vertices = []
    faces = []

    center = Vector((knowledge_box["center"].x, knowledge_box["center"].y, 0))
    toward_sia = Vector((-center.x, -center.y, 0))
    if toward_sia.length == 0:
        toward_sia = Vector((-1, 0, 0))
    toward_sia.normalize()
    side = Vector((-toward_sia.y, toward_sia.x, 0))
    side.normalize()

    front_offset = max(knowledge_box["size"].x, knowledge_box["size"].y) * 0.50 + 0.38
    facade_center = center + toward_sia * front_offset
    top_z = knowledge_box["max"].z + 2.25
    lip_z = knowledge_box["max"].z + 0.52
    base_z = 0.22
    half_width = max(1.35, min(2.0, knowledge_box["size"].x * 0.34))

    top_center = Vector((facade_center.x, facade_center.y, top_z))
    lip_center = Vector((facade_center.x, facade_center.y, lip_z))
    bottom_center = Vector((facade_center.x, facade_center.y, base_z))
    reservoir_center = Vector((facade_center.x, facade_center.y, 0.078))

    append_ring(vertices, faces, top_center, 0.52, 0.78, sides=24)
    append_ring(vertices, faces, lip_center, half_width * 0.62, half_width * 0.78, sides=28)

    stream_offsets = (-1.18, -0.78, -0.38, 0.0, 0.38, 0.78, 1.18)
    for stream_idx, offset in enumerate(stream_offsets, start=1):
        points = []
        stream_start = top_center + side * (offset * half_width)
        stream_lip = lip_center + side * (offset * half_width * 0.92)
        stream_end = bottom_center + side * (offset * half_width * 0.60)
        for step in range(14):
            t = step / 13
            z = (1 - t) * stream_lip.z + t * stream_end.z
            sway = math.sin((t * math.tau * 2.2) + stream_idx * 0.83) * 0.055
            pulse = math.cos((t * math.tau * 1.3) + stream_idx) * 0.035
            xy = stream_lip.lerp(stream_end, t)
            xy += side * sway + toward_sia * pulse
            xy.z = z
            points.append(xy)
        append_tube(vertices, faces, [stream_start, stream_lip] + points[1:], 0.035, sides=5)

    for strip_idx in range(5):
        strip_top = lip_center + toward_sia * 0.02
        strip_bottom = bottom_center + toward_sia * 0.08
        append_curtain_strip(vertices, faces, strip_top, strip_bottom, side, half_width * 0.95, strip_idx, 5)

    for idx, t in enumerate((0.16, 0.28, 0.40, 0.52, 0.64, 0.76, 0.88), start=1):
        z = (1 - t) * lip_z + t * base_z
        offset = math.sin(idx * 1.71) * half_width * 0.62
        drift = math.cos(idx * 0.77) * 0.18
        center_point = Vector((facade_center.x, facade_center.y, z)) + side * offset + toward_sia * drift
        radius = 0.055 + (0.012 if idx % 3 == 0 else 0.0)
        append_uv_sphere(vertices, faces, center_point, Vector((radius, radius, radius * 1.35)), segments=6, rings=3)

    append_disc(vertices, faces, tuple(reservoir_center), 0.72, sides=24)
    append_ring(vertices, faces, reservoir_center + Vector((0, 0, 0.012)), 0.84, 1.08, sides=28)
    append_ring(vertices, faces, reservoir_center + Vector((0, 0, 0.035)), 1.16, 1.44, sides=28)
    for idx in range(8):
        angle = math.tau * idx / 8 + 0.12
        append_vein_strip(vertices, faces, tuple(reservoir_center), angle, 3.05, 0.10)

    mesh = bpy.data.meshes.new(f"{prefix}_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(prefix, mesh)
    obj.data.materials.append(mat)
    collection.objects.link(obj)

    return obj, {
        "delivery_style": "waterfall",
        "receptor": "SIA-facing Knowledgebase crown lip",
        "stream_count": len(stream_offsets),
        "curtain_strip_count": 5,
        "droplet_count": 7,
        "ground_vein_count": 8,
        "has_downward_curtain": True,
        "has_reservoir_pool": True,
        "front_facade_center": [round(facade_center.x, 4), round(facade_center.y, 4), 0.0],
        "top": [round(top_center.x, 4), round(top_center.y, 4), round(top_center.z, 4)],
        "lip": [round(lip_center.x, 4), round(lip_center.y, 4), round(lip_center.z, 4)],
        "base": [round(reservoir_center.x, 4), round(reservoir_center.y, 4), round(reservoir_center.z, 4)],
        "drop_height": round(lip_z - base_z, 4),
        "facade_half_width": round(half_width, 4),
    }


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
    }
    try:
        bpy.ops.export_scene.gltf(**export_kwargs, export_apply_modifiers=True)
    except TypeError:
        bpy.ops.export_scene.gltf(**export_kwargs)
    bpy.ops.object.select_all(action="DESELECT")


def import_qa(glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb_path)
    objects = list(bpy.data.objects)
    mesh_objects = [obj for obj in objects if obj.type == "MESH"]
    materials = collect_materials(mesh_objects)
    return {
        "object_count": len(objects),
        "mesh_count": len(mesh_objects),
        "tris": count_tris(mesh_objects),
        "materials": materials,
        "materials_valid": materials == ["energy"],
        "file_size_bytes": os.path.getsize(glb_path),
    }


print("=" * 72)
print("Session 52: Knowledgebase Waterfall")
print("=" * 72)

bpy.ops.wm.read_factory_settings(use_empty=True)
energy_mat = make_energy_material()

lighting = load_python_module(os.path.join(SHARED, "lighting-rig.py"), "lighting_rig")
lighting["clear_lighting"]()
lighting["setup_viewport_lighting"]()
setup_render()

context_collection = bpy.data.collections.new("Approved_Structure_Context")
bpy.context.scene.collection.children.link(context_collection)
hard_pipeline_context = bpy.data.collections.new("Hard_Pipeline_Context")
bpy.context.scene.collection.children.link(hard_pipeline_context)
warm_mist_context = bpy.data.collections.new("Warm_Mist_Context")
bpy.context.scene.collection.children.link(warm_mist_context)
faint_thread_context = bpy.data.collections.new("Faint_Thread_Context")
bpy.context.scene.collection.children.link(faint_thread_context)
waterfall_collection = bpy.data.collections.new("Knowledgebase_Waterfall_S52")
bpy.context.scene.collection.children.link(waterfall_collection)

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

hard_context_imported = import_glb(HARD_PIPELINES_GLB, hard_pipeline_context) if os.path.exists(HARD_PIPELINES_GLB) else []
warm_context_imported = import_glb(WARM_MIST_GLB, warm_mist_context) if os.path.exists(WARM_MIST_GLB) else []
thread_context_imported = import_glb(FAINT_THREAD_GLB, faint_thread_context) if os.path.exists(FAINT_THREAD_GLB) else []

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

knowledge_item = registry["Knowledgebase"]
knowledge_box = knowledge_item["bbox"]
if knowledge_box is None:
    raise RuntimeError("Knowledgebase approved exterior could not be loaded for waterfall placement.")

waterfall_obj, waterfall_metrics = create_waterfall_mesh(
    "knowledgebase_waterfall_sia_endpoint", knowledge_box, energy_mat, waterfall_collection
)
waterfall_obj["pipeline_batch"] = "knowledgebase-waterfall-session52"
waterfall_obj["target_district"] = "Knowledgebase"
waterfall_obj["delivery_style"] = "waterfall"
waterfall_obj["runtime_hint"] = "downward liquid-light cascade fed by existing SIA hard pipeline endpoint"

waterfall_objects = [waterfall_obj]
root = bpy.data.objects.new("knowledgebase_waterfall_root", None)
waterfall_collection.objects.link(root)
root.empty_display_type = "PLAIN_AXES"
root.empty_display_size = 0.4
waterfall_obj.parent = root

screenshots = {
    "citywide": render_still(
        make_camera("S52_Knowledgebase_Waterfall_Citywide", (96, -140, 96), (8, -12, 18), lens=15),
        "s52-knowledgebase-waterfall-citywide.png",
    ),
    "route": render_still(
        make_camera("S52_SIA_To_Knowledgebase_Waterfall", (69, -67, 46), (22, -17, 18), lens=27),
        "s52-sia-knowledgebase-waterfall-route.png",
    ),
    "knowledgebase_receptor": render_still(
        make_camera("S52_Knowledgebase_Waterfall_Receptor", (49, -39, 23), (30, -22, 7.8), lens=38),
        "s52-knowledgebase-waterfall-receptor.png",
    ),
}

bpy.ops.wm.save_as_mainfile(filepath=SESSION_BLEND)

selected_for_export = [root] + waterfall_objects
export_selected_glb(DRAFT_GLB, selected_for_export)

waterfall_materials = collect_materials(waterfall_objects)
total_tris = count_tris(waterfall_objects)
file_size_bytes = os.path.getsize(DRAFT_GLB)
waterfall_metrics["tris"] = total_tris

checks = {
    "approved_structure_assets_present": not missing_assets,
    "prior_hard_pipeline_asset_present": os.path.exists(HARD_PIPELINES_GLB) and len(hard_context_imported) > 0,
    "prior_warm_mist_asset_present": os.path.exists(WARM_MIST_GLB) and len(warm_context_imported) > 0,
    "prior_faint_thread_asset_present": os.path.exists(FAINT_THREAD_GLB) and len(thread_context_imported) > 0,
    "waterfall_count": len(waterfall_objects) == 1,
    "starts_above_knowledgebase_crown": waterfall_metrics["top"][2] >= round(knowledge_box["max"].z + 2.0, 4),
    "cascades_down_facade": waterfall_metrics["drop_height"] >= 12.0 and waterfall_metrics["stream_count"] >= 7,
    "delivery_style_matches_spec": (
        waterfall_metrics["delivery_style"] == "waterfall"
        and waterfall_metrics["has_downward_curtain"]
        and waterfall_metrics["has_reservoir_pool"]
    ),
    "ground_veins": waterfall_metrics["ground_vein_count"] == 8,
    "material_named_energy": waterfall_materials == ["energy"],
    "technical_budget": 500 <= total_tris <= 1500,
    "file_budget": file_size_bytes <= 40 * 1024,
}

import_check = import_qa(DRAFT_GLB)
checks["approved_glb_reimports"] = import_check["mesh_count"] > 0
checks["approved_glb_materials_valid"] = import_check["materials_valid"]

overall = "APPROVED" if all(checks.values()) else "NEEDS REVIEW"
if overall == "APPROVED":
    shutil.copyfile(DRAFT_GLB, APPROVED_GLB)

report = {
    "session": 52,
    "asset": "energy-system/knowledgebase-waterfall",
    "scope": {
        "waterfall_count": 1,
        "targets": ["Knowledgebase"],
        "note": (
            "Builds the Knowledgebase special delivery as a downward liquid-light "
            "cascade on the SIA-facing facade. The existing hard pipeline remains "
            "the long-distance feed; this asset adds the crown lip, vertical streams, "
            "facade curtain, reservoir pool, and endpoint ground veins."
        ),
    },
    "source_layout_report": LATEST_LAYOUT_REPORT,
    "knowledgebase_bbox": bbox_dict(knowledge_box),
    "missing_assets": missing_assets,
    "waterfall_metrics": {"Knowledgebase": waterfall_metrics},
    "waterfall_materials": waterfall_materials,
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
print("SESSION 52 KNOWLEDGEBASE WATERFALL COMPLETE")
print(f"Blend: {SESSION_BLEND}")
print(f"Draft GLB: {DRAFT_GLB}")
print(f"Approved GLB: {APPROVED_GLB}")
print(f"Report: {SESSION_REPORT}")
print(f"Total tris: {total_tris}")
print(f"File size: {file_size_bytes / 1024:.1f} KB")
print(f"Overall verdict: {overall}")
for check, value in checks.items():
    print(f"  {check}: {'PASS' if value else 'FAIL'}")

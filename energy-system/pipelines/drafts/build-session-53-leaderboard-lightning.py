"""
Session 53: Phase 5 Leaderboard lightning special delivery.

Builds the dramatic endpoint flash where the existing SIA hard pipeline strikes
the Leaderboard arena apex, renders QA evidence, exports a draft GLB, and
promotes it when checks pass.
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
SESSION_REPORT = os.path.join(DRAFTS, "leaderboard-lightning-session53-report.json")
SESSION_BLEND = os.path.join(DRAFTS, "leaderboard-lightning-session53.blend")
DRAFT_GLB = os.path.join(DRAFTS, "leaderboard-lightning-session53.glb")
APPROVED_GLB = os.path.join(APPROVED, "leaderboard-lightning.glb")
HARD_PIPELINES_GLB = os.path.join(APPROVED, "hard-pipelines.glb")
WARM_MIST_GLB = os.path.join(APPROVED, "warm-mist.glb")
FAINT_THREAD_GLB = os.path.join(APPROVED, "faint-thread.glb")
WATERFALL_GLB = os.path.join(APPROVED, "knowledgebase-waterfall.glb")
HARD_PIPELINES_REPORT = os.path.join(DRAFTS, "hard-pipelines-session49-report.json")
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
            eevee.bloom_threshold = 0.12
            eevee.bloom_intensity = 0.9
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.6


def make_energy_material():
    mat = bpy.data.materials.new("energy")
    mat.diffuse_color = (1.0, 0.26, 0.0, 0.92)
    mat.use_nodes = True
    mat.blend_method = "BLEND"
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (1.0, 0.24, 0.0, 0.92)
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = 0.92
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.28, 0.02, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 2.25
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


def append_ring(vertices, faces, center, inner_radius, outer_radius, sides=32):
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


def append_disc(vertices, faces, center, radius, sides=24):
    center_index = len(vertices)
    vertices.append(tuple(center))
    ring_start = len(vertices)
    for idx in range(sides):
        angle = math.tau * idx / sides
        vertices.append((center.x + math.cos(angle) * radius, center.y + math.sin(angle) * radius, center.z))
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


def append_flash_shard(vertices, faces, center, angle, length, height, width):
    base = Vector(center)
    direction = Vector((math.cos(angle), math.sin(angle), 0))
    side = Vector((-direction.y, direction.x, 0))
    start_index = len(vertices)
    vertices.extend(
        [
            tuple(base - side * width),
            tuple(base + side * width),
            tuple(base + direction * length + Vector((0, 0, height))),
        ]
    )
    faces.append((start_index, start_index + 1, start_index + 2))


def point_on_polyline(points, t):
    if t <= 0:
        return points[0].copy()
    if t >= 1:
        return points[-1].copy()
    scaled = t * (len(points) - 1)
    idx = min(int(math.floor(scaled)), len(points) - 2)
    local_t = scaled - idx
    return points[idx].lerp(points[idx + 1], local_t)


def create_lightning_mesh(prefix, leaderboard_box, hard_metrics, mat, collection):
    vertices = []
    faces = []

    center = Vector((leaderboard_box["center"].x, leaderboard_box["center"].y, 0))
    hard_end = Vector(hard_metrics["end"])
    hard_start = Vector(hard_metrics["start"])
    apex_z = min(leaderboard_box["max"].z - 2.24, hard_end.z - 1.5)
    impact = Vector((center.x, center.y, apex_z))
    intake = hard_end

    main_offsets = [
        (0.0, 0.0, 1.0),
        (0.34, -0.16, 0.84),
        (-0.28, 0.26, 0.66),
        (0.48, 0.10, 0.48),
        (-0.42, -0.18, 0.29),
        (0.18, 0.20, 0.12),
        (0.0, 0.0, 0.0),
    ]
    main_points = []
    for ox, oy, t in main_offsets:
        z = impact.z + (intake.z - impact.z) * t
        radial_taper = 0.35 + t * 0.65
        main_points.append(Vector((center.x + ox * radial_taper, center.y + oy * radial_taper, z)))

    append_tube(vertices, faces, main_points, 0.072, sides=7)

    branch_records = []
    branch_angles = [
        0.10,
        0.62,
        1.10,
        1.75,
        2.22,
        2.78,
        3.32,
        3.90,
        4.45,
        5.02,
        5.52,
        6.02,
    ]
    for idx, angle in enumerate(branch_angles, start=1):
        t = 0.17 + (idx % 6) * 0.12
        base = point_on_polyline(main_points, min(t, 0.88))
        length = 0.72 + 0.20 * (idx % 3)
        drop = 0.30 + 0.08 * (idx % 4)
        direction = Vector((math.cos(angle), math.sin(angle), 0))
        mid = base + direction * (length * 0.48) + Vector((0, 0, -drop * 0.35))
        end = base + direction * length + Vector((0, 0, -drop))
        append_tube(vertices, faces, [base, mid, end], 0.028, sides=5)
        branch_records.append([round(end.x, 4), round(end.y, 4), round(end.z, 4)])

    pillar_jump_records = []
    for idx, angle in enumerate((0.0, math.pi * 0.5, math.pi, math.pi * 1.5), start=1):
        direction = Vector((math.cos(angle), math.sin(angle), 0))
        start = impact + direction * 0.55 + Vector((0, 0, 0.1))
        kink = impact + direction * 2.7 + Vector((0, 0, 0.52 + 0.12 * (idx % 2)))
        end = impact + direction * 5.1 + Vector((0, 0, 0.28))
        append_tube(vertices, faces, [start, kink, end], 0.035, sides=5)
        pillar_jump_records.append([round(end.x, 4), round(end.y, 4), round(end.z, 4)])

    append_ring(vertices, faces, intake, 0.42, 0.74, sides=30)
    append_ring(vertices, faces, impact + Vector((0, 0, -0.03)), 0.78, 1.18, sides=36)
    append_ring(vertices, faces, impact + Vector((0, 0, -0.08)), 1.52, 2.18, sides=40)
    append_disc(vertices, faces, impact + Vector((0, 0, -0.16)), 0.34, sides=24)

    for idx in range(16):
        angle = math.tau * idx / 16 + 0.05
        append_flash_shard(
            vertices,
            faces,
            impact + Vector((0, 0, -0.02)),
            angle,
            1.15 + 0.22 * (idx % 4),
            0.13 + 0.04 * (idx % 3),
            0.045,
        )

    ground_center = Vector((center.x, center.y, 0.078))
    append_disc(vertices, faces, ground_center, 0.30, sides=20)
    for idx in range(8):
        angle = math.tau * idx / 8 + 0.08
        append_vein_strip(vertices, faces, ground_center, angle, 3.1, 0.12)

    mesh = bpy.data.meshes.new(f"{prefix}_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(prefix, mesh)
    obj.data.materials.append(mat)
    collection.objects.link(obj)

    lateral_offsets = [
        math.hypot(point.x - center.x, point.y - center.y)
        for point in main_points
    ]
    return obj, {
        "delivery_style": "lightning",
        "receptor": "Leaderboard open-apex strike socket",
        "prior_hard_pipeline_start": [round(hard_start.x, 4), round(hard_start.y, 4), round(hard_start.z, 4)],
        "hard_pipeline_endpoint": [round(hard_end.x, 4), round(hard_end.y, 4), round(hard_end.z, 4)],
        "intake": [round(intake.x, 4), round(intake.y, 4), round(intake.z, 4)],
        "impact": [round(impact.x, 4), round(impact.y, 4), round(impact.z, 4)],
        "main_bolt_segment_count": len(main_points) - 1,
        "branch_count": len(branch_records),
        "pillar_jump_count": len(pillar_jump_records),
        "impact_ring_count": 2,
        "ground_vein_count": 8,
        "max_lateral_jag": round(max(lateral_offsets), 4),
        "drop_height": round(intake.z - impact.z, 4),
        "branch_endpoints": branch_records,
        "pillar_jump_endpoints": pillar_jump_records,
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
print("Session 53: Leaderboard Lightning")
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
waterfall_context = bpy.data.collections.new("Knowledgebase_Waterfall_Context")
bpy.context.scene.collection.children.link(waterfall_context)
lightning_collection = bpy.data.collections.new("Leaderboard_Lightning_S53")
bpy.context.scene.collection.children.link(lightning_collection)

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
waterfall_context_imported = import_glb(WATERFALL_GLB, waterfall_context) if os.path.exists(WATERFALL_GLB) else []

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

with open(HARD_PIPELINES_REPORT, "r", encoding="utf-8") as handle:
    hard_report = json.load(handle)

leaderboard_item = registry["Leaderboard"]
leaderboard_box = leaderboard_item["bbox"]
if leaderboard_box is None:
    raise RuntimeError("Leaderboard approved exterior could not be loaded for lightning placement.")

hard_metrics = hard_report["pipeline_metrics"]["Leaderboard"]

lightning_obj, lightning_metrics = create_lightning_mesh(
    "leaderboard_lightning_apex_strike", leaderboard_box, hard_metrics, energy_mat, lightning_collection
)
lightning_obj["pipeline_batch"] = "leaderboard-lightning-session53"
lightning_obj["target_district"] = "Leaderboard & Competition"
lightning_obj["delivery_style"] = "lightning"
lightning_obj["runtime_hint"] = "jagged apex strike, impact rings, branch forks, and endpoint veins fed by existing hard pipeline"

lightning_objects = [lightning_obj]
root = bpy.data.objects.new("leaderboard_lightning_root", None)
lightning_collection.objects.link(root)
root.empty_display_type = "PLAIN_AXES"
root.empty_display_size = 0.4
lightning_obj.parent = root

screenshots = {
    "citywide": render_still(
        make_camera("S53_Leaderboard_Lightning_Citywide", (92, -144, 94), (0, -12, 18), lens=15),
        "s53-leaderboard-lightning-citywide.png",
    ),
    "route": render_still(
        make_camera("S53_SIA_To_Leaderboard_Lightning", (44, -76, 43), (-4, -30, 20), lens=29),
        "s53-sia-leaderboard-lightning-route.png",
    ),
    "leaderboard_receptor": render_still(
        make_camera("S53_Leaderboard_Lightning_Receptor", (13, -70, 22), (-8, -45, 8.7), lens=38),
        "s53-leaderboard-lightning-receptor.png",
    ),
}

bpy.ops.wm.save_as_mainfile(filepath=SESSION_BLEND)

selected_for_export = [root] + lightning_objects
export_selected_glb(DRAFT_GLB, selected_for_export)

lightning_materials = collect_materials(lightning_objects)
total_tris = count_tris(lightning_objects)
file_size_bytes = os.path.getsize(DRAFT_GLB)
lightning_metrics["tris"] = total_tris

checks = {
    "approved_structure_assets_present": not missing_assets,
    "prior_hard_pipeline_asset_present": os.path.exists(HARD_PIPELINES_GLB) and len(hard_context_imported) > 0,
    "prior_warm_mist_asset_present": os.path.exists(WARM_MIST_GLB) and len(warm_context_imported) > 0,
    "prior_faint_thread_asset_present": os.path.exists(FAINT_THREAD_GLB) and len(thread_context_imported) > 0,
    "prior_waterfall_asset_present": os.path.exists(WATERFALL_GLB) and len(waterfall_context_imported) > 0,
    "prior_hard_route_arced": hard_metrics["arc_lift_over_linear_mid"] >= 12.0,
    "lightning_count": len(lightning_objects) == 1,
    "hard_endpoint_meets_lightning_intake": lightning_metrics["intake"] == lightning_metrics["hard_pipeline_endpoint"],
    "strikes_leaderboard_apex": (
        abs(lightning_metrics["impact"][0] - round(leaderboard_box["center"].x, 4)) <= 0.01
        and abs(lightning_metrics["impact"][1] - round(leaderboard_box["center"].y, 4)) <= 0.01
        and lightning_metrics["impact"][2] >= 7.8
    ),
    "jagged_bolt_not_straight": lightning_metrics["max_lateral_jag"] >= 0.30 and lightning_metrics["branch_count"] >= 10,
    "delivery_style_matches_spec": (
        lightning_metrics["delivery_style"] == "lightning"
        and lightning_metrics["branch_count"] >= 12
        and lightning_metrics["impact_ring_count"] >= 2
    ),
    "ground_veins": lightning_metrics["ground_vein_count"] == 8,
    "material_named_energy": lightning_materials == ["energy"],
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
    "session": 53,
    "asset": "energy-system/leaderboard-lightning",
    "scope": {
        "lightning_count": 1,
        "targets": ["Leaderboard"],
        "note": (
            "Builds the Leaderboard special delivery as a jagged lightning strike "
            "at the open arena apex. The existing hard pipeline remains the "
            "long-distance SIA feed; this asset adds the intake halo, main bolt, "
            "branch forks, rim flash, pillar jumpers, and endpoint ground veins."
        ),
    },
    "source_layout_report": LATEST_LAYOUT_REPORT,
    "leaderboard_bbox": bbox_dict(leaderboard_box),
    "missing_assets": missing_assets,
    "hard_pipeline_metrics": hard_metrics,
    "lightning_metrics": {"Leaderboard": lightning_metrics},
    "lightning_materials": lightning_materials,
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
print("SESSION 53 LEADERBOARD LIGHTNING COMPLETE")
print(f"Blend: {SESSION_BLEND}")
print(f"Draft GLB: {DRAFT_GLB}")
print(f"Approved GLB: {APPROVED_GLB}")
print(f"Report: {SESSION_REPORT}")
print(f"Total tris: {total_tris}")
print(f"File size: {file_size_bytes / 1024:.1f} KB")
print(f"Overall verdict: {overall}")
for check, value in checks.items():
    print(f"  {check}: {'PASS' if value else 'FAIL'}")

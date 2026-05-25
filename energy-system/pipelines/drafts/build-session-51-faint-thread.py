"""
Session 51: Phase 5 faint-thread delivery.

Builds the barely visible SIA-to-Recovery whisper line, renders QA evidence,
exports a draft GLB, and promotes it when checks pass.
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
SESSION_REPORT = os.path.join(DRAFTS, "faint-thread-session51-report.json")
SESSION_BLEND = os.path.join(DRAFTS, "faint-thread-session51.blend")
DRAFT_GLB = os.path.join(DRAFTS, "faint-thread-session51.glb")
APPROVED_GLB = os.path.join(APPROVED, "faint-thread.glb")
HARD_PIPELINES_GLB = os.path.join(APPROVED, "hard-pipelines.glb")
WARM_MIST_GLB = os.path.join(APPROVED, "warm-mist.glb")
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
        "receptor": "barely visible top wisp receiver above the cloud shell",
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

THREAD_RADIUS = 0.018
THREAD_ALPHA = 0.22


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
            eevee.bloom_threshold = 0.18
            eevee.bloom_intensity = 0.38
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.6


def make_energy_material():
    mat = bpy.data.materials.new("energy")
    mat.diffuse_color = (1.0, 0.30, 0.0, THREAD_ALPHA)
    mat.use_nodes = True
    mat.blend_method = "BLEND"
    if hasattr(mat, "use_screen_refraction"):
        mat.use_screen_refraction = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (1.0, 0.28, 0.0, THREAD_ALPHA)
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = THREAD_ALPHA
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.35, 0.05, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 0.42
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


def quadratic_point(start, peak, end, t):
    return ((1 - t) ** 2) * start + 2 * (1 - t) * t * peak + (t**2) * end


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


def append_disc(vertices, faces, center, radius, sides=18):
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
    taper = width * 0.18
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


def create_faint_thread_mesh(prefix, start, end, arc_peak_z, mat, collection):
    vertices = []
    faces = []
    arc_peak = (start + end) * 0.5
    arc_peak.z = arc_peak_z

    points = [quadratic_point(start, arc_peak, end, idx / 64) for idx in range(65)]
    append_tube(vertices, faces, points, THREAD_RADIUS, sides=6)

    travel = Vector((end.x - start.x, end.y - start.y, 0))
    if travel.length == 0:
        travel = Vector((1, 0, 0))
    travel.normalize()
    side = Vector((-travel.y, travel.x, 0))

    shimmer_count = 0
    for idx, t in enumerate((0.18, 0.30, 0.42, 0.54, 0.66, 0.78, 0.90), start=1):
        base = quadratic_point(start, arc_peak, end, t)
        offset = side * (math.sin(idx * 1.41) * 0.095) + Vector((0, 0, math.cos(idx * 0.73) * 0.055))
        radius = 0.042 + (0.008 if idx % 3 == 0 else 0.0)
        append_uv_sphere(vertices, faces, base + offset, Vector((radius, radius, radius * 0.72)), segments=6, rings=3)
        shimmer_count += 1

    append_uv_sphere(vertices, faces, start, Vector((0.075, 0.075, 0.055)), segments=6, rings=3)

    receptor_center = Vector((end.x, end.y, end.z - 0.08))
    append_uv_sphere(vertices, faces, receptor_center, Vector((0.11, 0.11, 0.07)), segments=6, rings=3)
    append_ring(vertices, faces, receptor_center - Vector((0, 0, 0.11)), 0.34, 0.43, sides=24)
    append_ring(vertices, faces, receptor_center - Vector((0, 0, 0.02)), 0.49, 0.58, sides=24)

    for idx in range(5):
        angle = math.tau * idx / 5 + 0.25
        base = receptor_center + Vector((math.cos(angle) * 0.18, math.sin(angle) * 0.18, -0.02))
        append_vein_strip(vertices, faces, base, angle, 0.72, 0.042)

    ground_center = (end.x, end.y, 0.075)
    append_disc(vertices, faces, ground_center, 0.22, sides=18)
    for idx in range(8):
        append_vein_strip(vertices, faces, ground_center, math.tau * idx / 8, 3.0, 0.085)

    mesh = bpy.data.meshes.new(f"{prefix}_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(prefix, mesh)
    obj.data.materials.append(mat)
    collection.objects.link(obj)
    return obj, {
        "thread_radius": THREAD_RADIUS,
        "material_alpha": THREAD_ALPHA,
        "shimmer_point_count": shimmer_count,
        "ground_vein_count": 8,
        "has_hard_tube": False,
        "is_continuous_core": True,
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
print("Session 51: Faint Thread")
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
thread_collection = bpy.data.collections.new("Faint_Thread_S51")
bpy.context.scene.collection.children.link(thread_collection)

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

thread_objects = []
thread_metrics = {}

sia_box = registry["SIA_Tower"]["bbox"]
recovery_item = registry["Recovery"]
recovery_box = recovery_item["bbox"]

sia_crown_z = max(sia_box["max"].z - 5.2, 36.8)
sia_ring_radius = 4.5
target_center = Vector((recovery_box["center"].x, recovery_box["center"].y, 0))
direction = Vector((target_center.x, target_center.y, 0))
if direction.length == 0:
    direction = Vector((1, 0, 0))
direction.normalize()

start = Vector((direction.x * sia_ring_radius, direction.y * sia_ring_radius, sia_crown_z))
end = Vector((recovery_box["center"].x, recovery_box["center"].y, recovery_box["max"].z + 0.42))
distance = (Vector((end.x, end.y, 0)) - Vector((start.x, start.y, 0))).length
arc_peak_z = max(start.z + 3.8, end.z + 17.0, min(43.0, 35.0 + distance * 0.18))

thread_obj, style_metrics = create_faint_thread_mesh(
    "faint_thread_sia_to_recovery", start, end, arc_peak_z, energy_mat, thread_collection
)
thread_obj["pipeline_batch"] = "faint-thread-session51"
thread_obj["target_district"] = "Recovery & Sleep"
thread_obj["delivery_style"] = "faint-thread"
thread_obj["runtime_hint"] = "barely visible whisper line, thinner and dimmer than hard pipelines"
thread_objects.append(thread_obj)

linear_mid_z = (start.z + end.z) * 0.5
thread_metrics["Recovery"] = {
    "label": "Recovery & Sleep",
    "receptor": recovery_item["config"]["receptor"],
    "start": [round(start.x, 4), round(start.y, 4), round(start.z, 4)],
    "end": [round(end.x, 4), round(end.y, 4), round(end.z, 4)],
    "ground_vein_center": [round(end.x, 4), round(end.y, 4), 0.075],
    "distance_xy": round(distance, 4),
    "arc_peak_z": round(arc_peak_z, 4),
    "linear_mid_z": round(linear_mid_z, 4),
    "arc_lift_over_linear_mid": round(arc_peak_z - linear_mid_z, 4),
    "tris": count_tris(thread_objects),
    "delivery_style": "faint_thread",
    **style_metrics,
}

root = bpy.data.objects.new("faint_thread_root", None)
thread_collection.objects.link(root)
root.empty_display_type = "PLAIN_AXES"
root.empty_display_size = 0.4
for obj in thread_objects:
    obj.parent = root

screenshots = {
    "citywide": render_still(
        make_camera("S51_Faint_Thread_Citywide", (98, -140, 96), (-8, -8, 18), lens=15),
        "s51-faint-thread-citywide.png",
    ),
    "route": render_still(
        make_camera("S51_Faint_Thread_Route", (-88, -36, 42), (-24, -5, 20), lens=28),
        "s51-faint-thread-route.png",
    ),
    "recovery_receptor": render_still(
        make_camera("S51_Faint_Thread_Recovery", (-67, -28, 25), (-43, -8, 8.2), lens=36),
        "s51-faint-thread-recovery.png",
    ),
}

bpy.ops.wm.save_as_mainfile(filepath=SESSION_BLEND)

selected_for_export = [root] + thread_objects
export_selected_glb(DRAFT_GLB, selected_for_export)

thread_materials = collect_materials(thread_objects)
total_tris = count_tris(thread_objects)
file_size_bytes = os.path.getsize(DRAFT_GLB)
thread_metrics["Recovery"]["tris"] = total_tris

checks = {
    "approved_structure_assets_present": not missing_assets,
    "prior_hard_pipeline_asset_present": os.path.exists(HARD_PIPELINES_GLB) and len(hard_context_imported) > 0,
    "prior_warm_mist_asset_present": os.path.exists(WARM_MIST_GLB) and len(warm_context_imported) > 0,
    "faint_thread_count": len(thread_objects) == 1,
    "connects_from_sia_crown": thread_metrics["Recovery"]["start"][2] >= 35.0,
    "reaches_recovery_receiver": thread_metrics["Recovery"]["end"][2] >= round(recovery_box["max"].z + 0.35, 4),
    "arced_thread_path": thread_metrics["Recovery"]["arc_lift_over_linear_mid"] >= 12.0,
    "delivery_style_matches_spec": (
        thread_metrics["Recovery"]["delivery_style"] == "faint_thread"
        and thread_metrics["Recovery"]["thread_radius"] <= 0.02
        and thread_metrics["Recovery"]["material_alpha"] <= 0.28
        and not thread_metrics["Recovery"]["has_hard_tube"]
    ),
    "ground_veins": thread_metrics["Recovery"]["ground_vein_count"] == 8,
    "material_named_energy": thread_materials == ["energy"],
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
    "session": 51,
    "asset": "energy-system/faint-thread",
    "scope": {
        "faint_thread_count": 1,
        "targets": ["Recovery"],
        "note": (
            "Builds the Recovery & Sleep delivery as the lightest SIA feed: an "
            "ultra-thin translucent energy thread with sparse shimmer points, a "
            "quiet top-wisp receptor, and endpoint ground veins."
        ),
    },
    "source_layout_report": LATEST_LAYOUT_REPORT,
    "missing_assets": missing_assets,
    "thread_metrics": thread_metrics,
    "thread_materials": thread_materials,
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
print("SESSION 51 FAINT THREAD COMPLETE")
print(f"Blend: {SESSION_BLEND}")
print(f"Draft GLB: {DRAFT_GLB}")
print(f"Approved GLB: {APPROVED_GLB}")
print(f"Report: {SESSION_REPORT}")
print(f"Total tris: {total_tris}")
print(f"File size: {file_size_bytes / 1024:.1f} KB")
print(f"Overall verdict: {overall}")
for check, value in checks.items():
    print(f"  {check}: {'PASS' if value else 'FAIL'}")

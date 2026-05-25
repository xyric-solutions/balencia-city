"""
Session 49: Phase 5 hard-pipeline batch.

Builds arced SIA-to-district hard pipelines, district endpoint vein clusters,
renders QA evidence, exports a draft GLB, and promotes it when checks pass.
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
SESSION_REPORT = os.path.join(DRAFTS, "hard-pipelines-session49-report.json")
SESSION_BLEND = os.path.join(DRAFTS, "hard-pipelines-session49.blend")
DRAFT_GLB = os.path.join(DRAFTS, "hard-pipelines-session49.glb")
APPROVED_GLB = os.path.join(APPROVED, "hard-pipelines.glb")
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
        "special_later": "cascading energy waterfall",
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
        "special_later": "lightning bolt entry",
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


HARD_PIPELINE_NAMES = [
    "Fitness",
    "Finance",
    "Knowledgebase",
    "Chat",
    "Leaderboard",
    "Career",
    "Analytics",
    "Nutrition",
]

VALID_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}


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
            eevee.bloom_threshold = 0.25
            eevee.bloom_intensity = 0.65
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.6


def make_energy_material():
    mat = bpy.data.materials.new("energy")
    mat.diffuse_color = (1.0, 0.25, 0.0, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (1.0, 0.23, 0.0, 1.0)
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.23, 0.0, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 1.8
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.35
    return mat


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


def link_to_collection(obj, collection):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def quadratic_point(start, peak, end, t):
    return ((1 - t) ** 2) * start + 2 * (1 - t) * t * peak + (t**2) * end


def create_pipeline_curve(name, start, end, arc_peak_z, mat, collection):
    curve = bpy.data.curves.new(name=f"{name}_curve_data", type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 64
    curve.bevel_depth = 0.08
    curve.bevel_resolution = 2
    curve.use_fill_caps = True

    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(1)

    p0 = spline.bezier_points[0]
    p1 = spline.bezier_points[1]
    p0.co = start
    p1.co = end

    mid = (start + end) * 0.5
    mid.z = arc_peak_z
    p0.handle_left_type = "AUTO"
    p1.handle_right_type = "AUTO"
    p0.handle_right_type = "FREE"
    p1.handle_left_type = "FREE"
    p0.handle_right = start.lerp(mid, 0.68)
    p1.handle_left = end.lerp(mid, 0.68)

    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    obj.data.materials.append(mat)

    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target="MESH")
    mesh_obj = bpy.context.view_layer.objects.active
    mesh_obj.name = name
    mesh_obj.data.name = f"{name}_mesh"
    mesh_obj.data.materials.clear()
    mesh_obj.data.materials.append(mat)
    link_to_collection(mesh_obj, collection)
    bpy.ops.object.select_all(action="DESELECT")
    return mesh_obj, mid


def create_uv_sphere(name, location, radius, mat, collection, segments=8, rings=4):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        radius=radius,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"{name}_mesh"
    obj.data.materials.append(mat)
    link_to_collection(obj, collection)
    bpy.ops.object.select_all(action="DESELECT")
    return obj


def create_flat_disc(name, location, radius, mat, collection, vertices=24):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=0.035,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"{name}_mesh"
    obj.data.materials.append(mat)
    link_to_collection(obj, collection)
    bpy.ops.object.select_all(action="DESELECT")
    return obj


def create_vein_strip(name, center, angle, length, width, mat, collection):
    start = Vector(center)
    direction = Vector((math.cos(angle), math.sin(angle), 0))
    perp = Vector((-direction.y, direction.x, 0)) * (width * 0.5)
    end = start + direction * length
    taper = width * 0.18
    end_perp = Vector((-direction.y, direction.x, 0)) * (taper * 0.5)

    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(
        [start - perp, start + perp, end + end_perp, end - end_perp],
        [],
        [(0, 1, 2, 3)],
    )
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    collection.objects.link(obj)
    return obj


def create_ground_veins(prefix, center_xy, mat, collection, radius=3.0):
    objects = []
    hub = create_flat_disc(
        f"{prefix}_ground_hub", (center_xy[0], center_xy[1], 0.07), 0.28, mat, collection, vertices=18
    )
    objects.append(hub)
    for idx in range(8):
        angle = (math.tau * idx) / 8
        objects.append(
            create_vein_strip(
                f"{prefix}_ground_vein_{idx + 1:02d}",
                (center_xy[0], center_xy[1], 0.075),
                angle,
                radius,
                0.12,
                mat,
                collection,
            )
        )
    return objects


def create_rooftop_star(prefix, center, mat, collection):
    objects = [create_uv_sphere(f"{prefix}_receiver_node", center, 0.22, mat, collection)]
    for idx in range(4):
        angle = (math.tau * idx) / 4
        objects.append(
            create_vein_strip(
                f"{prefix}_receiver_trace_{idx + 1:02d}",
                center,
                angle,
                0.9,
                0.08,
                mat,
                collection,
            )
        )
    return objects


def collect_materials(objects):
    names = set()
    for obj in objects:
        if obj.type != "MESH":
            continue
        for slot in obj.material_slots:
            if slot.material:
                names.add(slot.material.name)
    return sorted(names)


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
print("Session 49: Hard Pipelines")
print("=" * 72)

bpy.ops.wm.read_factory_settings(use_empty=True)
energy_mat = make_energy_material()

lighting = load_python_module(os.path.join(SHARED, "lighting-rig.py"), "lighting_rig")
lighting["clear_lighting"]()
lighting["setup_viewport_lighting"]()
setup_render()

context_collection = bpy.data.collections.new("Approved_Structure_Context")
bpy.context.scene.collection.children.link(context_collection)
pipeline_collection = bpy.data.collections.new("Hard_Pipelines_S49")
bpy.context.scene.collection.children.link(pipeline_collection)

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

pipeline_objects = []
pipeline_metrics = {}

sia_box = registry["SIA_Tower"]["bbox"]
sia_crown_z = max(sia_box["max"].z - 5.2, 36.8)
sia_ring_radius = 4.5
sia_base_veins = create_ground_veins("sia_hub", (0, 0), energy_mat, pipeline_collection, radius=4.1)
pipeline_objects.extend(sia_base_veins)

for name in HARD_PIPELINE_NAMES:
    cfg = registry[name]["config"]
    box = registry[name]["bbox"]
    if box is None:
        continue

    center = Vector((box["center"].x, box["center"].y, 0))
    direction = Vector((box["center"].x, box["center"].y, 0))
    if direction.length == 0:
        direction = Vector((1, 0, 0))
    direction.normalize()

    start = Vector((direction.x * sia_ring_radius, direction.y * sia_ring_radius, sia_crown_z))
    end_z = box["max"].z + 0.55
    end = Vector((box["center"].x, box["center"].y, end_z))
    distance = (Vector((end.x, end.y, 0)) - Vector((start.x, start.y, 0))).length
    arc_peak_z = max(start.z + 7.5, end.z + 11.0, min(50.0, 35.0 + distance * 0.2))
    arc_peak = (start + end) * 0.5
    arc_peak.z = arc_peak_z
    slug = name.lower().replace("_", "-")

    pipe, bezier_mid = create_pipeline_curve(
        f"hard_pipeline_sia_to_{slug}", start, end, arc_peak_z, energy_mat, pipeline_collection
    )
    objects = [pipe]
    objects.append(create_uv_sphere(f"{slug}_sia_departure_node", start, 0.18, energy_mat, pipeline_collection))
    objects.extend(create_rooftop_star(slug, end, energy_mat, pipeline_collection))
    objects.extend(create_ground_veins(slug, (center.x, center.y), energy_mat, pipeline_collection))

    for idx, t in enumerate((0.20, 0.36, 0.52, 0.68, 0.84), start=1):
        particle_loc = quadratic_point(start, arc_peak, end, t)
        objects.append(
            create_uv_sphere(
                f"{slug}_flow_marker_{idx:02d}",
                particle_loc,
                0.105,
                energy_mat,
                pipeline_collection,
                segments=8,
                rings=4,
            )
        )

    for obj in objects:
        obj["pipeline_batch"] = "hard-pipelines-session49"
        obj["target_district"] = cfg["label"]
    pipeline_objects.extend(objects)

    linear_mid_z = (start.z + end.z) * 0.5
    pipeline_metrics[name] = {
        "label": cfg["label"],
        "start": [round(start.x, 4), round(start.y, 4), round(start.z, 4)],
        "end": [round(end.x, 4), round(end.y, 4), round(end.z, 4)],
        "ground_vein_center": [round(center.x, 4), round(center.y, 4), 0.075],
        "distance_xy": round(distance, 4),
        "arc_peak_z": round(arc_peak_z, 4),
        "linear_mid_z": round(linear_mid_z, 4),
        "arc_lift_over_linear_mid": round(arc_peak_z - linear_mid_z, 4),
        "object_count": len(objects),
        "tris": count_tris(objects),
        "special_delivery_later": cfg.get("special_later"),
    }

root = bpy.data.objects.new("hard_pipelines_root", None)
pipeline_collection.objects.link(root)
root.empty_display_type = "PLAIN_AXES"
root.empty_display_size = 0.4
for obj in pipeline_objects:
    if obj.parent is None:
        obj.parent = root

screenshots = {
    "citywide": render_still(
        make_camera("S49_Hard_Pipelines_Citywide", (96, -142, 96), (0, -5, 18), lens=15),
        "s49-hard-pipelines-citywide.png",
    ),
    "east_ring": render_still(
        make_camera("S49_Hard_Pipelines_East_Ring", (76, 48, 46), (28, 0, 18), lens=26),
        "s49-hard-pipelines-east-ring.png",
    ),
    "west_ring": render_still(
        make_camera("S49_Hard_Pipelines_West_Ring", (-82, 54, 52), (-20, 8, 18), lens=26),
        "s49-hard-pipelines-west-ring.png",
    ),
}

bpy.ops.wm.save_as_mainfile(filepath=SESSION_BLEND)

selected_for_export = [root] + pipeline_objects
export_selected_glb(DRAFT_GLB, selected_for_export)

pipeline_materials = collect_materials(pipeline_objects)
total_tris = count_tris(pipeline_objects)
file_size_bytes = os.path.getsize(DRAFT_GLB)

checks = {
    "approved_structure_assets_present": not missing_assets,
    "pipeline_count": len(pipeline_metrics) == len(HARD_PIPELINE_NAMES),
    "connects_from_sia_crown": all(item["start"][2] >= 35.0 for item in pipeline_metrics.values()),
    "connects_to_district_roofs": all(item["end"][2] > 8.0 for item in pipeline_metrics.values()),
    "arced_paths": all(item["arc_lift_over_linear_mid"] >= 12.0 for item in pipeline_metrics.values()),
    "ground_veins": len([obj for obj in pipeline_objects if "ground_vein" in obj.name]) >= len(HARD_PIPELINE_NAMES) * 8,
    "material_named_energy": pipeline_materials == ["energy"],
    "technical_budget": total_tris <= 1500 * len(HARD_PIPELINE_NAMES) + 700,
    "file_budget": file_size_bytes <= 40 * 1024 * len(HARD_PIPELINE_NAMES),
}

import_check = import_qa(DRAFT_GLB)
checks["approved_glb_reimports"] = import_check["mesh_count"] > 0
checks["approved_glb_materials_valid"] = import_check["materials_valid"]

overall = "APPROVED" if all(checks.values()) else "NEEDS REVIEW"
if overall == "APPROVED":
    shutil.copyfile(DRAFT_GLB, APPROVED_GLB)

report = {
    "session": 49,
    "asset": "energy-system/hard-pipelines",
    "scope": {
        "hard_pipeline_count": len(HARD_PIPELINE_NAMES),
        "targets": HARD_PIPELINE_NAMES,
        "note": (
            "Builds the hard-tube feed for all module specs that request hard delivery. "
            "Knowledgebase waterfall and Leaderboard lightning stylization remain separate "
            "Phase 5 special-delivery passes."
        ),
    },
    "source_layout_report": LATEST_LAYOUT_REPORT,
    "missing_assets": missing_assets,
    "pipeline_metrics": pipeline_metrics,
    "pipeline_materials": pipeline_materials,
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
print("SESSION 49 HARD PIPELINES COMPLETE")
print(f"Blend: {SESSION_BLEND}")
print(f"Draft GLB: {DRAFT_GLB}")
print(f"Approved GLB: {APPROVED_GLB}")
print(f"Report: {SESSION_REPORT}")
print(f"Total tris: {total_tris}")
print(f"File size: {file_size_bytes / 1024:.1f} KB")
print(f"Overall verdict: {overall}")
for check, value in checks.items():
    print(f"  {check}: {'PASS' if value else 'FAIL'}")

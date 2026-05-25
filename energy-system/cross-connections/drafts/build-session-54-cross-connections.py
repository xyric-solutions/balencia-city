"""
Session 54: Phase 5 cross-district gold connections.

Builds the six specified cross-pillar intelligence links, adds midpoint
insight-card anchors, renders QA evidence, exports a draft GLB, and promotes it
when checks pass.
"""

import json
import math
import os
import shutil
from mathutils import Vector

import bpy


THIS_FILE = os.path.abspath(__file__)
DRAFTS = os.path.dirname(THIS_FILE)
CROSS_DIR = os.path.dirname(DRAFTS)
ENERGY_DIR = os.path.dirname(CROSS_DIR)
PROJECT = os.path.dirname(ENERGY_DIR)
MODULES = os.path.join(PROJECT, "modules")
SHARED = os.path.join(PROJECT, "shared")
SCREENSHOTS = os.path.join(ENERGY_DIR, "screenshots")
APPROVED = os.path.join(CROSS_DIR, "approved")
SESSION_REPORT = os.path.join(DRAFTS, "cross-connections-session54-report.json")
SESSION_BLEND = os.path.join(DRAFTS, "cross-connections-session54.blend")
DRAFT_GLB = os.path.join(DRAFTS, "cross-connections-session54.glb")
APPROVED_GLB = os.path.join(APPROVED, "cross-district-gold.glb")
LATEST_LAYOUT_REPORT = os.path.join(
    MODULES, "11-nutrition", "integration-session-48-report.json"
)

PRIOR_ENERGY_ASSETS = {
    "hard_pipelines": os.path.join(ENERGY_DIR, "pipelines/approved/hard-pipelines.glb"),
    "warm_mist": os.path.join(ENERGY_DIR, "pipelines/approved/warm-mist.glb"),
    "faint_thread": os.path.join(ENERGY_DIR, "pipelines/approved/faint-thread.glb"),
    "knowledgebase_waterfall": os.path.join(
        ENERGY_DIR, "pipelines/approved/knowledgebase-waterfall.glb"
    ),
    "leaderboard_lightning": os.path.join(
        ENERGY_DIR, "pipelines/approved/leaderboard-lightning.glb"
    ),
}

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


CONNECTIONS = [
    {
        "id": "fitness_recovery",
        "from": "Fitness",
        "to": "Recovery",
        "insight": "Recovery score impacts tomorrow's workout capacity",
        "height_boost": 12.5,
        "side_offset": -5.2,
    },
    {
        "id": "nutrition_career",
        "from": "Nutrition",
        "to": "Career",
        "insight": "Skipped meals on meeting days reduce afternoon focus 31%",
        "height_boost": 15.0,
        "side_offset": 4.5,
    },
    {
        "id": "relationships_yoga",
        "from": "Relationships",
        "to": "Yoga",
        "insight": "Social connection improves recovery scores by 24%",
        "height_boost": 11.5,
        "side_offset": 7.4,
    },
    {
        "id": "finance_career",
        "from": "Finance",
        "to": "Career",
        "insight": "Spending increases 40% during high-stress work weeks",
        "height_boost": 10.0,
        "side_offset": -3.8,
    },
    {
        "id": "recovery_analytics",
        "from": "Recovery",
        "to": "Analytics",
        "insight": "Evening meditation correlates with next-day focus scores",
        "height_boost": 9.0,
        "side_offset": 3.2,
    },
    {
        "id": "chat_relationships",
        "from": "Chat",
        "to": "Relationships",
        "insight": "You haven't spoken to [name] in 14 days",
        "height_boost": 8.5,
        "side_offset": -2.8,
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
            eevee.bloom_intensity = 0.82
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.6


def make_gold_energy_material():
    mat = bpy.data.materials.new("energy")
    mat.diffuse_color = (0.96, 0.62, 0.04, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (0.96, 0.62, 0.04, 1.0)
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (0.96, 0.62, 0.04, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 0.8
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.25
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
    mn = Vector((min(v.x for v in mins), min(v.y for v in mins), min(v.z for v in mins),))
    mx = Vector((max(v.x for v in maxs), max(v.y for v in maxs), max(v.z for v in maxs),))
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


def append_tube(vertices, faces, points, radius, sides=8):
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


def append_octahedron(vertices, faces, center, radius):
    start = len(vertices)
    vertices.extend(
        [
            (center.x, center.y, center.z + radius),
            (center.x + radius, center.y, center.z),
            (center.x, center.y + radius, center.z),
            (center.x - radius, center.y, center.z),
            (center.x, center.y - radius, center.z),
            (center.x, center.y, center.z - radius),
        ]
    )
    faces.extend(
        [
            (start, start + 1, start + 2),
            (start, start + 2, start + 3),
            (start, start + 3, start + 4),
            (start, start + 4, start + 1),
            (start + 5, start + 2, start + 1),
            (start + 5, start + 3, start + 2),
            (start + 5, start + 4, start + 3),
            (start + 5, start + 1, start + 4),
        ]
    )


def quadratic_point(start, peak, end, t):
    return ((1 - t) ** 2) * start + 2 * (1 - t) * t * peak + (t**2) * end


def connection_points(from_box, to_box, height_boost, side_offset):
    start = Vector((from_box["center"].x, from_box["center"].y, from_box["max"].z + 1.05))
    end = Vector((to_box["center"].x, to_box["center"].y, to_box["max"].z + 1.05))
    mid = (start + end) * 0.5
    direction = Vector((end.x - start.x, end.y - start.y, 0))
    if direction.length == 0:
        direction = Vector((1, 0, 0))
    direction.normalize()
    perp = Vector((-direction.y, direction.x, 0))
    mid += perp * side_offset
    mid.z = max(start.z, end.z) + height_boost
    points = [quadratic_point(start, mid, end, idx / 6.0) for idx in range(7)]
    return start, mid, end, points


def create_connection_mesh(cfg, registry, mat, collection):
    from_box = registry[cfg["from"]]["bbox"]
    to_box = registry[cfg["to"]]["bbox"]
    if from_box is None or to_box is None:
        raise RuntimeError(f"Missing bbox for connection {cfg['id']}")

    start, mid, end, points = connection_points(
        from_box, to_box, cfg["height_boost"], cfg["side_offset"]
    )
    vertices = []
    faces = []
    append_tube(vertices, faces, points, 0.038, sides=8)
    append_ring(vertices, faces, mid + Vector((0, 0, 0.02)), 0.36, 0.72, sides=24)
    append_octahedron(vertices, faces, start, 0.20)
    append_octahedron(vertices, faces, end, 0.20)
    for t in (0.28, 0.50, 0.72):
        append_octahedron(vertices, faces, quadratic_point(start, mid, end, t), 0.13)

    mesh = bpy.data.meshes.new(f"{cfg['id']}_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(f"cross_gold_{cfg['id']}", mesh)
    obj.data.materials.append(mat)
    obj["connection_id"] = cfg["id"]
    obj["connection_from"] = registry[cfg["from"]]["config"]["label"]
    obj["connection_to"] = registry[cfg["to"]]["config"]["label"]
    obj["insight"] = cfg["insight"]
    obj["runtime_hint"] = "cross-district gold line, activate emissive pulse and midpoint insight card"
    collection.objects.link(obj)

    anchor = bpy.data.objects.new(f"insight_anchor_{cfg['id']}", None)
    anchor.empty_display_type = "PLAIN_AXES"
    anchor.empty_display_size = 0.5
    anchor.location = mid
    anchor["connection_id"] = cfg["id"]
    anchor["connection_from"] = registry[cfg["from"]]["config"]["label"]
    anchor["connection_to"] = registry[cfg["to"]]["config"]["label"]
    anchor["insight"] = cfg["insight"]
    anchor["runtime_hint"] = "floating insight card anchor"
    collection.objects.link(anchor)

    linear_mid_z = (start.z + end.z) * 0.5
    metrics = {
        "from_key": cfg["from"],
        "to_key": cfg["to"],
        "from": registry[cfg["from"]]["config"]["label"],
        "to": registry[cfg["to"]]["config"]["label"],
        "insight": cfg["insight"],
        "start": [round(start.x, 4), round(start.y, 4), round(start.z, 4)],
        "end": [round(end.x, 4), round(end.y, 4), round(end.z, 4)],
        "midpoint_anchor": [round(mid.x, 4), round(mid.y, 4), round(mid.z, 4)],
        "arc_peak_z": round(mid.z, 4),
        "linear_mid_z": round(linear_mid_z, 4),
        "arc_lift_over_linear_mid": round(mid.z - linear_mid_z, 4),
        "endpoint_clearance": {
            "from": round(start.z - from_box["max"].z, 4),
            "to": round(end.z - to_box["max"].z, 4),
        },
        "distance_xy": round((Vector((end.x, end.y, 0)) - Vector((start.x, start.y, 0))).length, 4),
        "tris": count_tris([obj]),
    }
    return obj, anchor, metrics


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
    empty_objects = [obj for obj in objects if obj.type == "EMPTY"]
    materials = collect_materials(mesh_objects)
    anchors = [obj for obj in empty_objects if obj.name.startswith("insight_anchor_")]
    return {
        "object_count": len(objects),
        "mesh_count": len(mesh_objects),
        "empty_count": len(empty_objects),
        "anchor_count": len(anchors),
        "tris": count_tris(mesh_objects),
        "materials": materials,
        "materials_valid": materials == ["energy"],
        "file_size_bytes": os.path.getsize(glb_path),
    }


print("=" * 72)
print("Session 54: Cross-District Gold Connections")
print("=" * 72)

bpy.ops.wm.read_factory_settings(use_empty=True)
energy_mat = make_gold_energy_material()

lighting = load_python_module(os.path.join(SHARED, "lighting-rig.py"), "lighting_rig")
lighting["clear_lighting"]()
lighting["setup_viewport_lighting"]()
setup_render()

context_collection = bpy.data.collections.new("Approved_Structure_Context")
bpy.context.scene.collection.children.link(context_collection)
prior_energy_collection = bpy.data.collections.new("Approved_Energy_Context")
bpy.context.scene.collection.children.link(prior_energy_collection)
connection_collection = bpy.data.collections.new("Cross_District_Gold_S54")
bpy.context.scene.collection.children.link(connection_collection)

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

prior_energy_imports = {}
for key, path in PRIOR_ENERGY_ASSETS.items():
    collection = bpy.data.collections.new(key)
    prior_energy_collection.children.link(collection)
    prior_energy_imports[key] = import_glb(path, collection) if os.path.exists(path) else []

connection_objects = []
anchor_objects = []
connection_metrics = {}

for cfg in CONNECTIONS:
    obj, anchor, metrics = create_connection_mesh(cfg, registry, energy_mat, connection_collection)
    connection_objects.append(obj)
    anchor_objects.append(anchor)
    connection_metrics[cfg["id"]] = metrics

root = bpy.data.objects.new("cross_district_gold_root", None)
root.empty_display_type = "PLAIN_AXES"
root.empty_display_size = 0.4
connection_collection.objects.link(root)
for obj in connection_objects + anchor_objects:
    obj.parent = root

screenshots = {
    "citywide": render_still(
        make_camera("S54_Cross_Gold_Citywide", (96, -142, 100), (0, -10, 20), lens=15),
        "s54-cross-connections-citywide.png",
    ),
    "north_south_span": render_still(
        make_camera("S54_Cross_Gold_North_South", (44, 92, 56), (-8, -3, 19), lens=22),
        "s54-cross-connections-north-south.png",
    ),
    "southwest_cluster": render_still(
        make_camera("S54_Cross_Gold_Southwest", (-78, -74, 48), (-16, -38, 15), lens=25),
        "s54-cross-connections-southwest.png",
    ),
}

bpy.ops.wm.save_as_mainfile(filepath=SESSION_BLEND)

selected_for_export = [root] + connection_objects + anchor_objects
export_selected_glb(DRAFT_GLB, selected_for_export)

connection_materials = collect_materials(connection_objects)
total_tris = count_tris(connection_objects)
file_size_bytes = os.path.getsize(DRAFT_GLB)
expected_pairs = {(item["from"], item["to"]) for item in CONNECTIONS}
actual_pairs = {
    (metrics["from_key"], metrics["to_key"])
    for metrics in connection_metrics.values()
}

checks = {
    "approved_structure_assets_present": not missing_assets,
    "prior_energy_assets_present": all(
        os.path.exists(path) and len(prior_energy_imports[key]) > 0
        for key, path in PRIOR_ENERGY_ASSETS.items()
    ),
    "connection_count": len(connection_objects) == 6,
    "connection_pairs_match_spec": actual_pairs == expected_pairs,
    "arced_paths": all(
        item["arc_lift_over_linear_mid"] >= 4.0 for item in connection_metrics.values()
    ),
    "endpoints_clear_roofs": all(
        item["endpoint_clearance"]["from"] >= 1.0 and item["endpoint_clearance"]["to"] >= 1.0
        for item in connection_metrics.values()
    ),
    "midpoint_anchors": len(anchor_objects) == len(CONNECTIONS)
    and all(bool(anchor.get("insight")) for anchor in anchor_objects),
    "material_named_energy": connection_materials == ["energy"],
    "technical_budget": all(
        100 <= item["tris"] <= 300 for item in connection_metrics.values()
    )
    and total_tris <= 1800,
    "file_budget": file_size_bytes <= 70 * 1024,
}

import_check = import_qa(DRAFT_GLB)
checks["approved_glb_reimports"] = import_check["mesh_count"] == len(CONNECTIONS)
checks["approved_glb_materials_valid"] = import_check["materials_valid"]
checks["approved_glb_anchor_count"] = import_check["anchor_count"] == len(CONNECTIONS)

overall = "APPROVED" if all(checks.values()) else "NEEDS REVIEW"
if overall == "APPROVED":
    shutil.copyfile(DRAFT_GLB, APPROVED_GLB)

report = {
    "session": 54,
    "asset": "energy-system/cross-connections",
    "scope": {
        "connection_count": len(CONNECTIONS),
        "targets": [item["id"] for item in CONNECTIONS],
        "note": (
            "Builds the minimum six cross-district intelligence links as thin "
            "gold #F59E0B emissive geometry. The material is intentionally named "
            "energy for runtime override compatibility, with midpoint empties for "
            "floating insight cards."
        ),
    },
    "source_layout_report": LATEST_LAYOUT_REPORT,
    "missing_assets": missing_assets,
    "prior_energy_assets": PRIOR_ENERGY_ASSETS,
    "structure_scales": {name: bbox_dict(item["bbox"]) for name, item in registry.items() if item["bbox"]},
    "connection_metrics": connection_metrics,
    "connection_materials": connection_materials,
    "gold_hex": "#F59E0B",
    "emission_strength": 0.8,
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
print("SESSION 54 CROSS-DISTRICT GOLD CONNECTIONS COMPLETE")
print(f"Blend: {SESSION_BLEND}")
print(f"Draft GLB: {DRAFT_GLB}")
print(f"Approved GLB: {APPROVED_GLB}")
print(f"Report: {SESSION_REPORT}")
print(f"Total tris: {total_tris}")
print(f"File size: {file_size_bytes / 1024:.1f} KB")
print(f"Overall verdict: {overall}")
for check, value in checks.items():
    print(f"  {check}: {'PASS' if value else 'FAIL'}")

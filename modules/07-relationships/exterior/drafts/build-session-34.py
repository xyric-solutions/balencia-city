"""
Balencia City v3 - Module #07 Relationships
Session 34: Exterior Detail, Polish, Export

Loads the Session 33 Relationships major forms, adds the deferred garden detail
pass, exports the exterior GLB, validates import metrics, and captures the
all-nine-structure cohesion screenshot.
"""

import importlib.util
import json
import math
import os
import shutil
import sys

import bpy
from mathutils import Matrix, Vector


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/07-relationships")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
APPROVED = os.path.join(MODULE, "exterior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")

S33_BLEND = os.path.join(DRAFTS, "relationships-s33-major-forms.blend")
S34_BLEND = os.path.join(DRAFTS, "relationships-s34-detail-export.blend")
PACKED_BLEND = os.path.join(DRAFTS, "relationships-s34-export-packed.blend")
DRAFT_GLB = os.path.join(DRAFTS, "relationships-ext-draft-s34.glb")
APPROVED_GLB = os.path.join(APPROVED, "relationships-ext.glb")
METRICS_FILE = os.path.join(DRAFTS, "session34-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS, "session34-qa-import.json")

ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy"}
DISTRICT_HEX = "#F43F5E"

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s34", os.path.join(ROOT, "shared/lighting-rig.py"))
materials_mod = load_module("balencia_materials_s34", os.path.join(ROOT, "shared/material-library.py"))

created_categories = {}


def register(obj, category):
    if obj is not None:
        created_categories[obj.name] = category
    return obj


def material_base_name(material):
    return material.name.split(".")[0] if material else ""


def ensure_materials():
    mats = {name: bpy.data.materials.get(name) for name in ALLOWED_MATERIALS}
    if any(mat is None for mat in mats.values()):
        materials_mod.create_materials(DISTRICT_HEX, include_energy=True, include_holo=False)
    return {name: bpy.data.materials.get(name) for name in ALLOWED_MATERIALS}


def assign(obj, mat):
    if obj is None or obj.type != "MESH":
        return obj
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def apply_transforms(obj):
    if obj is None:
        return obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    return obj


def normalize_material_slots():
    mats = ensure_materials()
    fallback = mats["detail"]
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        if not obj.data.materials:
            obj.data.materials.append(fallback)
        for index, material in enumerate(obj.data.materials):
            base = material_base_name(material)
            if base in mats and mats[base] is not None:
                obj.data.materials[index] = mats[base]
            else:
                obj.data.materials[index] = fallback

    for mat in list(bpy.data.materials):
        base = material_base_name(mat)
        if base in ALLOWED_MATERIALS and mat.name != base and mat.users == 0:
            bpy.data.materials.remove(mat)


def current_object():
    obj = getattr(bpy.context.view_layer.objects, "active", None)
    if obj is not None:
        return obj
    selected = getattr(bpy.context, "selected_objects", [])
    if selected:
        return selected[-1]
    raise RuntimeError("No active object after primitive creation")


def make_mesh(name, verts, faces, mat, category, shade=True):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    if shade:
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return register(obj, category)


def cuboid_vertices(loc, dims, rot_z=0.0):
    x, y, z = dims[0] / 2.0, dims[1] / 2.0, dims[2] / 2.0
    corners = [
        Vector((-x, -y, -z)),
        Vector((x, -y, -z)),
        Vector((x, y, -z)),
        Vector((-x, y, -z)),
        Vector((-x, -y, z)),
        Vector((x, -y, z)),
        Vector((x, y, z)),
        Vector((-x, y, z)),
    ]
    rot = Matrix.Rotation(rot_z, 4, "Z")
    base = Vector(loc)
    return [tuple(base + rot @ corner) for corner in corners]


def box_mesh(name, boxes, mat, category):
    verts = []
    faces = []
    for loc, dims, rot_z in boxes:
        idx = len(verts)
        verts.extend(cuboid_vertices(loc, dims, rot_z))
        faces.extend(
            [
                (idx + 0, idx + 1, idx + 2, idx + 3),
                (idx + 4, idx + 7, idx + 6, idx + 5),
                (idx + 0, idx + 4, idx + 5, idx + 1),
                (idx + 1, idx + 5, idx + 6, idx + 2),
                (idx + 2, idx + 6, idx + 7, idx + 3),
                (idx + 3, idx + 7, idx + 4, idx + 0),
            ]
        )
    return make_mesh(name, verts, faces, mat, category, shade=False)


def add_box(name, loc, dims, mat, category, rot_z=0.0):
    return box_mesh(name, [(loc, dims, rot_z)], mat, category)


def cylinder(name, loc, radius, depth, mat, category, vertices=8, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, mat, category, vertices=7, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices, radius1=radius1, radius2=radius2, depth=depth, location=loc, rotation=rot
    )
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def torus(name, loc, major, minor, mat, category, seg=24, minor_seg=4):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=seg,
        minor_segments=minor_seg,
        major_radius=major,
        minor_radius=minor,
        location=loc,
    )
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def cylinder_between(name, start, end, radius, mat, category, vertices=6):
    start = Vector(start)
    end = Vector(end)
    direction = end - start
    length = direction.length
    if length < 0.001:
        return None
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=(start + end) * 0.5)
    obj = current_object()
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def oriented_box_between(name, start_xy, end_xy, z, width, height, mat, category):
    sx, sy = start_xy
    ex, ey = end_xy
    dx = ex - sx
    dy = ey - sy
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    return add_box(name, ((sx + ex) * 0.5, (sy + ey) * 0.5, z), (length, width, height), mat, category, angle)


def ellipse_band(name, outer_rx, outer_ry, inner_rx, inner_ry, z0, z1, mat, category, segments=48, center=(0, 0)):
    cx, cy = center
    verts = []
    for i in range(segments):
        a = math.tau * i / segments
        co = math.cos(a)
        si = math.sin(a)
        verts.extend(
            [
                (cx + outer_rx * co, cy + outer_ry * si, z0),
                (cx + outer_rx * co, cy + outer_ry * si, z1),
                (cx + inner_rx * co, cy + inner_ry * si, z1),
                (cx + inner_rx * co, cy + inner_ry * si, z0),
            ]
        )
    faces = []
    for i in range(segments):
        j = (i + 1) % segments
        a = i * 4
        b = j * 4
        faces.append((a + 0, b + 0, b + 1, a + 1))
        faces.append((a + 1, b + 1, b + 2, a + 2))
        faces.append((a + 2, b + 2, b + 3, a + 3))
        faces.append((a + 3, b + 3, b + 0, a + 0))
    return make_mesh(name, verts, faces, mat, category)


def ellipse_arc_segments(name, rx, ry, z, mat, category, segments=18, radius=0.028, center=(0, 0), start=0, end=math.tau):
    cx, cy = center
    points = []
    for i in range(segments + 1):
        t = i / segments
        a = start + (end - start) * t
        points.append((cx + math.cos(a) * rx, cy + math.sin(a) * ry, z))
    for i in range(segments):
        cylinder_between(f"{name}_{i:02d}", points[i], points[i + 1], radius, mat, category, vertices=5)


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
            eevee.bloom_threshold = 0.42
            eevee.bloom_intensity = 0.55
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.55


def setup_lighting():
    lighting.clear_lighting()
    lighting.setup_viewport_lighting()
    setup_render()


def render_shot(filename, camera_loc, target, lens=42):
    cam_data = bpy.data.cameras.new(filename.replace(".png", "_Camera"))
    cam = bpy.data.objects.new(filename.replace(".png", "_Camera"), cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    direction = Vector(target) - Vector(camera_loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.clip_start = 0.1
    cam.data.clip_end = 260
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = os.path.join(SCREENSHOTS, filename)
    bpy.ops.render.render(write_still=True)
    return bpy.context.scene.render.filepath


def set_emission_strengths(value):
    previous = {}
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        node = mat.node_tree.nodes.get("Principled BSDF")
        if not node or "Emission Strength" not in node.inputs:
            continue
        previous[mat.name] = node.inputs["Emission Strength"].default_value
        node.inputs["Emission Strength"].default_value = value
    return previous


def restore_emission_strengths(previous):
    for mat in bpy.data.materials:
        if mat.name not in previous or not mat.use_nodes:
            continue
        node = mat.node_tree.nodes.get("Principled BSDF")
        if node and "Emission Strength" in node.inputs:
            node.inputs["Emission Strength"].default_value = previous[mat.name]


def render_dark_first():
    previous = set_emission_strengths(0.0)
    path = render_shot("s34_dark_first.png", (18, -22, 8.8), (0, -0.4, 3.4), 42)
    restore_emission_strengths(previous)
    return path


def get_tri_count(obj):
    if obj.type != "MESH":
        return 0
    obj.data.calc_loop_triangles()
    return len(obj.data.loop_triangles)


def scene_triangles():
    return sum(get_tri_count(obj) for obj in bpy.data.objects if obj.type == "MESH")


def material_triangles():
    totals = {}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        mat_name = obj.data.materials[0].name if obj.data.materials else "NONE"
        mat_name = mat_base = mat_name.split(".")[0]
        totals[mat_base] = totals.get(mat_base, 0) + get_tri_count(obj)
    return dict(sorted(totals.items()))


def material_percentages(total_tris, mat_tris):
    if not total_tris:
        return {}
    return {name: round((tris / total_tris) * 100.0, 2) for name, tris in mat_tris.items()}


def material_surface_area():
    totals = {}
    total = 0.0
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for poly in obj.data.polygons:
            mat_name = obj.data.materials[poly.material_index].name if obj.data.materials else "NONE"
            mat_name = mat_name.split(".")[0]
            totals[mat_name] = totals.get(mat_name, 0.0) + poly.area
            total += poly.area
    return {
        "total": round(total, 3),
        "areas": {name: round(area, 3) for name, area in sorted(totals.items())},
        "percentages": {
            name: round((area / total) * 100.0, 2) for name, area in sorted(totals.items())
        } if total else {},
    }


def category_for_name(name):
    if name in created_categories:
        return created_categories[name]
    if "bridge" in name or "landing" in name or "crossing" in name or "walkway" in name:
        return "Bridges, walkways, and rail articulation"
    if "moat" in name or "water" in name or "shore" in name or "ripple" in name:
        return "Water moat and edge polish"
    if "dome" in name or "gathering_glow" in name:
        return "Glass roof domes and warm gathering glow"
    if "terrace" in name or "planter" in name or "garden" in name or "bloom" in name or "leaf" in name:
        return "Garden terraces, planters, and vegetation"
    if "portal" in name or "entry" in name:
        return "Curved welcoming entrances"
    if "mist" in name or "energy" in name or "receiver" in name:
        return "Warm mist roof receiver"
    if "floor_indicator" in name or "facade" in name or "panel" in name:
        return "Low pavilion facade articulation"
    return "Low curved pavilion body"


def object_metrics():
    rows = []
    for obj in sorted((o for o in bpy.data.objects if o.type == "MESH"), key=lambda o: o.name):
        rows.append(
            {
                "name": obj.name,
                "tris": get_tri_count(obj),
                "material": obj.data.materials[0].name.split(".")[0] if obj.data.materials else "NONE",
                "category": category_for_name(obj.name),
            }
        )
    return rows


def category_metrics():
    totals = {}
    counts = {}
    for row in object_metrics():
        category = row["category"]
        totals[category] = totals.get(category, 0) + row["tris"]
        counts[category] = counts.get(category, 0) + 1
    return [
        {"category": category, "objects": counts[category], "tris": totals[category]}
        for category in sorted(totals)
    ]


def bbox_vectors():
    coords = []
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for vertex in obj.data.vertices:
            coords.append(obj.matrix_world @ vertex.co)
    if not coords:
        return Vector((0, 0, 0)), Vector((0, 0, 0))
    return (
        Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords))),
        Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords))),
    )


def bbox():
    min_v, max_v = bbox_vectors()
    return {
        "min": [round(min_v.x, 4), round(min_v.y, 4), round(min_v.z, 4)],
        "max": [round(max_v.x, 4), round(max_v.y, 4), round(max_v.z, 4)],
    }


def rebalance_existing_glow(mats):
    """Keep rose glow intentional, but avoid neon-overload from every floor band."""
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        name = obj.name
        if "rose_floor_indicator_band" in name:
            digits = "".join(ch for ch in name.split("rose_floor_indicator_band_")[-1][:2] if ch.isdigit())
            floor = int(digits) if digits else 0
            if floor not in {1, 2, 5, 10, 14, 15}:
                assign(obj, mats["accent"])
        if "warm_rose_lip" in name:
            assign(obj, mats["accent"])
        if "rounded_planter_shelf" in name:
            assign(obj, mats["base"])


def add_facade_detail(mats):
    levels = [
        {"z": 0.22, "rx": 8.15, "ry": 4.72, "center": (0.0, 0.0), "phase": 0.10},
        {"z": 1.28, "rx": 7.78, "ry": 4.48, "center": (-0.14, 0.04), "phase": 0.12},
        {"z": 2.40, "rx": 6.75, "ry": 3.92, "center": (0.18, -0.02), "phase": 0.18},
        {"z": 3.62, "rx": 5.48, "ry": 3.08, "center": (-0.10, 0.10), "phase": 0.15},
        {"z": 4.78, "rx": 4.18, "ry": 2.42, "center": (0.12, -0.02), "phase": 0.22},
        {"z": 5.92, "rx": 3.10, "ry": 1.82, "center": (0.0, 0.05), "phase": 0.17},
    ]

    def interp(z):
        lower = max(i for i, item in enumerate(levels[:-1]) if item["z"] <= z)
        upper = min(lower + 1, len(levels) - 1)
        span = levels[upper]["z"] - levels[lower]["z"]
        t = 0 if span == 0 else (z - levels[lower]["z"]) / span
        rx = levels[lower]["rx"] + (levels[upper]["rx"] - levels[lower]["rx"]) * t
        ry = levels[lower]["ry"] + (levels[upper]["ry"] - levels[lower]["ry"]) * t
        cx = levels[lower]["center"][0] + (levels[upper]["center"][0] - levels[lower]["center"][0]) * t
        cy = levels[lower]["center"][1] + (levels[upper]["center"][1] - levels[lower]["center"][1]) * t
        return rx, ry, cx, cy

    min_z = levels[0]["z"]
    max_z = levels[-1]["z"]
    for floor in range(1, 15, 2):
        z = min_z + (max_z - min_z) * (floor + 0.48) / 15.0
        rx, ry, cx, cy = interp(z)
        ellipse_band(
            f"dark_curved_facade_recess_panel_floor_{floor:02d}",
            rx + 0.035,
            ry + 0.035,
            rx - 0.095,
            ry - 0.095,
            z - 0.030,
            z + 0.030,
            mats["base"],
            "Low pavilion facade articulation",
            segments=12,
            center=(cx, cy),
        )

    for idx, angle in enumerate(range(0, 360, 30)):
        a = math.radians(angle)
        rx, ry, cx, cy = interp(3.0)
        x = cx + math.cos(a) * (rx + 0.09)
        y = cy + math.sin(a) * (ry + 0.09)
        cylinder_between(
            f"subtle_vertical_facade_mullion_{idx:02d}",
            (x, y, 0.56),
            (x * 0.62, y * 0.62, 5.52),
            0.018,
            mats["detail"],
            "Low pavilion facade articulation",
            vertices=5,
        )


def add_water_edge_polish(mats):
    ellipse_band(
        "outer_moat_obsidian_ground_apron",
        12.58,
        7.86,
        12.05,
        7.52,
        0.015,
        0.045,
        mats["base"],
        "Water moat and edge polish",
        segments=36,
    )
    ellipse_band(
        "outer_moat_pedestrian_shadow_walkway",
        13.45,
        8.45,
        12.62,
        7.88,
        0.040,
        0.075,
        mats["detail"],
        "Water moat and edge polish",
        segments=36,
    )
    ellipse_band(
        "outer_still_water_dark_shoreline_trim",
        11.96,
        7.50,
        11.72,
        7.26,
        0.085,
        0.135,
        mats["detail"],
        "Water moat and edge polish",
        segments=42,
    )
    ellipse_band(
        "inner_island_waterline_soft_shadow_trim",
        9.36,
        5.68,
        9.10,
        5.42,
        0.115,
        0.165,
        mats["detail"],
        "Water moat and edge polish",
        segments=42,
    )
    ellipse_arc_segments(
        "subtle_reflective_moat_ripple_outer",
        10.95,
        6.75,
        0.091,
        mats["glass"],
        "Water moat and edge polish",
        segments=22,
        radius=0.012,
        start=math.radians(18),
        end=math.radians(156),
    )
    ellipse_arc_segments(
        "subtle_reflective_moat_ripple_inner",
        9.82,
        6.04,
        0.095,
        mats["glass"],
        "Water moat and edge polish",
        segments=20,
        radius=0.011,
        start=math.radians(205),
        end=math.radians(334),
    )
    ellipse_arc_segments(
        "low_rose_wayfinding_thread_moat_edge",
        12.34,
        7.68,
        0.105,
        mats["emissive"],
        "Water moat and edge polish",
        segments=4,
        radius=0.024,
        start=math.radians(190),
        end=math.radians(350),
    )


def add_bridge_articulation(mats):
    bridge_specs = [
        ("front_south", -90, 8.75, 12.25, 0.78),
        ("east", 0, 8.75, 12.25, 0.78),
        ("north_west", 140, 8.75, 12.25, 0.78),
        ("south_west", -150, 8.75, 12.25, 0.78),
    ]
    for name, angle_deg, inner_r, outer_r, width in bridge_specs:
        angle = math.radians(angle_deg)
        direction = Vector((math.cos(angle), math.sin(angle), 0.0))
        normal = Vector((-math.sin(angle), math.cos(angle), 0.0))
        start = direction * inner_r
        end = direction * outer_r
        rail_offset = width * 0.54
        for side, sign in (("left", -1), ("right", 1)):
            for idx, t in enumerate((0.16, 0.50, 0.84)):
                p = start.lerp(end, t) + normal * rail_offset * sign
                cylinder(
                    f"{name}_bridge_{side}_warm_post_{idx:02d}",
                    (p.x, p.y, 0.67),
                    0.040,
                    0.56,
                    mats["detail"],
                    "Bridges, walkways, and rail articulation",
                    vertices=6,
                )
        for idx, t in enumerate((0.30, 0.70)):
            p = start.lerp(end, t)
            oriented_box_between(
                f"{name}_bridge_dark_paver_joint_{idx:02d}",
                (p.x - normal.x * width * 0.34, p.y - normal.y * width * 0.34),
                (p.x + normal.x * width * 0.34, p.y + normal.y * width * 0.34),
                0.425,
                0.055,
                0.030,
                mats["base"],
                "Bridges, walkways, and rail articulation",
            )

    start = Vector((7.35, 3.55, 0.74))
    end = Vector((15.85, 6.85, 0.74))
    direction = end - start
    normal = Vector((-direction.y, direction.x, 0.0)).normalized()
    for side, sign in (("left", -1), ("right", 1)):
        for idx, t in enumerate((0.16, 0.38, 0.62, 0.84)):
            p = start.lerp(end, t) + normal * 0.50 * sign
            cylinder(
                f"adjacent_connection_bridge_{side}_intimate_post_{idx:02d}",
                (p.x, p.y, p.z),
                0.042,
                0.62,
                mats["detail"],
                "Bridges, walkways, and rail articulation",
                vertices=6,
            )
    for idx, t in enumerate((0.20, 0.40, 0.60, 0.80)):
        p = start.lerp(end, t)
        add_box(
            f"adjacent_connection_bridge_recessed_paver_{idx:02d}",
            (p.x, p.y, 0.605),
            (0.12, 0.82, 0.035),
            mats["base"],
            "Bridges, walkways, and rail articulation",
            math.atan2(direction.y, direction.x),
        )


def add_dome_frames_and_glow(mats):
    domes = [
        ("central_family", (0.0, -0.15, 6.26), (1.25, 0.92, 0.58)),
        ("west_intimate", (-2.85, 1.10, 5.22), (0.92, 0.70, 0.44)),
        ("east_intimate", (2.72, 0.92, 5.18), (0.88, 0.68, 0.42)),
    ]
    for prefix, loc, scale in domes:
        x, y, z = loc
        torus(
            f"{prefix}_dome_dark_base_frame_ring",
            (x, y, z - scale[2] * 0.52),
            max(scale[0], scale[1]) * 0.72,
            0.025,
            mats["detail"],
            "Glass roof domes and warm gathering glow",
            seg=18,
            minor_seg=4,
        )
        for rib_idx, angle in enumerate((0, 90)):
            a = math.radians(angle)
            points = []
            for step in range(5):
                t = step / 4.0
                theta = math.pi * t
                lateral = math.cos(theta) * scale[0] * 0.66
                height = math.sin(theta) * scale[2] * 0.95
                point = Vector((x, y, z - scale[2] * 0.52 + height))
                point += Vector((math.cos(a), math.sin(a), 0.0)) * lateral
                points.append(point)
            for i in range(len(points) - 1):
                cylinder_between(
                    f"{prefix}_dome_soft_structural_rib_{rib_idx:02d}_{i:02d}",
                    points[i],
                    points[i + 1],
                    0.020,
                    mats["detail"],
                    "Glass roof domes and warm gathering glow",
                    vertices=5,
                )
        for idx, angle in enumerate((30, 150, 270)):
            a = math.radians(angle)
            cylinder_between(
                f"{prefix}_visible_warm_room_glow_thread_{idx:02d}",
                (x, y, z - scale[2] * 0.46),
                (x + math.cos(a) * scale[0] * 0.46, y + math.sin(a) * scale[1] * 0.46, z - scale[2] * 0.40),
                0.018,
                mats["emissive"],
                "Glass roof domes and warm gathering glow",
                vertices=5,
            )


def add_garden_vegetation_detail(mats):
    terraces = [
        (7.95, 4.55, 1.62, 20, 0.08),
        (6.92, 3.98, 2.82, 16, 0.28),
        (5.58, 3.14, 4.04, 14, 0.48),
        (4.32, 2.42, 5.16, 10, 0.10),
        (3.08, 1.74, 6.26, 8, 0.34),
    ]
    bloom_index = 0
    for rx, ry, z, count, phase in terraces:
        for idx in range(count):
            if idx % 3 != 0:
                continue
            a = phase + math.tau * idx / count
            x = math.cos(a) * rx
            y = math.sin(a) * ry
            normal_angle = a + math.pi * 0.5
            cone(
                f"terrace_rose_bloom_cluster_{bloom_index:02d}",
                (x, y, z + 0.10),
                0.105,
                0.025,
                0.18,
                mats["accent"],
                "Garden terraces, planters, and vegetation",
                vertices=6,
                rot=(0, 0, normal_angle),
            )
            cone(
                f"terrace_dark_leaf_fan_{bloom_index:02d}",
                (x * 0.992, y * 0.992, z + 0.05),
                0.075,
                0.010,
                0.22,
                mats["detail"],
                "Garden terraces, planters, and vegetation",
                vertices=5,
                rot=(math.radians(72), 0, normal_angle),
            )
            bloom_index += 1

    planter_positions = [
        (-2.55, -6.10, 0.52),
        (2.50, -6.02, 0.52),
        (-4.85, -4.62, 0.52),
        (4.72, -4.42, 0.52),
        (-7.10, 1.18, 0.52),
        (7.05, 1.28, 0.52),
    ]
    for p_idx, (x, y, z) in enumerate(planter_positions):
        for idx, angle in enumerate((15, 105, 205, 295)):
            a = math.radians(angle)
            cone(
                f"entry_planter_visible_rose_bud_{p_idx:02d}_{idx:02d}",
                (x + math.cos(a) * 0.32, y + math.sin(a) * 0.13, z + 0.06),
                0.075,
                0.018,
                0.14,
                mats["emissive"] if idx == 0 else mats["accent"],
                "Garden terraces, planters, and vegetation",
                vertices=6,
            )


def add_portal_and_mist_polish(mats):
    portal_specs = [
        ("south_primary", (0.0, -5.28), 2.45, math.radians(90)),
        ("west_secondary", (-7.32, 0.28), 1.75, math.radians(0)),
    ]
    for prefix, center, width, angle in portal_specs:
        cx, cy = center
        forward = Vector((math.cos(angle), math.sin(angle), 0.0))
        right = Vector((-math.sin(angle), math.cos(angle), 0.0))
        for side, sign in (("left", -1), ("right", 1)):
            base = Vector((cx, cy, 0.84)) + right * width * 0.58 * sign
            cylinder_between(
                f"{prefix}_portal_thick_outer_{side}_return",
                base - forward * 0.36,
                base + forward * 0.36,
                0.052,
                mats["detail"],
                "Curved welcoming entrances",
                vertices=6,
            )
        oriented_box_between(
            f"{prefix}_portal_dark_threshold_paver",
            (cx - right.x * width * 0.40, cy - right.y * width * 0.40),
            (cx + right.x * width * 0.40, cy + right.y * width * 0.40),
            0.395,
            0.12,
            0.040,
            mats["base"],
            "Curved welcoming entrances",
        )

    for idx, angle in enumerate(range(0, 360, 45)):
        a = math.radians(angle)
        cylinder_between(
            f"roof_mist_diffuser_fine_spoke_{idx:02d}",
            (math.cos(a) * 0.32, math.sin(a) * 0.32 + 0.06, 6.78),
            (math.cos(a) * 0.88, math.sin(a) * 0.88 + 0.06, 6.82),
            0.018,
            mats["energy"],
            "Warm mist roof receiver",
            vertices=5,
        )


def remove_cameras_lights():
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)


def apply_mesh_world_transforms():
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(obj.matrix_world.copy())
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)
        obj.parent = None


def center_bottom_origin():
    min_v, max_v = bbox_vectors()
    correction = Matrix.Translation(Vector((-(min_v.x + max_v.x) / 2.0, -(min_v.y + max_v.y) / 2.0, -min_v.z)))
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(correction)
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)


def pack_export_meshes_by_material():
    groups = {name: [] for name in ALLOWED_MATERIALS}
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        material = obj.data.materials[0] if obj.data.materials else None
        mat_name = material_base_name(material)
        if mat_name in groups:
            groups[mat_name].append(obj)

    mats = ensure_materials()
    packed = []
    for mat_name, objects in sorted(groups.items()):
        if not objects:
            continue
        verts = []
        faces = []
        for obj in objects:
            offset = len(verts)
            verts.extend([tuple(v.co) for v in obj.data.vertices])
            faces.extend([tuple(offset + idx for idx in poly.vertices) for poly in obj.data.polygons])
        mesh = bpy.data.meshes.new(f"relationships_ext_{mat_name}_packed_mesh")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        packed_obj = bpy.data.objects.new(f"relationships_ext_{mat_name}_packed", mesh)
        bpy.context.collection.objects.link(packed_obj)
        packed_obj.data.materials.append(mats[mat_name])
        packed.append(packed_obj)

    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH" and obj not in packed]:
        bpy.data.objects.remove(obj, do_unlink=True)

    return packed


def export_relationships():
    remove_cameras_lights()
    for obj in list(bpy.data.objects):
        if obj.type == "EMPTY":
            bpy.data.objects.remove(obj, do_unlink=True)
    apply_mesh_world_transforms()
    normalize_material_slots()
    center_bottom_origin()
    pack_export_meshes_by_material()

    root = bpy.data.objects.new("relationships-ext", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.parent = root

    bpy.ops.wm.save_as_mainfile(filepath=PACKED_BLEND)
    mesh_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    for obj in mesh_objects:
        obj.select_set(True)
    if mesh_objects:
        bpy.context.view_layer.objects.active = mesh_objects[0]
    bpy.ops.export_scene.gltf(
        filepath=DRAFT_GLB,
        export_format="GLB",
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_yup=True,
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
    )
    shutil.copyfile(DRAFT_GLB, APPROVED_GLB)

    return {
        "draft_glb": DRAFT_GLB,
        "approved_glb": APPROVED_GLB,
        "packed_blend": PACKED_BLEND,
        "glb_bytes": os.path.getsize(APPROVED_GLB),
        "tris": scene_triangles(),
        "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "materials": sorted({material_base_name(mat) for mat in bpy.data.materials if mat.users}),
        "material_tris": material_triangles(),
        "material_percentages": material_percentages(scene_triangles(), material_triangles()),
        "bbox": bbox(),
    }


def validate_glb():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=APPROVED_GLB)
    materials = sorted(
        {
            material_base_name(mat)
            for obj in bpy.data.objects
            if obj.type == "MESH"
            for mat in obj.data.materials
            if mat
        }
    )
    non_identity = []
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        if any(abs(v) > 1e-5 for v in obj.location):
            non_identity.append(obj.name)
            continue
        if any(abs(v) > 1e-5 for v in obj.rotation_euler):
            non_identity.append(obj.name)
            continue
        if any(abs(v - 1.0) > 1e-5 for v in obj.scale):
            non_identity.append(obj.name)

    metrics = {
        "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "empty_objects": sum(1 for obj in bpy.data.objects if obj.type == "EMPTY"),
        "tris": scene_triangles(),
        "materials": materials,
        "rogue_materials": [mat for mat in materials if mat not in ALLOWED_MATERIALS],
        "uses_energy": "energy" in materials,
        "uses_holo": "holo" in materials,
        "cameras": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
        "lights": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
        "bbox": bbox(),
        "non_identity_mesh_transforms": non_identity,
        "glb_bytes": os.path.getsize(APPROVED_GLB),
    }
    with open(QA_IMPORT_FILE, "w") as f:
        json.dump(metrics, f, indent=2)
    return metrics


def create_cohesion_screenshot():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    setup_lighting()

    imports = [
        ("sia", os.path.join(ROOT, "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb"), (0, 0, 0)),
        ("fitness", os.path.join(ROOT, "modules/01-fitness/exterior/approved/fitness-ext.glb"), (25, 25, 0)),
        ("yoga", os.path.join(ROOT, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb"), (35, 10, 0)),
        ("finance", os.path.join(ROOT, "modules/03-finance/exterior/approved/finance-ext.glb"), (35, -5, 0)),
        ("knowledgebase", os.path.join(ROOT, "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"), (30, -20, 0)),
        ("chat", os.path.join(ROOT, "modules/05-chat-communication/exterior/approved/chat-ext.glb"), (18, -34, 0)),
        ("leaderboard", os.path.join(ROOT, "modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb"), (-8, -44, 0)),
        ("career", os.path.join(ROOT, "modules/08-career/exterior/approved/career-ext.glb"), (-28, -34, 0)),
        ("relationships", APPROVED_GLB, (7, -58, 0)),
    ]

    imported_labels = []
    for label, path, loc in imports:
        if not os.path.exists(path):
            continue
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=path)
        imported = [obj for obj in bpy.data.objects if obj not in before]
        for obj in imported:
            obj.location.x += loc[0]
            obj.location.y += loc[1]
            obj.location.z += loc[2]
            obj.name = f"{label}_{obj.name}"
        imported_labels.append(label)

    path = render_shot("s34_cohesion_all9.png", (78, -126, 74), (9, -20, 9), 22)
    return {"screenshot": path, "imported": imported_labels}


def build_session_34():
    if not os.path.exists(S33_BLEND):
        raise FileNotFoundError(S33_BLEND)

    print("=== Session 34: Relationships exterior detail, polish, export ===")
    bpy.ops.wm.open_mainfile(filepath=S33_BLEND)
    setup_lighting()
    mats = ensure_materials()
    normalize_material_slots()
    rebalance_existing_glow(mats)

    before_tris = scene_triangles()
    before_meshes = sum(1 for obj in bpy.data.objects if obj.type == "MESH")

    add_facade_detail(mats)
    add_water_edge_polish(mats)
    add_bridge_articulation(mats)
    add_dome_frames_and_glow(mats)
    add_garden_vegetation_detail(mats)
    add_portal_and_mist_polish(mats)
    normalize_material_slots()

    after_detail_tris = scene_triangles()
    if after_detail_tris > 15000:
        raise RuntimeError(f"Session 34 detail exceeded exterior budget before export: {after_detail_tris} tris")
    if after_detail_tris < 10000:
        raise RuntimeError(f"Session 34 detail under-used exterior budget before export: {after_detail_tris} tris")

    bpy.ops.wm.save_as_mainfile(filepath=S34_BLEND)

    screenshots = [
        render_shot("s34_front_elevation.png", (0, -24, 6.4), (0, -0.4, 3.0), 38),
        render_shot("s34_three_quarter.png", (18, -21, 9.6), (0.2, 0.0, 3.4), 40),
        render_shot("s34_distance_view.png", (32, -38, 17.2), (0.0, 0.0, 3.4), 44),
        render_dark_first(),
    ]

    mat_tris = material_triangles()
    metrics_before_export = {
        "session": 34,
        "module": "07-relationships",
        "blender_version": bpy.app.version_string,
        "source_blend": S33_BLEND,
        "blend": S34_BLEND,
        "before_mesh_objects": before_meshes,
        "before_tris": before_tris,
        "after_detail_mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "after_detail_tris": after_detail_tris,
        "detail_added_tris": after_detail_tris - before_tris,
        "category_metrics": category_metrics(),
        "material_tris": mat_tris,
        "material_percentages": material_percentages(after_detail_tris, mat_tris),
        "material_surface_area": material_surface_area(),
        "bbox": bbox(),
        "screenshots": screenshots,
        "objects": object_metrics(),
    }

    export_metrics = export_relationships()
    qa_import = validate_glb()
    cohesion = create_cohesion_screenshot()

    metrics = {
        **metrics_before_export,
        "export": export_metrics,
        "qa_import": qa_import,
        "cohesion": cohesion,
    }

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

    print("SESSION34_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_session_34()

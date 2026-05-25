"""
Balencia City v3 - Module #07 Relationships
Session 33: Exterior Major Forms

Low garden ecosystem: an anti-tower pavilion with a wide curved footprint,
cascading terraces, still-water moat, intimate bridges, glass roof domes,
welcoming portal arches, and a soft roof mist receiver.
"""

import importlib.util
import json
import math
import os
import sys

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/07-relationships")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
BLEND_FILE = os.path.join(DRAFTS, "relationships-s33-major-forms.blend")
METRICS_FILE = os.path.join(DRAFTS, "session33-metrics.json")

for path in (DRAFTS, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting", os.path.join(ROOT, "shared/lighting-rig.py"))
materials_mod = load_module("balencia_materials", os.path.join(ROOT, "shared/material-library.py"))


def assign(obj, mat):
    if obj.type == "MESH":
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return obj


def current_object():
    obj = getattr(bpy.context, "active_object", None)
    if obj is not None:
        return obj
    view_layer = getattr(bpy.context, "view_layer", None)
    if view_layer is not None and view_layer.objects.active is not None:
        return view_layer.objects.active
    selected = getattr(bpy.context, "selected_objects", [])
    if selected:
        return selected[-1]
    raise RuntimeError("Blender did not expose an active object after primitive creation")


def apply_transforms(obj, location=False, rotation=True, scale=True):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
    obj.select_set(False)
    return obj


def cleanup_slot_names():
    allowed = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
    for mat in bpy.data.materials:
        base = mat.name.split(".")[0]
        if base in allowed:
            mat.name = base


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_mesh(name, verts, faces, mat, shade=True):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    if shade:
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def box(name, loc, dims, mat, rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rot_z))
    obj = current_object()
    obj.name = name
    obj.scale = dims
    assign(obj, mat)
    apply_transforms(obj)
    return obj


def cylinder(name, loc, radius, depth, mat, vertices=24, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return obj


def cone(name, loc, radius1, radius2, depth, mat, vertices=18, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return obj


def torus(name, loc, major, minor, mat, seg=32, minor_seg=4):
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
    return obj


def cylinder_between(name, start, end, radius, mat, vertices=10):
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
    return obj


def ellipse_disc(name, rx, ry, z, mat, segments=72, center=(0.0, 0.0), phase=0.0):
    cx, cy = center
    verts = [(cx, cy, z)]
    for i in range(segments):
        a = phase + math.tau * i / segments
        verts.append((cx + math.cos(a) * rx, cy + math.sin(a) * ry, z))
    faces = []
    for i in range(segments):
        faces.append((0, 1 + i, 1 + ((i + 1) % segments)))
    return make_mesh(name, verts, faces, mat)


def ellipse_band(name, outer_rx, outer_ry, inner_rx, inner_ry, z0, z1, mat, segments=48, center=(0.0, 0.0)):
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
    return make_mesh(name, verts, faces, mat)


def tapered_ellipse_body(name, levels, mat, segments=48):
    verts = []
    for level in levels:
        z = level["z"]
        rx = level["rx"]
        ry = level["ry"]
        cx, cy = level.get("center", (0.0, 0.0))
        phase = level.get("phase", 0.0)
        for i in range(segments):
            a = phase + math.tau * i / segments
            organic = 1.0 + 0.035 * math.sin(3 * a + z * 0.7) + 0.02 * math.sin(5 * a)
            verts.append((cx + math.cos(a) * rx * organic, cy + math.sin(a) * ry * organic, z))

    faces = []
    for level_idx in range(len(levels) - 1):
        base = level_idx * segments
        nxt = (level_idx + 1) * segments
        for i in range(segments):
            faces.append((base + i, base + (i + 1) % segments, nxt + (i + 1) % segments, nxt + i))
    faces.append(tuple(reversed(range(segments))))
    top = (len(levels) - 1) * segments
    faces.append(tuple(range(top, top + segments)))
    return make_mesh(name, verts, faces, mat)


def ellipse_floor_bands(prefix, levels, floors, mat, segments=16):
    min_z = levels[0]["z"]
    max_z = levels[-1]["z"]
    for floor in range(1, floors + 1):
        z = min_z + (max_z - min_z) * floor / floors
        lower = max(i for i, item in enumerate(levels[:-1]) if item["z"] <= z)
        upper = min(lower + 1, len(levels) - 1)
        span = levels[upper]["z"] - levels[lower]["z"]
        t = 0 if span == 0 else (z - levels[lower]["z"]) / span
        rx = levels[lower]["rx"] + (levels[upper]["rx"] - levels[lower]["rx"]) * t
        ry = levels[lower]["ry"] + (levels[upper]["ry"] - levels[lower]["ry"]) * t
        ellipse_band(
            f"{prefix}_rose_floor_indicator_band_{floor:02d}",
            rx + 0.08,
            ry + 0.08,
            rx + 0.005,
            ry + 0.005,
            z - 0.015,
            z + 0.015,
            mat,
            segments=segments,
        )


def oriented_box_between(name, start_xy, end_xy, z, width, height, mat):
    sx, sy = start_xy
    ex, ey = end_xy
    dx = ex - sx
    dy = ey - sy
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    return box(name, ((sx + ex) * 0.5, (sy + ey) * 0.5, z), (length, width, height), mat, rot_z=angle)


def bridge(name, angle_deg, inner_r, outer_r, width, mats):
    angle = math.radians(angle_deg)
    direction = Vector((math.cos(angle), math.sin(angle), 0.0))
    normal = Vector((-math.sin(angle), math.cos(angle), 0.0))
    start = direction * inner_r
    end = direction * outer_r
    oriented_box_between(f"{name}_soft_arch_bridge_deck", (start.x, start.y), (end.x, end.y), 0.34, width, 0.14, mats["detail"])
    rail_offset = width * 0.54
    for side, sign in (("left", -1), ("right", 1)):
        points = []
        for i in range(8):
            t = i / 7
            p = start.lerp(end, t) + normal * rail_offset * sign
            z = 0.44 + math.sin(t * math.pi) * 0.34
            points.append((p.x, p.y, z))
        for i in range(len(points) - 1):
            cylinder_between(f"{name}_{side}_rose_arch_rail_{i:02d}", points[i], points[i + 1], 0.035, mats["accent"], vertices=6)
    box(f"{name}_arrival_landing_outer", (end.x, end.y, 0.22), (1.15, 0.82, 0.16), mats["base"], rot_z=angle)


def planter(name, loc, rx, ry, height, mats, rot_z=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1.0, depth=height, location=loc, rotation=(0, 0, rot_z))
    obj = current_object()
    obj.name = name + "_rounded_planter_bed"
    obj.scale = (rx, ry, 1.0)
    assign(obj, mats["detail"])
    apply_transforms(obj)
    torus(name + "_rose_planter_glow_rim", (loc[0], loc[1], loc[2] + height * 0.52), max(rx, ry) * 0.72, 0.025, mats["emissive"], seg=16, minor_seg=3)


def roof_dome(name, loc, scale, mats):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=8, radius=1.0, location=loc)
    obj = current_object()
    obj.name = name + "_transparent_roof_dome"
    obj.scale = scale
    assign(obj, mats["glass"])
    apply_transforms(obj)
    ellipse_disc(name + "_warm_gathering_glow_under_dome", scale[0] * 0.82, scale[1] * 0.82, loc[2] - scale[2] * 0.62, mats["emissive"], segments=18, center=(loc[0], loc[1]))


def portal_arch(name, center, width, height, depth, mats, angle_deg=0.0):
    cx, cy, base_z = center
    angle = math.radians(angle_deg)
    forward = Vector((math.cos(angle), math.sin(angle), 0.0))
    right = Vector((-math.sin(angle), math.cos(angle), 0.0))
    left_base = Vector((cx, cy, base_z)) - right * (width * 0.5)
    right_base = Vector((cx, cy, base_z)) + right * (width * 0.5)
    top_center = Vector((cx, cy, base_z + height * 0.58))
    cylinder_between(f"{name}_left_soft_portal_leg", left_base, left_base + Vector((0, 0, height * 0.58)), 0.10, mats["accent"], 6)
    cylinder_between(f"{name}_right_soft_portal_leg", right_base, right_base + Vector((0, 0, height * 0.58)), 0.10, mats["accent"], 6)
    arc_points = []
    for i in range(15):
        t = i / 14
        theta = math.pi - math.pi * t
        p = top_center + right * (math.cos(theta) * width * 0.5) + Vector((0, 0, math.sin(theta) * height * 0.42))
        arc_points.append((p.x, p.y, p.z))
    for i in range(len(arc_points) - 1):
        cylinder_between(f"{name}_curved_soft_portal_arch_{i:02d}", arc_points[i], arc_points[i + 1], 0.11, mats["accent"], 6)
    oriented_box_between(
        f"{name}_dark_recessed_entry_shadow",
        (cx - forward.x * depth * 0.5, cy - forward.y * depth * 0.5),
        (cx + forward.x * depth * 0.5, cy + forward.y * depth * 0.5),
        base_z + height * 0.38,
        width * 0.48,
        height * 0.52,
        mats["glass"],
    )


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
            eevee.bloom_threshold = 0.4
            eevee.bloom_intensity = 0.55
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.55


def render_shot(filename, camera_loc, target, lens=42):
    cam_data = bpy.data.cameras.new(filename.replace(".png", "_Camera"))
    cam = bpy.data.objects.new(filename.replace(".png", "_Camera"), cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    direction = Vector(target) - Vector(camera_loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.clip_start = 0.1
    cam.data.clip_end = 220
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = os.path.join(SCREENSHOTS, filename)
    bpy.ops.render.render(write_still=True)
    return bpy.context.scene.render.filepath


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
        mat_name = mat_name.split(".")[0]
        totals[mat_name] = totals.get(mat_name, 0) + get_tri_count(obj)
    return dict(sorted(totals.items()))


def category_for_object(name):
    if "bridge" in name or "landing" in name or "crossing" in name:
        return "Intimate water crossings and district bridge"
    if "moat" in name or "water" in name:
        return "Still water moat"
    if "dome" in name or "gathering_glow" in name:
        return "Glass roof gathering domes"
    if "terrace" in name or "planter" in name:
        return "Cascading gardens and rose planters"
    if "portal" in name or "entry" in name:
        return "Curved welcoming entrances"
    if "mist" in name or "energy" in name:
        return "Warm mist roof receiver"
    if "floor_indicator" in name:
        return "15-floor facade scale markers"
    return "Low curved pavilion body"


def object_metrics():
    rows = []
    for obj in sorted((o for o in bpy.data.objects if o.type == "MESH"), key=lambda o: o.name):
        rows.append(
            {
                "name": obj.name,
                "tris": get_tri_count(obj),
                "material": obj.data.materials[0].name.split(".")[0] if obj.data.materials else "NONE",
                "category": category_for_object(obj.name),
            }
        )
    return rows


def category_metrics(objects):
    totals = {}
    counts = {}
    for row in objects:
        category = row["category"]
        totals[category] = totals.get(category, 0) + row["tris"]
        counts[category] = counts.get(category, 0) + 1
    return [
        {"category": category, "objects": counts[category], "tris": totals[category]}
        for category in sorted(totals)
    ]


def world_bbox():
    coords = []
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            coords.append(obj.matrix_world @ Vector(corner))
    if not coords:
        return {}
    return {
        "min": [round(min(v[i] for v in coords), 4) for i in range(3)],
        "max": [round(max(v[i] for v in coords), 4) for i in range(3)],
    }


def build_scene():
    print("=== Session 33: Relationships exterior major forms ===")
    clear_scene()
    lighting.setup_viewport_lighting()
    setup_render()
    mats = materials_mod.create_materials("#F43F5E", include_energy=True, include_holo=False)
    cleanup_slot_names()
    print(f"Material slots: {sorted(mats.keys())}")

    # Still-water island setting: wide, horizontal, and visibly unlike the tower districts.
    ellipse_band("still_reflective_water_moat_surrounding_garden", 11.8, 7.35, 9.12, 5.35, 0.02, 0.07, mats["glass"], 40)
    ellipse_band("low_dark_island_plinth_inside_moat", 9.25, 5.55, 8.20, 4.75, 0.07, 0.22, mats["base"], 36)

    levels = [
        {"z": 0.22, "rx": 8.15, "ry": 4.72, "center": (0.0, 0.0), "phase": 0.10},
        {"z": 1.28, "rx": 7.78, "ry": 4.48, "center": (-0.14, 0.04), "phase": 0.12},
        {"z": 2.40, "rx": 6.75, "ry": 3.92, "center": (0.18, -0.02), "phase": 0.18},
        {"z": 3.62, "rx": 5.48, "ry": 3.08, "center": (-0.10, 0.10), "phase": 0.15},
        {"z": 4.78, "rx": 4.18, "ry": 2.42, "center": (0.12, -0.02), "phase": 0.22},
        {"z": 5.92, "rx": 3.10, "ry": 1.82, "center": (0.0, 0.05), "phase": 0.17},
    ]
    tapered_ellipse_body("low_curved_15_floor_relationships_pavilion_body", levels, mats["base"], 44)
    ellipse_floor_bands("low_curved_pavilion", levels, 15, mats["emissive"], 16)

    # Cascading terrace shelves: primary garden forms now, vegetation detail later.
    terrace_specs = [
        ("garden_terrace_cascade_lower", 8.55, 5.02, 7.75, 4.38, 1.34),
        ("garden_terrace_cascade_mid_low", 7.48, 4.34, 6.62, 3.72, 2.54),
        ("garden_terrace_cascade_mid_high", 6.05, 3.54, 5.18, 2.82, 3.78),
        ("garden_terrace_cascade_roof_base", 4.72, 2.78, 3.92, 2.12, 4.90),
        ("garden_terrace_cascade_top_garden", 3.54, 2.08, 2.62, 1.42, 6.02),
    ]
    for name, outer_rx, outer_ry, inner_rx, inner_ry, z in terrace_specs:
        ellipse_band(name + "_rounded_planter_shelf", outer_rx, outer_ry, inner_rx, inner_ry, z, z + 0.18, mats["detail"], 20)
        ellipse_band(name + "_warm_rose_lip", outer_rx + 0.04, outer_ry + 0.04, outer_rx - 0.18, outer_ry - 0.18, z + 0.19, z + 0.24, mats["accent"], 20)

    # Four intimate crossings over the moat and one longer adjacent-district bridge.
    for name, angle in [
        ("front_south", -90),
        ("east", 0),
        ("north_west", 140),
        ("south_west", -150),
    ]:
        bridge(f"{name}_intimate_water_crossing", angle, 8.75, 12.25, 0.78, mats)

    oriented_box_between("single_extended_connection_bridge_to_adjacent_district", (7.35, 3.55), (15.85, 6.85), 0.58, 0.92, 0.18, mats["detail"])
    cylinder_between("connection_bridge_left_warm_edge", (7.05, 4.00, 0.74), (15.55, 7.30, 0.74), 0.04, mats["accent"], 8)
    cylinder_between("connection_bridge_right_warm_edge", (7.65, 3.10, 0.74), (16.15, 6.40, 0.74), 0.04, mats["accent"], 8)

    # Low rose garden forms near entrances, not final vegetation.
    for idx, (x, y, rx, ry, rot) in enumerate(
        [
            (-2.55, -6.10, 0.88, 0.34, 8),
            (2.50, -6.02, 0.90, 0.35, -6),
            (-4.85, -4.62, 0.74, 0.30, 28),
            (4.72, -4.42, 0.76, 0.31, -22),
            (-7.10, 1.18, 0.78, 0.32, 80),
            (7.05, 1.28, 0.80, 0.32, -82),
        ]
    ):
        planter(f"entrance_rose_garden_{idx:02d}", (x, y, 0.36), rx, ry, 0.22, mats, math.radians(rot))

    # Transparent roof domes showing warm-lit gathering spaces.
    roof_dome("central_family_gathering", (0.0, -0.15, 6.26), (1.25, 0.92, 0.58), mats)
    roof_dome("west_intimate_gathering", (-2.85, 1.10, 5.22), (0.92, 0.70, 0.44), mats)
    roof_dome("east_intimate_gathering", (2.72, 0.92, 5.18), (0.88, 0.68, 0.42), mats)

    # Two welcoming portals, arched and soft rather than monumental.
    portal_arch("south_primary_welcoming", (0.0, -5.28, 0.34), 2.45, 1.92, 0.92, mats, angle_deg=90)
    portal_arch("west_secondary_welcoming", (-7.32, 0.28, 0.34), 1.75, 1.46, 0.82, mats, angle_deg=0)

    # Warm mist reception point: visible soft energy target, no hard pipeline.
    torus("roof_warm_mist_reception_diffuser_ring", (0.0, 0.06, 6.72), 0.78, 0.045, mats["energy"], seg=24, minor_seg=4)
    cone("roof_warm_mist_soft_receiver_core", (0.0, 0.06, 6.76), 0.42, 0.16, 0.42, mats["energy"], vertices=12)
    for idx, angle in enumerate([20, 92, 168, 236, 300]):
        a = math.radians(angle)
        start = (math.cos(a) * 0.25, math.sin(a) * 0.25 + 0.06, 6.94)
        mid = (math.cos(a) * 0.55, math.sin(a) * 0.55 + 0.06, 7.34)
        end = (math.cos(a) * 0.82, math.sin(a) * 0.82 + 0.06, 7.04)
        cylinder_between(f"warm_mist_rising_diffuse_wisp_{idx:02d}_a", start, mid, 0.025, mats["energy"], 6)
        cylinder_between(f"warm_mist_rising_diffuse_wisp_{idx:02d}_b", mid, end, 0.020, mats["energy"], 6)

    cleanup_slot_names()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    screenshots = [
        render_shot("s33_front_elevation.png", (0, -24, 6.0), (0, -0.4, 3.0), 38),
        render_shot("s33_three_quarter.png", (18, -21, 9.2), (0.2, 0.0, 3.3), 40),
        render_shot("s33_distance_view.png", (32, -38, 17.0), (0.0, 0.0, 3.4), 44),
    ]

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    objects = object_metrics()
    metrics = {
        "session": 33,
        "module": "07-relationships",
        "blend": BLEND_FILE,
        "screenshots": screenshots,
        "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "triangles": scene_triangles(),
        "materials": sorted([m.name for m in bpy.data.materials]),
        "material_tris": material_triangles(),
        "category_metrics": category_metrics(objects),
        "objects": objects,
        "lights": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
        "cameras": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
        "bbox": world_bbox(),
    }

    with open(METRICS_FILE, "w") as handle:
        json.dump(metrics, handle, indent=2)

    print("SESSION33_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_scene()

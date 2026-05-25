"""
Balencia City v3 - Module #08 Career
Session 29: Exterior Major Forms

Professional tower cluster with a dominant 40-floor main tower, three shorter
career-stage towers, glass skybridges, exterior elevator tubes, a crown
observation deck, and an SIA energy hardpoint.
"""

import importlib.util
import json
import math
import os
import sys

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/08-career")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
BLEND_FILE = os.path.join(DRAFTS, "career-s29-major-forms.blend")
METRICS_FILE = os.path.join(DRAFTS, "session29-metrics.json")

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
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for datablock_collection in (
        bpy.data.meshes,
        bpy.data.cameras,
        bpy.data.lights,
        bpy.data.materials,
    ):
        for datablock in list(datablock_collection):
            if datablock.users == 0:
                datablock_collection.remove(datablock)


def make_mesh(name, verts, faces, mat):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    return obj


def box(name, loc, dims, mat, rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rot_z))
    obj = current_object()
    obj.name = name
    obj.scale = dims
    assign(obj, mat)
    apply_transforms(obj)
    return obj


def cylinder(name, loc, radius, depth, mat, vertices=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return obj


def cone(name, loc, radius1, radius2, depth, mat, vertices=4, rot=(0, 0, 0)):
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


def torus(name, loc, major, minor, mat, seg=32, minor_seg=6):
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


def chamfered_points(width, depth, chamfer):
    w = width * 0.5
    d = depth * 0.5
    c = min(chamfer, w * 0.42, d * 0.42)
    return [
        (-w + c, -d),
        (w - c, -d),
        (w, -d + c),
        (w, d - c),
        (w - c, d),
        (-w + c, d),
        (-w, d - c),
        (-w, -d + c),
    ]


def chamfered_tower(name, center, floors, height, bottom_width, bottom_depth, top_width, top_depth, base_z, mat):
    cx, cy = center
    verts = []
    for level in range(floors + 1):
        t = level / floors
        width = bottom_width + (top_width - bottom_width) * t
        depth = bottom_depth + (top_depth - bottom_depth) * t
        chamfer = min(width, depth) * 0.12
        z = base_z + height * t
        for x, y in chamfered_points(width, depth, chamfer):
            verts.append((cx + x, cy + y, z))

    faces = []
    sides = 8
    for level in range(floors):
        base = level * sides
        nxt = (level + 1) * sides
        for side in range(sides):
            a = base + side
            b = base + (side + 1) % sides
            c = nxt + (side + 1) % sides
            d = nxt + side
            faces.append((a, b, c, d))

    faces.append(tuple(reversed(range(sides))))
    top_start = floors * sides
    faces.append(tuple(range(top_start, top_start + sides)))
    return make_mesh(name, verts, faces, mat)


def width_at_z(z, base_z, height, bottom_width, top_width):
    t = max(0.0, min(1.0, (z - base_z) / height))
    return bottom_width + (top_width - bottom_width) * t


def depth_at_z(z, base_z, height, bottom_depth, top_depth):
    t = max(0.0, min(1.0, (z - base_z) / height))
    return bottom_depth + (top_depth - bottom_depth) * t


def floor_light_bands(name, center, floors, height, bottom_width, bottom_depth, top_width, top_depth, base_z, mat):
    cx, cy = center
    verts = []
    faces = []
    half_band = 0.018
    inset = 0.12
    offset = 0.018

    def add_face(points):
        idx = len(verts)
        verts.extend(points)
        faces.append((idx, idx + 1, idx + 2, idx + 3))

    for floor in range(1, floors + 1):
        z = base_z + height * (floor / floors)
        width = width_at_z(z, base_z, height, bottom_width, top_width)
        depth = depth_at_z(z, base_z, height, bottom_depth, top_depth)
        x0 = cx - width * 0.5 + inset
        x1 = cx + width * 0.5 - inset
        y0 = cy - depth * 0.5 + inset
        y1 = cy + depth * 0.5 - inset
        z0 = z - half_band
        z1 = z + half_band

        add_face([(x0, cy - depth * 0.5 - offset, z0), (x1, cy - depth * 0.5 - offset, z0), (x1, cy - depth * 0.5 - offset, z1), (x0, cy - depth * 0.5 - offset, z1)])
        add_face([(x1, cy + depth * 0.5 + offset, z0), (x0, cy + depth * 0.5 + offset, z0), (x0, cy + depth * 0.5 + offset, z1), (x1, cy + depth * 0.5 + offset, z1)])
        add_face([(cx - width * 0.5 - offset, y1, z0), (cx - width * 0.5 - offset, y0, z0), (cx - width * 0.5 - offset, y0, z1), (cx - width * 0.5 - offset, y1, z1)])
        add_face([(cx + width * 0.5 + offset, y0, z0), (cx + width * 0.5 + offset, y1, z0), (cx + width * 0.5 + offset, y1, z1), (cx + width * 0.5 + offset, y0, z1)])

    return make_mesh(name, verts, faces, mat)


def vertical_ascent_edges(prefix, center, height, bottom_width, bottom_depth, top_width, top_depth, base_z, mat, radius=0.035):
    cx, cy = center
    for idx, (sx, sy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)]):
        start = (cx + sx * bottom_width * 0.5, cy + sy * bottom_depth * 0.5, base_z + 0.12)
        end = (cx + sx * top_width * 0.5, cy + sy * top_depth * 0.5, base_z + height + 0.42)
        cylinder_between(f"{prefix}_upward_corner_edge_{idx:02d}", start, end, radius, mat, vertices=8)


def roof_fins(prefix, center, top_z, width, depth, mat, height=0.9):
    cx, cy = center
    anchors = [
        (-width * 0.44, -depth * 0.44),
        (width * 0.44, -depth * 0.44),
        (width * 0.44, depth * 0.44),
        (-width * 0.44, depth * 0.44),
    ]
    for idx, (x, y) in enumerate(anchors):
        cone(
            f"{prefix}_upward_roof_fin_{idx:02d}",
            (cx + x, cy + y, top_z + height * 0.5),
            0.18,
            0.035,
            height,
            mat,
            vertices=4,
            rot=(0, 0, math.radians(45)),
        )


def oriented_box_between(name, start_xy, end_xy, z, width, height, mat):
    sx, sy = start_xy
    ex, ey = end_xy
    dx = ex - sx
    dy = ey - sy
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    return box(name, ((sx + ex) * 0.5, (sy + ey) * 0.5, z), (length, width, height), mat, rot_z=angle)


def skybridge(name, start_xy, end_xy, z, mats):
    oriented_box_between(f"{name}_glass_enclosure", start_xy, end_xy, z, 0.74, 0.58, mats["glass"])
    oriented_box_between(f"{name}_dark_floor_spine", start_xy, end_xy, z - 0.34, 0.66, 0.10, mats["detail"])
    oriented_box_between(f"{name}_blue_upper_edge", start_xy, end_xy, z + 0.34, 0.82, 0.045, mats["accent"])
    oriented_box_between(f"{name}_blue_lower_edge", start_xy, end_xy, z - 0.02, 0.82, 0.035, mats["emissive"])


def elevator_tube(prefix, center, height, base_z, mats, radius=0.25):
    cx, cy = center
    cylinder(f"{prefix}_transparent_elevator_tube", (cx, cy, base_z + height * 0.5), radius, height, mats["glass"], vertices=18)
    cylinder_between(f"{prefix}_left_blue_elevator_rail", (cx - radius * 0.62, cy, base_z + 0.12), (cx - radius * 0.62, cy, base_z + height - 0.12), 0.028, mats["accent"], vertices=8)
    cylinder_between(f"{prefix}_right_blue_elevator_rail", (cx + radius * 0.62, cy, base_z + 0.12), (cx + radius * 0.62, cy, base_z + height - 0.12), 0.028, mats["accent"], vertices=8)
    box(f"{prefix}_visible_ascending_cab_marker", (cx, cy, base_z + height * 0.62), (radius * 1.15, radius * 0.56, 0.34), mats["emissive"])


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
    cam.data.clip_end = 260
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
    if "energy" in name or "hardpoint" in name or "pipeline" in name:
        return "Crown SIA energy hardpoint"
    if "elevator" in name:
        return "Exterior elevator tubes"
    if "observation" in name:
        return "Executive observation deck"
    if "plaza" in name or "footprint" in name or "lobby" in name:
        return "Networking plaza, footprints, and lobby"
    if name.startswith("main_tower"):
        return "Main 40-floor tower and crown"
    if name.startswith("secondary_"):
        return "Secondary tower bodies"
    if "skybridge" in name:
        return "Glass skybridge system"
    return "Ascent edges, floor bands, and roof fins"


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
        cat = row["category"]
        totals[cat] = totals.get(cat, 0) + row["tris"]
        counts[cat] = counts.get(cat, 0) + 1
    return [
        {"category": cat, "objects": counts[cat], "tris": totals[cat]}
        for cat in sorted(totals)
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
    print("=== Session 29: Career exterior major forms ===")
    clear_scene()
    lighting.clear_lighting()
    lighting.setup_viewport_lighting()
    setup_render()
    mats = materials_mod.create_materials("#3B82F6", include_energy=True, include_holo=False)
    cleanup_slot_names()

    print(f"Material slots: {sorted(mats.keys())}")

    base_z = 0.24

    # Ground-level professional networking plaza.
    box("networking_plaza_dark_connector_slab", (0.0, 1.2, 0.06), (15.8, 12.4, 0.12), mats["base"])
    box("networking_plaza_front_arrival_step", (0.0, -5.45, 0.13), (6.0, 0.72, 0.16), mats["base"])
    box("networking_plaza_blue_central_path", (0.0, -2.75, 0.175), (0.18, 5.6, 0.045), mats["emissive"])
    box("networking_plaza_cross_connection_path", (0.0, 1.2, 0.18), (12.4, 0.16, 0.04), mats["accent"])

    tower_specs = {
        "main_tower": {
            "center": (0.0, 0.0),
            "floors": 40,
            "height": 16.0,
            "bottom": (2.85, 2.35),
            "top": (2.00, 1.68),
        },
        "secondary_west_tower": {
            "center": (-5.4, 1.45),
            "floors": 34,
            "height": 13.6,
            "bottom": (2.35, 2.02),
            "top": (1.76, 1.56),
        },
        "secondary_east_tower": {
            "center": (5.25, -1.35),
            "floors": 30,
            "height": 12.0,
            "bottom": (2.20, 1.92),
            "top": (1.62, 1.42),
        },
        "secondary_north_tower": {
            "center": (1.35, 5.25),
            "floors": 27,
            "height": 10.8,
            "bottom": (2.05, 1.82),
            "top": (1.50, 1.32),
        },
    }

    for prefix, spec in tower_specs.items():
        cx, cy = spec["center"]
        bottom_w, bottom_d = spec["bottom"]
        top_w, top_d = spec["top"]
        floors = spec["floors"]
        height = spec["height"]
        box(f"{prefix}_raised_footprint_plinth", (cx, cy, 0.20), (bottom_w + 0.55, bottom_d + 0.55, 0.28), mats["base"])
        chamfered_tower(
            f"{prefix}_tapered_{floors:02d}_floor_body",
            spec["center"],
            floors,
            height,
            bottom_w,
            bottom_d,
            top_w,
            top_d,
            base_z,
            mats["base"],
        )
        floor_light_bands(
            f"{prefix}_electric_blue_floor_joint_bands",
            spec["center"],
            floors,
            height,
            bottom_w,
            bottom_d,
            top_w,
            top_d,
            base_z,
            mats["emissive"],
        )
        vertical_ascent_edges(
            prefix,
            spec["center"],
            height,
            bottom_w,
            bottom_d,
            top_w,
            top_d,
            base_z,
            mats["accent"],
            radius=0.035 if prefix == "main_tower" else 0.028,
        )
        roof_fins(prefix, spec["center"], base_z + height, top_w, top_d, mats["accent"], height=0.95 if prefix == "main_tower" else 0.72)

    # Double-height entry lobby on the main tower.
    box("main_tower_double_height_entry_lobby_glass", (0.0, -1.205, 0.98), (1.78, 0.06, 1.38), mats["glass"])
    box("main_tower_entry_lobby_dark_header", (0.0, -1.245, 1.76), (1.92, 0.08, 0.16), mats["detail"])
    box("main_tower_entry_lobby_blue_threshold", (0.0, -1.31, 0.30), (2.08, 0.08, 0.10), mats["accent"])

    # Enclosed skybridges at visibly different career-stage heights.
    skybridge("skybridge_main_to_west_upper", (-1.02, 0.34), (-4.33, 1.12), 11.30, mats)
    skybridge("skybridge_main_to_east_mid", (1.02, -0.34), (4.18, -1.02), 8.45, mats)
    skybridge("skybridge_main_to_north_executive", (0.34, 1.05), (1.06, 4.27), 12.85, mats)

    # Transparent elevator tubes: one on main tower and one secondary tower.
    elevator_tube("main_tower_exterior", (1.62, -0.74), 15.0, base_z + 0.20, mats, radius=0.27)
    elevator_tube("secondary_west_exterior", (-6.72, 1.02), 12.2, base_z + 0.18, mats, radius=0.22)

    # Executive observation deck and crown hardpoint.
    box("main_tower_executive_observation_deck_glass_slab", (0.0, -1.55, 15.86), (2.42, 1.18, 0.16), mats["glass"])
    box("main_tower_observation_deck_front_rail", (0.0, -2.14, 16.24), (2.34, 0.06, 0.48), mats["detail"])
    box("main_tower_observation_deck_left_rail", (-1.22, -1.55, 16.24), (0.06, 1.14, 0.48), mats["detail"])
    box("main_tower_observation_deck_right_rail", (1.22, -1.55, 16.24), (0.06, 1.14, 0.48), mats["detail"])
    cylinder_between("main_tower_observation_deck_left_underbrace", (-0.94, -2.00, 15.78), (-0.52, -0.92, 14.85), 0.035, mats["detail"], vertices=8)
    cylinder_between("main_tower_observation_deck_right_underbrace", (0.94, -2.00, 15.78), (0.52, -0.92, 14.85), 0.035, mats["detail"], vertices=8)

    torus("main_tower_crown_energy_hardpoint_ring", (0.0, 0.0, 17.32), 0.42, 0.055, mats["energy"], seg=32, minor_seg=6)
    cylinder("main_tower_crown_pipeline_socket_core", (0.0, 0.0, 17.25), 0.18, 0.42, mats["energy"], vertices=12)
    cone("main_tower_crown_upward_pipeline_receiver", (0.0, 0.0, 17.72), 0.26, 0.055, 0.64, mats["energy"], vertices=8)

    cleanup_slot_names()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    screenshots = [
        render_shot("s29_front_elevation.png", (0, -25, 8.8), (0, 1.0, 8.3), 38),
        render_shot("s29_three_quarter.png", (17, -22, 12.0), (0.1, 1.0, 8.4), 40),
        render_shot("s29_distance_view.png", (33, -38, 21.0), (0.0, 1.0, 8.5), 44),
    ]

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    objects = object_metrics()
    metrics = {
        "session": 29,
        "module": "08-career",
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

    print("SESSION29_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_scene()

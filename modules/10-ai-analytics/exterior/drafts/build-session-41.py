"""
Balencia City v3 - Module #10 AI Analytics
Session 41: Exterior Major Forms

Data Cathedral: a tall pointed analytics building with living-wall data displays,
flying buttress data conduits, pointed holographic arch windows, a data-waterfall
entrance, observation platforms, and a hard-pipeline receiver for Phase 5.
"""

import importlib.util
import json
import math
import os
import sys

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Desktop/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/10-ai-analytics")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
BLEND_FILE = os.path.join(DRAFTS, "analytics-s41-major-forms.blend")
METRICS_FILE = os.path.join(DRAFTS, "session41-metrics.json")

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
    if hasattr(obj.data, "materials"):
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


def set_principled(mat, base_hex=None, emission_hex=None, emission_strength=None, alpha=None):
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf is None:
        return
    if base_hex:
        bsdf.inputs["Base Color"].default_value = materials_mod.hex_to_linear(base_hex)
    if emission_hex:
        bsdf.inputs["Emission Color"].default_value = materials_mod.hex_to_linear(emission_hex)
    if emission_strength is not None:
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    if alpha is not None:
        mat.blend_method = "BLEND"
        bsdf.inputs["Alpha"].default_value = alpha


def tune_analytics_materials(mats):
    set_principled(mats["accent"], base_hex="#123A39", emission_hex="#14B8A6", emission_strength=0.18)
    set_principled(mats["glass"], base_hex="#0B1A1D", emission_hex="#D1FAE5", emission_strength=0.05, alpha=0.82)
    set_principled(mats["emissive"], base_hex="#0D1F20", emission_hex="#14B8A6", emission_strength=0.18)
    set_principled(mats["holo"], base_hex="#082B2B", emission_hex="#14B8A6", emission_strength=0.24, alpha=0.46)
    set_principled(mats["energy"], base_hex="#231106", emission_hex="#FF5E00", emission_strength=0.14)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def fallback_lighting():
    world = bpy.context.scene.world or bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)
        bg.inputs["Strength"].default_value = 1.0

    sun = bpy.data.lights.new("Key_Light", "SUN")
    sun.color = (1.0, 0.894, 0.8)
    sun.energy = 0.8
    sun_obj = bpy.data.objects.new("Key_Light", sun)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

    rim = bpy.data.lights.new("Rim_Light", "SPOT")
    rim.color = (1.0, 0.369, 0.0)
    rim.energy = 200
    rim.spot_size = math.radians(45)
    rim.spot_blend = 0.9
    rim_obj = bpy.data.objects.new("Rim_Light", rim)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (10, 18, -14)
    direction = Vector((0, 0, 6)) - Vector(rim_obj.location)
    rim_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    fill = bpy.data.lights.new("Fill_Light", "AREA")
    fill.color = (0.102, 0.102, 0.251)
    fill.energy = 50
    fill.size = 20
    fill_obj = bpy.data.objects.new("Fill_Light", fill)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (5, 15, 10)


def setup_lighting():
    try:
        if hasattr(lighting, "clear_lighting"):
            lighting.clear_lighting()
        lighting.setup_viewport_lighting()
    except Exception as exc:
        print("Lighting rig fallback used: " + repr(exc))
        fallback_lighting()


def shade_smooth(obj):
    if obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def make_mesh(name, verts, faces, mat, smooth=False):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    if smooth:
        shade_smooth(obj)
    return obj


def box(name, loc, dims, mat, rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rot_z))
    obj = current_object()
    obj.name = name
    obj.scale = dims
    assign(obj, mat)
    apply_transforms(obj)
    return obj


def cylinder(name, loc, radius, depth, mat, vertices=16, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    shade_smooth(obj)
    apply_transforms(obj)
    return obj


def cone(name, loc, radius1, radius2, depth, mat, vertices=12, rot=(0.0, 0.0, 0.0)):
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
    shade_smooth(obj)
    apply_transforms(obj)
    return obj


def torus(name, loc, major, minor, mat, seg=32, minor_seg=6, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=seg,
        minor_segments=minor_seg,
        major_radius=major,
        minor_radius=minor,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    shade_smooth(obj)
    apply_transforms(obj)
    return obj


def cylinder_between(name, start, end, radius, mat, vertices=8):
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
    shade_smooth(obj)
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


def tapered_cathedral_body(name, floors, height, bottom_width, bottom_depth, top_width, top_depth, base_z, mat):
    verts = []
    sides = 8
    for level in range(floors + 1):
        t = level / floors
        width = bottom_width + (top_width - bottom_width) * t
        depth = bottom_depth + (top_depth - bottom_depth) * t
        chamfer = min(width, depth) * 0.10
        z = base_z + height * t
        for x, y in chamfered_points(width, depth, chamfer):
            verts.append((x, y, z))

    faces = []
    for level in range(floors):
        base = level * sides
        nxt = (level + 1) * sides
        for side in range(sides):
            faces.append((base + side, base + (side + 1) % sides, nxt + (side + 1) % sides, nxt + side))

    faces.append(tuple(reversed(range(sides))))
    top_start = floors * sides
    faces.append(tuple(range(top_start, top_start + sides)))
    return make_mesh(name, verts, faces, mat)


def gabled_roof(name, width, depth, base_z, ridge_z, mat):
    w = width * 0.5
    d = depth * 0.5
    verts = [
        (-w, -d, base_z),
        (w, -d, base_z),
        (w, d, base_z),
        (-w, d, base_z),
        (0, -d, ridge_z),
        (0, d, ridge_z),
    ]
    faces = [
        (0, 1, 4),
        (3, 5, 2),
        (0, 4, 5, 3),
        (1, 2, 5, 4),
        (0, 3, 2, 1),
    ]
    return make_mesh(name, verts, faces, mat)


def floor_bands(width_bottom, width_top, depth_bottom, depth_top, base_z, height, floors, mat):
    for floor in range(1, floors + 1):
        if floor % 2 == 0:
            z = base_z + height * (floor / floors)
            t = (z - base_z) / height
            width = width_bottom + (width_top - width_bottom) * t
            depth = depth_bottom + (depth_top - depth_bottom) * t
            band_h = 0.026
            box(f"living_facade_teal_floor_band_front_{floor:02d}", (0, -depth * 0.5 - 0.026, z), (width * 0.78, 0.035, band_h), mat)
            box(f"living_facade_teal_floor_band_back_{floor:02d}", (0, depth * 0.5 + 0.026, z), (width * 0.72, 0.035, band_h), mat)
            if floor % 4 == 0:
                box(f"living_facade_teal_floor_band_left_{floor:02d}", (-width * 0.5 - 0.026, 0, z), (0.035, depth * 0.62, band_h), mat)
                box(f"living_facade_teal_floor_band_right_{floor:02d}", (width * 0.5 + 0.026, 0, z), (0.035, depth * 0.62, band_h), mat)


def data_streams(mat):
    front_y = -2.82
    back_y = 2.82
    for idx, x in enumerate([-1.55, -0.78, 0.0, 0.78, 1.55]):
        zc = 6.35 + 0.28 * math.sin(idx)
        box(f"vertical_teal_data_stream_front_{idx:02d}", (x, front_y, zc), (0.045, 0.04, 7.4), mat)
    for idx, x in enumerate([-1.20, 0.0, 1.20]):
        box(f"vertical_teal_data_stream_back_{idx:02d}", (x, back_y, 6.25), (0.038, 0.04, 6.6), mat)
    for side, x in [("left", -2.08), ("right", 2.08)]:
        for idx, y in enumerate([-1.65, -0.55, 0.55, 1.65]):
            box(f"vertical_teal_data_stream_{side}_{idx:02d}", (x, y, 6.1), (0.04, 0.036, 6.2), mat)


def dashboard_panel_front(name, center_x, y, center_z, width, height, mats):
    box(name + "_dark_display_slab", (center_x, y, center_z), (width, 0.035, height), mats["glass"])
    bar_count = 5
    for idx in range(bar_count):
        x = center_x - width * 0.36 + idx * (width * 0.18)
        bar_h = height * (0.20 + 0.10 * ((idx * 3) % 5))
        z = center_z - height * 0.34 + bar_h * 0.5
        box(f"{name}_teal_chart_bar_{idx:02d}", (x, y - 0.026, z), (width * 0.055, 0.028, bar_h), mats["emissive"])
    box(name + "_dashboard_trend_line_low", (center_x, y - 0.029, center_z + height * 0.22), (width * 0.72, 0.025, 0.026), mats["emissive"], rot_z=math.radians(8))
    box(name + "_dashboard_trend_line_high", (center_x, y - 0.030, center_z + height * 0.34), (width * 0.42, 0.025, 0.022), mats["accent"], rot_z=math.radians(-10))


def dashboard_panel_side(name, x, center_y, center_z, depth, height, mats):
    box(name + "_dark_display_slab", (x, center_y, center_z), (0.035, depth, height), mats["glass"])
    for idx in range(4):
        y = center_y - depth * 0.34 + idx * (depth * 0.22)
        bar_h = height * (0.18 + 0.12 * ((idx + 1) % 4))
        z = center_z - height * 0.32 + bar_h * 0.5
        box(f"{name}_side_teal_chart_bar_{idx:02d}", (x, y, z), (0.028, depth * 0.055, bar_h), mats["emissive"])


def arch_panel_front(name, cx, y, base_z, width, height, mats):
    w = width * 0.5
    shoulder = base_z + height * 0.64
    peak = base_z + height
    verts = [
        (cx - w, y, base_z),
        (cx + w, y, base_z),
        (cx + w, y, shoulder),
        (cx, y, peak),
        (cx - w, y, shoulder),
    ]
    make_mesh(name + "_holographic_pointed_arch_window", verts, [(0, 1, 2, 3, 4)], mats["holo"])
    box(name + "_left_dark_arch_jamb", (cx - w - 0.045, y - 0.018, base_z + height * 0.34), (0.055, 0.035, height * 0.68), mats["detail"])
    box(name + "_right_dark_arch_jamb", (cx + w + 0.045, y - 0.018, base_z + height * 0.34), (0.055, 0.035, height * 0.68), mats["detail"])
    cylinder_between(name + "_left_pointed_arch_frame", (cx - w, y - 0.018, shoulder), (cx, y - 0.018, peak), 0.028, mats["detail"], vertices=6)
    cylinder_between(name + "_right_pointed_arch_frame", (cx + w, y - 0.018, shoulder), (cx, y - 0.018, peak), 0.028, mats["detail"], vertices=6)


def arch_panel_side(name, x, cy, base_z, depth, height, mats):
    d = depth * 0.5
    shoulder = base_z + height * 0.64
    peak = base_z + height
    verts = [
        (x, cy - d, base_z),
        (x, cy + d, base_z),
        (x, cy + d, shoulder),
        (x, cy, peak),
        (x, cy - d, shoulder),
    ]
    make_mesh(name + "_side_holographic_pointed_arch_window", verts, [(0, 1, 2, 3, 4)], mats["holo"])
    cylinder_between(name + "_side_arch_lower_jamb_a", (x, cy - d, base_z), (x, cy - d, shoulder), 0.026, mats["detail"], vertices=6)
    cylinder_between(name + "_side_arch_lower_jamb_b", (x, cy + d, base_z), (x, cy + d, shoulder), 0.026, mats["detail"], vertices=6)
    cylinder_between(name + "_side_arch_peak_frame_a", (x, cy - d, shoulder), (x, cy, peak), 0.026, mats["detail"], vertices=6)
    cylinder_between(name + "_side_arch_peak_frame_b", (x, cy + d, shoulder), (x, cy, peak), 0.026, mats["detail"], vertices=6)


def buttress_arc(prefix, side_sign, y, lower_z, upper_z, mats, index):
    anchor_x = side_sign * 5.1
    wall_x = side_sign * 2.05
    anchor = Vector((anchor_x, y, 0.45))
    wall = Vector((wall_x, y, upper_z))
    control = Vector((side_sign * 4.25, y, upper_z + 1.35))
    points = []
    steps = 6
    for step in range(steps + 1):
        t = step / steps
        p = (1 - t) * (1 - t) * anchor + 2 * (1 - t) * t * control + t * t * wall
        points.append(p)

    box(f"{prefix}_ground_anchor_block_{index:02d}", (anchor_x, y, 0.22), (0.72, 0.72, 0.44), mats["base"])
    cylinder_between(f"{prefix}_data_buttress_foundation_pin_{index:02d}", (anchor_x, y, 0.44), (anchor_x, y, lower_z), 0.11, mats["detail"], vertices=10)
    for seg in range(len(points) - 1):
        cylinder_between(f"{prefix}_flying_buttress_data_conduit_segment_{index:02d}_{seg:02d}", points[seg], points[seg + 1], 0.105, mats["detail"], vertices=10)
        if seg in (1, 3, 5):
            a = points[seg] + Vector((0, 0, 0.10))
            b = points[seg + 1] + Vector((0, 0, 0.10))
            cylinder_between(f"{prefix}_teal_buttress_edge_stream_{index:02d}_{seg:02d}", a, b, 0.026, mats["emissive"], vertices=6)

    mid = points[3]
    platform_x = mid.x + side_sign * 0.35
    box(f"{prefix}_observation_platform_flat_extension_{index:02d}", (platform_x, y, mid.z - 0.08), (1.05, 0.82, 0.12), mats["detail"])
    box(f"{prefix}_observation_platform_teal_edge_{index:02d}", (platform_x + side_sign * 0.50, y, mid.z + 0.03), (0.035, 0.74, 0.06), mats["emissive"])


def entrance_waterfall(mats):
    box("front_entry_dark_recessed_doorway", (0, -2.91, 1.34), (0.96, 0.08, 1.72), mats["detail"])
    for side, x in [("left", -0.70), ("right", 0.70)]:
        box(f"data_waterfall_{side}_main_vertical_cascade", (x, -2.98, 1.62), (0.075, 0.045, 2.55), mats["emissive"])
        for idx in range(5):
            z = 0.48 + idx * 0.48
            box(f"data_waterfall_{side}_falling_teal_block_{idx:02d}", (x + 0.07 * math.sin(idx), -3.02, z), (0.16, 0.035, 0.08), mats["emissive"])
    box("front_entry_cathedral_threshold_slab", (0, -3.18, 0.18), (1.92, 0.72, 0.16), mats["base"])


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
            eevee.bloom_threshold = 0.35
            eevee.bloom_intensity = 0.65
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
    if "buttress" in name or "anchor" in name:
        return "Flying buttress data conduits and anchors"
    if "spire" in name or "beacon" in name or "pipeline_receiver" in name or "hard_socket" in name:
        return "Central spire, beacon, and SIA hardpoint"
    if "arch" in name or "window" in name:
        return "Pointed holographic data windows"
    if "waterfall" in name or "entry" in name or "doorway" in name:
        return "Data-waterfall entrance"
    if "dashboard" in name or "data_stream" in name or "floor_band" in name or "chart" in name:
        return "Living facade data displays"
    if "platform" in name:
        return "Buttress observation platforms"
    if "foundation" in name or "plaza" in name or "body" in name or "roof" in name or "aisle" in name or "nave" in name:
        return "Cathedral body and foundation"
    return "Analytics cathedral major forms"


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
    print("=== Session 41: AI Analytics exterior major forms ===")
    clear_scene()
    setup_lighting()
    setup_render()
    mats = materials_mod.create_materials("#14B8A6", include_energy=True, include_holo=True)
    cleanup_slot_names()
    tune_analytics_materials(mats)
    print(f"Material slots: {sorted(mats.keys())}")

    base_z = 0.24
    body_height = 12.0
    body_width_bottom = 4.2
    body_depth_bottom = 5.7
    body_width_top = 2.75
    body_depth_top = 4.05

    box("cathedral_foundation_dark_plaza_slab", (0.0, 0.0, 0.06), (10.7, 8.1, 0.12), mats["base"])
    box("front_analytics_arrival_axis_dark_stone", (0.0, -4.62, 0.14), (2.5, 1.52, 0.12), mats["base"])
    tapered_cathedral_body(
        "thirty_floor_data_cathedral_main_body",
        30,
        body_height,
        body_width_bottom,
        body_depth_bottom,
        body_width_top,
        body_depth_top,
        base_z,
        mats["base"],
    )
    box("left_lower_cathedral_side_aisle_mass", (-2.82, 0, 3.52), (1.06, 5.20, 6.56), mats["base"])
    box("right_lower_cathedral_side_aisle_mass", (2.82, 0, 3.52), (1.06, 5.20, 6.56), mats["base"])
    gabled_roof("pointed_cathedral_nave_roof_dark_data_shed", 3.15, 4.85, base_z + body_height, base_z + body_height + 1.35, mats["detail"])
    gabled_roof("left_aisle_small_pointed_roof", 1.22, 5.30, 6.78, 7.45, mats["detail"])
    gabled_roof("right_aisle_small_pointed_roof", 1.22, 5.30, 6.78, 7.45, mats["detail"])

    floor_bands(body_width_bottom, body_width_top, body_depth_bottom, body_depth_top, base_z, body_height, 30, mats["emissive"])
    data_streams(mats["emissive"])

    cone("central_spire_dark_pinnacle_taper", (0.0, 0.0, 14.82), 0.58, 0.06, 3.12, mats["detail"], vertices=12)
    cylinder("central_spire_teal_data_beacon_core", (0.0, 0.0, 16.52), 0.13, 0.36, mats["emissive"], vertices=12)
    torus("central_spire_teal_beacon_ring", (0.0, 0.0, 16.36), 0.34, 0.026, mats["emissive"], seg=28, minor_seg=4)
    torus("rear_roof_orange_sia_pipeline_receiver_hard_socket", (0.0, 2.08, 12.98), 0.42, 0.045, mats["energy"], seg=28, minor_seg=5, rot=(math.radians(90), 0, 0))
    cylinder("rear_roof_orange_pipeline_receiver_core", (0.0, 2.22, 12.98), 0.18, 0.36, mats["energy"], vertices=12, rot=(math.radians(90), 0, 0))

    for idx, y in enumerate([-2.15, 0.0, 2.15]):
        buttress_arc("left", -1, y, 1.15, 6.1 + idx * 0.74, mats, idx)
        buttress_arc("right", 1, y, 1.15, 6.1 + idx * 0.74, mats, idx)

    arch_panel_front("front_lower_left", -1.22, -2.90, 2.65, 0.74, 2.55, mats)
    arch_panel_front("front_lower_center", 0.0, -2.93, 3.05, 0.92, 3.05, mats)
    arch_panel_front("front_lower_right", 1.22, -2.90, 2.65, 0.74, 2.55, mats)
    arch_panel_front("front_upper_left", -0.66, -2.62, 7.52, 0.62, 2.05, mats)
    arch_panel_front("front_upper_right", 0.66, -2.62, 7.52, 0.62, 2.05, mats)
    arch_panel_side("left_side_arch_window_forward", -2.10, -1.45, 4.05, 0.86, 2.25, mats)
    arch_panel_side("left_side_arch_window_rear", -2.10, 1.45, 4.05, 0.86, 2.25, mats)
    arch_panel_side("right_side_arch_window_forward", 2.10, -1.45, 4.05, 0.86, 2.25, mats)
    arch_panel_side("right_side_arch_window_rear", 2.10, 1.45, 4.05, 0.86, 2.25, mats)

    dashboard_panel_front("front_left_broad_dashboard_data_wall", -1.22, -2.95, 7.02, 0.86, 1.18, mats)
    dashboard_panel_front("front_right_broad_dashboard_data_wall", 1.22, -2.95, 7.02, 0.86, 1.18, mats)
    dashboard_panel_front("front_upper_nave_metric_dashboard", 0.0, -2.62, 10.12, 1.30, 1.05, mats)
    dashboard_panel_side("left_side_buttress_metric_dashboard", -3.38, -0.05, 5.98, 1.50, 1.16, mats)
    dashboard_panel_side("right_side_buttress_metric_dashboard", 3.38, -0.05, 5.98, 1.50, 1.16, mats)

    entrance_waterfall(mats)

    cleanup_slot_names()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    screenshots = [
        render_shot("s41_front_elevation.png", (0, -27, 9.0), (0, -0.2, 8.2), 38),
        render_shot("s41_three_quarter.png", (18, -24, 13.2), (0.0, 0.0, 8.4), 40),
        render_shot("s41_distance_view.png", (35, -42, 21.0), (0.0, 0.0, 8.3), 44),
    ]

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    objects = object_metrics()
    metrics = {
        "session": 41,
        "module": "10-ai-analytics",
        "blender_version": bpy.app.version_string,
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

    print("SESSION41_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_scene()

if os.environ.get("BALENCIA_QUIT_AFTER_RUN", "0") == "1":
    bpy.ops.wm.quit_blender()

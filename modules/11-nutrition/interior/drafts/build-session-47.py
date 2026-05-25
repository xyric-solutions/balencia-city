"""
Balencia City v3 - Module #11 Nutrition
Session 47: Interior - Nourishment Hall

Fresh Nutrition interior scene for the approved vertical farm exterior.
Builds the living market focal shelves, communal dining tables, nutrition
breakdowns, AI scan station, adaptive calorie wall, chef prep zones, hydration
stations, runtime empties, screenshots, metrics, GLB export, import QA, and
approved promotion when gates pass.
"""

import importlib.util
import json
import math
import os
import shutil
import sys
from mathutils import Matrix, Vector

import bpy


ROOT = "/Users/hamza/Desktop/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/11-nutrition")
DRAFTS = os.path.join(MODULE, "interior/drafts")
APPROVED = os.path.join(MODULE, "interior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
SHARED = os.path.join(ROOT, "shared")

BLEND_FILE = os.path.join(DRAFTS, "nutrition-int-session47.blend")
DRAFT_GLB = os.path.join(DRAFTS, "nutrition-int-draft-s47.glb")
APPROVED_GLB = os.path.join(APPROVED, "nutrition-int.glb")
METRICS_FILE = os.path.join(DRAFTS, "session47-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS, "session47-qa-import.json")

DISTRICT_HEX = "#D97706"
VALID_SLOTS = {"base", "accent", "glass", "detail", "emissive", "holo"}
INT_TRI_MIN = 5000
INT_TRI_MAX = 10000
INT_SIZE_MIN = 60 * 1024
INT_SIZE_MAX = 200 * 1024
REQUIRED_EMPTIES = {"light_0", "light_1", "light_2", "camera_target"}

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s47", os.path.join(SHARED, "lighting-rig.py"))
materials_mod = load_module("balencia_materials_s47", os.path.join(SHARED, "material-library.py"))
interior_lighting = load_module("balencia_interior_lighting_s47", os.path.join(SHARED, "interior-lighting-rig.py"))

MATS = {}
created_categories = {}


def register(obj, category):
    if obj is not None:
        created_categories[obj.name] = category
    return obj


def material_base_name(material):
    return material.name.split(".")[0] if material else "none"


def current_object():
    obj = getattr(bpy.context.view_layer.objects, "active", None)
    if obj is not None:
        return obj
    selected = getattr(bpy.context, "selected_objects", [])
    if selected:
        return selected[-1]
    raise RuntimeError("No active object after primitive creation")


def set_principled(mat, base_hex=None, emission_hex=None, emission_strength=None, alpha=None):
    if mat is None or not mat.use_nodes:
        return
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


def tune_nutrition_materials():
    set_principled(MATS["base"], base_hex="#1A1712", emission_hex="#0B0703", emission_strength=0.012)
    set_principled(MATS["detail"], base_hex="#11100D", emission_hex="#120A02", emission_strength=0.010)
    set_principled(MATS["accent"], base_hex="#17311F", emission_hex="#34A853", emission_strength=0.150)
    set_principled(MATS["glass"], base_hex="#17110A", emission_hex="#FBBF24", emission_strength=0.080, alpha=0.72)
    set_principled(MATS["emissive"], base_hex="#261104", emission_hex=DISTRICT_HEX, emission_strength=0.260)
    set_principled(MATS["holo"], base_hex="#140B24", emission_hex="#F59E0B", emission_strength=0.220, alpha=0.46)


def assign(obj, slot):
    if obj.type == "MESH":
        obj.data.materials.clear()
        obj.data.materials.append(MATS[slot])
    return obj


def shade_smooth(obj):
    if obj is not None and obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def apply_transforms(obj):
    if obj is None or obj.type != "MESH":
        return obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    return obj


def box(name, loc, dims, slot, category, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    obj.scale = dims
    assign(obj, slot)
    apply_transforms(obj)
    return register(obj, category)


def cylinder(name, loc, radius, depth, slot, category, vertices=16, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    assign(obj, slot)
    shade_smooth(obj)
    apply_transforms(obj)
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, slot, category, vertices=12, rot=(0.0, 0.0, 0.0)):
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
    assign(obj, slot)
    shade_smooth(obj)
    apply_transforms(obj)
    return register(obj, category)


def sphere(name, loc, radius, slot, category, segments=8, rings=4, scale=(1.0, 1.0, 1.0)):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        radius=radius,
        location=loc,
    )
    obj = current_object()
    obj.name = name
    obj.scale = scale
    assign(obj, slot)
    shade_smooth(obj)
    apply_transforms(obj)
    return register(obj, category)


def torus(name, loc, major, minor, slot, category, seg=14, minor_seg=4, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)):
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
    obj.scale = scale
    assign(obj, slot)
    shade_smooth(obj)
    apply_transforms(obj)
    return register(obj, category)


def cylinder_between(name, start, end, radius, slot, category, vertices=6):
    start_v = Vector(start)
    end_v = Vector(end)
    direction = end_v - start_v
    length = direction.length
    if length < 0.001:
        return None
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=(start_v + end_v) * 0.5)
    obj = current_object()
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign(obj, slot)
    shade_smooth(obj)
    apply_transforms(obj)
    return register(obj, category)


def create_empty(name, loc, size=0.32):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=loc)
    obj = current_object()
    obj.name = name
    obj.empty_display_size = size
    return obj


def point_camera(cam, target):
    direction = Vector(target) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_camera(name, loc, target, lens=34):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.1
    data.clip_end = 120
    cam = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    point_camera(cam, target)
    return cam


def render_still(camera, path, resolution=(1600, 1000)):
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]
    bpy.context.scene.render.resolution_percentage = 100
    bpy.ops.render.render(write_still=True)
    return path


def render_still_with_hidden(camera, path, names):
    hidden = {}
    for obj in bpy.data.objects:
        if obj.name in names:
            hidden[obj.name] = (obj.hide_render, obj.hide_viewport)
            obj.hide_render = True
            obj.hide_viewport = True
    try:
        return render_still(camera, path)
    finally:
        for obj in bpy.data.objects:
            if obj.name in hidden:
                obj.hide_render, obj.hide_viewport = hidden[obj.name]


def set_all_emission_strength(value):
    previous = {}
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is None or "Emission Strength" not in bsdf.inputs:
            continue
        previous[mat.name] = bsdf.inputs["Emission Strength"].default_value
        bsdf.inputs["Emission Strength"].default_value = value
    return previous


def restore_emission_strength(previous):
    for mat_name, value in previous.items():
        mat = bpy.data.materials.get(mat_name)
        if not mat or not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf and "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = value


def build_room_shell():
    box("nutrition_hall_floor_plate", (0.0, 0.0, 0.05), (8.2, 13.2, 0.10), "base", "room_shell")
    box("nutrition_hall_center_aisle_inlay", (0.0, -0.8, 0.13), (1.35, 9.2, 0.035), "detail", "room_shell")
    box("nutrition_hall_market_end_wall", (0.0, 6.52, 2.45), (8.2, 0.18, 4.9), "base", "room_shell")
    box("nutrition_hall_left_wall", (-4.18, 0.0, 2.45), (0.18, 13.0, 4.9), "base", "room_shell")
    box("nutrition_hall_right_wall", (4.18, 0.0, 2.45), (0.18, 13.0, 4.9), "base", "room_shell")
    box("nutrition_hall_open_entry_left_pier", (-3.35, -6.52, 2.30), (0.72, 0.20, 4.6), "base", "room_shell")
    box("nutrition_hall_open_entry_right_pier", (3.35, -6.52, 2.30), (0.72, 0.20, 4.6), "base", "room_shell")
    box("nutrition_hall_open_entry_lintel", (0.0, -6.52, 4.58), (8.2, 0.20, 0.34), "detail", "room_shell")
    box("nutrition_hall_ceiling_left", (-2.12, 0.0, 4.92), (3.65, 13.1, 0.14), "base", "room_shell", rot=(0.0, math.radians(-4), 0.0))
    box("nutrition_hall_ceiling_right", (2.12, 0.0, 4.92), (3.65, 13.1, 0.14), "base", "room_shell", rot=(0.0, math.radians(4), 0.0))
    box("nutrition_hall_ceiling_center_glow", (0.0, -0.2, 4.84), (0.34, 11.6, 0.035), "emissive", "room_shell")

    for idx, y in enumerate([-5.35, -3.75, -2.15, -0.55, 1.05, 2.65, 4.25, 5.85]):
        box(f"nutrition_hall_floor_amber_band_{idx}", (0.0, y, 0.18), (7.6, 0.035, 0.035), "emissive", "room_shell")
        cylinder_between(f"nutrition_hall_left_arch_rib_{idx}", (-4.03, y, 0.40), (-2.80, y, 4.78), 0.025, "detail", "room_shell")
        cylinder_between(f"nutrition_hall_right_arch_rib_{idx}", (4.03, y, 0.40), (2.80, y, 4.78), 0.025, "detail", "room_shell")


def build_living_market():
    shelf_levels = [0.82, 1.42, 2.02, 2.62, 3.22]
    x_positions = [-2.75, -1.38, 0.0, 1.38, 2.75]
    y_positions = [3.50, 4.25, 5.00]

    box("living_market_back_glass_wall", (0.0, 6.36, 2.35), (6.55, 0.055, 3.15), "glass", "living_market")
    box("living_market_lower_planter_basin", (0.0, 4.28, 0.42), (6.35, 2.80, 0.34), "detail", "living_market")
    box("living_market_basin_amber_underlight", (0.0, 4.28, 0.63), (6.18, 2.58, 0.035), "emissive", "living_market")

    for level_idx, z in enumerate(shelf_levels):
        width = 6.25 - level_idx * 0.22
        depth = 2.78 - level_idx * 0.16
        box(f"living_market_glass_shelf_level_{level_idx}", (0.0, 4.28, z), (width, depth, 0.070), "glass", "living_market")
        box(f"living_market_amber_shelf_light_{level_idx}", (0.0, 2.92 + level_idx * 0.08, z + 0.08), (width * 0.96, 0.040, 0.045), "emissive", "living_market")
        for side_x in (-width / 2, width / 2):
            cylinder_between(
                f"living_market_vertical_side_frame_{level_idx}_{side_x:.1f}",
                (side_x, 3.02, 0.68),
                (side_x, 5.48, z + 0.18),
                0.024,
                "detail",
                "living_market",
            )

    produce_index = 0
    for level_idx, z in enumerate(shelf_levels[1:]):
        for xi, x in enumerate(x_positions):
            y = y_positions[(xi + level_idx) % len(y_positions)]
            slot = "accent" if (xi + level_idx) % 2 else "emissive"
            sphere(
                f"living_market_produce_cluster_{produce_index:02d}",
                (x, y, z + 0.13),
                0.145 + 0.015 * (xi % 3),
                slot,
                "living_market",
                segments=8,
                rings=4,
                scale=(1.10, 0.88, 0.72),
            )
            cone(
                f"living_market_leaf_bundle_{produce_index:02d}",
                (x + 0.10, y - 0.08, z + 0.27),
                0.105,
                0.015,
                0.24,
                "accent",
                "living_market",
                vertices=7,
                rot=(math.radians(86), 0.0, math.radians(25 + xi * 11)),
            )
            box(
                f"living_market_holo_tag_{produce_index:02d}",
                (x + 0.30, y - 0.35, z + 0.28),
                (0.22, 0.025, 0.105),
                "holo",
                "living_market",
                rot=(0.0, 0.0, math.radians(5 * (xi - 2))),
            )
            if produce_index % 4 == 0:
                cylinder(
                    f"living_market_spotlight_cone_{produce_index:02d}",
                    (x, y - 0.12, z + 0.48),
                    0.065,
                    0.18,
                    "emissive",
                    "living_market",
                    vertices=10,
                    rot=(math.radians(90), 0.0, 0.0),
                )
            produce_index += 1

    for i, x in enumerate([-2.9, -1.45, 0.0, 1.45, 2.9]):
        cylinder_between(f"living_market_hanging_irrigation_line_{i}", (x, 3.04, 3.78), (x, 5.62, 3.55), 0.012, "detail", "living_market")
        sphere(f"living_market_mist_node_{i}", (x, 4.22, 3.58), 0.055, "holo", "living_market", segments=7, rings=3)


def build_communal_tables():
    table_specs = [(-1.05, -1.85), (1.05, -1.85), (0.0, 1.10)]
    for table_idx, (x, y) in enumerate(table_specs):
        length = 4.65 if table_idx < 2 else 3.70
        width = 0.62 if table_idx < 2 else 0.78
        box(f"communal_table_{table_idx}_slab", (x, y, 0.78), (width, length, 0.13), "base", "communal_tables")
        box(f"communal_table_{table_idx}_amber_edge_left", (x - width / 2 - 0.025, y, 0.88), (0.025, length, 0.035), "emissive", "communal_tables")
        box(f"communal_table_{table_idx}_amber_edge_right", (x + width / 2 + 0.025, y, 0.88), (0.025, length, 0.035), "emissive", "communal_tables")
        for leg_y in [y - length / 2 + 0.35, y + length / 2 - 0.35]:
            for leg_x in [x - width / 2 + 0.12, x + width / 2 - 0.12]:
                cylinder(f"communal_table_{table_idx}_leg_{leg_x:.1f}_{leg_y:.1f}", (leg_x, leg_y, 0.39), 0.030, 0.72, "detail", "communal_tables", vertices=8)
        for side, offset in [("left", -0.62), ("right", 0.62)]:
            box(f"communal_table_{table_idx}_bench_{side}", (x + offset, y, 0.47), (0.26, length * 0.88, 0.11), "detail", "communal_tables")

        for display_idx, dy in enumerate([-length * 0.32, -length * 0.08, length * 0.16, length * 0.38]):
            px = x + (0.55 if display_idx % 2 else -0.55)
            py = y + dy
            torus(
                f"nutrition_macro_ring_t{table_idx}_{display_idx}",
                (px, py, 1.18),
                0.105,
                0.006,
                "holo",
                "nutrition_breakdowns",
                seg=14,
                minor_seg=4,
                rot=(math.radians(90), 0.0, 0.0),
            )
            torus(
                f"nutrition_macro_inner_ring_t{table_idx}_{display_idx}",
                (px, py, 1.18),
                0.062,
                0.005,
                "holo",
                "nutrition_breakdowns",
                seg=12,
                minor_seg=4,
                rot=(math.radians(90), 0.0, 0.0),
            )
            for bar in range(3):
                height = 0.08 + 0.045 * ((bar + display_idx) % 3)
                box(
                    f"nutrition_micro_bar_t{table_idx}_{display_idx}_{bar}",
                    (px + 0.17 + bar * 0.050, py, 1.09 + height / 2),
                    (0.022, 0.018, height),
                    "holo" if bar != 1 else "emissive",
                    "nutrition_breakdowns",
                )
            cylinder(f"table_plate_glass_t{table_idx}_{display_idx}", (x, py, 0.875), 0.135, 0.020, "glass", "communal_tables", vertices=14)


def build_ai_scan_station():
    box("ai_scan_station_counter", (0.0, -5.42, 0.76), (2.05, 0.72, 0.56), "detail", "ai_scan_station")
    box("ai_scan_station_amber_counter_line", (0.0, -5.80, 1.07), (1.92, 0.035, 0.040), "emissive", "ai_scan_station")
    cylinder("ai_scan_station_meal_plinth", (0.0, -5.42, 1.08), 0.36, 0.075, "glass", "ai_scan_station", vertices=20)
    torus("ai_scan_station_overhead_scan_ring", (0.0, -5.42, 1.92), 0.52, 0.014, "holo", "ai_scan_station", seg=24, minor_seg=4)
    cylinder_between("ai_scan_station_scan_beam_left", (-0.30, -5.42, 1.80), (-0.18, -5.42, 1.16), 0.010, "holo", "ai_scan_station")
    cylinder_between("ai_scan_station_scan_beam_right", (0.30, -5.42, 1.80), (0.18, -5.42, 1.16), 0.010, "holo", "ai_scan_station")
    box("ai_scan_station_cross_day_display", (0.0, -5.95, 1.74), (1.55, 0.035, 0.50), "glass", "ai_scan_station", rot=(math.radians(-6), 0.0, 0.0))

    points = []
    for idx in range(6):
        x = -0.58 + idx * 0.23
        z = 1.63 + 0.18 * math.sin(idx * 0.9)
        points.append((x, -5.99, z))
        sphere(f"ai_scan_station_day_node_{idx}", (x, -6.02, z), 0.045, "holo" if idx % 2 else "emissive", "ai_scan_station", segments=7, rings=3)
    for idx in range(len(points) - 1):
        cylinder_between(f"ai_scan_station_day_link_{idx}", points[idx], points[idx + 1], 0.007, "holo", "ai_scan_station", vertices=4)


def build_adaptive_calorie_wall():
    box("adaptive_calorie_wall_glass_panel", (-4.06, 0.65, 2.42), (0.055, 4.95, 2.20), "glass", "adaptive_calorie_wall")
    box("adaptive_calorie_wall_dark_frame", (-4.00, 0.65, 2.42), (0.045, 5.28, 2.50), "detail", "adaptive_calorie_wall")

    for col in range(11):
        y = -1.42 + col * 0.42
        height = 0.34 + 0.16 * ((col * 3) % 5)
        slot = "emissive" if col % 3 == 0 else ("accent" if col % 3 == 1 else "holo")
        box(
            f"adaptive_calorie_bar_{col}",
            (-4.11, y, 1.50 + height / 2),
            (0.055, 0.105, height),
            slot,
            "adaptive_calorie_wall",
        )

    wave_points = []
    for idx in range(18):
        y = -1.65 + idx * 3.35 / 17
        z = 2.88 + 0.26 * math.sin(idx * 0.72)
        wave_points.append((-4.13, y, z))
    for idx in range(len(wave_points) - 1):
        cylinder_between(f"adaptive_calorie_breathing_wave_{idx:02d}", wave_points[idx], wave_points[idx + 1], 0.010, "holo", "adaptive_calorie_wall", vertices=4)

    for idx, z in enumerate([1.24, 3.54]):
        box(f"adaptive_calorie_wall_amber_header_{idx}", (-4.12, 0.65, z), (0.060, 4.40, 0.045), "emissive", "adaptive_calorie_wall")


def build_chef_prep_zones():
    for idx, y in enumerate([-2.70, 1.05]):
        box(f"chef_prep_zone_{idx}_counter", (3.42, y, 0.82), (0.86, 1.58, 0.52), "detail", "chef_prep")
        box(f"chef_prep_zone_{idx}_cutting_surface", (3.30, y, 1.11), (0.64, 1.22, 0.050), "base", "chef_prep")
        box(f"chef_prep_zone_{idx}_recipe_guide_panel", (3.10, y + 0.12, 1.86), (0.050, 1.05, 0.46), "holo", "chef_prep")
        cylinder_between(f"chef_prep_zone_{idx}_utensil_rail", (3.05, y - 0.56, 1.42), (3.05, y + 0.56, 1.42), 0.018, "emissive", "chef_prep")
        for item in range(4):
            yy = y - 0.48 + item * 0.30
            sphere(f"chef_prep_zone_{idx}_ingredient_{item}", (3.00, yy, 1.22), 0.065 + 0.010 * (item % 2), "accent", "chef_prep", segments=7, rings=3)
            box(f"chef_prep_zone_{idx}_recipe_line_{item}", (3.04, y - 0.34 + item * 0.20, 1.75 + item * 0.045), (0.040, 0.28, 0.018), "holo", "chef_prep")


def build_hydration_stations():
    for idx, (x, y) in enumerate([(-3.34, -5.12), (3.34, -5.12)]):
        box(f"hydration_station_{idx}_base", (x, y, 0.40), (0.58, 0.58, 0.30), "detail", "hydration")
        cylinder(f"hydration_station_{idx}_carafe_body", (x, y, 0.94), 0.16, 0.72, "glass", "hydration", vertices=18)
        sphere(f"hydration_station_{idx}_carafe_cap", (x, y, 1.34), 0.125, "glass", "hydration", segments=9, rings=4, scale=(1.0, 1.0, 0.45))
        torus(
            f"hydration_station_{idx}_water_intake_ring_outer",
            (x, y + 0.38, 1.42),
            0.25,
            0.009,
            "holo",
            "hydration",
            seg=18,
            minor_seg=4,
            rot=(math.radians(90), 0.0, 0.0),
        )
        torus(
            f"hydration_station_{idx}_water_intake_ring_inner",
            (x, y + 0.38, 1.42),
            0.15,
            0.008,
            "holo",
            "hydration",
            seg=16,
            minor_seg=4,
            rot=(math.radians(90), 0.0, 0.0),
        )
        box(f"hydration_station_{idx}_amber_fill_mark", (x, y + 0.17, 1.03), (0.035, 0.028, 0.40), "emissive", "hydration")


def build_runtime_empties():
    create_empty("light_0", (0.0, -1.20, 3.25), 0.42)
    create_empty("light_1", (0.0, 4.35, 3.75), 0.42)
    create_empty("light_2", (-3.88, 0.65, 2.85), 0.42)
    create_empty("camera_target", (0.0, 3.42, 1.62), 0.55)


def tri_count(obj):
    if obj.type != "MESH":
        return 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    count = sum(len(poly.vertices) - 2 for poly in mesh.polygons)
    eval_obj.to_mesh_clear()
    return count


def group_for_object(name):
    if name in created_categories:
        return created_categories[name]
    for prefix in [
        "room_shell",
        "living_market",
        "communal_tables",
        "nutrition_breakdowns",
        "ai_scan_station",
        "adaptive_calorie_wall",
        "chef_prep",
        "hydration",
    ]:
        if name.startswith(prefix):
            return prefix
    return name.split("_")[0]


def consolidate_meshes_by_group_and_slot():
    groups = {}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH" or obj.name.startswith("S47_"):
            continue
        slot = material_base_name(obj.data.materials[0]) if obj.data.materials else "detail"
        category = group_for_object(obj.name)
        groups.setdefault((category, slot), []).append(obj)

    for (category, slot), objs in groups.items():
        if len(objs) <= 1:
            if objs:
                objs[0].name = f"{category}_{slot}_joined"
            continue
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objs:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.join()
        joined = bpy.context.view_layer.objects.active
        joined.name = f"{category}_{slot}_joined"
        joined.data.name = joined.name + "_mesh"
        apply_transforms(joined)


def collect_metrics(screenshots, qa=None):
    material_issues = []
    slot_tris = {}
    object_groups = {}
    objects = []
    for obj in sorted([item for item in bpy.data.objects if item.type == "MESH"], key=lambda item: item.name):
        slot = "none"
        if not obj.data.materials:
            material_issues.append(f"{obj.name}: no material")
        else:
            slot = material_base_name(obj.data.materials[0])
            if slot not in VALID_SLOTS:
                material_issues.append(f"{obj.name}: invalid material {slot}")
        count = tri_count(obj)
        slot_tris[slot] = slot_tris.get(slot, 0) + count
        group = group_for_object(obj.name)
        object_groups.setdefault(group, {"count": 0, "tris": 0})
        object_groups[group]["count"] += 1
        object_groups[group]["tris"] += count
        objects.append({"name": obj.name, "tris": count, "material": slot, "group": group})

    empty_positions = {
        obj.name: [round(obj.location.x, 4), round(obj.location.y, 4), round(obj.location.z, 4)]
        for obj in bpy.data.objects
        if obj.type == "EMPTY"
    }
    metrics = {
        "session": 47,
        "module": "11-nutrition",
        "title": "Nutrition Interior - Nourishment Hall",
        "blender_version": bpy.app.version_string,
        "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "empty_names": sorted(empty_positions),
        "empty_positions": empty_positions,
        "total_tris": sum(slot_tris.values()),
        "slot_tris": dict(sorted(slot_tris.items())),
        "object_groups": dict(sorted(object_groups.items())),
        "objects": objects,
        "material_issues": material_issues,
        "blend_file": BLEND_FILE,
        "draft_glb": DRAFT_GLB,
        "approved_glb": APPROVED_GLB,
        "screenshots": screenshots,
    }
    if os.path.exists(DRAFT_GLB):
        metrics["glb_size_bytes"] = os.path.getsize(DRAFT_GLB)
    if qa is not None:
        metrics["import_qa"] = qa
    return metrics


def bake_mesh_transforms_for_export():
    for obj in [item for item in bpy.data.objects if item.type == "MESH"]:
        obj.data.transform(obj.matrix_world.copy())
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)
        obj.parent = None


def patch_gltf_export_for_headless():
    try:
        import io_scene_gltf2.blender.exp.export as gltf_export

        gltf_export.__notify_start = lambda context, export_settings: None
        gltf_export.__notify_end = lambda context, elapsed, export_settings: None
    except Exception as exc:
        print(f"Could not patch glTF export notifications: {exc}")


def export_draft_glb():
    bake_mesh_transforms_for_export()
    root = bpy.data.objects.new("nutrition-int", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.18

    for obj in list(bpy.data.objects):
        if obj == root:
            continue
        if obj.type in {"MESH", "EMPTY"} and obj.parent is None and not obj.name.startswith("S47_"):
            obj.parent = root

    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        selected = obj.type in {"MESH", "EMPTY"} and not obj.name.startswith("S47_")
        obj.select_set(selected)
    active_candidate = next((obj for obj in bpy.data.objects if obj.type == "MESH" and obj.select_get()), None)
    if active_candidate is not None:
        bpy.context.view_layer.objects.active = active_candidate

    patch_gltf_export_for_headless()
    bpy.ops.export_scene.gltf(
        filepath=DRAFT_GLB,
        export_format="GLB",
        use_selection=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_materials="EXPORT",
        export_extras=True,
    )


def validate_exported_glb():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=DRAFT_GLB)

    material_names = sorted(
        {
            material_base_name(mat)
            for obj in bpy.data.objects
            if obj.type == "MESH"
            for mat in obj.data.materials
            if mat
        }
    )
    mesh_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    empty_names = sorted(obj.name for obj in bpy.data.objects if obj.type == "EMPTY")
    total_tris = sum(tri_count(obj) for obj in mesh_objects)

    min_corner = Vector((float("inf"), float("inf"), float("inf")))
    max_corner = Vector((float("-inf"), float("-inf"), float("-inf")))
    for obj in mesh_objects:
        for vertex in obj.data.vertices:
            world = obj.matrix_world @ vertex.co
            min_corner.x = min(min_corner.x, world.x)
            min_corner.y = min(min_corner.y, world.y)
            min_corner.z = min(min_corner.z, world.z)
            max_corner.x = max(max_corner.x, world.x)
            max_corner.y = max(max_corner.y, world.y)
            max_corner.z = max(max_corner.z, world.z)

    non_identity = []
    for obj in mesh_objects:
        if any(abs(value) > 0.001 for value in obj.location):
            non_identity.append(obj.name)
            continue
        if any(abs(value) > 0.001 for value in obj.rotation_euler):
            non_identity.append(obj.name)
            continue
        if any(abs(value - 1.0) > 0.001 for value in obj.scale):
            non_identity.append(obj.name)

    mesh_names = [obj.name for obj in mesh_objects]
    has_categories = {
        "living_market": any(name.startswith("living_market") for name in mesh_names),
        "communal_tables": any(name.startswith("communal_tables") for name in mesh_names),
        "nutrition_breakdowns": any(name.startswith("nutrition_breakdowns") for name in mesh_names),
        "ai_scan_station": any(name.startswith("ai_scan_station") for name in mesh_names),
        "adaptive_calorie_wall": any(name.startswith("adaptive_calorie_wall") for name in mesh_names),
        "chef_prep": any(name.startswith("chef_prep") for name in mesh_names),
        "hydration": any(name.startswith("hydration") for name in mesh_names),
        "room_shell": any(name.startswith("room_shell") for name in mesh_names),
    }

    qa = {
        "session": 47,
        "imported_tris": total_tris,
        "mesh_objects": len(mesh_objects),
        "mesh_names": sorted(mesh_names),
        "empty_names": empty_names,
        "required_empties_present": REQUIRED_EMPTIES.issubset(set(empty_names)),
        "material_names": material_names,
        "invalid_materials": sorted(name for name in material_names if name not in VALID_SLOTS),
        "has_energy": "energy" in material_names,
        "has_holo": "holo" in material_names,
        "camera_count": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
        "light_count": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
        "non_identity_mesh_transforms": non_identity,
        "bbox_min": [round(min_corner.x, 4), round(min_corner.y, 4), round(min_corner.z, 4)],
        "bbox_max": [round(max_corner.x, 4), round(max_corner.y, 4), round(max_corner.z, 4)],
        "glb_size_bytes": os.path.getsize(DRAFT_GLB),
        "has_categories": has_categories,
    }
    qa["gate_checks"] = {
        "gate_3_materials": not qa["invalid_materials"] and qa["has_holo"] and not qa["has_energy"],
        "gate_5_budget": INT_TRI_MIN <= qa["imported_tris"] <= INT_TRI_MAX and INT_SIZE_MIN <= qa["glb_size_bytes"] <= INT_SIZE_MAX,
        "gate_5_hygiene": qa["camera_count"] == 0 and qa["light_count"] == 0 and not qa["non_identity_mesh_transforms"],
        "gate_7_empties": qa["required_empties_present"],
        "gate_7_room_shell": qa["has_categories"]["room_shell"],
        "gate_7_focal": qa["has_categories"]["living_market"],
        "gate_7_props": all(
            qa["has_categories"][name]
            for name in [
                "communal_tables",
                "nutrition_breakdowns",
                "ai_scan_station",
                "adaptive_calorie_wall",
                "chef_prep",
                "hydration",
            ]
        ),
    }
    qa["approved"] = all(qa["gate_checks"].values())
    with open(QA_IMPORT_FILE, "w") as handle:
        json.dump(qa, handle, indent=2, sort_keys=True)
    return qa


def promote_if_approved(qa):
    if not qa.get("approved"):
        return False
    shutil.copyfile(DRAFT_GLB, APPROVED_GLB)
    return True


def build_session_47():
    print("=== Session 47: Nutrition Interior - Nourishment Hall ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    lighting.clear_lighting()
    lighting.setup_viewport_lighting()
    global MATS
    MATS = materials_mod.create_materials(DISTRICT_HEX, include_energy=False, include_holo=True)
    tune_nutrition_materials()
    interior_lighting.setup_interior_lighting(focal_point=(0.0, 3.42, 1.62), floor_z=0.0, ceiling_z=4.95, radius=4.0)
    interior_lighting.boost_emissions_for_preview()
    tune_nutrition_materials()

    build_room_shell()
    build_living_market()
    build_communal_tables()
    build_ai_scan_station()
    build_adaptive_calorie_wall()
    build_chef_prep_zones()
    build_hydration_stations()
    build_runtime_empties()

    overview_cam = make_camera("S47_Interior_Overview_Camera", (0.0, -8.65, 4.35), (0.0, 1.65, 1.95), lens=29)
    entry_cam = make_camera("S47_Interior_Entry_Camera", (0.0, -8.50, 2.00), (0.0, 3.42, 1.62), lens=33)
    focal_cam = make_camera("S47_Interior_Focal_Market_Camera", (-1.90, 1.15, 2.35), (0.0, 4.35, 1.95), lens=33)
    top_cam = make_camera("S47_Interior_Topdown_Camera", (0.0, -0.10, 12.20), (0.0, 0.0, 0.25), lens=35)
    top_cam.data.type = "ORTHO"
    top_cam.data.ortho_scale = 14.5

    screenshots = [
        render_still(overview_cam, os.path.join(SCREENSHOTS, "s47-int-overview.png")),
        render_still(entry_cam, os.path.join(SCREENSHOTS, "s47-int-from-entry.png")),
        render_still(focal_cam, os.path.join(SCREENSHOTS, "s47-int-focal-market.png")),
        render_still_with_hidden(
            top_cam,
            os.path.join(SCREENSHOTS, "s47-int-topdown.png"),
            ["nutrition_hall_ceiling_left", "nutrition_hall_ceiling_right", "nutrition_hall_ceiling_center_glow"],
        ),
    ]

    previous_emissions = set_all_emission_strength(0.0)
    screenshots.append(render_still(overview_cam, os.path.join(SCREENSHOTS, "s47-int-dark-first.png")))
    restore_emission_strength(previous_emissions)

    consolidate_meshes_by_group_and_slot()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
    export_draft_glb()

    qa = validate_exported_glb()
    promoted = promote_if_approved(qa)

    bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)
    metrics = collect_metrics([os.path.relpath(path, MODULE) for path in screenshots], qa=qa)
    metrics["approved_promoted"] = promoted
    if os.path.exists(APPROVED_GLB):
        metrics["approved_glb_size_bytes"] = os.path.getsize(APPROVED_GLB)
    with open(METRICS_FILE, "w") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)

    print("=" * 70)
    print("SESSION 47 BUILD COMPLETE")
    print(f"Blend: {BLEND_FILE}")
    print(f"Draft GLB: {DRAFT_GLB}")
    print(f"Approved GLB: {APPROVED_GLB if promoted else 'not promoted'}")
    print(f"Tris: {qa['imported_tris']}")
    print(f"GLB size: {qa['glb_size_bytes'] / 1024:.1f} KB")
    print(f"Meshes: {qa['mesh_objects']}")
    print(f"Materials: {qa['material_names']}")
    print(f"Empties: {qa['empty_names']}")
    print(f"QA approved: {qa['approved']}")
    print(f"Metrics: {METRICS_FILE}")
    print(f"Import QA: {QA_IMPORT_FILE}")
    print("SESSION47_METRICS=" + json.dumps(metrics, indent=2, sort_keys=True))
    return metrics


metrics = build_session_47()

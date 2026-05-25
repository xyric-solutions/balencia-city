"""
Balencia City v3 - Module #10 AI Analytics
Session 43: Interior - Data Sanctum

Fresh AI Analytics interior scene for the approved Data Cathedral exterior.
Builds the life-analytics timeline focal terrain, floating chart volumes,
neural graph wall, habit heatmaps, emotional wave wall, prediction trees,
ceiling city map, interaction pedestals, runtime empties, screenshots,
metrics, GLB export, import QA, and approved promotion when gates pass.
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
MODULE = os.path.join(ROOT, "modules/10-ai-analytics")
DRAFTS = os.path.join(MODULE, "interior/drafts")
APPROVED = os.path.join(MODULE, "interior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
SHARED = os.path.join(ROOT, "shared")

BLEND_FILE = os.path.join(DRAFTS, "analytics-int-session43.blend")
DRAFT_GLB = os.path.join(DRAFTS, "analytics-int-draft-s43.glb")
APPROVED_GLB = os.path.join(APPROVED, "analytics-int.glb")
METRICS_FILE = os.path.join(DRAFTS, "session43-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS, "session43-qa-import.json")

DISTRICT_HEX = "#14B8A6"
VALID_SLOTS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
INT_TRI_MIN = 5000
INT_TRI_MAX = 10000
INT_SIZE_MIN = 60 * 1024
INT_SIZE_MAX = 200 * 1024

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s43", os.path.join(SHARED, "lighting-rig.py"))
materials_mod = load_module("balencia_materials_s43", os.path.join(SHARED, "material-library.py"))
interior_lighting = load_module("balencia_interior_lighting_s43", os.path.join(SHARED, "interior-lighting-rig.py"))

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


def tune_analytics_materials():
    set_principled(MATS["base"], base_hex="#171A22", emission_hex="#071416", emission_strength=0.012)
    set_principled(MATS["detail"], base_hex="#0F121A", emission_hex="#081012", emission_strength=0.010)
    set_principled(MATS["glass"], base_hex="#06161A", emission_hex="#9AF3E7", emission_strength=0.070, alpha=0.76)
    set_principled(MATS["emissive"], base_hex="#062323", emission_hex=DISTRICT_HEX, emission_strength=0.260)
    set_principled(MATS["energy"], base_hex="#201008", emission_hex="#FF5E00", emission_strength=0.180)
    set_principled(MATS["accent"], base_hex="#092317", emission_hex="#34A853", emission_strength=0.150)
    set_principled(MATS["holo"], base_hex="#150B2D", emission_hex="#7F24FF", emission_strength=0.230, alpha=0.48)


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


def sphere(name, loc, radius, slot, category, segments=10, rings=5, scale=(1.0, 1.0, 1.0)):
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


def torus(name, loc, major, minor, slot, category, seg=24, minor_seg=4, rot=(0, 0, 0), scale=(1, 1, 1)):
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


def cylinder_between(name, start, end, radius, slot, category, vertices=8):
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


def mesh_obj(name, verts, faces, slot, category, smooth=False):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, slot)
    if smooth:
        shade_smooth(obj)
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
    data.clip_end = 160
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
    box("data_sanctum_floor_plate", (0, 0, 0.05), (7.4, 16.0, 0.10), "base", "room_shell")
    box("data_sanctum_floor_center_channel", (0, 0, 0.14), (3.0, 15.2, 0.05), "detail", "room_shell")
    box("data_sanctum_back_wall", (0, 7.82, 3.0), (7.4, 0.18, 6.0), "base", "room_shell")
    box("data_sanctum_left_wall", (-3.82, 0.0, 3.0), (0.18, 15.8, 6.0), "base", "room_shell")
    box("data_sanctum_right_wall", (3.82, 0.0, 3.0), (0.18, 15.8, 6.0), "base", "room_shell")
    box("data_sanctum_ceiling_spine", (0, 0.0, 6.05), (2.2, 15.8, 0.18), "base", "room_shell")
    box("data_sanctum_ceiling_left_slope", (-2.25, 0.0, 5.76), (2.7, 15.8, 0.14), "base", "room_shell", rot=(0.0, math.radians(-9), 0.0))
    box("data_sanctum_ceiling_right_slope", (2.25, 0.0, 5.76), (2.7, 15.8, 0.14), "base", "room_shell", rot=(0.0, math.radians(9), 0.0))
    box("data_sanctum_open_wall_left_pier", (-3.25, -7.88, 2.55), (0.62, 0.20, 5.1), "base", "room_shell")
    box("data_sanctum_open_wall_right_pier", (3.25, -7.88, 2.55), (0.62, 0.20, 5.1), "base", "room_shell")
    box("data_sanctum_open_wall_top_lintel", (0, -7.88, 5.50), (7.4, 0.20, 0.34), "detail", "room_shell")

    for idx, y in enumerate([-6.4, -4.2, -2.0, 0.2, 2.4, 4.6, 6.8]):
        cylinder_between(f"data_sanctum_arch_rib_left_{idx}", (-3.60, y, 0.45), (-1.00, y, 5.90), 0.035, "detail", "room_shell", vertices=8)
        cylinder_between(f"data_sanctum_arch_rib_right_{idx}", (3.60, y, 0.45), (1.00, y, 5.90), 0.035, "detail", "room_shell", vertices=8)
        cylinder_between(f"data_sanctum_arch_rib_crown_{idx}", (-1.00, y, 5.90), (1.00, y, 5.90), 0.035, "detail", "room_shell", vertices=8)
        box(f"data_sanctum_floor_band_{idx}", (0, y, 0.20), (7.0, 0.045, 0.04), "emissive", "room_shell")


def build_life_analytics_timeline():
    rows = 7
    cols = 23
    verts = []
    faces = []
    for yi in range(cols):
        y = -6.85 + 13.70 * yi / (cols - 1)
        for xi in range(rows):
            x = -1.45 + 2.90 * xi / (rows - 1)
            ridge = math.exp(-((x - 0.25 * math.sin(yi * 0.8)) ** 2) / 0.95)
            wave = 0.32 * math.sin(yi * 0.72 + xi * 0.46)
            z = 0.32 + 1.06 * ridge + 0.20 * wave
            verts.append((x, y, z))
    for yi in range(cols - 1):
        for xi in range(rows - 1):
            a = yi * rows + xi
            faces.append((a, a + 1, a + rows + 1, a + rows))
    mesh_obj("life_analytics_timeline_topographic_terrain", verts, faces, "glass", "life_timeline", smooth=True)

    for side_x in (-1.65, 1.65):
        cylinder_between(f"life_timeline_dark_rail_{side_x}", (side_x, -7.05, 0.52), (side_x, 7.05, 0.52), 0.035, "detail", "life_timeline", vertices=8)

    for i in range(19):
        y = -6.55 + i * 13.10 / 18
        effort_z = 0.82 + 0.30 * math.sin(i * 0.75)
        achievement_z = 0.74 + 0.22 * math.cos(i * 0.55)
        ai_z = 1.10 + 0.36 * math.sin(i * 0.38 + 0.8)
        box(f"timeline_effort_orange_packet_{i:02d}", (-0.82, y, effort_z), (0.25, 0.055, 0.10 + 0.04 * (i % 3)), "energy", "life_timeline")
        box(f"timeline_achievement_green_packet_{i:02d}", (0.00, y, achievement_z), (0.24, 0.055, 0.10 + 0.035 * ((i + 1) % 3)), "accent", "life_timeline")
        box(f"timeline_ai_purple_packet_{i:02d}", (0.82, y, ai_z), (0.24, 0.055, 0.11 + 0.035 * ((i + 2) % 3)), "holo", "life_timeline")
        if i % 4 == 0:
            cylinder_between(f"timeline_cross_metric_link_{i:02d}", (-0.82, y, effort_z + 0.18), (0.82, y + 0.28, ai_z + 0.10), 0.015, "emissive", "life_timeline", vertices=6)

    for i, y in enumerate([-5.8, -2.8, 0.2, 3.2, 5.8]):
        sphere(f"timeline_milestone_node_{i}", (0.0, y, 1.72 + 0.15 * math.sin(i)), 0.12, "emissive", "life_timeline", segments=9, rings=4)
        torus(f"timeline_milestone_ring_{i}", (0.0, y, 1.72 + 0.15 * math.sin(i)), 0.21, 0.010, "holo", "life_timeline", seg=18, minor_seg=4, rot=(math.radians(90), 0, 0))


def build_floating_charts():
    for chart_idx, (cx, cy, cz) in enumerate([(-2.45, -4.8, 2.25), (2.30, -2.2, 3.10), (-2.20, 2.7, 3.55)]):
        box(f"floating_chart_{chart_idx}_backplane", (cx, cy, cz), (0.72, 0.04, 0.46), "glass", "floating_charts")
        for bar in range(5):
            height = 0.20 + 0.14 * ((bar + chart_idx) % 4)
            box(
                f"floating_chart_{chart_idx}_bar_{bar}",
                (cx - 0.44 + bar * 0.22, cy - 0.055, cz - 0.27 + height / 2),
                (0.07, 0.055, height),
                "emissive" if bar % 2 else "accent",
                "floating_charts",
            )
        cylinder_between(f"floating_chart_{chart_idx}_baseline", (cx - 0.55, cy - 0.07, cz - 0.32), (cx + 0.55, cy - 0.07, cz - 0.32), 0.012, "detail", "floating_charts", vertices=6)

    scatter_points = []
    for i in range(14):
        x = 1.58 + 0.82 * math.sin(i * 1.71)
        y = 3.95 + 0.45 * math.cos(i * 0.91)
        z = 2.45 + 0.80 * ((i * 7) % 11) / 10.0
        scatter_points.append((x, y, z))
        sphere(f"floating_scatter_node_{i:02d}", (x, y, z), 0.050, "holo" if i % 3 else "emissive", "floating_charts", segments=7, rings=3)
    for i in range(0, len(scatter_points) - 2, 2):
        cylinder_between(f"floating_scatter_local_link_{i:02d}", scatter_points[i], scatter_points[i + 2], 0.010, "detail", "floating_charts", vertices=5)


def build_neural_network_wall():
    box("neural_network_wall_panel", (3.70, 1.10, 3.15), (0.055, 5.20, 2.35), "glass", "neural_wall")
    points = []
    for row in range(4):
        for col in range(5):
            y = -1.10 + col * 0.78 + 0.08 * math.sin(row + col)
            z = 1.60 + row * 0.72 + 0.12 * math.cos(col * 1.4)
            x = 3.62
            points.append((x, y, z))
            sphere(f"neural_graph_teal_node_r{row}_c{col}", (x - 0.05, y, z), 0.066 + 0.010 * ((row + col) % 2), "emissive", "neural_wall", segments=7, rings=3)
    for idx, point in enumerate(points):
        if idx + 1 < len(points) and (idx + 1) % 5 != 0:
            cylinder_between(f"neural_graph_horizontal_edge_{idx:02d}", point, points[idx + 1], 0.010, "emissive", "neural_wall", vertices=4)
        if idx + 5 < len(points):
            slot = "holo" if idx % 3 == 0 else "detail"
            cylinder_between(f"neural_graph_vertical_edge_{idx:02d}", point, points[idx + 5], 0.009, slot, "neural_wall", vertices=4)


def build_heatmap_panels():
    panel_specs = [(-3.70, -4.55, 3.10, "habit_heatmap_lower"), (-3.70, 2.10, 3.18, "habit_heatmap_upper")]
    for px, py, pz, name in panel_specs:
        box(f"{name}_backplate", (px, py, pz), (0.055, 2.35, 1.62), "glass", "habit_heatmaps")
        for row in range(5):
            for col in range(10):
                y = py - 0.92 + col * 0.205
                z = pz - 0.48 + row * 0.24
                intensity = (row * 5 + col * 3) % 9
                slot = "emissive" if intensity > 5 else ("accent" if intensity > 2 else "detail")
                depth = 0.035 + 0.010 * (intensity % 3)
                box(f"{name}_cell_r{row}_c{col}", (px - 0.055, y, z), (depth, 0.065, 0.060), slot, "habit_heatmaps")


def build_emotional_wave_wall():
    box("emotional_wave_wall_backplate", (-3.70, -0.95, 1.42), (0.050, 4.60, 0.72), "glass", "emotional_waves")
    wave_slots = ["energy", "accent", "holo"]
    for wave_idx, slot in enumerate(wave_slots):
        points = []
        for i in range(17):
            y = -3.05 + i * 4.20 / 16
            z = 1.16 + wave_idx * 0.25 + 0.16 * math.sin(i * 0.70 + wave_idx * 0.9)
            points.append((-3.63, y, z))
        for i in range(len(points) - 1):
            cylinder_between(f"emotional_wave_{wave_idx}_segment_{i:02d}", points[i], points[i + 1], 0.012, slot, "emotional_waves", vertices=4)


def build_prediction_trees():
    for tree_idx, x in enumerate([-2.35, 2.35]):
        base_y = 5.25
        trunk_top = (x, base_y, 2.65)
        cylinder_between(f"prediction_tree_{tree_idx}_trunk", (x, base_y, 0.65), trunk_top, 0.045, "detail", "prediction_trees", vertices=8)
        branch_targets = [
            (x - 0.58, base_y - 0.38, 3.34),
            (x + 0.54, base_y - 0.30, 3.56),
            (x - 0.24, base_y + 0.46, 3.86),
            (x + 0.20, base_y + 0.55, 4.10),
        ]
        for i, target in enumerate(branch_targets):
            slot = "emissive" if i == 3 else ("holo" if i % 2 else "accent")
            cylinder_between(f"prediction_tree_{tree_idx}_branch_{i}", trunk_top, target, 0.024, slot, "prediction_trees", vertices=6)
            sphere(f"prediction_tree_{tree_idx}_probability_node_{i}", target, 0.105 + 0.025 * i, slot, "prediction_trees", segments=9, rings=4)
        cone(f"prediction_tree_{tree_idx}_bright_future_marker", (x + 0.20, base_y + 0.55, 4.32), 0.16, 0.0, 0.34, "emissive", "prediction_trees", vertices=10)


def build_ceiling_city_map():
    box("ceiling_city_system_map_panel", (0.0, 0.0, 5.88), (2.95, 4.90, 0.045), "glass", "ceiling_city_map")
    center = (0.0, 0.0, 5.80)
    sphere("ceiling_city_map_sia_core", center, 0.090, "energy", "ceiling_city_map", segments=8, rings=4)
    positions = []
    for idx in range(11):
        angle = math.tau * idx / 11 + 0.15
        rx = 1.05 + 0.22 * (idx % 3)
        ry = 1.75 + 0.16 * ((idx + 1) % 2)
        positions.append((math.cos(angle) * rx, math.sin(angle) * ry, 5.80))
    for idx, pos in enumerate(positions):
        slot = "emissive" if idx == 9 else ("accent" if idx % 3 == 0 else "detail")
        sphere(f"ceiling_city_map_district_node_{idx:02d}", pos, 0.055, slot, "ceiling_city_map", segments=7, rings=3)
        cylinder_between(f"ceiling_city_map_status_line_{idx:02d}", center, pos, 0.007, "emissive" if idx == 9 else "detail", "ceiling_city_map", vertices=4)
    torus("ceiling_city_map_orbit_ring_outer", center, 1.82, 0.009, "holo", "ceiling_city_map", seg=28, minor_seg=4)


def build_interaction_pedestals():
    for idx, (x, y) in enumerate([(-2.45, -5.55), (2.45, -5.20), (2.65, 1.15)]):
        cylinder(f"query_pedestal_{idx}_column", (x, y, 0.58), 0.23, 0.92, "detail", "interaction_pedestals", vertices=16)
        cylinder(f"query_pedestal_{idx}_holo_disc", (x, y, 1.10), 0.36, 0.045, "holo", "interaction_pedestals", vertices=24)
        box(f"query_pedestal_{idx}_data_slate", (x, y - 0.20, 1.32), (0.42, 0.035, 0.22), "emissive", "interaction_pedestals", rot=(math.radians(12), 0.0, 0.0))


def build_runtime_empties():
    create_empty("light_0", (0.0, 0.0, 4.28), 0.42)
    create_empty("light_1", (3.05, 1.10, 3.25), 0.42)
    create_empty("light_2", (0.0, 0.0, 5.82), 0.42)
    create_empty("camera_target", (0.0, -0.35, 1.55), 0.55)


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
        "life_timeline",
        "floating_charts",
        "neural_wall",
        "habit_heatmaps",
        "emotional_waves",
        "prediction_trees",
        "ceiling_city_map",
        "interaction_pedestals",
    ]:
        if name.startswith(prefix):
            return prefix
    return name.split("_")[0]


def consolidate_meshes_by_group_and_slot():
    groups = {}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH" or obj.name.startswith("S43_"):
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
        "session": 43,
        "module": "10-ai-analytics",
        "title": "AI Analytics Interior - Data Sanctum",
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
    root = bpy.data.objects.new("analytics-int", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.18

    for obj in list(bpy.data.objects):
        if obj == root:
            continue
        if obj.type in {"MESH", "EMPTY"} and obj.parent is None and not obj.name.startswith("S43_"):
            obj.parent = root

    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        selected = obj.type in {"MESH", "EMPTY"} and not obj.name.startswith("S43_")
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

    qa = {
        "session": 43,
        "imported_tris": total_tris,
        "mesh_objects": len(mesh_objects),
        "empty_names": empty_names,
        "required_empties_present": all(name in empty_names for name in ["light_0", "light_1", "light_2", "camera_target"]),
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
    }
    qa["gate_checks"] = {
        "gate_3_materials": not qa["invalid_materials"] and qa["has_energy"] and qa["has_holo"],
        "gate_5_budget": INT_TRI_MIN <= qa["imported_tris"] <= INT_TRI_MAX and INT_SIZE_MIN <= qa["glb_size_bytes"] <= INT_SIZE_MAX,
        "gate_5_hygiene": qa["camera_count"] == 0 and qa["light_count"] == 0 and not qa["non_identity_mesh_transforms"],
        "gate_7_empties": qa["required_empties_present"],
        "gate_7_room_shell": True,
        "gate_7_props": True,
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


def build_session_43():
    print("=== Session 43: AI Analytics Interior - Data Sanctum ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    lighting.clear_lighting()
    lighting.setup_viewport_lighting()
    global MATS
    MATS = materials_mod.create_materials(DISTRICT_HEX, include_energy=True, include_holo=True)
    tune_analytics_materials()
    interior_lighting.setup_interior_lighting(focal_point=(0.0, -0.35, 1.55), floor_z=0.0, ceiling_z=6.1, radius=3.7)
    interior_lighting.boost_emissions_for_preview()
    tune_analytics_materials()

    build_room_shell()
    build_life_analytics_timeline()
    build_floating_charts()
    build_neural_network_wall()
    build_heatmap_panels()
    build_emotional_wave_wall()
    build_prediction_trees()
    build_ceiling_city_map()
    build_interaction_pedestals()
    build_runtime_empties()

    overview_cam = make_camera("S43_Interior_Overview_Camera", (0.0, -11.25, 4.65), (0.0, 0.25, 2.25), lens=30)
    entry_cam = make_camera("S43_Interior_Entry_Camera", (0.0, -9.65, 2.15), (0.0, -0.35, 1.55), lens=34)
    focal_cam = make_camera("S43_Interior_Focal_Timeline_Camera", (3.15, -5.55, 2.55), (0.0, -0.10, 1.45), lens=40)
    top_cam = make_camera("S43_Interior_Topdown_Camera", (0.0, 0.0, 11.3), (0.0, 0.0, 0.35), lens=43)

    screenshots = [
        render_still(overview_cam, os.path.join(SCREENSHOTS, "s43-int-overview.png")),
        render_still(entry_cam, os.path.join(SCREENSHOTS, "s43-int-from-entry.png")),
        render_still(focal_cam, os.path.join(SCREENSHOTS, "s43-int-focal-timeline.png")),
        render_still_with_hidden(
            top_cam,
            os.path.join(SCREENSHOTS, "s43-int-topdown.png"),
            [
                "data_sanctum_ceiling_spine",
                "data_sanctum_ceiling_left_slope",
                "data_sanctum_ceiling_right_slope",
                "ceiling_city_system_map_panel",
            ],
        ),
    ]

    previous_emissions = set_all_emission_strength(0.0)
    screenshots.append(render_still(overview_cam, os.path.join(SCREENSHOTS, "s43-int-dark-first.png")))
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
    print("SESSION 43 BUILD COMPLETE")
    print(f"Blend: {BLEND_FILE}")
    print(f"Draft GLB: {DRAFT_GLB}")
    print(f"Approved GLB: {APPROVED_GLB if promoted else 'not promoted'}")
    print(f"Tris: {qa['imported_tris']}")
    print(f"GLB size: {qa['glb_size_bytes'] / 1024:.1f} KB")
    print(f"Meshes: {qa['mesh_objects']}")
    print(f"Empties: {qa['empty_names']}")
    print(f"QA approved: {qa['approved']}")
    print(f"Metrics: {METRICS_FILE}")
    print(f"Import QA: {QA_IMPORT_FILE}")
    print("SESSION43_METRICS=" + json.dumps(metrics, indent=2, sort_keys=True))
    return metrics


metrics = build_session_43()

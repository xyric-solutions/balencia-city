"""
Balencia City v3 -- Module #08 Career
Session 31: Interior -- Executive Command Hub

Fresh Career interior scene for the approved tower-cluster exterior. Builds a
professional command hub with a growth-chart focal wall, advisor workstations,
focus booths, strategy table, skill trees, upper skybridge, runtime empties,
screenshots, metrics, and a draft GLB export.
"""

import json
import math
import os
from mathutils import Matrix, Vector

import bpy


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE_DIR = os.path.join(ROOT, "modules/08-career")
SHARED_DIR = os.path.join(ROOT, "shared")
DRAFTS_DIR = os.path.join(MODULE_DIR, "interior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")

BLEND_FILE = os.path.join(DRAFTS_DIR, "career-int-session31.blend")
DRAFT_GLB = os.path.join(DRAFTS_DIR, "career-int-draft-s31.glb")
METRICS_FILE = os.path.join(DRAFTS_DIR, "session31-metrics.json")

VALID_SLOTS = {"base", "accent", "glass", "detail", "emissive", "energy"}

os.makedirs(DRAFTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


def active_object():
    return getattr(bpy.context, "active_object", None) or bpy.context.view_layer.objects.active


def material_base_name(material):
    return material.name.split(".")[0] if material else "none"


def tri_count(obj):
    if obj.type != "MESH":
        return 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    count = sum(len(poly.vertices) - 2 for poly in mesh.polygons)
    eval_obj.to_mesh_clear()
    return count


def assign_mat(obj, slot):
    obj.data.materials.clear()
    obj.data.materials.append(MATS[slot])
    return obj


def apply_transforms(obj):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    return obj


def shade(obj):
    if obj.type != "MESH":
        return obj
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    obj.select_set(False)
    return obj


def make_box(name, loc, dims, slot, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rotation)
    obj = active_object()
    obj.name = name
    obj.scale = dims
    assign_mat(obj, slot)
    apply_transforms(obj)
    return obj


def make_cylinder(name, loc, radius, depth, slot, vertices=16, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=loc,
        rotation=rotation,
    )
    obj = active_object()
    obj.name = name
    assign_mat(obj, slot)
    apply_transforms(obj)
    shade(obj)
    return obj


def make_cone(name, loc, radius1, radius2, depth, slot, vertices=8, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        location=loc,
        rotation=rotation,
    )
    obj = active_object()
    obj.name = name
    assign_mat(obj, slot)
    apply_transforms(obj)
    shade(obj)
    return obj


def make_uv_sphere(name, loc, radius, slot, segments=10, rings=5):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        radius=radius,
        location=loc,
    )
    obj = active_object()
    obj.name = name
    assign_mat(obj, slot)
    apply_transforms(obj)
    shade(obj)
    return obj


def make_torus(name, loc, major_radius, minor_radius, slot, rotation=(0, 0, 0), major_segments=18, minor_segments=3):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=major_segments,
        minor_segments=minor_segments,
        location=loc,
        rotation=rotation,
    )
    obj = active_object()
    obj.name = name
    assign_mat(obj, slot)
    apply_transforms(obj)
    shade(obj)
    return obj


def make_cylinder_between(name, start, end, radius, slot, vertices=8):
    start_v = Vector(start)
    end_v = Vector(end)
    direction = end_v - start_v
    length = direction.length
    if length < 0.001:
        return None
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=(start_v + end_v) * 0.5)
    obj = active_object()
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign_mat(obj, slot)
    apply_transforms(obj)
    shade(obj)
    return obj


def cuboid_vertices(loc, dims, rot_z=0.0):
    x, y, z = dims[0] / 2, dims[1] / 2, dims[2] / 2
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


def make_box_mesh(name, boxes, slot):
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
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign_mat(obj, slot)
    return obj


def create_empty(name, loc, size=0.35):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=loc)
    obj = active_object()
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


def render_still(camera, path):
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = path
    bpy.context.scene.render.resolution_x = 1600
    bpy.context.scene.render.resolution_y = 1000
    bpy.context.scene.render.resolution_percentage = 100
    bpy.ops.render.render(write_still=True)
    return path


def render_still_with_hidden(camera, path, object_names):
    hidden = {}
    for name in object_names:
        obj = bpy.data.objects.get(name)
        if obj is None:
            continue
        hidden[obj.name] = obj.hide_render
        obj.hide_render = True
    try:
        return render_still(camera, path)
    finally:
        for name, was_hidden in hidden.items():
            obj = bpy.data.objects.get(name)
            if obj is not None:
                obj.hide_render = was_hidden


def set_all_emission_strength(value):
    previous = {}
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if not bsdf or "Emission Strength" not in bsdf.inputs:
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
    make_box("executive_command_floor_slab", (0, 0, 0.05), (11.2, 8.6, 0.10), "base")
    make_box("executive_command_back_wall_display_host", (0, 4.12, 2.78), (11.2, 0.18, 5.46), "base")
    make_box("executive_command_left_wall", (-5.58, 0, 2.78), (0.18, 8.6, 5.46), "base")
    make_box("executive_command_right_wall", (5.58, 0, 2.78), (0.18, 8.6, 5.46), "base")
    make_box("executive_command_ceiling_slab", (0, 0, 5.54), (11.2, 8.6, 0.12), "base")
    make_box("open_front_threshold_blue_floor_line", (0, -4.22, 0.14), (5.5, 0.08, 0.035), "accent")

    side_panel_boxes = []
    for side, x in [("left", -5.47), ("right", 5.47)]:
        for idx, y in enumerate([-2.65, -1.25, 0.15, 1.55, 2.95]):
            side_panel_boxes.append(((x, y, 2.75), (0.04, 0.76, 2.20), 0.0))
    make_box_mesh("side_wall_vertical_inactive_glass_panels", side_panel_boxes, "glass")

    path_boxes = []
    for idx, y in enumerate([-3.35, -2.20, -1.05, 0.10, 1.25, 2.40]):
        path_boxes.append(((0, y, 0.145), (0.13, 0.72, 0.035), 0.0))
    for x in [-3.65, -2.45, 2.45, 3.65]:
        path_boxes.append(((x, -1.55, 0.15), (0.86, 0.10, 0.035), 0.0))
    make_box_mesh("floor_embedded_directional_blue_path_strips", path_boxes, "emissive")


def build_growth_chart_wall():
    make_box("growth_chart_wall_glass_display_surface", (0, 3.98, 2.82), (9.72, 0.075, 2.95), "glass")
    make_box("growth_chart_wall_lower_dark_plinth", (0, 3.91, 1.19), (10.0, 0.16, 0.18), "detail")
    make_box("growth_chart_wall_upper_header_track", (0, 3.90, 4.38), (10.0, 0.13, 0.16), "accent")

    axis_boxes = []
    for x in [-4.15, -2.75, -1.35, 0.05, 1.45, 2.85, 4.25]:
        axis_boxes.append(((x, 3.85, 1.42), (0.045, 0.055, 0.25), 0.0))
    for z in [1.62, 2.02, 2.42, 2.82, 3.22, 3.62, 4.02]:
        axis_boxes.append(((-4.64, 3.85, z), (0.32, 0.055, 0.035), 0.0))
    make_box_mesh("growth_chart_wall_axis_ticks_and_scale_marks", axis_boxes, "detail")

    line_specs = [
        ("executive_path", -4.22, 1.54, 3.92, 4.02, 0.00),
        ("leadership_path", -4.00, 1.78, 4.18, 3.72, 0.55),
        ("skill_mastery_path", -4.36, 1.42, 4.04, 3.46, 1.05),
        ("network_growth_path", -4.10, 1.66, 3.78, 3.98, 1.75),
        ("opportunity_path", -4.46, 1.34, 4.34, 3.58, 2.35),
    ]
    for label, x0, z0, x1, z1, phase in line_specs:
        points = []
        for step in range(6):
            t = step / 5.0
            x = x0 + (x1 - x0) * t
            z = z0 + (z1 - z0) * t + math.sin(t * math.pi + phase) * 0.13
            points.append((x, 3.80, z))
        for idx in range(len(points) - 1):
            make_cylinder_between(
                f"growth_chart_{label}_ascending_segment_{idx:02d}",
                points[idx],
                points[idx + 1],
                0.026,
                "emissive",
                vertices=8,
            )
        for marker_idx in [1, 3, 5]:
            marker = points[marker_idx]
            make_uv_sphere(
                f"growth_chart_{label}_orange_milestone_marker_{marker_idx}",
                (marker[0], 3.735, marker[2]),
                0.115,
                "energy",
                segments=10,
                rings=5,
            )

    make_torus(
        "growth_chart_executive_goal_ring_marker",
        (4.22, 3.74, 4.02),
        0.28,
        0.018,
        "energy",
        rotation=(math.radians(90), 0, 0),
        major_segments=20,
        minor_segments=3,
    )
    make_box("growth_chart_wall_bottom_blue_status_bar", (0, 3.76, 1.34), (8.8, 0.052, 0.055), "emissive")


def build_advisor_workstations():
    stations = [
        ("left_front", -3.92, -2.75, math.radians(18)),
        ("left_mid", -3.92, -0.88, math.radians(4)),
        ("right_front", 3.92, -2.75, math.radians(-18)),
        ("right_mid", 3.92, -0.88, math.radians(-4)),
        ("center_rear", 0.0, 1.08, 0.0),
    ]
    for label, x, y, rot in stations:
        make_box(f"ai_career_advisor_{label}_standing_desk_pedestal", (x, y, 0.62), (0.44, 0.54, 1.04), "detail", rotation=(0, 0, rot))
        make_box(f"ai_career_advisor_{label}_thin_desk_surface", (x, y, 1.20), (0.92, 0.48, 0.08), "base", rotation=(0, 0, rot))
        make_box(f"ai_career_advisor_{label}_glass_projection_panel", (x, y + 0.18, 1.82), (1.02, 0.045, 0.74), "glass", rotation=(0, 0, rot))
        make_box(f"ai_career_advisor_{label}_blue_projection_header", (x, y + 0.16, 2.20), (0.78, 0.035, 0.052), "emissive", rotation=(0, 0, rot))
        make_cylinder(f"ai_career_advisor_{label}_voice_core_column", (x - 0.32, y - 0.10, 1.66), 0.07, 0.82, "accent", vertices=12)
        for tick in range(3):
            make_box(
                f"ai_career_advisor_{label}_trajectory_tick_{tick}",
                (x - 0.18 + tick * 0.20, y + 0.13, 1.68 + tick * 0.13),
                (0.18, 0.030, 0.030),
                "emissive",
                rotation=(0, 0, rot),
            )


def build_focus_booths():
    booth_specs = [
        ("left_focus_a", -4.86, 2.42, math.radians(0)),
        ("right_focus_a", 4.86, 2.42, math.radians(0)),
        ("left_focus_b", -4.86, 0.64, math.radians(0)),
    ]
    for label, x, y, rot in booth_specs:
        make_box(f"deep_focus_productivity_booth_{label}_rear_panel", (x, y + 0.54, 1.42), (1.00, 0.10, 2.54), "detail", rotation=(0, 0, rot))
        make_box(f"deep_focus_productivity_booth_{label}_left_cheek", (x - 0.53, y, 1.25), (0.10, 1.18, 2.18), "base", rotation=(0, 0, rot))
        make_box(f"deep_focus_productivity_booth_{label}_right_cheek", (x + 0.53, y, 1.25), (0.10, 1.18, 2.18), "base", rotation=(0, 0, rot))
        make_box(f"deep_focus_productivity_booth_{label}_floating_task_board", (x, y + 0.46, 1.86), (0.78, 0.046, 0.72), "glass", rotation=(0, 0, rot))
        task_boxes = []
        for row in range(4):
            task_boxes.append(((x - 0.18, y + 0.415, 1.62 + row * 0.15), (0.36, 0.030, 0.035), rot))
            task_boxes.append(((x + 0.25, y + 0.415, 1.62 + row * 0.15), (0.16, 0.030, 0.035), rot))
        make_box_mesh(f"deep_focus_productivity_booth_{label}_prioritized_task_items", task_boxes, "emissive")
        make_box(f"deep_focus_productivity_booth_{label}_seat_block", (x, y - 0.16, 0.60), (0.52, 0.50, 0.34), "detail", rotation=(0, 0, rot))


def build_strategy_table():
    make_cylinder("strategy_room_interactive_map_table_round_base", (0, 2.18, 0.76), 1.34, 0.18, "detail", vertices=32)
    make_cylinder("strategy_room_interactive_map_table_glass_surface", (0, 2.18, 0.90), 1.22, 0.07, "glass", vertices=32)
    make_torus("strategy_room_map_table_blue_perimeter_ring", (0, 2.18, 0.96), 1.18, 0.025, "emissive", major_segments=28, minor_segments=3)

    terrain_specs = [
        (-0.78, -0.12, 0.18),
        (-0.46, 0.26, 0.28),
        (-0.12, -0.30, 0.22),
        (0.18, 0.18, 0.42),
        (0.52, -0.18, 0.34),
        (0.78, 0.24, 0.24),
        (-0.18, 0.52, 0.30),
        (0.42, 0.54, 0.20),
    ]
    for idx, (dx, dy, height) in enumerate(terrain_specs):
        make_cone(
            f"strategy_room_market_terrain_peak_{idx:02d}",
            (dx, 2.18 + dy, 1.02 + height * 0.5),
            0.20,
            0.04,
            height,
            "energy" if idx in {1, 4} else "accent",
            vertices=6,
        )

    for idx, x in enumerate([-0.88, -0.44, 0.0, 0.44, 0.88]):
        make_cylinder_between(f"strategy_room_map_grid_x_{idx:02d}", (x, 1.18, 1.01), (x, 3.18, 1.01), 0.012, "emissive", vertices=6)
    for idx, y in enumerate([1.34, 1.76, 2.18, 2.60, 3.02]):
        make_cylinder_between(f"strategy_room_map_grid_y_{idx:02d}", (-1.00, y, 1.012), (1.00, y, 1.012), 0.012, "emissive", vertices=6)


def build_skill_growth_trees():
    tree_specs = [
        ("left", -2.55, 2.50),
        ("right", 2.55, 2.50),
        ("front", 0.0, -2.85),
    ]
    branch_dirs = [
        (-0.55, 0.10, 0.48),
        (0.55, 0.14, 0.58),
        (-0.42, -0.22, 0.78),
        (0.46, -0.18, 0.88),
        (-0.30, 0.26, 1.12),
        (0.32, 0.22, 1.24),
    ]
    for label, x, y in tree_specs:
        make_cylinder(f"skill_growth_tree_{label}_floor_base", (x, y, 0.22), 0.34, 0.18, "detail", vertices=18)
        make_cylinder(f"skill_growth_tree_{label}_vertical_trunk", (x, y, 1.60), 0.085, 2.70, "detail", vertices=12)
        make_torus(f"skill_growth_tree_{label}_mastery_orbit_ring", (x, y, 2.92), 0.48, 0.016, "accent", major_segments=18, minor_segments=3)
        for idx, (dx, dy, dz) in enumerate(branch_dirs):
            start_z = 1.08 + idx * 0.32
            start = (x, y, start_z)
            end = (x + dx, y + dy, start_z + dz)
            slot = "energy" if idx in {1, 4} else "accent"
            make_cylinder_between(f"skill_growth_tree_{label}_branch_{idx:02d}", start, end, 0.030, slot, vertices=8)
            make_uv_sphere(f"skill_growth_tree_{label}_mastery_node_{idx:02d}", end, 0.105, "emissive", segments=10, rings=5)


def build_upper_skybridge():
    make_box("upper_networking_skybridge_glass_walkway", (0, -0.26, 4.62), (6.70, 0.86, 0.34), "glass")
    make_box("upper_networking_skybridge_left_rail", (0, -0.76, 4.96), (6.86, 0.065, 0.18), "detail")
    make_box("upper_networking_skybridge_right_rail", (0, 0.24, 4.96), (6.86, 0.065, 0.18), "detail")
    for idx, x in enumerate([-2.7, -1.62, -0.54, 0.54, 1.62, 2.70]):
        make_box(f"upper_networking_skybridge_business_card_pulse_{idx:02d}", (x, -0.26, 5.04), (0.38, 0.045, 0.12), "energy" if idx % 2 else "emissive")
    for idx, x in enumerate([-3.24, -2.16, -1.08, 0.0, 1.08, 2.16, 3.24]):
        make_cylinder_between(
            f"upper_networking_skybridge_hanger_{idx:02d}",
            (x, -0.26, 4.76),
            (x, -0.26, 5.46),
            0.022,
            "detail",
            vertices=6,
        )


def build_runtime_empties():
    create_empty("light_0", (0.0, -0.20, 5.22), 0.50)
    create_empty("light_1", (0.0, 3.54, 3.18), 0.50)
    create_empty("light_2", (0.0, 2.18, 2.05), 0.46)
    create_empty("camera_target", (0.0, 2.72, 2.82), 0.58)


def group_for_object(name):
    if name.startswith(("executive_command", "open_front", "side_wall", "floor_embedded")):
        return "Room shell and floor guidance"
    if name.startswith("growth_chart"):
        return "Growth chart wall focal"
    if name.startswith("ai_career_advisor"):
        return "AI career advisor workstations"
    if name.startswith("deep_focus_productivity_booth"):
        return "Deep-focus productivity booths"
    if name.startswith("strategy_room"):
        return "Strategy table and market terrain"
    if name.startswith("skill_growth_tree"):
        return "Skill growth trees"
    if name.startswith("upper_networking_skybridge"):
        return "Upper skybridge interior"
    return "Other"


GROUP_EXPORT_PREFIX = {
    "Room shell and floor guidance": "executive_command_room_shell",
    "Growth chart wall focal": "growth_chart_wall",
    "AI career advisor workstations": "ai_career_advisor",
    "Deep-focus productivity booths": "deep_focus_productivity_booth",
    "Strategy table and market terrain": "strategy_room",
    "Skill growth trees": "skill_growth_tree",
    "Upper skybridge interior": "upper_networking_skybridge",
}


def consolidate_meshes_by_group_and_slot():
    """Reduce GLB object overhead while preserving material-slot boundaries."""
    buckets = {}
    for obj in [item for item in bpy.data.objects if item.type == "MESH"]:
        group = group_for_object(obj.name)
        if group == "Other":
            continue
        slot = material_base_name(obj.data.materials[0]) if obj.data.materials else "none"
        if slot not in VALID_SLOTS:
            continue
        buckets.setdefault((group, slot), []).append(obj)

    for (group, slot), objs in sorted(buckets.items()):
        if len(objs) < 2:
            continue
        bpy.ops.object.select_all(action="DESELECT")
        active = objs[0]
        for obj in objs:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = active
        bpy.ops.object.join()
        joined = bpy.context.view_layer.objects.active
        prefix = GROUP_EXPORT_PREFIX[group]
        joined.name = f"{prefix}_{slot}_joined"
        joined.data.name = joined.name + "_mesh"
        apply_transforms(joined)


def collect_metrics(screenshots):
    material_issues = []
    slot_tris = {}
    object_groups = {}
    objects = []
    for obj in sorted((item for item in bpy.data.objects if item.type == "MESH"), key=lambda item: item.name):
        if not obj.data.materials:
            material_issues.append(f"{obj.name}: no material")
            slot = "none"
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
    return {
        "session": 31,
        "module": "08-career",
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
        "screenshots": screenshots,
    }


def bake_mesh_transforms_for_export():
    for obj in [item for item in bpy.data.objects if item.type == "MESH"]:
        obj.data.transform(obj.matrix_world.copy())
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)
        obj.parent = None


def export_draft_glb(metrics):
    bake_mesh_transforms_for_export()

    root = bpy.data.objects.new("career-int", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.1
    for obj in list(bpy.data.objects):
        if obj == root:
            continue
        if obj.type in {"MESH", "EMPTY"} and obj.parent is None and not obj.name.startswith("S31_"):
            obj.parent = root

    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        selected = obj.type in {"MESH", "EMPTY"} and not obj.name.startswith("S31_")
        obj.select_set(selected)

    active_candidate = next((obj for obj in bpy.data.objects if obj.type == "MESH" and obj.select_get()), None)
    if active_candidate is not None:
        bpy.context.view_layer.objects.active = active_candidate

    if not hasattr(bpy.context, "active_object"):
        try:
            setattr(type(bpy.context), "active_object", property(lambda context: context.view_layer.objects.active))
        except Exception as exc:
            print(f"Could not add active_object context shim: {exc}")

    if getattr(bpy.context, "window", None) is None:
        class ExportWindowShim:
            def __init__(self, scene):
                self.scene = scene

            def cursor_set(self, _value):
                return None

        window_shim = ExportWindowShim(bpy.context.scene)
        original_context = bpy.context

        class ExportContextProxy:
            def __init__(self, context, window):
                object.__setattr__(self, "_context", context)
                object.__setattr__(self, "window", window)

            def __getattr__(self, name):
                if name == "active_object":
                    return self._context.view_layer.objects.active
                return getattr(self._context, name)

            def __setattr__(self, name, value):
                if name == "window":
                    object.__setattr__(self, name, value)
                else:
                    setattr(self._context, name, value)

        try:
            setattr(type(bpy.context), "window", property(lambda _context: window_shim))
        except Exception as exc:
            print(f"Could not add window context shim: {exc}")
        try:
            bpy.context = ExportContextProxy(original_context, window_shim)
        except Exception as exc:
            print(f"Could not add bpy.context proxy: {exc}")

    try:
        import io_scene_gltf2.blender.exp.export as gltf_export

        gltf_export.__notify_start = lambda context, export_settings: None
        gltf_export.__notify_end = lambda context, elapsed, export_settings: None
    except Exception as exc:
        print(f"Could not patch glTF export notifications: {exc}")

    bpy.ops.export_scene.gltf(
        filepath=DRAFT_GLB,
        export_format="GLB",
        use_selection=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_extras=True,
    )
    metrics["glb_size_bytes"] = os.path.getsize(DRAFT_GLB)
    return metrics


def build_session_31():
    print("=== Session 31: Career Interior ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    lighting = load_python_module(os.path.join(SHARED_DIR, "lighting-rig.py"), "lighting_rig_s31")
    lighting["clear_lighting"]()
    lighting["setup_viewport_lighting"]()

    material_library = load_python_module(os.path.join(SHARED_DIR, "material-library.py"), "material_library_s31")
    global MATS
    MATS = material_library["create_materials"]("#3B82F6", include_energy=True, include_holo=False)

    interior_lighting = load_python_module(os.path.join(SHARED_DIR, "interior-lighting-rig.py"), "interior_lighting_s31")
    interior_lighting["setup_interior_lighting"](focal_point=(0, 2.72, 2.82), floor_z=0.0, ceiling_z=5.6, radius=5.4)
    interior_lighting["boost_emissions_for_preview"]()

    build_room_shell()
    build_growth_chart_wall()
    build_advisor_workstations()
    build_focus_booths()
    build_strategy_table()
    build_skill_growth_trees()
    build_upper_skybridge()
    build_runtime_empties()
    consolidate_meshes_by_group_and_slot()

    overview_cam = make_camera("S31_Interior_Overview_Camera", (7.7, -8.9, 5.8), (0, 1.20, 2.70), lens=31)
    entry_cam = make_camera("S31_Interior_Entry_Camera", (0.0, -8.95, 2.72), (0, 2.72, 2.82), lens=34)
    focal_cam = make_camera("S31_Interior_Focal_Growth_Chart_Camera", (2.75, -4.80, 3.42), (0, 3.12, 2.92), lens=38)
    top_cam = make_camera("S31_Interior_Topdown_Camera", (0.0, -0.20, 10.7), (0, 0.2, 0.18), lens=43)

    screenshots = [
        render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s31-int-overview.png")),
        render_still(entry_cam, os.path.join(SCREENSHOTS_DIR, "s31-int-from-entry.png")),
        render_still(focal_cam, os.path.join(SCREENSHOTS_DIR, "s31-int-focal-growth-chart.png")),
        render_still_with_hidden(
            top_cam,
            os.path.join(SCREENSHOTS_DIR, "s31-int-topdown.png"),
            ["executive_command_room_shell_base_joined"],
        ),
    ]

    previous_emissions = set_all_emission_strength(0.0)
    screenshots.append(render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s31-int-dark-first.png")))
    restore_emission_strength(previous_emissions)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    metrics = collect_metrics([os.path.relpath(path, MODULE_DIR) for path in screenshots])
    metrics = export_draft_glb(metrics)
    with open(METRICS_FILE, "w") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)

    print("=" * 70)
    print("SESSION 31 BUILD COMPLETE")
    print(f"Blend: {BLEND_FILE}")
    print(f"Draft GLB: {DRAFT_GLB}")
    print(f"GLB size: {metrics['glb_size_bytes'] / 1024:.1f} KB")
    print(f"Tris: {metrics['total_tris']}")
    print(f"Meshes: {metrics['mesh_objects']}")
    print(f"Empties: {metrics['empty_names']}")
    print(f"Metrics: {METRICS_FILE}")
    print("SESSION31_METRICS=" + json.dumps(metrics, indent=2, sort_keys=True))
    return metrics


metrics = build_session_31()

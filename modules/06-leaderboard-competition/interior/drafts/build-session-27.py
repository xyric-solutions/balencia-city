"""
Balencia City v3 -- Module #06 Leaderboard & Competition
Session 27: Interior -- Competition Floor

Fresh interior scene for the approved arena exterior. Builds a bowl-shaped
competition floor with a central holographic leaderboard, required support props,
runtime empties, screenshots, metrics, and a draft GLB export.
"""

import json
import math
import os
from mathutils import Matrix, Vector

import bpy


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE_DIR = os.path.join(ROOT, "modules/06-leaderboard-competition")
SHARED_DIR = os.path.join(ROOT, "shared")
DRAFTS_DIR = os.path.join(MODULE_DIR, "interior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")

BLEND_FILE = os.path.join(DRAFTS_DIR, "leaderboard-competition-int-session27.blend")
DRAFT_GLB = os.path.join(DRAFTS_DIR, "leaderboard-int-draft-s27.glb")
METRICS_FILE = os.path.join(DRAFTS_DIR, "session27-metrics.json")

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


def make_cylinder(name, loc, radius, depth, slot, vertices=32, rotation=(0, 0, 0)):
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


def make_cone(name, loc, radius1, radius2, depth, slot, vertices=16, rotation=(0, 0, 0)):
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


def make_uv_sphere(name, loc, radius, slot, segments=16, rings=8):
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


def make_torus(name, loc, major_radius, minor_radius, slot, rotation=(0, 0, 0), major_segments=32, minor_segments=3):
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


def make_mesh(name, verts, faces, slot):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign_mat(obj, slot)
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


def box_mesh(name, boxes, slot):
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
    return make_mesh(name, verts, faces, slot)


def make_annular_band(name, inner_r, outer_r, z0, z1, start_deg, end_deg, slot, segments=36, closed=False):
    start = math.radians(start_deg)
    end = math.radians(end_deg)
    points = segments if closed else segments + 1
    verts = []
    for i in range(points):
        t = i / segments
        angle = start + (end - start) * t
        co = math.cos(angle)
        si = math.sin(angle)
        verts.extend(
            [
                (outer_r * co, outer_r * si, z0),
                (outer_r * co, outer_r * si, z1),
                (inner_r * co, inner_r * si, z1),
                (inner_r * co, inner_r * si, z0),
            ]
        )
    faces = []
    face_segments = segments if closed else segments
    for i in range(face_segments):
        j = (i + 1) % points
        a = i * 4
        b = j * 4
        faces.append((a + 0, b + 0, b + 1, a + 1))
        faces.append((a + 1, b + 1, b + 2, a + 2))
        faces.append((a + 2, b + 2, b + 3, a + 3))
        faces.append((a + 3, b + 3, b + 0, a + 0))
    if not closed:
        faces.append((0, 1, 2, 3))
        n = segments * 4
        faces.append((n + 3, n + 2, n + 1, n + 0))
    return make_mesh(name, verts, faces, slot)


def polar_box(angle_deg, radius, z, dims, rot_extra=math.pi / 2):
    angle = math.radians(angle_deg)
    loc = (math.cos(angle) * radius, math.sin(angle) * radius, z)
    return loc, dims, angle + rot_extra


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
    data.clip_end = 180
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
    make_cylinder("competition_floor_disc", (0, 0, 0.08), 6.2, 0.16, "base", vertices=48)
    make_cylinder("central_competition_platform", (0, 0, 0.23), 1.55, 0.18, "detail", vertices=36)
    make_torus("floor_outer_service_ring", (0, 0, 0.20), 5.95, 0.035, "detail", major_segments=40, minor_segments=3)
    make_torus("floor_inner_challenge_ring", (0, 0, 0.30), 2.25, 0.026, "accent", major_segments=32, minor_segments=3)
    make_torus("floor_energy_target_ring", (0, 0, 0.32), 1.12, 0.024, "energy", major_segments=32, minor_segments=3)

    for row in range(5):
        inner = 2.72 + row * 0.56
        outer = inner + 0.38
        z0 = 0.42 + row * 0.34
        z1 = z0 + 0.16
        make_annular_band(
            f"tiered_seating_row_{row:02d}_concentric_bowl",
            inner,
            outer,
            z0,
            z1,
            0,
            360,
            "detail",
            segments=28,
            closed=True,
        )

        tick_boxes = []
        for idx in range(14):
            angle = idx * (360.0 / 14.0) + row * 2.0
            if 247 <= angle <= 293:
                continue
            tick_boxes.append(polar_box(angle, inner + 0.17, z1 + 0.075, (0.16, 0.05, 0.075)))
        box_mesh(f"tiered_seating_row_{row:02d}_seat_markers", tick_boxes, "accent" if row % 2 == 0 else "detail")

    wall_boxes = []
    glass_boxes = []
    for idx, angle_deg in enumerate([-160, -135, -25, 0, 25, 50, 75, 100, 125, 150, 180, 205]):
        angle = math.radians(angle_deg)
        rot = angle + math.pi / 2
        wall_boxes.append(((math.cos(angle) * 6.27, math.sin(angle) * 6.27, 3.22), (1.25, 0.14, 6.35), rot))
        if idx % 2 == 0:
            glass_boxes.append(((math.cos(angle) * 6.18, math.sin(angle) * 6.18, 3.42), (0.70, 0.045, 2.60), rot))
    box_mesh("arena_interior_curved_wall_panels_with_front_gap", wall_boxes, "base")
    box_mesh("arena_interior_inactive_display_slits", glass_boxes, "glass")

    make_torus("open_sky_ceiling_rim_aperture", (0, 0, 6.56), 5.82, 0.075, "detail", major_segments=40, minor_segments=3)
    make_annular_band("rear_partial_ceiling_canopy_back_half", 4.15, 6.10, 6.38, 6.50, -10, 190, "base", segments=24)
    make_torus("ceiling_inner_rank_orbit_track", (0, 0, 6.34), 2.30, 0.038, "accent", major_segments=32, minor_segments=3)

    for idx, angle_deg in enumerate([0, 36, 72, 108, 144, 180]):
        angle = math.radians(angle_deg)
        make_cylinder_between(
            f"overhead_open_sky_truss_{idx:02d}",
            (math.cos(angle) * 2.42, math.sin(angle) * 2.42, 6.32),
            (math.cos(angle) * 5.78, math.sin(angle) * 5.78, 6.48),
            0.033,
            "detail",
            vertices=8,
        )

    make_cylinder_between("front_open_wall_left_guard_rail", (-5.05, -3.52, 1.05), (-2.25, -5.72, 1.05), 0.045, "detail")
    make_cylinder_between("front_open_wall_right_guard_rail", (5.05, -3.52, 1.05), (2.25, -5.72, 1.05), 0.045, "detail")
    make_cylinder_between("front_open_wall_coral_threshold", (-2.10, -5.72, 0.32), (2.10, -5.72, 0.32), 0.035, "accent")


def build_central_leaderboard():
    make_cylinder("central_holographic_leaderboard_cylinder", (0, 0, 3.22), 1.24, 5.86, "glass", vertices=48)
    make_cylinder("leaderboard_dark_inner_core_shadow", (0, 0, 3.22), 0.18, 5.40, "base", vertices=16)

    for idx, z in enumerate([0.92, 1.78, 2.64, 3.50, 4.36, 5.22]):
        slot = "emissive" if idx % 2 == 0 else "energy"
        make_torus(f"leaderboard_cylindrical_rank_ring_{idx:02d}", (0, 0, z), 1.26, 0.026, slot, major_segments=32, minor_segments=3)

    rank_boxes = []
    score_boxes = []
    for row in range(8):
        z = 1.04 + row * 0.51
        for col in range(5):
            angle = -68 + col * 11.0 + row * 1.2
            rank_boxes.append(polar_box(angle, 1.31, z, (0.16, 0.035, 0.105)))
        for col in range(4):
            angle = 10 + col * 13.5 - row * 0.8
            score_boxes.append(polar_box(angle, 1.32, z + 0.045, (0.22 + col * 0.06, 0.035, 0.050)))
    box_mesh("leaderboard_rank_position_glyph_columns", rank_boxes, "emissive")
    box_mesh("leaderboard_score_shift_bar_geometry", score_boxes, "accent")

    make_cone("leaderboard_upward_rank_arrow", (0, -1.35, 4.78), 0.20, 0.03, 0.56, "energy", vertices=3, rotation=(math.radians(90), 0, math.radians(30)))
    make_cone("leaderboard_downward_rank_arrow", (0.72, -1.12, 2.18), 0.18, 0.03, 0.46, "emissive", vertices=3, rotation=(math.radians(-90), 0, math.radians(30)))

    for idx, angle_deg in enumerate([20, 82, 143, 205, 264, 322]):
        angle = math.radians(angle_deg)
        radius = 2.18 + 0.15 * (idx % 2)
        z = 2.10 + 0.45 * (idx % 4)
        make_box(
            f"orbiting_challenge_card_{idx:02d}",
            (math.cos(angle) * radius, math.sin(angle) * radius, z),
            (0.80, 0.045, 0.46),
            "glass",
            rotation=(0, 0, angle + math.pi / 2),
        )
        make_box(
            f"orbiting_challenge_card_{idx:02d}_coral_header",
            (math.cos(angle) * radius, math.sin(angle) * radius, z + 0.19),
            (0.64, 0.035, 0.045),
            "emissive",
            rotation=(0, 0, angle + math.pi / 2),
        )


def build_support_props():
    for idx in range(10):
        angle = idx * math.tau / 10.0 + math.radians(8)
        radius = 4.85
        height = 1.45 + (idx % 5) * 0.38 + (0.18 if idx in {2, 7} else 0)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        make_cylinder(f"achievement_tower_{idx:02d}_pillar", (x, y, 0.34 + height * 0.5), 0.13, height, "detail", vertices=14)
        make_cylinder(f"achievement_tower_{idx:02d}_glow_cap", (x, y, 0.42 + height), 0.18, 0.15, "emissive", vertices=14)
        make_cylinder_between(
            f"achievement_tower_{idx:02d}_vertical_energy_strip",
            (x, y, 0.62),
            (x, y, 0.20 + height),
            0.028,
            "energy" if idx % 3 == 0 else "accent",
            vertices=6,
        )

    h2h_pairs = [("north", 1.55), ("south", -1.70)]
    for label, y in h2h_pairs:
        for side, x in [("left", -2.35), ("right", 2.35)]:
            make_torus(f"head_to_head_zone_{label}_{side}_circle", (x, y, 0.35), 0.53, 0.025, "accent", major_segments=24, minor_segments=3)
        make_cylinder_between(f"head_to_head_zone_{label}_challenge_line", (-1.82, y, 0.36), (1.82, y, 0.36), 0.028, "energy", vertices=8)

    platform_specs = [
        ("west", -3.35, 0.15, math.radians(90)),
        ("east", 3.35, 0.15, math.radians(90)),
    ]
    for label, x, y, rot in platform_specs:
        make_box(f"team_challenge_platform_{label}_raised_deck", (x, y, 0.44), (1.05, 2.05, 0.22), "detail", rotation=(0, 0, rot))
        make_box(f"team_challenge_platform_{label}_center_score_strip", (x, y, 0.61), (0.13, 1.72, 0.055), "emissive", rotation=(0, 0, rot))
        for side in [-1, 1]:
            for seat in range(5):
                sy = y - 0.78 + seat * 0.39
                sx = x + side * 0.54
                make_box(
                    f"team_challenge_platform_{label}_seat_{'a' if side < 0 else 'b'}_{seat}",
                    (sx, sy, 0.74),
                    (0.20, 0.22, 0.12),
                    "base",
                    rotation=(0, 0, 0),
                )

    blooms = [("north_west", -2.88, 2.72, 2.25), ("south_east", 2.78, -2.48, 2.52)]
    for label, x, y, z in blooms:
        make_uv_sphere(f"milestone_light_bloom_{label}_core", (x, y, z), 0.23, "energy", segments=12, rings=6)
        make_torus(f"milestone_light_bloom_{label}_outer_wave", (x, y, z), 0.48, 0.018, "emissive", major_segments=24, minor_segments=3)
        make_torus(
            f"milestone_light_bloom_{label}_tilted_wave",
            (x, y, z),
            0.62,
            0.015,
            "accent",
            rotation=(math.radians(62), 0, math.radians(22)),
            major_segments=24,
            minor_segments=3,
        )

    stair_specs = [("left", -4.05, -2.82, math.radians(20)), ("right", 4.05, 2.82, math.radians(200))]
    for label, x, y, rot in stair_specs:
        for step in range(5):
            offset = (step - 2) * 0.28
            make_box(
                f"progression_monument_{label}_ascending_step_{step}",
                (x + math.cos(rot) * offset, y + math.sin(rot) * offset, 0.38 + step * 0.12),
                (0.46 + step * 0.08, 0.22, 0.18 + step * 0.05),
                "accent" if step >= 3 else "detail",
                rotation=(0, 0, rot),
            )
        make_cylinder_between(
            f"progression_monument_{label}_energy_spine",
            (x - math.cos(rot) * 0.70, y - math.sin(rot) * 0.70, 0.58),
            (x + math.cos(rot) * 0.70, y + math.sin(rot) * 0.70, 1.22),
            0.026,
            "energy",
            vertices=6,
        )


def build_runtime_empties():
    create_empty("light_0", (0, 0, 6.92), 0.48)
    create_empty("light_1", (0, 1.85, 3.52), 0.46)
    create_empty("light_2", (3.95, 2.75, 2.35), 0.46)
    create_empty("camera_target", (0, 0, 3.25), 0.58)


def group_for_object(name):
    if name.startswith(("competition_floor", "central_competition", "floor_", "arena_interior", "open_sky", "rear_partial", "ceiling_", "overhead_", "front_open")):
        return "Room shell, tiered seating, and open-sky rim"
    if name.startswith(("central_holographic", "leaderboard_")):
        return "Central holographic leaderboard focal"
    if name.startswith("achievement_tower"):
        return "Achievement towers"
    if name.startswith("head_to_head"):
        return "Head-to-head competition zones"
    if name.startswith("team_challenge"):
        return "Team challenge platforms and seats"
    if name.startswith("orbiting_challenge"):
        return "Orbiting challenge cards"
    if name.startswith("milestone_light"):
        return "Milestone light bloom emitters"
    if name.startswith("progression_monument"):
        return "Progression monuments"
    if name.startswith("tiered_seating"):
        return "Room shell, tiered seating, and open-sky rim"
    return "Other"


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
        "session": 27,
        "module": "06-leaderboard-competition",
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

    root = bpy.data.objects.new("leaderboard-int", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.1
    for obj in list(bpy.data.objects):
        if obj == root:
            continue
        if obj.type in {"MESH", "EMPTY"} and obj.parent is None and not obj.name.startswith("S27_"):
            obj.parent = root

    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        selected = obj.type in {"MESH", "EMPTY"} and not obj.name.startswith("S27_")
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

    export_kwargs = {
        "filepath": DRAFT_GLB,
        "export_format": "GLB",
        "use_selection": True,
        "export_draco_mesh_compression_enable": True,
        "export_draco_mesh_compression_level": 6,
        "export_yup": True,
        "export_cameras": False,
        "export_lights": False,
        "export_extras": True,
    }
    bpy.ops.export_scene.gltf(**export_kwargs)
    metrics["glb_size_bytes"] = os.path.getsize(DRAFT_GLB)
    return metrics


def build_session_27():
    print("=== Session 27: Leaderboard Competition Interior ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    lighting = load_python_module(os.path.join(SHARED_DIR, "lighting-rig.py"), "lighting_rig_s27")
    lighting["clear_lighting"]()
    lighting["setup_viewport_lighting"]()

    material_library = load_python_module(os.path.join(SHARED_DIR, "material-library.py"), "material_library_s27")
    global MATS
    MATS = material_library["create_materials"]("#FB7185", include_energy=True, include_holo=False)

    interior_lighting = load_python_module(os.path.join(SHARED_DIR, "interior-lighting-rig.py"), "interior_lighting_s27")
    interior_lighting["setup_interior_lighting"](focal_point=(0, 0, 3.3), floor_z=0.0, ceiling_z=6.7, radius=6.2)
    interior_lighting["boost_emissions_for_preview"]()

    build_room_shell()
    build_central_leaderboard()
    build_support_props()
    build_runtime_empties()

    overview_cam = make_camera("S27_Interior_Overview_Camera", (7.8, -8.8, 6.6), (0, 0, 3.15), lens=32)
    entry_cam = make_camera("S27_Interior_Entry_Camera", (0, -8.8, 3.15), (0, 0, 3.20), lens=34)
    top_cam = make_camera("S27_Interior_Topdown_Camera", (0, -0.35, 12.8), (0, 0, 0.25), lens=42)
    focal_cam = make_camera("S27_Interior_Focal_Camera", (3.8, -4.8, 4.6), (0, 0, 3.25), lens=40)

    screenshots = [
        render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s27-int-overview.png")),
        render_still(entry_cam, os.path.join(SCREENSHOTS_DIR, "s27-int-from-entry.png")),
        render_still(top_cam, os.path.join(SCREENSHOTS_DIR, "s27-int-topdown.png")),
        render_still(focal_cam, os.path.join(SCREENSHOTS_DIR, "s27-int-focal-leaderboard.png")),
    ]

    previous_emissions = set_all_emission_strength(0.0)
    screenshots.append(render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s27-int-dark-first.png")))
    restore_emission_strength(previous_emissions)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    metrics = collect_metrics([os.path.relpath(path, MODULE_DIR) for path in screenshots])
    metrics = export_draft_glb(metrics)
    with open(METRICS_FILE, "w") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)

    print("=" * 70)
    print("SESSION 27 BUILD COMPLETE")
    print(f"Blend: {BLEND_FILE}")
    print(f"Draft GLB: {DRAFT_GLB}")
    print(f"GLB size: {metrics['glb_size_bytes'] / 1024:.1f} KB")
    print(f"Tris: {metrics['total_tris']}")
    print(f"Meshes: {metrics['mesh_objects']}")
    print(f"Empties: {metrics['empty_names']}")
    print(f"Metrics: {METRICS_FILE}")
    print("SESSION27_METRICS=" + json.dumps(metrics, indent=2, sort_keys=True))
    return metrics


metrics = build_session_27()

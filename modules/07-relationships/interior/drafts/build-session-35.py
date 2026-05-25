"""
Balencia City v3 -- Module #07 Relationships
Session 35: Interior -- Connection Gardens

Fresh Relationships interior scene for the approved low garden exterior. Builds
the family bonding dome focal point, winding rose paths, insight benches, trust
vines, memory timeline moments, empathy alcoves, planter beds, runtime empties,
screenshots, metrics, and a draft GLB export.
"""

import json
import math
import os
from mathutils import Matrix, Vector

import bpy


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE_DIR = os.path.join(ROOT, "modules/07-relationships")
SHARED_DIR = os.path.join(ROOT, "shared")
DRAFTS_DIR = os.path.join(MODULE_DIR, "interior", "drafts")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")

BLEND_FILE = os.path.join(DRAFTS_DIR, "relationships-int-session35.blend")
DRAFT_GLB = os.path.join(DRAFTS_DIR, "relationships-int-draft-s35.glb")
METRICS_FILE = os.path.join(DRAFTS_DIR, "session35-metrics.json")

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


def make_ellipse_cylinder(name, loc, rx, ry, depth, slot, vertices=36, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=1.0,
        depth=depth,
        location=loc,
        rotation=rotation,
    )
    obj = active_object()
    obj.name = name
    obj.scale = (rx, ry, 1.0)
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


def make_scaled_uv_sphere(name, loc, scale, slot, segments=12, rings=6, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        radius=1.0,
        location=loc,
        rotation=rotation,
    )
    obj = active_object()
    obj.name = name
    obj.scale = scale
    assign_mat(obj, slot)
    apply_transforms(obj)
    shade(obj)
    return obj


def make_torus(name, loc, major_radius, minor_radius, slot, rotation=(0, 0, 0), major_segments=24, minor_segments=4):
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


def make_hemisphere(name, center, radius, slot, segments=32, rings=8):
    cx, cy, cz = center
    verts = [(cx, cy, cz + radius)]
    for ring in range(1, rings + 1):
        phi = (math.pi / 2.0) * ring / rings
        r = math.sin(phi) * radius
        z = cz + math.cos(phi) * radius
        for idx in range(segments):
            angle = math.tau * idx / segments
            verts.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r, z))

    faces = []
    for idx in range(segments):
        faces.append((0, 1 + idx, 1 + ((idx + 1) % segments)))
    for ring in range(1, rings):
        start = 1 + (ring - 1) * segments
        next_start = 1 + ring * segments
        for idx in range(segments):
            faces.append((start + idx, start + ((idx + 1) % segments), next_start + ((idx + 1) % segments), next_start + idx))
    obj = make_mesh(name, verts, faces, slot)
    shade(obj)
    return obj


def ribbon_from_points(name, points, width, slot):
    verts = []
    faces = []
    vectors = [Vector(point) for point in points]
    for idx, point in enumerate(vectors):
        if idx == 0:
            tangent = vectors[1] - point
        elif idx == len(vectors) - 1:
            tangent = point - vectors[idx - 1]
        else:
            tangent = vectors[idx + 1] - vectors[idx - 1]
        if tangent.length < 0.001:
            tangent = Vector((0, 1, 0))
        tangent.normalize()
        perp = Vector((-tangent.y, tangent.x, 0))
        if perp.length < 0.001:
            perp = Vector((1, 0, 0))
        perp.normalize()
        verts.append(tuple(point + perp * width * 0.5))
        verts.append(tuple(point - perp * width * 0.5))
    for idx in range(len(vectors) - 1):
        a = idx * 2
        faces.append((a, a + 1, a + 3, a + 2))
    return make_mesh(name, verts, faces, slot)


def ellipse_arc_points(rx, ry, start_deg, end_deg, z, segments, y_offset=0.0):
    points = []
    for idx in range(segments + 1):
        t = idx / segments
        angle = math.radians(start_deg + (end_deg - start_deg) * t)
        points.append((math.cos(angle) * rx, math.sin(angle) * ry + y_offset, z))
    return points


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
    make_ellipse_cylinder("connection_garden_room_shell_elliptical_floor_slab", (0, 0, 0.06), 6.35, 5.15, 0.12, "base", vertices=48)
    make_ellipse_cylinder("connection_garden_room_shell_low_inner_garden_floor", (0, -0.05, 0.145), 4.92, 3.78, 0.035, "detail", vertices=48)
    make_ellipse_cylinder("connection_garden_room_shell_ceiling_canopy", (0, 0.22, 5.36), 6.18, 4.88, 0.12, "base", vertices=48)
    make_ellipse_cylinder("connection_garden_room_shell_warm_glass_skylight", (0, 0.08, 5.45), 2.18, 1.62, 0.035, "glass", vertices=36)
    make_torus("connection_garden_room_shell_skylight_rose_trim", (0, 0.08, 5.49), 1.84, 0.026, "accent", major_segments=32, minor_segments=3)
    make_box("connection_garden_room_shell_open_front_threshold", (0, -5.02, 0.20), (3.7, 0.10, 0.055), "accent")

    wall_boxes = []
    glass_boxes = []
    for idx, angle_deg in enumerate(range(25, 156, 10)):
        angle = math.radians(angle_deg)
        x = math.cos(angle) * 6.25
        y = math.sin(angle) * 5.02
        rot = angle + math.pi / 2
        wall_boxes.append(((x, y, 2.72), (0.82, 0.15, 5.16), rot))
        if idx % 2 == 0:
            glass_boxes.append(((math.cos(angle) * 6.05, math.sin(angle) * 4.86, 2.95), (0.48, 0.045, 2.56), rot))
    box_mesh("connection_garden_room_shell_curved_back_and_side_wall_panels", wall_boxes, "base")
    box_mesh("connection_garden_room_shell_warm_window_slits", glass_boxes, "glass")

    rib_points = []
    for angle_deg in [30, 48, 66, 84, 102, 120, 138, 156]:
        angle = math.radians(angle_deg)
        rib_points.append(((math.cos(angle) * 1.95, math.sin(angle) * 1.55, 5.46), (math.cos(angle) * 5.88, math.sin(angle) * 4.64, 5.40), angle))
    for idx, (start, end, angle) in enumerate(rib_points):
        make_cylinder_between(f"connection_garden_room_shell_ceiling_garden_rib_{idx:02d}", start, end, 0.026, "detail", vertices=8)


def box_mesh(name, boxes, slot):
    verts = []
    faces = []
    for loc, dims, rot_z in boxes:
        x, y, z = dims[0] / 2.0, dims[1] / 2.0, dims[2] / 2.0
        base = Vector(loc)
        rot = Matrix.Rotation(rot_z, 4, "Z")
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
        idx = len(verts)
        verts.extend([tuple(base + rot @ corner) for corner in corners])
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


def build_family_bonding_dome():
    make_ellipse_cylinder("family_bonding_dome_dark_garden_plinth", (0, 0, 0.23), 2.12, 1.92, 0.20, "detail", vertices=36)
    make_torus("family_bonding_dome_rose_base_ring", (0, 0, 0.39), 1.82, 0.045, "emissive", major_segments=28, minor_segments=3)
    make_hemisphere("family_bonding_dome_transparent_glass_shell", (0, 0, 0.38), 1.84, "glass", segments=28, rings=6)
    make_torus("family_bonding_dome_upper_soft_crown_ring", (0, 0, 1.90), 0.72, 0.022, "accent", major_segments=20, minor_segments=3)

    people = []
    for idx, angle_deg in enumerate([-120, -38, 32, 112, 180]):
        angle = math.radians(angle_deg)
        pos = (math.cos(angle) * 0.82, math.sin(angle) * 0.64, 0.86)
        people.append(pos)
        make_uv_sphere(f"family_bonding_dome_connection_node_{idx:02d}", pos, 0.115, "emissive", segments=8, rings=4)
        make_cylinder(f"family_bonding_dome_low_seat_{idx:02d}", (pos[0], pos[1], 0.50), 0.20, 0.20, "detail", vertices=8)
    center = (0, 0, 1.22)
    make_uv_sphere("family_bonding_dome_heart_core", center, 0.18, "energy", segments=10, rings=5)
    for idx, pos in enumerate(people):
        make_cylinder_between(f"family_bonding_dome_core_thread_{idx:02d}", pos, center, 0.024, "emissive", vertices=6)
    for idx, (a, b) in enumerate([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 3)]):
        make_cylinder_between(f"family_bonding_dome_bond_strength_thread_{idx:02d}", people[a], people[b], 0.016, "energy" if idx % 2 else "emissive", vertices=5)


def build_walking_paths():
    paths = [
        ("rose_energy_path_entry_to_dome", [(0, -4.80, 0.235), (-0.62, -3.50, 0.24), (-0.36, -2.22, 0.245), (0, -1.78, 0.245)], 0.54, "detail"),
        ("rose_energy_path_left_memory_curve", ellipse_arc_points(3.95, 3.05, 204, 92, 0.255, 30), 0.40, "detail"),
        ("rose_energy_path_right_memory_curve", ellipse_arc_points(3.95, 3.05, -24, 88, 0.26, 30), 0.40, "detail"),
        ("rose_energy_path_perimeter_loop", ellipse_arc_points(5.35, 4.24, 25, 155, 0.265, 36), 0.30, "detail"),
    ]
    for name, points, width, slot in paths:
        ribbon_from_points(name, points, width, slot)

    glow_paths = [
        ("rose_energy_path_entry_glow_thread", [(0, -4.82, 0.315), (-0.42, -3.48, 0.32), (-0.20, -2.16, 0.325), (0, -1.86, 0.33)]),
        ("rose_energy_path_left_glow_thread", ellipse_arc_points(3.48, 2.66, 206, 94, 0.335, 28)),
        ("rose_energy_path_right_glow_thread", ellipse_arc_points(3.48, 2.66, -26, 86, 0.335, 28)),
    ]
    for name, points in glow_paths:
        ribbon_from_points(name, points, 0.075, "emissive")


def build_ai_insight_benches():
    bench_specs = [
        ("front_left", -2.40, -2.88, math.radians(22)),
        ("front_right", 2.40, -2.88, math.radians(-22)),
        ("rear_left", -3.78, 1.72, math.radians(-42)),
        ("rear_right", 3.78, 1.72, math.radians(42)),
    ]
    for label, x, y, rot in bench_specs:
        make_box(f"ai_insight_bench_{label}_curved_seat", (x, y, 0.55), (0.72, 0.28, 0.16), "detail", rotation=(0, 0, rot))
        make_box(f"ai_insight_bench_{label}_low_back", (x, y + 0.22, 0.84), (0.78, 0.08, 0.48), "base", rotation=(0, 0, rot))
        make_cylinder(f"ai_insight_bench_{label}_left_support", (x - 0.28, y - 0.08, 0.34), 0.045, 0.36, "detail", vertices=8)
        make_cylinder(f"ai_insight_bench_{label}_right_support", (x + 0.28, y - 0.08, 0.34), 0.045, 0.36, "detail", vertices=8)
        make_box(f"ai_insight_bench_{label}_glass_connection_display", (x, y + 0.55, 1.44), (0.84, 0.04, 0.46), "glass", rotation=(0, 0, rot))
        for tick in range(3):
            make_box(
                f"ai_insight_bench_{label}_bond_metric_bar_{tick}",
                (x - 0.22 + tick * 0.22, y + 0.525, 1.33 + tick * 0.10),
                (0.14 + tick * 0.08, 0.030, 0.030),
                "emissive",
                rotation=(0, 0, rot),
            )


def build_trust_vines():
    vine_specs = [
        ("left_wall_deep_trust", [(-5.38, 0.25, 0.52), (-5.62, 1.22, 1.22), (-5.32, 2.10, 2.02), (-5.62, 3.00, 3.10), (-5.12, 3.70, 4.20)], 0.060),
        ("right_wall_growing_trust", [(5.38, 0.05, 0.50), (5.58, 1.00, 1.05), (5.28, 1.78, 1.82), (5.62, 2.84, 2.72), (5.18, 3.58, 3.64)], 0.045),
        ("rear_wall_family_line", [(-2.80, 4.52, 0.62), (-1.65, 4.70, 1.36), (-0.48, 4.56, 2.25), (0.92, 4.68, 3.08), (2.50, 4.42, 4.05)], 0.070),
        ("ceiling_canopy_trust_arc", [(-3.10, 2.90, 4.72), (-1.58, 2.35, 5.02), (0.0, 2.10, 5.12), (1.58, 2.35, 5.02), (3.10, 2.90, 4.72)], 0.042),
    ]
    for label, points, radius in vine_specs:
        for idx in range(len(points) - 1):
            make_cylinder_between(f"trust_vines_{label}_segment_{idx:02d}", points[idx], points[idx + 1], radius * (1.0 - idx * 0.08), "detail", vertices=6)
        for idx, point in enumerate(points[1:]):
            slot = "emissive" if idx % 2 == 0 else "accent"
            make_uv_sphere(f"trust_vines_{label}_rose_growth_node_{idx:02d}", point, radius * 1.95, slot, segments=6, rings=3)
            side = -1 if idx % 2 == 0 else 1
            leaf_end = (point[0] + side * 0.30, point[1] + 0.10 * side, point[2] + 0.12)
            make_cylinder_between(f"trust_vines_{label}_leaflet_{idx:02d}_{side}", point, leaf_end, 0.018, "accent", vertices=5)


def build_memory_timeline():
    moments = [
        ("first_meeting", -4.32, -1.25, 1.22, 0.0),
        ("shared_win", -4.88, 0.42, 1.62, 0.22),
        ("hard_conversation", -4.42, 2.10, 2.05, -0.16),
        ("celebration", 4.32, -1.25, 1.22, 0.0),
        ("family_trip", 4.88, 0.42, 1.62, -0.22),
        ("renewed_trust", 4.42, 2.10, 2.05, 0.16),
    ]
    for idx, (label, x, y, z, tilt) in enumerate(moments):
        side = -1 if x < 0 else 1
        rot = math.radians(90 * side)
        make_box(f"memory_timeline_{label}_soft_glass_moment_panel", (x, y, z), (0.62, 0.045, 0.42), "glass", rotation=(0, 0, rot))
        make_torus(
            f"memory_timeline_{label}_abstract_shared_moment_ring",
            (x - side * 0.05, y, z + 0.08),
            0.24,
            0.016,
            "emissive",
            rotation=(math.radians(72), tilt, rot),
            major_segments=12,
            minor_segments=3,
        )
        make_scaled_uv_sphere(f"memory_timeline_{label}_warm_blob", (x - side * 0.13, y, z - 0.08), (0.13, 0.03, 0.09), "energy" if idx % 2 else "accent", segments=6, rings=3, rotation=(0, 0, rot))
    for side, x in [("left", -4.62), ("right", 4.62)]:
        make_cylinder_between(f"memory_timeline_{side}_perimeter_guide_thread", (x, -1.84, 0.84), (x, 2.82, 2.38), 0.018, "emissive", vertices=6)


def build_empathy_alcoves():
    alcoves = [
        ("left", -4.62, 0.18, math.radians(-68)),
        ("right", 4.62, 0.18, math.radians(68)),
    ]
    for label, x, y, rot in alcoves:
        make_box(f"empathy_alcove_{label}_recessed_dark_nook_back", (x, y + 0.78, 1.30), (1.26, 0.12, 2.30), "base", rotation=(0, 0, rot))
        make_box(f"empathy_alcove_{label}_pair_seat_a", (x - (0.32 if label == 'left' else -0.32), y, 0.54), (0.44, 0.40, 0.18), "detail", rotation=(0, 0, rot))
        make_box(f"empathy_alcove_{label}_pair_seat_b", (x + (0.32 if label == 'left' else -0.32), y, 0.54), (0.44, 0.40, 0.18), "detail", rotation=(0, 0, rot))
        make_scaled_uv_sphere(f"empathy_alcove_{label}_aura_field_one", (x - 0.18, y + 0.15, 1.20), (0.52, 0.055, 0.40), "glass", segments=8, rings=4, rotation=(0, 0, rot))
        make_scaled_uv_sphere(f"empathy_alcove_{label}_aura_field_two", (x + 0.18, y + 0.15, 1.20), (0.52, 0.055, 0.40), "glass", segments=8, rings=4, rotation=(0, 0, rot))
        make_cylinder_between(f"empathy_alcove_{label}_merged_emotional_thread", (x - 0.42, y + 0.20, 1.22), (x + 0.42, y + 0.20, 1.22), 0.022, "emissive", vertices=6)


def build_low_planter_beds():
    planter_specs = [
        ("entry_left", -1.62, -3.78, 0.62, 0.30, math.radians(18)),
        ("entry_right", 1.62, -3.78, 0.62, 0.30, math.radians(-18)),
        ("memory_left", -3.62, 2.74, 0.82, 0.32, math.radians(-30)),
        ("memory_right", 3.62, 2.74, 0.82, 0.32, math.radians(30)),
        ("rear_family", 0.0, 3.58, 1.05, 0.35, 0.0),
    ]
    for label, x, y, rx, ry, rot in planter_specs:
        make_ellipse_cylinder(f"low_planter_beds_{label}_organic_dark_basin", (x, y, 0.30), rx, ry, 0.28, "detail", vertices=16, rotation=(0, 0, rot))
        make_ellipse_cylinder(f"low_planter_beds_{label}_rose_soil_glow_line", (x, y, 0.47), rx * 0.78, ry * 0.72, 0.045, "accent", vertices=16, rotation=(0, 0, rot))
        for idx in range(3):
            angle = rot + math.radians(idx * 120 + (18 if label.endswith("right") else 0))
            px = x + math.cos(angle) * rx * 0.42
            py = y + math.sin(angle) * ry * 0.42
            height = 0.28 + 0.05 * (idx % 3)
            make_cone(f"low_planter_beds_{label}_leaf_fan_{idx:02d}", (px, py, 0.58 + height * 0.5), 0.07, 0.015, height, "accent" if idx % 2 else "emissive", vertices=5, rotation=(math.radians(8), 0, angle))


def build_runtime_empties():
    create_empty("light_0", (0.0, 0.0, 1.55), 0.50)
    create_empty("light_1", (-4.20, 2.16, 2.25), 0.46)
    create_empty("light_2", (0.0, 0.18, 4.90), 0.46)
    create_empty("camera_target", (0.0, -0.42, 1.34), 0.58)


def group_for_object(name):
    if name.startswith("connection_garden_room_shell"):
        return "Room shell and garden canopy"
    if name.startswith("family_bonding_dome"):
        return "Family bonding dome focal"
    if name.startswith("rose_energy_path"):
        return "Walking paths with rose energy threads"
    if name.startswith("ai_insight_bench"):
        return "AI relationship insight benches"
    if name.startswith("trust_vines"):
        return "Trust vines on walls and ceiling"
    if name.startswith("memory_timeline"):
        return "Memory timeline hologram moments"
    if name.startswith("empathy_alcove"):
        return "Empathy space alcoves"
    if name.startswith("low_planter_beds"):
        return "Low planter beds and rose vegetation"
    return "Other"


GROUP_EXPORT_PREFIX = {
    "Room shell and garden canopy": "connection_garden_room_shell",
    "Family bonding dome focal": "family_bonding_dome",
    "Walking paths with rose energy threads": "rose_energy_path",
    "AI relationship insight benches": "ai_insight_bench",
    "Trust vines on walls and ceiling": "trust_vines",
    "Memory timeline hologram moments": "memory_timeline",
    "Empathy space alcoves": "empathy_alcove",
    "Low planter beds and rose vegetation": "low_planter_beds",
}


def consolidate_meshes_by_group_and_slot():
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
        "session": 35,
        "module": "07-relationships",
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

    root = bpy.data.objects.new("relationships-int", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.1
    for obj in list(bpy.data.objects):
        if obj == root:
            continue
        if obj.type in {"MESH", "EMPTY"} and obj.parent is None and not obj.name.startswith("S35_"):
            obj.parent = root

    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        selected = obj.type in {"MESH", "EMPTY"} and not obj.name.startswith("S35_")
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


def build_session_35():
    print("=== Session 35: Relationships Interior ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    lighting = load_python_module(os.path.join(SHARED_DIR, "lighting-rig.py"), "lighting_rig_s35")
    lighting["clear_lighting"]()
    lighting["setup_viewport_lighting"]()

    material_library = load_python_module(os.path.join(SHARED_DIR, "material-library.py"), "material_library_s35")
    global MATS
    MATS = material_library["create_materials"]("#F43F5E", include_energy=True, include_holo=False)

    interior_lighting = load_python_module(os.path.join(SHARED_DIR, "interior-lighting-rig.py"), "interior_lighting_s35")
    interior_lighting["setup_interior_lighting"](focal_point=(0, -0.42, 1.34), floor_z=0.0, ceiling_z=5.45, radius=5.2)
    interior_lighting["boost_emissions_for_preview"]()

    build_room_shell()
    build_family_bonding_dome()
    build_walking_paths()
    build_ai_insight_benches()
    build_trust_vines()
    build_memory_timeline()
    build_empathy_alcoves()
    build_low_planter_beds()
    build_runtime_empties()
    consolidate_meshes_by_group_and_slot()

    overview_cam = make_camera("S35_Interior_Overview_Camera", (7.4, -8.2, 5.4), (0, -0.18, 1.72), lens=31)
    entry_cam = make_camera("S35_Interior_Entry_Camera", (0.0, -8.15, 2.02), (0, -0.42, 1.34), lens=35)
    focal_cam = make_camera("S35_Interior_Focal_Bonding_Dome_Camera", (2.95, -4.72, 2.46), (0, -0.20, 1.38), lens=41)
    top_cam = make_camera("S35_Interior_Topdown_Camera", (0.0, -0.25, 10.7), (0, 0.0, 0.20), lens=43)

    screenshots = [
        render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s35-int-overview.png")),
        render_still(entry_cam, os.path.join(SCREENSHOTS_DIR, "s35-int-from-entry.png")),
        render_still(focal_cam, os.path.join(SCREENSHOTS_DIR, "s35-int-focal-bonding-dome.png")),
        render_still_with_hidden(top_cam, os.path.join(SCREENSHOTS_DIR, "s35-int-topdown.png"), ["connection_garden_room_shell_base_joined", "connection_garden_room_shell_glass_joined"]),
    ]

    previous_emissions = set_all_emission_strength(0.0)
    screenshots.append(render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s35-int-dark-first.png")))
    restore_emission_strength(previous_emissions)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    metrics = collect_metrics([os.path.relpath(path, MODULE_DIR) for path in screenshots])
    metrics = export_draft_glb(metrics)
    with open(METRICS_FILE, "w") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)

    print("=" * 70)
    print("SESSION 35 BUILD COMPLETE")
    print(f"Blend: {BLEND_FILE}")
    print(f"Draft GLB: {DRAFT_GLB}")
    print(f"GLB size: {metrics['glb_size_bytes'] / 1024:.1f} KB")
    print(f"Tris: {metrics['total_tris']}")
    print(f"Meshes: {metrics['mesh_objects']}")
    print(f"Empties: {metrics['empty_names']}")
    print(f"Metrics: {METRICS_FILE}")
    print("SESSION35_METRICS=" + json.dumps(metrics, indent=2, sort_keys=True))
    return metrics


metrics = build_session_35()

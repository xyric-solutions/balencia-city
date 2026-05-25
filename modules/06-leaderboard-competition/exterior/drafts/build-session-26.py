"""
Balencia City v3 - Module #06 Leaderboard & Competition
Session 26: Exterior Detail, Polish, Export

Loads the Session 25 arena major forms, adds the deferred arena detail pass,
exports the approved exterior GLB, and writes QA metrics/screenshots.
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
MODULE = os.path.join(ROOT, "modules/06-leaderboard-competition")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
APPROVED = os.path.join(MODULE, "exterior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")

S25_BLEND = os.path.join(DRAFTS, "leaderboard-competition-s25-major-forms.blend")
S26_BLEND = os.path.join(DRAFTS, "leaderboard-competition-s26-detail-export.blend")
DRAFT_GLB = os.path.join(DRAFTS, "leaderboard-ext-draft-s26.glb")
APPROVED_GLB = os.path.join(APPROVED, "leaderboard-ext.glb")
METRICS_FILE = os.path.join(DRAFTS, "session26-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS, "session26-qa-import.json")

ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy"}

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s26", os.path.join(ROOT, "shared/lighting-rig.py"))
materials_mod = load_module("balencia_materials_s26", os.path.join(ROOT, "shared/material-library.py"))


created_objects = []
created_categories = {}


def register(obj, category):
    if obj is None:
        return obj
    created_objects.append(obj.name)
    created_categories[obj.name] = category
    return obj


def material_base_name(material):
    return material.name.split(".")[0] if material else ""


def ensure_materials():
    mats = {name: bpy.data.materials.get(name) for name in ALLOWED_MATERIALS}
    missing = [name for name, mat in mats.items() if mat is None]
    if missing:
        new_mats = materials_mod.create_materials("#FB7185", include_energy=True, include_holo=False)
        for name, mat in new_mats.items():
            if name in mats and mats[name] is None:
                mats[name] = mat
    mats = {name: bpy.data.materials.get(name) or mats.get(name) for name in ALLOWED_MATERIALS}
    return mats


def assign(obj, mat):
    if obj is None or obj.type != "MESH":
        return obj
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def apply_transforms(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    return obj


def make_mesh(name, verts, faces, mat, category):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    return register(obj, category)


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
    return make_mesh(name, verts, faces, mat, category)


def add_box(name, loc, dims, mat, category, rot_z=0.0):
    return box_mesh(name, [(loc, dims, rot_z)], mat, category)


def cylinder(name, loc, radius, depth, mat, category, vertices=10, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, mat, category, vertices=10, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices, radius1=radius1, radius2=radius2, depth=depth, location=loc, rotation=rot
    )
    obj = bpy.context.view_layer.objects.active
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
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def cylinder_between(name, start, end, radius, mat, category, vertices=8):
    start = Vector(start)
    end = Vector(end)
    direction = end - start
    length = direction.length
    if length < 0.001:
        return None
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=(start + end) * 0.5)
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def arc_band(name, outer_r, inner_r, z0, z1, start_deg, end_deg, mat, category, segments=16, closed=False):
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
    for i in range(segments):
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
    return make_mesh(name, verts, faces, mat, category)


def arc_panel(name, radius, z_center, height, thickness, start_deg, end_deg, mat, category, segments=12):
    return arc_band(
        name,
        radius + thickness * 0.5,
        radius - thickness * 0.5,
        z_center - height * 0.5,
        z_center + height * 0.5,
        start_deg,
        end_deg,
        mat,
        category,
        segments=segments,
        closed=False,
    )


def polar_box(angle_deg, radius, z, dims, rot_extra=math.pi / 2):
    angle = math.radians(angle_deg)
    loc = (math.cos(angle) * radius, math.sin(angle) * radius, z)
    return loc, dims, angle + rot_extra


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
        mat_name = material_base_name(obj.data.materials[0]) if obj.data.materials else "NONE"
        totals[mat_name] = totals.get(mat_name, 0) + get_tri_count(obj)
    return dict(sorted(totals.items()))


def object_metrics():
    rows = []
    for obj in sorted((o for o in bpy.data.objects if o.type == "MESH"), key=lambda o: o.name):
        rows.append(
            {
                "name": obj.name,
                "tris": get_tri_count(obj),
                "material": material_base_name(obj.data.materials[0]) if obj.data.materials else "NONE",
                "category": created_categories.get(obj.name, "Session 25 retained major forms"),
            }
        )
    return rows


def category_metrics():
    metrics = {}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        category = created_categories.get(obj.name, "Session 25 retained major forms")
        if category not in metrics:
            metrics[category] = {"objects": 0, "tris": 0}
        metrics[category]["objects"] += 1
        metrics[category]["tris"] += get_tri_count(obj)
    return dict(sorted(metrics.items()))


def bbox():
    min_v = Vector((1e9, 1e9, 1e9))
    max_v = Vector((-1e9, -1e9, -1e9))
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for vertex in obj.data.vertices:
            v = obj.matrix_world @ vertex.co
            min_v.x = min(min_v.x, v.x)
            min_v.y = min(min_v.y, v.y)
            min_v.z = min(min_v.z, v.z)
            max_v.x = max(max_v.x, v.x)
            max_v.y = max(max_v.y, v.y)
            max_v.z = max(max_v.z, v.z)
    return {
        "min": [round(min_v.x, 4), round(min_v.y, 4), round(min_v.z, 4)],
        "max": [round(max_v.x, 4), round(max_v.y, 4), round(max_v.z, 4)],
    }


def bbox_vectors():
    data = bbox()
    return Vector(data["min"]), Vector(data["max"])


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_shot(filename, camera_loc, target, lens=38):
    cam_data = bpy.data.cameras.new(filename.replace(".png", "_Camera"))
    cam = bpy.data.objects.new(filename.replace(".png", "_Camera"), cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    cam.data.lens = lens
    cam.data.clip_start = 0.1
    cam.data.clip_end = 260
    look_at(cam, target)
    bpy.context.scene.camera = cam
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.image_settings.file_format = "PNG"
    path = os.path.join(SCREENSHOTS, filename)
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    return path


def emission_slots():
    slots = []
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if not bsdf:
            continue
        if "Emission Strength" in bsdf.inputs:
            slots.append((mat, bsdf.inputs["Emission Strength"], bsdf.inputs["Emission Strength"].default_value))
    return slots


def render_dark_first():
    slots = emission_slots()
    for _, slot, _ in slots:
        slot.default_value = 0.0
    path = render_shot("s26_dark_first.png", (18, -24, 8.8), (0, 0, 4.4), 40)
    for _, slot, value in slots:
        slot.default_value = value
    return path


def remove_cameras_lights():
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)


def setup_lighting():
    remove_cameras_lights()
    lighting.setup_viewport_lighting()


def add_facade_rhythm(mats):
    category = "Facade rhythm and panelization"
    base_boxes = []
    detail_boxes = []
    glass_boxes = []
    accent_boxes = []

    for tier in range(4):
        z = 1.18 + tier * 0.78
        radius = 7.70 + tier * 0.15
        for idx in range(16):
            angle = idx * 22.5
            if 240 <= angle <= 300:
                continue
            base_boxes.append(polar_box(angle, radius + 0.04, z, (0.52, 0.08, 0.24)))
            if idx % 2 == 0:
                glass_boxes.append(polar_box(angle + 4.5, radius + 0.08, z + 0.23, (0.30, 0.045, 0.12)))
            else:
                accent_boxes.append(polar_box(angle - 4.5, radius + 0.09, z + 0.24, (0.22, 0.04, 0.07)))

    for idx in range(18):
        angle = idx * 20.0
        if 247 <= angle <= 293:
            continue
        detail_boxes.append(polar_box(angle, 7.98, 3.78, (0.08, 0.11, 4.76)))

    box_mesh("s26_outer_armored_facade_base_panels", base_boxes, mats["base"], category)
    box_mesh("s26_outer_vertical_pilaster_rhythm", detail_boxes, mats["detail"], category)
    box_mesh("s26_facade_shadow_glass_slit_breaks", glass_boxes, mats["glass"], category)
    box_mesh("s26_coral_floor_index_ticks", accent_boxes, mats["accent"], category)


def add_seating_and_aisles(mats):
    category = "Seating and aisle articulation"
    aisle_boxes = []
    row_marker_boxes = []
    step_break_boxes = []

    for idx in range(12):
        angle = idx * 30.0
        if 250 <= angle <= 290:
            continue
        aisle_boxes.append(polar_box(angle, 4.25, 2.85, (4.35, 0.055, 0.055), rot_extra=0.0))

    for ring in range(4):
        radius = 2.65 + ring * 0.68
        z = 1.05 + ring * 0.50
        for idx in range(16):
            angle = idx * 22.5 + ring * 3.0
            row_marker_boxes.append(polar_box(angle, radius, z, (0.18, 0.055, 0.08)))
            if idx % 5 == 0:
                step_break_boxes.append(polar_box(angle + 4.0, radius + 0.25, z + 0.08, (0.24, 0.07, 0.16)))

    box_mesh("s26_inner_bowl_radial_aisle_lines", aisle_boxes, mats["detail"], category)
    box_mesh("s26_seating_row_coral_markers", row_marker_boxes, mats["accent"], category)
    box_mesh("s26_seating_section_break_blocks", step_break_boxes, mats["detail"], category)


def add_rim_and_apex_detail(mats):
    category = "Rim engineering and apex receiver polish"

    for idx in range(16):
        angle = math.radians(idx * 22.5)
        start = (math.cos(angle) * 8.32, math.sin(angle) * 8.32, 6.48)
        end = (math.cos(angle) * 6.42, math.sin(angle) * 6.42, 6.05)
        cylinder_between(f"s26_rim_underbrace_truss_{idx:02d}", start, end, 0.035, mats["detail"], category, vertices=8)

    bolt_boxes = [polar_box(idx * 15.0, 8.72, 6.95, (0.15, 0.10, 0.12)) for idx in range(24)]
    box_mesh("s26_top_rim_segmented_bolt_blocks", bolt_boxes, mats["detail"], category)

    for start in range(0, 360, 90):
        arc_panel(
            f"s26_upper_coral_rim_lip_{start:03d}",
            8.78,
            7.03,
            0.075,
            0.055,
            start + 4,
            start + 70,
            mats["accent"],
            category,
            segments=8,
        )

    torus("s26_apex_receiver_inner_gold_collar", (0, 0, 7.44), 0.68, 0.035, mats["accent"], category, 22, 3)
    torus("s26_apex_receiver_outer_detail_collar", (0, 0, 7.18), 1.22, 0.045, mats["detail"], category, 26, 3)

    for idx in range(6):
        angle = math.radians(idx * 60.0)
        start = (math.cos(angle) * 1.05, math.sin(angle) * 1.05, 7.45)
        end = (math.cos(angle) * 0.40, math.sin(angle) * 0.40, 8.16)
        cylinder_between(f"s26_apex_receiver_splayed_rod_{idx:02d}", start, end, 0.032, mats["energy"], category, vertices=8)
    cone("s26_apex_strike_micro_spire", (0, 0, 8.42), 0.16, 0.035, 0.58, mats["energy"], category, vertices=10)


def add_entry_and_walkway_detail(mats):
    category = "Entry portal and competitor walkway"

    front_y = -8.78
    arch_radius = 1.98
    arch_center_z = 3.84
    arch_points = []
    for step in range(10):
        theta = math.pi - (math.pi * step / 9)
        arch_points.append((arch_radius * math.cos(theta), front_y - 0.05, arch_center_z + arch_radius * math.sin(theta)))
    for idx in range(len(arch_points) - 1):
        cylinder_between(
            f"s26_grand_arch_inner_energy_trace_{idx:02d}",
            arch_points[idx],
            arch_points[idx + 1],
            0.055,
            mats["energy"],
            category,
            vertices=8,
        )

    add_box("s26_grand_entry_keystone_block", (0, front_y - 0.08, 5.82), (0.54, 0.22, 0.46), mats["accent"], category)
    add_box("s26_grand_entry_left_buttress_plinth", (-2.48, front_y - 0.08, 1.36), (0.34, 0.42, 1.28), mats["detail"], category)
    add_box("s26_grand_entry_right_buttress_plinth", (2.48, front_y - 0.08, 1.36), (0.34, 0.42, 1.28), mats["detail"], category)

    chevrons = []
    edge_ticks = []
    for idx in range(8):
        y = -9.7 - idx * 0.64
        chevrons.append(((0, y, 0.48), (1.25 - idx * 0.03, 0.055, 0.055), math.radians(24)))
        chevrons.append(((0, y, 0.48), (1.25 - idx * 0.03, 0.055, 0.055), math.radians(-24)))
        edge_ticks.append(((-1.15, y, 0.50), (0.16, 0.05, 0.10), 0.0))
        edge_ticks.append(((1.15, y, 0.50), (0.16, 0.05, 0.10), 0.0))
    box_mesh("s26_competitor_walkway_coral_chevrons", chevrons, mats["accent"], category)
    box_mesh("s26_competitor_walkway_lane_tick_blocks", edge_ticks, mats["detail"], category)

    for x in (-0.62, 0.0, 0.62):
        cylinder(f"s26_entry_turnstile_post_{x:+.2f}", (x, -9.02, 0.82), 0.06, 0.82, mats["detail"], category, vertices=8)
        cylinder_between(
            f"s26_entry_turnstile_crossbar_{x:+.2f}",
            (x - 0.28, -9.02, 0.92),
            (x + 0.28, -9.02, 0.92),
            0.025,
            mats["accent"],
            category,
            vertices=6,
        )


def add_leaderboard_display_detail(mats):
    category = "Leaderboard display graphics"

    arc_panel("s26_leaderboard_upper_frame_arc", 8.99, 4.48, 0.11, 0.07, -70, 20, mats["accent"], category, 18)
    arc_panel("s26_leaderboard_lower_frame_arc", 8.99, 3.12, 0.11, 0.07, -70, 20, mats["accent"], category, 18)
    arc_panel("s26_leaderboard_mid_scanline", 9.02, 3.80, 0.04, 0.04, -66, 16, mats["energy"], category, 18)

    score_boxes = []
    glyph_boxes = []
    for row in range(5):
        z = 3.32 + row * 0.22
        for col in range(4):
            angle = -58 + col * 10.2 + row * 0.7
            glyph_boxes.append(polar_box(angle, 9.07, z, (0.12, 0.035, 0.13)))
        for tick in range(3):
            angle = -12 + tick * 6.2 - row * 1.1
            score_boxes.append(polar_box(angle, 9.08, z + 0.035, (0.20 + tick * 0.045, 0.035, 0.055)))
    box_mesh("s26_leaderboard_rank_number_glyphs", glyph_boxes, mats["emissive"], category)
    box_mesh("s26_leaderboard_score_tick_geometry", score_boxes, mats["accent"], category)


def add_victory_pillar_detail(mats):
    category = "Victory pillar hardware"

    pillar_radius = 9.18
    diagonal = pillar_radius / math.sqrt(2)
    pillars = [
        ("north_east", diagonal, diagonal),
        ("south_east", diagonal, -diagonal),
        ("south_west", -diagonal, -diagonal),
        ("north_west", -diagonal, diagonal),
    ]

    for name, x, y in pillars:
        angle = math.atan2(y, x)
        torus(f"s26_{name}_upper_victory_collar", (x, y, 7.25), 0.28, 0.035, mats["accent"], category, 16, 3)

        for side in (-1, 1):
            start = (x + math.cos(angle + side * 1.35) * 0.64, y + math.sin(angle + side * 1.35) * 0.64, 0.72)
            end = (x + math.cos(angle + side * 0.55) * 0.30, y + math.sin(angle + side * 0.55) * 0.30, 3.18)
            cylinder_between(f"s26_{name}_diagonal_base_brace_{side:+d}", start, end, 0.035, mats["detail"], category, vertices=8)

        for rod_idx in range(3):
            rod_angle = angle + rod_idx * math.tau / 3 + math.pi / 4
            offset = Vector((math.cos(rod_angle) * 0.26, math.sin(rod_angle) * 0.26, 0))
            cylinder_between(
                f"s26_{name}_beacon_cage_rod_{rod_idx}",
                (x + offset.x, y + offset.y, 8.82),
                (x + offset.x, y + offset.y, 9.92),
                0.025,
                mats["detail"],
                category,
                vertices=5,
            )

        fin_boxes = []
        for fin_idx in range(4):
            fin_angle = angle + fin_idx * math.pi / 2
            loc = (x + math.cos(fin_angle) * 0.36, y + math.sin(fin_angle) * 0.36, 8.76)
            fin_boxes.append((loc, (0.16, 0.055, 0.32), fin_angle + math.pi / 2))
        box_mesh(f"s26_{name}_beacon_heat_fins", fin_boxes, mats["detail"], category)


def normalize_material_slots():
    mats = ensure_materials()
    fallback = mats["detail"]
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        if not obj.data.materials:
            obj.data.materials.append(fallback)
        for index, material in enumerate(obj.data.materials):
            base = material_base_name(material)
            if base in mats:
                obj.data.materials[index] = mats[base]
            elif base not in ALLOWED_MATERIALS:
                obj.data.materials[index] = fallback


def apply_mesh_world_transforms():
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(obj.matrix_world.copy())
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)
        obj.parent = None


def center_bottom_origin():
    min_v, max_v = bbox_vectors()
    center_x = (min_v.x + max_v.x) / 2
    center_y = (min_v.y + max_v.y) / 2
    lift_z = -min_v.z
    correction = Matrix.Translation(Vector((-center_x, -center_y, lift_z)))
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(correction)
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)


def export_leaderboard():
    remove_cameras_lights()
    for obj in list(bpy.data.objects):
        if obj.type == "EMPTY":
            bpy.data.objects.remove(obj, do_unlink=True)
    apply_mesh_world_transforms()
    normalize_material_slots()
    center_bottom_origin()

    root = bpy.data.objects.new("leaderboard-ext", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.parent = root

    bpy.ops.wm.save_as_mainfile(filepath=S26_BLEND)
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
        "glb_bytes": os.path.getsize(APPROVED_GLB),
        "tris": scene_triangles(),
        "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "materials": sorted({material_base_name(mat) for mat in bpy.data.materials if mat.users}),
        "material_tris": material_triangles(),
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
        if any(abs(v - 1) > 1e-5 for v in obj.scale):
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
    lighting.setup_viewport_lighting()

    imports = [
        ("sia", os.path.join(ROOT, "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb"), (0, 0, 0)),
        ("fitness", os.path.join(ROOT, "modules/01-fitness/exterior/approved/fitness-ext.glb"), (25, 25, 0)),
        ("yoga", os.path.join(ROOT, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb"), (35, 10, 0)),
        ("finance", os.path.join(ROOT, "modules/03-finance/exterior/approved/finance-ext.glb"), (35, -5, 0)),
        ("knowledgebase", os.path.join(ROOT, "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"), (30, -20, 0)),
        ("chat", os.path.join(ROOT, "modules/05-chat-communication/exterior/approved/chat-ext.glb"), (18, -34, 0)),
        ("leaderboard", APPROVED_GLB, (-8, -44, 0)),
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

    path = render_shot("s26_cohesion_all7.png", (82, -122, 78), (12, -16, 9), 22)
    return {"screenshot": path, "imported": imported_labels}


def build_session_26():
    if not os.path.exists(S25_BLEND):
        raise FileNotFoundError(S25_BLEND)

    print("=== Session 26: Leaderboard exterior detail, polish, export ===")
    bpy.ops.wm.open_mainfile(filepath=S25_BLEND)
    setup_lighting()
    mats = ensure_materials()
    normalize_material_slots()

    before_tris = scene_triangles()
    before_meshes = sum(1 for obj in bpy.data.objects if obj.type == "MESH")

    add_facade_rhythm(mats)
    add_seating_and_aisles(mats)
    add_rim_and_apex_detail(mats)
    add_entry_and_walkway_detail(mats)
    add_leaderboard_display_detail(mats)
    add_victory_pillar_detail(mats)
    normalize_material_slots()

    after_detail_tris = scene_triangles()
    if after_detail_tris > 18000:
        raise RuntimeError(f"Session 26 detail exceeded exterior budget before export: {after_detail_tris} tris")

    bpy.ops.wm.save_as_mainfile(filepath=S26_BLEND)

    screenshots = [
        render_shot("s26_front_elevation.png", (0, -25, 6.8), (0, 0, 4.55), 38),
        render_shot("s26_three_quarter.png", (18, -24, 10.2), (0, 0, 4.7), 38),
        render_shot("s26_distance_view.png", (32, -40, 17.0), (0, 0, 5.0), 42),
        render_dark_first(),
    ]

    metrics_before_export = {
        "session": 26,
        "module": "06-leaderboard-competition",
        "blender_version": bpy.app.version_string,
        "source_blend": S25_BLEND,
        "blend": S26_BLEND,
        "before_mesh_objects": before_meshes,
        "before_tris": before_tris,
        "after_detail_mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "after_detail_tris": after_detail_tris,
        "detail_added_tris": after_detail_tris - before_tris,
        "category_metrics": category_metrics(),
        "material_tris": material_triangles(),
        "bbox": bbox(),
        "screenshots": screenshots,
        "objects": object_metrics(),
    }

    export_metrics = export_leaderboard()
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

    print("SESSION26_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_session_26()

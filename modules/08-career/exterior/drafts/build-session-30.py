"""
Balencia City v3 - Module #08 Career
Session 30: Exterior Detail, Polish, Export

Loads the Session 29 Career major forms, adds the deferred professional tower
detail pass, exports the exterior GLB, validates import metrics, and captures
the all-eight-structure cohesion screenshot.
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
MODULE = os.path.join(ROOT, "modules/08-career")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
APPROVED = os.path.join(MODULE, "exterior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")

S29_BLEND = os.path.join(DRAFTS, "career-s29-major-forms.blend")
S30_BLEND = os.path.join(DRAFTS, "career-s30-detail-export.blend")
DRAFT_GLB = os.path.join(DRAFTS, "career-ext-draft-s30.glb")
APPROVED_GLB = os.path.join(APPROVED, "career-ext.glb")
METRICS_FILE = os.path.join(DRAFTS, "session30-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS, "session30-qa-import.json")

ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy"}
DISTRICT_HEX = "#3B82F6"

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s30", os.path.join(ROOT, "shared/lighting-rig.py"))
materials_mod = load_module("balencia_materials_s30", os.path.join(ROOT, "shared/material-library.py"))

created_categories = {}


TOWERS = {
    "main_tower": {
        "center": (0.0, 0.0),
        "floors": 40,
        "height": 16.0,
        "bottom": (2.85, 2.35),
        "top": (2.00, 1.68),
        "base_z": 0.24,
        "window_columns": 2,
    },
    "secondary_west_tower": {
        "center": (-5.4, 1.45),
        "floors": 34,
        "height": 13.6,
        "bottom": (2.35, 2.02),
        "top": (1.76, 1.56),
        "base_z": 0.24,
        "window_columns": 1,
    },
    "secondary_east_tower": {
        "center": (5.25, -1.35),
        "floors": 30,
        "height": 12.0,
        "bottom": (2.20, 1.92),
        "top": (1.62, 1.42),
        "base_z": 0.24,
        "window_columns": 1,
    },
    "secondary_north_tower": {
        "center": (1.35, 5.25),
        "floors": 27,
        "height": 10.8,
        "bottom": (2.05, 1.82),
        "top": (1.50, 1.32),
        "base_z": 0.24,
        "window_columns": 1,
    },
}


BRIDGES = [
    ("main_to_west_upper", (-1.02, 0.34), (-4.33, 1.12), 11.30),
    ("main_to_east_mid", (1.02, -0.34), (4.18, -1.02), 8.45),
    ("main_to_north_executive", (0.34, 1.05), (1.06, 4.27), 12.85),
]


def register(obj, category):
    if obj is None:
        return obj
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
            elif base not in ALLOWED_MATERIALS:
                obj.data.materials[index] = fallback

    for mat in list(bpy.data.materials):
        base = material_base_name(mat)
        if base in ALLOWED_MATERIALS and mat.name != base and mat.users == 0:
            bpy.data.materials.remove(mat)


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
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    return register(obj, category)


def add_box(name, loc, dims, mat, category, rot_z=0.0):
    return box_mesh(name, [(loc, dims, rot_z)], mat, category)


def cylinder(name, loc, radius, depth, mat, category, vertices=8, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, mat, category, vertices=8, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices, radius1=radius1, radius2=radius2, depth=depth, location=loc, rotation=rot
    )
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def torus(name, loc, major, minor, mat, category, seg=16, minor_seg=3):
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


def oriented_box_between(name, start_xy, end_xy, z, width, height, mat, category):
    sx, sy = start_xy
    ex, ey = end_xy
    dx = ex - sx
    dy = ey - sy
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    return add_box(name, ((sx + ex) * 0.5, (sy + ey) * 0.5, z), (length, width, height), mat, category, angle)


def width_at_z(z, spec):
    base_z = spec["base_z"]
    t = max(0.0, min(1.0, (z - base_z) / spec["height"]))
    return spec["bottom"][0] + (spec["top"][0] - spec["bottom"][0]) * t


def depth_at_z(z, spec):
    base_z = spec["base_z"]
    t = max(0.0, min(1.0, (z - base_z) / spec["height"]))
    return spec["bottom"][1] + (spec["top"][1] - spec["bottom"][1]) * t


def add_facade_floor_plates(mats):
    category = "Dark floor-plate ledges and spandrel panels"
    ledge_boxes = []
    spandrel_boxes = []

    for prefix, spec in TOWERS.items():
        cx, cy = spec["center"]
        floors = spec["floors"]
        for floor in range(1, floors + 1):
            z = spec["base_z"] + spec["height"] * (floor / floors)
            width = width_at_z(z, spec)
            depth = depth_at_z(z, spec)
            ledge_boxes.extend(
                [
                    ((cx, cy - depth * 0.5 - 0.075, z), (width + 0.25, 0.07, 0.045), 0.0),
                    ((cx, cy + depth * 0.5 + 0.075, z), (width + 0.25, 0.07, 0.045), 0.0),
                    ((cx - width * 0.5 - 0.075, cy, z), (0.07, depth + 0.25, 0.045), 0.0),
                    ((cx + width * 0.5 + 0.075, cy, z), (0.07, depth + 0.25, 0.045), 0.0),
                ]
            )

        for floor in range(3, floors, 5):
            z = spec["base_z"] + spec["height"] * (floor / floors) + 0.13
            width = width_at_z(z, spec)
            depth = depth_at_z(z, spec)
            panel_w = max(0.36, width * 0.36)
            panel_d = max(0.30, depth * 0.34)
            spandrel_boxes.extend(
                [
                    ((cx, cy - depth * 0.5 - 0.052, z), (panel_w, 0.045, 0.28), 0.0),
                    ((cx, cy + depth * 0.5 + 0.052, z), (panel_w, 0.045, 0.28), 0.0),
                    ((cx - width * 0.5 - 0.052, cy, z), (0.045, panel_d, 0.28), 0.0),
                    ((cx + width * 0.5 + 0.052, cy, z), (0.045, panel_d, 0.28), 0.0),
                ]
            )

    box_mesh("s30_career_dark_floor_plate_ledge_system", ledge_boxes, mats["base"], category)
    box_mesh("s30_career_dark_spandrel_facade_panels", spandrel_boxes, mats["base"], category)


def add_window_and_mullion_rhythm(mats):
    glass_category = "Corporate glass window rhythm"
    detail_category = "Facade mullions and professional rails"
    accent_category = "Electric-blue ascent trim"
    glass_boxes = []
    mullion_boxes = []
    accent_boxes = []

    for prefix, spec in TOWERS.items():
        cx, cy = spec["center"]
        floors = spec["floors"]
        column_count = spec["window_columns"]
        z_step = 4 if prefix == "main_tower" else 5

        for floor in range(2, floors, z_step):
            z = spec["base_z"] + spec["height"] * (floor / floors)
            width = width_at_z(z, spec)
            depth = depth_at_z(z, spec)
            if column_count == 2:
                x_offsets = (-width * 0.23, width * 0.23)
                y_offsets = (-depth * 0.22, depth * 0.22)
            else:
                x_offsets = (0.0,)
                y_offsets = (0.0,)
            for x_off in x_offsets:
                glass_boxes.append(((cx + x_off, cy - depth * 0.5 - 0.092, z), (0.30, 0.035, 0.32), 0.0))
                glass_boxes.append(((cx + x_off, cy + depth * 0.5 + 0.092, z), (0.30, 0.035, 0.32), 0.0))
            for y_off in y_offsets:
                glass_boxes.append(((cx - width * 0.5 - 0.092, cy + y_off, z), (0.035, 0.30, 0.32), 0.0))
                glass_boxes.append(((cx + width * 0.5 + 0.092, cy + y_off, z), (0.035, 0.30, 0.32), 0.0))

        for floor in range(2, floors, 8):
            z = spec["base_z"] + spec["height"] * (floor / floors)
            width = width_at_z(z, spec)
            depth = depth_at_z(z, spec)
            mullion_boxes.extend(
                [
                    ((cx, cy - depth * 0.5 - 0.125, z), (0.045, 0.05, 0.50), 0.0),
                    ((cx, cy + depth * 0.5 + 0.125, z), (0.045, 0.05, 0.50), 0.0),
                    ((cx - width * 0.5 - 0.125, cy, z), (0.05, 0.045, 0.50), 0.0),
                    ((cx + width * 0.5 + 0.125, cy, z), (0.05, 0.045, 0.50), 0.0),
                ]
            )

        for floor in range(4, floors + 1, 6):
            z = spec["base_z"] + spec["height"] * (floor / floors) + 0.04
            width = width_at_z(z, spec)
            depth = depth_at_z(z, spec)
            accent_boxes.extend(
                [
                    ((cx - width * 0.5 - 0.16, cy - depth * 0.28, z), (0.08, 0.34, 0.065), 0.0),
                    ((cx + width * 0.5 + 0.16, cy + depth * 0.28, z), (0.08, 0.34, 0.065), 0.0),
                    ((cx - width * 0.28, cy - depth * 0.5 - 0.16, z), (0.34, 0.08, 0.065), 0.0),
                    ((cx + width * 0.28, cy + depth * 0.5 + 0.16, z), (0.34, 0.08, 0.065), 0.0),
                ]
            )

    box_mesh("s30_career_recessed_glass_window_panel_rhythm", glass_boxes, mats["glass"], glass_category)
    box_mesh("s30_career_vertical_mullion_rail_segments", mullion_boxes, mats["detail"], detail_category)
    box_mesh("s30_career_blue_ascent_trim_ticks", accent_boxes, mats["accent"], accent_category)


def add_skybridge_hardware(mats):
    category = "Skybridge enclosure hardware and underbraces"
    rib_boxes = []
    accent_boxes = []
    glass_boxes = []

    for bridge_name, start_xy, end_xy, z in BRIDGES:
        sx, sy = start_xy
        ex, ey = end_xy
        angle = math.atan2(ey - sy, ex - sx)
        direction = Vector((ex - sx, ey - sy, 0.0))
        length = max(direction.length, 0.001)
        unit = direction.normalized()
        perp = Vector((-unit.y, unit.x, 0.0))

        for idx in range(7):
            t = (idx + 1) / 8.0
            point = Vector((sx, sy, 0.0)) + direction * t
            rib_boxes.append(((point.x, point.y, z), (0.065, 0.94, 0.76), angle))
            if idx % 2 == 0:
                glass_boxes.append(((point.x, point.y, z + 0.04), (0.34, 0.78, 0.32), angle))
            accent_boxes.append(((point.x, point.y, z + 0.42), (0.12, 0.88, 0.055), angle))

        for side in (-1, 1):
            side_offset = perp * side * 0.43
            for idx in range(3):
                a = Vector((sx, sy, z - 0.42)) + direction * ((idx + 0.2) / 3.5) + side_offset
                b = Vector((sx, sy, z + 0.36)) + direction * ((idx + 0.9) / 3.5) + side_offset
                cylinder_between(
                    f"s30_{bridge_name}_diagonal_enclosure_brace_{side:+d}_{idx:02d}",
                    a,
                    b,
                    0.024,
                    mats["detail"],
                    category,
                    vertices=6,
                )

        oriented_box_between(
            f"s30_{bridge_name}_lower_structural_spine_reinforcement",
            start_xy,
            end_xy,
            z - 0.47,
            0.22,
            0.12,
            mats["detail"],
            category,
        )
        for side in (-1, 1):
            start = Vector((sx, sy, z - 0.50)) + perp * side * 0.30
            end = Vector((ex, ey, z - 0.50)) + perp * side * 0.30
            cylinder_between(
                f"s30_{bridge_name}_side_tension_cable_{side:+d}",
                start,
                end,
                0.018,
                mats["detail"],
                category,
                vertices=5,
            )

    box_mesh("s30_career_skybridge_vertical_rib_frames", rib_boxes, mats["detail"], category)
    box_mesh("s30_career_skybridge_blue_status_ticks", accent_boxes, mats["accent"], category)
    box_mesh("s30_career_skybridge_recessed_glass_panes", glass_boxes, mats["glass"], category)


def add_elevator_detail(mats):
    category = "Exterior elevator tube hardware"
    tube_specs = [
        ("main_tower", 1.62, -0.74, 15.0, 0.24 + 0.20, 0.27),
        ("secondary_west", -6.72, 1.02, 12.2, 0.24 + 0.18, 0.22),
    ]

    for name, x, y, height, base_z, radius in tube_specs:
        collar_count = 7 if name == "main_tower" else 6
        for idx in range(collar_count):
            z = base_z + height * ((idx + 1) / (collar_count + 1))
            torus(f"s30_{name}_elevator_tube_metal_collar_{idx:02d}", (x, y, z), radius + 0.025, 0.018, mats["detail"], category, seg=14, minor_seg=3)
            add_box(
                f"s30_{name}_elevator_blue_floor_call_marker_{idx:02d}",
                (x, y - radius - 0.045, z),
                (0.14, 0.035, 0.09),
                mats["accent"],
                category,
            )
        for side in (-1, 1):
            cylinder_between(
                f"s30_{name}_elevator_outer_service_ladder_{side:+d}",
                (x + side * (radius + 0.11), y, base_z + 0.45),
                (x + side * (radius + 0.11), y, base_z + height - 0.45),
                0.018,
                mats["detail"],
                category,
                vertices=5,
            )
        add_box(f"s30_{name}_elevator_base_docking_frame", (x, y, base_z + 0.08), (radius * 2.6, radius * 2.1, 0.16), mats["detail"], category)
        add_box(f"s30_{name}_elevator_top_docking_frame", (x, y, base_z + height - 0.08), (radius * 2.2, radius * 1.9, 0.14), mats["detail"], category)


def add_observation_deck_and_lobby_detail(mats):
    category = "Executive observation deck and lobby polish"
    deck_post_boxes = []

    for idx, x in enumerate([-1.08, -0.72, -0.36, 0.0, 0.36, 0.72, 1.08]):
        deck_post_boxes.append(((x, -2.17, 16.25), (0.045, 0.06, 0.54), 0.0))
    for y in [-1.90, -1.60, -1.30, -1.00]:
        deck_post_boxes.append(((-1.25, y, 16.25), (0.055, 0.045, 0.48), 0.0))
        deck_post_boxes.append(((1.25, y, 16.25), (0.055, 0.045, 0.48), 0.0))
    box_mesh("s30_observation_deck_detail_rail_posts", deck_post_boxes, mats["detail"], category)

    for idx, x in enumerate([-0.92, -0.46, 0.0, 0.46, 0.92]):
        add_box(
            f"s30_observation_deck_blue_floor_marker_{idx:02d}",
            (x, -2.18, 15.95),
            (0.22, 0.04, 0.06),
            mats["accent"],
            category,
        )
    for x in (-0.92, 0.0, 0.92):
        cylinder_between(
            f"s30_observation_deck_underside_v_brace_{x:+.2f}",
            (x, -2.05, 15.75),
            (x * 0.45, -0.98, 15.05),
            0.024,
            mats["detail"],
            category,
            vertices=6,
        )

    lobby_frames = []
    for x in [-0.72, -0.24, 0.24, 0.72]:
        lobby_frames.append(((x, -1.34, 1.03), (0.05, 0.045, 1.28), 0.0))
    for z in [0.55, 1.05, 1.55]:
        lobby_frames.append(((0.0, -1.36, z), (1.90, 0.045, 0.055), 0.0))
    box_mesh("s30_main_lobby_glass_mullion_frame", lobby_frames, mats["detail"], category)
    add_box("s30_main_lobby_executive_entry_canopy", (0.0, -1.58, 2.00), (2.35, 0.45, 0.10), mats["base"], category)
    add_box("s30_main_lobby_blue_arrival_marker", (0.0, -1.82, 0.42), (1.76, 0.08, 0.07), mats["accent"], category)


def add_plaza_and_crown_polish(mats):
    plaza_category = "Networking plaza detail"
    crown_category = "Crown hardpoint refinement"
    grid_boxes = []
    node_boxes = []

    for x in [-6.6, -4.4, -2.2, 2.2, 4.4, 6.6]:
        grid_boxes.append(((x, 1.2, 0.23), (0.055, 10.7, 0.035), 0.0))
    for y in [-4.2, -2.6, -1.0, 2.8, 4.4, 6.0]:
        grid_boxes.append(((0.0, y, 0.235), (14.2, 0.055, 0.035), 0.0))
    for idx, (x, y) in enumerate([(0.0, -3.25), (-5.4, 1.45), (5.25, -1.35), (1.35, 5.25), (0.0, 1.25)]):
        node_boxes.append(((x, y, 0.285), (0.58, 0.58, 0.06), math.radians(45)))
        add_box(f"s30_networking_plaza_blue_node_core_{idx:02d}", (x, y, 0.335), (0.24, 0.24, 0.055), mats["accent"], plaza_category, math.radians(45))

    box_mesh("s30_networking_plaza_subtle_tile_grid", grid_boxes, mats["detail"], plaza_category)
    box_mesh("s30_networking_plaza_career_node_pads", node_boxes, mats["base"], plaza_category)

    for idx, angle in enumerate([0, 90, 180, 270]):
        rad = math.radians(angle)
        start = (math.cos(rad) * 0.28, math.sin(rad) * 0.28, 17.28)
        end = (math.cos(rad) * 0.70, math.sin(rad) * 0.70, 17.55)
        cylinder_between(f"s30_crown_energy_socket_splayed_brace_{idx:02d}", start, end, 0.024, mats["energy"], crown_category, vertices=6)
    torus("s30_crown_energy_socket_outer_orange_collar", (0.0, 0.0, 17.55), 0.62, 0.034, mats["energy"], crown_category, seg=20, minor_seg=3)
    torus("s30_crown_dark_mechanical_mount_collar", (0.0, 0.0, 17.10), 0.74, 0.032, mats["detail"], crown_category, seg=20, minor_seg=3)
    cone("s30_crown_upward_blue_professional_fin", (0.0, 0.0, 18.08), 0.16, 0.035, 0.56, mats["accent"], crown_category, vertices=8)


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
                "category": created_categories.get(obj.name, "Session 29 retained major forms"),
            }
        )
    return rows


def category_metrics():
    metrics = {}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        category = created_categories.get(obj.name, "Session 29 retained major forms")
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
    cam.data.clip_end = 280
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
    path = render_shot("s30_dark_first.png", (18, -26, 12.0), (0, 1.1, 8.6), 40)
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
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"


def apply_mesh_world_transforms():
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(obj.matrix_world.copy())
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)
        obj.parent = None


def center_bottom_origin():
    min_v, max_v = bbox_vectors()
    center_x = (min_v.x + max_v.x) / 2.0
    center_y = (min_v.y + max_v.y) / 2.0
    lift_z = -min_v.z
    correction = Matrix.Translation(Vector((-center_x, -center_y, lift_z)))
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(correction)
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)


def export_career():
    remove_cameras_lights()
    for obj in list(bpy.data.objects):
        if obj.type == "EMPTY":
            bpy.data.objects.remove(obj, do_unlink=True)
    apply_mesh_world_transforms()
    normalize_material_slots()
    center_bottom_origin()

    root = bpy.data.objects.new("career-ext", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.parent = root

    bpy.ops.wm.save_as_mainfile(filepath=S30_BLEND)
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
    lighting.setup_viewport_lighting()

    imports = [
        ("sia", os.path.join(ROOT, "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb"), (0, 0, 0)),
        ("fitness", os.path.join(ROOT, "modules/01-fitness/exterior/approved/fitness-ext.glb"), (25, 25, 0)),
        ("yoga", os.path.join(ROOT, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb"), (35, 10, 0)),
        ("finance", os.path.join(ROOT, "modules/03-finance/exterior/approved/finance-ext.glb"), (35, -5, 0)),
        ("knowledgebase", os.path.join(ROOT, "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"), (30, -20, 0)),
        ("chat", os.path.join(ROOT, "modules/05-chat-communication/exterior/approved/chat-ext.glb"), (18, -34, 0)),
        ("leaderboard", os.path.join(ROOT, "modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb"), (-8, -44, 0)),
        ("career", APPROVED_GLB, (-28, -34, 0)),
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

    path = render_shot("s30_cohesion_all8.png", (84, -128, 82), (9, -17, 10), 22)
    return {"screenshot": path, "imported": imported_labels}


def material_percentages(total_tris, material_tris):
    return {name: round((tris / total_tris) * 100.0, 2) for name, tris in material_tris.items()} if total_tris else {}


def build_session_30():
    if not os.path.exists(S29_BLEND):
        raise FileNotFoundError(S29_BLEND)

    print("=== Session 30: Career exterior detail, polish, export ===")
    bpy.ops.wm.open_mainfile(filepath=S29_BLEND)
    setup_lighting()
    mats = ensure_materials()
    normalize_material_slots()

    before_tris = scene_triangles()
    before_meshes = sum(1 for obj in bpy.data.objects if obj.type == "MESH")

    add_facade_floor_plates(mats)
    add_window_and_mullion_rhythm(mats)
    add_skybridge_hardware(mats)
    add_elevator_detail(mats)
    add_observation_deck_and_lobby_detail(mats)
    add_plaza_and_crown_polish(mats)
    normalize_material_slots()

    after_detail_tris = scene_triangles()
    if after_detail_tris > 20000:
        raise RuntimeError(f"Session 30 detail exceeded exterior budget before export: {after_detail_tris} tris")
    if after_detail_tris < 15000:
        raise RuntimeError(f"Session 30 detail under-used exterior budget before export: {after_detail_tris} tris")

    bpy.ops.wm.save_as_mainfile(filepath=S30_BLEND)

    screenshots = [
        render_shot("s30_front_elevation.png", (0, -27, 9.5), (0, 1.0, 8.7), 38),
        render_shot("s30_three_quarter.png", (18, -25, 13.2), (0.2, 1.0, 8.9), 40),
        render_shot("s30_distance_view.png", (35, -42, 24.0), (0.1, 1.0, 9.0), 44),
        render_dark_first(),
    ]

    mat_tris = material_triangles()
    metrics_before_export = {
        "session": 30,
        "module": "08-career",
        "blender_version": bpy.app.version_string,
        "source_blend": S29_BLEND,
        "blend": S30_BLEND,
        "before_mesh_objects": before_meshes,
        "before_tris": before_tris,
        "after_detail_mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "after_detail_tris": after_detail_tris,
        "detail_added_tris": after_detail_tris - before_tris,
        "category_metrics": category_metrics(),
        "material_tris": mat_tris,
        "material_percentages": material_percentages(after_detail_tris, mat_tris),
        "bbox": bbox(),
        "screenshots": screenshots,
        "objects": object_metrics(),
    }

    export_metrics = export_career()
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

    print("SESSION30_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_session_30()

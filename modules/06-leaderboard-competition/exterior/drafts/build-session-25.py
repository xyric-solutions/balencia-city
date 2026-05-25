"""
Balencia City v3 - Module #06 Leaderboard & Competition
Session 25: Exterior Major Forms

Open-top arena colosseum with rising tiers, four victory pillars, curved leaderboard
display, raised competitor walkway, and an apex lightning receiver.
"""

import importlib.util
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/06-leaderboard-competition")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
BLEND_FILE = os.path.join(DRAFTS, "leaderboard-competition-s25-major-forms.blend")
METRICS_FILE = os.path.join(DRAFTS, "session25-metrics.json")

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
    if obj.type != "MESH":
        return obj
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


def make_mesh(name, verts, faces, mat):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    return obj


def arc_band(name, outer_r, inner_r, z0, z1, start_deg, end_deg, mat, segments=48, closed=False):
    start = math.radians(start_deg)
    end = math.radians(end_deg)
    points = segments if closed else segments + 1
    verts = []
    for i in range(points):
        t = i / segments
        if closed:
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
    face_count = segments if closed else segments
    for i in range(face_count):
        j = (i + 1) % points
        a = i * 4
        b = j * 4
        faces.append((a + 0, b + 0, b + 1, a + 1))  # outer wall
        faces.append((a + 1, b + 1, b + 2, a + 2))  # top deck
        faces.append((a + 2, b + 2, b + 3, a + 3))  # inner wall
        faces.append((a + 3, b + 3, b + 0, a + 0))  # bottom
    if not closed:
        faces.append((0, 1, 2, 3))
        n = segments * 4
        faces.append((n + 3, n + 2, n + 1, n + 0))
    return make_mesh(name, verts, faces, mat)


def ring_band(name, outer_r, inner_r, z0, z1, mat, segments=64):
    return arc_band(name, outer_r, inner_r, z0, z1, 0, 360, mat, segments=segments, closed=True)


def arc_panel(name, radius, z_center, height, thickness, start_deg, end_deg, mat, segments=24):
    return arc_band(
        name,
        radius + thickness * 0.5,
        radius - thickness * 0.5,
        z_center - height * 0.5,
        z_center + height * 0.5,
        start_deg,
        end_deg,
        mat,
        segments=segments,
        closed=False,
    )


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


def cone(name, loc, radius1, radius2, depth, mat, vertices=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices, radius1=radius1, radius2=radius2, depth=depth, location=loc, rotation=rot
    )
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    apply_transforms(obj)
    return obj


def torus(name, loc, major, minor, mat, seg=72, minor_seg=8):
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


def cylinder_between(name, start, end, radius, mat, vertices=12):
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


def object_metrics():
    rows = []
    for obj in sorted((o for o in bpy.data.objects if o.type == "MESH"), key=lambda o: o.name):
        rows.append(
            {
                "name": obj.name,
                "tris": get_tri_count(obj),
                "material": obj.data.materials[0].name.split(".")[0] if obj.data.materials else "NONE",
            }
        )
    return rows


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


def build_scene():
    print("=== Session 25: Leaderboard exterior major forms ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lighting.setup_viewport_lighting()
    mats = materials_mod.create_materials("#FB7185", include_energy=True, include_holo=False)
    cleanup_slot_names()

    light_count = sum(1 for obj in bpy.data.objects if obj.type == "LIGHT")
    camera_count = sum(1 for obj in bpy.data.objects if obj.type == "CAMERA")
    print(f"Scene setup: {light_count} lights, {camera_count} camera, materials={list(mats.keys())}")

    # 1. Monumental arena foundation and rising shell.
    ring_band("arena_ground_plinth_outer_disc", 9.2, 3.7, 0.00, 0.28, mats["base"], 40)
    ring_band("arena_inner_floor_void_shadow", 3.65, 1.05, 0.02, 0.08, mats["glass"], 32)
    ring_band("arena_lower_service_podium", 8.55, 4.05, 0.28, 0.72, mats["base"], 40)

    for i in range(8):
        z0 = 0.82 + i * 0.75
        z1 = z0 + 0.42
        outer_r = 7.45 + i * 0.14
        inner_r = 4.15 + i * 0.43
        mat = mats["base"] if i < 4 else mats["detail"]
        if i < 4:
            arc_band(
                f"arena_outer_tier_band_{i:02d}_with_entrance_gap",
                outer_r,
                inner_r,
                z0,
                z1,
                -76,
                256,
                mat,
                segments=32,
                closed=False,
            )
        else:
            ring_band(f"arena_outer_tier_band_{i:02d}", outer_r, inner_r, z0, z1, mat, segments=36)

        if i < 7:
            ring_band(
                f"arena_dark_facade_gap_band_{i:02d}",
                outer_r + 0.03,
                outer_r - 0.13,
                z1 + 0.08,
                z1 + 0.28,
                mats["glass"],
                segments=32,
            )

    # 2. Interior bowl seating, visible through the open roof.
    for i in range(7):
        inner = 2.0 + i * 0.62
        outer = inner + 0.48
        z0 = 0.62 + i * 0.46
        z1 = z0 + 0.18
        ring_band(f"visible_stepped_seating_ring_{i:02d}", outer, inner, z0, z1, mats["detail"], 28)

    ring_band("competition_floor_major_disc", 2.0, 0.0, 0.12, 0.20, mats["base"], 32)
    ring_band("competition_floor_energy_target_ring", 1.35, 1.12, 0.23, 0.29, mats["energy"], 32)

    # 3. Thick open-roof rim and internal receiver ring.
    torus("structural_top_rim_ring_open_roof", (0, 0, 6.72), 8.55, 0.18, mats["detail"], 48, 6)
    torus("inner_bowl_guard_rim", (0, 0, 6.12), 6.55, 0.075, mats["accent"], 44, 5)
    torus("apex_lightning_receiver_ring", (0, 0, 7.28), 0.95, 0.075, mats["energy"], 32, 5)

    # 4. Grand entrance archway and ceremonial approach.
    front_y = -8.72
    box("grand_entrance_left_pillar", (-1.85, front_y, 1.98), (0.34, 0.44, 1.98), mats["accent"])
    box("grand_entrance_right_pillar", (1.85, front_y, 1.98), (0.34, 0.44, 1.98), mats["accent"])
    box("grand_entrance_shadow_opening", (0, front_y - 0.06, 1.78), (1.48, 0.08, 1.62), mats["glass"])
    box("grand_entrance_threshold_block", (0, front_y - 0.42, 0.28), (2.65, 0.82, 0.28), mats["base"])

    arch_center_z = 3.90
    arch_radius = 1.78
    arch_points = []
    for step in range(19):
        theta = math.pi - (math.pi * step / 18)
        arch_points.append((arch_radius * math.cos(theta), front_y, arch_center_z + arch_radius * math.sin(theta)))
    for i in range(len(arch_points) - 1):
        cylinder_between(f"grand_entrance_curved_arch_segment_{i:02d}", arch_points[i], arch_points[i + 1], 0.16, mats["accent"], 8)

    box("competitor_walkway_main_slab", (0, -12.95, 0.18), (1.35, 4.28, 0.16), mats["base"])
    box("competitor_walkway_left_coral_edge", (-1.42, -12.95, 0.36), (0.055, 4.35, 0.055), mats["accent"])
    box("competitor_walkway_right_coral_edge", (1.42, -12.95, 0.36), (0.055, 4.35, 0.055), mats["accent"])
    box("competitor_walkway_entry_step", (0, -16.95, 0.10), (1.75, 0.70, 0.10), mats["base"])

    # 5. Victory pillars at cardinal points.
    pillar_radius = 9.18
    diagonal = pillar_radius / math.sqrt(2)
    cardinal = [
        ("north_east", diagonal, diagonal),
        ("south_east", diagonal, -diagonal),
        ("south_west", -diagonal, -diagonal),
        ("north_west", -diagonal, diagonal),
    ]
    for name, x, y in cardinal:
        angle = math.atan2(y, x)
        box(f"victory_pillar_{name}_footing", (x, y, 0.42), (0.72, 0.72, 0.32), mats["base"], rot_z=angle)
        cylinder(f"victory_pillar_{name}_shaft", (x, y, 4.66), 0.22, 8.15, mats["detail"], vertices=12)
        torus(f"victory_pillar_{name}_beacon_collar", (x, y, 8.90), 0.34, 0.055, mats["accent"], 20, 4)
        cone(f"victory_pillar_{name}_energy_flame", (x, y, 9.38), 0.31, 0.045, 0.92, mats["emissive"], vertices=12)
        cylinder(f"victory_pillar_{name}_orange_core", (x, y, 9.40), 0.105, 0.72, mats["energy"], vertices=10)

    # 6. Curved exterior leaderboard screen wrapping a 90 degree arc.
    arc_panel("curved_leaderboard_display_main_panel", 8.88, 3.82, 1.12, 0.08, -70, 20, mats["emissive"], 18)
    for row in range(5):
        z = 3.42 + row * 0.18
        start = -63 + row * 2
        end = -12 - row * 3
        arc_panel(f"leaderboard_rank_bar_{row + 1:02d}", 8.96, z, 0.055, 0.045, start, end, mats["accent"], 6)

    # 7. Lightning receiver marker, deliberately not the final SIA pipeline.
    lightning_points = [(0.18, 0.0, 10.65), (-0.30, 0.16, 9.58), (0.26, -0.10, 8.54), (-0.08, 0.04, 7.45)]
    for i in range(len(lightning_points) - 1):
        cylinder_between(f"apex_lightning_major_form_segment_{i:02d}", lightning_points[i], lightning_points[i + 1], 0.08, mats["energy"], 8)
    cone("apex_strike_socket_core", (0, 0, 7.18), 0.26, 0.05, 0.58, mats["energy"], vertices=10)

    # 8. Four radial structural braces pointing to the apex receiver.
    for idx, angle in enumerate([0, math.pi / 2, math.pi, math.pi * 1.5]):
        start = (math.cos(angle) * 6.6, math.sin(angle) * 6.6, 6.22)
        end = (math.cos(angle) * 1.35, math.sin(angle) * 1.35, 7.06)
        cylinder_between(f"apex_radial_brace_{idx:02d}", start, end, 0.055, mats["detail"], 8)

    cleanup_slot_names()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.image_settings.file_format = "PNG"

    screenshots = [
        render_shot("s25_front_elevation.png", (0, -24, 6.2), (0, 0, 4.6), 38),
        render_shot("s25_three_quarter.png", (17, -22, 9.0), (0, 0, 4.8), 38),
        render_shot("s25_distance_view.png", (28, -35, 16), (0, 0, 4.8), 42),
    ]

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    metrics = {
        "session": 25,
        "module": "06-leaderboard-competition",
        "blend": BLEND_FILE,
        "screenshots": screenshots,
        "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "triangles": scene_triangles(),
        "materials": sorted([m.name for m in bpy.data.materials]),
        "material_tris": material_triangles(),
        "objects": object_metrics(),
        "lights": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
        "cameras": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
        "bbox": {},
    }

    mesh_objs = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    coords = []
    for obj in mesh_objs:
        for corner in obj.bound_box:
            coords.append(obj.matrix_world @ Vector(corner))
    if coords:
        metrics["bbox"] = {
            "min": [round(min(v[i] for v in coords), 4) for i in range(3)],
            "max": [round(max(v[i] for v in coords), 4) for i in range(3)],
        }

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

    print("SESSION25_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_scene()

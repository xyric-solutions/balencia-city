"""
Balencia City v3 -- Module #05 Chat & Communication
Session 23: Interior -- Communication Nexus

Fresh interior scene with a circular communication room, conversation-thread
focal web, calling booths, whiteboards, message paths, table/seats, ceiling
lattice, required empties, screenshots, blend save, and GLB export.
"""

import json
import math
import os
import random
from mathutils import Vector

import bpy


MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/05-chat-communication"
SHARED_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared"
DRAFTS_DIR = os.path.join(MODULE_DIR, "interior", "drafts")
APPROVED_DIR = os.path.join(MODULE_DIR, "interior", "approved")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")

BLEND_FILE = os.path.join(DRAFTS_DIR, "chat-communication-int-session23.blend")
DRAFT_GLB = os.path.join(DRAFTS_DIR, "chat-int-draft-s23.glb")
METRICS_FILE = os.path.join(DRAFTS_DIR, "session23-metrics.json")

random.seed(23)
os.makedirs(DRAFTS_DIR, exist_ok=True)
os.makedirs(APPROVED_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


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


def apply_transforms(obj):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)


def shade(obj):
    if obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        try:
            bpy.ops.object.shade_smooth()
        except Exception:
            pass
        obj.select_set(False)


def active_object():
    return getattr(bpy.context, "active_object", None) or bpy.context.object


def make_box(name, loc, dims, slot, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rotation)
    obj = active_object()
    obj.name = name
    obj.scale = dims
    assign_mat(obj, slot)
    apply_transforms(obj)
    return obj


def make_cylinder(name, loc, radius, depth, slot, vertices=24, rotation=(0, 0, 0)):
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


def make_uv_sphere(name, loc, radius, slot, segments=12, rings=6):
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


def make_torus(name, loc, major_radius, minor_radius, slot, rotation=(0, 0, 0), major_segments=32, minor_segments=6):
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


def make_cylinder_between(name, start, end, radius, slot, vertices=12):
    start_v = Vector(start)
    end_v = Vector(end)
    mid = (start_v + end_v) * 0.5
    direction = end_v - start_v
    length = direction.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=mid)
    obj = active_object()
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign_mat(obj, slot)
    apply_transforms(obj)
    shade(obj)
    return obj


def make_ribbon(name, start, end, arch_height, width, slot, segments=28, wave=0.0):
    start_v = Vector(start)
    end_v = Vector(end)
    verts = []
    faces = []
    for i in range(segments + 1):
        t = i / segments
        p = start_v.lerp(end_v, t)
        p.z += math.sin(math.pi * t) * arch_height
        p.z += math.sin(t * math.pi * 4.0) * wave
        tangent = (end_v - start_v).normalized()
        perp = Vector((-tangent.y, tangent.x, 0.0))
        if perp.length < 0.01:
            perp = Vector((1.0, 0.0, 0.0))
        perp.normalize()
        verts.append(tuple(p + perp * width * 0.5))
        verts.append(tuple(p - perp * width * 0.5))
    for i in range(segments):
        a = i * 2
        faces.append((a, a + 1, a + 3, a + 2))
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign_mat(obj, slot)
    return obj


def make_diamond_particles(name, positions, radius, slot):
    verts = []
    faces = []
    for pos in positions:
        x, y, z = pos
        base = len(verts)
        verts.extend(
            [
                (x, y, z + radius),
                (x, y, z - radius),
                (x + radius, y, z),
                (x - radius, y, z),
                (x, y + radius, z),
                (x, y - radius, z),
            ]
        )
        faces.extend(
            [
                (base + 0, base + 2, base + 4),
                (base + 0, base + 4, base + 3),
                (base + 0, base + 3, base + 5),
                (base + 0, base + 5, base + 2),
                (base + 1, base + 4, base + 2),
                (base + 1, base + 3, base + 4),
                (base + 1, base + 5, base + 3),
                (base + 1, base + 2, base + 5),
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


def make_camera(name, loc, target, lens=35):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.1
    data.clip_end = 200
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
    bpy.ops.render.render(write_still=True)


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


print("=== Session 23: Chat Communication Interior ===")
print("Phase 1: Fresh scene")
bpy.ops.wm.read_factory_settings(use_empty=True)

print("Phase 2: Lighting rig")
lighting = load_python_module(os.path.join(SHARED_DIR, "lighting-rig.py"), "lighting_rig")
lighting["clear_lighting"]()
lighting["setup_viewport_lighting"]()

print("Phase 3: Material library")
material_library = load_python_module(os.path.join(SHARED_DIR, "material-library.py"), "material_library")
MATS = material_library["create_materials"]("#FF5E00", include_energy=True, include_holo=False)
assert "holo" not in MATS

print("Phase 4: Circular room shell")
ROOM_R = 5.0
ROOM_H = 6.4
WALL_THICK = 0.12

make_cylinder("circular_room_floor_disc", (0, 0, 0.06), ROOM_R, 0.12, "base", vertices=48)
make_torus("floor_outer_service_ring", (0, 0, 0.16), ROOM_R - 0.12, 0.035, "detail", major_segments=48)
make_torus("floor_inner_signal_ring", (0, 0, 0.18), 1.65, 0.025, "accent", major_segments=36)
make_cylinder("circular_room_ceiling_disc", (0, 0, ROOM_H), ROOM_R, 0.14, "base", vertices=48)

wall_angles = [-30, 0, 30, 60, 90, 120, 150, 180, 210]
for idx, deg in enumerate(wall_angles):
    angle = math.radians(deg)
    x = math.cos(angle) * ROOM_R
    y = math.sin(angle) * ROOM_R
    tangent_rot = angle + math.pi / 2.0
    make_box(
        f"curved_wall_panel_{idx:02d}",
        (x, y, ROOM_H * 0.5),
        (2.0, WALL_THICK, ROOM_H),
        "base",
        rotation=(0, 0, tangent_rot),
    )
    if idx % 2 == 0:
        make_box(
            f"curved_wall_inactive_interface_{idx:02d}",
            (math.cos(angle) * (ROOM_R - 0.08), math.sin(angle) * (ROOM_R - 0.08), ROOM_H * 0.52),
            (0.72, 0.035, 2.3),
            "glass",
            rotation=(0, 0, tangent_rot),
        )

for idx, x in enumerate([-2.85, 2.85]):
    make_box(f"front_city_window_glass_{idx}", (x, -ROOM_R - 0.03, 3.2), (1.35, 0.05, 4.2), "glass")
for idx, x in enumerate([-3.65, -1.95, 1.95, 3.65]):
    make_box(f"front_window_mullion_{idx}", (x, -ROOM_R - 0.01, 3.2), (0.08, 0.10, 4.45), "detail")
make_box("front_window_top_lintel", (0, -ROOM_R - 0.01, 5.45), (7.3, 0.12, 0.16), "accent")
make_box("front_window_bottom_sill", (0, -ROOM_R - 0.01, 1.05), (7.3, 0.14, 0.18), "detail")

print("Phase 5: Floor channels and ceiling lattice")
for idx, deg in enumerate([0, 45, 90, 135, 180, 225, 315]):
    angle = math.radians(deg)
    length = ROOM_R * 0.68
    x = math.cos(angle) * length * 0.5
    y = math.sin(angle) * length * 0.5
    make_box(
        f"floor_signal_channel_{idx:02d}",
        (x, y, 0.19),
        (length, 0.045, 0.035),
        "accent",
        rotation=(0, 0, angle),
    )

for idx, x in enumerate([-3.0, -1.5, 0.0, 1.5, 3.0]):
    make_box(f"ceiling_lattice_x_{idx}", (x, 0, ROOM_H - 0.28), (0.055, 8.6, 0.075), "detail")
for idx, y in enumerate([-3.0, -1.5, 0.0, 1.5, 3.0]):
    make_box(f"ceiling_lattice_y_{idx}", (0, y, ROOM_H - 0.24), (8.6, 0.055, 0.075), "detail")
make_torus("ceiling_skybridge_hub_ring", (0, 0, ROOM_H - 0.22), 1.25, 0.035, "accent", major_segments=36)

print("Phase 6: Focal conversation-thread web")
focal_center = (0, 0, 3.25)
make_uv_sphere("conversation_hub_core", focal_center, 0.28, "emissive", segments=16, rings=8)
make_torus("conversation_orbit_ring_flat", focal_center, 1.05, 0.025, "emissive", major_segments=40)
make_torus(
    "conversation_orbit_ring_tilt_a",
    focal_center,
    1.35,
    0.022,
    "emissive",
    rotation=(math.radians(58), 0, math.radians(24)),
    major_segments=40,
)
make_torus(
    "conversation_orbit_ring_tilt_b",
    focal_center,
    1.65,
    0.020,
    "energy",
    rotation=(math.radians(-45), math.radians(18), math.radians(-35)),
    major_segments=40,
)

booth_points = {
    "north": (0, 3.55, 1.55),
    "east": (3.55, 0, 1.55),
    "south": (0, -3.55, 1.55),
    "west": (-3.55, 0, 1.55),
}
for idx, (label, point) in enumerate(booth_points.items()):
    make_ribbon(f"conversation_ribbon_center_{label}", (0, 0, 2.7), point, 1.55, 0.11, "emissive", wave=0.08)
    make_ribbon(
        f"conversation_ribbon_secondary_{label}",
        (0.25 * math.cos(idx), 0.25 * math.sin(idx), 3.05),
        (point[0] * 0.93, point[1] * 0.93, 1.95),
        1.15,
        0.055,
        "energy",
        segments=24,
        wave=0.05,
    )

ring_pairs = [
    ("north_east", booth_points["north"], booth_points["east"]),
    ("east_south", booth_points["east"], booth_points["south"]),
    ("south_west", booth_points["south"], booth_points["west"]),
    ("west_north", booth_points["west"], booth_points["north"]),
]
for label, start, end in ring_pairs:
    make_ribbon(f"booth_to_booth_thread_{label}", start, end, 1.85, 0.055, "emissive", segments=26, wave=0.04)

particle_positions = []
for i in range(60):
    angle = (i / 60.0) * math.tau
    radius = 0.8 + (i % 9) * 0.29
    z = 2.05 + (i % 6) * 0.33 + math.sin(angle * 3) * 0.18
    particle_positions.append((math.cos(angle) * radius, math.sin(angle) * radius, z))
make_diamond_particles("message_particle_packets", particle_positions, 0.055, "energy")

print("Phase 7: Collaboration table and seating")
make_cylinder("central_collaboration_table_top", (0, 0, 0.72), 1.35, 0.16, "detail", vertices=32)
make_cylinder("central_collaboration_table_core", (0, 0, 0.43), 0.32, 0.52, "base", vertices=24)
make_torus("table_underlight_ring", (0, 0, 0.64), 1.18, 0.025, "emissive", major_segments=36)

for idx in range(8):
    angle = idx * math.tau / 8.0
    x = math.cos(angle) * 2.15
    y = math.sin(angle) * 2.15
    rot = angle + math.pi
    make_box(f"seat_pod_{idx:02d}_pan", (x, y, 0.45), (0.34, 0.40, 0.16), "detail", rotation=(0, 0, rot))
    make_box(
        f"seat_pod_{idx:02d}_back",
        (x + math.cos(angle) * 0.17, y + math.sin(angle) * 0.17, 0.82),
        (0.36, 0.08, 0.58),
        "base",
        rotation=(0, 0, rot),
    )
    make_box(
        f"seat_pod_{idx:02d}_accent_rib",
        (x - math.cos(angle) * 0.03, y - math.sin(angle) * 0.03, 0.61),
        (0.28, 0.045, 0.06),
        "accent",
        rotation=(0, 0, rot),
    )

print("Phase 8: Calling booths")
for idx, (label, (x, y, _z)) in enumerate(booth_points.items()):
    angle = math.atan2(y, x)
    make_cylinder(f"calling_booth_{label}_glass_shell", (x, y, 1.42), 0.48, 2.45, "glass", vertices=18)
    make_cylinder(f"calling_booth_{label}_base_ring", (x, y, 0.22), 0.56, 0.18, "detail", vertices=18)
    make_torus(f"calling_booth_{label}_top_signal_ring", (x, y, 2.66), 0.50, 0.035, "accent", major_segments=24)
    for rail_idx, offset in enumerate([0, math.pi / 2, math.pi, math.pi * 1.5]):
        rx = x + math.cos(offset) * 0.50
        ry = y + math.sin(offset) * 0.50
        make_cylinder_between(
            f"calling_booth_{label}_vertical_rail_{rail_idx}",
            (rx, ry, 0.35),
            (rx, ry, 2.55),
            0.025,
            "detail",
            vertices=8,
        )
    make_box(
        f"calling_booth_{label}_remote_projection",
        (x - math.cos(angle) * 0.08, y - math.sin(angle) * 0.08, 1.45),
        (0.42, 0.035, 1.20),
        "emissive",
        rotation=(0, 0, angle + math.pi / 2),
    )
    make_uv_sphere(
        f"calling_booth_{label}_projection_head",
        (x - math.cos(angle) * 0.08, y - math.sin(angle) * 0.08, 2.18),
        0.14,
        "emissive",
        segments=8,
        rings=4,
    )

print("Phase 9: Whiteboards and communication panels")
whiteboards = [
    ("left", (-2.65, -1.8, 2.55), math.radians(34)),
    ("right", (2.75, -1.65, 2.7), math.radians(-32)),
    ("rear", (0.0, 2.9, 2.65), 0.0),
]
for label, loc, rot_z in whiteboards:
    make_box(f"whiteboard_{label}_glass_panel", loc, (1.40, 0.045, 0.84), "glass", rotation=(0, 0, rot_z))
    make_box(
        f"whiteboard_{label}_top_frame",
        (loc[0], loc[1], loc[2] + 0.46),
        (1.48, 0.055, 0.055),
        "detail",
        rotation=(0, 0, rot_z),
    )
    for line_idx in range(5):
        line_z = loc[2] - 0.27 + line_idx * 0.13
        line_x = loc[0] + ((line_idx % 2) - 0.5) * 0.18
        make_box(
            f"whiteboard_{label}_notation_{line_idx}",
            (line_x, loc[1] - 0.035, line_z),
            (0.52 + 0.12 * (line_idx % 3), 0.035, 0.025),
            "emissive",
            rotation=(0, 0, rot_z + math.radians(2 * line_idx)),
        )

for idx, deg in enumerate([35, 75, 115, 155, 205, 325]):
    angle = math.radians(deg)
    x = math.cos(angle) * (ROOM_R - 0.22)
    y = math.sin(angle) * (ROOM_R - 0.22)
    rot = angle + math.pi / 2.0
    make_box(f"perimeter_message_panel_{idx:02d}", (x, y, 3.55), (0.82, 0.035, 0.52), "glass", rotation=(0, 0, rot))
    make_box(f"perimeter_message_panel_trim_{idx:02d}", (x, y, 3.88), (0.92, 0.045, 0.05), "accent", rotation=(0, 0, rot))

print("Phase 10: Guided message tubes")
for idx, (label, start, end) in enumerate(ring_pairs):
    make_cylinder_between(
        f"overhead_message_conduit_{label}",
        (start[0] * 0.86, start[1] * 0.86, 5.25),
        (end[0] * 0.86, end[1] * 0.86, 5.25),
        0.035,
        "energy",
        vertices=10,
    )
for idx, deg in enumerate([0, 60, 120, 180, 240, 300]):
    angle = math.radians(deg)
    make_uv_sphere(
        f"ceiling_message_packet_{idx:02d}",
        (math.cos(angle) * 2.8, math.sin(angle) * 2.8, 5.25),
        0.09,
        "energy",
        segments=8,
        rings=4,
    )

print("Phase 11: Runtime empties")
create_empty("light_0", (0, 0, 5.45), 0.45)
create_empty("light_1", (0, 3.95, 2.55), 0.45)
create_empty("light_2", (0, 0, 0.65), 0.45)
create_empty("camera_target", (0, 0, 3.18), 0.55)

print("Phase 12: Metrics and material audit")
valid_slots = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
material_issues = []
slot_tris = {}
object_groups = {}
for obj in bpy.data.objects:
    if obj.type != "MESH":
        continue
    if not obj.data.materials:
        material_issues.append(f"{obj.name}: no material")
        continue
    slot = obj.data.materials[0].name
    if slot not in valid_slots:
        material_issues.append(f"{obj.name}: invalid material {slot}")
    count = tri_count(obj)
    slot_tris[slot] = slot_tris.get(slot, 0) + count
    group = obj.name.split("_")[0]
    if obj.name.startswith("calling_booth"):
        group = "calling_booth"
    elif obj.name.startswith("conversation") or obj.name.startswith("booth_to_booth") or obj.name.startswith("message_particle"):
        group = "conversation_web"
    elif obj.name.startswith("whiteboard"):
        group = "whiteboard"
    elif obj.name.startswith("seat"):
        group = "seat_pods"
    elif obj.name.startswith("ceiling") or obj.name.startswith("overhead"):
        group = "ceiling_lattice"
    elif obj.name.startswith("curved_wall") or obj.name.startswith("front") or obj.name.startswith("perimeter"):
        group = "room_shell"
    object_groups.setdefault(group, {"count": 0, "tris": 0})
    object_groups[group]["count"] += 1
    object_groups[group]["tris"] += count

total_tris = sum(slot_tris.values())
mesh_count = sum(1 for obj in bpy.data.objects if obj.type == "MESH")
empty_names = sorted(obj.name for obj in bpy.data.objects if obj.type == "EMPTY")
print(f"  Mesh objects: {mesh_count}")
print(f"  Total tris: {total_tris}")
print(f"  Slot tris: {slot_tris}")
print(f"  Empties: {empty_names}")
if material_issues:
    print("  Material issues:")
    for issue in material_issues:
        print("   - " + issue)

print("Phase 13: Preview cameras and screenshots")
overview_cam = make_camera("S23_Overview_Camera", (7.4, -9.0, 6.4), (0, 0, 2.8), lens=32)
entrance_cam = make_camera("S23_Entrance_Camera", (0, -8.4, 2.7), (0, 0, 2.8), lens=34)
top_cam = make_camera("S23_Topdown_Camera", (0, -0.2, 12.0), (0, 0, 0.4), lens=38)

render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s23-int-overview.png"))
render_still(entrance_cam, os.path.join(SCREENSHOTS_DIR, "s23-int-from-entrance.png"))
render_still(top_cam, os.path.join(SCREENSHOTS_DIR, "s23-int-topdown.png"))
previous_emissions = set_all_emission_strength(0.0)
render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s23-int-dark-first.png"))
restore_emission_strength(previous_emissions)

print("Phase 14: Save blend")
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

print("Phase 15: Export draft GLB")
root = bpy.data.objects.new("chat-int", None)
bpy.context.collection.objects.link(root)
root.empty_display_type = "PLAIN_AXES"
root.empty_display_size = 0.1
for obj in list(bpy.data.objects):
    if obj == root:
        continue
    if obj.type in {"MESH", "EMPTY"} and obj.parent is None and not obj.name.startswith("S23_"):
        obj.parent = root

bpy.ops.object.select_all(action="DESELECT")
for obj in bpy.data.objects:
    if obj.type in {"MESH", "EMPTY"} and obj.name not in {"S23_Overview_Camera", "S23_Entrance_Camera", "S23_Topdown_Camera"}:
        obj.select_set(True)
    else:
        obj.select_set(False)

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
try:
    bpy.ops.export_scene.gltf(**export_kwargs, export_apply_modifiers=True)
except TypeError:
    bpy.ops.export_scene.gltf(**export_kwargs)

file_size = os.path.getsize(DRAFT_GLB)
metrics = {
    "session": 23,
    "module": "05-chat-communication",
    "mesh_objects": mesh_count,
    "empty_names": empty_names,
    "total_tris": total_tris,
    "slot_tris": slot_tris,
    "object_groups": object_groups,
    "material_issues": material_issues,
    "blend_file": BLEND_FILE,
    "draft_glb": DRAFT_GLB,
    "glb_size_bytes": file_size,
    "screenshots": [
        "screenshots/s23-int-overview.png",
        "screenshots/s23-int-from-entrance.png",
        "screenshots/s23-int-topdown.png",
        "screenshots/s23-int-dark-first.png",
    ],
}
with open(METRICS_FILE, "w") as handle:
    json.dump(metrics, handle, indent=2, sort_keys=True)

print("=" * 70)
print("SESSION 23 BUILD COMPLETE")
print(f"Blend: {BLEND_FILE}")
print(f"Draft GLB: {DRAFT_GLB}")
print(f"GLB size: {file_size / 1024:.1f} KB")
print(f"Tris: {total_tris}")
print(f"Meshes: {mesh_count}")
print(f"Empties: {empty_names}")
print(f"Metrics: {METRICS_FILE}")

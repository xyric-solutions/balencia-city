import importlib.util
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/05-chat-communication")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
APPROVED = os.path.join(MODULE, "exterior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
S21_BLEND = os.path.join(DRAFTS, "chat-communication-s21-major-forms.blend")
S22A_BLEND = os.path.join(DRAFTS, "chat-communication-s22a-form-reinforcement.blend")
S22B_BLEND = os.path.join(DRAFTS, "chat-communication-s22b-detail-export.blend")
CHAT_GLB = os.path.join(APPROVED, "chat-ext.glb")

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting", os.path.join(ROOT, "shared/lighting-rig.py"))
materials_mod = load_module("balencia_materials", os.path.join(ROOT, "shared/material-library.py"))


def count_tris():
    total = 0
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        obj.data.calc_loop_triangles()
        total += len(obj.data.loop_triangles)
    return total


def material_tris():
    totals = {}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        obj.data.calc_loop_triangles()
        mat = obj.data.materials[0].name if obj.data.materials else "NONE"
        mat = mat.split(".")[0]
        totals[mat] = totals.get(mat, 0) + len(obj.data.loop_triangles)
    return dict(sorted(totals.items()))


def mesh_count():
    return sum(1 for obj in bpy.data.objects if obj.type == "MESH")


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for block in list(collection):
            if not block.users:
                collection.remove(block)


def cleanup_names():
    for mat in bpy.data.materials:
        base = mat.name.split(".")[0]
        if base in {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}:
            mat.name = base


def chamfer_points(w, d, c):
    c = min(c, w * 0.35, d * 0.35)
    return [
        (-w / 2 + c, -d / 2),
        (w / 2 - c, -d / 2),
        (w / 2, -d / 2 + c),
        (w / 2, d / 2 - c),
        (w / 2 - c, d / 2),
        (-w / 2 + c, d / 2),
        (-w / 2, d / 2 - c),
        (-w / 2, -d / 2 + c),
    ]


def make_prism(name, loc, rings, mat, chamfer=0.22):
    verts = []
    faces = []
    for z, w, d in rings:
        for x, y in chamfer_points(w, d, chamfer):
            verts.append((loc[0] + x, loc[1] + y, loc[2] + z))
    n = 8
    for level in range(len(rings) - 1):
        a = level * n
        b = (level + 1) * n
        for i in range(n):
            faces.append((a + i, a + (i + 1) % n, b + (i + 1) % n, b + i))
    faces.append(tuple(range(n - 1, -1, -1)))
    top = (len(rings) - 1) * n
    faces.append(tuple(range(top, top + n)))
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
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


def box_mesh(name, boxes, mat):
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
    return obj


def add_box(name, loc, dims, mat, rot_z=0.0):
    return box_mesh(name, [(loc, dims, rot_z)], mat)


def cylinder_between(name, start, end, radius, mat, vertices=12):
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
    return obj


def tube_mesh(name, start, end, radius, mat, sides=14, steps=10, lift=0.0, offset=(0, 0, 0)):
    start = Vector(start) + Vector(offset)
    end = Vector(end) + Vector(offset)
    control = (start + end) * 0.5 + Vector((0, 0, lift))
    verts = []
    faces = []
    rings = []
    prev_normal = None
    for s in range(steps + 1):
        t = s / steps
        p = ((1 - t) ** 2) * start + 2 * (1 - t) * t * control + (t**2) * end
        tangent = (2 * (1 - t) * (control - start) + 2 * t * (end - control)).normalized()
        up = Vector((0, 0, 1))
        if abs(tangent.dot(up)) > 0.92:
            up = Vector((1, 0, 0))
        normal = tangent.cross(up).normalized()
        if prev_normal and normal.dot(prev_normal) < 0:
            normal.negate()
        binormal = tangent.cross(normal).normalized()
        prev_normal = normal.copy()
        ring = []
        for i in range(sides):
            angle = math.tau * i / sides
            v = p + math.cos(angle) * radius * normal + math.sin(angle) * radius * binormal
            ring.append(len(verts))
            verts.append(tuple(v))
        rings.append(ring)
    for s in range(steps):
        for i in range(sides):
            faces.append((rings[s][i], rings[s][(i + 1) % sides], rings[s + 1][(i + 1) % sides], rings[s + 1][i]))
    faces.append(tuple(reversed(rings[0])))
    faces.append(tuple(rings[-1]))
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    return obj


def cone_between(name, start, end, radius1, radius2, mat, vertices=12):
    start = Vector(start)
    end = Vector(end)
    direction = end - start
    length = direction.length
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2, depth=length, location=(start + end) * 0.5)
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign(obj, mat)
    return obj


def torus(name, loc, major, minor, mat, seg=28, minor_seg=8):
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
    return obj


def dish(name, center, radius, depth, normal, mat, segments=24, rings=5):
    normal = Vector(normal).normalized()
    up = Vector((0, 0, 1))
    if abs(normal.dot(up)) > 0.9:
        up = Vector((1, 0, 0))
    tangent = up.cross(normal).normalized()
    vertical = normal.cross(tangent).normalized()
    center = Vector(center)
    verts = [tuple(center - normal * depth)]
    faces = []
    ring_indices = []
    for r_i in range(1, rings + 1):
        r = radius * r_i / rings
        offset = depth * (r / radius) ** 2
        ring = []
        for i in range(segments):
            angle = math.tau * i / segments
            pos = center + tangent * math.cos(angle) * r + vertical * math.sin(angle) * r + normal * offset
            ring.append(len(verts))
            verts.append(tuple(pos))
        ring_indices.append(ring)
    first = ring_indices[0]
    for i in range(segments):
        faces.append((0, first[i], first[(i + 1) % segments]))
    for a, b in zip(ring_indices[:-1], ring_indices[1:]):
        for i in range(segments):
            faces.append((a[i], b[i], b[(i + 1) % segments], a[(i + 1) % segments]))
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    return obj


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_shot(filename, camera_loc, target, lens=42):
    cam_data = bpy.data.cameras.new("Shot_Camera")
    cam = bpy.data.objects.new("Shot_Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    cam_data.lens = lens
    cam_data.clip_end = 250
    look_at(cam, target)
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = os.path.join(SCREENSHOTS, filename)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)


def setup_scene():
    clear_scene()
    mats = materials_mod.create_materials("#FF5E00", include_energy=True, include_holo=False)
    lighting.clear_lighting()
    lighting.setup_viewport_lighting()
    cleanup_names()
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    try:
        bpy.context.scene.eevee.taa_render_samples = 32
    except Exception:
        pass
    return mats


towers = {
    "A": {"loc": (0.0, 0.0), "h": 12.0, "w": 2.25, "d": 1.8, "floors": 30},
    "B": {"loc": (-4.3, 0.7), "h": 11.2, "w": 2.05, "d": 1.68, "floors": 28},
    "C": {"loc": (2.7, -2.25), "h": 10.4, "w": 1.95, "d": 1.6, "floors": 26},
    "D": {"loc": (5.15, 0.9), "h": 10.0, "w": 1.85, "d": 1.55, "floors": 25},
}


def build_tower_shells(mats):
    for key, t in towers.items():
        x, y = t["loc"]
        h, w, d = t["h"], t["w"], t["d"]
        make_prism(
            f"chat_pod_{key}_tapered_octagonal_body",
            (x, y, 0),
            [
                (0.0, w * 1.10, d * 1.08),
                (0.75, w * 1.02, d * 1.02),
                (h * 0.36, w * 0.96, d * 1.04),
                (h * 0.68, w * 0.88, d * 0.97),
                (h, w * 0.78, d * 0.88),
            ],
            mats["base"],
            chamfer=0.26,
        )
        make_prism(
            f"chat_pod_{key}_podium_flare",
            (x, y, 0),
            [(0, w * 1.62, d * 1.48), (0.34, w * 1.42, d * 1.34), (0.68, w * 1.22, d * 1.18)],
            mats["base"],
            chamfer=0.30,
        )
        make_prism(
            f"chat_pod_{key}_crown_cap",
            (x, y, h),
            [(0, w * 0.96, d * 1.02), (0.32, w * 1.12, d * 1.18), (0.56, w * 0.86, d * 0.92)],
            mats["detail"],
            chamfer=0.22,
        )

        glass_boxes = []
        accent_boxes = []
        detail_boxes = []
        levels = 6 if key == "A" else 5
        for i in range(levels):
            z = 1.25 + i * ((h - 2.2) / max(1, levels - 1))
            glass_boxes.append(((x, y - d * 0.51, z), (w * 0.58, 0.055, 0.18), 0))
            glass_boxes.append(((x, y + d * 0.51, z + 0.08), (w * 0.48, 0.055, 0.15), 0))
            glass_boxes.append(((x - w * 0.51, y, z + 0.04), (0.055, d * 0.44, 0.15), 0))
            glass_boxes.append(((x + w * 0.51, y, z - 0.03), (0.055, d * 0.44, 0.15), 0))
        for sx in (-1, 1):
            accent_boxes.append(((x + sx * w * 0.56, y - d * 0.30, h * 0.50), (0.16, 0.10, h * 0.76), 0))
            accent_boxes.append(((x + sx * w * 0.42, y + d * 0.54, h * 0.45), (0.12, 0.08, h * 0.60), 0))
        for i in range(3):
            z = 2.3 + i * (h - 4.2) / 2
            detail_boxes.append(((x, y - d * 0.535, z), (w * 0.84, 0.045, 0.055), 0))
            detail_boxes.append(((x, y + d * 0.535, z + 0.16), (w * 0.70, 0.045, 0.055), 0))
        box_mesh(f"chat_pod_{key}_glass_floor_bands", glass_boxes, mats["glass"])
        box_mesh(f"chat_pod_{key}_burnt_orange_edge_fins", accent_boxes, mats["accent"])
        box_mesh(f"chat_pod_{key}_recessed_floor_ledges", detail_boxes, mats["detail"])


def add_displays(mats):
    screen_specs = [
        ("A_front", "A", "front", 6.2, 1.05, 2.0),
        ("A_right", "A", "right", 8.6, 0.9, 1.5),
        ("B_left", "B", "left", 6.0, 0.78, 1.5),
        ("C_front", "C", "front", 5.1, 0.82, 1.45),
        ("D_right", "D", "right", 5.8, 0.74, 1.3),
    ]
    for name, key, face, z, width, height in screen_specs:
        t = towers[key]
        x, y = t["loc"]
        w, d = t["w"], t["d"]
        if face == "front":
            loc = (x, y - d * 0.58, z)
            dims = (width, 0.06, height)
            frame = [
                ((x, y - d * 0.61, z + height / 2 + 0.06), (width + 0.18, 0.07, 0.08), 0),
                ((x, y - d * 0.61, z - height / 2 - 0.06), (width + 0.18, 0.07, 0.08), 0),
                ((x - width / 2 - 0.07, y - d * 0.61, z), (0.08, 0.07, height + 0.18), 0),
                ((x + width / 2 + 0.07, y - d * 0.61, z), (0.08, 0.07, height + 0.18), 0),
            ]
        elif face == "right":
            loc = (x + w * 0.58, y, z)
            dims = (0.06, width, height)
            frame = [
                ((x + w * 0.61, y, z + height / 2 + 0.06), (0.07, width + 0.18, 0.08), 0),
                ((x + w * 0.61, y, z - height / 2 - 0.06), (0.07, width + 0.18, 0.08), 0),
                ((x + w * 0.61, y - width / 2 - 0.07, z), (0.07, 0.08, height + 0.18), 0),
                ((x + w * 0.61, y + width / 2 + 0.07, z), (0.07, 0.08, height + 0.18), 0),
            ]
        else:
            loc = (x - w * 0.58, y, z)
            dims = (0.06, width, height)
            frame = [
                ((x - w * 0.61, y, z + height / 2 + 0.06), (0.07, width + 0.18, 0.08), 0),
                ((x - w * 0.61, y, z - height / 2 - 0.06), (0.07, width + 0.18, 0.08), 0),
                ((x - w * 0.61, y - width / 2 - 0.07, z), (0.07, 0.08, height + 0.18), 0),
                ((x - w * 0.61, y + width / 2 + 0.07, z), (0.07, 0.08, height + 0.18), 0),
            ]
        add_box(f"chat_display_{name}_emissive_panel", loc, dims, mats["emissive"])
        box_mesh(f"chat_display_{name}_raised_frame", frame, mats["detail"])


bridges = [
    ("AB_upper", "A", "B", 8.8),
    ("AC_lower", "A", "C", 5.15),
    ("BC_mid", "B", "C", 6.65),
    ("AD_high", "A", "D", 9.65),
    ("CD_side", "C", "D", 7.35),
]


def tower_point(key, z):
    x, y = towers[key]["loc"]
    return Vector((x, y, z))


def add_bridge_volume(name, start, end, z, mats, width=0.46, height=0.38):
    start = Vector((start[0], start[1], z))
    end = Vector((end[0], end[1], z))
    direction = end - start
    angle = math.atan2(direction.y, direction.x)
    length = direction.length
    center = (start + end) * 0.5
    add_box(f"chat_skybridge_{name}_glass_enclosure", center, (length, width, height), mats["glass"], angle)
    frame_boxes = [
        (center + Vector((0, 0, height / 2 + 0.07)), (length + 0.18, 0.08, 0.08), angle),
        (center + Vector((0, 0, -height / 2 - 0.07)), (length + 0.18, 0.08, 0.08), angle),
        (center + Vector((0, 0, 0.0)), (length + 0.14, width + 0.12, 0.045), angle),
    ]
    box_mesh(f"chat_skybridge_{name}_structural_frames", frame_boxes, mats["detail"])
    add_box(f"chat_skybridge_{name}_energy_spine", center + Vector((0, 0, height / 2 + 0.13)), (length * 0.92, 0.045, 0.045), mats["energy"], angle)
    cylinder_between(f"chat_skybridge_{name}_collar_start", start - direction.normalized() * 0.18, start + direction.normalized() * 0.18, width * 0.58, mats["detail"], 16)
    cylinder_between(f"chat_skybridge_{name}_collar_end", end - direction.normalized() * 0.18, end + direction.normalized() * 0.18, width * 0.58, mats["detail"], 16)


def add_bridges_and_conduits(mats):
    for name, a, b, z in bridges:
        add_bridge_volume(name, tower_point(a, z), tower_point(b, z), z, mats)
        s = tower_point(a, z - 0.55)
        e = tower_point(b, z - 0.55)
        tube_mesh(f"chat_conduit_{name}_transparent_arc", s, e, 0.12, mats["glass"], sides=16, steps=12, lift=0.45)
        tube_mesh(f"chat_conduit_{name}_inner_energy_filament", s, e, 0.035, mats["energy"], sides=8, steps=12, lift=0.48, offset=(0, 0, 0.10))


def add_crowns_antennas_plaza(mats):
    for key, t in towers.items():
        x, y = t["loc"]
        h, w, d = t["h"], t["w"], t["d"]
        torus(f"chat_pod_{key}_crown_signal_ring", (x, y, h + 0.38), max(w, d) * 0.42, 0.035, mats["accent"], 28, 6)
        for idx, (dx, dy, ht) in enumerate([(-0.38, 0.18, 1.25), (0.34, -0.18, 1.05), (0.0, 0.38, 0.88)]):
            cylinder_between(
                f"chat_antenna_{key}_{idx}_mast",
                (x + dx, y + dy, h + 0.42),
                (x + dx, y + dy, h + 0.42 + ht),
                0.035,
                mats["detail"],
                10,
            )
            cone_between(
                f"chat_antenna_{key}_{idx}_needle",
                (x + dx, y + dy, h + 0.42 + ht),
                (x + dx, y + dy, h + 0.68 + ht),
                0.035,
                0.006,
                mats["detail"],
                10,
            )
        dish(f"chat_antenna_{key}_small_dish", (x + w * 0.25, y - d * 0.60, h + 0.92), 0.28, 0.10, (0, -1, 0.15), mats["detail"], 18, 4)

    dish("chat_main_satellite_bowl", (0.50, -1.42, towers["A"]["h"] + 1.15), 0.58, 0.22, (0, -1, 0.25), mats["detail"], 28, 5)
    cylinder_between("chat_main_satellite_support_arm", (0.30, -0.88, towers["A"]["h"] + 0.62), (0.50, -1.40, towers["A"]["h"] + 1.06), 0.05, mats["detail"], 12)
    cylinder_between("chat_main_satellite_focus_node", (0.50, -1.70, towers["A"]["h"] + 1.26), (0.50, -1.88, towers["A"]["h"] + 1.33), 0.08, mats["emissive"], 12)

    make_prism("chat_shared_plaza_octagonal_deck", (0.65, -0.45, 0), [(0.02, 9.8, 5.8), (0.16, 9.4, 5.4)], mats["base"], chamfer=0.65)
    torus("chat_plaza_outer_signal_ring", (0.65, -0.45, 0.18), 4.35, 0.045, mats["accent"], 48, 6)
    torus("chat_plaza_inner_energy_ring", (0.65, -0.45, 0.21), 2.55, 0.032, mats["energy"], 44, 6)
    grid_boxes = []
    for x in [-3.2, -1.6, 0, 1.6, 3.2]:
        grid_boxes.append(((0.65 + x, -0.45, 0.24), (0.035, 5.1, 0.035), 0))
    for y in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        grid_boxes.append(((0.65, -0.45 + y, 0.25), (8.2, 0.035, 0.035), 0))
    box_mesh("chat_plaza_recessed_grid_lines", grid_boxes, mats["detail"])
    torus("chat_pipeline_hardpoint_outer_collar", (0.0, -1.05, 11.4), 0.42, 0.06, mats["energy"], 32, 8)
    torus("chat_pipeline_hardpoint_inner_collar", (0.0, -1.05, 11.4), 0.22, 0.04, mats["accent"], 28, 6)
    cylinder_between("chat_pipeline_hardpoint_socket", (0.0, -1.18, 11.4), (0.0, -1.65, 11.4), 0.16, mats["energy"], 16)


def add_final_detail(mats):
    for key, t in towers.items():
        x, y = t["loc"]
        h, w, d = t["h"], t["w"], t["d"]
        line_boxes = []
        mullion_boxes = []
        for i in range(1, int(t["floors"] * 0.55)):
            z = 0.82 + i * ((h - 1.5) / int(t["floors"] * 0.55))
            line_boxes.append(((x, y - d * 0.545, z), (w * 0.84, 0.032, 0.026), 0))
            line_boxes.append(((x, y + d * 0.545, z + 0.04), (w * 0.70, 0.032, 0.026), 0))
            if i % 2 == 0:
                line_boxes.append(((x - w * 0.545, y, z + 0.02), (0.032, d * 0.64, 0.026), 0))
                line_boxes.append(((x + w * 0.545, y, z - 0.02), (0.032, d * 0.64, 0.026), 0))
        for sx in [-0.28, 0.0, 0.28]:
            mullion_boxes.append(((x + sx * w, y - d * 0.57, h * 0.55), (0.035, 0.05, h * 0.65), 0))
            mullion_boxes.append(((x + sx * w * 0.75, y + d * 0.57, h * 0.52), (0.032, 0.05, h * 0.55), 0))
        box_mesh(f"chat_pod_{key}_dense_floor_line_detail", line_boxes, mats["detail"])
        box_mesh(f"chat_pod_{key}_glass_mullion_columns", mullion_boxes, mats["glass"])
        torus(f"chat_pod_{key}_base_signal_ring", (x, y, 0.78), max(w, d) * 0.58, 0.028, mats["accent"], 28, 5)

    for name, a, b, z in bridges:
        start = tower_point(a, z)
        end = tower_point(b, z)
        direction = (end - start).normalized()
        side = Vector((-direction.y, direction.x, 0)).normalized()
        length = (end - start).length
        segments = 5
        for i in range(segments):
            p0 = start.lerp(end, (i + 0.18) / segments) + side * 0.26 + Vector((0, 0, -0.33))
            p1 = start.lerp(end, (i + 0.82) / segments) - side * 0.26 + Vector((0, 0, -0.33))
            cylinder_between(f"chat_bridge_{name}_diagonal_truss_{i}_a", p0, p1, 0.025, mats["detail"], 8)
            p2 = start.lerp(end, (i + 0.18) / segments) - side * 0.26 + Vector((0, 0, -0.36))
            p3 = start.lerp(end, (i + 0.82) / segments) + side * 0.26 + Vector((0, 0, -0.36))
            cylinder_between(f"chat_bridge_{name}_diagonal_truss_{i}_b", p2, p3, 0.025, mats["detail"], 8)
        rail_center = (start + end) * 0.5 + Vector((0, 0, 0.31))
        angle = math.atan2((end - start).y, (end - start).x)
        add_box(f"chat_bridge_{name}_top_signal_run", rail_center, (length * 0.88, 0.04, 0.04), mats["energy"], angle)

    wave_boxes = []
    for obj in list(bpy.data.objects):
        if not obj.name.startswith("chat_display_") or "emissive_panel" not in obj.name:
            continue
        x, y, z = obj.location
        dims = obj.dimensions
        vertical_face = dims.x < dims.y
        width = dims.y if vertical_face else dims.x
        height = dims.z
        for row in range(5):
            for seg in range(4):
                offset = -width * 0.35 + seg * width * 0.22
                zoff = -height * 0.28 + row * height * 0.14 + math.sin(seg * 1.7 + row) * 0.035
                if vertical_face:
                    wave_boxes.append(((x + (0.038 if x > 0 else -0.038), y + offset, z + zoff), (0.035, width * 0.12, 0.035), 0))
                else:
                    wave_boxes.append(((x + offset, y - 0.038, z + zoff), (width * 0.12, 0.035, 0.035), 0))
    box_mesh("chat_display_waveform_relief_lines", wave_boxes, mats["emissive"])

    # Crown hardware and signal repeaters.
    for i, angle in enumerate([0, math.pi / 2, math.pi, math.pi * 1.5]):
        x = math.cos(angle) * 0.85
        y = math.sin(angle) * 0.65
        cylinder_between(f"chat_main_crown_repeater_{i}", (x, y, 12.46), (x * 1.15, y * 1.15, 13.02), 0.035, mats["detail"], 10)
        torus(f"chat_main_crown_repeater_ring_{i}", (x * 1.18, y * 1.18, 13.04), 0.13, 0.018, mats["emissive"], 18, 5)

    # More visible pipeline receiver geometry on the main pod.
    cylinder_between("chat_pipeline_receiver_backbone", (-0.34, -1.26, 10.82), (0.34, -1.26, 11.98), 0.045, mats["detail"], 12)
    for i, z in enumerate([10.95, 11.25, 11.55, 11.85]):
        add_box(f"chat_pipeline_receiver_heat_sink_{i}", (0.0, -1.31, z), (0.72 - i * 0.08, 0.055, 0.045), mats["accent"])


def create_chat_scene():
    if os.path.exists(S21_BLEND):
        bpy.ops.wm.open_mainfile(filepath=S21_BLEND)
        old_metrics = {"objects": len(bpy.data.objects), "mesh_objects": mesh_count(), "tris": count_tris()}
    else:
        old_metrics = {"objects": 0, "mesh_objects": 0, "tris": 0}

    mats = setup_scene()
    build_tower_shells(mats)
    add_displays(mats)
    add_bridges_and_conduits(mats)
    add_crowns_antennas_plaza(mats)
    cleanup_names()
    s22a_metrics = {"mesh_objects": mesh_count(), "tris": count_tris(), "material_tris": material_tris()}
    render_shot("s22a_front_elevation.png", (0, -28, 8.4), (0.0, 0.0, 7.2), 30)
    render_shot("s22a_three_quarter.png", (17, -25, 11.5), (0.0, 0.0, 7.2), 32)
    render_shot("s22a_distance_view.png", (24, -38, 18), (0.0, 0.0, 7.0), 35)
    bpy.ops.wm.save_as_mainfile(filepath=S22A_BLEND)

    add_final_detail(mats)
    cleanup_names()
    s22b_pre_export = {"mesh_objects": mesh_count(), "tris": count_tris(), "material_tris": material_tris()}
    render_shot("s22b_front_elevation.png", (0, -28, 8.4), (0.0, 0.0, 7.2), 30)
    render_shot("s22b_three_quarter.png", (17, -25, 11.5), (0.0, 0.0, 7.2), 32)
    render_shot("s22b_distance_view.png", (24, -38, 18), (0.0, 0.0, 7.0), 35)

    emission_values = []
    for mat in bpy.data.materials:
        if mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf and "Emission Strength" in bsdf.inputs:
                emission_values.append((mat.name, bsdf.inputs["Emission Strength"].default_value))
                bsdf.inputs["Emission Strength"].default_value = 0
    render_shot("s22b_dark_first.png", (17, -25, 11.5), (0.0, 0.0, 7.2), 32)
    for name, value in emission_values:
        mat = bpy.data.materials.get(name)
        if mat and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf and "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = value

    # Prepare final production scene: no cameras/lights, transforms baked, root at bottom-center.
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.select_all(action="DESELECT")
    root = bpy.data.objects.new("chat-ext", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.parent = root
    cleanup_names()
    bpy.ops.wm.save_as_mainfile(filepath=S22B_BLEND)

    if not hasattr(bpy.context, "active_object"):
        final_metrics = {
            "mesh_objects": mesh_count(),
            "tris": count_tris(),
            "material_tris": material_tris(),
            "blend": S22B_BLEND,
            "glb": "export handled by export-session-22.py in background Blender",
        }
        return {"old": old_metrics, "s22a": s22a_metrics, "s22b_pre_export": s22b_pre_export, "final": final_metrics}

    bpy.ops.export_scene.gltf(
        filepath=CHAT_GLB,
        export_format="GLB",
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_yup=True,
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
    )
    glb_size = os.path.getsize(CHAT_GLB)
    final_metrics = {
        "mesh_objects": mesh_count(),
        "tris": count_tris(),
        "material_tris": material_tris(),
        "glb_bytes": glb_size,
        "blend": S22B_BLEND,
        "glb": CHAT_GLB,
    }

    create_cohesion_screenshot()
    bpy.ops.wm.open_mainfile(filepath=S22B_BLEND)

    return {"old": old_metrics, "s22a": s22a_metrics, "s22b_pre_export": s22b_pre_export, "final": final_metrics}


def create_cohesion_screenshot():
    clear_scene()
    lighting.setup_viewport_lighting()
    imports = [
        ("sia", os.path.join(ROOT, "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb"), (0, 0, 0)),
        ("fitness", os.path.join(ROOT, "modules/01-fitness/exterior/approved/fitness-ext.glb"), (25, 25, 0)),
        ("yoga", os.path.join(ROOT, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb"), (35, 10, 0)),
        ("finance", os.path.join(ROOT, "modules/03-finance/exterior/approved/finance-ext.glb"), (35, -5, 0)),
        ("knowledgebase", os.path.join(ROOT, "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"), (30, -20, 0)),
        ("chat", CHAT_GLB, (18, -18, 0)),
    ]
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
    render_shot("s22b_cohesion_all6.png", (70, -92, 54), (18, -6, 8), 30)


metrics = create_chat_scene()
print("SESSION22_METRICS=" + json.dumps(metrics, indent=2))

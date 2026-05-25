"""
Balencia City v3 -- Module #09 Recovery & Sleep
Session 39: Interior -- Neural Recovery Chamber

Fresh Recovery interior scene for the approved floating dreamscape exterior.
Builds the central sleep brain hologram, cocoon recovery pods, biometric
symbols, dream particles, emotional reset nooks, breathing wall sections,
runtime empties, screenshots, metrics, and a draft GLB export.
"""

import json
import math
import os
from mathutils import Matrix, Vector

import bpy


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE_DIR = os.path.join(ROOT, "modules/09-recovery-sleep")
SHARED_DIR = os.path.join(ROOT, "shared")
DRAFTS_DIR = os.path.join(MODULE_DIR, "interior", "drafts")
APPROVED_DIR = os.path.join(MODULE_DIR, "interior", "approved")
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")

BLEND_FILE = os.path.join(DRAFTS_DIR, "recovery-int-session39.blend")
DRAFT_GLB = os.path.join(DRAFTS_DIR, "recovery-int-draft-s39.glb")
APPROVED_GLB = os.path.join(APPROVED_DIR, "recovery-int.glb")
METRICS_FILE = os.path.join(DRAFTS_DIR, "session39-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS_DIR, "session39-qa-import.json")

VALID_SLOTS = {"base", "accent", "glass", "detail", "emissive", "energy"}

os.makedirs(DRAFTS_DIR, exist_ok=True)
os.makedirs(APPROVED_DIR, exist_ok=True)
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


def set_principled(mat, base_hex=None, emission_hex=None, emission_strength=None, alpha=None):
    if mat is None or not mat.use_nodes:
        return
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf is None:
        return
    material_library = load_python_module(os.path.join(SHARED_DIR, "material-library.py"), "material_hex_s39")
    if base_hex:
        bsdf.inputs["Base Color"].default_value = material_library["hex_to_linear"](base_hex)
    if emission_hex:
        bsdf.inputs["Emission Color"].default_value = material_library["hex_to_linear"](emission_hex)
    if emission_strength is not None:
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    if alpha is not None:
        mat.blend_method = "BLEND"
        bsdf.inputs["Alpha"].default_value = alpha


def tune_recovery_materials():
    set_principled(MATS["base"], base_hex="#171923", emission_hex="#0C0E18", emission_strength=0.018)
    set_principled(MATS["detail"], base_hex="#10121A", emission_hex="#111827", emission_strength=0.012)
    set_principled(MATS["glass"], base_hex="#15183A", emission_hex="#A5B4FC", emission_strength=0.13, alpha=0.66)
    set_principled(MATS["accent"], base_hex="#1D2148", emission_hex="#6366F1", emission_strength=0.20)
    set_principled(MATS["emissive"], base_hex="#101125", emission_hex="#C7D2FE", emission_strength=0.24)
    set_principled(MATS["energy"], base_hex="#1A1008", emission_hex="#FF5E00", emission_strength=0.08)


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


def make_scaled_uv_sphere(name, loc, scale, slot, segments=14, rings=7, rotation=(0, 0, 0)):
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


def make_torus(name, loc, major_radius, minor_radius, slot, rotation=(0, 0, 0), major_segments=24, minor_segments=4, scale=(1, 1, 1)):
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
    obj.scale = scale
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
    shade(obj)
    return obj


def make_tetrahedron(name, loc, radius, slot, rotation=(0, 0, 0)):
    points = [
        Vector((1, 1, 1)),
        Vector((-1, -1, 1)),
        Vector((-1, 1, -1)),
        Vector((1, -1, -1)),
    ]
    rot = Matrix.Rotation(rotation[2], 4, "Z") @ Matrix.Rotation(rotation[1], 4, "Y") @ Matrix.Rotation(rotation[0], 4, "X")
    verts = [tuple(Vector(loc) + rot @ (point.normalized() * radius)) for point in points]
    faces = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2)]
    return make_mesh(name, verts, faces, slot)


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


def make_curved_wall_panel(name, rx, ry, start_deg, end_deg, zmin, zmax, thickness, slot, segments=24):
    verts = []
    faces = []
    for idx in range(segments + 1):
        angle = math.radians(start_deg + (end_deg - start_deg) * idx / segments)
        inner = Vector((math.cos(angle) * rx, math.sin(angle) * ry, 0))
        outer = Vector((math.cos(angle) * (rx + thickness), math.sin(angle) * (ry + thickness), 0))
        verts.extend(
            [
                (inner.x, inner.y, zmin),
                (inner.x, inner.y, zmax),
                (outer.x, outer.y, zmin),
                (outer.x, outer.y, zmax),
            ]
        )
    for idx in range(segments):
        a = idx * 4
        b = (idx + 1) * 4
        faces.extend(
            [
                (a + 0, b + 0, b + 1, a + 1),
                (a + 2, a + 3, b + 3, b + 2),
                (a + 1, b + 1, b + 3, a + 3),
                (a + 0, a + 2, b + 2, b + 0),
            ]
        )
    faces.append((0, 1, 3, 2))
    last = segments * 4
    faces.append((last + 0, last + 2, last + 3, last + 1))
    return make_mesh(name, verts, faces, slot)


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
    make_ellipse_cylinder("neural_recovery_room_shell_outer_soft_floor_basin", (0, 0, 0.055), 6.55, 5.10, 0.11, "base", vertices=44)
    make_ellipse_cylinder("neural_recovery_room_shell_midnight_floor_pool", (0, 0.05, 0.135), 5.42, 4.08, 0.045, "detail", vertices=36)
    make_ellipse_cylinder("floor_gradient_sleep_brain_center_glow_disc", (0, -0.05, 0.175), 2.28, 1.70, 0.032, "glass", vertices=32)
    make_torus("floor_gradient_deep_to_light_sleep_ring_outer", (0, 0.02, 0.215), 1.0, 0.016, "accent", major_segments=32, minor_segments=3, scale=(4.18, 3.16, 1.0))
    make_torus("floor_gradient_deep_to_light_sleep_ring_mid", (0, -0.02, 0.225), 1.0, 0.014, "emissive", major_segments=28, minor_segments=3, scale=(2.85, 2.12, 1.0))
    make_torus("floor_gradient_deep_to_light_sleep_ring_inner", (0, -0.04, 0.235), 1.0, 0.012, "energy", major_segments=24, minor_segments=3, scale=(1.10, 0.82, 1.0))

    make_curved_wall_panel("neural_recovery_room_shell_continuous_curved_back_wall", 6.18, 4.70, -22, 202, 0.12, 5.18, 0.20, "base", segments=24)
    make_curved_wall_panel("neural_recovery_room_shell_inner_shadow_gap_band", 5.86, 4.38, 7, 173, 0.58, 4.74, 0.08, "detail", segments=20)
    make_curved_wall_panel("neural_recovery_room_shell_soft_glass_upper_window_ribbon", 5.72, 4.25, 18, 162, 2.35, 4.52, 0.055, "glass", segments=16)
    make_curved_wall_panel("neural_recovery_room_shell_open_front_lip_threshold", 4.20, 3.34, 226, 314, 0.16, 0.36, 0.08, "accent", segments=10)

    make_ellipse_cylinder("neural_recovery_room_shell_ceiling_cloud_canopy", (0, 0.20, 5.30), 6.10, 4.58, 0.12, "base", vertices=42)
    make_ellipse_cylinder("neural_recovery_room_shell_ceiling_silver_sleep_aperture", (0, 0.10, 5.39), 2.45, 1.72, 0.036, "glass", vertices=30)
    make_torus("neural_recovery_room_shell_ceiling_aperture_indigo_trim", (0, 0.10, 5.43), 1.0, 0.017, "emissive", major_segments=28, minor_segments=3, scale=(2.45, 1.72, 1.0))

    for idx, angle_deg in enumerate([12, 34, 56, 78, 102, 124, 146, 168]):
        angle = math.radians(angle_deg)
        start = (math.cos(angle) * 2.24, math.sin(angle) * 1.56, 5.38)
        end = (math.cos(angle) * 5.58, math.sin(angle) * 4.18, 5.28)
        make_cylinder_between(f"neural_recovery_room_shell_sleep_canopy_rib_{idx:02d}", start, end, 0.023, "detail", vertices=6)


def build_breathing_walls():
    sections = [
        ("right", 18, 54),
        ("left", 126, 162),
    ]
    for label, start, end in sections:
        make_curved_wall_panel(f"breathing_wall_section_{label}_expanded_outer_membrane", 5.56, 4.10, start, end, 0.92, 4.58, 0.08, "glass", segments=7)
        make_curved_wall_panel(f"breathing_wall_section_{label}_contracted_inner_shadow", 5.28, 3.84, start + 4, end - 4, 1.16, 4.30, 0.05, "base", segments=6)
        for band_idx, z in enumerate([1.42, 2.18, 2.94, 3.70]):
            points = ellipse_arc_points(5.18 - band_idx * 0.05, 3.76 - band_idx * 0.03, start + 7, end - 7, z, 7)
            ribbon_from_points(f"breathing_wall_section_{label}_four_second_pulse_band_{band_idx:02d}", points, 0.060, "emissive" if band_idx % 2 else "accent")


def build_sleep_brain_hologram():
    make_ellipse_cylinder("sleep_brain_hologram_dark_floating_plinth", (0, -0.02, 0.54), 1.70, 1.20, 0.18, "detail", vertices=32)
    make_torus("sleep_brain_hologram_sixty_bpm_floor_pulse", (0, -0.02, 0.68), 1.0, 0.022, "energy", major_segments=30, minor_segments=3, scale=(1.70, 1.20, 1.0))

    make_scaled_uv_sphere("sleep_brain_hologram_left_translucent_lobe", (-0.58, 0.0, 2.34), (0.92, 0.54, 0.72), "glass", segments=20, rings=8, rotation=(0.05, 0.18, -0.08))
    make_scaled_uv_sphere("sleep_brain_hologram_right_translucent_lobe", (0.58, 0.0, 2.34), (0.92, 0.54, 0.72), "glass", segments=20, rings=8, rotation=(0.05, -0.18, 0.08))
    make_scaled_uv_sphere("sleep_brain_hologram_front_rem_lobe", (0.0, -0.46, 2.22), (1.08, 0.42, 0.48), "glass", segments=16, rings=6, rotation=(-0.08, 0.0, 0.0))
    make_scaled_uv_sphere("sleep_brain_hologram_rear_deep_sleep_lobe", (0.0, 0.46, 2.24), (0.96, 0.38, 0.50), "glass", segments=16, rings=6, rotation=(0.08, 0.0, 0.0))
    make_scaled_uv_sphere("sleep_brain_hologram_lower_cerebellum_glow", (0.0, 0.20, 1.78), (0.66, 0.34, 0.30), "emissive", segments=12, rings=5)

    wave_specs = [
        ("rem_phase", 2.58, 0.00, "emissive", 0.26),
        ("deep_phase", 2.34, 1.25, "accent", 0.22),
        ("light_phase", 2.12, 2.35, "energy", 0.18),
        ("transition_phase", 1.94, 3.35, "emissive", 0.16),
    ]
    for label, z, phase, slot, width in wave_specs:
        points = []
        for step in range(11):
            t = step / 10.0
            x = -1.28 + 2.56 * t
            y = -0.58 + math.sin(t * math.tau * 1.5 + phase) * 0.18
            points.append((x, y, z + math.sin(t * math.tau + phase) * 0.06))
        ribbon_from_points(f"sleep_phase_wave_{label}_flowing_color_band", points, width * 0.12, slot)

    make_torus("sleep_brain_hologram_vertical_pulse_orbit_x", (0, -0.02, 2.24), 1.42, 0.014, "emissive", rotation=(math.radians(90), 0, 0), major_segments=24, minor_segments=3)
    make_torus("sleep_brain_hologram_vertical_pulse_orbit_y", (0, -0.02, 2.24), 1.30, 0.012, "accent", rotation=(0, math.radians(90), 0), major_segments=22, minor_segments=3)
    make_torus("sleep_brain_hologram_horizontal_heartbeat_ring", (0, -0.02, 2.24), 1.55, 0.012, "energy", major_segments=24, minor_segments=3)


def build_recovery_pods():
    pod_angles = [28, 62, 96, 130, 164]
    for idx, angle_deg in enumerate(pod_angles):
        angle = math.radians(angle_deg)
        x = math.cos(angle) * 4.46
        y = math.sin(angle) * 3.34
        rot_z = angle - math.pi / 2
        make_ellipse_cylinder(f"recovery_pod_{idx:02d}_soft_floor_cradle", (x, y, 0.38), 0.58, 0.36, 0.18, "detail", vertices=12, rotation=(0, 0, rot_z))
        make_scaled_uv_sphere(f"recovery_pod_{idx:02d}_translucent_cocoon_capsule", (x, y, 1.28), (0.46, 0.30, 0.92), "glass", segments=10, rings=5, rotation=(0, 0, rot_z))
        make_torus(f"recovery_pod_{idx:02d}_slow_cycle_indigo_life_ring", (x, y, 1.34), 0.44, 0.014, "emissive", rotation=(math.radians(90), 0, rot_z), major_segments=14, minor_segments=3, scale=(0.66, 1.0, 1.0))
        make_cylinder_between(
            f"recovery_pod_{idx:02d}_silver_sleep_state_line",
            (x - math.sin(angle) * 0.30, y + math.cos(angle) * 0.30, 1.78),
            (x + math.sin(angle) * 0.30, y - math.cos(angle) * 0.30, 1.78),
            0.013,
            "accent",
            vertices=5,
        )


def build_biometric_symbols():
    for pod_idx, angle_deg in enumerate([28, 62, 96, 130, 164]):
        angle = math.radians(angle_deg)
        base_x = math.cos(angle) * 4.46
        base_y = math.sin(angle) * 3.34
        for item in range(3):
            offset = (item - 1) * 0.24
            loc = (
                base_x + math.cos(angle + math.pi / 2) * offset,
                base_y + math.sin(angle + math.pi / 2) * offset,
                2.42 + item * 0.10,
            )
            if item == 0:
                make_box(f"biometric_symbol_pod_{pod_idx:02d}_heart_rate_bar", loc, (0.22, 0.024, 0.045), "emissive", rotation=(0, 0, angle))
            elif item == 1:
                make_torus(f"biometric_symbol_pod_{pod_idx:02d}_breath_loop", loc, 0.10, 0.010, "accent", rotation=(math.radians(90), 0, angle), major_segments=10, minor_segments=3)
            else:
                make_tetrahedron(f"biometric_symbol_pod_{pod_idx:02d}_sleep_phase_marker", loc, 0.105, "energy", rotation=(0.2, 0.4, angle))


def build_dream_particles():
    particle_positions = [
        (-2.9, -2.7, 1.28), (-2.1, -1.9, 2.26), (-1.4, -3.35, 2.78),
        (-0.55, -2.55, 1.72), (0.32, -3.10, 2.40), (1.22, -2.25, 1.36),
        (2.28, -2.80, 2.92), (3.05, -1.50, 1.92), (-3.35, 0.12, 3.02),
        (-2.48, 1.18, 2.18), (-1.16, 2.34, 3.30), (0.18, 2.68, 1.56),
        (1.34, 2.02, 2.74), (2.54, 1.28, 3.18), (3.42, 0.08, 2.08),
        (-0.18, -0.88, 3.55), (0.92, 0.64, 3.28), (-0.96, 0.52, 1.24),
    ]
    for idx, loc in enumerate(particle_positions):
        slot = ["glass", "emissive", "accent"][idx % 3]
        if idx % 3 == 0:
            make_scaled_uv_sphere(f"dream_particle_{idx:02d}_slow_silver_sphere", loc, (0.075, 0.075, 0.075), slot, segments=6, rings=3)
        elif idx % 3 == 1:
            make_box(f"dream_particle_{idx:02d}_drifting_cube_fragment", loc, (0.085, 0.085, 0.085), slot, rotation=(0.28 * idx, 0.17 * idx, 0.11 * idx))
        else:
            make_tetrahedron(f"dream_particle_{idx:02d}_soft_tetra_fragment", loc, 0.105, slot, rotation=(0.11 * idx, 0.21 * idx, 0.33 * idx))


def build_emotional_reset_nooks():
    nooks = [
        ("left", -4.98, 0.34, math.radians(-70), 138, 168),
        ("right", 4.98, 0.34, math.radians(70), 12, 42),
    ]
    for label, x, y, rot, start, end in nooks:
        make_curved_wall_panel(f"emotional_reset_nook_{label}_carved_wall_alcove_shell", 5.08, 3.56, start, end, 0.64, 3.34, 0.09, "base", segments=6)
        make_scaled_uv_sphere(f"emotional_reset_nook_{label}_single_person_sleep_seat", (x, y - 0.20, 0.68), (0.44, 0.58, 0.26), "detail", segments=10, rings=5, rotation=(0, 0, rot))
        make_scaled_uv_sphere(f"emotional_reset_nook_{label}_soft_reset_aura_field", (x, y - 0.03, 1.36), (0.76, 0.095, 0.62), "glass", segments=10, rings=5, rotation=(0, 0, rot))
        make_torus(f"emotional_reset_nook_{label}_private_breathing_orbit", (x, y - 0.03, 1.38), 0.56, 0.012, "accent", rotation=(math.radians(90), 0, rot), major_segments=14, minor_segments=3)
        for idx, phase in enumerate([0.0, math.pi * 0.5, math.pi, math.pi * 1.5]):
            lx = x + math.cos(phase) * 0.48
            ly = y - 0.03 + math.sin(phase) * 0.08
            lz = 1.38 + math.sin(phase) * 0.28
            make_uv_sphere(f"orbiting_light_point_{label}_{idx:02d}_slow_reset_marker", (lx, ly, lz), 0.072, "emissive", segments=6, rings=3)


def build_runtime_empties():
    create_empty("light_0", (0.0, -0.02, 4.35), 0.50)
    create_empty("light_1", (-3.30, 1.92, 2.34), 0.46)
    create_empty("light_2", (0.0, -0.10, 0.46), 0.46)
    create_empty("camera_target", (0.0, -0.02, 2.28), 0.58)


def group_for_object(name):
    if name.startswith(("neural_recovery_room_shell", "floor_gradient", "breathing_wall_section")):
        return "Room shell, breathing walls, and gradient floor"
    if name.startswith(("sleep_brain_hologram", "sleep_phase_wave")):
        return "Sleep brain hologram focal"
    if name.startswith("recovery_pod"):
        return "Recovery pod perimeter"
    if name.startswith("biometric_symbol"):
        return "Biometric data symbols above pods"
    if name.startswith("dream_particle"):
        return "Dream particles"
    if name.startswith("emotional_reset_nook"):
        return "Emotional reset nooks"
    if name.startswith("orbiting_light_point"):
        return "Orbiting nook light points"
    return "Other"


GROUP_EXPORT_PREFIX = {
    "Room shell, breathing walls, and gradient floor": "neural_recovery_room_shell",
    "Sleep brain hologram focal": "sleep_brain_hologram",
    "Recovery pod perimeter": "recovery_pod",
    "Biometric data symbols above pods": "biometric_symbol",
    "Dream particles": "dream_particle",
    "Emotional reset nooks": "emotional_reset_nook",
    "Orbiting nook light points": "orbiting_light_point",
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
        prefix = GROUP_EXPORT_PREFIX[group]
        joined_name = f"{prefix}_{slot}_joined"
        verts = []
        faces = []
        for obj in objs:
            index_offset = len(verts)
            verts.extend([tuple(obj.matrix_world @ vertex.co) for vertex in obj.data.vertices])
            for polygon in obj.data.polygons:
                faces.append(tuple(index_offset + vertex_index for vertex_index in polygon.vertices))
        joined = make_mesh(joined_name, verts, faces, slot)
        joined.data.name = joined.name + "_mesh"
        for obj in objs:
            bpy.data.objects.remove(obj, do_unlink=True)


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
        "session": 39,
        "module": "09-recovery-sleep",
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
        "qa_import_file": QA_IMPORT_FILE,
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

    root = bpy.data.objects.new("recovery-int", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.1
    for obj in list(bpy.data.objects):
        if obj == root:
            continue
        if obj.type in {"MESH", "EMPTY"} and obj.parent is None and not obj.name.startswith("S39_"):
            obj.parent = root

    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        selected = obj.type in {"MESH", "EMPTY"} and not obj.name.startswith("S39_")
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


def validate_exported_glb():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=DRAFT_GLB)

    material_names = sorted({material_base_name(mat) for mat in bpy.data.materials})
    invalid_materials = sorted(name for name in material_names if name not in VALID_SLOTS)
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

    transform_issues = []
    for obj in mesh_objects:
        scale = obj.matrix_world.to_scale()
        rot = obj.rotation_euler
        if any(abs(value - 1.0) > 0.001 for value in scale) or any(abs(value) > 0.001 for value in rot):
            transform_issues.append(obj.name)

    qa = {
        "session": 39,
        "imported_tris": total_tris,
        "mesh_objects": len(mesh_objects),
        "empty_names": empty_names,
        "material_names": material_names,
        "invalid_materials": invalid_materials,
        "has_energy": "energy" in material_names,
        "has_holo": "holo" in material_names,
        "camera_count": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
        "light_count": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
        "non_identity_mesh_transforms": transform_issues,
        "bbox_min": [round(min_corner.x, 4), round(min_corner.y, 4), round(min_corner.z, 4)],
        "bbox_max": [round(max_corner.x, 4), round(max_corner.y, 4), round(max_corner.z, 4)],
        "glb_size_bytes": os.path.getsize(DRAFT_GLB),
    }
    with open(QA_IMPORT_FILE, "w") as handle:
        json.dump(qa, handle, indent=2, sort_keys=True)
    return qa


def build_session_39():
    print("=== Session 39: Recovery & Sleep Interior ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    lighting = load_python_module(os.path.join(SHARED_DIR, "lighting-rig.py"), "lighting_rig_s39")
    lighting["clear_lighting"]()
    lighting["setup_viewport_lighting"]()

    material_library = load_python_module(os.path.join(SHARED_DIR, "material-library.py"), "material_library_s39")
    global MATS
    MATS = material_library["create_materials"]("#6366F1", include_energy=True, include_holo=False)
    tune_recovery_materials()

    interior_lighting = load_python_module(os.path.join(SHARED_DIR, "interior-lighting-rig.py"), "interior_lighting_s39")
    interior_lighting["setup_interior_lighting"](focal_point=(0, -0.02, 2.28), floor_z=0.0, ceiling_z=5.45, radius=5.4)
    interior_lighting["boost_emissions_for_preview"]()
    tune_recovery_materials()

    build_room_shell()
    build_breathing_walls()
    build_sleep_brain_hologram()
    build_recovery_pods()
    build_biometric_symbols()
    build_dream_particles()
    build_emotional_reset_nooks()
    build_runtime_empties()

    overview_cam = make_camera("S39_Interior_Overview_Camera", (7.2, -8.0, 4.75), (0, -0.02, 2.22), lens=32)
    entry_cam = make_camera("S39_Interior_Entry_Camera", (0.0, -8.05, 2.20), (0, -0.02, 2.28), lens=36)
    focal_cam = make_camera("S39_Interior_Focal_Brain_Camera", (2.80, -4.72, 2.88), (0, -0.02, 2.28), lens=43)
    top_cam = make_camera("S39_Interior_Topdown_Camera", (0.0, -0.20, 10.25), (0, 0, 0.30), lens=43)

    screenshots = [
        render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s39-int-overview.png")),
        render_still(entry_cam, os.path.join(SCREENSHOTS_DIR, "s39-int-from-entry.png")),
        render_still(focal_cam, os.path.join(SCREENSHOTS_DIR, "s39-int-focal-sleep-brain.png")),
        render_still_with_hidden(
            top_cam,
            os.path.join(SCREENSHOTS_DIR, "s39-int-topdown.png"),
            [
                "neural_recovery_room_shell_ceiling_cloud_canopy",
                "neural_recovery_room_shell_ceiling_silver_sleep_aperture",
                "neural_recovery_room_shell_ceiling_aperture_indigo_trim",
            ],
        ),
    ]

    previous_emissions = set_all_emission_strength(0.0)
    screenshots.append(render_still(overview_cam, os.path.join(SCREENSHOTS_DIR, "s39-int-dark-first.png")))
    restore_emission_strength(previous_emissions)

    consolidate_meshes_by_group_and_slot()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    metrics = collect_metrics([os.path.relpath(path, MODULE_DIR) for path in screenshots])
    metrics = export_draft_glb(metrics)
    with open(METRICS_FILE, "w") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)

    qa = validate_exported_glb()
    metrics["import_qa"] = qa
    with open(METRICS_FILE, "w") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)

    bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

    print("=" * 70)
    print("SESSION 39 BUILD COMPLETE")
    print(f"Blend: {BLEND_FILE}")
    print(f"Draft GLB: {DRAFT_GLB}")
    print(f"GLB size: {metrics['glb_size_bytes'] / 1024:.1f} KB")
    print(f"Tris: {metrics['total_tris']}")
    print(f"Meshes: {metrics['mesh_objects']}")
    print(f"Empties: {metrics['empty_names']}")
    print(f"Metrics: {METRICS_FILE}")
    print(f"Import QA: {QA_IMPORT_FILE}")
    print("SESSION39_METRICS=" + json.dumps(metrics, indent=2, sort_keys=True))
    return metrics


metrics = build_session_39()

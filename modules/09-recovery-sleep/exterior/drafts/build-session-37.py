"""
Balencia City v3 - Module #09 Recovery & Sleep
Session 37: Exterior Major Forms

Floating dreamscape: a smooth cloud-like organic building hovering over a
mirror-still lake on soft indigo light pillars, with nested translucent shells,
edge wisps, star points, and a barely visible SIA energy thread receiver.
"""

import importlib.util
import json
import math
import os
import sys

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/09-recovery-sleep")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
BLEND_FILE = os.path.join(DRAFTS, "recovery-s37-major-forms.blend")
METRICS_FILE = os.path.join(DRAFTS, "session37-metrics.json")

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
    if hasattr(obj.data, "materials"):
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


def set_principled(mat, base_hex=None, emission_hex=None, emission_strength=None, alpha=None):
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


def tune_recovery_materials(mats):
    set_principled(mats["glass"], base_hex="#171A3F", emission_hex="#A5B4FC", emission_strength=0.045, alpha=0.76)
    set_principled(mats["emissive"], base_hex="#111225", emission_hex="#6366F1", emission_strength=0.22)
    set_principled(mats["accent"], base_hex="#1B1D3B", emission_hex="#6366F1", emission_strength=0.16)
    set_principled(mats["energy"], base_hex="#1A1008", emission_hex="#FF5E00", emission_strength=0.055)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def shade_smooth(obj):
    if obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def make_mesh(name, verts, faces, mat, smooth=True):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    if smooth:
        shade_smooth(obj)
    return obj


def uv_ellipsoid(name, loc, scale, mat, segments=24, rings=10, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        radius=1.0,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    obj.scale = scale
    assign(obj, mat)
    shade_smooth(obj)
    apply_transforms(obj)
    return obj


def cylinder(name, loc, radius, depth, mat, vertices=18, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    shade_smooth(obj)
    apply_transforms(obj)
    return obj


def cone(name, loc, radius1, radius2, depth, mat, vertices=12, rot=(0.0, 0.0, 0.0)):
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
    assign(obj, mat)
    shade_smooth(obj)
    apply_transforms(obj)
    return obj


def torus(name, loc, major, minor, mat, seg=32, minor_seg=4):
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
    shade_smooth(obj)
    apply_transforms(obj)
    return obj


def cylinder_between(name, start, end, radius, mat, vertices=8):
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
    shade_smooth(obj)
    apply_transforms(obj)
    return obj


def ellipse_disc(name, rx, ry, z, mat, segments=96, center=(0.0, 0.0), phase=0.0):
    cx, cy = center
    verts = [(cx, cy, z)]
    for i in range(segments):
        a = phase + math.tau * i / segments
        ripple = 1.0 + 0.01 * math.sin(4 * a)
        verts.append((cx + math.cos(a) * rx * ripple, cy + math.sin(a) * ry * ripple, z))
    faces = []
    for i in range(segments):
        faces.append((0, 1 + i, 1 + ((i + 1) % segments)))
    return make_mesh(name, verts, faces, mat, smooth=False)


def ellipse_band(name, outer_rx, outer_ry, inner_rx, inner_ry, z0, z1, mat, segments=72, center=(0.0, 0.0), phase=0.0):
    cx, cy = center
    verts = []
    for i in range(segments):
        a = phase + math.tau * i / segments
        organic = 1.0 + 0.015 * math.sin(3 * a + phase)
        co = math.cos(a)
        si = math.sin(a)
        verts.extend(
            [
                (cx + outer_rx * co * organic, cy + outer_ry * si * organic, z0),
                (cx + outer_rx * co * organic, cy + outer_ry * si * organic, z1),
                (cx + inner_rx * co * organic, cy + inner_ry * si * organic, z1),
                (cx + inner_rx * co * organic, cy + inner_ry * si * organic, z0),
            ]
        )
    faces = []
    for i in range(segments):
        j = (i + 1) % segments
        a = i * 4
        b = j * 4
        faces.append((a + 0, b + 0, b + 1, a + 1))
        faces.append((a + 1, b + 1, b + 2, a + 2))
        faces.append((a + 2, b + 2, b + 3, a + 3))
        faces.append((a + 3, b + 3, b + 0, a + 0))
    return make_mesh(name, verts, faces, mat)


def tapered_wisp(prefix, points, start_radius, mat):
    for idx in range(len(points) - 1):
        t = idx / max(1, len(points) - 2)
        radius = start_radius * (1.0 - 0.62 * t)
        cylinder_between(f"{prefix}_soft_tapering_wisp_segment_{idx:02d}", points[idx], points[idx + 1], radius, mat, vertices=7)


def setup_render():
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        try:
            scene.render.engine = "BLENDER_EEVEE"
        except Exception:
            scene.render.engine = "CYCLES"
            scene.cycles.samples = 64
    if hasattr(scene, "eevee"):
        eevee = scene.eevee
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
            eevee.bloom_threshold = 0.35
            eevee.bloom_intensity = 0.7
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.5


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


def category_for_object(name):
    if "lake" in name or "shore" in name or "reflection" in name:
        return "Mirror-still lake and reflection setting"
    if "pillar" in name or "beam" in name:
        return "Indigo light pillar support system"
    if "outer_shell" in name or "cloud_lobe" in name:
        return "Outer translucent cloud shell"
    if "inner_shell" in name or "aurora" in name:
        return "Nested inner shell and aurora glow"
    if "star" in name:
        return "Faint star-like surface lights"
    if "wisp" in name and "receiver" not in name:
        return "Trailing edge wisps"
    if "energy" in name or "receiver" in name or "sia_thread" in name:
        return "Barely visible SIA thread receiver"
    if "underside" in name or "gap" in name:
        return "Smooth concave underside and shell gap"
    return "Recovery dreamscape primary forms"


def object_metrics():
    rows = []
    for obj in sorted((o for o in bpy.data.objects if o.type == "MESH"), key=lambda o: o.name):
        rows.append(
            {
                "name": obj.name,
                "tris": get_tri_count(obj),
                "material": obj.data.materials[0].name.split(".")[0] if obj.data.materials else "NONE",
                "category": category_for_object(obj.name),
            }
        )
    return rows


def category_metrics(objects):
    totals = {}
    counts = {}
    for row in objects:
        category = row["category"]
        totals[category] = totals.get(category, 0) + row["tris"]
        counts[category] = counts.get(category, 0) + 1
    return [
        {"category": category, "objects": counts[category], "tris": totals[category]}
        for category in sorted(totals)
    ]


def world_bbox():
    coords = []
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            coords.append(obj.matrix_world @ Vector(corner))
    if not coords:
        return {}
    return {
        "min": [round(min(v[i] for v in coords), 4) for i in range(3)],
        "max": [round(max(v[i] for v in coords), 4) for i in range(3)],
    }


def build_scene():
    print("=== Session 37: Recovery & Sleep exterior major forms ===")
    clear_scene()
    lighting.setup_viewport_lighting()
    setup_render()
    mats = materials_mod.create_materials("#6366F1", include_energy=True, include_holo=False)
    cleanup_slot_names()
    tune_recovery_materials(mats)
    print(f"Material slots: {sorted(mats.keys())}")

    # Mirror lake and subtle dark shoreline. Recovery's setting must read as still,
    # quiet, and distinct from Yoga's occupied sanctuary platform.
    ellipse_disc("mirror_still_lake_flat_reflective_plane", 9.8, 5.8, 0.02, mats["glass"], segments=112)
    ellipse_band("dark_silent_shoreline_frame_around_lake", 10.25, 6.15, 9.8, 5.8, 0.01, 0.07, mats["base"], segments=72)
    ellipse_disc("soft_cloud_reflection_shadow_on_lake", 5.4, 3.0, 0.035, mats["detail"], segments=64, phase=0.12)

    # Five soft indigo support beams from lake to the hovering cloud.
    pillar_positions = [
        (-3.05, -1.55, 3.28),
        (-0.95, -2.30, 3.45),
        (2.48, -1.25, 3.32),
        (-2.15, 1.55, 3.18),
        (2.05, 1.48, 3.26),
    ]
    for idx, (x, y, top_z) in enumerate(pillar_positions):
        height = top_z - 0.10
        cylinder(f"indigo_light_pillar_beam_{idx:02d}", (x, y, 0.10 + height * 0.5), 0.105, height, mats["emissive"], vertices=18)
        torus(f"indigo_light_pillar_lake_ripple_ring_{idx:02d}", (x, y, 0.105), 0.38, 0.018, mats["emissive"], seg=24, minor_seg=3)
        torus(f"indigo_light_pillar_cloud_contact_halo_{idx:02d}", (x, y, top_z), 0.28, 0.016, mats["emissive"], seg=20, minor_seg=3)

    # Smooth concave underside and dark shell gap. This gives the cloud a bottom
    # surface without turning it into a platform or a tower.
    uv_ellipsoid(
        "smooth_concave_underside_dark_cloud_belly",
        (0.0, -0.05, 3.56),
        (4.85, 2.72, 0.58),
        mats["base"],
        segments=32,
        rings=8,
    )
    uv_ellipsoid(
        "dark_nested_shell_gap_between_outer_and_inner_cloud",
        (0.0, 0.02, 4.20),
        (4.25, 2.32, 0.36),
        mats["detail"],
        segments=28,
        rings=8,
    )

    # Outer shell: overlapping smooth lobes, intentionally unmerged so the
    # silhouette reads as organic cloud massing rather than a dome.
    outer_specs = [
        ("central_outer_shell_cloud_lobe_organic_mass", (0.0, -0.05, 5.05), (3.68, 2.18, 1.22), 0.02),
        ("west_outer_shell_cloud_lobe_organic_mass", (-2.35, 0.18, 5.18), (2.25, 1.62, 1.04), -0.16),
        ("east_outer_shell_cloud_lobe_organic_mass", (2.18, -0.18, 5.03), (2.18, 1.55, 0.98), 0.22),
        ("rear_upper_outer_shell_cloud_lobe_organic_mass", (0.32, 1.10, 5.58), (2.38, 1.18, 0.82), 0.08),
    ]
    for name, loc, scale, rz in outer_specs:
        uv_ellipsoid(name, loc, scale, mats["glass"], segments=30, rings=12, rot=(0.0, 0.0, rz))

    # Nested shell and aurora glow: smaller visible interior volumes set inside
    # the glass shell. No holo slot is used for Recovery.
    inner_specs = [
        ("inner_shell_dream_cocoon_visible_through_cloud", (-0.58, -0.08, 5.18), (2.35, 1.22, 0.66), 0.08),
        ("inner_shell_secondary_sleep_lobe_visible_gap", (1.42, 0.34, 5.20), (1.55, 0.88, 0.54), -0.12),
        ("aurora_interior_glow_soft_indigo_core", (0.20, -0.02, 5.32), (2.70, 0.55, 0.34), 0.04),
        ("aurora_interior_glow_silver_phase_band", (-0.30, 0.72, 5.58), (1.92, 0.42, 0.28), -0.20),
    ]
    for idx, (name, loc, scale, rz) in enumerate(inner_specs):
        mat = mats["glass"] if idx < 2 else mats["emissive"]
        uv_ellipsoid(name, loc, scale, mat, segments=22, rings=8, rot=(0.0, 0.0, rz))

    # Surface star lights are sparse, not a facade grid. They serve the SPEC's
    # embedded jewel read while preserving no-floor-separation continuity.
    star_points = [
        (-3.42, -0.72, 5.02, 0.070),
        (-2.62, 0.92, 5.72, 0.064),
        (-1.62, -1.70, 5.66, 0.058),
        (-0.36, 1.82, 6.12, 0.055),
        (0.22, -2.10, 5.26, 0.062),
        (1.18, 1.64, 6.20, 0.060),
        (2.08, -1.46, 5.48, 0.066),
        (2.84, 0.72, 5.18, 0.058),
        (-2.08, 0.02, 6.28, 0.052),
        (0.88, -0.78, 6.48, 0.048),
        (3.45, -0.18, 4.82, 0.058),
        (-3.78, 0.30, 4.72, 0.054),
    ]
    for idx, (x, y, z, size) in enumerate(star_points):
        uv_ellipsoid(
            f"faint_star_like_surface_light_{idx:02d}",
            (x, y, z),
            (size, size, size),
            mats["emissive"],
            segments=8,
            rings=4,
        )

    # Edge wisps: long, tapering, and soft. These define Recovery's silhouette
    # without adding hard walkways or cables.
    wisp_specs = [
        ("west_upper_trailing", [(-3.95, 0.55, 5.36), (-4.90, 1.03, 5.44), (-5.88, 1.56, 5.18), (-6.52, 1.92, 4.86)]),
        ("east_low_trailing", [(3.72, -0.52, 4.92), (4.74, -0.85, 4.78), (5.62, -1.36, 4.45), (6.10, -1.82, 4.06)]),
        ("south_soft_trailing", [(-0.34, -2.44, 5.10), (-0.28, -3.28, 5.02), (-0.02, -4.10, 4.72), (0.18, -4.68, 4.30)]),
        ("north_silver_trailing", [(1.05, 2.05, 5.76), (1.40, 2.78, 5.88), (1.94, 3.32, 5.64), (2.36, 3.80, 5.30)]),
        ("west_lower_trailing", [(-3.22, -1.26, 4.72), (-4.02, -1.70, 4.54), (-4.82, -2.16, 4.18), (-5.24, -2.58, 3.88)]),
    ]
    for idx, (label, points) in enumerate(wisp_specs):
        tapered_wisp(f"{label}_edge", points, 0.052 if idx < 2 else 0.045, mats["accent"])

    # Barely visible SIA thread reception point. Final energy routing belongs to
    # Phase 5; this is only the district-side receptor.
    torus("barely_visible_sia_thread_receiver_top_ring_energy", (0.05, 0.18, 6.98), 0.34, 0.020, mats["energy"], seg=24, minor_seg=3)
    cone("minimal_orange_energy_thread_receiver_wisp_core", (0.05, 0.18, 7.28), 0.16, 0.028, 0.64, mats["energy"], vertices=10)
    cylinder_between(
        "minimal_sia_thread_receiver_wisp_curve_00",
        (-0.10, 0.08, 7.16),
        (0.34, 0.46, 7.68),
        0.018,
        mats["energy"],
        vertices=7,
    )
    cylinder_between(
        "minimal_sia_thread_receiver_wisp_curve_01",
        (0.34, 0.46, 7.68),
        (0.58, 0.66, 7.92),
        0.012,
        mats["energy"],
        vertices=7,
    )

    cleanup_slot_names()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    screenshots = [
        render_shot("s37_front_elevation.png", (0, -22, 6.0), (0, -0.1, 4.2), 38),
        render_shot("s37_three_quarter.png", (16, -20, 8.8), (0.0, 0.0, 4.4), 40),
        render_shot("s37_distance_view.png", (31, -36, 15.5), (0.0, 0.0, 4.3), 44),
    ]

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    objects = object_metrics()
    metrics = {
        "session": 37,
        "module": "09-recovery-sleep",
        "blender_version": bpy.app.version_string,
        "blend": BLEND_FILE,
        "screenshots": screenshots,
        "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "triangles": scene_triangles(),
        "materials": sorted([m.name for m in bpy.data.materials]),
        "material_tris": material_triangles(),
        "category_metrics": category_metrics(objects),
        "objects": objects,
        "lights": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
        "cameras": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
        "bbox": world_bbox(),
    }

    with open(METRICS_FILE, "w") as handle:
        json.dump(metrics, handle, indent=2)

    print("SESSION37_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_scene()

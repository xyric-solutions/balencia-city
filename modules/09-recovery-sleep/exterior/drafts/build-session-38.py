"""
Balencia City v3 - Module #09 Recovery & Sleep
Session 38: Exterior Detail, Polish, Export

Loads the Session 37 Recovery major forms, adds the deferred detail pass,
exports the exterior GLB, validates import metrics, and captures all-ten
exterior cohesion proof.
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
MODULE = os.path.join(ROOT, "modules/09-recovery-sleep")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
APPROVED = os.path.join(MODULE, "exterior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")

S37_BLEND = os.path.join(DRAFTS, "recovery-s37-major-forms.blend")
S38_BLEND = os.path.join(DRAFTS, "recovery-s38-detail-export.blend")
PACKED_BLEND = os.path.join(DRAFTS, "recovery-s38-export-packed.blend")
DRAFT_GLB = os.path.join(DRAFTS, "recovery-ext-draft-s38.glb")
APPROVED_GLB = os.path.join(APPROVED, "recovery-ext.glb")
METRICS_FILE = os.path.join(DRAFTS, "session38-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS, "session38-qa-import.json")

DISTRICT_HEX = "#6366F1"
ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy"}

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s38", os.path.join(ROOT, "shared/lighting-rig.py"))
materials_mod = load_module("balencia_materials_s38", os.path.join(ROOT, "shared/material-library.py"))

created_categories = {}


def register(obj, category):
    if obj is not None:
        created_categories[obj.name] = category
    return obj


def material_base_name(material):
    return material.name.split(".")[0] if material else ""


def set_principled(mat, base_hex=None, emission_hex=None, emission_strength=None, alpha=None):
    if mat is None or not mat.use_nodes:
        return
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


def ensure_materials():
    existing = {material_base_name(mat): mat for mat in bpy.data.materials if material_base_name(mat) in ALLOWED_MATERIALS}
    if any(name not in existing for name in ALLOWED_MATERIALS):
        materials_mod.create_materials(DISTRICT_HEX, include_energy=True, include_holo=False)
    mats = {}
    for mat in bpy.data.materials:
        base = material_base_name(mat)
        if base in ALLOWED_MATERIALS and base not in mats:
            mats[base] = mat
    for name in ALLOWED_MATERIALS:
        if name not in mats:
            raise RuntimeError(f"Missing material slot after setup: {name}")
        mats[name].name = name
    return mats


def tune_recovery_materials(mats):
    set_principled(mats["base"], base_hex="#1B1C26")
    set_principled(mats["detail"], base_hex="#12131C")
    set_principled(mats["glass"], base_hex="#15183A", emission_hex="#A5B4FC", emission_strength=0.035, alpha=0.74)
    set_principled(mats["emissive"], base_hex="#101125", emission_hex="#6366F1", emission_strength=0.20)
    set_principled(mats["accent"], base_hex="#1B1D3B", emission_hex="#6366F1", emission_strength=0.13)
    set_principled(mats["energy"], base_hex="#1A1008", emission_hex="#FF5E00", emission_strength=0.050)


def normalize_material_slots():
    mats = ensure_materials()
    fallback = mats["detail"]
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        if not obj.data.materials:
            obj.data.materials.append(fallback)
        for index, material in enumerate(obj.data.materials):
            base = material_base_name(material)
            obj.data.materials[index] = mats[base] if base in mats else fallback
    for mat in list(bpy.data.materials):
        base = material_base_name(mat)
        if base not in ALLOWED_MATERIALS and mat.users == 0:
            bpy.data.materials.remove(mat)
    return mats


def current_object():
    obj = getattr(bpy.context.view_layer.objects, "active", None)
    if obj is not None:
        return obj
    selected = getattr(bpy.context, "selected_objects", [])
    if selected:
        return selected[-1]
    raise RuntimeError("No active object after primitive creation")


def assign(obj, mat):
    if obj is None or obj.type != "MESH":
        return obj
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def shade_smooth(obj):
    if obj is not None and obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def apply_transforms(obj):
    if obj is None:
        return obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    return obj


def make_mesh(name, verts, faces, mat, category, shade=True):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    if shade:
        shade_smooth(obj)
    return register(obj, category)


def uv_ellipsoid(name, loc, scale, mat, category, segments=20, rings=8, rot=(0.0, 0.0, 0.0)):
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
    return register(obj, category)


def cylinder(name, loc, radius, depth, mat, category, vertices=12, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    shade_smooth(obj)
    apply_transforms(obj)
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, mat, category, vertices=10, rot=(0, 0, 0)):
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
    return register(obj, category)


def torus(name, loc, major, minor, mat, category, seg=28, minor_seg=4, scale=(1.0, 1.0, 1.0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=seg,
        minor_segments=minor_seg,
        major_radius=major,
        minor_radius=minor,
        location=loc,
        rotation=rot,
    )
    obj = current_object()
    obj.name = name
    obj.scale = scale
    assign(obj, mat)
    shade_smooth(obj)
    apply_transforms(obj)
    return register(obj, category)


def cylinder_between(name, start, end, radius, mat, category, vertices=7):
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
    return register(obj, category)


def ellipse_disc(name, rx, ry, z, mat, category, segments=96, center=(0.0, 0.0), phase=0.0):
    cx, cy = center
    verts = [(cx, cy, z)]
    for i in range(segments):
        a = phase + math.tau * i / segments
        organic = 1.0 + 0.008 * math.sin(5 * a + phase)
        verts.append((cx + math.cos(a) * rx * organic, cy + math.sin(a) * ry * organic, z))
    faces = [(0, 1 + i, 1 + ((i + 1) % segments)) for i in range(segments)]
    return make_mesh(name, verts, faces, mat, category, shade=False)


def ellipse_band(
    name,
    outer_rx,
    outer_ry,
    inner_rx,
    inner_ry,
    z0,
    z1,
    mat,
    category,
    segments=72,
    center=(0.0, 0.0),
    phase=0.0,
):
    cx, cy = center
    verts = []
    for i in range(segments):
        a = phase + math.tau * i / segments
        organic = 1.0 + 0.012 * math.sin(3 * a + phase)
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
    return make_mesh(name, verts, faces, mat, category)


def segmented_arc(name, center, rx, ry, z, start_deg, end_deg, radius, mat, category, segments=18, vertices=6, height_wave=0.0):
    cx, cy = center
    points = []
    for i in range(segments + 1):
        t = i / segments
        a = math.radians(start_deg + (end_deg - start_deg) * t)
        points.append((cx + math.cos(a) * rx, cy + math.sin(a) * ry, z + math.sin(t * math.pi) * height_wave))
    made = []
    for idx in range(len(points) - 1):
        made.append(cylinder_between(f"{name}_segment_{idx:02d}", points[idx], points[idx + 1], radius, mat, category, vertices))
    return made


def setup_lighting_and_render():
    lighting.setup_viewport_lighting()
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
            eevee.bloom_intensity = 0.65
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.6


def render_shot(filename, camera_loc, target, lens=42):
    cam_data = bpy.data.cameras.new(filename.replace(".png", "_Camera"))
    cam = bpy.data.objects.new(filename.replace(".png", "_Camera"), cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    direction = Vector(target) - Vector(camera_loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.clip_start = 0.1
    cam.data.clip_end = 250
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = os.path.join(SCREENSHOTS, filename)
    bpy.ops.render.render(write_still=True)
    return bpy.context.scene.render.filepath


def render_dark_first():
    saved = []
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is None or "Emission Strength" not in bsdf.inputs:
            continue
        saved.append((bsdf, bsdf.inputs["Emission Strength"].default_value))
        bsdf.inputs["Emission Strength"].default_value = 0.0
    path = render_shot("s38_dark_first.png", (15, -22, 8.4), (0.0, 0.0, 4.0), 42)
    for bsdf, strength in saved:
        bsdf.inputs["Emission Strength"].default_value = strength
    return path


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


def material_percentages(total_tris, mat_tris):
    if not total_tris:
        return {}
    return {name: round((tris / total_tris) * 100.0, 2) for name, tris in mat_tris.items()}


def material_surface_area():
    totals = {}
    total = 0.0
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for poly in obj.data.polygons:
            mat_name = obj.data.materials[poly.material_index].name if obj.data.materials else "NONE"
            mat_name = mat_name.split(".")[0]
            area = poly.area
            totals[mat_name] = totals.get(mat_name, 0.0) + area
            total += area
    return {
        "total": round(total, 3),
        "areas": {name: round(area, 3) for name, area in sorted(totals.items())},
        "percentages": {
            name: round((area / total) * 100.0, 2) for name, area in sorted(totals.items())
        } if total else {},
    }


def bbox_vectors():
    coords = []
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for vertex in obj.data.vertices:
            coords.append(obj.matrix_world @ vertex.co)
    if not coords:
        zero = Vector((0, 0, 0))
        return zero, zero
    min_v = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
    max_v = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
    return min_v, max_v


def bbox():
    min_v, max_v = bbox_vectors()
    return {
        "min": [round(min_v.x, 4), round(min_v.y, 4), round(min_v.z, 4)],
        "max": [round(max_v.x, 4), round(max_v.y, 4), round(max_v.z, 4)],
    }


def category_for_name(name):
    if name in created_categories:
        return created_categories[name]
    if "lake" in name or "shore" in name or "reflection" in name:
        return "Mirror-still lake and reflection polish"
    if "pillar" in name or "beam" in name:
        return "Indigo light pillar support polish"
    if "outer_shell" in name or "cloud_lobe" in name or "shell_contour" in name:
        return "Outer cloud shell and contour articulation"
    if "inner_shell" in name or "aurora" in name or "shadow" in name or "gap" in name:
        return "Nested shell gaps and dark sleep shadows"
    if "star" in name:
        return "Faint star-like surface lights"
    if "wisp" in name and "receiver" not in name:
        return "Trailing edge wisps"
    if "energy" in name or "receiver" in name or "sia_thread" in name:
        return "Barely visible SIA thread receiver"
    return "Recovery dreamscape exterior detail"


def object_metrics():
    rows = []
    for obj in sorted((o for o in bpy.data.objects if o.type == "MESH"), key=lambda o: o.name):
        rows.append(
            {
                "name": obj.name,
                "tris": get_tri_count(obj),
                "material": material_base_name(obj.data.materials[0]) if obj.data.materials else "NONE",
                "category": category_for_name(obj.name),
            }
        )
    return rows


def category_metrics():
    totals = {}
    counts = {}
    for row in object_metrics():
        category = row["category"]
        totals[category] = totals.get(category, 0) + row["tris"]
        counts[category] = counts.get(category, 0) + 1
    return [
        {"category": category, "objects": counts[category], "tris": totals[category]}
        for category in sorted(totals)
    ]


def add_lake_reflection_polish(mats):
    ellipse_disc(
        "dark_sleep_lake_bed_visible_through_glass",
        10.85,
        6.55,
        -0.035,
        mats["base"],
        "Mirror-still lake and reflection polish",
        segments=120,
        phase=0.08,
    )
    ellipse_disc(
        "deep_center_lake_shadow_gradient_under_cloud",
        6.9,
        3.85,
        -0.018,
        mats["base"],
        "Mirror-still lake and reflection polish",
        segments=96,
        phase=0.21,
    )
    ellipse_band(
        "soft_reflection_outer_crescent_detail_ring",
        8.65,
        5.02,
        7.96,
        4.62,
        0.045,
        0.072,
        mats["detail"],
        "Mirror-still lake and reflection polish",
        segments=84,
        phase=0.11,
    )
    ellipse_band(
        "still_water_indigo_reflection_inner_ring",
        5.95,
        3.18,
        5.56,
        2.95,
        0.055,
        0.078,
        mats["glass"],
        "Mirror-still lake and reflection polish",
        segments=72,
        phase=0.28,
    )
    ellipse_band(
        "thin_dark_waterline_scale_shadow",
        10.28,
        6.16,
        10.06,
        6.00,
        0.078,
        0.116,
        mats["base"],
        "Mirror-still lake and reflection polish",
        segments=88,
        phase=0.0,
    )
    for idx, (x, y, sx, sy) in enumerate(
        [
            (-3.25, -0.66, 0.16, 0.035),
            (-1.30, 1.06, 0.12, 0.030),
            (0.78, -1.76, 0.13, 0.032),
            (2.15, 0.82, 0.15, 0.036),
            (3.36, -0.26, 0.11, 0.028),
            (-4.05, 0.20, 0.10, 0.026),
        ]
    ):
        uv_ellipsoid(
            f"faint_reflected_star_glint_on_mirror_lake_{idx:02d}",
            (x, y, 0.105),
            (sx, sy, 0.010),
            mats["emissive"],
            "Mirror-still lake and reflection polish",
            segments=8,
            rings=4,
        )


def add_shell_articulation(mats):
    shadow_specs = [
        ("west_lower_sleep_shadow_shell_layer", (-2.55, -0.10, 4.66), (2.25, 0.55, 0.18), 0.18, "base"),
        ("east_lower_sleep_shadow_shell_layer", (2.25, -0.18, 4.52), (2.12, 0.50, 0.16), -0.22, "base"),
        ("central_inner_dark_void_between_shell_layers", (-0.10, 0.18, 4.72), (3.10, 0.62, 0.20), 0.04, "detail"),
        ("rear_upper_nested_shell_shadow_crescent", (0.25, 1.10, 5.28), (2.10, 0.42, 0.15), -0.08, "detail"),
        ("front_soft_cloud_belly_shadow_band", (-0.12, -1.18, 4.46), (3.20, 0.34, 0.12), 0.02, "base"),
        ("silverless_back_shell_gap_shadow_band", (0.42, 1.82, 5.02), (2.35, 0.26, 0.10), -0.18, "detail"),
    ]
    for name, loc, scale, rz, mat_name in shadow_specs:
        uv_ellipsoid(
            name,
            loc,
            scale,
            mats[mat_name],
            "Nested shell gaps and dark sleep shadows",
            segments=14,
            rings=5,
            rot=(0.0, 0.0, rz),
        )

    arc_specs = [
        ("central_shell_contour_soft_upper_ribbon", (0.0, -0.03), 3.65, 2.05, 5.84, 206, 332, 0.026, "detail", 0.12),
        ("west_shell_contour_lobe_transition_ribbon", (-2.28, 0.16), 1.92, 1.18, 5.70, 126, 266, 0.022, "detail", 0.10),
        ("east_shell_contour_lobe_transition_ribbon", (2.14, -0.12), 1.86, 1.06, 5.54, -66, 78, 0.022, "detail", 0.08),
        ("rear_shell_contour_high_sleep_ribbon", (0.30, 1.05), 2.10, 0.82, 6.07, 10, 170, 0.020, "accent", 0.08),
        ("front_lower_cloud_merge_ribbon", (-0.05, -1.32), 3.15, 0.58, 4.86, 194, 346, 0.022, "base", 0.04),
    ]
    for name, center, rx, ry, z, start, end, radius, mat_name, wave in arc_specs:
        segmented_arc(
            name,
            center,
            rx,
            ry,
            z,
            start,
            end,
            radius,
            mats[mat_name],
            "Outer cloud shell and contour articulation",
            segments=10,
            vertices=5,
            height_wave=wave,
        )

    for idx, (loc, scale, rot) in enumerate(
        [
            ((-1.35, -0.82, 5.42), (0.82, 0.075, 0.055), 0.46),
            ((1.28, 0.62, 5.50), (0.72, 0.070, 0.050), -0.36),
            ((-2.88, 0.36, 5.18), (0.62, 0.060, 0.045), 0.12),
            ((2.76, -0.46, 5.04), (0.58, 0.056, 0.042), -0.08),
        ]
    ):
        uv_ellipsoid(
            f"subtle_shell_gap_oval_detail_marker_{idx:02d}",
            loc,
            scale,
            mats["detail"],
            "Nested shell gaps and dark sleep shadows",
            segments=10,
            rings=4,
            rot=(0, 0, rot),
        )


def add_pillar_hardware(mats):
    pillar_positions = [
        (-3.05, -1.55, 3.28),
        (-0.95, -2.30, 3.45),
        (2.48, -1.25, 3.32),
        (-2.15, 1.55, 3.18),
        (2.05, 1.48, 3.26),
    ]
    for idx, (x, y, top_z) in enumerate(pillar_positions):
        torus(
            f"soft_lake_pillar_receptor_dark_collar_{idx:02d}",
            (x, y, 0.155),
            0.54,
            0.025,
            mats["detail"],
            "Indigo light pillar support polish",
            seg=18,
            minor_seg=3,
            scale=(1.18, 0.72, 1.0),
        )
        torus(
            f"muted_indigo_pillar_upper_sleep_halo_{idx:02d}",
            (x, y, top_z + 0.03),
            0.42,
            0.018,
            mats["emissive"],
            "Indigo light pillar support polish",
            seg=16,
            minor_seg=3,
            scale=(1.08, 0.78, 1.0),
        )
        cylinder(
            f"transparent_pillar_core_softened_sleeve_{idx:02d}",
            (x, y, top_z * 0.5 + 0.10),
            0.155,
            max(0.1, top_z - 0.12),
            mats["glass"],
            "Indigo light pillar support polish",
            vertices=8,
        )


def add_wisp_refinement(mats):
    wisp_paths = [
        [(-4.18, 0.72, 5.36), (-4.86, 1.08, 5.31), (-5.54, 1.48, 5.06), (-6.20, 1.82, 4.76)],
        [(3.92, -0.62, 4.88), (4.60, -0.92, 4.70), (5.30, -1.32, 4.36), (5.94, -1.76, 4.02)],
        [(-0.28, -2.70, 5.02), (-0.18, -3.34, 4.88), (0.02, -4.02, 4.58), (0.18, -4.56, 4.24)],
        [(1.16, 2.28, 5.80), (1.48, 2.78, 5.80), (1.96, 3.25, 5.58), (2.30, 3.72, 5.26)],
        [(-3.46, -1.42, 4.64), (-4.12, -1.78, 4.44), (-4.74, -2.18, 4.14), (-5.16, -2.54, 3.86)],
    ]
    for path_idx, points in enumerate(wisp_paths):
        for idx, point in enumerate(points[1:]):
            t = (idx + 1) / (len(points) - 1)
            uv_ellipsoid(
                f"trailing_wisp_fading_sleep_bead_{path_idx:02d}_{idx:02d}",
                point,
                (0.070 * (1.0 - 0.35 * t), 0.040 * (1.0 - 0.45 * t), 0.030 * (1.0 - 0.55 * t)),
                mats["accent"],
                "Trailing edge wisps",
                segments=6,
                rings=3,
                rot=(0, 0, 0.25 * path_idx),
            )
        cone(
            f"trailing_wisp_terminal_fade_taper_{path_idx:02d}",
            points[-1],
            0.055,
            0.006,
            0.34,
            mats["accent"],
            "Trailing edge wisps",
            vertices=7,
            rot=(math.radians(82), 0, math.radians(path_idx * 28)),
        )


def add_star_and_receiver_cleanup(mats):
    extra_stars = [
        (-3.12, 1.22, 5.28, 0.052),
        (-0.92, -1.84, 6.02, 0.048),
        (1.76, 1.12, 5.90, 0.046),
        (2.96, -0.96, 5.70, 0.044),
    ]
    for idx, (x, y, z, size) in enumerate(extra_stars):
        uv_ellipsoid(
            f"session38_sparse_star_light_cleanup_{idx:02d}",
            (x, y, z),
            (size, size, size),
            mats["emissive"],
            "Faint star-like surface lights",
            segments=8,
            rings=4,
        )

    torus(
        "barely_visible_receiver_secondary_sleep_ring_energy",
        (0.05, 0.18, 7.43),
        0.23,
        0.012,
        mats["energy"],
        "Barely visible SIA thread receiver",
        seg=20,
        minor_seg=3,
        scale=(1.1, 0.75, 1.0),
    )
    receiver_paths = [
        ((0.04, 0.18, 7.36), (-0.28, 0.46, 7.62), (-0.44, 0.64, 7.80)),
        ((0.08, 0.16, 7.34), (0.38, 0.02, 7.58), (0.64, -0.10, 7.76)),
    ]
    for idx, (a, b, c) in enumerate(receiver_paths):
        cylinder_between(
            f"minimal_receiver_thread_split_curve_{idx:02d}_a",
            a,
            b,
            0.010,
            mats["energy"],
            "Barely visible SIA thread receiver",
            vertices=6,
        )
        cylinder_between(
            f"minimal_receiver_thread_split_curve_{idx:02d}_b",
            b,
            c,
            0.007,
            mats["energy"],
            "Barely visible SIA thread receiver",
            vertices=6,
        )


def remove_cameras_lights():
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)


def apply_mesh_world_transforms():
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(obj.matrix_world.copy())
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)
        obj.parent = None


def center_bottom_origin():
    min_v, max_v = bbox_vectors()
    correction = Matrix.Translation(Vector((-(min_v.x + max_v.x) / 2.0, -(min_v.y + max_v.y) / 2.0, -min_v.z)))
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(correction)
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)


def pack_export_meshes_by_material():
    groups = {name: [] for name in ALLOWED_MATERIALS}
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        material = obj.data.materials[0] if obj.data.materials else None
        mat_name = material_base_name(material)
        if mat_name in groups:
            groups[mat_name].append(obj)

    mats = ensure_materials()
    packed = []
    for mat_name, objects in sorted(groups.items()):
        if not objects:
            continue
        verts = []
        faces = []
        for obj in objects:
            offset = len(verts)
            verts.extend([tuple(v.co) for v in obj.data.vertices])
            faces.extend([tuple(offset + idx for idx in poly.vertices) for poly in obj.data.polygons])
        mesh = bpy.data.meshes.new(f"recovery_ext_{mat_name}_packed_mesh")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        packed_obj = bpy.data.objects.new(f"recovery_ext_{mat_name}_packed", mesh)
        bpy.context.collection.objects.link(packed_obj)
        packed_obj.data.materials.append(mats[mat_name])
        packed.append(packed_obj)

    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH" and obj not in packed]:
        bpy.data.objects.remove(obj, do_unlink=True)
    return packed


def export_recovery():
    remove_cameras_lights()
    for obj in list(bpy.data.objects):
        if obj.type == "EMPTY":
            bpy.data.objects.remove(obj, do_unlink=True)
    apply_mesh_world_transforms()
    normalize_material_slots()
    center_bottom_origin()
    pack_export_meshes_by_material()

    root = bpy.data.objects.new("recovery-ext", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.parent = root

    bpy.ops.wm.save_as_mainfile(filepath=PACKED_BLEND)
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
    mat_tris = material_triangles()
    return {
        "draft_glb": DRAFT_GLB,
        "approved_glb": APPROVED_GLB,
        "packed_blend": PACKED_BLEND,
        "glb_bytes": os.path.getsize(APPROVED_GLB),
        "tris": scene_triangles(),
        "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "materials": sorted({material_base_name(mat) for mat in bpy.data.materials if mat.users}),
        "material_tris": mat_tris,
        "material_percentages": material_percentages(scene_triangles(), mat_tris),
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
    setup_lighting_and_render()
    imports = [
        ("sia", os.path.join(ROOT, "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb"), (0, 0, 0)),
        ("fitness", os.path.join(ROOT, "modules/01-fitness/exterior/approved/fitness-ext.glb"), (26, 25, 0)),
        ("yoga", os.path.join(ROOT, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb"), (36, 10, 0)),
        ("finance", os.path.join(ROOT, "modules/03-finance/exterior/approved/finance-ext.glb"), (35, -6, 0)),
        ("knowledgebase", os.path.join(ROOT, "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"), (31, -22, 0)),
        ("chat", os.path.join(ROOT, "modules/05-chat-communication/exterior/approved/chat-ext.glb"), (19, -36, 0)),
        ("leaderboard", os.path.join(ROOT, "modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb"), (-8, -45, 0)),
        ("relationships", os.path.join(ROOT, "modules/07-relationships/exterior/approved/relationships-ext.glb"), (8, -59, 0)),
        ("career", os.path.join(ROOT, "modules/08-career/exterior/approved/career-ext.glb"), (-30, -34, 0)),
        ("recovery", APPROVED_GLB, (-43, -8, 0)),
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
    path = render_shot("s38_cohesion_all10.png", (96, -158, 112), (1, -17, 8), 16)
    return {"screenshot": path, "imported": imported_labels}


def build_session_38():
    if not os.path.exists(S37_BLEND):
        raise FileNotFoundError(S37_BLEND)

    print("=== Session 38: Recovery exterior detail, polish, export ===")
    bpy.ops.wm.open_mainfile(filepath=S37_BLEND)
    setup_lighting_and_render()
    mats = normalize_material_slots()
    tune_recovery_materials(mats)

    before_tris = scene_triangles()
    before_meshes = sum(1 for obj in bpy.data.objects if obj.type == "MESH")

    add_lake_reflection_polish(mats)
    add_shell_articulation(mats)
    add_pillar_hardware(mats)
    add_wisp_refinement(mats)
    add_star_and_receiver_cleanup(mats)
    normalize_material_slots()

    after_detail_tris = scene_triangles()
    if after_detail_tris > 15000:
        raise RuntimeError(f"Session 38 detail exceeded exterior budget before export: {after_detail_tris} tris")
    if after_detail_tris < 10000:
        raise RuntimeError(f"Session 38 detail under-used exterior budget before export: {after_detail_tris} tris")

    bpy.ops.wm.save_as_mainfile(filepath=S38_BLEND)

    screenshots = [
        render_shot("s38_front_elevation.png", (0, -24, 6.6), (0, -0.1, 4.2), 38),
        render_shot("s38_three_quarter.png", (17, -22, 9.2), (0.0, 0.0, 4.4), 40),
        render_shot("s38_distance_view.png", (33, -39, 16.4), (0.0, 0.0, 4.3), 44),
        render_dark_first(),
    ]

    mat_tris = material_triangles()
    metrics_before_export = {
        "session": 38,
        "module": "09-recovery-sleep",
        "blender_version": bpy.app.version_string,
        "source_blend": S37_BLEND,
        "blend": S38_BLEND,
        "before_mesh_objects": before_meshes,
        "before_tris": before_tris,
        "after_detail_mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
        "after_detail_tris": after_detail_tris,
        "detail_added_tris": after_detail_tris - before_tris,
        "category_metrics": category_metrics(),
        "material_tris": mat_tris,
        "material_percentages": material_percentages(after_detail_tris, mat_tris),
        "material_surface_area": material_surface_area(),
        "bbox": bbox(),
        "screenshots": screenshots,
        "objects": object_metrics(),
    }

    export_metrics = export_recovery()
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

    print("SESSION38_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_session_38()

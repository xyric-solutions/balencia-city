"""
Balencia City v3 - Module #11 Nutrition
Session 46: Exterior Detail, Polish, Export

Loads the approved Session 45 organic farm-structure major forms, adds deferred
terrace, greenhouse, foliage, irrigation, market, roof, and receiver detail,
exports a packed Draco GLB, validates the import, and captures all-built-
structures cohesion proof.
"""

import importlib.util
import json
import math
import os
import shutil
import sys

import bpy
from mathutils import Matrix, Vector


ROOT = "/Users/hamza/Desktop/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/11-nutrition")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
APPROVED = os.path.join(MODULE, "exterior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")

S45_BLEND = os.path.join(DRAFTS, "nutrition-s45-major-forms.blend")
S46_BLEND = os.path.join(DRAFTS, "nutrition-s46-detail-export.blend")
PACKED_BLEND = os.path.join(DRAFTS, "nutrition-s46-export-packed.blend")
DRAFT_GLB = os.path.join(DRAFTS, "nutrition-ext-draft-s46.glb")
APPROVED_GLB = os.path.join(APPROVED, "nutrition-ext.glb")
METRICS_FILE = os.path.join(DRAFTS, "session46-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS, "session46-qa-import.json")

DISTRICT_HEX = "#D97706"
ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy"}
MIN_TRIS = 12000
MAX_TRIS = 18000

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s46", os.path.join(ROOT, "shared/lighting-rig.py"))
materials_mod = load_module("balencia_materials_s46", os.path.join(ROOT, "shared/material-library.py"))

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
    mats = {}
    for mat in bpy.data.materials:
        base = material_base_name(mat)
        if base in ALLOWED_MATERIALS and base not in mats:
            mats[base] = mat
    if ALLOWED_MATERIALS - set(mats):
        materials_mod.create_materials(DISTRICT_HEX, include_energy=True, include_holo=False)
        mats = {}
        for mat in bpy.data.materials:
            base = material_base_name(mat)
            if base in ALLOWED_MATERIALS and base not in mats:
                mats[base] = mat
    missing = sorted(ALLOWED_MATERIALS - set(mats))
    if missing:
        raise RuntimeError(f"Missing material slots after setup: {missing}")
    for name, mat in mats.items():
        mat.name = name
    return mats


def tune_nutrition_materials(mats):
    set_principled(mats["base"], base_hex="#24221C")
    set_principled(mats["accent"], base_hex="#1F6F3A", emission_hex="#34A853", emission_strength=0.14)
    set_principled(mats["glass"], base_hex="#151714", emission_hex="#FBBF24", emission_strength=0.05, alpha=0.86)
    set_principled(mats["detail"], base_hex="#17150F")
    set_principled(mats["emissive"], base_hex="#221408", emission_hex=DISTRICT_HEX, emission_strength=0.14)
    set_principled(mats["energy"], base_hex="#271005", emission_hex="#FF5E00", emission_strength=0.14)


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
    if obj is not None and obj.type == "MESH":
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return obj


def shade_smooth(obj):
    if obj is not None and obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def apply_transforms(obj, location=False, rotation=True, scale=True):
    if obj is None:
        return obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
    obj.select_set(False)
    return obj


def box(name, loc, dims, mat, category, rot_z=0.0, bevel=0.0, bevel_segments=1):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rot_z))
    obj = current_object()
    obj.name = name
    obj.scale = dims
    assign(obj, mat)
    apply_transforms(obj)
    if bevel > 0:
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        mod = obj.modifiers.new("soft_agricultural_bevel", "BEVEL")
        mod.width = bevel
        mod.segments = bevel_segments
        mod.profile = 0.5
        bpy.ops.object.modifier_apply(modifier=mod.name)
        try:
            normal = obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
            bpy.ops.object.modifier_apply(modifier=normal.name)
        except Exception:
            pass
        obj.select_set(False)
    return register(obj, category)


def cylinder(name, loc, radius, depth, mat, category, vertices=8, rot=(0.0, 0.0, 0.0)):
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
    return register(obj, category)


def cone(name, loc, radius1, radius2, depth, mat, category, vertices=8, rot=(0.0, 0.0, 0.0)):
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


def torus(name, loc, major, minor, mat, category, seg=18, minor_seg=4, rot=(0, 0, 0), scale=(1.0, 1.0, 1.0)):
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


def ico(name, loc, radius, mat, category):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=loc)
    obj = current_object()
    obj.name = name
    assign(obj, mat)
    shade_smooth(obj)
    apply_transforms(obj)
    return register(obj, category)


def cylinder_between(name, start, end, radius, mat, category, vertices=5):
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


def make_leaf(name, loc, size, mat, category, side="front", tilt=0.0):
    x, y, z = loc
    s = size
    if side in {"front", "rear"}:
        verts = [
            (x, y, z + s * 0.62),
            (x + s * 0.35, y, z + tilt),
            (x, y, z - s * 0.62),
            (x - s * 0.35, y, z - tilt),
        ]
    else:
        verts = [
            (x, y, z + s * 0.62),
            (x, y + s * 0.35, z + tilt),
            (x, y, z - s * 0.62),
            (x, y - s * 0.35, z - tilt),
        ]
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    return register(obj, category)


def tier_specs():
    tiers = 12
    z_start = 0.98
    floor_step = 0.50
    floor_depth = 0.42
    specs = []
    for idx in range(tiers):
        t = idx / (tiers - 1)
        specs.append(
            {
                "idx": idx + 1,
                "width": 8.85 - 5.05 * t,
                "depth": 6.15 - 3.25 * t,
                "z0": z_start + idx * floor_step,
                "z1": z_start + idx * floor_step + floor_depth,
                "t": t,
            }
        )
    return specs


def setup_lighting_and_render():
    try:
        if hasattr(lighting, "clear_lighting"):
            lighting.clear_lighting()
        lighting.setup_viewport_lighting()
    except Exception as exc:
        print("Lighting setup warning: " + repr(exc))
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
            eevee.bloom_threshold = 0.36
            eevee.bloom_intensity = 0.55
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.58


def render_shot(filename, camera_loc, target, lens=40):
    cam_data = bpy.data.cameras.new(filename.replace(".png", "_Camera"))
    cam = bpy.data.objects.new(filename.replace(".png", "_Camera"), cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    direction = Vector(target) - Vector(camera_loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.clip_start = 0.1
    cam.data.clip_end = 300
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
    path = render_shot("s46_dark_first.png", (17, -24, 11.6), (0.0, -0.1, 4.4), 40)
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
    if "greenhouse" in name or "hydroponic" in name or "seedling" in name:
        return "Greenhouse panels and hydroponic detail"
    if "plant" in name or "leaf" in name or "vine" in name or "foliage" in name:
        return "Cascading plant refinement"
    if "market" in name or "produce" in name or "crate" in name or "stall" in name:
        return "Open market and produce detail"
    if "irrigation" in name or "water" in name or "valve" in name or "downspout" in name:
        return "Irrigation channels and valves"
    if "roof" in name or "chimney" in name or "vent" in name:
        return "Roof kitchen vent and service polish"
    if "pipeline" in name or "socket" in name or "receiver" in name:
        return "SIA hard-pipeline receiver"
    if "tier" in name or "terrace" in name or "farm_bed" in name or "floor" in name:
        return "Tier edge and terrace polish"
    return "Nutrition exterior detail"


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


def add_tier_edge_polish(mats):
    category = "Tier edge and terrace polish"
    for spec in tier_specs():
        idx = spec["idx"]
        width = spec["width"]
        depth = spec["depth"]
        z0 = spec["z0"]
        z1 = spec["z1"]
        terrace_z = z1 + 0.072

        box(f"tier_{idx:02d}_front_dark_underledge_shadow", (0, -depth * 0.5 - 0.135, z0 + 0.08), (width * 0.92, 0.034, 0.038), mats["detail"], category)
        box(f"tier_{idx:02d}_rear_dark_underledge_shadow", (0, depth * 0.5 + 0.135, z0 + 0.08), (width * 0.74, 0.034, 0.038), mats["detail"], category)
        box(f"tier_{idx:02d}_left_dark_underledge_shadow", (-width * 0.5 - 0.135, 0, z0 + 0.08), (0.034, depth * 0.62, 0.038), mats["detail"], category)
        box(f"tier_{idx:02d}_right_dark_underledge_shadow", (width * 0.5 + 0.135, 0, z0 + 0.08), (0.034, depth * 0.62, 0.038), mats["detail"], category)

        box(f"tier_{idx:02d}_front_recessed_base_shadow_panel", (0, -depth * 0.5 - 0.047, z0 + 0.225), (width * 0.74, 0.018, 0.24), mats["base"], category)
        box(f"tier_{idx:02d}_rear_recessed_base_shadow_panel", (0, depth * 0.5 + 0.047, z0 + 0.225), (width * 0.62, 0.018, 0.22), mats["base"], category)

        for jdx, x_frac in enumerate([-0.36, -0.12, 0.12, 0.36]):
            box(
                f"tier_{idx:02d}_front_farm_bed_divider_{jdx:02d}",
                (width * x_frac, -depth * 0.5 - 0.205, terrace_z),
                (0.026, 0.18, 0.045),
                mats["detail"],
                category,
            )
        for side, sign in [("left", -1), ("right", 1)]:
            for jdx, y_frac in enumerate([-0.24, 0.24]):
                box(
                    f"tier_{idx:02d}_{side}_farm_bed_divider_{jdx:02d}",
                    (sign * (width * 0.5 + 0.205), depth * y_frac, terrace_z),
                    (0.17, 0.026, 0.045),
                    mats["detail"],
                    category,
                )

        box(f"tier_{idx:02d}_front_amber_light_dark_louver", (0, -depth * 0.5 - 0.19, z1 + 0.18), (width * 0.80, 0.020, 0.030), mats["detail"], category)
        box(f"tier_{idx:02d}_rear_amber_light_dark_louver", (0, depth * 0.5 + 0.19, z1 + 0.18), (width * 0.60, 0.020, 0.030), mats["detail"], category)
        box(f"tier_{idx:02d}_left_amber_light_dark_louver", (-width * 0.5 - 0.19, 0, z1 + 0.18), (0.020, depth * 0.56, 0.030), mats["detail"], category)
        box(f"tier_{idx:02d}_right_amber_light_dark_louver", (width * 0.5 + 0.19, 0, z1 + 0.18), (0.020, depth * 0.56, 0.030), mats["detail"], category)


def add_greenhouse_polish(mats):
    category = "Greenhouse panels and hydroponic detail"
    specs = [
        ("front_mid", "front", (-2.25, -3.385, 3.18), (1.35, 0.28, 1.35)),
        ("right_lower", "side", (4.325, -0.72, 2.02), (0.28, 1.45, 1.18)),
        ("left_upper", "side", (-3.225, 0.78, 4.82), (0.28, 1.24, 1.18)),
    ]
    for prefix, side, loc, dims in specs:
        x, y, z = loc
        sx, sy, sz = dims
        if side == "front":
            box(f"{prefix}_greenhouse_outer_dark_header_frame", (x, y - 0.022, z + sz * 0.47), (sx * 0.94, 0.030, 0.040), mats["detail"], category)
            box(f"{prefix}_greenhouse_outer_dark_sill_frame", (x, y - 0.022, z - sz * 0.47), (sx * 0.94, 0.030, 0.040), mats["detail"], category)
            for col, xoff in enumerate([-0.42, -0.20, 0.0, 0.20, 0.42]):
                box(f"{prefix}_greenhouse_fine_vertical_mullion_{col:02d}", (x + sx * xoff, y - 0.036, z), (0.018, 0.020, sz * 0.82), mats["detail"], category)
            for row, zoff in enumerate([-0.24, 0.0, 0.24]):
                box(f"{prefix}_hydroponic_seedling_tray_{row:02d}", (x, y - 0.060, z + sz * zoff), (sx * 0.76, 0.028, 0.034), mats["accent"], category)
                for col, xoff in enumerate([-0.30, 0.0, 0.30]):
                    cylinder(f"{prefix}_hydroponic_tube_{row:02d}_{col:02d}", (x + sx * xoff, y - 0.075, z + sz * zoff + 0.07), 0.014, 0.34, mats["detail"], category, vertices=6, rot=(math.radians(90), 0, 0))
            box(f"{prefix}_greenhouse_warm_roof_grow_cap", (x, y - 0.060, z + sz * 0.58), (sx * 0.72, 0.020, 0.026), mats["emissive"], category)
        else:
            box(f"{prefix}_greenhouse_outer_dark_header_frame", (x, y, z + sz * 0.47), (0.030, sy * 0.94, 0.040), mats["detail"], category)
            box(f"{prefix}_greenhouse_outer_dark_sill_frame", (x, y, z - sz * 0.47), (0.030, sy * 0.94, 0.040), mats["detail"], category)
            for col, yoff in enumerate([-0.42, -0.20, 0.0, 0.20, 0.42]):
                box(f"{prefix}_greenhouse_fine_side_mullion_{col:02d}", (x, y + sy * yoff, z), (0.020, 0.018, sz * 0.80), mats["detail"], category)
            for row, zoff in enumerate([-0.24, 0.0, 0.24]):
                box(f"{prefix}_hydroponic_side_seedling_tray_{row:02d}", (x, y, z + sz * zoff), (0.028, sy * 0.72, 0.034), mats["accent"], category)
                for col, yoff in enumerate([-0.28, 0.0, 0.28]):
                    cylinder(f"{prefix}_hydroponic_side_tube_{row:02d}_{col:02d}", (x, y + sy * yoff, z + sz * zoff + 0.07), 0.014, 0.32, mats["detail"], category, vertices=6, rot=(0, math.radians(90), 0))
            box(f"{prefix}_greenhouse_warm_side_roof_grow_cap", (x, y, z + sz * 0.58), (0.020, sy * 0.68, 0.026), mats["emissive"], category)


def add_foliage_refinement(mats):
    category = "Cascading plant refinement"
    for spec in tier_specs()[1:]:
        idx = spec["idx"]
        width = spec["width"]
        depth = spec["depth"]
        z1 = spec["z1"]
        front_y = -depth * 0.5 - 0.315
        for cidx, x_frac in enumerate([-0.38, -0.12, 0.14, 0.38]):
            height = 0.42 + 0.08 * ((idx + cidx) % 4)
            x = width * x_frac
            cylinder_between(
                f"tier_{idx:02d}_front_varied_hanging_vine_{cidx:02d}",
                (x, front_y, z1 + 0.02),
                (x + 0.05 * math.sin(idx + cidx), front_y - 0.02, z1 - height),
                0.014,
                mats["accent"],
                category,
                vertices=5,
            )
            for leaf_idx, frac in enumerate([0.22, 0.50, 0.76]):
                leaf_z = z1 - height * frac
                make_leaf(
                    f"tier_{idx:02d}_front_leaf_cluster_{cidx:02d}_{leaf_idx:02d}",
                    (x + 0.04 * ((leaf_idx % 2) - 0.5), front_y - 0.018, leaf_z),
                    0.105 - leaf_idx * 0.012,
                    mats["accent"],
                    category,
                    side="front",
                    tilt=0.012 * math.sin(idx + leaf_idx),
                )
        if idx % 2 == 0:
            for side, sign in [("left", -1), ("right", 1)]:
                x = sign * (width * 0.5 + 0.325)
                for cidx, y_frac in enumerate([-0.24, 0.18]):
                    y = depth * y_frac
                    cylinder_between(
                        f"tier_{idx:02d}_{side}_side_trailing_vine_{cidx:02d}",
                        (x, y, z1 + 0.02),
                        (x + sign * 0.02, y + 0.04 * math.sin(idx + cidx), z1 - 0.42),
                        0.013,
                        mats["accent"],
                        category,
                        vertices=5,
                    )
                    for leaf_idx in range(2):
                        make_leaf(
                            f"tier_{idx:02d}_{side}_side_leaf_cluster_{cidx:02d}_{leaf_idx:02d}",
                            (x + sign * 0.012, y + 0.025 * leaf_idx, z1 - 0.14 - 0.16 * leaf_idx),
                            0.095,
                            mats["accent"],
                            category,
                            side="side",
                            tilt=0.010,
                        )


def add_irrigation_hardware(mats):
    category = "Irrigation channels and valves"
    for spec in tier_specs():
        idx = spec["idx"]
        width = spec["width"]
        depth = spec["depth"]
        z1 = spec["z1"]
        front_y = -depth * 0.5 - 0.265
        box(f"tier_{idx:02d}_front_irrigation_dark_trough_lip", (0, front_y, z1 + 0.025), (width * 0.74, 0.020, 0.025), mats["detail"], category)
        if idx % 3 == 0:
            x = -width * 0.38
            cylinder_between(
                f"tier_{idx:02d}_front_irrigation_drop_pipe",
                (x, front_y - 0.012, z1 + 0.03),
                (x, front_y - 0.012, z1 - 0.42),
                0.017,
                mats["detail"],
                category,
                vertices=6,
            )
            ico(f"tier_{idx:02d}_front_irrigation_valve_node", (x, front_y - 0.016, z1 - 0.15), 0.055, mats["detail"], category)
        if idx in {4, 8, 12}:
            for sign in [-1, 1]:
                x = sign * (width * 0.5 + 0.25)
                cylinder_between(
                    f"tier_{idx:02d}_{'left' if sign < 0 else 'right'}_side_irrigation_riser",
                    (x, -depth * 0.22, z1 + 0.02),
                    (x, depth * 0.25, z1 - 0.08),
                    0.015,
                    mats["detail"],
                    category,
                    vertices=6,
                )


def add_market_polish(mats):
    category = "Open market and produce detail"
    box("open_market_front_dark_wayfinding_sign_frame", (0, -3.71, 0.83), (2.15, 0.040, 0.30), mats["detail"], category, bevel=0.015)
    box("open_market_front_warm_nutrition_sign_panel", (0, -3.735, 0.84), (1.72, 0.016, 0.16), mats["emissive"], category)
    for idx, x in enumerate([-3.15, -1.85, -0.55, 0.55, 1.85, 3.15]):
        box(f"open_market_low_produce_crate_{idx:02d}", (x, -3.02, 0.32), (0.42, 0.34, 0.18), mats["detail"], category, bevel=0.018)
        box(f"open_market_crate_amber_underlight_{idx:02d}", (x, -3.205, 0.43), (0.34, 0.016, 0.024), mats["emissive"], category)
        for item in range(4):
            px = x - 0.14 + item * 0.09
            pz = 0.46 + 0.035 * (item % 2)
            ico(f"open_market_visible_green_produce_{idx:02d}_{item:02d}", (px, -3.08, pz), 0.055, mats["accent"], category)
    for side, sx in [("left", -1), ("right", 1)]:
        cylinder_between(f"open_market_{side}_canopy_diagonal_brace_front", (sx * 4.1, -3.05, 0.42), (sx * 3.55, -2.52, 0.96), 0.025, mats["detail"], category, vertices=6)
        cylinder_between(f"open_market_{side}_canopy_diagonal_brace_rear", (sx * 4.1, 2.75, 0.42), (sx * 3.55, 2.32, 0.96), 0.025, mats["detail"], category, vertices=6)
    for idx, x in enumerate([-2.7, -1.35, 0.0, 1.35, 2.7]):
        cylinder(f"open_market_ceiling_warm_pendant_grow_lamp_{idx:02d}", (x, -1.58, 0.78), 0.055, 0.08, mats["emissive"], category, vertices=10)
        cone(f"open_market_dark_pendant_lamp_shade_{idx:02d}", (x, -1.58, 0.73), 0.15, 0.055, 0.16, mats["detail"], category, vertices=10)


def add_roof_and_receiver_polish(mats):
    category = "Roof kitchen vent and service polish"
    roof_z = tier_specs()[-1]["z1"] + 0.10
    for idx, y in enumerate([-0.66, -0.22, 0.22, 0.66]):
        box(f"roof_service_guardrail_front_segment_{idx:02d}", (-1.04 + idx * 0.69, -0.98, roof_z + 0.25), (0.42, 0.026, 0.24), mats["detail"], category)
        box(f"roof_service_guardrail_rear_segment_{idx:02d}", (-1.04 + idx * 0.69, 0.98, roof_z + 0.25), (0.42, 0.026, 0.24), mats["detail"], category)
        box(f"roof_service_guardrail_left_segment_{idx:02d}", (-1.34, y, roof_z + 0.25), (0.026, 0.30, 0.24), mats["detail"], category)
        box(f"roof_service_guardrail_right_segment_{idx:02d}", (1.34, y, roof_z + 0.25), (0.026, 0.30, 0.24), mats["detail"], category)
    for idx, angle in enumerate([0, 60, 120, 180, 240, 300]):
        a = math.radians(angle)
        cylinder_between(
            f"roof_kitchen_chimney_dark_vent_fin_{idx:02d}",
            (0.74 + math.cos(a) * 0.19, 0.20 + math.sin(a) * 0.19, roof_z + 0.90),
            (0.74 + math.cos(a) * 0.30, 0.20 + math.sin(a) * 0.30, roof_z + 1.32),
            0.015,
            mats["detail"],
            category,
            vertices=5,
        )
    torus("roof_kitchen_chimney_secondary_warm_exhaust_halo", (0.74, 0.20, roof_z + 1.58), 0.20, 0.015, mats["emissive"], category, seg=18, minor_seg=4)
    box("roof_service_dark_maintenance_pad", (-0.80, 0.18, roof_z + 0.19), (0.52, 0.46, 0.035), mats["detail"], category, bevel=0.015)

    receiver_category = "SIA hard-pipeline receiver"
    top = tier_specs()[-1]
    receiver_z = top["z1"] - 0.28
    torus(
        "rear_roof_orange_sia_pipeline_receiver_inner_lock_ring",
        (0.0, top["depth"] * 0.5 + 0.575, receiver_z),
        0.24,
        0.025,
        mats["energy"],
        receiver_category,
        seg=20,
        minor_seg=4,
        rot=(math.radians(90), 0, 0),
    )
    for idx, x in enumerate([-0.34, -0.12, 0.12, 0.34]):
        cylinder_between(
            f"rear_roof_orange_pipeline_receiver_locking_lug_{idx:02d}",
            (x, top["depth"] * 0.5 + 0.37, receiver_z - 0.18),
            (x * 0.65, top["depth"] * 0.5 + 0.58, receiver_z + 0.18),
            0.018,
            mats["energy"],
            receiver_category,
            vertices=5,
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
        mat_name = material_base_name(obj.data.materials[0]) if obj.data.materials else ""
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
        mesh = bpy.data.meshes.new(f"nutrition_ext_{mat_name}_packed_mesh")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        packed_obj = bpy.data.objects.new(f"nutrition_ext_{mat_name}_packed", mesh)
        bpy.context.collection.objects.link(packed_obj)
        packed_obj.data.materials.append(mats[mat_name])
        packed.append(packed_obj)

    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH" and obj not in packed]:
        bpy.data.objects.remove(obj, do_unlink=True)
    return packed


def export_nutrition():
    remove_cameras_lights()
    for obj in list(bpy.data.objects):
        if obj.type == "EMPTY":
            bpy.data.objects.remove(obj, do_unlink=True)
    apply_mesh_world_transforms()
    normalize_material_slots()
    center_bottom_origin()
    pack_export_meshes_by_material()

    root = bpy.data.objects.new("nutrition-ext", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.parent = root

    bpy.ops.wm.save_as_mainfile(filepath=PACKED_BLEND)
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
        "material_surface_area": material_surface_area(),
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
        ("recovery", os.path.join(ROOT, "modules/09-recovery-sleep/exterior/approved/recovery-ext.glb"), (-43, -8, 0)),
        ("analytics", os.path.join(ROOT, "modules/10-ai-analytics/exterior/approved/analytics-ext.glb"), (-31, 14, 0)),
        ("nutrition", APPROVED_GLB, (-8, 41, 0)),
    ]
    imported_labels = []
    for label, path, loc in imports:
        if not os.path.exists(path):
            continue
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=path)
        imported = [obj for obj in bpy.data.objects if obj not in before]
        for obj in imported:
            obj.name = f"{label}_{obj.name}"
        for obj in [obj for obj in imported if obj.parent is None]:
            obj.location.x += loc[0]
            obj.location.y += loc[1]
            obj.location.z += loc[2]
        imported_labels.append(label)
    path = render_shot("s46_cohesion_all12.png", (108, -154, 118), (0, -10, 9), 16)
    return {"screenshot": path, "imported": imported_labels}


def build_session_46():
    if not os.path.exists(S45_BLEND):
        raise FileNotFoundError(S45_BLEND)

    print("=== Session 46: Nutrition exterior detail, polish, export ===")
    bpy.ops.wm.open_mainfile(filepath=S45_BLEND)
    setup_lighting_and_render()
    mats = normalize_material_slots()
    tune_nutrition_materials(mats)

    before_tris = scene_triangles()
    before_meshes = sum(1 for obj in bpy.data.objects if obj.type == "MESH")

    add_tier_edge_polish(mats)
    add_greenhouse_polish(mats)
    add_foliage_refinement(mats)
    add_irrigation_hardware(mats)
    add_market_polish(mats)
    add_roof_and_receiver_polish(mats)
    normalize_material_slots()

    after_detail_tris = scene_triangles()
    if after_detail_tris > MAX_TRIS:
        raise RuntimeError(f"Session 46 detail exceeded exterior budget before export: {after_detail_tris} tris")
    if after_detail_tris < MIN_TRIS:
        raise RuntimeError(f"Session 46 detail under-used exterior budget before export: {after_detail_tris} tris")

    bpy.ops.wm.save_as_mainfile(filepath=S46_BLEND)

    screenshots = [
        render_shot("s46_front_elevation.png", (0, -24, 7.4), (0, -0.1, 4.25), 38),
        render_shot("s46_three_quarter.png", (17, -22, 10.2), (0.0, 0.0, 4.55), 40),
        render_shot("s46_distance_view.png", (31, -38, 17.0), (0.0, 0.0, 4.75), 45),
        render_dark_first(),
    ]

    mat_tris = material_triangles()
    metrics_before_export = {
        "session": 46,
        "module": "11-nutrition",
        "blender_version": bpy.app.version_string,
        "source_blend": S45_BLEND,
        "blend": S46_BLEND,
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

    export_metrics = export_nutrition()
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

    print("SESSION46_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_session_46()

if os.environ.get("BALENCIA_QUIT_AFTER_RUN", "0") == "1":
    bpy.ops.wm.quit_blender()

"""
Balencia City v3 - Module #10 AI Analytics
Session 42: Exterior Detail, Polish, Export

Loads the approved Session 41 Data Cathedral major forms, adds the deferred
living-wall, buttress, arch, crown, entrance, and plaza detail pass, exports a
packed Draco GLB, validates the import, and captures all-built-structures
cohesion proof.
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
MODULE = os.path.join(ROOT, "modules/10-ai-analytics")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
APPROVED = os.path.join(MODULE, "exterior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")

S41_BLEND = os.path.join(DRAFTS, "analytics-s41-major-forms.blend")
S42_BLEND = os.path.join(DRAFTS, "analytics-s42-detail-export.blend")
PACKED_BLEND = os.path.join(DRAFTS, "analytics-s42-export-packed.blend")
DRAFT_GLB = os.path.join(DRAFTS, "analytics-ext-draft-s42.glb")
APPROVED_GLB = os.path.join(APPROVED, "analytics-ext.glb")
METRICS_FILE = os.path.join(DRAFTS, "session42-metrics.json")
QA_IMPORT_FILE = os.path.join(DRAFTS, "session42-qa-import.json")

DISTRICT_HEX = "#14B8A6"
ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}

for path in (DRAFTS, APPROVED, SCREENSHOTS):
    os.makedirs(path, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s42", os.path.join(ROOT, "shared/lighting-rig.py"))
materials_mod = load_module("balencia_materials_s42", os.path.join(ROOT, "shared/material-library.py"))

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
    existing = {
        material_base_name(mat): mat
        for mat in bpy.data.materials
        if material_base_name(mat) in ALLOWED_MATERIALS
    }
    if any(name not in existing for name in ALLOWED_MATERIALS):
        materials_mod.create_materials(DISTRICT_HEX, include_energy=True, include_holo=True)
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


def tune_analytics_materials(mats):
    set_principled(mats["base"], base_hex="#1B1C27")
    set_principled(mats["detail"], base_hex="#11141C")
    set_principled(mats["accent"], base_hex="#103433", emission_hex=DISTRICT_HEX, emission_strength=0.12)
    set_principled(mats["glass"], base_hex="#07171B", emission_hex="#9AF3E7", emission_strength=0.035, alpha=0.82)
    set_principled(mats["emissive"], base_hex="#082323", emission_hex=DISTRICT_HEX, emission_strength=0.20)
    set_principled(mats["energy"], base_hex="#211008", emission_hex="#FF5E00", emission_strength=0.14)
    set_principled(mats["holo"], base_hex="#062B2B", emission_hex=DISTRICT_HEX, emission_strength=0.22, alpha=0.46)


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


def box(name, loc, dims, mat, category, rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rot_z))
    obj = current_object()
    obj.name = name
    obj.scale = dims
    assign(obj, mat)
    apply_transforms(obj)
    return register(obj, category)


def cylinder(name, loc, radius, depth, mat, category, vertices=10, rot=(0.0, 0.0, 0.0)):
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


def cone(name, loc, radius1, radius2, depth, mat, category, vertices=10, rot=(0.0, 0.0, 0.0)):
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


def torus(name, loc, major, minor, mat, category, seg=20, minor_seg=4, scale=(1.0, 1.0, 1.0), rot=(0, 0, 0)):
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


def cylinder_between(name, start, end, radius, mat, category, vertices=6):
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


def make_mesh(name, verts, faces, mat, category, shade=False):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    if shade:
        shade_smooth(obj)
    return register(obj, category)


def width_depth_at_z(z):
    base_z = 0.24
    body_height = 12.0
    t = max(0.0, min(1.0, (z - base_z) / body_height))
    width = 4.2 + (2.75 - 4.2) * t
    depth = 5.7 + (4.05 - 5.7) * t
    return width, depth


def setup_lighting_and_render():
    try:
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
            eevee.bloom_threshold = 0.34
            eevee.bloom_intensity = 0.62
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
    cam.data.clip_end = 280
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
    path = render_shot("s42_dark_first.png", (17, -24, 13.0), (0.0, -0.1, 8.2), 40)
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
    if "buttress" in name or "anchor" in name or "platform" in name:
        return "Flying buttress data conduits and observation hardware"
    if "spire" in name or "beacon" in name or "crown" in name or "pipeline_receiver" in name:
        return "Central spire, beacon, and SIA hardpoint"
    if "arch" in name or "window" in name or "mullion" in name:
        return "Pointed holographic data windows"
    if "waterfall" in name or "entry" in name or "doorway" in name:
        return "Data-waterfall entrance"
    if "dashboard" in name or "data_stream" in name or "floor_band" in name or "chart" in name or "heatmap" in name:
        return "Living facade data displays"
    if "roof" in name or "rib" in name:
        return "Cathedral roof and ridge polish"
    if "plaza" in name or "trace" in name or "threshold" in name:
        return "Analytics plaza and ground data lattice"
    if "foundation" in name or "body" in name or "aisle" in name or "nave" in name:
        return "Cathedral body and foundation"
    return "Analytics cathedral exterior detail"


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


def add_facade_panel_depth(mats):
    category = "Facade panel depth and cathedral scale ribs"
    for floor in range(3, 31, 3):
        z = 0.24 + 12.0 * (floor / 30)
        width, depth = width_depth_at_z(z)
        box(f"front_dark_floor_plate_shadow_ledge_{floor:02d}", (0, -depth * 0.5 - 0.058, z), (width * 0.92, 0.026, 0.035), mats["detail"], category)
        box(f"rear_dark_floor_plate_shadow_ledge_{floor:02d}", (0, depth * 0.5 + 0.058, z), (width * 0.82, 0.026, 0.035), mats["detail"], category)
        box(f"left_side_floor_plate_shadow_ledge_{floor:02d}", (-width * 0.5 - 0.058, 0, z), (0.026, depth * 0.75, 0.035), mats["detail"], category)
        box(f"right_side_floor_plate_shadow_ledge_{floor:02d}", (width * 0.5 + 0.058, 0, z), (0.026, depth * 0.75, 0.035), mats["detail"], category)

    for idx, x_frac in enumerate([-0.42, -0.21, 0.21, 0.42]):
        x = 4.2 * x_frac
        box(f"front_recessed_vertical_cathedral_panel_rib_{idx:02d}", (x, -2.93, 6.55), (0.036, 0.035, 10.8), mats["base"], category)
        box(f"rear_recessed_vertical_cathedral_panel_rib_{idx:02d}", (x * 0.86, 2.93, 6.25), (0.032, 0.035, 9.8), mats["base"], category)
    for side, x in [("left", -2.13), ("right", 2.13)]:
        for idx, y in enumerate([-2.08, -0.78, 0.78, 2.08]):
            box(f"{side}_side_deep_panel_shadow_rib_{idx:02d}", (x, y, 5.85), (0.036, 0.035, 8.7), mats["base"], category)


def add_panel_cells_front(prefix, cx, y, cz, width, height, rows, cols, mats):
    category = "Dense living-wall chart articulation"
    box(f"{prefix}_dark_recessed_data_screen_backer", (cx, y, cz), (width, 0.026, height), mats["glass"], category)
    cell_w = width / (cols + 1.8)
    cell_h = height / (rows + 1.8)
    x0 = cx - width * 0.40
    z0 = cz - height * 0.40
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 5 == 0:
                continue
            x = x0 + col * cell_w * 1.18
            z = z0 + row * cell_h * 1.18
            mat = mats["emissive"] if (row * 3 + col) % 4 else mats["accent"]
            box(f"{prefix}_heatmap_cell_{row:02d}_{col:02d}", (x, y - 0.027, z), (cell_w * 0.48, 0.018, cell_h * 0.34), mat, category)
    for idx in range(3):
        z = cz - height * 0.25 + idx * height * 0.22
        box(f"{prefix}_dashboard_trend_microline_{idx:02d}", (cx, y - 0.033, z), (width * (0.34 + idx * 0.10), 0.016, 0.018), mats["emissive"], category, rot_z=math.radians(-8 + idx * 8))


def add_panel_cells_side(prefix, x, cy, cz, depth, height, rows, cols, mats):
    category = "Dense living-wall chart articulation"
    box(f"{prefix}_dark_side_data_screen_backer", (x, cy, cz), (0.026, depth, height), mats["glass"], category)
    cell_d = depth / (cols + 1.8)
    cell_h = height / (rows + 1.8)
    y0 = cy - depth * 0.40
    z0 = cz - height * 0.40
    for row in range(rows):
        for col in range(cols):
            if (row * 2 + col) % 5 == 0:
                continue
            y = y0 + col * cell_d * 1.18
            z = z0 + row * cell_h * 1.18
            mat = mats["emissive"] if (row + col) % 3 else mats["accent"]
            box(f"{prefix}_side_heatmap_cell_{row:02d}_{col:02d}", (x, y, z), (0.018, cell_d * 0.48, cell_h * 0.34), mat, category)


def add_living_wall_chart_density(mats):
    add_panel_cells_front("front_lower_left_dense_analytics_wall", -1.28, -2.99, 5.22, 0.96, 1.56, 6, 7, mats)
    add_panel_cells_front("front_lower_right_dense_analytics_wall", 1.28, -2.99, 5.22, 0.96, 1.56, 6, 7, mats)
    add_panel_cells_front("front_upper_nave_prediction_wall", 0.0, -2.67, 9.72, 1.35, 1.42, 5, 7, mats)
    add_panel_cells_front("rear_live_city_status_wall_left", -0.92, 2.99, 6.35, 1.12, 1.52, 5, 7, mats)
    add_panel_cells_front("rear_live_city_status_wall_right", 0.92, 2.99, 8.82, 1.02, 1.36, 5, 6, mats)
    for side, x in [("left", -3.41), ("right", 3.41)]:
        add_panel_cells_side(f"{side}_forward_buttress_data_wall", x, -1.22, 5.12, 1.18, 1.34, 5, 6, mats)
        add_panel_cells_side(f"{side}_rear_buttress_data_wall", x, 1.28, 7.08, 1.18, 1.34, 5, 6, mats)


def add_arch_detail_front(prefix, cx, y, base_z, width, height, mats):
    category = "Pointed arch mullions and holographic scan detail"
    w = width * 0.5
    shoulder = base_z + height * 0.64
    peak = base_z + height
    mid_z = base_z + height * 0.34
    box(f"{prefix}_central_dark_arch_mullion", (cx, y - 0.035, mid_z), (0.032, 0.022, height * 0.64), mats["detail"], category)
    box(f"{prefix}_lower_arch_sill_shadow", (cx, y - 0.038, base_z + 0.04), (width * 1.12, 0.025, 0.045), mats["detail"], category)
    box(f"{prefix}_upper_arch_shoulder_crossbar", (cx, y - 0.040, shoulder - 0.05), (width * 0.78, 0.021, 0.032), mats["detail"], category)
    cylinder_between(f"{prefix}_secondary_left_arch_lancet", (cx - w * 0.46, y - 0.04, shoulder - 0.08), (cx, y - 0.04, peak - 0.16), 0.016, mats["detail"], category)
    cylinder_between(f"{prefix}_secondary_right_arch_lancet", (cx + w * 0.46, y - 0.04, shoulder - 0.08), (cx, y - 0.04, peak - 0.16), 0.016, mats["detail"], category)
    for idx in range(4):
        z = base_z + height * (0.18 + 0.12 * idx)
        box(f"{prefix}_holo_window_horizontal_scanline_{idx:02d}", (cx, y - 0.046, z), (width * (0.48 + 0.08 * idx), 0.014, 0.014), mats["holo"], category)


def add_arch_detail_side(prefix, x, cy, base_z, depth, height, mats):
    category = "Pointed arch mullions and holographic scan detail"
    d = depth * 0.5
    shoulder = base_z + height * 0.64
    peak = base_z + height
    box(f"{prefix}_side_central_dark_arch_mullion", (x, cy, base_z + height * 0.34), (0.021, 0.032, height * 0.64), mats["detail"], category)
    box(f"{prefix}_side_lower_arch_sill_shadow", (x, cy, base_z + 0.04), (0.022, depth * 1.10, 0.045), mats["detail"], category)
    cylinder_between(f"{prefix}_side_secondary_lancet_a", (x, cy - d * 0.46, shoulder - 0.08), (x, cy, peak - 0.16), 0.015, mats["detail"], category)
    cylinder_between(f"{prefix}_side_secondary_lancet_b", (x, cy + d * 0.46, shoulder - 0.08), (x, cy, peak - 0.16), 0.015, mats["detail"], category)
    for idx in range(3):
        z = base_z + height * (0.20 + 0.15 * idx)
        box(f"{prefix}_side_holo_window_scanline_{idx:02d}", (x, cy, z), (0.014, depth * (0.44 + 0.08 * idx), 0.014), mats["holo"], category)


def add_arch_frame_reinforcement(mats):
    add_arch_detail_front("front_lower_left", -1.22, -2.93, 2.65, 0.74, 2.55, mats)
    add_arch_detail_front("front_lower_center", 0.0, -2.96, 3.05, 0.92, 3.05, mats)
    add_arch_detail_front("front_lower_right", 1.22, -2.93, 2.65, 0.74, 2.55, mats)
    add_arch_detail_front("front_upper_left", -0.66, -2.65, 7.52, 0.62, 2.05, mats)
    add_arch_detail_front("front_upper_right", 0.66, -2.65, 7.52, 0.62, 2.05, mats)
    add_arch_detail_side("left_side_forward", -2.13, -1.45, 4.05, 0.86, 2.25, mats)
    add_arch_detail_side("left_side_rear", -2.13, 1.45, 4.05, 0.86, 2.25, mats)
    add_arch_detail_side("right_side_forward", 2.13, -1.45, 4.05, 0.86, 2.25, mats)
    add_arch_detail_side("right_side_rear", 2.13, 1.45, 4.05, 0.86, 2.25, mats)


def add_buttress_hardware(mats):
    category = "Flying buttress collars, braces, sockets, and railings"
    for side_name, sign in [("left", -1), ("right", 1)]:
        for idx, y in enumerate([-2.15, 0.0, 2.15]):
            anchor_x = sign * 5.1
            wall_x = sign * 2.05
            upper_z = 6.1 + idx * 0.74
            torus(f"{side_name}_buttress_anchor_collar_ring_{idx:02d}", (anchor_x, y, 0.92), 0.42, 0.028, mats["detail"], category, seg=18, minor_seg=4, scale=(1.18, 0.90, 1.0))
            torus(f"{side_name}_buttress_mid_data_collar_ring_{idx:02d}", (sign * 3.78, y, upper_z + 0.74), 0.28, 0.020, mats["emissive"], category, seg=16, minor_seg=4, scale=(1.20, 0.74, 1.0))
            torus(f"{side_name}_buttress_wall_socket_collar_ring_{idx:02d}", (wall_x, y, upper_z), 0.31, 0.024, mats["detail"], category, seg=18, minor_seg=4, scale=(1.12, 0.74, 1.0))
            cylinder_between(f"{side_name}_buttress_lower_tension_cable_{idx:02d}", (anchor_x, y - 0.23, 0.72), (wall_x, y - 0.23, upper_z - 0.24), 0.013, mats["emissive"], category, vertices=5)
            cylinder_between(f"{side_name}_buttress_upper_tension_cable_{idx:02d}", (anchor_x, y + 0.23, 0.96), (wall_x, y + 0.23, upper_z + 0.22), 0.013, mats["emissive"], category, vertices=5)
            cylinder_between(f"{side_name}_buttress_dark_crossbrace_a_{idx:02d}", (anchor_x, y - 0.18, 1.18), (sign * 3.62, y + 0.18, upper_z + 0.80), 0.020, mats["detail"], category, vertices=6)
            cylinder_between(f"{side_name}_buttress_dark_crossbrace_b_{idx:02d}", (anchor_x, y + 0.18, 1.18), (sign * 3.62, y - 0.18, upper_z + 0.80), 0.020, mats["detail"], category, vertices=6)
            platform_x = sign * 4.08
            rail_z = upper_z + 0.88
            box(f"{side_name}_observation_platform_outer_guardrail_{idx:02d}", (platform_x + sign * 0.52, y, rail_z), (0.028, 0.74, 0.18), mats["detail"], category)
            box(f"{side_name}_observation_platform_front_guardrail_{idx:02d}", (platform_x, y - 0.40, rail_z), (0.92, 0.025, 0.16), mats["detail"], category)
            box(f"{side_name}_observation_platform_rear_guardrail_{idx:02d}", (platform_x, y + 0.40, rail_z), (0.92, 0.025, 0.16), mats["detail"], category)


def add_spire_and_crown_polish(mats):
    category = "Spire beacon rings and data crown polish"
    for idx, z in enumerate([13.06, 13.62, 14.16, 15.42]):
        torus(f"central_spire_nested_teal_beacon_halo_{idx:02d}", (0.0, 0.0, z), 0.34 - idx * 0.035, 0.018, mats["emissive"], category, seg=22, minor_seg=4)
    for idx, angle in enumerate([0, 60, 120, 180, 240, 300]):
        a = math.radians(angle)
        x = math.cos(a) * 0.42
        y = math.sin(a) * 0.42
        cone(f"central_crown_dark_data_fin_{idx:02d}", (x * 0.55, y * 0.55, 13.72), 0.11, 0.012, 0.72, mats["detail"], category, vertices=6, rot=(math.radians(18), 0, a))
        cylinder_between(f"central_spire_teal_micro_lattice_rod_{idx:02d}", (x * 0.36, y * 0.36, 13.12), (x * 0.18, y * 0.18, 15.28), 0.014, mats["emissive"], category, vertices=5)
    torus("rear_orange_hard_socket_secondary_receiver_ring", (0.0, 2.24, 12.98), 0.58, 0.026, mats["energy"], category, seg=22, minor_seg=4, rot=(math.radians(90), 0, 0))
    for idx, x in enumerate([-0.26, 0.26]):
        cylinder_between(f"rear_orange_hard_socket_locking_pin_{idx:02d}", (x, 2.22, 12.72), (x * 0.55, 2.34, 13.22), 0.018, mats["energy"], category, vertices=5)


def add_entry_and_plaza_detail(mats):
    category = "Data waterfall entry and analytics plaza lattice"
    for side, sx in [("left", -1), ("right", 1)]:
        x = sx * 0.90
        box(f"entry_{side}_dark_cathedral_jamb_outer_frame", (x, -3.04, 1.40), (0.075, 0.060, 2.82), mats["detail"], category)
        box(f"entry_{side}_thin_teal_waterfall_side_channel", (sx * 0.56, -3.09, 1.58), (0.042, 0.026, 2.50), mats["emissive"], category)
        for idx in range(8):
            z = 0.42 + idx * 0.31
            box(f"entry_{side}_falling_data_packet_cluster_{idx:02d}", (sx * (0.55 + 0.09 * math.sin(idx)), -3.12, z), (0.13, 0.020, 0.052), mats["emissive"], category)

    box("front_entry_deep_shadow_threshold_lip", (0, -3.26, 0.28), (2.20, 0.20, 0.10), mats["detail"], category)
    for idx, y in enumerate([-4.85, -4.18, -3.54]):
        box(f"arrival_axis_transverse_teal_data_trace_{idx:02d}", (0, y, 0.225), (2.72 - idx * 0.38, 0.032, 0.026), mats["emissive"], category)
    for idx, x in enumerate([-1.88, -1.20, 1.20, 1.88]):
        box(f"arrival_axis_lengthwise_dark_cable_channel_{idx:02d}", (x, -4.22, 0.235), (0.030, 1.80, 0.026), mats["detail"], category)
    for idx, x in enumerate([-4.3, -3.2, 3.2, 4.3]):
        box(f"plaza_low_analytics_wayfinding_monolith_{idx:02d}", (x, -3.72, 0.64), (0.12, 0.18, 0.92), mats["detail"], category)
        box(f"plaza_low_analytics_wayfinding_teal_strip_{idx:02d}", (x, -3.83, 0.78), (0.065, 0.020, 0.58), mats["emissive"], category)


def add_roof_ridge_polish(mats):
    category = "Cathedral roof ridge ribs and dark-first silhouette polish"
    for idx, y in enumerate([-2.18, -1.45, -0.72, 0.0, 0.72, 1.45, 2.18]):
        cylinder_between(f"nave_roof_dark_transverse_ridge_rib_{idx:02d}", (-1.52, y, 12.36), (0.0, y, 13.58), 0.022, mats["detail"], category, vertices=6)
        cylinder_between(f"nave_roof_dark_transverse_ridge_rib_mirror_{idx:02d}", (1.52, y, 12.36), (0.0, y, 13.58), 0.022, mats["detail"], category, vertices=6)
    cylinder_between("nave_roof_teal_data_ridge_line", (0.0, -2.42, 13.62), (0.0, 2.42, 13.62), 0.018, mats["emissive"], category, vertices=6)
    for side, x in [("left", -2.82), ("right", 2.82)]:
        cylinder_between(f"{side}_aisle_roof_dark_outer_ridge_line", (x, -2.58, 7.48), (x, 2.58, 7.48), 0.020, mats["detail"], category, vertices=6)
        for idx, y in enumerate([-1.90, -0.95, 0.0, 0.95, 1.90]):
            cylinder_between(f"{side}_aisle_roof_short_gothic_rib_{idx:02d}", (x - (0.38 if side == "left" else -0.38), y, 6.90), (x, y, 7.50), 0.017, mats["detail"], category, vertices=6)


def add_dark_gothic_data_lattice(mats):
    category = "Dark gothic data lattice overlay"
    front_y = -3.015
    for idx, x in enumerate([-1.70, -1.28, -0.86, -0.42, 0.42, 0.86, 1.28, 1.70]):
        cylinder_between(f"front_upper_dark_gothic_vertical_lattice_rod_{idx:02d}", (x, front_y, 5.10), (x * 0.72, front_y, 11.72), 0.014, mats["detail"], category, vertices=5)
    for idx, z in enumerate([5.72, 6.58, 7.42, 8.28, 9.14, 10.02, 10.88]):
        width, depth = width_depth_at_z(z)
        cylinder_between(f"front_upper_dark_gothic_lattice_crossbar_{idx:02d}", (-width * 0.42, -depth * 0.5 - 0.065, z), (width * 0.42, -depth * 0.5 - 0.065, z + 0.08 * math.sin(idx)), 0.012, mats["detail"], category, vertices=5)
    for idx, (x0, x1, z0, z1) in enumerate(
        [
            (-1.66, -0.32, 5.42, 7.96),
            (1.66, 0.32, 5.42, 7.96),
            (-1.28, 0.00, 7.20, 10.04),
            (1.28, 0.00, 7.20, 10.04),
            (-0.92, -1.58, 8.80, 11.22),
            (0.92, 1.58, 8.80, 11.22),
        ]
    ):
        cylinder_between(f"front_upper_dark_gothic_diagonal_lattice_{idx:02d}", (x0, front_y - 0.01, z0), (x1, front_y - 0.01, z1), 0.012, mats["detail"], category, vertices=5)

    for side, x in [("left", -3.48), ("right", 3.48)]:
        for idx, y in enumerate([-2.15, -1.45, -0.75, 0.0, 0.75, 1.45, 2.15]):
            cylinder_between(f"{side}_side_dark_data_lattice_vertical_rod_{idx:02d}", (x, y, 3.85), (x, y * 0.74, 8.84), 0.012, mats["detail"], category, vertices=5)
        for idx, z in enumerate([4.52, 5.32, 6.16, 7.02, 7.86, 8.62]):
            cylinder_between(f"{side}_side_dark_data_lattice_crossbar_{idx:02d}", (x, -2.16, z), (x, 2.16, z + 0.06 * math.sin(idx)), 0.011, mats["detail"], category, vertices=5)
        for idx, (y0, y1, z0, z1) in enumerate(
            [
                (-2.10, -0.40, 4.10, 6.82),
                (2.10, 0.40, 4.10, 6.82),
                (-1.30, 1.30, 6.25, 8.58),
                (1.30, -1.30, 6.25, 8.58),
            ]
        ):
            cylinder_between(f"{side}_side_dark_data_lattice_diagonal_{idx:02d}", (x, y0, z0), (x, y1, z1), 0.011, mats["detail"], category, vertices=5)


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
        mesh = bpy.data.meshes.new(f"analytics_ext_{mat_name}_packed_mesh")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        packed_obj = bpy.data.objects.new(f"analytics_ext_{mat_name}_packed", mesh)
        bpy.context.collection.objects.link(packed_obj)
        packed_obj.data.materials.append(mats[mat_name])
        packed.append(packed_obj)

    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH" and obj not in packed]:
        bpy.data.objects.remove(obj, do_unlink=True)
    return packed


def export_analytics():
    remove_cameras_lights()
    for obj in list(bpy.data.objects):
        if obj.type == "EMPTY":
            bpy.data.objects.remove(obj, do_unlink=True)
    apply_mesh_world_transforms()
    normalize_material_slots()
    center_bottom_origin()
    pack_export_meshes_by_material()

    root = bpy.data.objects.new("analytics-ext", None)
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
        ("recovery", os.path.join(ROOT, "modules/09-recovery-sleep/exterior/approved/recovery-ext.glb"), (-43, -8, 0)),
        ("analytics", APPROVED_GLB, (-31, 14, 0)),
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
    path = render_shot("s42_cohesion_all11.png", (102, -154, 112), (0, -18, 9), 16)
    return {"screenshot": path, "imported": imported_labels}


def build_session_42():
    if not os.path.exists(S41_BLEND):
        raise FileNotFoundError(S41_BLEND)

    print("=== Session 42: AI Analytics exterior detail, polish, export ===")
    bpy.ops.wm.open_mainfile(filepath=S41_BLEND)
    setup_lighting_and_render()
    mats = normalize_material_slots()
    tune_analytics_materials(mats)

    before_tris = scene_triangles()
    before_meshes = sum(1 for obj in bpy.data.objects if obj.type == "MESH")

    add_facade_panel_depth(mats)
    add_living_wall_chart_density(mats)
    add_arch_frame_reinforcement(mats)
    add_buttress_hardware(mats)
    add_spire_and_crown_polish(mats)
    add_entry_and_plaza_detail(mats)
    add_roof_ridge_polish(mats)
    add_dark_gothic_data_lattice(mats)
    normalize_material_slots()

    after_detail_tris = scene_triangles()
    if after_detail_tris > 18000:
        raise RuntimeError(f"Session 42 detail exceeded exterior budget before export: {after_detail_tris} tris")
    if after_detail_tris < 12000:
        raise RuntimeError(f"Session 42 detail under-used exterior budget before export: {after_detail_tris} tris")

    bpy.ops.wm.save_as_mainfile(filepath=S42_BLEND)

    screenshots = [
        render_shot("s42_front_elevation.png", (0, -28, 9.4), (0, -0.2, 8.3), 38),
        render_shot("s42_three_quarter.png", (18, -25, 13.6), (0.0, 0.0, 8.5), 40),
        render_shot("s42_distance_view.png", (36, -43, 22.0), (0.0, 0.0, 8.4), 44),
        render_dark_first(),
    ]

    mat_tris = material_triangles()
    metrics_before_export = {
        "session": 42,
        "module": "10-ai-analytics",
        "blender_version": bpy.app.version_string,
        "source_blend": S41_BLEND,
        "blend": S42_BLEND,
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

    export_metrics = export_analytics()
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

    print("SESSION42_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_session_42()

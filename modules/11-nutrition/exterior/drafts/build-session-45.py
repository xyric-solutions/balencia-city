"""
Balencia City v3 - Module #11 Nutrition
Session 45: Exterior Major Forms

Organic Farm-Structure: a 12-floor stepped vertical farm with rounded terrace
edges, cascading green plant masses, amber grow-light bands, greenhouse volumes,
an open market base, roof ventilation, irrigation channels, and a hard-pipeline
receiver for Phase 5.
"""

import importlib.util
import json
import math
import os
import sys

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Desktop/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/11-nutrition")
DRAFTS = os.path.join(MODULE, "exterior/drafts")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
BLEND_FILE = os.path.join(DRAFTS, "nutrition-s45-major-forms.blend")
METRICS_FILE = os.path.join(DRAFTS, "session45-metrics.json")

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
    if obj.type == "MESH":
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


def tune_nutrition_materials(mats):
    set_principled(mats["base"], base_hex="#24221C")
    set_principled(mats["accent"], base_hex="#1F6F3A", emission_hex="#34A853", emission_strength=0.16)
    set_principled(mats["glass"], base_hex="#151714", emission_hex="#FBBF24", emission_strength=0.06, alpha=0.86)
    set_principled(mats["detail"], base_hex="#17150F")
    set_principled(mats["emissive"], base_hex="#221408", emission_hex="#D97706", emission_strength=0.14)
    set_principled(mats["energy"], base_hex="#271005", emission_hex="#FF5E00", emission_strength=0.14)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def fallback_lighting():
    world = bpy.context.scene.world or bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)
        bg.inputs["Strength"].default_value = 1.0

    sun = bpy.data.lights.new("Key_Light", "SUN")
    sun.color = (1.0, 0.894, 0.8)
    sun.energy = 0.8
    sun_obj = bpy.data.objects.new("Key_Light", sun)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

    rim = bpy.data.lights.new("Rim_Light", "SPOT")
    rim.color = (1.0, 0.369, 0.0)
    rim.energy = 200
    rim.spot_size = math.radians(45)
    rim.spot_blend = 0.9
    rim_obj = bpy.data.objects.new("Rim_Light", rim)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (10, 18, -14)
    direction = Vector((0, 0, 4)) - Vector(rim_obj.location)
    rim_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    fill = bpy.data.lights.new("Fill_Light", "AREA")
    fill.color = (0.102, 0.102, 0.251)
    fill.energy = 50
    fill.size = 20
    fill_obj = bpy.data.objects.new("Fill_Light", fill)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (5, 15, 10)


def setup_lighting():
    try:
        if hasattr(lighting, "clear_lighting"):
            lighting.clear_lighting()
        lighting.setup_viewport_lighting()
    except Exception as exc:
        print("Lighting rig fallback used: " + repr(exc))
        fallback_lighting()


def shade_smooth(obj):
    if obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def make_mesh(name, verts, faces, mat, smooth=False):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    if smooth:
        shade_smooth(obj)
    return obj


def box(name, loc, dims, mat, rot_z=0.0, bevel=0.0, bevel_segments=2):
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
        mod = obj.modifiers.new("organic_soft_edge_bevel", "BEVEL")
        mod.width = bevel
        mod.segments = bevel_segments
        mod.profile = 0.5
        bpy.ops.object.modifier_apply(modifier=mod.name)
        try:
            normal = obj.modifiers.new("weighted_organic_normals", "WEIGHTED_NORMAL")
            bpy.ops.object.modifier_apply(modifier=normal.name)
        except Exception:
            pass
        obj.select_set(False)
    return obj


def cylinder(name, loc, radius, depth, mat, vertices=16, rot=(0.0, 0.0, 0.0)):
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


def cone(name, loc, radius1, radius2, depth, mat, vertices=18, rot=(0.0, 0.0, 0.0)):
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


def torus(name, loc, major, minor, mat, seg=32, minor_seg=5, rot=(0.0, 0.0, 0.0)):
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


def rounded_rect_points(width, depth, radius, steps=6):
    w = width * 0.5
    d = depth * 0.5
    r = min(radius, w * 0.48, d * 0.48)
    centers = [
        (w - r, d - r, 0.0),
        (-w + r, d - r, math.pi * 0.5),
        (-w + r, -d + r, math.pi),
        (w - r, -d + r, math.pi * 1.5),
    ]
    points = []
    for cx, cy, start in centers:
        for idx in range(steps + 1):
            a = start + (math.pi * 0.5) * (idx / steps)
            points.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return points


def rounded_prism(name, width, depth, z0, z1, radius, mat, steps=5, center=(0.0, 0.0)):
    cx, cy = center
    pts = rounded_rect_points(width, depth, radius, steps)
    verts = [(cx + x, cy + y, z0) for x, y in pts] + [(cx + x, cy + y, z1) for x, y in pts]
    n = len(pts)
    faces = []
    for idx in range(n):
        faces.append((idx, (idx + 1) % n, n + (idx + 1) % n, n + idx))
    faces.append(tuple(reversed(range(n))))
    faces.append(tuple(range(n, n * 2)))
    return make_mesh(name, verts, faces, mat, smooth=True)


def greenhouse(name, loc, dims, mats, side="front"):
    box(name + "_amber_tinted_greenhouse_glass_mass", loc, dims, mats["glass"], bevel=0.035, bevel_segments=2)
    x, y, z = loc
    sx, sy, sz = dims
    if side in {"front", "rear"}:
        for level in [-0.25, 0.05, 0.35]:
            box(name + f"_hydroponic_internal_rack_{level:+.2f}", (x, y - sy * 0.54, z + sz * level), (sx * 0.78, 0.035, 0.035), mats["detail"])
        for offset in [-0.32, 0.0, 0.32]:
            box(name + f"_vertical_greenhouse_mullion_{offset:+.2f}", (x + sx * offset, y - sy * 0.55, z), (0.035, 0.035, sz * 0.78), mats["detail"])
    else:
        for level in [-0.25, 0.05, 0.35]:
            box(name + f"_hydroponic_side_rack_{level:+.2f}", (x - sx * 0.54, y, z + sz * level), (0.035, sy * 0.78, 0.035), mats["detail"])
        for offset in [-0.32, 0.0, 0.32]:
            box(name + f"_side_greenhouse_mullion_{offset:+.2f}", (x - sx * 0.55, y + sy * offset, z), (0.035, 0.035, sz * 0.78), mats["detail"])


def plant_curtain(name, x, y, z, width, height, mats, side="front"):
    if side in {"front", "rear"}:
        box(name, (x, y, z - height * 0.5), (width, 0.055, height), mats["accent"], bevel=0.025, bevel_segments=2)
    else:
        box(name, (x, y, z - height * 0.5), (0.055, width, height), mats["accent"], bevel=0.025, bevel_segments=2)


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
            eevee.bloom_intensity = 0.55
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.55


def render_shot(filename, camera_loc, target, lens=40):
    cam_data = bpy.data.cameras.new(filename.replace(".png", "_Camera"))
    cam = bpy.data.objects.new(filename.replace(".png", "_Camera"), cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    direction = Vector(target) - Vector(camera_loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.clip_start = 0.1
    cam.data.clip_end = 260
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
    if "grow_light" in name or "amber" in name:
        return "Amber grow-light bands"
    if "greenhouse" in name or "hydroponic" in name:
        return "Glass greenhouse volumes and racks"
    if "plant" in name or "vine" in name or "green" in name:
        return "Cascading plant massing"
    if "market" in name or "produce" in name or "stall" in name:
        return "Open market base"
    if "chimney" in name or "vent" in name:
        return "Roof kitchen ventilation"
    if "irrigation" in name or "water" in name:
        return "Water irrigation channels"
    if "pipeline" in name or "socket" in name or "receiver" in name:
        return "SIA hard-pipeline receiver"
    if "tier" in name or "farm_pyramid" in name:
        return "Twelve-floor rounded farm pyramid"
    return "Nutrition major forms"


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
    print("=== Session 45: Nutrition exterior major forms ===")
    clear_scene()
    setup_lighting()
    setup_render()
    mats = materials_mod.create_materials("#D97706", include_energy=True, include_holo=False)
    cleanup_slot_names()
    tune_nutrition_materials(mats)
    print(f"Material slots: {sorted(mats.keys())}")

    # Ground-level open market base.
    box("open_market_dark_plaza_slab", (0, 0, 0.06), (11.2, 8.2, 0.12), mats["base"], bevel=0.08, bevel_segments=3)
    box("open_market_recessed_warm_floor", (0, -0.35, 0.17), (7.8, 5.0, 0.08), mats["base"], bevel=0.06, bevel_segments=2)
    for idx, x in enumerate([-4.15, 4.15]):
        for jdx, y in enumerate([-2.75, 2.75]):
            cylinder(f"open_market_structural_column_{idx}_{jdx}", (x, y, 0.58), 0.16, 1.05, mats["detail"], vertices=14)
    box("open_market_canopy_supporting_first_farm_tier", (0, 0, 0.92), (9.35, 6.65, 0.22), mats["base"], bevel=0.12, bevel_segments=3)
    box("open_market_front_open_amber_threshold", (0, -3.47, 0.54), (4.9, 0.10, 0.20), mats["emissive"], bevel=0.035, bevel_segments=2)
    for idx, x in enumerate([-2.25, -0.75, 0.75, 2.25]):
        box(f"open_market_amber_lit_produce_display_stall_{idx:02d}", (x, -2.55, 0.40), (0.74, 0.56, 0.28), mats["accent"], bevel=0.05, bevel_segments=2)
        box(f"open_market_produce_stall_warm_light_strip_{idx:02d}", (x, -2.84, 0.59), (0.66, 0.035, 0.035), mats["emissive"])

    tier_data = []
    tiers = 12
    z_start = 0.98
    floor_step = 0.50
    floor_depth = 0.42
    for idx in range(tiers):
        t = idx / (tiers - 1)
        width = 8.85 - 5.05 * t
        depth = 6.15 - 3.25 * t
        z0 = z_start + idx * floor_step
        z1 = z0 + floor_depth
        tier_data.append({"idx": idx + 1, "width": width, "depth": depth, "z0": z0, "z1": z1})
        rounded_prism(
            f"twelve_floor_farm_pyramid_rounded_tier_{idx + 1:02d}",
            width,
            depth,
            z0,
            z1,
            radius=0.34 - 0.10 * t,
            mat=mats["base"],
            steps=5,
        )

        terrace_z = z1 + 0.015
        box(
            f"vertical_farm_detail_bed_front_tier_{idx + 1:02d}",
            (0, -depth * 0.5 - 0.02, terrace_z),
            (width * 0.84, 0.22, 0.045),
            mats["detail"],
            bevel=0.025,
            bevel_segments=1,
        )
        box(
            f"vertical_farm_detail_bed_left_tier_{idx + 1:02d}",
            (-width * 0.5 - 0.02, 0, terrace_z),
            (0.20, depth * 0.62, 0.045),
            mats["detail"],
            bevel=0.025,
            bevel_segments=1,
        )
        box(
            f"vertical_farm_detail_bed_right_tier_{idx + 1:02d}",
            (width * 0.5 + 0.02, 0, terrace_z),
            (0.20, depth * 0.62, 0.045),
            mats["detail"],
            bevel=0.025,
            bevel_segments=1,
        )

        box(
            f"amber_grow_light_front_band_tier_{idx + 1:02d}",
            (0, -depth * 0.5 - 0.16, z1 + 0.12),
            (width * 0.86, 0.045, 0.045),
            mats["emissive"],
        )
        box(
            f"amber_grow_light_rear_band_tier_{idx + 1:02d}",
            (0, depth * 0.5 + 0.16, z1 + 0.12),
            (width * 0.66, 0.045, 0.045),
            mats["emissive"],
        )
        box(
            f"amber_grow_light_left_band_tier_{idx + 1:02d}",
            (-width * 0.5 - 0.16, 0, z1 + 0.12),
            (0.045, depth * 0.62, 0.045),
            mats["emissive"],
        )
        box(
            f"amber_grow_light_right_band_tier_{idx + 1:02d}",
            (width * 0.5 + 0.16, 0, z1 + 0.12),
            (0.045, depth * 0.62, 0.045),
            mats["emissive"],
        )

        if idx >= 1:
            for cidx, x_frac in enumerate([-0.32, 0.0, 0.32]):
                curtain_height = 0.36 + 0.10 * ((idx + cidx) % 3)
                plant_curtain(
                    f"cascading_green_plant_curtain_front_tier_{idx + 1:02d}_{cidx:02d}",
                    width * x_frac,
                    -depth * 0.5 - 0.28,
                    z1,
                    width * 0.15,
                    curtain_height,
                    mats,
                    side="front",
                )
            if idx % 2 == 0:
                plant_curtain(
                    f"cascading_green_plant_curtain_left_tier_{idx + 1:02d}",
                    -width * 0.5 - 0.28,
                    -depth * 0.18,
                    z1,
                    depth * 0.20,
                    0.42,
                    mats,
                    side="side",
                )
                plant_curtain(
                    f"cascading_green_plant_curtain_right_tier_{idx + 1:02d}",
                    width * 0.5 + 0.28,
                    depth * 0.18,
                    z1,
                    depth * 0.20,
                    0.42,
                    mats,
                    side="side",
                )

        if idx in {2, 5, 8, 10}:
            box(
                f"water_irrigation_front_channel_tier_{idx + 1:02d}",
                (0, -depth * 0.5 - 0.235, z1 + 0.045),
                (width * 0.72, 0.035, 0.03),
                mats["detail"],
            )
        if idx in {3, 7, 11}:
            box(
                f"water_irrigation_side_channel_tier_{idx + 1:02d}",
                (width * 0.5 + 0.235, 0, z1 + 0.045),
                (0.035, depth * 0.52, 0.03),
                mats["detail"],
            )

    greenhouse("front_mid_greenhouse_section", (-2.25, -3.22, 3.18), (1.35, 0.28, 1.35), mats, side="front")
    greenhouse("right_lower_greenhouse_section", (4.16, -0.72, 2.02), (0.28, 1.45, 1.18), mats, side="side")
    greenhouse("left_upper_greenhouse_section", (-3.06, 0.78, 4.82), (0.28, 1.24, 1.18), mats, side="side")

    top = tier_data[-1]
    roof_z = top["z1"] + 0.10
    box("roof_service_dark_kitchen_terrace", (0, 0, roof_z), (2.55, 1.82, 0.16), mats["detail"], bevel=0.08, bevel_segments=2)
    cylinder("roof_kitchen_chimney_vertical_vent_stack", (0.74, 0.20, roof_z + 0.68), 0.18, 1.20, mats["detail"], vertices=18)
    cone("roof_kitchen_chimney_wide_vent_cap", (0.74, 0.20, roof_z + 1.35), 0.34, 0.22, 0.22, mats["detail"], vertices=18)
    cylinder("roof_kitchen_chimney_amber_warm_exhaust_core", (0.74, 0.20, roof_z + 1.48), 0.10, 0.16, mats["emissive"], vertices=12)

    receiver_z = top["z1"] - 0.28
    torus(
        "rear_roof_orange_sia_pipeline_receiver_hard_socket",
        (0.0, top["depth"] * 0.5 + 0.39, receiver_z),
        0.38,
        0.045,
        mats["energy"],
        seg=28,
        minor_seg=5,
        rot=(math.radians(90), 0, 0),
    )
    cylinder(
        "rear_roof_orange_pipeline_receiver_core",
        (0.0, top["depth"] * 0.5 + 0.52, receiver_z),
        0.16,
        0.30,
        mats["energy"],
        vertices=14,
        rot=(math.radians(90), 0, 0),
    )

    for idx, data in enumerate(tier_data[1::2]):
        z = data["z1"] + 0.07
        x = -data["width"] * 0.43
        y0 = -data["depth"] * 0.5 - 0.24
        y1 = data["depth"] * 0.5 + 0.12
        cylinder_between(
            f"water_irrigation_vertical_downspout_left_{idx:02d}",
            (x, y0, z),
            (x, y1, z - 0.10),
            0.018,
            mats["detail"],
            vertices=6,
        )

    cleanup_slot_names()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    screenshots = [
        render_shot("s45_front_elevation.png", (0, -24, 7.2), (0, -0.1, 4.2), 38),
        render_shot("s45_three_quarter.png", (17, -22, 10.2), (0.0, 0.0, 4.55), 40),
        render_shot("s45_distance_view.png", (31, -38, 17.0), (0.0, 0.0, 4.75), 45),
    ]

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)

    objects = object_metrics()
    metrics = {
        "session": 45,
        "module": "11-nutrition",
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

    print("SESSION45_METRICS=" + json.dumps(metrics, indent=2))
    return metrics


metrics = build_scene()

if os.environ.get("BALENCIA_QUIT_AFTER_RUN", "0") == "1":
    bpy.ops.wm.quit_blender()

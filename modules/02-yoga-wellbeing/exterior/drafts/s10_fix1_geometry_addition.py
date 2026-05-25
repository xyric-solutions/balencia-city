"""
Session 10 Fix 1 -- Geometry Addition Pass
Run: blender yoga-exterior-s10.blend -b -P s10_fix1_geometry_addition.py

Fixes Gate 3 (material compliance) and Gate 5 (technical budget) by adding
~5,000-7,000 tris of base and detail geometry. All additions are ADDITIVE --
no existing geometry is removed.

Target post-fix:
  - Total: 12,000-14,000 tris
  - base: 50-52%
  - detail: 12-14%
  - glass: ~10%
  - Others: diluted to closer to spec ranges
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector

# ============================================================
# CONFIGURATION
# ============================================================
SAVE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/exterior/drafts"
BLEND_OUT = os.path.join(SAVE_DIR, "yoga-exterior-s10-fix1.blend")
GLB_OUT = os.path.join(SAVE_DIR, "yoga-ext-draft-s10-fix1.glb")
MAX_TRIS = 18000

# ============================================================
# HELPERS
# ============================================================
def assign_mat(obj, slot_name):
    """Assign an existing material by slot name to an object."""
    mat = bpy.data.materials.get(slot_name)
    if mat:
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
    else:
        print(f"  WARNING: Material '{slot_name}' not found for {obj.name}")

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

def apply_smooth(obj):
    """Apply smooth shading to an object."""
    for poly in obj.data.polygons:
        poly.use_smooth = True

def count_tris_per_object():
    """Return list of (name, tri_count, material_name) for all mesh objects."""
    results = []
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj_eval = obj.evaluated_get(depsgraph)
            mesh_eval = obj_eval.to_mesh()
            tris = 0
            for poly in mesh_eval.polygons:
                tris += max(1, len(poly.vertices) - 2)
            obj_eval.to_mesh_clear()
            mat_name = obj.data.materials[0].name if obj.data.materials and obj.data.materials[0] else "none"
            results.append((obj.name, tris, mat_name))
    return results

def count_total_tris():
    return sum(t for _, t, _ in count_tris_per_object())

def print_tri_report(label=""):
    report = count_tris_per_object()
    total = sum(t for _, t, _ in report)
    print(f"\n=== TRI REPORT {label} ===")
    for name, tris, mat in sorted(report, key=lambda x: -x[1]):
        print(f"  {name}: {tris} [{mat}]")
    print(f"  TOTAL: {total} / {MAX_TRIS} ({total/MAX_TRIS*100:.1f}%)")

    # Material distribution
    slot_tris = {"base": 0, "accent": 0, "glass": 0, "detail": 0,
                 "emissive": 0, "energy": 0, "holo": 0}
    for _, tris, mat in report:
        if mat in slot_tris:
            slot_tris[mat] += tris
    print("\n  Material Distribution:")
    spec = {"base": "50-55%", "accent": "10-15%", "glass": "10-18%",
            "detail": "12-18%", "emissive": "3-8%", "energy": "0-5%", "holo": "0-5%"}
    for slot in ["base", "accent", "glass", "detail", "emissive", "energy", "holo"]:
        t = slot_tris[slot]
        pct = t / total * 100 if total > 0 else 0
        print(f"    {slot}: {t} tris ({pct:.1f}%) [spec: {spec[slot]}]")
    return total

# ============================================================
# STEP 0: VERIFY SCENE STATE
# ============================================================
print("=" * 60)
print("SESSION 10 FIX 1: Geometry Addition Pass")
print("=" * 60)

mesh_count = sum(1 for obj in bpy.data.objects if obj.type == 'MESH')
initial_tris = count_total_tris()
print(f"\nScene verification: {mesh_count} mesh objects, {initial_tris} tris")

# Quick sanity check
if initial_tris < 5000 or initial_tris > 10000:
    print(f"  WARNING: Expected ~6,954 tris, got {initial_tris}. Proceeding anyway.")
else:
    print(f"  Scene state matches expectations (~6,954 tris).")

print_tri_report("INITIAL STATE")

# ============================================================
# BASE ADDITION 1: Platform Underside Structural Ribbing
# Add 8 radial ribs on the underside of main_platform
# Target: ~400-500 tris assigned to base
# ============================================================
print("\n--- BASE 1: Platform Underside Structural Ribbing ---")

platform = bpy.data.objects.get("main_platform")
if platform:
    # The platform is an elliptical disc at Z=0.8, radius ~5.0 x 3.5 (Y scaled 0.7)
    # Platform depth is 0.35, so bottom is at Z = 0.8 - 0.175 = 0.625
    # Ribs go from near center to near edge, on the underside
    platform_z_bottom = 0.625
    rib_count = 8

    for i in range(rib_count):
        angle = i * (2 * math.pi / rib_count)
        inner_r = 0.8
        outer_r = 4.2

        # Calculate elliptical outer radius
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        # Ellipse: x^2/5^2 + y^2/3.5^2 = 1
        # Parametric: actual outer radius varies with angle
        eff_outer = outer_r * (1.0 / math.sqrt((cos_a/5.0)**2 + (sin_a/3.5)**2)) * 0.85
        eff_outer = min(eff_outer, 4.5)

        # Start and end points
        sx = cos_a * inner_r
        sy = sin_a * inner_r
        ex = cos_a * eff_outer
        ey = sin_a * eff_outer

        dx = ex - sx
        dy = ey - sy
        length = math.sqrt(dx*dx + dy*dy)
        mid_x = (sx + ex) / 2
        mid_y = (sy + ey) / 2
        rot_z = math.atan2(dy, dx)

        # Create rib as a flattened box (wide and thin)
        # Using bmesh for a proper rib cross-section
        verts = []
        faces = []
        rib_width = 0.08
        rib_depth = 0.06  # how far it hangs below platform bottom
        segments = 6  # along length

        for j in range(segments + 1):
            t = j / segments
            x = t * length
            # Slight downward curve for organic feel
            z_sag = -rib_depth * math.sin(t * math.pi)

            # 4 vertices per cross-section (rectangular profile)
            verts.append(Vector((x, -rib_width/2, 0)))
            verts.append(Vector((x,  rib_width/2, 0)))
            verts.append(Vector((x,  rib_width/2, z_sag)))
            verts.append(Vector((x, -rib_width/2, z_sag)))

        # Create faces connecting cross-sections
        for j in range(segments):
            base = j * 4
            for k in range(4):
                k_next = (k + 1) % 4
                faces.append((base + k, base + k_next, base + 4 + k_next, base + 4 + k))
        # Cap ends
        faces.append((0, 1, 2, 3))
        faces.append((segments*4, segments*4+3, segments*4+2, segments*4+1))

        rib_name = f"platform_rib_{i+1:02d}"
        mesh = bpy.data.meshes.new(rib_name)
        mesh.from_pydata([v[:] for v in verts], [], faces)
        mesh.update()
        rib_obj = bpy.data.objects.new(rib_name, mesh)
        bpy.context.collection.objects.link(rib_obj)
        rib_obj.location = (sx, sy, platform_z_bottom)
        rib_obj.rotation_euler = (0, 0, rot_z)
        bpy.context.view_layer.objects.active = rib_obj
        rib_obj.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        rib_obj.select_set(False)
        apply_smooth(rib_obj)
        assign_mat(rib_obj, "base")
        deselect_all()

    print(f"  Created {rib_count} platform ribs")
else:
    print("  WARNING: main_platform not found!")

# ============================================================
# BASE ADDITION 2: Dome Base Skirt Geometry
# Low collar/threshold rings where each dome meets the platform
# Target: ~600-700 tris assigned to base
# ============================================================
print("\n--- BASE 2: Dome Base Skirt Geometry ---")

dome_configs = [
    {"name": "dome_large",  "radius": 1.8,  "pos": (-1.2, -0.3, 0.97), "segs": 24},
    {"name": "dome_medium", "radius": 1.2,  "pos": (2.0, 0.5, 0.97),   "segs": 20},
    {"name": "dome_small",  "radius": 0.8,  "pos": (0.5, 1.8, 0.97),   "segs": 16},
]

for dc in dome_configs:
    # Create a short cylinder (annular ring) around each dome base
    # This is a visible threshold/step ring
    inner_r = dc["radius"] + 0.08
    outer_r = dc["radius"] + 0.35
    height = 0.06
    segs = dc["segs"]

    # Build annular ring mesh (ring of quads)
    verts = []
    faces = []

    for i in range(segs):
        angle = i * (2 * math.pi / segs)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # Bottom inner, bottom outer, top outer, top inner
        verts.append(Vector((cos_a * inner_r, sin_a * inner_r, 0)))
        verts.append(Vector((cos_a * outer_r, sin_a * outer_r, 0)))
        verts.append(Vector((cos_a * outer_r, sin_a * outer_r, height)))
        verts.append(Vector((cos_a * inner_r, sin_a * inner_r, height)))

    for i in range(segs):
        base = i * 4
        next_base = ((i + 1) % segs) * 4
        # Outer face
        faces.append((base + 1, next_base + 1, next_base + 2, base + 2))
        # Inner face
        faces.append((base + 0, base + 3, next_base + 3, next_base + 0))
        # Top face
        faces.append((base + 2, next_base + 2, next_base + 3, base + 3))
        # Bottom face
        faces.append((base + 0, next_base + 0, next_base + 1, base + 1))

    skirt_name = dc["name"].replace("dome_", "dome_skirt_")
    mesh = bpy.data.meshes.new(skirt_name)
    mesh.from_pydata([v[:] for v in verts], [], faces)
    mesh.update()
    skirt_obj = bpy.data.objects.new(skirt_name, mesh)
    bpy.context.collection.objects.link(skirt_obj)
    skirt_obj.location = dc["pos"]
    bpy.context.view_layer.objects.active = skirt_obj
    skirt_obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    skirt_obj.select_set(False)
    apply_smooth(skirt_obj)
    assign_mat(skirt_obj, "base")
    deselect_all()

print(f"  Created 3 dome base skirts")

# ============================================================
# BASE ADDITION 3: Platform Edge Thickening
# A visible thickness lip/ring around the platform perimeter
# Target: ~500-600 tris assigned to base
# ============================================================
print("\n--- BASE 3: Platform Edge Thickening ---")

# The platform is elliptical: radius 5.0 in X, 3.5 in Y (0.7 scale)
# Create a ring of geometry around the perimeter that gives it visible depth
# This is an outer lip/fascia band
edge_segs = 32
lip_width = 0.15
lip_depth = 0.12
platform_top_z = 0.8 + 0.175  # 0.975
platform_bot_z = 0.8 - 0.175  # 0.625

verts = []
faces = []

for i in range(edge_segs):
    angle = i * (2 * math.pi / edge_segs)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    # Elliptical radii
    rx = 5.0
    ry = 3.5
    r = (rx * ry) / math.sqrt((ry * cos_a)**2 + (rx * sin_a)**2)
    r_inner = r - 0.05
    r_outer = r + lip_width

    # 6 vertices per segment for a beveled lip profile
    # Inner-top, outer-top, outer-mid, outer-bottom, inner-bottom, inner-mid
    verts.append(Vector((cos_a * r_inner, sin_a * r_inner, platform_top_z - 0.02)))
    verts.append(Vector((cos_a * r_outer, sin_a * r_outer, platform_top_z - 0.02)))
    verts.append(Vector((cos_a * (r_outer + 0.03), sin_a * (r_outer + 0.03), platform_top_z - 0.06)))
    verts.append(Vector((cos_a * (r_outer + 0.03), sin_a * (r_outer + 0.03), platform_bot_z + 0.04)))
    verts.append(Vector((cos_a * r_inner, sin_a * r_inner, platform_bot_z + 0.04)))

for i in range(edge_segs):
    base = i * 5
    next_base = ((i + 1) % edge_segs) * 5

    # Top face
    faces.append((base + 0, base + 1, next_base + 1, next_base + 0))
    # Outer top bevel
    faces.append((base + 1, base + 2, next_base + 2, next_base + 1))
    # Outer vertical
    faces.append((base + 2, base + 3, next_base + 3, next_base + 2))
    # Bottom face
    faces.append((base + 3, base + 4, next_base + 4, next_base + 3))
    # Inner vertical
    faces.append((base + 4, base + 0, next_base + 0, next_base + 4))

lip_mesh = bpy.data.meshes.new("platform_lip")
lip_mesh.from_pydata([v[:] for v in verts], [], faces)
lip_mesh.update()
lip_obj = bpy.data.objects.new("platform_lip", lip_mesh)
bpy.context.collection.objects.link(lip_obj)
bpy.context.view_layer.objects.active = lip_obj
lip_obj.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
lip_obj.select_set(False)
apply_smooth(lip_obj)
assign_mat(lip_obj, "base")
deselect_all()
print("  Created platform edge lip")

# ============================================================
# BASE ADDITION 4: Garden Platform Surface Enrichment
# Subdivide garden platforms for more organic curvature
# Target: +480-780 tris to base
# ============================================================
print("\n--- BASE 4: Garden Platform Surface Enrichment ---")

garden_names = ["garden_platform_01", "garden_platform_02", "garden_platform_03"]
for gname in garden_names:
    gp = bpy.data.objects.get(gname)
    if gp:
        bpy.context.view_layer.objects.active = gp
        gp.select_set(True)
        mod = gp.modifiers.new(name="Subdivision", type='SUBSURF')
        mod.levels = 1
        mod.render_levels = 1
        bpy.ops.object.modifier_apply(modifier="Subdivision")
        gp.select_set(False)
        deselect_all()
        print(f"  Subdivided {gname}")
    else:
        print(f"  WARNING: {gname} not found!")

# ============================================================
# BASE ADDITION 5: Structural Floor Panels Between Domes
# Flat structural plates visible from walkway level
# Target: ~600-800 tris assigned to base
# ============================================================
print("\n--- BASE 5: Structural Floor Panels ---")

# Create several floor panel segments on the platform surface, between the domes
# These are slightly raised from the platform surface, suggesting structural flooring
panel_configs = [
    {"name": "floor_panel_01", "pos": (0.0, 0.0, 0.98), "size": (1.2, 0.8), "segs": (4, 3)},
    {"name": "floor_panel_02", "pos": (-2.5, 0.5, 0.98), "size": (1.5, 1.0), "segs": (5, 3)},
    {"name": "floor_panel_03", "pos": (0.8, -1.5, 0.98), "size": (1.0, 1.2), "segs": (3, 4)},
    {"name": "floor_panel_04", "pos": (-0.8, 1.5, 0.98), "size": (1.0, 0.9), "segs": (3, 3)},
    {"name": "floor_panel_05", "pos": (2.5, -0.8, 0.98), "size": (1.0, 1.0), "segs": (3, 3)},
]

for pc in panel_configs:
    sx, sy = pc["size"]
    seg_x, seg_y = pc["segs"]
    verts = []
    faces = []

    for iy in range(seg_y + 1):
        for ix in range(seg_x + 1):
            x = (ix / seg_x - 0.5) * sx
            y = (iy / seg_y - 0.5) * sy
            # Slight dome shape for organic feel
            dist = math.sqrt((x/(sx/2))**2 + (y/(sy/2))**2)
            z = 0.015 * max(0, 1.0 - dist)
            verts.append(Vector((x, y, z)))

    for iy in range(seg_y):
        for ix in range(seg_x):
            v0 = iy * (seg_x + 1) + ix
            v1 = v0 + 1
            v2 = v1 + (seg_x + 1)
            v3 = v0 + (seg_x + 1)
            faces.append((v0, v1, v2, v3))

    panel_mesh = bpy.data.meshes.new(pc["name"])
    panel_mesh.from_pydata([v[:] for v in verts], [], faces)
    panel_mesh.update()
    panel_obj = bpy.data.objects.new(pc["name"], panel_mesh)
    bpy.context.collection.objects.link(panel_obj)
    panel_obj.location = pc["pos"]
    bpy.context.view_layer.objects.active = panel_obj
    panel_obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    panel_obj.select_set(False)
    apply_smooth(panel_obj)
    assign_mat(panel_obj, "base")
    deselect_all()

print(f"  Created {len(panel_configs)} floor panels")

# ============================================================
# BASE ADDITION 6: Platform Underside Secondary Layer
# A second disc below the main platform to give visible depth
# Target: ~500-600 tris assigned to base
# ============================================================
print("\n--- BASE 6: Platform Underside Layer ---")

bpy.ops.mesh.primitive_cylinder_add(
    radius=4.5, depth=0.08, vertices=28,
    location=(0, 0, 0.6)
)
underside = bpy.context.active_object
underside.name = "platform_underside"
underside.scale = (1.0, 0.7, 1.0)
bpy.context.view_layer.objects.active = underside
underside.select_set(True)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
# Subdivide once for density
mod = underside.modifiers.new(name="Subdivision", type='SUBSURF')
mod.levels = 1
mod.render_levels = 1
bpy.ops.object.modifier_apply(modifier="Subdivision")
underside.select_set(False)
apply_smooth(underside)
assign_mat(underside, "base")
deselect_all()
print("  Created platform underside layer")

# ============================================================
# DETAIL ADDITION 1: Enhanced Walkway Deck Tessellation
# Existing walkways have ~10-12 tris. Create overlay panels with more detail.
# Target: +150-200 tris assigned to detail
# ============================================================
print("\n--- DETAIL 1: Walkway Deck Enhancement ---")

# Add deck plank detail strips on each walkway surface
walkway_deck_configs = [
    {"name": "walkway_deck_detail_01", "start": (0.6, -0.3, 0.985), "end": (0.8, 0.5, 0.985),
     "width": 0.16, "planks": 8},
    {"name": "walkway_deck_detail_02", "start": (1.5, 1.2, 0.985), "end": (0.8, 1.3, 0.985),
     "width": 0.13, "planks": 6},
    {"name": "walkway_deck_detail_03", "start": (-3.5, -1.0, 0.815), "end": (-3.2, -1.0, 0.515),
     "width": 0.13, "planks": 6},
]

for wdc in walkway_deck_configs:
    sx, sy, sz = wdc["start"]
    ex, ey, ez = wdc["end"]
    dx = ex - sx
    dy = ey - sy
    dz = ez - sz
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    angle_z = math.atan2(dy, dx)
    angle_y = math.atan2(dz, math.sqrt(dx*dx + dy*dy))
    half_w = wdc["width"] / 2
    planks = wdc["planks"]

    verts = []
    faces = []
    plank_gap = 0.01

    for p in range(planks):
        t0 = p / planks
        t1 = (p + 0.85) / planks  # 85% plank, 15% gap
        x0 = t0 * length
        x1 = t1 * length
        # Slight arc
        z0 = 0.003 * math.sin(t0 * math.pi)
        z1 = 0.003 * math.sin((t0 + t1)/2 * math.pi)

        base_idx = len(verts)
        verts.append(Vector((x0, -half_w, z0)))
        verts.append(Vector((x1, -half_w, z1)))
        verts.append(Vector((x1,  half_w, z1)))
        verts.append(Vector((x0,  half_w, z0)))
        faces.append((base_idx, base_idx+1, base_idx+2, base_idx+3))

    mesh = bpy.data.meshes.new(wdc["name"])
    mesh.from_pydata([v[:] for v in verts], [], faces)
    mesh.update()
    obj = bpy.data.objects.new(wdc["name"], mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = (sx, sy, sz)
    obj.rotation_euler = (angle_y, 0, angle_z)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    apply_smooth(obj)
    assign_mat(obj, "detail")
    deselect_all()

print(f"  Created {len(walkway_deck_configs)} walkway deck detail overlays")

# ============================================================
# DETAIL ADDITION 2: Pillar Base Footings at Water Level
# Broad flat footings where each pillar meets the water surface
# Target: ~250-300 tris assigned to detail
# ============================================================
print("\n--- DETAIL 2: Pillar Base Footings ---")

pillar_positions = [
    (-2.5, -1.5),
    (2.5, -1.5),
    (-3.0, 1.0),
    (3.0, 1.0),
    (0.0, 2.0),
]

for i, (px, py) in enumerate(pillar_positions):
    # Create a wide, flat disc at water level as a footing plate
    footing_segs = 12
    footing_r = 0.35
    footing_h = 0.03

    bpy.ops.mesh.primitive_cylinder_add(
        radius=footing_r, depth=footing_h, vertices=footing_segs,
        location=(px, py, -0.02)  # Just at/below water surface
    )
    footing = bpy.context.active_object
    footing.name = f"pillar_footing_{i+1:02d}"
    bpy.context.view_layer.objects.active = footing
    footing.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    footing.select_set(False)
    apply_smooth(footing)
    assign_mat(footing, "detail")
    deselect_all()

print(f"  Created {len(pillar_positions)} pillar footings")

# ============================================================
# DETAIL ADDITION 3: Enhanced Dome Rib Tessellation
# Existing ribs are 12 tris each. Add parallel companion ribs
# and cross-bracing for richer dome surface detail
# Target: ~400-500 tris assigned to detail
# ============================================================
print("\n--- DETAIL 3: Dome Rib Enhancement ---")

dome_rib_enhance = [
    {"dome": "dome_large",  "radius": 1.8, "pos": (-1.2, -0.3, 0.97), "count": 6},
    {"dome": "dome_medium", "radius": 1.2, "pos": (2.0, 0.5, 0.97),   "count": 4},
    {"dome": "dome_small",  "radius": 0.8, "pos": (0.5, 1.8, 0.97),   "count": 3},
]

for dc in dome_rib_enhance:
    r = dc["radius"] + 0.04  # Slightly outside existing ribs
    pos = dc["pos"]

    # Add horizontal ring ribs at 1/3 and 2/3 height of each dome
    for ring_idx, height_frac in enumerate([0.33, 0.66]):
        ring_z = r * math.sin(height_frac * math.pi / 2)
        ring_r = r * math.cos(height_frac * math.pi / 2)

        if ring_r < 0.1:
            continue

        ring_segs = max(8, dc["count"] * 2)
        rib_thickness = 0.012

        bpy.ops.mesh.primitive_torus_add(
            major_radius=ring_r, minor_radius=rib_thickness,
            major_segments=ring_segs, minor_segments=4,
            location=(pos[0], pos[1], pos[2] + ring_z)
        )
        ring_rib = bpy.context.active_object
        ring_rib.name = f"rib_ring_{dc['dome']}_{ring_idx+1:02d}"
        bpy.context.view_layer.objects.active = ring_rib
        ring_rib.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        ring_rib.select_set(False)
        apply_smooth(ring_rib)
        assign_mat(ring_rib, "detail")
        deselect_all()

print("  Created dome ring ribs (6 horizontal rings)")

# ============================================================
# DETAIL ADDITION 4: Decorative Trim Along Platform Edges
# Thin trim strips running along the main platform and garden edges
# Target: ~400-600 tris assigned to detail
# ============================================================
print("\n--- DETAIL 4: Decorative Platform Trim ---")

# Main platform trim - a detail-material ring slightly inset from the edge
bpy.ops.mesh.primitive_torus_add(
    major_radius=4.65, minor_radius=0.025,
    major_segments=32, minor_segments=4,
    location=(0, 0, 0.975)
)
trim_main = bpy.context.active_object
trim_main.name = "trim_platform_main"
trim_main.scale = (1.0, 0.7, 0.6)
bpy.context.view_layer.objects.active = trim_main
trim_main.select_set(True)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
trim_main.select_set(False)
apply_smooth(trim_main)
assign_mat(trim_main, "detail")
deselect_all()

# Inner trim ring
bpy.ops.mesh.primitive_torus_add(
    major_radius=3.8, minor_radius=0.02,
    major_segments=28, minor_segments=4,
    location=(0, 0, 0.978)
)
trim_inner = bpy.context.active_object
trim_inner.name = "trim_platform_inner"
trim_inner.scale = (1.0, 0.7, 0.5)
bpy.context.view_layer.objects.active = trim_inner
trim_inner.select_set(True)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
trim_inner.select_set(False)
apply_smooth(trim_inner)
assign_mat(trim_inner, "detail")
deselect_all()

# Garden platform trims
garden_trim_configs = [
    {"name": "trim_garden_01", "radius": 1.15, "pos": (-4.0, -1.0, 0.575)},
    {"name": "trim_garden_02", "radius": 0.85, "pos": (3.8, -1.5, 0.66)},
    {"name": "trim_garden_03", "radius": 0.65, "pos": (-3.5, 2.0, 0.75)},
]

for gtc in garden_trim_configs:
    bpy.ops.mesh.primitive_torus_add(
        major_radius=gtc["radius"], minor_radius=0.018,
        major_segments=16, minor_segments=4,
        location=gtc["pos"]
    )
    trim_g = bpy.context.active_object
    trim_g.name = gtc["name"]
    bpy.context.view_layer.objects.active = trim_g
    trim_g.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    trim_g.select_set(False)
    apply_smooth(trim_g)
    assign_mat(trim_g, "detail")
    deselect_all()

print("  Created 5 decorative trim elements")

# ============================================================
# DETAIL ADDITION 5: Railing Enrichment on Terraces
# Add vertical balusters/panel subdivisions to existing railings
# Target: ~180-240 tris assigned to detail
# ============================================================
print("\n--- DETAIL 5: Terrace Railing Balusters ---")

# Add vertical baluster posts along each terrace railing
garden_railing_configs = [
    {"name_prefix": "baluster_terrace_01", "radius": 1.25, "pos": (-4.0, -1.0, 0.58), "arc": 0.65, "count": 8},
    {"name_prefix": "baluster_terrace_02", "radius": 0.95, "pos": (3.8, -1.5, 0.68), "arc": 0.55, "count": 6},
    {"name_prefix": "baluster_terrace_03", "radius": 0.75, "pos": (-3.5, 2.0, 0.78), "arc": 0.50, "count": 5},
]

for grc in garden_railing_configs:
    r = grc["radius"]
    pos = grc["pos"]
    arc_span = grc["arc"]
    start_angle = -arc_span * math.pi
    end_angle = arc_span * math.pi

    for b in range(grc["count"]):
        t = b / (grc["count"] - 1) if grc["count"] > 1 else 0.5
        angle = start_angle + t * (end_angle - start_angle)
        bx = pos[0] + r * math.cos(angle)
        by = pos[1] + r * math.sin(angle)
        bz = pos[2]

        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.008, depth=0.12, vertices=4,
            location=(bx, by, bz)
        )
        bal = bpy.context.active_object
        bal.name = f"{grc['name_prefix']}_{b+1:02d}"
        bpy.context.view_layer.objects.active = bal
        bal.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bal.select_set(False)
        assign_mat(bal, "detail")
        deselect_all()

print("  Created terrace balusters (19 posts)")

# ============================================================
# DETAIL ADDITION 6: Walkway Connection Brackets
# Small structural brackets where walkways meet the platforms
# Target: ~180 tris assigned to detail
# ============================================================
print("\n--- DETAIL 6: Walkway Connection Brackets ---")

bracket_configs = [
    # Walkway 01 endpoints
    {"name": "bracket_w01_start", "pos": (0.6, -0.3, 0.97), "angle": math.atan2(0.8, 0.2)},
    {"name": "bracket_w01_end",   "pos": (0.8, 0.5, 0.97),  "angle": math.atan2(0.8, 0.2) + math.pi},
    # Walkway 02 endpoints
    {"name": "bracket_w02_start", "pos": (1.5, 1.2, 0.97), "angle": math.atan2(0.1, -0.7)},
    {"name": "bracket_w02_end",   "pos": (0.8, 1.3, 0.97), "angle": math.atan2(0.1, -0.7) + math.pi},
    # Walkway 03 endpoints
    {"name": "bracket_w03_start", "pos": (-3.5, -1.0, 0.8), "angle": math.atan2(0, 0.3)},
    {"name": "bracket_w03_end",   "pos": (-3.2, -1.0, 0.5), "angle": math.atan2(0, 0.3) + math.pi},
]

for bc in bracket_configs:
    # L-shaped bracket: horizontal plate + vertical brace
    verts = [
        Vector((0, -0.06, 0)),
        Vector((0.12, -0.06, 0)),
        Vector((0.12, 0.06, 0)),
        Vector((0, 0.06, 0)),
        Vector((0, -0.06, -0.08)),
        Vector((0.04, -0.06, -0.08)),
        Vector((0.04, 0.06, -0.08)),
        Vector((0, 0.06, -0.08)),
    ]
    faces = [
        (0, 1, 2, 3),  # top
        (4, 7, 6, 5),  # bottom of brace
        (0, 4, 5, 1),  # front
        (2, 6, 7, 3),  # back
        (0, 3, 7, 4),  # inner
        (1, 5, 6, 2),  # outer
    ]
    bracket_mesh = bpy.data.meshes.new(bc["name"])
    bracket_mesh.from_pydata([v[:] for v in verts], [], faces)
    bracket_mesh.update()
    bracket_obj = bpy.data.objects.new(bc["name"], bracket_mesh)
    bpy.context.collection.objects.link(bracket_obj)
    bracket_obj.location = bc["pos"]
    bracket_obj.rotation_euler = (0, 0, bc["angle"])
    bpy.context.view_layer.objects.active = bracket_obj
    bracket_obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bracket_obj.select_set(False)
    assign_mat(bracket_obj, "detail")
    deselect_all()

print(f"  Created {len(bracket_configs)} walkway brackets")

# ============================================================
# GLASS ADDITION: Dome Panel Subdivisions
# Add glass panel frames/mullion lines on dome surfaces
# Target: ~200-400 tris assigned to glass
# ============================================================
print("\n--- GLASS: Dome Panel Subdivisions ---")

# Add additional glass panels (small window inserts) around the platform
# These suggest enclosed spaces beneath the domes
glass_panel_configs = [
    {"name": "glass_panel_01", "pos": (-2.5, -1.8, 0.97), "size": (0.4, 0.3)},
    {"name": "glass_panel_02", "pos": (1.5, -1.5, 0.97),  "size": (0.35, 0.25)},
    {"name": "glass_panel_03", "pos": (-0.5, 2.2, 0.97),  "size": (0.3, 0.3)},
    {"name": "glass_panel_04", "pos": (3.0, 1.5, 0.97),   "size": (0.35, 0.28)},
]

for gpc in glass_panel_configs:
    sx, sy = gpc["size"]
    # Subdivided panel with 3x3 grid for visual richness
    verts = []
    faces = []
    divs = 3

    for iy in range(divs + 1):
        for ix in range(divs + 1):
            x = (ix / divs - 0.5) * sx
            y = (iy / divs - 0.5) * sy
            # Slight curvature
            z = 0.01 * (1 - (2*ix/divs - 1)**2) * (1 - (2*iy/divs - 1)**2)
            verts.append(Vector((x, y, z)))

    for iy in range(divs):
        for ix in range(divs):
            v0 = iy * (divs + 1) + ix
            v1 = v0 + 1
            v2 = v1 + (divs + 1)
            v3 = v0 + (divs + 1)
            faces.append((v0, v1, v2, v3))

    panel_mesh = bpy.data.meshes.new(gpc["name"])
    panel_mesh.from_pydata([v[:] for v in verts], [], faces)
    panel_mesh.update()
    panel_obj = bpy.data.objects.new(gpc["name"], panel_mesh)
    bpy.context.collection.objects.link(panel_obj)
    panel_obj.location = gpc["pos"]
    bpy.context.view_layer.objects.active = panel_obj
    panel_obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    panel_obj.select_set(False)
    apply_smooth(panel_obj)
    assign_mat(panel_obj, "glass")
    deselect_all()

# Also add glass lens caps on dome apexes (small convex panels)
for dc in dome_configs:
    cap_r = dc["radius"] * 0.15
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=cap_r, segments=8, ring_count=4,
        location=(dc["pos"][0], dc["pos"][1], dc["pos"][2] + dc["radius"] - cap_r * 0.3)
    )
    cap = bpy.context.active_object
    cap.name = f"glass_cap_{dc['name']}"

    # Remove bottom half
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(cap.data)
    bm.verts.ensure_lookup_table()
    verts_to_del = [v for v in bm.verts if v.co.z < -0.01]
    if verts_to_del:
        bmesh.ops.delete(bm, geom=verts_to_del, context='VERTS')
    bmesh.update_edit_mesh(cap.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.context.view_layer.objects.active = cap
    cap.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    cap.select_set(False)
    apply_smooth(cap)
    assign_mat(cap, "glass")
    deselect_all()

print("  Created 4 glass panels + 3 dome apex caps")

# ============================================================
# CHECKPOINT: Verify metrics
# ============================================================
print("\n" + "=" * 60)
print("CHECKPOINT: Post-Addition Metrics")
print("=" * 60)

checkpoint_total = print_tri_report("POST-ADDITION")

# ============================================================
# POLISH: Apply all transforms
# ============================================================
print("\n--- Applying all transforms ---")
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
if any(obj.select_get() for obj in bpy.data.objects):
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')
print("  All transforms applied")

# ============================================================
# POLISH: Verify no generic names
# ============================================================
bad_names = [obj.name for obj in bpy.data.objects if obj.type == 'MESH'
             and any(obj.name.startswith(p) for p in
                     ["Cube", "Cylinder", "Sphere", "Cone", "Torus", "Plane"])]
if bad_names:
    print(f"  WARNING: Generic object names found: {bad_names}")
else:
    print("  All objects named descriptively")

# ============================================================
# EXPORT GLB
# ============================================================
print("\n" + "=" * 60)
print("EXPORT GLB")
print("=" * 60)

# Remove cameras and lights before export
to_remove = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in to_remove:
    bpy.data.objects.remove(obj, do_unlink=True)
print(f"  Removed {len(to_remove)} cameras/lights")

# Verify origin -- find global min Z
global_min_z = float('inf')
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.data.vertices:
        for v in obj.data.vertices:
            world_z = (obj.matrix_world @ v.co).z
            if world_z < global_min_z:
                global_min_z = world_z

if global_min_z != float('inf') and abs(global_min_z) > 0.01:
    print(f"  Adjusting origin: global min Z was {global_min_z:.3f}, shifting to 0")
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.location.z -= global_min_z

os.makedirs(os.path.dirname(GLB_OUT), exist_ok=True)

bpy.ops.export_scene.gltf(
    filepath=GLB_OUT,
    export_format='GLB',
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
    export_apply=True,
    export_yup=True,
    export_texcoords=True,
    export_normals=True,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False,
)

file_size_kb = os.path.getsize(GLB_OUT) / 1024
final_tris = count_total_tris()
print(f"\n  Exported: {GLB_OUT}")
print(f"  Triangles: {final_tris}")
print(f"  File size: {file_size_kb:.0f} KB")
print(f"  Budget check: {'PASS' if final_tris <= MAX_TRIS else 'OVER BUDGET'}")
print(f"  Min check: {'PASS' if final_tris >= 12000 else 'BELOW MINIMUM'}")
print(f"  Size check: {'PASS' if file_size_kb <= 400 else 'LARGE (>400KB)'}")

# ============================================================
# RE-ADD CAMERA + LIGHTING FOR SAVE & SCREENSHOTS
# ============================================================
cam_data = bpy.data.cameras.new(name="Overview_Camera")
cam_data.lens_unit = 'FOV'
cam_data.angle = math.radians(45)
cam_data.clip_start = 0.1
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Overview_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (12, -10, 6)
target = Vector((0, 0, 1.2))
cam_dir = target - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam_obj

key_data = bpy.data.lights.new(name="Key_Light", type='SUN')
key_data.color = (1.0, 0.894, 0.8)
key_data.energy = 0.8
key_obj = bpy.data.objects.new("Key_Light", key_data)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (-8, 20, -6)
key_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

fill_data = bpy.data.lights.new(name="Fill_Light", type='AREA')
fill_data.color = (0.102, 0.102, 0.251)
fill_data.energy = 50
fill_data.size = 20
fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (5, 15, 10)
fill_obj.rotation_euler = (math.radians(60), 0, 0)

# ============================================================
# SAVE .BLEND
# ============================================================
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print(f"\n  Saved .blend: {BLEND_OUT}")

# ============================================================
# SCREENSHOTS
# ============================================================
print("\n" + "=" * 60)
print("RENDERING SCREENSHOTS")
print("=" * 60)

bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100

try:
    engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'ShaderNodeEeveeSpecular') else 'BLENDER_EEVEE'
    bpy.context.scene.render.engine = engine
except Exception:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGB'

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)

# Screenshot 1: Front elevation
cam_obj.location = (0, -14, 3)
cam_dir = Vector((0, 0, 1.0)) - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.render.filepath = os.path.join(SAVE_DIR, "s10fix1_front_elevation.png")
bpy.ops.render.render(write_still=True)
print("  s10fix1_front_elevation.png rendered")

# Screenshot 2: 3/4 angle
cam_obj.location = (12, -10, 6)
cam_dir = Vector((0, 0, 1.2)) - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.render.filepath = os.path.join(SAVE_DIR, "s10fix1_three_quarter.png")
bpy.ops.render.render(write_still=True)
print("  s10fix1_three_quarter.png rendered")

# Screenshot 3: Distance overview
cam_obj.location = (18, -15, 10)
cam_dir = Vector((0, 0, 0.8)) - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.render.filepath = os.path.join(SAVE_DIR, "s10fix1_distance_overview.png")
bpy.ops.render.render(write_still=True)
print("  s10fix1_distance_overview.png rendered")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("SESSION 10 FIX 1 COMPLETE")
print("=" * 60)
print(f"  Initial tris: {initial_tris}")
print(f"  Final tris: {final_tris}")
print(f"  Added: {final_tris - initial_tris} tris")
print(f"  Budget: {MAX_TRIS}")
print(f"  GLB size: {file_size_kb:.0f} KB")
print(f"  .blend: {BLEND_OUT}")
print(f"  .glb: {GLB_OUT}")
print(f"  Screenshots: 3 (front, 3/4, distance)")
mesh_count_final = sum(1 for o in bpy.data.objects if o.type == 'MESH')
print(f"  Mesh objects: {mesh_count_final}")
print("=" * 60)

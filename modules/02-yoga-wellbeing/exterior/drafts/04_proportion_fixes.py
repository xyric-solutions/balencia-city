"""
Session 9 — Proportion Fixes
After screenshot evaluation, adjust:
1. Garden platforms slightly larger for better visibility
2. Walkways slightly wider for better read at distance
3. Platform gap from water more pronounced (raise platform a bit)
4. Add a second accent ring near the platform top edge
5. Make vine clusters taller for vertical interest at edges
"""
import bpy
import math
from mathutils import Vector

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

# 1. Garden platforms — increase radius by 30%
for name, new_radius in [("garden_platform_01", 1.5), ("garden_platform_02", 1.1), ("garden_platform_03", 0.9)]:
    obj = bpy.data.objects.get(name)
    if obj:
        obj.scale = (new_radius / 1.2 if "01" in name else new_radius / 0.9 if "02" in name else new_radius / 0.7,
                     new_radius / 1.2 if "01" in name else new_radius / 0.9 if "02" in name else new_radius / 0.7,
                     1.0)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.select_set(False)
        deselect_all()

# Move garden platforms slightly further out and lower (more spread)
gp1 = bpy.data.objects.get("garden_platform_01")
if gp1:
    gp1.location = (-4.8, -1.2, 0.45)
gp2 = bpy.data.objects.get("garden_platform_02")
if gp2:
    gp2.location = (4.5, -1.8, 0.55)
gp3 = bpy.data.objects.get("garden_platform_03")
if gp3:
    gp3.location = (-4.0, 2.5, 0.65)

print("1. Garden platforms enlarged and repositioned")

# 2. Walkways — scale width slightly for better visibility
for wname in ["walkway_01", "walkway_02", "walkway_03"]:
    obj = bpy.data.objects.get(wname)
    if obj:
        obj.scale.y = 1.5  # 50% wider
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.select_set(False)
        deselect_all()

print("2. Walkways widened")

# 3. Raise main platform slightly for more visible gap above water
platform = bpy.data.objects.get("main_platform")
if platform:
    platform.location.z = 0.95  # was 0.8, raise to show more gap
rim = bpy.data.objects.get("platform_rim")
if rim:
    rim.location.z = 0.78  # was 0.63

# Raise all domes correspondingly
for dname in ["dome_large", "dome_medium", "dome_small",
              "dome_collar_large", "dome_collar_medium", "dome_collar_small"]:
    obj = bpy.data.objects.get(dname)
    if obj:
        obj.location.z += 0.15  # raise by same amount

# Raise planter walls and walkways too
for pname in ["planter_wall_01", "planter_wall_02",
              "walkway_01", "walkway_01_rail_L", "walkway_01_rail_R",
              "walkway_02", "walkway_02_rail_L", "walkway_02_rail_R"]:
    obj = bpy.data.objects.get(pname)
    if obj:
        obj.location.z += 0.15

# Move walkway_03 endpoint to match new platform height
for w3 in ["walkway_03", "walkway_03_rail_L", "walkway_03_rail_R"]:
    obj = bpy.data.objects.get(w3)
    if obj:
        obj.location.z += 0.10

# Raise energy receptor
receptor = bpy.data.objects.get("energy_receptor")
if receptor:
    receptor.location.z += 0.15

print("3. Platform and domes raised for more visible water gap")

# 4. Add second accent ring at platform top edge
bpy.ops.mesh.primitive_torus_add(
    major_radius=4.85, minor_radius=0.08,
    major_segments=32, minor_segments=6,
    location=(0, 0, 1.12)  # at top edge of platform
)
top_rim = bpy.context.active_object
top_rim.name = "platform_rim_top"
top_rim.scale = (1.0, 0.7, 0.8)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
mat = bpy.data.materials.get("accent")
if mat:
    top_rim.data.materials.append(mat)
deselect_all()

print("4. Top platform accent rim added")

# 5. Make vine clusters taller
for vc_name in ["vine_cluster_01", "vine_cluster_02", "vine_cluster_03", "vine_cluster_04"]:
    obj = bpy.data.objects.get(vc_name)
    if obj:
        obj.scale.z = 1.8  # stretch vertically
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.select_set(False)
        deselect_all()

# Also reposition vine clusters to hang from raised platform edge
vc1 = bpy.data.objects.get("vine_cluster_01")
if vc1:
    vc1.location = (-4.2, 0.0, 0.55)
vc2 = bpy.data.objects.get("vine_cluster_02")
if vc2:
    vc2.location = (4.0, -0.8, 0.55)
vc3 = bpy.data.objects.get("vine_cluster_03")
if vc3:
    vc3.location = (-2.0, -2.8, 0.55)
vc4 = bpy.data.objects.get("vine_cluster_04")
if vc4:
    vc4.location = (1.5, -2.5, 0.55)

print("5. Vine clusters elongated and repositioned")

# Recount triangles
total_tris = 0
mesh_report = []
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh_eval = obj_eval.to_mesh()
        tris = sum(max(1, len(p.vertices) - 2) for p in mesh_eval.polygons)
        obj_eval.to_mesh_clear()
        mesh_report.append((obj.name, tris))
        total_tris += tris

print(f"\nUpdated total: {total_tris} tris ({total_tris/10800*100:.1f}% of budget)")

# Save updated file
import os
bpy.ops.wm.save_as_mainfile(
    filepath="/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/exterior/drafts/yoga-exterior-s09.blend"
)
print("Saved updated .blend")

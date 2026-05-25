"""
Finance Interior Detail Pass -- Session 15
Final detail additions to reach 5K tri minimum.
Subdivides room shell, adds more architectural and data elements.

Run: blender -b finance-interior-s15.blend -P detail-pass-s15.py
"""

import bpy
import math
from mathutils import Vector

mats = {}
for mat in bpy.data.materials:
    if mat.name in ("base", "accent", "glass", "detail", "emissive", "energy"):
        mats[mat.name] = mat

def assign_mat(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)

def make_box(name, loc, dims, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        loc[0], loc[1], loc[2] + dims[2] / 2.0
    ))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (dims[0], dims[1], dims[2])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign_mat(obj, mat)
    return obj

def make_cylinder(name, loc, radius, depth, mat, segments=8):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, vertices=segments,
        location=(loc[0], loc[1], loc[2] + depth / 2.0)
    )
    obj = bpy.context.active_object
    obj.name = name
    assign_mat(obj, mat)
    return obj


# ============================================================
# DETAIL 1: Subdivide room shell planes for more geometry
# Each wall/floor/ceiling gets a 3x3 subdivision = 18 tris each
# ============================================================
shell_objects = [
    "room_floor", "room_ceiling", "room_wall_back",
    "room_wall_left", "room_wall_right",
    "room_front_glass_left", "room_front_glass_right", "room_front_glass_center"
]

for obj_name in shell_objects:
    obj = bpy.data.objects.get(obj_name)
    if obj:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=3)
        bpy.ops.object.mode_set(mode='OBJECT')

print("Detail 1: Room shell subdivided.")


# ============================================================
# DETAIL 2: Additional data visualization panels on wealth wall
# Small floating data cards at various heights
# ============================================================
data_card_positions = [
    (-4.2, -4.65, 5.5, 0.8, 0.5),
    (-4.2, -4.65, 3.2, 0.7, 0.4),
    (4.3, -4.65, 5.8, 0.8, 0.5),
    (4.3, -4.65, 3.5, 0.6, 0.45),
    (-1.8, -4.65, 6.8, 0.9, 0.3),
    (2.0, -4.65, 6.8, 0.9, 0.3),
]

for i, (dx, dy, dz, dw, dh) in enumerate(data_card_positions):
    make_box(f"data_card_{i:02d}", (dx, dy, dz - dh/2), (dw, 0.03, dh), mats["accent"])
    # Thin emissive border on each card
    make_box(f"data_card_{i:02d}_border", (dx, dy + 0.01, dz - dh/2), (dw + 0.04, 0.01, dh + 0.04), mats["emissive"])

print("Detail 2: Data cards added.")


# ============================================================
# DETAIL 3: Ceiling mounted projector units above workstations
# Small cylindrical projectors hanging from ceiling
# ============================================================
proj_positions = [(-3.5, -1.5), (-3.5, 1.5), (3.5, -1.5), (3.5, 1.5)]
for i, (px, py) in enumerate(proj_positions):
    # Projector body (small cylinder hanging down)
    make_cylinder(f"ceiling_proj_{i:02d}", (px, py, 7.2), 0.12, 0.4, mats["detail"], segments=8)
    # Projector mount rod
    make_cylinder(f"ceiling_proj_{i:02d}_rod", (px, py, 7.6), 0.03, 0.4, mats["detail"], segments=6)
    # Projector lens glow
    make_cylinder(f"ceiling_proj_{i:02d}_lens", (px, py, 7.15), 0.08, 0.05, mats["emissive"], segments=8)

print("Detail 3: Ceiling projectors added.")


# ============================================================
# DETAIL 4: Data ticker strip along the top of the back wall
# A continuous horizontal emissive strip with data segments
# ============================================================
make_box("data_ticker_strip", (0, -4.95, 7.3), (10.5, 0.04, 0.15), mats["emissive"])

# Ticker segment dividers
for i in range(12):
    x_pos = -4.75 + i * 0.87
    make_box(f"ticker_div_{i:02d}", (x_pos, -4.93, 7.3), (0.03, 0.02, 0.18), mats["detail"])

print("Detail 4: Data ticker strip added.")


# ============================================================
# DETAIL 5: Side alcove shelving/display niche (right wall)
# Mirror the stress display with a market status panel
# ============================================================
make_box("market_panel_screen", (5.5, -2.5, 2.0), (0.08, 1.8, 1.5), mats["accent"])
make_box("market_panel_frame_top", (5.5, -2.5, 3.3), (0.1, 2.0, 0.06), mats["detail"])
make_box("market_panel_frame_bot", (5.5, -2.5, 1.5), (0.1, 2.0, 0.06), mats["detail"])

# Market data bars (vertical bars like a bar chart)
for i in range(8):
    bar_height = 0.3 + (i % 3) * 0.25 + (i * 0.07)
    x = 5.45
    y = -3.2 + i * 0.2
    make_box(f"market_bar_{i:02d}", (x, y, 1.8), (0.02, 0.1, bar_height), mats["emissive"])

print("Detail 5: Market status panel added.")


# ============================================================
# DETAIL 6: Additional furniture -- side table between workstations
# ============================================================
for i, (tx, ty) in enumerate([(-3.5, 0), (3.5, 0)]):
    make_box(f"side_table_{i:02d}", (tx, ty, 0.0), (0.6, 0.6, 0.5), mats["detail"])
    make_box(f"side_table_{i:02d}_top_glow", (tx, ty, 0.49), (0.55, 0.55, 0.02), mats["emissive"])

print("Detail 6: Side tables added.")


# ============================================================
# DETAIL 7: Wall-mounted mini displays on side walls (2 per wall)
# ============================================================
for i, (wx, wy, wside) in enumerate([
    (-5.9, 1.5, "left"), (-5.9, -1.0, "left"),
    (5.9, 1.5, "right"), (5.9, 0.5, "right")
]):
    make_box(f"wall_display_{i:02d}", (wx, wy, 2.5), (0.05, 0.8, 0.5), mats["accent"])
    make_box(f"wall_display_{i:02d}_glow", (wx + (0.02 if "left" in wside else -0.02), wy, 2.5), (0.02, 0.7, 0.4), mats["emissive"])

print("Detail 7: Wall-mounted displays added.")


# ============================================================
# DETAIL 8: Decorative floor inlays (accent patterns near entry)
# ============================================================
# Circular inlay at the entry
bpy.ops.mesh.primitive_circle_add(vertices=16, radius=1.5, location=(0, 3.5, 0.01), fill_type='NGON')
floor_inlay = bpy.context.active_object
floor_inlay.name = "floor_inlay_circle"
assign_mat(floor_inlay, mats["accent"])

# Inner circle
bpy.ops.mesh.primitive_circle_add(vertices=12, radius=0.8, location=(0, 3.5, 0.015), fill_type='NGON')
floor_inlay_inner = bpy.context.active_object
floor_inlay_inner.name = "floor_inlay_inner"
assign_mat(floor_inlay_inner, mats["emissive"])

print("Detail 8: Floor inlays added.")


# ============================================================
# DETAIL 9: Additional energy conduit routing
# ============================================================
# Energy conduit running along the base of the right wall
make_box("energy_conduit_02", (5.7, 0, 0.0), (0.1, 7.0, 0.08), mats["energy"])
# Energy junction box
make_box("energy_junction_01", (5.5, -4.5, 0.0), (0.25, 0.25, 0.2), mats["energy"])

print("Detail 9: Additional energy conduits added.")


# ============================================================
# FINAL TRI COUNT
# ============================================================
print("\n=== FINAL TRIANGLE COUNT ===")
total_tris = 0
mat_tris = {}
mesh_count = 0
for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type != 'MESH':
        continue
    mesh_count += 1
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    mesh.calc_loop_triangles()
    tris = len(mesh.loop_triangles)
    eval_obj.to_mesh_clear()
    total_tris += tris
    mat_name = obj.data.materials[0].name if obj.data.materials else "NONE"
    mat_tris[mat_name] = mat_tris.get(mat_name, 0) + tris

print(f"\nMesh objects: {mesh_count}")
print(f"TOTAL: {total_tris} tris")
print(f"\nBy material slot:")
for slot, count in sorted(mat_tris.items()):
    pct = count / total_tris * 100
    print(f"  {slot}: {count} tris ({pct:.1f}%)")

print(f"\nBudget: 5,000 - 10,000 tris")
status = 'WITHIN BUDGET' if 5000 <= total_tris <= 10000 else 'UNDER BUDGET' if total_tris < 5000 else 'OVER BUDGET'
print(f"Status: {status}")

# ============================================================
# Save .blend
# ============================================================
blend_path = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/interior/drafts/finance-interior-s15.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved: {blend_path}")

print("\n=== DETAIL PASS COMPLETE ===")

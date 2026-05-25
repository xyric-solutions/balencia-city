"""
Finance Interior Final Detail -- Session 15
Push tri count into 5K-10K range with additional architectural and data elements.
"""

import bpy
import math

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


# ============================================================
# ADD 1: Further subdivide the wealth analytics wall
# ============================================================
wall = bpy.data.objects.get("wealth_analytics_wall")
if wall:
    bpy.ops.object.select_all(action='DESELECT')
    wall.select_set(True)
    bpy.context.view_layer.objects.active = wall
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=2)
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Wealth wall subdivided further.")

# ============================================================
# ADD 2: Subdivide depth panels behind wealth wall
# ============================================================
for i in range(3):
    panel = bpy.data.objects.get(f"display_depth_panel_{i:02d}")
    if panel:
        bpy.ops.object.select_all(action='DESELECT')
        panel.select_set(True)
        bpy.context.view_layer.objects.active = panel
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=3)
        bpy.ops.object.mode_set(mode='OBJECT')

print("Depth panels subdivided.")

# ============================================================
# ADD 3: Additional ceiling detail -- cross beams
# ============================================================
for i, y_pos in enumerate([-3.5, -1.0, 1.5, 4.0]):
    make_box(f"ceiling_beam_{i:02d}", (0, y_pos, 7.5), (11.5, 0.15, 0.2), mats["detail"])

# Ceiling beam side accents
for i, y_pos in enumerate([-3.5, -1.0, 1.5, 4.0]):
    make_box(f"ceiling_beam_{i:02d}_glow", (0, y_pos, 7.45), (11.0, 0.08, 0.03), mats["emissive"])

print("Ceiling beams added.")

# ============================================================
# ADD 4: More detailed chair geometry -- armrests
# ============================================================
for i, (cx, cy) in enumerate([(-3.5, -0.7), (-3.5, 2.3), (3.5, -0.7), (3.5, 2.3)]):
    # Left armrest
    make_box(f"chair_{i:02d}_arm_l", (cx - 0.22, cy + 0.05, 0.32), (0.06, 0.35, 0.18), mats["detail"])
    # Right armrest
    make_box(f"chair_{i:02d}_arm_r", (cx + 0.22, cy + 0.05, 0.32), (0.06, 0.35, 0.18), mats["detail"])

print("Chair armrests added.")

# ============================================================
# ADD 5: Wall panel accent grid (more subdivisions on visible walls)
# ============================================================
# Additional accent trim on back wall (vertical)
for i, x_pos in enumerate([-4.0, -2.0, 0, 2.0, 4.0]):
    make_box(f"wall_back_strip_v_{i:02d}", (x_pos, -4.98, 0.5), (0.04, 0.03, 6.5), mats["accent"])

print("Back wall accent grid added.")

# ============================================================
# ADD 6: Workstation keyboard/input surfaces
# ============================================================
for i, (wx, wy) in enumerate([(-3.5, -1.5), (-3.5, 1.5), (3.5, -1.5), (3.5, 1.5)]):
    # Keyboard surface (thin slab on desk)
    make_box(f"workstation_{i:02d}_keyboard", (wx, wy + 0.15, 0.76), (0.6, 0.25, 0.02), mats["detail"])
    # Small status indicator light
    make_box(f"workstation_{i:02d}_status", (wx + 0.8, wy - 0.3, 0.76), (0.06, 0.06, 0.02), mats["emissive"])

print("Workstation keyboards added.")


# ============================================================
# FINAL TRI COUNT AND SAVE
# ============================================================
print("\n=== FINAL TRIANGLE COUNT ===")
total_tris = 0
mat_tris = {}
mesh_count = 0
empty_count = 0

for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type == 'EMPTY':
        empty_count += 1
        print(f"  [EMPTY] {obj.name}: pos ({obj.location.x:.1f}, {obj.location.y:.1f}, {obj.location.z:.1f})")
        continue
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
print(f"Empty objects: {empty_count}")
print(f"TOTAL: {total_tris} tris")
print(f"\nBy material slot:")
for slot, count in sorted(mat_tris.items()):
    pct = count / total_tris * 100
    print(f"  {slot}: {count} tris ({pct:.1f}%)")

print(f"\nBudget: 5,000 - 10,000 tris")
status = 'WITHIN BUDGET' if 5000 <= total_tris <= 10000 else 'UNDER BUDGET' if total_tris < 5000 else 'OVER BUDGET'
print(f"Status: {status}")

# Save
blend_path = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/interior/drafts/finance-interior-s15.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved: {blend_path}")
print("=== FINAL DETAIL COMPLETE ===")

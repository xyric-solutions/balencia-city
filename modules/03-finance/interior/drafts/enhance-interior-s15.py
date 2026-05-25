"""
Finance Interior Enhancement Pass -- Session 15
Adds geometric detail to bring tri count from ~1,600 into 5K-10K range.
Loads the existing .blend and adds detail elements.

Run: blender -b finance-interior-s15.blend -P enhance-interior-s15.py
"""

import bpy
import math
from mathutils import Vector

# ============================================================
# Load material references
# ============================================================
mats = {}
for mat in bpy.data.materials:
    if mat.name in ("base", "accent", "glass", "detail", "emissive", "energy"):
        mats[mat.name] = mat

print("Materials loaded:", list(mats.keys()))

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

def make_cylinder(name, loc, radius, depth, mat, segments=12):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, vertices=segments,
        location=(loc[0], loc[1], loc[2] + depth / 2.0)
    )
    obj = bpy.context.active_object
    obj.name = name
    assign_mat(obj, mat)
    return obj


# ============================================================
# ENHANCEMENT 1: Wall panel subdivisions
# Accent trim lines on side walls and back wall to add architectural grid
# ============================================================

# Left wall -- vertical accent strips (3 strips)
for i, y_pos in enumerate([-3.0, -0.5, 2.0]):
    make_box(f"wall_left_strip_v_{i:02d}", (-5.95, y_pos, 0.5), (0.04, 0.06, 6.0), mats["accent"])

# Left wall -- horizontal accent strips (2)
for i, z_pos in enumerate([2.5, 5.5]):
    make_box(f"wall_left_strip_h_{i:02d}", (-5.95, 0, z_pos - 0.5), (0.04, 9.0, 0.06), mats["accent"])

# Right wall -- vertical accent strips (3)
for i, y_pos in enumerate([-3.0, -0.5, 2.0]):
    make_box(f"wall_right_strip_v_{i:02d}", (5.95, y_pos, 0.5), (0.04, 0.06, 6.0), mats["accent"])

# Right wall -- horizontal accent strips (2)
for i, z_pos in enumerate([2.5, 5.5]):
    make_box(f"wall_right_strip_h_{i:02d}", (5.95, 0, z_pos - 0.5), (0.04, 9.0, 0.06), mats["accent"])

# Back wall -- horizontal accent below the display
make_box("wall_back_accent_low", (0, -4.95, 0.7), (11.0, 0.04, 0.06), mats["accent"])

print("Enhancement 1: Wall panel accents added.")


# ============================================================
# ENHANCEMENT 2: Ceiling recessed light troughs
# Two long recessed channels in ceiling running front-to-back
# ============================================================

# Left trough
make_box("ceiling_trough_left", (-3.0, 0, 7.7), (0.8, 8.5, 0.25), mats["detail"])
make_box("ceiling_trough_left_glow", (-3.0, 0, 7.6), (0.5, 8.0, 0.04), mats["emissive"])

# Right trough
make_box("ceiling_trough_right", (3.0, 0, 7.7), (0.8, 8.5, 0.25), mats["detail"])
make_box("ceiling_trough_right_glow", (3.0, 0, 7.6), (0.5, 8.0, 0.04), mats["emissive"])

# Center trough (smaller, above the aisle)
make_box("ceiling_trough_center", (0, 0, 7.8), (0.4, 8.5, 0.15), mats["detail"])
make_box("ceiling_trough_center_glow", (0, 0, 7.7), (0.25, 8.0, 0.03), mats["emissive"])

print("Enhancement 2: Ceiling troughs added.")


# ============================================================
# ENHANCEMENT 3: Wealth analytics wall depth elements
# Add more data cascade elements and layered depth panels
# ============================================================

# Secondary data streams (thinner, between main cascades)
secondary_x = [-2.8, -1.2, 0.2, 1.5, 3.0]
for i, x_pos in enumerate(secondary_x):
    make_box(
        f"data_cascade_sec_{i:02d}",
        (x_pos, -4.72, 2.0),
        (0.08, 0.03, 4.5),
        mats["emissive"]
    )

# Data node points (small cubes at cascade intersections with bands)
node_positions = [
    (-3.5, 2.5), (-2.0, 4.5), (-0.5, 2.5), (0.8, 6.5),
    (2.2, 4.5), (3.8, 2.5), (-2.8, 4.5), (1.5, 2.5),
    (0.2, 6.5), (3.0, 4.5), (-1.2, 6.5), (-3.5, 6.5),
]
for i, (nx, nz) in enumerate(node_positions):
    make_box(
        f"data_node_{i:02d}",
        (nx, -4.70, nz - 0.5),
        (0.12, 0.04, 0.12),
        mats["emissive"]
    )

# Sub-panels behind the main display (layered depth effect)
for i, x_off in enumerate([-3.5, 0, 3.5]):
    make_box(
        f"display_depth_panel_{i:02d}",
        (x_off, -4.92, 3.0),
        (2.8, 0.03, 3.5),
        mats["accent"]
    )

print("Enhancement 3: Wealth analytics wall detail added.")


# ============================================================
# ENHANCEMENT 4: Enhanced workstation geometry
# Add monitor screens and desk edge accents
# ============================================================

workstation_positions = [
    (-3.5, -1.5), (-3.5, 1.5), (3.5, -1.5), (3.5, 1.5)
]

for i, (wx, wy) in enumerate(workstation_positions):
    # Monitor/screen above desk (thin vertical panel)
    make_box(
        f"workstation_{i:02d}_screen",
        (wx, wy - 0.2, 0.78),
        (1.2, 0.04, 0.7),
        mats["accent"]
    )

    # Desk edge accent (thin emissive strip along front edge)
    front_y = wy + 0.38 if wy < 0 else wy + 0.38
    make_box(
        f"workstation_{i:02d}_edge_glow",
        (wx, front_y, 0.73),
        (1.8, 0.02, 0.02),
        mats["emissive"]
    )

print("Enhancement 4: Workstation screens and accents added.")


# ============================================================
# ENHANCEMENT 5: Floor detail -- raised platform for workstations
# ============================================================

# Slightly raised platforms under each workstation pair
for i, (px, py_center) in enumerate([(-3.5, 0), (3.5, 0)]):
    make_box(
        f"workstation_platform_{i:02d}",
        (px, py_center, 0.0),
        (3.0, 5.5, 0.04),
        mats["detail"]
    )
    # Platform edge glow
    make_box(
        f"platform_edge_{i:02d}_front",
        (px, py_center + 2.72, 0.0),
        (3.0, 0.04, 0.03),
        mats["emissive"]
    )
    make_box(
        f"platform_edge_{i:02d}_back",
        (px, py_center - 2.72, 0.0),
        (3.0, 0.04, 0.03),
        mats["emissive"]
    )

print("Enhancement 5: Workstation platforms added.")


# ============================================================
# ENHANCEMENT 6: Column supports at room edges
# 4 cylindrical columns at the corners
# ============================================================

corner_positions = [(-5.5, -4.5), (-5.5, 4.5), (5.5, -4.5), (5.5, 4.5)]
for i, (cx, cy) in enumerate(corner_positions):
    col = make_cylinder(f"column_{i:02d}", (cx, cy, 0), 0.2, 8.0, mats["detail"], segments=8)
    # Column base ring
    make_cylinder(f"column_{i:02d}_base", (cx, cy, 0), 0.3, 0.15, mats["accent"], segments=8)
    # Column capital ring
    make_cylinder(f"column_{i:02d}_cap", (cx, cy, 7.85), 0.3, 0.15, mats["accent"], segments=8)

print("Enhancement 6: Corner columns added.")


# ============================================================
# ENHANCEMENT 7: Additional investment visualization elements
# Floating data rings around holograms
# ============================================================

# Ring around main globe hologram
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.55, minor_radius=0.02,
    major_segments=20, minor_segments=6,
    location=(0, -0.5, 2.0)
)
ring1 = bpy.context.active_object
ring1.name = "holo_ring_01"
ring1.rotation_euler = (math.radians(30), math.radians(15), 0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
assign_mat(ring1, mats["emissive"])

# Second ring at different angle
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.55, minor_radius=0.02,
    major_segments=20, minor_segments=6,
    location=(0, -0.5, 2.0)
)
ring2 = bpy.context.active_object
ring2.name = "holo_ring_02"
ring2.rotation_euler = (math.radians(-20), math.radians(45), math.radians(30))
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
assign_mat(ring2, mats["emissive"])

# Data axis lines (thin cylinders through the globe hologram)
for j, (rx, ry, rz) in enumerate([(90, 0, 0), (0, 0, 0), (0, 90, 0)]):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.01, depth=1.2, vertices=6,
        location=(0, -0.5, 2.0)
    )
    axis = bpy.context.active_object
    axis.name = f"holo_axis_{j:02d}"
    axis.rotation_euler = (math.radians(rx), math.radians(ry), math.radians(rz))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    assign_mat(axis, mats["emissive"])

print("Enhancement 7: Hologram rings and axes added.")


# ============================================================
# ENHANCEMENT 8: More stress display detail
# ============================================================

# Additional wave patterns (curved strips on stress display)
for i in range(5):
    z_off = 0.3 * i
    make_box(
        f"stress_wave_sec_{i:02d}",
        (-5.43, -3.0, 1.6 + z_off),
        (0.02, 1.6, 0.04),
        mats["emissive"]
    )

# Stress display side frame
make_box("stress_frame_left", (-5.5, -4.28, 1.8), (0.1, 0.06, 1.8), mats["detail"])
make_box("stress_frame_right", (-5.5, -1.72, 1.8), (0.1, 0.06, 1.8), mats["detail"])

print("Enhancement 8: Stress display detail added.")


# ============================================================
# ENHANCEMENT 9: Front glass mullions (structural dividers)
# ============================================================

# Vertical mullions on front glass
for x_pos in [-5.0, -2.0, -1.0, 1.0, 2.0, 5.0]:
    make_box(
        f"glass_mullion_v_{x_pos:.0f}",
        (x_pos, 5.0, 0.0),
        (0.08, 0.08, 8.0),
        mats["detail"]
    )

# Horizontal mullion at mid-height
make_box("glass_mullion_h_mid", (0, 5.0, 3.5), (12.0, 0.08, 0.08), mats["detail"])

# Top header
make_box("glass_mullion_h_top", (0, 5.0, 7.5), (12.0, 0.1, 0.12), mats["detail"])

# Bottom sill
make_box("glass_mullion_h_bottom", (0, 5.0, 0.0), (12.0, 0.1, 0.1), mats["detail"])

print("Enhancement 9: Glass mullions added.")


# ============================================================
# ENHANCEMENT 10: Baseboard and crown molding
# ============================================================

# Baseboard -- accent strip along floor/wall junction
make_box("baseboard_back", (0, -4.98, 0.0), (11.8, 0.03, 0.12), mats["accent"])
make_box("baseboard_left", (-5.98, 0, 0.0), (0.03, 9.8, 0.12), mats["accent"])
make_box("baseboard_right", (5.98, 0, 0.0), (0.03, 9.8, 0.12), mats["accent"])

# Crown molding -- detail strip along ceiling/wall junction
make_box("crown_back", (0, -4.98, 7.7), (11.8, 0.03, 0.1), mats["detail"])
make_box("crown_left", (-5.98, 0, 7.7), (0.03, 9.8, 0.1), mats["detail"])
make_box("crown_right", (5.98, 0, 7.7), (0.03, 9.8, 0.1), mats["detail"])

print("Enhancement 10: Baseboard and crown molding added.")


# ============================================================
# FINAL TRI COUNT
# ============================================================
print("\n=== FINAL TRIANGLE COUNT ===")
total_tris = 0
mat_tris = {}
for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type != 'MESH':
        continue
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    mesh.calc_loop_triangles()
    tris = len(mesh.loop_triangles)
    eval_obj.to_mesh_clear()
    total_tris += tris
    mat_name = obj.data.materials[0].name if obj.data.materials else "NONE"
    mat_tris[mat_name] = mat_tris.get(mat_name, 0) + tris
    print(f"  {obj.name}: {tris} tris ({mat_name})")

print(f"\nTOTAL: {total_tris} tris")
print(f"\nBy material slot:")
for slot, count in sorted(mat_tris.items()):
    pct = count / total_tris * 100
    print(f"  {slot}: {count} tris ({pct:.1f}%)")

print(f"\nBudget: 5,000 - 10,000 tris")
status = 'WITHIN BUDGET' if 5000 <= total_tris <= 10000 else 'UNDER BUDGET' if total_tris < 5000 else 'OVER BUDGET'
print(f"Status: {status}")


# ============================================================
# Save updated .blend
# ============================================================
blend_path = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/interior/drafts/finance-interior-s15.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved: {blend_path}")


# ============================================================
# Render from camera_target perspective
# ============================================================
cam = bpy.data.objects.get("Overview_Camera")
if cam:
    cam_target = bpy.data.objects.get("camera_target")
    if cam_target:
        # Position camera near camera_target, looking toward wealth analytics wall
        cam.location = (0, 3.5, 2.5)
        look_at = Vector((0, -4.5, 4.0))
        direction = look_at - cam.location
        cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        cam.data.lens = 24  # Wide angle for interior

    screenshot_path = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s15_interior_camera_target.png"
    bpy.context.scene.render.filepath = screenshot_path
    bpy.ops.render.render(write_still=True)
    print(f"Screenshot: {screenshot_path}")

    # Render from open wall looking in
    cam.location = (3, 8, 3)
    look_at2 = Vector((-1, -3, 4))
    direction2 = look_at2 - cam.location
    cam.rotation_euler = direction2.to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = 28

    screenshot_path2 = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s15_interior_from_entrance.png"
    bpy.context.scene.render.filepath = screenshot_path2
    bpy.ops.render.render(write_still=True)
    print(f"Screenshot: {screenshot_path2}")


print("\n=== ENHANCEMENT PASS COMPLETE ===")

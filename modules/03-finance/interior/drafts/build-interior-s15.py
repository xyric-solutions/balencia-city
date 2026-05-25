"""
Balencia City v3 -- Finance Interior Build Script
Session 15 (2026-05-23)

Room: Double-height financial advisory space (~12m x 10m x 8m)
Focal element: Wealth analytics wall (curved display, back wall)
Props: Workstations, investment holograms, budget wheels, stress display, seating, floor channels
Empties: light_0, light_1, light_2, camera_target

Run: blender -b -P build-interior-s15.py
"""

import bpy
import math
import bmesh

# ============================================================
# STEP 1: Clear scene
# ============================================================
bpy.ops.wm.read_factory_settings(use_empty=True)
print("Scene cleared.")

# ============================================================
# STEP 2: Lighting rig + Materials
# ============================================================

# -- World background --
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
if hasattr(world, 'use_nodes'):
    world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background") if world.node_tree else None
if bg_node:
    bg_node.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)  # #0A0A0F
    bg_node.inputs["Strength"].default_value = 1.0

# -- Viewport lights (for preview only, removed before export) --
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

# -- Camera (for preview only, removed before export) --
cam_data = bpy.data.cameras.new(name="Overview_Camera")
cam_data.lens = 35
cam_data.clip_start = 0.1
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Overview_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (0, 12, 5)
from mathutils import Vector
cam_dir = Vector((0, 0, 3)) - cam_obj.location
cam_obj.rotation_euler = cam_dir.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam_obj

# -- Render settings --
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

print("Lighting rig loaded.")

# -- Material Library (7-slot, district color #F59E0B) --
def hex_to_linear(hex_color):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    def to_linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (to_linear(r), to_linear(g), to_linear(b), 1.0)

BASE_COLOR = hex_to_linear("#1E1E28")
ACCENT_INACTIVE = hex_to_linear("#2A2A38")
GLASS_COLOR = hex_to_linear("#0F0F18")
DETAIL_COLOR = hex_to_linear("#16161E")
ENERGY_ORANGE = hex_to_linear("#FF5E00")
DISTRICT_COLOR = hex_to_linear("#F59E0B")

def _make_mat(name, base_color, roughness, metallic, emission_color=None, emission_strength=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name=name)
    if hasattr(mat, 'use_nodes'):
        mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission_color and emission_strength > 0:
        bsdf.inputs["Emission Color"].default_value = emission_color
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        if hasattr(mat, 'surface_render_method'):
            mat.surface_render_method = 'BLENDED'
        elif hasattr(mat, 'blend_method'):
            mat.blend_method = 'BLEND'
    return mat

mats = {}
mats["base"] = _make_mat("base", BASE_COLOR, 0.80, 0.05)
mats["accent"] = _make_mat("accent", ACCENT_INACTIVE, 0.55, 0.16, DISTRICT_COLOR, 0.24)
mats["glass"] = _make_mat("glass", GLASS_COLOR, 0.10, 0.30, hex_to_linear("#FEF3C7"), 0.08, 0.86)
mats["detail"] = _make_mat("detail", DETAIL_COLOR, 0.60, 0.15)
mats["emissive"] = _make_mat("emissive", DETAIL_COLOR, 0.22, 0.00, DISTRICT_COLOR, 0.06)
mats["energy"] = _make_mat("energy", DETAIL_COLOR, 0.15, 0.10, ENERGY_ORANGE, 0.10)
print("Materials created:", list(mats.keys()))


# ============================================================
# Helper functions
# ============================================================
def assign_mat(obj, mat):
    """Assign a single material to an object."""
    obj.data.materials.clear()
    obj.data.materials.append(mat)

def make_box(name, loc, dims, mat):
    """Create a box (cube) with given dimensions at location. dims = (width, depth, height)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        loc[0], loc[1], loc[2] + dims[2] / 2.0
    ))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (dims[0], dims[1], dims[2])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign_mat(obj, mat)
    return obj

def make_plane(name, loc, rot_deg, scale, mat):
    """Create a plane with rotation (degrees) and scale."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = (math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2]))
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    assign_mat(obj, mat)
    return obj

def make_cylinder(name, loc, radius, depth, mat, segments=16):
    """Create a cylinder."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, vertices=segments,
        location=(loc[0], loc[1], loc[2] + depth / 2.0)
    )
    obj = bpy.context.active_object
    obj.name = name
    assign_mat(obj, mat)
    return obj

def make_torus(name, loc, major_r, minor_r, mat, major_seg=24, minor_seg=8):
    """Create a torus (flat disc shape for budget wheels)."""
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_r, minor_radius=minor_r,
        major_segments=major_seg, minor_segments=minor_seg,
        location=loc
    )
    obj = bpy.context.active_object
    obj.name = name
    assign_mat(obj, mat)
    return obj


# ============================================================
# STEP 3: Room shell
# 12m wide (X: -6 to +6), 10m deep (Y: -5 to +5), 8m tall (Z: 0 to 8)
# Front (Y=+5) is glass. Back (Y=-5) is solid wall.
# ============================================================

# Floor
make_plane("room_floor", (0, 0, 0), (0, 0, 0), (12, 10, 1), mats["base"])

# Ceiling
make_plane("room_ceiling", (0, 0, 8), (0, 0, 0), (12, 10, 1), mats["base"])

# Back wall
make_plane("room_wall_back", (0, -5, 4), (90, 0, 0), (12, 8, 1), mats["base"])

# Left wall
make_plane("room_wall_left", (-6, 0, 4), (90, 0, 90), (10, 8, 1), mats["base"])

# Right wall
make_plane("room_wall_right", (6, 0, 4), (90, 0, -90), (10, 8, 1), mats["base"])

# Front glass panels (3 panels -- city light enters here)
make_plane("room_front_glass_left", (-3.5, 5, 4), (90, 0, 180), (5, 8, 1), mats["glass"])
make_plane("room_front_glass_right", (3.5, 5, 4), (90, 0, 180), (5, 8, 1), mats["glass"])
make_plane("room_front_glass_center", (0, 4.95, 4), (90, 0, 180), (2, 8, 1), mats["glass"])

print("Room shell complete.")


# ============================================================
# STEP 4: Focal element -- Wealth Analytics Wall
# Floor-to-ceiling curved display on back wall, ~10m wide x 6m tall
# Positioned against back wall (Y=-4.9)
# ============================================================

# Main curved display surface -- subdivided plane curved into slight concave arc
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -4.85, 4.5))
wall_display = bpy.context.active_object
wall_display.name = "wealth_analytics_wall"
wall_display.scale = (10, 6, 1)
wall_display.rotation_euler = (math.radians(90), 0, 0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

# Subdivide for curvature
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=6)
bpy.ops.object.mode_set(mode='OBJECT')

# Apply slight concave curve via proportional editing (manual vertex displacement)
mesh = wall_display.data
for v in mesh.vertices:
    # Create a gentle concave curve: center vertices push forward (toward +Y)
    # x ranges from -5 to +5 (half-width = 5)
    norm_x = v.co.x / 5.0  # -1 to 1
    curve_amount = (1.0 - norm_x * norm_x) * 0.6  # parabolic, max 0.6m at center
    v.co.y += curve_amount

assign_mat(wall_display, mats["accent"])

# Data cascade streams -- vertical emissive strips flowing down the display
cascade_positions = [-3.5, -2.0, -0.5, 0.8, 2.2, 3.8]
for i, x_pos in enumerate(cascade_positions):
    # Tall thin box representing a flowing data stream
    stream = make_box(
        f"data_cascade_{i:02d}",
        (x_pos, -4.75, 1.5),
        (0.15, 0.05, 5.5),
        mats["emissive"]
    )

# Data cascade horizontal bands (3 bands across the display)
for i, z_pos in enumerate([2.5, 4.5, 6.5]):
    band = make_box(
        f"data_band_{i:02d}",
        (0, -4.75, z_pos - 0.5),
        (9.5, 0.04, 0.08),
        mats["emissive"]
    )

# Display frame -- thin border around the wealth analytics wall
# Top frame
make_box("display_frame_top", (0, -4.88, 7.5 - 0.5), (10.2, 0.08, 0.12), mats["detail"])
# Bottom frame
make_box("display_frame_bottom", (0, -4.88, 1.2), (10.2, 0.08, 0.12), mats["detail"])
# Left frame
make_box("display_frame_left", (-5.1, -4.88, 3.8), (0.12, 0.08, 5.6), mats["detail"])
# Right frame
make_box("display_frame_right", (5.1, -4.88, 3.8), (0.12, 0.08, 5.6), mats["detail"])

print("Focal element complete: wealth analytics wall with data cascades.")


# ============================================================
# STEP 5: Props
# ============================================================

# --- PROP 1: AI Advisor Workstations (4 stations, 2 per side) ---
workstation_positions = [
    (-3.5, -1.5, "left"),   # Left row, near back
    (-3.5, 1.5, "left"),    # Left row, near front
    (3.5, -1.5, "right"),   # Right row, near back
    (3.5, 1.5, "right"),    # Right row, near front
]

for i, (wx, wy, side) in enumerate(workstation_positions):
    # Desk surface (sleek slab)
    desk = make_box(
        f"workstation_{i:02d}_desk",
        (wx, wy, 0.0),
        (2.0, 0.8, 0.75),
        mats["detail"]
    )

    # Desk leg supports (two thin columns)
    leg_offset = 0.7
    for j, lx in enumerate([wx - leg_offset, wx + leg_offset]):
        leg = make_box(
            f"workstation_{i:02d}_leg_{j}",
            (lx, wy, 0.0),
            (0.08, 0.5, 0.72),
            mats["detail"]
        )

    # Holographic projector surface (thin glowing plate above desk)
    holo_proj = make_box(
        f"workstation_{i:02d}_holo_proj",
        (wx, wy, 0.85),
        (1.4, 0.5, 0.03),
        mats["emissive"]
    )

print("Prop 1 complete: 4 AI advisor workstations.")


# --- PROP 2: Investment Holograms (3 floating geometric shapes at center) ---
# These float at eye level (Z ~1.5-2.0) in the center aisle between workstation rows

# Ico sphere -- portfolio globe
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.35, subdivisions=2, location=(0, -0.5, 2.0))
holo_globe = bpy.context.active_object
holo_globe.name = "investment_holo_01"
assign_mat(holo_globe, mats["emissive"])

# Octahedron-like shape (diamond) -- investment diamond
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.28, subdivisions=1, location=(-1.2, 0.5, 1.8))
holo_diamond = bpy.context.active_object
holo_diamond.name = "investment_holo_02"
holo_diamond.scale = (1, 1, 1.5)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
assign_mat(holo_diamond, mats["emissive"])

# Cube frame -- market cube
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(1.0, 0.2, 1.9))
holo_cube = bpy.context.active_object
holo_cube.name = "investment_holo_03"
holo_cube.rotation_euler = (math.radians(15), math.radians(30), math.radians(20))
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
assign_mat(holo_cube, mats["emissive"])

print("Prop 2 complete: 3 investment holograms.")


# --- PROP 3: Budget Wheels (4 flat torus discs near workstations) ---
for i, (bx, by) in enumerate([(-3.5, -1.5), (-3.5, 1.5), (3.5, -1.5), (3.5, 1.5)]):
    wheel = make_torus(
        f"budget_wheel_{i:02d}",
        (bx, by, 1.3),
        0.22, 0.03,
        mats["emissive"],
        major_seg=16, minor_seg=6
    )
    # Tilt slightly toward viewer
    wheel.rotation_euler = (math.radians(25), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

print("Prop 3 complete: 4 budget wheels.")


# --- PROP 4: Stress-Spending Correlation Display (side alcove) ---
# Curved screen in the left wall alcove area
make_box("stress_display_screen", (-5.5, -3.0, 1.5), (0.08, 2.5, 2.0), mats["accent"])

# Wave pattern strips on the stress display (3 horizontal emissive lines)
for i, z_off in enumerate([0.0, 0.6, 1.2]):
    make_box(
        f"stress_wave_{i:02d}",
        (-5.45, -3.0, 1.8 + z_off),
        (0.02, 2.0, 0.06),
        mats["emissive"]
    )

# Display frame
make_box("stress_display_frame_top", (-5.5, -3.0, 3.3), (0.1, 2.6, 0.06), mats["detail"])
make_box("stress_display_frame_bottom", (-5.5, -3.0, 1.3), (0.1, 2.6, 0.06), mats["detail"])

print("Prop 4 complete: stress-spending display.")


# --- PROP 5: Seating (4 chairs at workstations) ---
for i, (cx, cy) in enumerate([(-3.5, -0.7), (-3.5, 2.3), (3.5, -0.7), (3.5, 2.3)]):
    # Seat (flat box)
    seat = make_box(
        f"chair_{i:02d}_seat",
        (cx, cy, 0.0),
        (0.5, 0.5, 0.42),
        mats["detail"]
    )
    # Back rest (thin vertical box)
    back = make_box(
        f"chair_{i:02d}_back",
        (cx, cy + 0.22, 0.42),
        (0.5, 0.06, 0.45),
        mats["detail"]
    )

print("Prop 5 complete: 4 chairs.")


# --- PROP 6: Floor Channel Lights (gold-lit recessed strips) ---
# Central aisle channel
make_box("floor_channel_center", (0, 0, -0.01), (0.12, 8.0, 0.02), mats["emissive"])

# Cross channels connecting workstation rows
for i, y_pos in enumerate([-2.5, 0.0, 2.5]):
    make_box(
        f"floor_channel_cross_{i:02d}",
        (0, y_pos, -0.01),
        (10.0, 0.08, 0.02),
        mats["emissive"]
    )

# Perimeter channel along walls
make_box("floor_channel_back", (0, -4.8, -0.01), (11.0, 0.08, 0.02), mats["emissive"])
make_box("floor_channel_left", (-5.8, 0, -0.01), (0.08, 9.0, 0.02), mats["emissive"])
make_box("floor_channel_right", (5.8, 0, -0.01), (0.08, 9.0, 0.02), mats["emissive"])

print("Prop 6 complete: floor channel lights.")


# --- BONUS: Energy conduit element (single visible conduit on floor) ---
make_box("energy_conduit_01", (5.5, -4.0, 0.0), (0.15, 3.0, 0.1), mats["energy"])

print("Energy conduit placed.")


# ============================================================
# STEP 6: Place Empties
# ============================================================

# light_0: Center of advisory space -- warm gold key light at double-height ceiling
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 7.5))
light_0 = bpy.context.active_object
light_0.name = "light_0"
light_0.empty_display_size = 0.5

# light_1: Behind wealth analytics wall -- intense gold backlight
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, -5.2, 4.5))
light_1 = bpy.context.active_object
light_1.name = "light_1"
light_1.empty_display_size = 0.5

# light_2: Above workstation row -- cool fill
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 1.5, 7.0))
light_2 = bpy.context.active_object
light_2.name = "light_2"
light_2.empty_display_size = 0.5

# camera_target: Center of room at standing eye height, facing wealth analytics wall
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.5, 1.6))
cam_target = bpy.context.active_object
cam_target.name = "camera_target"
cam_target.empty_display_size = 0.3

print("Empties placed: light_0, light_1, light_2, camera_target")


# ============================================================
# STEP 7: Material Audit
# ============================================================
VALID_SLOTS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
issues = []
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    if not obj.data.materials:
        issues.append(f"{obj.name}: NO MATERIAL")
        continue
    for mat in obj.data.materials:
        if mat and mat.name not in VALID_SLOTS:
            issues.append(f"{obj.name}: invalid material '{mat.name}'")

if issues:
    print("MATERIAL AUDIT ISSUES:")
    for iss in issues:
        print(f"  - {iss}")
else:
    print("Material audit PASSED: all objects use valid 7-slot materials.")


# ============================================================
# STEP 8: Count triangles per object
# ============================================================
print("\n=== TRIANGLE COUNT ===")
total_tris = 0
obj_tris = []
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
    obj_tris.append((obj.name, tris))
    mat_name = obj.data.materials[0].name if obj.data.materials else "NONE"
    print(f"  {obj.name}: {tris} tris ({mat_name})")

print(f"\nTOTAL: {total_tris} tris")
print(f"Budget: 5,000 - 10,000 tris")
print(f"Status: {'WITHIN BUDGET' if 5000 <= total_tris <= 10000 else 'UNDER BUDGET' if total_tris < 5000 else 'OVER BUDGET'}")


# ============================================================
# STEP 9: Save .blend
# ============================================================
blend_path = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/interior/drafts/finance-interior-s15.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")


# ============================================================
# STEP 10: Render a preview screenshot
# ============================================================
# Position camera to see the room from the open wall looking in
cam_obj.location = (0, 10, 5)
cam_dir2 = Vector((0, -1, 3)) - cam_obj.location
cam_obj.rotation_euler = cam_dir2.to_track_quat('-Z', 'Y').to_euler()

screenshot_path = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s15_interior_overview.png"
bpy.context.scene.render.filepath = screenshot_path
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print(f"Screenshot saved: {screenshot_path}")


print("\n=== BUILD COMPLETE ===")
print("Next steps: dark-first test, decimation if needed, export GLB")

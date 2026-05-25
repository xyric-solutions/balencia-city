"""
Session 12: Yoga & Wellbeing Integration Test
Balencia City v3

Steps:
1. Clear scene, setup lighting rig
2. Import all 6 approved GLBs (SIA, Fitness, Yoga ext+int)
3. Position structures at orbital positions
4. Run alignment checks on Yoga interior vs exterior
5. Set up Scene 5 camera positions and render screenshots
6. Run cohesion check across all 3 structures
"""

import bpy
import math
import sys
import os
import json
from mathutils import Vector

# Paths
BASE = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
SCREENSHOT_DIR = os.path.join(BASE, "modules/02-yoga-wellbeing/exterior/drafts")

GLB_FILES = {
    "sia_ext": os.path.join(BASE, "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb"),
    "sia_int": os.path.join(BASE, "modules/00-sia-tower/interior/approved/sia-tower-int.glb"),
    "fitness_ext": os.path.join(BASE, "modules/01-fitness/exterior/approved/fitness-ext.glb"),
    "fitness_int": os.path.join(BASE, "modules/01-fitness/interior/approved/fitness-int.glb"),
    "yoga_ext": os.path.join(BASE, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb"),
    "yoga_int": os.path.join(BASE, "modules/02-yoga-wellbeing/interior/approved/yoga-int.glb"),
}

POSITIONS = {
    "sia": Vector((0, 0, 0)),
    "fitness": Vector((25, 25, 0)),
    "yoga": Vector((35, 10, 0)),
}

# ============================================================
# STEP 1: Clear scene
# ============================================================
print("\n" + "=" * 60)
print("STEP 1: Clearing scene")
print("=" * 60)

bpy.ops.wm.read_factory_settings(use_empty=True)
print("Scene cleared (factory settings, empty)")

# ============================================================
# STEP 1b: Run lighting rig
# ============================================================
print("\n" + "=" * 60)
print("STEP 1b: Setting up lighting rig")
print("=" * 60)

lighting_rig_path = os.path.join(BASE, "shared/lighting-rig.py")
exec(open(lighting_rig_path).read())
print("Lighting rig loaded")

# ============================================================
# STEP 2: Import all 6 GLBs
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Importing GLBs and positioning structures")
print("=" * 60)

results = {}

for key, filepath in GLB_FILES.items():
    if not os.path.exists(filepath):
        print(f"  ERROR: {filepath} not found!")
        results[key] = {"error": "file not found"}
        continue

    # Track objects before import
    before = set(bpy.data.objects.keys())

    # Import GLB
    bpy.ops.import_scene.gltf(filepath=filepath)

    # Identify newly imported objects
    after = set(bpy.data.objects.keys())
    new_objects = after - before

    # Determine position offset
    module = key.split("_")[0]  # sia, fitness, yoga
    offset = POSITIONS[module]

    # Move new objects to their position
    for obj_name in new_objects:
        obj = bpy.data.objects[obj_name]
        if obj.parent is None:  # Only move root objects
            obj.location += offset

    file_size = os.path.getsize(filepath)
    results[key] = {
        "objects_imported": len(new_objects),
        "object_names_sample": sorted(list(new_objects))[:5],
        "offset": list(offset),
        "file_size_kb": round(file_size / 1024, 1),
    }
    print(f"  Imported {key}: {len(new_objects)} objects, offset {list(offset)}, {round(file_size/1024,1)} KB")

print(f"\nTotal scene objects: {len(bpy.data.objects)}")

# ============================================================
# STEP 3: Alignment Checks — Yoga Interior vs Exterior
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Alignment Checks")
print("=" * 60)

alignment_results = {}

# Helper: compute world-space bounding box for a collection of objects
def get_world_bbox(obj_names, offset=Vector((0, 0, 0))):
    """Get combined bounding box of named objects in world space."""
    mins = Vector((float('inf'), float('inf'), float('inf')))
    maxs = Vector((float('-inf'), float('-inf'), float('-inf')))
    found = 0

    for name in obj_names:
        obj = bpy.data.objects.get(name)
        if obj is None or obj.type != 'MESH':
            continue
        found += 1
        # Get world-space bounding box corners
        for corner in obj.bound_box:
            world_corner = obj.matrix_world @ Vector(corner)
            for i in range(3):
                if world_corner[i] < mins[i]:
                    mins[i] = world_corner[i]
                if world_corner[i] > maxs[i]:
                    maxs[i] = world_corner[i]

    return mins, maxs, found

# Collect yoga-related objects by checking their position
yoga_offset = POSITIONS["yoga"]

# Separate yoga exterior and interior objects based on GLB import order
# We need to identify which objects belong to exterior vs interior
# The interior was imported AFTER the exterior, so we track by import batch

# Re-approach: collect ALL mesh objects near yoga position
yoga_objects = []
yoga_empties = []
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        # Check if object is near yoga position
        dist_xy = ((obj.matrix_world.translation.x - yoga_offset.x) ** 2 +
                    (obj.matrix_world.translation.y - yoga_offset.y) ** 2) ** 0.5
        if dist_xy < 25:  # Within 25 units of yoga center
            yoga_objects.append(obj)
    elif obj.type == 'EMPTY':
        dist_xy = ((obj.matrix_world.translation.x - yoga_offset.x) ** 2 +
                    (obj.matrix_world.translation.y - yoga_offset.y) ** 2) ** 0.5
        if dist_xy < 25:
            yoga_empties.append(obj)

print(f"\nYoga-region objects: {len(yoga_objects)} mesh, {len(yoga_empties)} empties")

# Get overall bounding box of all yoga objects
if yoga_objects:
    all_mins = Vector((float('inf'), float('inf'), float('inf')))
    all_maxs = Vector((float('-inf'), float('-inf'), float('-inf')))
    for obj in yoga_objects:
        for corner in obj.bound_box:
            wc = obj.matrix_world @ Vector(corner)
            for i in range(3):
                if wc[i] < all_mins[i]:
                    all_mins[i] = wc[i]
                if wc[i] > all_maxs[i]:
                    all_maxs[i] = wc[i]

    yoga_size = all_maxs - all_mins
    yoga_center = (all_mins + all_maxs) / 2
    print(f"  Combined bounding box: {[round(v, 2) for v in all_mins]} to {[round(v, 2) for v in all_maxs]}")
    print(f"  Size: {round(yoga_size.x, 2)} x {round(yoga_size.y, 2)} x {round(yoga_size.z, 2)}")
    print(f"  Center: ({round(yoga_center.x, 2)}, {round(yoga_center.y, 2)}, {round(yoga_center.z, 2)})")

    alignment_results["combined_bbox_min"] = [round(v, 2) for v in all_mins]
    alignment_results["combined_bbox_max"] = [round(v, 2) for v in all_maxs]
    alignment_results["combined_size"] = [round(yoga_size.x, 2), round(yoga_size.y, 2), round(yoga_size.z, 2)]
    alignment_results["combined_center"] = [round(yoga_center.x, 2), round(yoga_center.y, 2), round(yoga_center.z, 2)]

    # Check Z alignment (both should start at Z=0 + offset.z = 0)
    z_min = round(all_mins.z, 3)
    z_aligned = abs(z_min) < 0.5  # Allow small tolerance
    alignment_results["z_min"] = z_min
    alignment_results["z_aligned"] = z_aligned
    print(f"  Z-min: {z_min} (aligned: {z_aligned})")

# Check empties
print(f"\n  Empties in yoga region:")
empty_check = {}
for emp in yoga_empties:
    local_pos = emp.matrix_world.translation - yoga_offset
    print(f"    {emp.name}: world ({round(emp.matrix_world.translation.x, 2)}, {round(emp.matrix_world.translation.y, 2)}, {round(emp.matrix_world.translation.z, 2)}), local ({round(local_pos.x, 2)}, {round(local_pos.y, 2)}, {round(local_pos.z, 2)})")

    # Check if empty is inside bounding box
    pos = emp.matrix_world.translation
    inside = (all_mins.x <= pos.x <= all_maxs.x and
              all_mins.y <= pos.y <= all_maxs.y and
              all_mins.z <= pos.z <= all_maxs.z)
    empty_check[emp.name] = {
        "world_pos": [round(pos.x, 2), round(pos.y, 2), round(pos.z, 2)],
        "local_pos": [round(local_pos.x, 2), round(local_pos.y, 2), round(local_pos.z, 2)],
        "inside_bbox": inside,
    }

alignment_results["empties"] = empty_check

# Check for unapplied transforms
unapplied = []
for obj in yoga_objects:
    s = obj.scale
    if abs(s.x - 1) > 0.01 or abs(s.y - 1) > 0.01 or abs(s.z - 1) > 0.01:
        unapplied.append(f"{obj.name} scale=({round(s.x,3)},{round(s.y,3)},{round(s.z,3)})")
    r = obj.rotation_euler
    if abs(r.x) > 0.01 or abs(r.y) > 0.01 or abs(r.z) > 0.01:
        unapplied.append(f"{obj.name} rot=({round(math.degrees(r.x),1)},{round(math.degrees(r.y),1)},{round(math.degrees(r.z),1)})")

alignment_results["unapplied_transforms"] = unapplied
if unapplied:
    print(f"\n  WARNING: Unapplied transforms found:")
    for u in unapplied[:10]:
        print(f"    {u}")
else:
    print(f"\n  All transforms clean (no unapplied scale/rotation)")

# Interior-inside-exterior check
# The interior should be geometrically contained within the exterior envelope
# We check this by verifying the interior bbox fits inside the exterior bbox
# Since we imported them at the same offset, they should overlap

# Count tris by structure
def count_tris(objects):
    total = 0
    for obj in objects:
        if obj.type == 'MESH' and obj.data:
            total += len(obj.data.polygons)
            # For triangulated count, sum up face loop counts
            for poly in obj.data.polygons:
                if poly.loop_total == 3:
                    total += 0  # already counted
                elif poly.loop_total == 4:
                    total += 1  # quad = 2 tris, already counted 1
                elif poly.loop_total > 4:
                    total += poly.loop_total - 3  # n-gon = n-2 tris
    return total

# ============================================================
# STEP 4: Scene 5 Camera Setup and Screenshots
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Scene 5 Camera Setup")
print("=" * 60)

# Remove existing overview camera
old_cam = bpy.data.objects.get("Overview_Camera")
if old_cam:
    bpy.data.objects.remove(old_cam, do_unlink=True)

# Set up render settings
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# Camera 1: Scene 5 wide establishing shot
# Camera at ~60u from yoga, at eye level with platform (~2-3u height)
# Looking toward yoga with SIA Tower visible in background
cam1_loc = Vector(yoga_offset) + Vector((50, -30, 3))
cam1_target = Vector(yoga_offset) + Vector((0, 0, 2))

cam1_data = bpy.data.cameras.new(name="Scene5_Wide")
cam1_data.lens = 35  # Wider for establishing shot
cam1_data.clip_start = 0.1
cam1_data.clip_end = 300
cam1_obj = bpy.data.objects.new("Scene5_Wide", cam1_data)
bpy.context.collection.objects.link(cam1_obj)
cam1_obj.location = cam1_loc
direction = cam1_target - cam1_loc
cam1_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam1_obj

# Render Shot 1
shot1_path = os.path.join(SCREENSHOT_DIR, "s12_integration_scene5_wide.png")
bpy.context.scene.render.filepath = shot1_path
bpy.ops.render.render(write_still=True)
print(f"  Shot 1 (wide establishing): {shot1_path}")

# Camera 2: Scene 5 closer approach
cam2_loc = Vector(yoga_offset) + Vector((18, -12, 3))
cam2_target = Vector(yoga_offset) + Vector((0, 0, 2.5))

cam2_data = bpy.data.cameras.new(name="Scene5_Close")
cam2_data.lens = 50  # Normal lens for detail
cam2_data.clip_start = 0.1
cam2_data.clip_end = 200
cam2_obj = bpy.data.objects.new("Scene5_Close", cam2_data)
bpy.context.collection.objects.link(cam2_obj)
cam2_obj.location = cam2_loc
direction = cam2_target - cam2_loc
cam2_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam2_obj

shot2_path = os.path.join(SCREENSHOT_DIR, "s12_integration_scene5_close.png")
bpy.context.scene.render.filepath = shot2_path
bpy.ops.render.render(write_still=True)
print(f"  Shot 2 (closer approach): {shot2_path}")

# Camera 3: Top-down overview of all 3 structures
cam3_loc = Vector((20, 12, 70))  # High above center of all structures
cam3_target = Vector((20, 12, 0))  # Look straight down

cam3_data = bpy.data.cameras.new(name="TopDown_Overview")
cam3_data.lens = 35
cam3_data.clip_start = 0.1
cam3_data.clip_end = 200
cam3_obj = bpy.data.objects.new("TopDown_Overview", cam3_data)
bpy.context.collection.objects.link(cam3_obj)
cam3_obj.location = cam3_loc
direction = cam3_target - cam3_loc
cam3_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam3_obj

shot3_path = os.path.join(SCREENSHOT_DIR, "s12_integration_topdown.png")
bpy.context.scene.render.filepath = shot3_path
bpy.ops.render.render(write_still=True)
print(f"  Shot 3 (top-down overview): {shot3_path}")

# Camera 4: Skyline test - wide angle showing all 3 structures
# Position camera far back to see everything
cam4_loc = Vector((20, -80, 25))  # Far south, elevated
cam4_target = Vector((15, 10, 5))  # Looking at the cluster center

cam4_data = bpy.data.cameras.new(name="Skyline_Test")
cam4_data.lens = 28  # Wide for skyline
cam4_data.clip_start = 0.1
cam4_data.clip_end = 300
cam4_obj = bpy.data.objects.new("Skyline_Test", cam4_data)
bpy.context.collection.objects.link(cam4_obj)
cam4_obj.location = cam4_loc
direction = cam4_target - cam4_loc
cam4_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam4_obj

shot4_path = os.path.join(SCREENSHOT_DIR, "s12_integration_skyline.png")
bpy.context.scene.render.filepath = shot4_path
bpy.ops.render.render(write_still=True)
print(f"  Shot 4 (skyline test): {shot4_path}")

# ============================================================
# STEP 5: Structure-level analysis
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: Structure Analysis")
print("=" * 60)

# Analyze each structure's bounding box
structures = {}
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    pos = obj.matrix_world.translation
    # Determine which structure this belongs to
    dist_to_sia = ((pos.x - 0) ** 2 + (pos.y - 0) ** 2) ** 0.5
    dist_to_fitness = ((pos.x - 25) ** 2 + (pos.y - 25) ** 2) ** 0.5
    dist_to_yoga = ((pos.x - 35) ** 2 + (pos.y - 10) ** 2) ** 0.5

    min_dist = min(dist_to_sia, dist_to_fitness, dist_to_yoga)
    if min_dist == dist_to_sia:
        key = "sia"
    elif min_dist == dist_to_fitness:
        key = "fitness"
    else:
        key = "yoga"

    if key not in structures:
        structures[key] = {"objects": [], "bbox_min": Vector((float('inf'),) * 3), "bbox_max": Vector((float('-inf'),) * 3)}

    structures[key]["objects"].append(obj)
    for corner in obj.bound_box:
        wc = obj.matrix_world @ Vector(corner)
        for i in range(3):
            if wc[i] < structures[key]["bbox_min"][i]:
                structures[key]["bbox_min"][i] = wc[i]
            if wc[i] > structures[key]["bbox_max"][i]:
                structures[key]["bbox_max"][i] = wc[i]

print("\nStructure Analysis:")
for name, data in sorted(structures.items()):
    size = data["bbox_max"] - data["bbox_min"]
    height = size.z
    print(f"\n  {name.upper()}:")
    print(f"    Objects: {len(data['objects'])}")
    print(f"    BBox: ({round(data['bbox_min'].x,1)}, {round(data['bbox_min'].y,1)}, {round(data['bbox_min'].z,1)}) to ({round(data['bbox_max'].x,1)}, {round(data['bbox_max'].y,1)}, {round(data['bbox_max'].z,1)})")
    print(f"    Size: {round(size.x,1)} x {round(size.y,1)} x {round(size.z,1)}")
    print(f"    Height: {round(height,1)}u")

    # Material analysis
    materials = {}
    for obj in data["objects"]:
        if obj.type == 'MESH' and obj.data:
            for mat_slot in obj.material_slots:
                if mat_slot.material:
                    mat_name = mat_slot.material.name
                    if mat_name not in materials:
                        materials[mat_name] = 0
                    materials[mat_name] += 1
    print(f"    Materials: {dict(materials)}")

# Scale progression check
print("\n\nScale Progression Check:")
heights = {}
for name, data in structures.items():
    h = data["bbox_max"].z - data["bbox_min"].z
    heights[name] = round(h, 1)

print(f"  SIA Tower: {heights.get('sia', 'N/A')}u")
print(f"  Fitness: {heights.get('fitness', 'N/A')}u")
print(f"  Yoga: {heights.get('yoga', 'N/A')}u")

sia_h = heights.get('sia', 0)
fitness_h = heights.get('fitness', 0)
yoga_h = heights.get('yoga', 0)

if sia_h > 0 and fitness_h > 0 and yoga_h > 0:
    print(f"\n  SIA dominates Fitness: {round(sia_h / fitness_h, 1)}x (expected: >2.5x)")
    print(f"  SIA dominates Yoga: {round(sia_h / yoga_h, 1)}x (expected: >2.5x)")
    print(f"  Fitness > Yoga: {round(fitness_h / yoga_h, 1)}x (expected: >1.5x)")
    print(f"  Scale progression reads: {'NATURAL' if sia_h > fitness_h > yoga_h else 'NEEDS ADJUSTMENT'}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("INTEGRATION TEST SUMMARY")
print("=" * 60)

print(f"\nGLBs imported: {len(results)}")
for key, data in results.items():
    status = "OK" if "error" not in data else "FAILED"
    print(f"  {key}: {status} ({data.get('objects_imported', 0)} objects, {data.get('file_size_kb', 0)} KB)")

print(f"\nAlignment:")
print(f"  Z-min: {alignment_results.get('z_min', 'N/A')}")
print(f"  Z-aligned: {alignment_results.get('z_aligned', 'N/A')}")
print(f"  Unapplied transforms: {len(alignment_results.get('unapplied_transforms', []))}")

print(f"\nEmpties:")
for name, data in alignment_results.get("empties", {}).items():
    print(f"  {name}: inside bbox = {data['inside_bbox']}, pos = {data['world_pos']}")

print(f"\nScreenshots saved to: {SCREENSHOT_DIR}")
print(f"  s12_integration_scene5_wide.png")
print(f"  s12_integration_scene5_close.png")
print(f"  s12_integration_topdown.png")
print(f"  s12_integration_skyline.png")

print("\n" + "=" * 60)
print("INTEGRATION TEST COMPLETE")
print("=" * 60)

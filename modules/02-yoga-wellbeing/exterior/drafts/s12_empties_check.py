"""
Session 12: Targeted empties and alignment check for Yoga module
"""
import bpy
import os
from mathutils import Vector

BASE = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"

# Clear and reimport just yoga ext+int to check alignment precisely
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import yoga exterior
yoga_ext_path = os.path.join(BASE, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb")
before_ext = set(bpy.data.objects.keys())
bpy.ops.import_scene.gltf(filepath=yoga_ext_path)
after_ext = set(bpy.data.objects.keys())
ext_objects = after_ext - before_ext

# Import yoga interior
yoga_int_path = os.path.join(BASE, "modules/02-yoga-wellbeing/interior/approved/yoga-int.glb")
before_int = set(bpy.data.objects.keys())
bpy.ops.import_scene.gltf(filepath=yoga_int_path)
after_int = set(bpy.data.objects.keys())
int_objects = after_int - before_int

print("\n" + "=" * 60)
print("YOGA EXTERIOR OBJECTS")
print("=" * 60)

ext_mesh_count = 0
ext_bbox_min = Vector((float('inf'),) * 3)
ext_bbox_max = Vector((float('-inf'),) * 3)
for name in sorted(ext_objects):
    obj = bpy.data.objects[name]
    if obj.type == 'MESH':
        ext_mesh_count += 1
        for corner in obj.bound_box:
            wc = obj.matrix_world @ Vector(corner)
            for i in range(3):
                if wc[i] < ext_bbox_min[i]:
                    ext_bbox_min[i] = wc[i]
                if wc[i] > ext_bbox_max[i]:
                    ext_bbox_max[i] = wc[i]
    elif obj.type == 'EMPTY':
        print(f"  EMPTY: {name} at {[round(v, 3) for v in obj.matrix_world.translation]}")

ext_size = ext_bbox_max - ext_bbox_min
print(f"\n  Exterior mesh objects: {ext_mesh_count}")
print(f"  Exterior BBox: {[round(v, 3) for v in ext_bbox_min]} to {[round(v, 3) for v in ext_bbox_max]}")
print(f"  Exterior Size: {round(ext_size.x, 2)} x {round(ext_size.y, 2)} x {round(ext_size.z, 2)}")

print("\n" + "=" * 60)
print("YOGA INTERIOR OBJECTS")
print("=" * 60)

int_mesh_count = 0
int_bbox_min = Vector((float('inf'),) * 3)
int_bbox_max = Vector((float('-inf'),) * 3)
int_empties = []
for name in sorted(int_objects):
    obj = bpy.data.objects[name]
    if obj.type == 'MESH':
        int_mesh_count += 1
        for corner in obj.bound_box:
            wc = obj.matrix_world @ Vector(corner)
            for i in range(3):
                if wc[i] < int_bbox_min[i]:
                    int_bbox_min[i] = wc[i]
                if wc[i] > int_bbox_max[i]:
                    int_bbox_max[i] = wc[i]
    elif obj.type == 'EMPTY':
        pos = obj.matrix_world.translation
        int_empties.append((name, [round(v, 3) for v in pos]))
        print(f"  EMPTY: {name} at {[round(v, 3) for v in pos]}")

int_size = int_bbox_max - int_bbox_min
print(f"\n  Interior mesh objects: {int_mesh_count}")
print(f"  Interior BBox: {[round(v, 3) for v in int_bbox_min]} to {[round(v, 3) for v in int_bbox_max]}")
print(f"  Interior Size: {round(int_size.x, 2)} x {round(int_size.y, 2)} x {round(int_size.z, 2)}")

print("\n" + "=" * 60)
print("ALIGNMENT CHECK")
print("=" * 60)

# Check 1: Interior fits inside exterior shell
int_inside_ext = True
for i in range(3):
    if int_bbox_min[i] < ext_bbox_min[i] - 0.5:
        int_inside_ext = False
        print(f"  FAIL: Interior min[{i}] ({round(int_bbox_min[i], 3)}) outside exterior min[{i}] ({round(ext_bbox_min[i], 3)})")
    if int_bbox_max[i] > ext_bbox_max[i] + 0.5:
        int_inside_ext = False
        print(f"  FAIL: Interior max[{i}] ({round(int_bbox_max[i], 3)}) outside exterior max[{i}] ({round(ext_bbox_max[i], 3)})")

if int_inside_ext:
    print("  PASS: Interior fits within exterior shell (with 0.5u tolerance)")
else:
    print("  WARNING: Some interior geometry extends beyond exterior")

# Check 2: Origin alignment (both bottom-center at Y=0 plane)
ext_z_min = round(ext_bbox_min.z, 3)
int_z_min = round(int_bbox_min.z, 3)
z_diff = abs(ext_z_min - int_z_min)
print(f"\n  Exterior Z-min: {ext_z_min}")
print(f"  Interior Z-min: {int_z_min}")
print(f"  Z difference: {round(z_diff, 3)}")
print(f"  Origin aligned: {'PASS' if z_diff < 0.5 else 'FAIL'}")

# Check 3: Scale match (1:1)
ext_center = (ext_bbox_min + ext_bbox_max) / 2
int_center = (int_bbox_min + int_bbox_max) / 2
center_offset = int_center - ext_center
print(f"\n  Exterior center: ({round(ext_center.x, 2)}, {round(ext_center.y, 2)}, {round(ext_center.z, 2)})")
print(f"  Interior center: ({round(int_center.x, 2)}, {round(int_center.y, 2)}, {round(int_center.z, 2)})")
print(f"  Center offset: ({round(center_offset.x, 2)}, {round(center_offset.y, 2)}, {round(center_offset.z, 2)})")

# Interior should be smaller than exterior in XY, similar height or shorter
print(f"\n  Ext size: {round(ext_size.x, 2)} x {round(ext_size.y, 2)} x {round(ext_size.z, 2)}")
print(f"  Int size: {round(int_size.x, 2)} x {round(int_size.y, 2)} x {round(int_size.z, 2)}")
scale_ok = int_size.x <= ext_size.x + 1 and int_size.y <= ext_size.y + 1
print(f"  Interior smaller than exterior in XY: {'PASS' if scale_ok else 'FAIL'}")

# Check 4: Empties inside the building volume
print(f"\n  Empty placement check:")
for name, pos in int_empties:
    inside = (ext_bbox_min.x - 1 <= pos[0] <= ext_bbox_max.x + 1 and
              ext_bbox_min.y - 1 <= pos[1] <= ext_bbox_max.y + 1 and
              ext_bbox_min.z - 0.5 <= pos[2] <= ext_bbox_max.z + 1)
    print(f"    {name}: {pos} inside building: {'PASS' if inside else 'FAIL'}")

# Check 5: Window/opening orientation
# The open wall should face outward toward the city center (toward 0,0,0)
# The interior has a 60-90 degree wall gap. We check by finding the window_wall object
window_obj = None
for name in int_objects:
    if 'window' in name.lower():
        window_obj = bpy.data.objects[name]
        break

if window_obj:
    win_pos = window_obj.matrix_world.translation
    print(f"\n  Window wall position: ({round(win_pos.x, 2)}, {round(win_pos.y, 2)}, {round(win_pos.z, 2)})")
    # The window should face toward the city center (0,0,0 before offset)
    # So the window wall normal should point away from center
    print(f"  Window faces: toward city center assessment requires visual verification")
else:
    print(f"\n  Window wall object not found by name search")

# Check all objects for unapplied transforms
print(f"\n  Transform check (all yoga objects):")
unapplied = 0
for name in sorted(ext_objects | int_objects):
    obj = bpy.data.objects.get(name)
    if obj and obj.type == 'MESH':
        s = obj.scale
        if abs(s.x - 1) > 0.01 or abs(s.y - 1) > 0.01 or abs(s.z - 1) > 0.01:
            unapplied += 1
            if unapplied <= 5:
                print(f"    Unapplied scale: {name} ({round(s.x,3)}, {round(s.y,3)}, {round(s.z,3)})")
print(f"  Total unapplied: {unapplied}")
print(f"  Transforms: {'PASS' if unapplied == 0 else 'FAIL'}")

print("\n" + "=" * 60)
print("EMPTIES CHECK COMPLETE")
print("=" * 60)

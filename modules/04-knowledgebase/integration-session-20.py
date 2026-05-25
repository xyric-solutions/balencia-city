"""
Session 20: Knowledgebase Integration Test (Headless)
- Import all 5 modules (ext + int)
- Position at orbital positions
- Apply lighting rig
- Run alignment checks on Knowledgebase (#04)
- Set up camera for Scene 7
- Render screenshots
"""
import bpy
import math
import os
import json
import sys
from mathutils import Vector

# ===========================================================================
# CONFIG
# ===========================================================================
BASE = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules"
SHARED = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared"
SCREENSHOTS = f"{BASE}/04-knowledgebase/screenshots"

# Ensure screenshots dir exists
os.makedirs(SCREENSHOTS, exist_ok=True)

structures = [
    ("SIA_Tower",
     f"{BASE}/00-sia-tower/exterior/approved/sia-tower-ext.glb",
     f"{BASE}/00-sia-tower/interior/approved/sia-tower-int.glb",
     (0, 0, 0)),
    ("Fitness",
     f"{BASE}/01-fitness/exterior/approved/fitness-ext.glb",
     f"{BASE}/01-fitness/interior/approved/fitness-int.glb",
     (25, 25, 0)),
    ("Yoga",
     f"{BASE}/02-yoga-wellbeing/exterior/approved/yoga-ext.glb",
     f"{BASE}/02-yoga-wellbeing/interior/approved/yoga-int.glb",
     (35, 10, 0)),
    ("Finance",
     f"{BASE}/03-finance/exterior/approved/finance-ext.glb",
     f"{BASE}/03-finance/interior/approved/finance-int-approved-s15.glb",
     (35, -5, 0)),
    ("Knowledgebase",
     f"{BASE}/04-knowledgebase/exterior/approved/knowledgebase-ext.glb",
     f"{BASE}/04-knowledgebase/interior/approved/knowledgebase-int.glb",
     (30, -20, 0)),
]

# ===========================================================================
# STEP 1a — Clear scene
# ===========================================================================
print("=" * 60)
print("STEP 1: Scene Setup")
print("=" * 60)
bpy.ops.wm.read_factory_settings(use_empty=True)

# ===========================================================================
# STEP 1b — Import and position all structures
# ===========================================================================
import_results = {}

for name, ext_path, int_path, pos in structures:
    px, py, pz = pos
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    ext_count = 0
    int_count = 0

    # Import exterior
    if os.path.exists(ext_path):
        bpy.ops.import_scene.gltf(filepath=ext_path)
        imported = list(bpy.context.selected_objects)
        for obj in imported:
            for c in obj.users_collection:
                c.objects.unlink(obj)
            col.objects.link(obj)
            obj.location.x += px
            obj.location.y += py
            obj.location.z += pz
        ext_count = len(imported)
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print(f"  WARNING: Missing exterior: {ext_path}")

    # Import interior
    if os.path.exists(int_path):
        bpy.ops.import_scene.gltf(filepath=int_path)
        imported = list(bpy.context.selected_objects)
        for obj in imported:
            for c in obj.users_collection:
                c.objects.unlink(obj)
            col.objects.link(obj)
            obj.location.x += px
            obj.location.y += py
            obj.location.z += pz
        int_count = len(imported)
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print(f"  WARNING: Missing interior: {int_path}")

    import_results[name] = {"ext": ext_count, "int": int_count, "pos": pos}
    print(f"  {name}: ext={ext_count}, int={int_count}, pos={pos}")

total_objects = len([o for o in bpy.data.objects if o.type in ('MESH', 'EMPTY')])
print(f"\nTotal scene objects: {total_objects}")

# ===========================================================================
# STEP 2 — Run lighting rig
# ===========================================================================
print("\n" + "=" * 60)
print("STEP 2: Lighting Rig")
print("=" * 60)
exec(open(f"{SHARED}/lighting-rig.py").read())

# ===========================================================================
# STEP 3 — Alignment Checks (Knowledgebase #04)
# ===========================================================================
print("\n" + "=" * 60)
print("STEP 3: Alignment Checks (Knowledgebase #04)")
print("=" * 60)

kb_col = bpy.data.collections.get("Knowledgebase")
kb_pos = Vector((30, -20, 0))

if kb_col:
    kb_objects = list(kb_col.objects)

    # Separate exterior and interior objects by inspecting their original names/positions
    ext_objects = []
    int_objects = []
    empties = []

    for obj in kb_objects:
        if obj.type == 'EMPTY':
            empties.append(obj)
        elif obj.type == 'MESH':
            # Interior objects tend to have names like room_*, knowledge_*, book_*, memory_*, etc.
            # Exterior objects have names like stone_*, arched_*, data_floor_*, crown_*, etc.
            n = obj.name.lower()
            int_markers = ['room_', 'knowledge_', 'book_', 'memory_', 'reading_', 'alcove_',
                          'research_', 'focal_', 'graph_', 'cloud_', 'droplet_',
                          'floor_center', 'floor_trim', 'rustication_', 'panel_inset',
                          'ceiling_', 'molding_', 'cornice_int', 'pilaster_',
                          'tree_', 'seat_', 'floor_border', 'floor_cross', 'floor_aisle',
                          'shelf_', 'doorway_', 'desk_', 'root_']
            is_interior = any(marker in n for marker in int_markers)
            if is_interior:
                int_objects.append(obj)
            else:
                ext_objects.append(obj)

    print(f"\nKnowledgebase collection: {len(kb_objects)} total objects")
    print(f"  Mesh objects classified as exterior: {len(ext_objects)}")
    print(f"  Mesh objects classified as interior: {len(int_objects)}")
    print(f"  Empties: {len(empties)}")

    # --- Check 3a: Bounding boxes ---
    def get_bbox_world(obj):
        """Get world-space bounding box corners."""
        if not hasattr(obj, 'bound_box'):
            return None
        corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        mins = Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners)))
        maxs = Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners)))
        return mins, maxs

    def get_group_bbox(objects):
        """Get combined bounding box for a group of objects."""
        all_mins = []
        all_maxs = []
        for obj in objects:
            bb = get_bbox_world(obj)
            if bb:
                all_mins.append(bb[0])
                all_maxs.append(bb[1])
        if not all_mins:
            return None
        mins = Vector((min(m.x for m in all_mins), min(m.y for m in all_mins), min(m.z for m in all_mins)))
        maxs = Vector((max(m.x for m in all_maxs), max(m.y for m in all_maxs), max(m.z for m in all_maxs)))
        return mins, maxs

    ext_bbox = get_group_bbox(ext_objects)
    int_bbox = get_group_bbox(int_objects)

    if ext_bbox:
        ext_min, ext_max = ext_bbox
        ext_size = ext_max - ext_min
        print(f"\n  Exterior bounding box:")
        print(f"    Min: ({ext_min.x:.2f}, {ext_min.y:.2f}, {ext_min.z:.2f})")
        print(f"    Max: ({ext_max.x:.2f}, {ext_max.y:.2f}, {ext_max.z:.2f})")
        print(f"    Size: ({ext_size.x:.2f}, {ext_size.y:.2f}, {ext_size.z:.2f})")

    if int_bbox:
        int_min, int_max = int_bbox
        int_size = int_max - int_min
        print(f"\n  Interior bounding box:")
        print(f"    Min: ({int_min.x:.2f}, {int_min.y:.2f}, {int_min.z:.2f})")
        print(f"    Max: ({int_max.x:.2f}, {int_max.y:.2f}, {int_max.z:.2f})")
        print(f"    Size: ({int_size.x:.2f}, {int_size.y:.2f}, {int_size.z:.2f})")

    # --- Check 3b: Interior fits inside exterior ---
    checks = {}
    if ext_bbox and int_bbox:
        fits_x = int_min.x >= ext_min.x - 0.5 and int_max.x <= ext_max.x + 0.5
        fits_y = int_min.y >= ext_min.y - 0.5 and int_max.y <= ext_max.y + 0.5
        fits_z = int_min.z >= ext_min.z - 0.5 and int_max.z <= ext_max.z + 0.5
        fits = fits_x and fits_y and fits_z
        checks['interior_fits'] = fits
        print(f"\n  CHECK: Interior fits inside exterior: {'PASS' if fits else 'FAIL'}")
        if not fits:
            print(f"    X: {'OK' if fits_x else 'CLIPPING'} (int [{int_min.x:.2f},{int_max.x:.2f}] vs ext [{ext_min.x:.2f},{ext_max.x:.2f}])")
            print(f"    Y: {'OK' if fits_y else 'CLIPPING'} (int [{int_min.y:.2f},{int_max.y:.2f}] vs ext [{ext_min.y:.2f},{ext_max.y:.2f}])")
            print(f"    Z: {'OK' if fits_z else 'CLIPPING'} (int [{int_min.z:.2f},{int_max.z:.2f}] vs ext [{ext_min.z:.2f},{ext_max.z:.2f}])")

    # --- Check 3c: Origin alignment (both at same Z=0 plane relative to position) ---
    ext_z_min = ext_min.z if ext_bbox else 0
    int_z_min = int_min.z if int_bbox else 0
    z_aligned = abs(ext_z_min - int_z_min) < 0.5
    checks['origin_alignment'] = z_aligned
    print(f"\n  CHECK: Origin Z alignment: {'PASS' if z_aligned else 'FAIL'}")
    print(f"    Exterior Z min: {ext_z_min:.3f}, Interior Z min: {int_z_min:.3f}, Delta: {abs(ext_z_min - int_z_min):.3f}")

    # --- Check 3d: Scale match (1:1) ---
    if ext_bbox and int_bbox:
        # Interior should be smaller than exterior (it fits inside)
        scale_ok = (int_size.x < ext_size.x + 1 and int_size.y < ext_size.y + 1 and
                   int_size.z < ext_size.z + 1)
        # But not dramatically smaller (less than half would be suspicious)
        scale_ratio_x = int_size.x / ext_size.x if ext_size.x > 0 else 0
        scale_ratio_y = int_size.y / ext_size.y if ext_size.y > 0 else 0
        scale_ratio_z = int_size.z / ext_size.z if ext_size.z > 0 else 0
        reasonable = scale_ratio_x > 0.3 and scale_ratio_y > 0.3 and scale_ratio_z > 0.3
        checks['scale_match'] = scale_ok and reasonable
        print(f"\n  CHECK: Scale match: {'PASS' if (scale_ok and reasonable) else 'NEEDS REVIEW'}")
        print(f"    Ratio X: {scale_ratio_x:.2f}, Y: {scale_ratio_y:.2f}, Z: {scale_ratio_z:.2f}")
        print(f"    (Expected: interior ~0.8-0.95x of exterior)")

    # --- Check 3e: Open wall faces outward ---
    # The open/windowed wall should face toward the city (away from the exterior edge)
    # For Knowledgebase at (30, -20, 0), the front should generally face toward SIA Tower (origin)
    # Direction from KB to origin: (-30, 20, 0) -> roughly NW
    print(f"\n  CHECK: Open wall orientation:")
    print(f"    Knowledgebase position: (30, -20, 0)")
    print(f"    Direction to SIA Tower: (-30, 20, 0) = NW")
    # The front wall glass panel is the indicator
    glass_objects = [o for o in int_objects if 'glass' in o.name.lower() or 'front_wall' in o.name.lower()]
    if glass_objects:
        for go in glass_objects:
            print(f"    Glass/front wall object '{go.name}' at ({go.location.x:.2f}, {go.location.y:.2f}, {go.location.z:.2f})")
    # Need to determine which direction the interior faces based on the front wall Y position
    # In the interior build, front wall is at Y = -1.6 (negative Y = front/south)
    # After positioning at (30, -20, 0), front wall Y would be around -21.6
    checks['open_wall'] = "REVIEW - see notes"
    print(f"    Assessment: Interior's front (open) wall faces -Y direction (south)")
    print(f"    From KB position, -Y means further south, which faces away from SIA Tower")
    print(f"    RESULT: The front wall faces southward. This may need rotation to face toward SIA Tower.")

    # --- Check 3f: Light empties inside room volume ---
    print(f"\n  CHECK: Light empties:")
    light_empties = [e for e in empties if 'light' in e.name.lower()]
    camera_targets = [e for e in empties if 'camera' in e.name.lower()]

    for emp in light_empties:
        inside = True
        if int_bbox:
            inside = (int_min.x - 0.5 <= emp.location.x <= int_max.x + 0.5 and
                     int_min.y - 0.5 <= emp.location.y <= int_max.y + 0.5 and
                     int_min.z - 0.5 <= emp.location.z <= int_max.z + 0.5)
        status = "INSIDE" if inside else "OUTSIDE"
        print(f"    {emp.name}: ({emp.location.x:.2f}, {emp.location.y:.2f}, {emp.location.z:.2f}) - {status}")
    checks['light_empties'] = len(light_empties) >= 3

    # --- Check 3g: camera_target inside room ---
    for ct in camera_targets:
        inside = True
        if int_bbox:
            inside = (int_min.x - 0.5 <= ct.location.x <= int_max.x + 0.5 and
                     int_min.y - 0.5 <= ct.location.y <= int_max.y + 0.5 and
                     int_min.z - 0.5 <= ct.location.z <= int_max.z + 0.5)
        status = "INSIDE" if inside else "OUTSIDE"
        print(f"    {ct.name}: ({ct.location.x:.2f}, {ct.location.y:.2f}, {ct.location.z:.2f}) - {status}")
    checks['camera_target'] = len(camera_targets) >= 1

    # --- Check 3h: Apply all transforms ---
    print(f"\n  CHECK: Transform application:")
    non_identity = 0
    for obj in kb_objects:
        if obj.type == 'MESH':
            # After repositioning, location will not be identity
            # But rotation and scale should be identity
            rot = obj.rotation_euler
            scl = obj.scale
            rot_ok = (abs(rot.x) < 0.01 and abs(rot.y) < 0.01 and abs(rot.z) < 0.01)
            scl_ok = (abs(scl.x - 1) < 0.01 and abs(scl.y - 1) < 0.01 and abs(scl.z - 1) < 0.01)
            if not rot_ok or not scl_ok:
                non_identity += 1
                if non_identity <= 5:  # Only print first 5
                    print(f"    Non-identity transform: {obj.name} rot=({rot.x:.3f},{rot.y:.3f},{rot.z:.3f}) scale=({scl.x:.3f},{scl.y:.3f},{scl.z:.3f})")
    checks['transforms'] = non_identity == 0
    print(f"    Objects with non-identity rotation/scale: {non_identity}")
    print(f"    RESULT: {'PASS' if non_identity == 0 else 'REVIEW - ' + str(non_identity) + ' objects have non-identity transforms'}")

    # Print summary
    print(f"\n  ALIGNMENT SUMMARY:")
    for k, v in checks.items():
        print(f"    {k}: {v}")

# ===========================================================================
# STEP 4 — Scene 7 Camera: "Knowledgebase — Descend into grand library cathedral"
# ===========================================================================
print("\n" + "=" * 60)
print("STEP 4: Scene 7 Camera Setup")
print("=" * 60)

# Position camera above and to one side, looking downward toward Knowledgebase
# KB is at (30, -20, 0). Camera above-left, descending angle.
cam_data = bpy.data.cameras.new(name="Scene7_Camera")
cam_data.lens = 35  # Slightly wide for drama
cam_data.clip_start = 0.1
cam_data.clip_end = 300
cam_obj = bpy.data.objects.new("Scene7_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)

# Camera position: above and to the northwest of the KB, looking down
# This creates a "descending into" perspective
cam_pos = Vector((22, -12, 18))  # Above and NW of KB (closer to SIA Tower side)
cam_obj.location = cam_pos

# Target: the center of the Knowledgebase structure at mid-height
kb_target = Vector((30, -20, 5))  # Mid-height of the building

# Calculate rotation to look at target
direction = kb_target - cam_pos
cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

bpy.context.scene.camera = cam_obj
print(f"  Camera position: ({cam_pos.x:.1f}, {cam_pos.y:.1f}, {cam_pos.z:.1f})")
print(f"  Camera target: ({kb_target.x:.1f}, {kb_target.y:.1f}, {kb_target.z:.1f})")
print(f"  Lens: {cam_data.lens}mm")

# ===========================================================================
# STEP 5 — Render screenshots
# ===========================================================================
print("\n" + "=" * 60)
print("STEP 5: Rendering Screenshots")
print("=" * 60)

# Setup render settings for screenshots
scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

# Try EEVEE for speed
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
except:
    try:
        scene.render.engine = 'BLENDER_EEVEE'
    except:
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 64

# Screenshot 1: Scene 7 camera (Knowledgebase descent)
scene.camera = cam_obj
scene.render.filepath = f"{SCREENSHOTS}/s20-scene7-descent.png"
bpy.ops.render.render(write_still=True)
print(f"  Rendered: s20-scene7-descent.png")

# Screenshot 2: Wide-angle skyline (all 5 structures)
wide_cam_data = bpy.data.cameras.new(name="Wide_Camera")
wide_cam_data.lens = 18  # Wide angle for skyline
wide_cam_data.clip_start = 0.1
wide_cam_data.clip_end = 400
wide_cam_obj = bpy.data.objects.new("Wide_Camera", wide_cam_data)
bpy.context.collection.objects.link(wide_cam_obj)

# Position: high above and to the south, looking north to see all structures
wide_cam_obj.location = Vector((15, -45, 35))
wide_target = Vector((15, 5, 5))  # Center of the cluster
direction = wide_target - wide_cam_obj.location
wide_cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

scene.camera = wide_cam_obj
scene.render.filepath = f"{SCREENSHOTS}/s20-skyline-all5.png"
bpy.ops.render.render(write_still=True)
print(f"  Rendered: s20-skyline-all5.png")

# Screenshot 3: KB best angle (three-quarter view)
kb_cam_data = bpy.data.cameras.new(name="KB_Best_Camera")
kb_cam_data.lens = 50
kb_cam_data.clip_start = 0.1
kb_cam_data.clip_end = 200
kb_cam_obj = bpy.data.objects.new("KB_Best_Camera", kb_cam_data)
bpy.context.collection.objects.link(kb_cam_obj)

# Three-quarter view of KB
kb_cam_obj.location = Vector((22, -28, 8))
kb_target2 = Vector((30, -20, 5))
direction = kb_target2 - kb_cam_obj.location
kb_cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

scene.camera = kb_cam_obj
scene.render.filepath = f"{SCREENSHOTS}/s20-kb-threequarter.png"
bpy.ops.render.render(write_still=True)
print(f"  Rendered: s20-kb-threequarter.png")

# Screenshot 4: Close-up of KB from front
kb_front_data = bpy.data.cameras.new(name="KB_Front_Camera")
kb_front_data.lens = 50
kb_front_data.clip_start = 0.1
kb_front_data.clip_end = 200
kb_front_obj = bpy.data.objects.new("KB_Front_Camera", kb_front_data)
bpy.context.collection.objects.link(kb_front_obj)

kb_front_obj.location = Vector((30, -30, 5))
kb_front_target = Vector((30, -20, 5))
direction = kb_front_target - kb_front_obj.location
kb_front_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

scene.camera = kb_front_obj
scene.render.filepath = f"{SCREENSHOTS}/s20-kb-front.png"
bpy.ops.render.render(write_still=True)
print(f"  Rendered: s20-kb-front.png")

# ===========================================================================
# STEP 5b — Individual structure best-angle shots for cohesion comparison
# ===========================================================================
structure_cam_positions = {
    "SIA_Tower": {"pos": (-8, -10, 20), "target": (0, 0, 15), "lens": 35},
    "Fitness": {"pos": (17, 17, 10), "target": (25, 25, 5), "lens": 50},
    "Yoga": {"pos": (27, 2, 8), "target": (35, 10, 5), "lens": 50},
    "Finance": {"pos": (27, -13, 8), "target": (35, -5, 5), "lens": 50},
}

for struct_name, cam_cfg in structure_cam_positions.items():
    s_cam_data = bpy.data.cameras.new(name=f"{struct_name}_Cam")
    s_cam_data.lens = cam_cfg["lens"]
    s_cam_data.clip_start = 0.1
    s_cam_data.clip_end = 200
    s_cam_obj = bpy.data.objects.new(f"{struct_name}_Cam", s_cam_data)
    bpy.context.collection.objects.link(s_cam_obj)
    s_cam_obj.location = Vector(cam_cfg["pos"])
    s_target = Vector(cam_cfg["target"])
    direction = s_target - s_cam_obj.location
    s_cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    scene.camera = s_cam_obj
    fname = f"s20-cohesion-{struct_name.lower().replace('_', '-')}.png"
    scene.render.filepath = f"{SCREENSHOTS}/{fname}"
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {fname}")

# ===========================================================================
# FINAL — Print scene summary for report
# ===========================================================================
print("\n" + "=" * 60)
print("SCENE SUMMARY")
print("=" * 60)
for col in bpy.data.collections:
    mesh_count = len([o for o in col.objects if o.type == 'MESH'])
    empty_count = len([o for o in col.objects if o.type == 'EMPTY'])
    if mesh_count > 0 or empty_count > 0:
        print(f"  {col.name}: {mesh_count} meshes, {empty_count} empties")

# Get all structure bounding boxes for scale comparison
print("\nStructure scales (bounding box sizes):")
for struct_name in ["SIA_Tower", "Fitness", "Yoga", "Finance", "Knowledgebase"]:
    col = bpy.data.collections.get(struct_name)
    if col:
        meshes = [o for o in col.objects if o.type == 'MESH']
        if meshes:
            all_mins = []
            all_maxs = []
            for obj in meshes:
                if hasattr(obj, 'bound_box'):
                    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
                    all_mins.append(Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners))))
                    all_maxs.append(Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners))))
            if all_mins:
                mn = Vector((min(m.x for m in all_mins), min(m.y for m in all_mins), min(m.z for m in all_mins)))
                mx = Vector((max(m.x for m in all_maxs), max(m.y for m in all_maxs), max(m.z for m in all_maxs)))
                sz = mx - mn
                height = sz.z
                print(f"  {struct_name}: size=({sz.x:.1f}, {sz.y:.1f}, {sz.z:.1f}), height={height:.1f}u")

print("\nIntegration script complete.")

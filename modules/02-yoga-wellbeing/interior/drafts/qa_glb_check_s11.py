"""
QA GLB Export Check -- verify what's inside the exported GLB.
Opens the GLB in a fresh Blender scene to count what's exported.
"""
import bpy
import json

# Clear scene completely
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the GLB
bpy.ops.import_scene.gltf(
    filepath='/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/interior/drafts/yoga-int-draft-s11.glb'
)

all_objects = list(bpy.data.objects)
mesh_objects = [o for o in all_objects if o.type == 'MESH']
empty_objects = [o for o in all_objects if o.type == 'EMPTY']
camera_objects = [o for o in all_objects if o.type == 'CAMERA']
light_objects = [o for o in all_objects if o.type == 'LIGHT']
armature_objects = [o for o in all_objects if o.type == 'ARMATURE']
other_objects = [o for o in all_objects if o.type not in ('MESH', 'EMPTY', 'CAMERA', 'LIGHT', 'ARMATURE')]

# Count tris in imported GLB
total_tris = 0
mat_tris = {}
for obj in mesh_objects:
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    eval_mesh = eval_obj.to_mesh()
    tri_count = sum(len(p.vertices) - 2 for p in eval_mesh.polygons)
    total_tris += tri_count
    for slot in obj.material_slots:
        mat_name = slot.material.name if slot.material else 'NONE'
        mat_tris[mat_name] = mat_tris.get(mat_name, 0) + tri_count
    eval_obj.to_mesh_clear()

# Material names in GLB
glb_materials = [m.name for m in bpy.data.materials]

# Empties
empties_info = []
for obj in empty_objects:
    empties_info.append({
        'name': obj.name,
        'location': [round(c, 3) for c in obj.location],
    })

results = {
    'glb_total_objects': len(all_objects),
    'glb_mesh_count': len(mesh_objects),
    'glb_empty_count': len(empty_objects),
    'glb_camera_count': len(camera_objects),
    'glb_light_count': len(light_objects),
    'glb_armature_count': len(armature_objects),
    'glb_other_count': len(other_objects),
    'glb_total_tris': total_tris,
    'glb_materials': glb_materials,
    'glb_material_tris': mat_tris,
    'glb_empties': empties_info,
    'glb_cameras_names': [c.name for c in camera_objects],
    'glb_lights_names': [l.name for l in light_objects],
}

print("=" * 80)
print("GLB IMPORT AUDIT")
print("=" * 80)
print(json.dumps(results, indent=2))
print("=" * 80)

"""
QA Audit Script for Yoga & Wellbeing Interior (Session 11)
Gates 3, 4, 5, 7 -- Independent verification
Run headless: blender -b yoga-interior-s11.blend -P qa_audit_s11.py
"""
import bpy
import json
import math
import sys

results = {}

# ============================================================
# 1. SCENE OVERVIEW
# ============================================================
scene = bpy.context.scene
all_objects = list(bpy.data.objects)

mesh_objects = [o for o in all_objects if o.type == 'MESH']
empty_objects = [o for o in all_objects if o.type == 'EMPTY']
camera_objects = [o for o in all_objects if o.type == 'CAMERA']
light_objects = [o for o in all_objects if o.type == 'LIGHT']
other_objects = [o for o in all_objects if o.type not in ('MESH', 'EMPTY', 'CAMERA', 'LIGHT')]

results['scene_overview'] = {
    'total_objects': len(all_objects),
    'mesh_count': len(mesh_objects),
    'empty_count': len(empty_objects),
    'camera_count': len(camera_objects),
    'light_count': len(light_objects),
    'other_count': len(other_objects),
    'other_types': [f"{o.name} ({o.type})" for o in other_objects],
}

# ============================================================
# 2. TRI COUNT AUDIT (per object + per material)
# ============================================================
total_tris = 0
per_object = []
material_tris = {}
objects_no_material = []
objects_multi_material = []
generic_names = []

for obj in mesh_objects:
    mesh = obj.data
    # Ensure mesh is evaluated with modifiers
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    eval_mesh = eval_obj.to_mesh()

    # Calculate triangulated face count
    tri_count = 0
    for poly in eval_mesh.polygons:
        # Each polygon with N vertices produces N-2 triangles
        tri_count += len(poly.vertices) - 2

    total_tris += tri_count
    per_object.append({
        'name': obj.name,
        'tris': tri_count,
        'verts': len(eval_mesh.vertices),
        'material_slots': len(obj.material_slots),
        'materials': [slot.material.name if slot.material else 'NONE' for slot in obj.material_slots],
    })

    # Check for generic names
    for bad in ['Cube', 'Sphere', 'Cylinder', 'Cone', 'Torus', 'Plane', 'Circle', 'Mesh']:
        if obj.name.startswith(bad) and (obj.name == bad or obj.name[len(bad):].startswith('.')):
            generic_names.append(obj.name)

    # Material assignment checks
    if len(obj.material_slots) == 0:
        objects_no_material.append(obj.name)
    elif len(obj.material_slots) > 1:
        objects_multi_material.append(obj.name)

    # Per-material tri accumulation
    if obj.material_slots:
        for slot in obj.material_slots:
            mat_name = slot.material.name if slot.material else 'NONE'
            if mat_name not in material_tris:
                material_tris[mat_name] = 0
            material_tris[mat_name] += tri_count
    else:
        if 'UNASSIGNED' not in material_tris:
            material_tris['UNASSIGNED'] = 0
        material_tris['UNASSIGNED'] += tri_count

    eval_obj.to_mesh_clear()

# Per-material tri distribution (using per-face material assignment for multi-mat objects)
# Since we already counted per-object and most objects have single material, this is accurate
# for single-material objects. For multi-material objects, we'd need per-face analysis.

results['tri_audit'] = {
    'total_tris': total_tris,
    'budget_min': 5000,
    'budget_max': 10000,
    'within_budget': 5000 <= total_tris <= 10000,
    'objects_no_material': objects_no_material,
    'objects_multi_material': objects_multi_material,
    'generic_names': generic_names,
}

# Sort objects by tris descending
per_object.sort(key=lambda x: x['tris'], reverse=True)
results['per_object_top30'] = per_object[:30]

# ============================================================
# 3. MATERIAL SYSTEM AUDIT
# ============================================================
VALID_SLOTS = {'base', 'accent', 'glass', 'detail', 'emissive', 'energy', 'holo'}
SPEC_RANGES = {
    'base':     (50, 55),
    'accent':   (10, 15),
    'glass':    (10, 18),
    'detail':   (12, 18),
    'emissive': (3, 8),
    'energy':   (0, 5),
    'holo':     (0, 5),
}

all_materials = list(bpy.data.materials)
mat_names = [m.name for m in all_materials]
invalid_names = [n for n in mat_names if n not in VALID_SLOTS and n != 'Dots Stroke']
unused_slots = VALID_SLOTS - set(mat_names)

# Material distribution
mat_distribution = {}
for slot in VALID_SLOTS:
    tris = material_tris.get(slot, 0)
    pct = (tris / total_tris * 100) if total_tris > 0 else 0
    lo, hi = SPEC_RANGES[slot]
    if pct < lo:
        status = f"BELOW (-{lo - pct:.1f}pp)"
    elif pct > hi:
        status = f"ABOVE (+{pct - hi:.1f}pp)"
    else:
        status = "IN SPEC"
    mat_distribution[slot] = {
        'tris': tris,
        'pct': round(pct, 1),
        'spec_range': f"{lo}-{hi}%",
        'status': status,
    }

results['material_audit'] = {
    'total_materials': len(all_materials),
    'material_names': mat_names,
    'invalid_names': invalid_names,
    'missing_slots': list(unused_slots),
    'distribution': mat_distribution,
}

# ============================================================
# 4. MATERIAL PROPERTIES AUDIT (Dark-First Test)
# ============================================================
mat_properties = {}
for mat in all_materials:
    if mat.name == 'Dots Stroke':
        continue
    if not mat.use_nodes:
        mat_properties[mat.name] = {'error': 'no node tree'}
        continue

    bsdf = None
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            bsdf = node
            break

    if not bsdf:
        mat_properties[mat.name] = {'error': 'no Principled BSDF found'}
        continue

    base_color = list(bsdf.inputs['Base Color'].default_value)
    emission_color = list(bsdf.inputs['Emission Color'].default_value)
    emission_strength = bsdf.inputs['Emission Strength'].default_value
    metallic = bsdf.inputs['Metallic'].default_value
    roughness = bsdf.inputs['Roughness'].default_value
    alpha = bsdf.inputs['Alpha'].default_value

    # Check if sage (#6EE7B7 = 0.431, 0.906, 0.718 in linear sRGB approx)
    # In linear: approx (0.153, 0.797, 0.475)
    sage_in_base = False
    r, g, b = base_color[0], base_color[1], base_color[2]
    # Sage detection: green channel significantly higher than red, with noticeable blue
    if g > 0.1 and g > r * 2 and b > 0.05 and b < g:
        sage_in_base = True

    mat_properties[mat.name] = {
        'base_color': [round(c, 4) for c in base_color[:3]],
        'emission_color': [round(c, 4) for c in emission_color[:3]],
        'emission_strength': round(emission_strength, 4),
        'metallic': round(metallic, 4),
        'roughness': round(roughness, 4),
        'alpha': round(alpha, 4),
        'sage_in_base_color': sage_in_base,
        'base_is_dark': all(c < 0.05 for c in base_color[:3]),
    }

results['material_properties'] = mat_properties

# ============================================================
# 5. TRANSFORM & ORIGIN AUDIT
# ============================================================
unapplied_transforms = []
for obj in mesh_objects:
    s = obj.scale
    r = obj.rotation_euler
    if not (abs(s.x - 1.0) < 0.001 and abs(s.y - 1.0) < 0.001 and abs(s.z - 1.0) < 0.001):
        unapplied_transforms.append({'name': obj.name, 'issue': 'scale', 'value': list(s)})
    if not (abs(r.x) < 0.001 and abs(r.y) < 0.001 and abs(r.z) < 0.001):
        unapplied_transforms.append({'name': obj.name, 'issue': 'rotation', 'value': [math.degrees(a) for a in r]})

# Bounding box of all mesh geometry
min_x = min_y = min_z = float('inf')
max_x = max_y = max_z = float('-inf')
for obj in mesh_objects:
    for corner in obj.bound_box:
        world_corner = obj.matrix_world @ bpy.mathutils.Vector(corner) if hasattr(bpy, 'mathutils') else None
        if world_corner is None:
            import mathutils
            world_corner = obj.matrix_world @ mathutils.Vector(corner)
        min_x = min(min_x, world_corner.x)
        min_y = min(min_y, world_corner.y)
        min_z = min(min_z, world_corner.z)
        max_x = max(max_x, world_corner.x)
        max_y = max(max_y, world_corner.y)
        max_z = max(max_z, world_corner.z)

results['transform_audit'] = {
    'unapplied_count': len(unapplied_transforms),
    'unapplied_details': unapplied_transforms[:20],
    'bounding_box': {
        'min': [round(min_x, 3), round(min_y, 3), round(min_z, 3)],
        'max': [round(max_x, 3), round(max_y, 3), round(max_z, 3)],
        'size': [round(max_x - min_x, 3), round(max_y - min_y, 3), round(max_z - min_z, 3)],
    },
    'origin_at_bottom_center': min_z <= 0.01 and abs((min_x + max_x) / 2) < 0.5 and abs((min_y + max_y) / 2) < 0.5,
}

# ============================================================
# 6. EMPTIES AUDIT
# ============================================================
empties_data = []
for obj in empty_objects:
    empties_data.append({
        'name': obj.name,
        'location': [round(c, 3) for c in obj.location],
        'type': obj.empty_display_type,
    })

required_empties = ['light_0', 'light_1', 'light_2', 'camera_target']
found_empties = {e['name'] for e in empties_data}
missing_empties = [n for n in required_empties if n not in found_empties]
extra_empties = [e for e in empties_data if e['name'] not in required_empties]

results['empties_audit'] = {
    'empties': empties_data,
    'required': required_empties,
    'missing': missing_empties,
    'extra': [e['name'] for e in extra_empties],
}

# ============================================================
# 7. CAMERAS AND LIGHTS IN SCENE
# ============================================================
results['cameras_lights'] = {
    'cameras': [c.name for c in camera_objects],
    'lights': [l.name for l in light_objects],
    'cameras_count': len(camera_objects),
    'lights_count': len(light_objects),
}

# ============================================================
# 8. OBJECT INVENTORY (full list for completeness)
# ============================================================
results['full_object_list'] = [
    {'name': o['name'], 'tris': o['tris'], 'material': o['materials'][0] if o['materials'] else 'NONE'}
    for o in per_object
]

# ============================================================
# OUTPUT
# ============================================================
print("=" * 80)
print("QA AUDIT RESULTS -- YOGA INTERIOR S11")
print("=" * 80)
print(json.dumps(results, indent=2))
print("=" * 80)

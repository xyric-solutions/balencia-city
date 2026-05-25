"""
Finance Tower (Module #03) — Major Forms
35-floor crystalline monolith with faceted gemstone silhouette.
Height target: ~14 units (35 floors, based on SIA Tower scale of ~40u for 100+ floors).
"""
import bpy
import bmesh
import math
from mathutils import Vector, Matrix

# Retrieve materials
mat_base = bpy.data.materials.get("base")
mat_accent = bpy.data.materials.get("accent")
mat_glass = bpy.data.materials.get("glass")
mat_detail = bpy.data.materials.get("detail")
mat_emissive = bpy.data.materials.get("emissive")
mat_energy = bpy.data.materials.get("energy")

def assign_mat(obj, mat):
    """Assign material to object."""
    if mat:
        obj.data.materials.append(mat)


# ============================================================
# ELEMENT 1: Faceted Crystalline Main Body
# 35 floors, ~14u tall, 8-10 major facet faces
# Wide octagonal base tapering to narrower crown
# ============================================================

def create_faceted_body():
    """Create the main crystalline body as a faceted tapered form."""

    # We build this as a custom mesh: a series of octagonal cross-sections
    # at different heights, each rotated/scaled slightly to create faceted effect.

    bm = bmesh.new()

    # Parameters
    total_height = 14.0
    num_sections = 8  # number of cross-section levels
    base_radius = 4.0  # wide stable base (widest in city)
    top_radius = 2.8   # narrower crown
    sides = 8          # octagonal cross-section

    # Define cross-section heights, radii, and rotation offsets
    # Each section has (height_fraction, radius_fraction, rotation_offset_degrees)
    sections = [
        (0.00, 1.00, 0),      # Ground level - full width
        (0.05, 1.02, 0),      # Slight outward flare at base
        (0.12, 0.95, 3),      # First taper
        (0.28, 0.88, -2),     # Second taper
        (0.45, 0.82, 4),      # Mid section
        (0.62, 0.76, -3),     # Upper mid
        (0.80, 0.72, 2),      # Near crown
        (0.92, 0.70, -1),     # Crown transition
        (1.00, 0.68, 0),      # Top
    ]

    all_verts = []

    for i, (h_frac, r_frac, rot_offset) in enumerate(sections):
        height = h_frac * total_height
        radius = base_radius * r_frac
        # Add slight per-vertex radial variation for faceted look
        rot = math.radians(rot_offset)

        section_verts = []
        for j in range(sides):
            angle = (2 * math.pi * j / sides) + rot
            # Per-vertex radius variation for crystalline faceting
            r_var = radius * (1.0 + 0.06 * math.sin(angle * 3 + i * 0.7))
            x = r_var * math.cos(angle)
            y = r_var * math.sin(angle)
            v = bm.verts.new((x, y, height))
            section_verts.append(v)
        all_verts.append(section_verts)

    bm.verts.ensure_lookup_table()

    # Create faces between adjacent sections
    for i in range(len(all_verts) - 1):
        lower = all_verts[i]
        upper = all_verts[i + 1]
        for j in range(sides):
            j_next = (j + 1) % sides
            # Quad face between sections
            bm.faces.new([lower[j], lower[j_next], upper[j_next], upper[j]])

    # Cap the top
    top_verts = all_verts[-1]
    bm.faces.new(top_verts)

    # Cap the bottom
    bottom_verts = list(reversed(all_verts[0]))
    bm.faces.new(bottom_verts)

    # Create mesh
    mesh = bpy.data.meshes.new("main_body_mesh")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("main_body", mesh)
    bpy.context.collection.objects.link(obj)

    # Assign glass material (crystalline faceted surfaces)
    assign_mat(obj, mat_glass)

    # Shade flat to preserve faceted look
    for poly in obj.data.polygons:
        poly.use_smooth = False

    print(f"main_body: {len(obj.data.polygons)} faces, {len(obj.data.vertices)} verts")
    return obj


body = create_faceted_body()


# ============================================================
# ELEMENT 2: Wide Stable Base / Ground Platform
# Stepped hexagonal platform at street level
# ============================================================

def create_base_platform():
    """Create the wide stepped base that transitions from ground to tower."""

    # Lower platform — very wide octagonal pad
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=5.5, depth=0.6,
        location=(0, 0, 0.3)
    )
    platform_lower = bpy.context.active_object
    platform_lower.name = "base_platform_lower"
    assign_mat(platform_lower, mat_base)
    for poly in platform_lower.data.polygons:
        poly.use_smooth = False

    # Upper platform — slightly narrower, sits on top
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=4.8, depth=0.4,
        location=(0, 0, 0.8)
    )
    platform_upper = bpy.context.active_object
    platform_upper.name = "base_platform_upper"
    assign_mat(platform_upper, mat_base)
    for poly in platform_upper.data.polygons:
        poly.use_smooth = False

    # Step ring between platforms — accent material
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=5.0, depth=0.08,
        location=(0, 0, 0.64)
    )
    step_ring = bpy.context.active_object
    step_ring.name = "base_step_ring"
    assign_mat(step_ring, mat_emissive)
    for poly in step_ring.data.polygons:
        poly.use_smooth = False

    print("Base platform created (3 objects)")
    return platform_lower, platform_upper, step_ring


base_objects = create_base_platform()

# Raise main body to sit on top of base
body.location.z = 1.0


# ============================================================
# ELEMENT 3: Gold Accent Edge Lines (Facet Junction Wireframe)
# Emissive gold lines tracing every major facet edge
# ============================================================

def create_edge_accents():
    """Create gold wireframe lines along the major facet edges of the body."""

    edges = []
    total_height = 14.0
    base_radius = 4.0
    sides = 8

    # Same section parameters as main body, offset up by 1.0 for base
    sections = [
        (0.00, 1.00, 0),
        (0.05, 1.02, 0),
        (0.12, 0.95, 3),
        (0.28, 0.88, -2),
        (0.45, 0.82, 4),
        (0.62, 0.76, -3),
        (0.80, 0.72, 2),
        (0.92, 0.70, -1),
        (1.00, 0.68, 0),
    ]
    z_offset = 1.0  # base height offset

    edge_objects = []

    # Vertical edge lines (one per octagonal vertex, running up the tower)
    for j in range(sides):
        bm = bmesh.new()
        verts = []
        for i, (h_frac, r_frac, rot_offset) in enumerate(sections):
            height = h_frac * total_height + z_offset
            radius = base_radius * r_frac
            rot = math.radians(rot_offset)
            angle = (2 * math.pi * j / sides) + rot
            r_var = radius * (1.0 + 0.06 * math.sin(angle * 3 + i * 0.7))
            x = r_var * math.cos(angle)
            y = r_var * math.sin(angle)
            v = bm.verts.new((x, y, height))
            verts.append(v)

        for k in range(len(verts) - 1):
            bm.edges.new([verts[k], verts[k+1]])

        mesh = bpy.data.meshes.new(f"edge_vert_{j}_mesh")
        bm.to_mesh(mesh)
        bm.free()

        obj = bpy.data.objects.new(f"edge_vert_{j}", mesh)
        bpy.context.collection.objects.link(obj)

        # Convert to curve for thickness, then back to mesh for export
        # Instead, use solidify modifier on the edge mesh
        # Actually, let's create thin cylinder segments for each edge
        edge_objects.append(obj)

    # Horizontal ring lines (one per section)
    for i, (h_frac, r_frac, rot_offset) in enumerate(sections):
        height = h_frac * total_height + z_offset
        radius = base_radius * r_frac
        rot = math.radians(rot_offset)

        bm = bmesh.new()
        ring_verts = []
        for j in range(sides):
            angle = (2 * math.pi * j / sides) + rot
            r_var = radius * (1.0 + 0.06 * math.sin(angle * 3 + i * 0.7))
            x = r_var * math.cos(angle)
            y = r_var * math.sin(angle)
            v = bm.verts.new((x, y, height))
            ring_verts.append(v)

        for j in range(sides):
            bm.edges.new([ring_verts[j], ring_verts[(j+1) % sides]])

        mesh = bpy.data.meshes.new(f"edge_ring_{i}_mesh")
        bm.to_mesh(mesh)
        bm.free()

        obj = bpy.data.objects.new(f"edge_ring_{i}", mesh)
        bpy.context.collection.objects.link(obj)
        edge_objects.append(obj)

    # Give all edge objects thickness via a skin modifier or solidify
    # We'll use the skin modifier approach for thin tubes
    for obj in edge_objects:
        bpy.context.view_layer.objects.active = obj

        # Add skin modifier for tube-like wireframe
        skin_mod = obj.modifiers.new("Skin", type='SKIN')

        # Set skin radius for all vertices (thin gold wire)
        for v in obj.data.vertices:
            # Access skin data
            pass

        # Actually, let's use a simpler approach: convert to curve, set bevel
        # Remove skin modifier
        obj.modifiers.remove(skin_mod)

    # Better approach: use curves with bevel for clean wireframe tubes
    # Remove the edge mesh objects and recreate as curves
    for obj in edge_objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    edge_objects = []

    # Recreate as curves with bevel depth
    # Vertical edge curves
    for j in range(sides):
        curve_data = bpy.data.curves.new(f"edge_vert_{j}_curve", 'CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = 0.04  # thin gold wire
        curve_data.bevel_resolution = 2

        spline = curve_data.splines.new('POLY')
        spline.points.add(len(sections) - 1)

        for i, (h_frac, r_frac, rot_offset) in enumerate(sections):
            height = h_frac * total_height + z_offset
            radius = base_radius * r_frac
            rot = math.radians(rot_offset)
            angle = (2 * math.pi * j / sides) + rot
            r_var = radius * (1.0 + 0.06 * math.sin(angle * 3 + i * 0.7))
            x = r_var * math.cos(angle)
            y = r_var * math.sin(angle)
            spline.points[i].co = (x, y, height, 1.0)

        obj = bpy.data.objects.new(f"edge_vert_{j}", curve_data)
        bpy.context.collection.objects.link(obj)
        assign_mat(obj, mat_emissive)
        edge_objects.append(obj)

    # Horizontal ring curves
    for i, (h_frac, r_frac, rot_offset) in enumerate(sections):
        height = h_frac * total_height + z_offset
        radius = base_radius * r_frac
        rot = math.radians(rot_offset)

        curve_data = bpy.data.curves.new(f"edge_ring_{i}_curve", 'CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = 0.04
        curve_data.bevel_resolution = 2

        spline = curve_data.splines.new('POLY')
        spline.points.add(sides)  # +1 to close the loop

        for j in range(sides):
            angle = (2 * math.pi * j / sides) + rot
            r_var = radius * (1.0 + 0.06 * math.sin(angle * 3 + i * 0.7))
            x = r_var * math.cos(angle)
            y = r_var * math.sin(angle)
            spline.points[j].co = (x, y, height, 1.0)

        # Close the loop
        angle_close = rot  # same as j=0
        r_var_close = radius * (1.0 + 0.06 * math.sin(angle_close * 3 + i * 0.7))
        spline.points[sides].co = (
            r_var_close * math.cos(angle_close),
            r_var_close * math.sin(angle_close),
            height, 1.0
        )
        spline.use_cyclic_u = True

        obj = bpy.data.objects.new(f"edge_ring_{i}", curve_data)
        bpy.context.collection.objects.link(obj)
        assign_mat(obj, mat_emissive)
        edge_objects.append(obj)

    print(f"Gold edge accents: {len(edge_objects)} curves ({sides} vertical + {len(sections)} horizontal)")
    return edge_objects


edge_accents = create_edge_accents()


# ============================================================
# ELEMENT 4: Crown Financial Data Display
# Ring of illuminated panels at top 2 floors
# ============================================================

def create_crown():
    """Create the crown data display ring at the top of the tower."""
    crown_z = 14.0 + 1.0  # main body top + base offset
    crown_radius = 4.0 * 0.68  # same as top section radius
    panel_count = 8

    crown_objects = []

    # Data display panels — thin rectangular panels arranged in octagonal ring
    for i in range(panel_count):
        angle = 2 * math.pi * i / panel_count

        # Panel position (slightly outside the main body silhouette)
        px = (crown_radius + 0.15) * math.cos(angle)
        py = (crown_radius + 0.15) * math.sin(angle)
        pz = crown_z - 0.7  # centered on top 2 floors

        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(px, py, pz),
            scale=(0.12, 1.4, 0.9)
        )
        panel = bpy.context.active_object
        panel.name = f"crown_panel_{i}"
        panel.rotation_euler.z = angle + math.pi/2
        assign_mat(panel, mat_accent)

        for poly in panel.data.polygons:
            poly.use_smooth = False

        crown_objects.append(panel)

    # Crown cap — flat octagonal top plate (slightly wider than body top)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=crown_radius + 0.3, depth=0.15,
        location=(0, 0, crown_z + 0.1)
    )
    crown_cap = bpy.context.active_object
    crown_cap.name = "crown_cap"
    assign_mat(crown_cap, mat_detail)
    for poly in crown_cap.data.polygons:
        poly.use_smooth = False
    crown_objects.append(crown_cap)

    # Crown edge accent ring
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=crown_radius + 0.35, depth=0.06,
        location=(0, 0, crown_z + 0.18)
    )
    crown_edge = bpy.context.active_object
    crown_edge.name = "crown_edge_ring"
    assign_mat(crown_edge, mat_emissive)
    for poly in crown_edge.data.polygons:
        poly.use_smooth = False
    crown_objects.append(crown_edge)

    print(f"Crown: {len(crown_objects)} objects ({panel_count} panels + cap + edge ring)")
    return crown_objects


crown = create_crown()


# ============================================================
# ELEMENT 5: Recessed Window Clusters
# Large plate glass windows recessed into faceted faces
# 1-2 per face, arranged in vertical clusters (floor groupings)
# ============================================================

def create_windows():
    """Create recessed window panels on the main body faces."""

    total_height = 14.0
    base_radius = 4.0
    sides = 8
    z_offset = 1.0

    # Window clusters: groups of floors with recessed windows
    # Each cluster is a thin recessed panel on a face
    window_objects = []

    # Floor clusters (3 vertical zones)
    clusters = [
        (0.10, 0.35, 0.95),  # lower third (height start, height end, radius fraction avg)
        (0.38, 0.58, 0.85),  # middle third
        (0.62, 0.85, 0.74),  # upper third
    ]

    for cluster_idx, (h_start, h_end, r_frac) in enumerate(clusters):
        z_start = h_start * total_height + z_offset
        z_end = h_end * total_height + z_offset
        z_mid = (z_start + z_end) / 2
        z_height = z_end - z_start
        radius = base_radius * r_frac

        # Place windows on alternating faces (4 out of 8)
        for face_idx in range(0, sides, 2):
            angle = 2 * math.pi * face_idx / sides

            # Position window slightly inset from face surface
            wx = (radius - 0.15) * math.cos(angle)
            wy = (radius - 0.15) * math.sin(angle)

            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(wx, wy, z_mid),
                scale=(0.06, 1.2, z_height * 0.85)
            )
            window = bpy.context.active_object
            window.name = f"window_c{cluster_idx}_f{face_idx}"
            window.rotation_euler.z = angle + math.pi/2
            assign_mat(window, mat_glass)

            for poly in window.data.polygons:
                poly.use_smooth = False

            window_objects.append(window)

    print(f"Windows: {len(window_objects)} recessed panels")
    return window_objects


windows = create_windows()


# ============================================================
# ELEMENT 6: Reinforced Geometric Entry
# Heavy angular frame at street level with gold-lit edges
# ============================================================

def create_entry():
    """Create the reinforced geometric entry portal."""

    entry_width = 2.4
    entry_height = 2.8
    entry_depth = 1.2

    # Main entry frame — thick angular doorway
    # Left pillar
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-entry_width/2 - 0.2, -4.2, entry_height/2 + 1.0),
        scale=(0.35, entry_depth/2, entry_height/2)
    )
    left_pillar = bpy.context.active_object
    left_pillar.name = "entry_pillar_left"
    assign_mat(left_pillar, mat_detail)
    for poly in left_pillar.data.polygons:
        poly.use_smooth = False

    # Right pillar
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(entry_width/2 + 0.2, -4.2, entry_height/2 + 1.0),
        scale=(0.35, entry_depth/2, entry_height/2)
    )
    right_pillar = bpy.context.active_object
    right_pillar.name = "entry_pillar_right"
    assign_mat(right_pillar, mat_detail)
    for poly in right_pillar.data.polygons:
        poly.use_smooth = False

    # Top lintel (heavy angular beam)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, -4.2, entry_height + 1.0 + 0.2),
        scale=(entry_width/2 + 0.55, entry_depth/2, 0.3)
    )
    lintel = bpy.context.active_object
    lintel.name = "entry_lintel"
    assign_mat(lintel, mat_detail)
    for poly in lintel.data.polygons:
        poly.use_smooth = False

    # Gold edge accents on entry frame
    # Left edge strip
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-entry_width/2 - 0.2, -4.2 - entry_depth/2 - 0.02, entry_height/2 + 1.0),
        scale=(0.04, 0.04, entry_height/2 + 0.3)
    )
    edge_l = bpy.context.active_object
    edge_l.name = "entry_edge_left"
    assign_mat(edge_l, mat_emissive)

    # Right edge strip
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(entry_width/2 + 0.2, -4.2 - entry_depth/2 - 0.02, entry_height/2 + 1.0),
        scale=(0.04, 0.04, entry_height/2 + 0.3)
    )
    edge_r = bpy.context.active_object
    edge_r.name = "entry_edge_right"
    assign_mat(edge_r, mat_emissive)

    # Top edge strip
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, -4.2 - entry_depth/2 - 0.02, entry_height + 1.0 + 0.5),
        scale=(entry_width/2 + 0.55, 0.04, 0.04)
    )
    edge_t = bpy.context.active_object
    edge_t.name = "entry_edge_top"
    assign_mat(edge_t, mat_emissive)

    print("Entry portal: 6 objects (2 pillars + lintel + 3 gold edges)")
    return [left_pillar, right_pillar, lintel, edge_l, edge_r, edge_t]


entry = create_entry()


# ============================================================
# ELEMENT 7: Rooftop Observation Deck
# Cantilevered transparent platform extending from crown
# ============================================================

def create_observation_deck():
    """Create the cantilevered observation deck at the top."""

    crown_z = 14.0 + 1.0  # top of main body + base offset

    # Transparent floor platform — extends outward from one side
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(3.5, 0, crown_z + 0.25),
        scale=(2.0, 1.5, 0.05)
    )
    deck_floor = bpy.context.active_object
    deck_floor.name = "obs_deck_floor"
    assign_mat(deck_floor, mat_glass)
    for poly in deck_floor.data.polygons:
        poly.use_smooth = False

    # Railing — thin detail strips
    # Back railing
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(5.4, 0, crown_z + 0.7),
        scale=(0.04, 1.5, 0.4)
    )
    railing_back = bpy.context.active_object
    railing_back.name = "obs_railing_back"
    assign_mat(railing_back, mat_detail)

    # Side railings
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(3.5, 1.45, crown_z + 0.7),
        scale=(2.0, 0.04, 0.4)
    )
    railing_side1 = bpy.context.active_object
    railing_side1.name = "obs_railing_side1"
    assign_mat(railing_side1, mat_detail)

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(3.5, -1.45, crown_z + 0.7),
        scale=(2.0, 0.04, 0.4)
    )
    railing_side2 = bpy.context.active_object
    railing_side2.name = "obs_railing_side2"
    assign_mat(railing_side2, mat_detail)

    # Railing top rail — emissive gold
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(3.5, 0, crown_z + 1.05),
        scale=(2.0, 1.5, 0.03)
    )
    railing_top = bpy.context.active_object
    railing_top.name = "obs_railing_top"
    # Only keep 3 sides (no inner side). For simplicity, use full frame.
    assign_mat(railing_top, mat_emissive)

    print("Observation deck: 5 objects (floor + 3 railings + top rail)")
    return [deck_floor, railing_back, railing_side1, railing_side2, railing_top]


obs_deck = create_observation_deck()


# ============================================================
# ELEMENT 8: Clock/Market Display Panel
# Small flat emissive panel near the entry facade
# ============================================================

def create_market_display():
    """Create a small market data display panel at the entry level."""

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(2.0, -4.0, 3.5),
        scale=(0.8, 0.05, 0.5)
    )
    display = bpy.context.active_object
    display.name = "market_display"
    assign_mat(display, mat_emissive)
    for poly in display.data.polygons:
        poly.use_smooth = False

    print("Market display: 1 object")
    return display


market_display = create_market_display()


# ============================================================
# ELEMENT 9: Pipeline Connection Hardpoint
# Simple geometry at crown level for SIA energy conduit
# ============================================================

def create_energy_hardpoint():
    """Create a small connection point for the SIA energy pipeline."""

    crown_z = 14.0 + 1.0

    # Small octagonal collar at the back of the crown
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=0.4, depth=0.5,
        location=(0, 3.0, crown_z - 1.0)
    )
    hardpoint = bpy.context.active_object
    hardpoint.name = "energy_hardpoint"
    assign_mat(hardpoint, mat_energy)
    for poly in hardpoint.data.polygons:
        poly.use_smooth = False

    print("Energy hardpoint: 1 object")
    return hardpoint


hardpoint = create_energy_hardpoint()


# ============================================================
# ELEMENT 10: Additional Facet Detail — Diagonal Edge Lines
# Extra facet junction lines between the octagonal vertices
# to make the crystalline pattern richer
# ============================================================

def create_diagonal_edges():
    """Add diagonal facet lines across select faces for gemstone richness."""

    total_height = 14.0
    base_radius = 4.0
    sides = 8
    z_offset = 1.0

    sections = [
        (0.00, 1.00, 0),
        (0.05, 1.02, 0),
        (0.12, 0.95, 3),
        (0.28, 0.88, -2),
        (0.45, 0.82, 4),
        (0.62, 0.76, -3),
        (0.80, 0.72, 2),
        (0.92, 0.70, -1),
        (1.00, 0.68, 0),
    ]

    diag_objects = []

    # Diagonal lines: connect vertex j of section i to vertex j+1 of section i+1
    # This creates X-pattern faceting across faces
    for i in range(0, len(sections) - 1, 2):  # every other section pair
        for j in range(0, sides, 2):  # every other face
            # Start point: section i, vertex j
            h1 = sections[i][0] * total_height + z_offset
            r1 = base_radius * sections[i][1]
            rot1 = math.radians(sections[i][2])
            angle1 = (2 * math.pi * j / sides) + rot1
            r_var1 = r1 * (1.0 + 0.06 * math.sin(angle1 * 3 + i * 0.7))
            p1 = (r_var1 * math.cos(angle1), r_var1 * math.sin(angle1), h1)

            # End point: section i+1, vertex j+1
            j_next = (j + 1) % sides
            h2 = sections[i+1][0] * total_height + z_offset
            r2 = base_radius * sections[i+1][1]
            rot2 = math.radians(sections[i+1][2])
            angle2 = (2 * math.pi * j_next / sides) + rot2
            r_var2 = r2 * (1.0 + 0.06 * math.sin(angle2 * 3 + (i+1) * 0.7))
            p2 = (r_var2 * math.cos(angle2), r_var2 * math.sin(angle2), h2)

            curve_data = bpy.data.curves.new(f"edge_diag_{i}_{j}_curve", 'CURVE')
            curve_data.dimensions = '3D'
            curve_data.bevel_depth = 0.03
            curve_data.bevel_resolution = 1

            spline = curve_data.splines.new('POLY')
            spline.points.add(1)
            spline.points[0].co = (*p1, 1.0)
            spline.points[1].co = (*p2, 1.0)

            obj = bpy.data.objects.new(f"edge_diag_{i}_{j}", curve_data)
            bpy.context.collection.objects.link(obj)
            assign_mat(obj, mat_emissive)
            diag_objects.append(obj)

    print(f"Diagonal facet edges: {len(diag_objects)} curves")
    return diag_objects


diag_edges = create_diagonal_edges()


# ============================================================
# FINAL: Report tri counts
# ============================================================

print("\n--- OBJECT INVENTORY ---")
total_tris = 0
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        # Apply transforms for accurate count
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh_eval = obj_eval.to_mesh()
        tris = sum(len(poly.vertices) - 2 for poly in mesh_eval.polygons)
        print(f"  {obj.name}: {tris} tris, mat={obj.data.materials[0].name if obj.data.materials else 'NONE'}")
        total_tris += tris
        obj_eval.to_mesh_clear()
    elif obj.type == 'CURVE':
        # Curves will be converted later; estimate tris from bevel
        print(f"  {obj.name}: CURVE (will convert in detail session)")

# Count curve objects
curve_count = sum(1 for obj in bpy.data.objects if obj.type == 'CURVE')

print(f"\nTotal mesh tris: {total_tris}")
print(f"Curve objects (edge accents): {curve_count}")
print(f"Total objects: {len(bpy.data.objects)}")
print("Major forms complete.")

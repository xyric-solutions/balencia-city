"""
Balencia City v3 — Material Library (7-Slot System)
Run in Blender before building any module.
Creates the 7-slot material set for the active module.

Usage:
    import material_library
    mats = material_library.create_materials("#FF5E00")  # pass district color hex
    mats = material_library.create_materials("#FF5E00", include_energy=True, include_holo=True)
"""
import bpy


def hex_to_linear(hex_color):
    """Convert hex color string to linear RGB tuple (Blender internal)."""
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


def _make_material(name, base_color, roughness, metallic, emission_color=None, emission_strength=0.0, alpha=1.0):
    """Create a Principled BSDF material with the given properties."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic

    if emission_color and emission_strength > 0:
        bsdf.inputs["Emission Color"].default_value = emission_color
        bsdf.inputs["Emission Strength"].default_value = emission_strength

    if alpha < 1.0:
        mat.blend_method = 'BLEND' if hasattr(mat, 'blend_method') else None
        bsdf.inputs["Alpha"].default_value = alpha

    return mat


def create_materials(district_color_hex, include_energy=True, include_holo=False):
    """
    Create the 7-slot material set for a Balencia City structure.

    Slots 1-5 (always created): base, accent, glass, detail, emissive
    Slot 6 (energy): Orange pipeline conduits — opt-in via include_energy
    Slot 7 (holo): Holographic/bioluminescent elements — opt-in via include_holo

    Args:
        district_color_hex: The district's accent color as hex string (e.g., "#FF5E00")
        include_energy: Whether to create the energy material (default True)
        include_holo: Whether to create the holo material (default False)

    Returns:
        dict with keys: base, accent, glass, detail, emissive, [energy], [holo]
    """
    district_color = hex_to_linear(district_color_hex)

    materials = {
        "base": _make_material(
            name="base",
            base_color=BASE_COLOR,
            roughness=0.80,
            metallic=0.05,
        ),
        "accent": _make_material(
            name="accent",
            base_color=ACCENT_INACTIVE,
            roughness=0.55,
            metallic=0.16,
            emission_color=district_color,
            emission_strength=0.24,
        ),
        "glass": _make_material(
            name="glass",
            base_color=GLASS_COLOR,
            roughness=0.10,
            metallic=0.30,
            emission_color=hex_to_linear("#FEF3C7"),
            emission_strength=0.08,
            alpha=0.86,
        ),
        "detail": _make_material(
            name="detail",
            base_color=DETAIL_COLOR,
            roughness=0.60,
            metallic=0.15,
        ),
        "emissive": _make_material(
            name="emissive",
            base_color=DETAIL_COLOR,
            roughness=0.22,
            metallic=0.00,
            emission_color=district_color,
            emission_strength=0.06,
        ),
    }

    if include_energy:
        materials["energy"] = _make_material(
            name="energy",
            base_color=DETAIL_COLOR,
            roughness=0.15,
            metallic=0.10,
            emission_color=ENERGY_ORANGE,
            emission_strength=0.10,
        )

    if include_holo:
        materials["holo"] = _make_material(
            name="holo",
            base_color=DETAIL_COLOR,
            roughness=0.20,
            metallic=0.05,
            emission_color=district_color,
            emission_strength=0.15,
            alpha=0.40,
        )

    return materials


def assign_material(obj, material):
    """Assign a material to an object, replacing existing if same name."""
    for i, slot in enumerate(obj.data.materials):
        if slot and slot.name == material.name:
            obj.data.materials[i] = material
            return
    obj.data.materials.append(material)


def clear_materials():
    """Remove all unused materials from the Blender file."""
    for mat in bpy.data.materials:
        if not mat.users:
            bpy.data.materials.remove(mat)

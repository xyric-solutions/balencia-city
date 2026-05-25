# SIA Life Coach Tower -- Central Hero

## Identity
- **Module**: #00
- **Color**: Burnt Orange `#FF5E00`
- **Floors**: 100+ (tallest structure in city by 2.5x)
- **GLB Filename**: `sia-tower-ext.glb` / `sia-tower-int.glb`
- **Energy Delivery**: Hub -- all 11 pipelines originate from its crown junction ring
- **Tri Budget**: Exterior 20K-30K | Interior 10K-15K
- **File Budget**: Exterior 200-500 KB | Interior 100-300 KB

## Exterior Architecture

### Description
The SIA Tower dominates the Balencia skyline as the undeniable center of gravity. A dark glass monolith tapered from a wide angular base platform to a narrow crown, wrapped in a warm bronze geometric framework that traces diagonal and horizontal lines across the facade like a structural exoskeleton. The framework catches light and gives the tower its signature lattice silhouette.

Every 10 floors, a horizontal ring of burnt orange energy encircles the tower, pulsing faintly. These rings intensify toward the crown, where they converge into the crystalline glass crown structure -- a geometric, faceted formation emitting a vertical beacon of orange light skyward. Below the crown sits the junction ring: a thick structural band from which 11 neural energy pipelines arc outward toward each district building.

At street level, a 5-story entrance archway opens into the building, framed by angular supports and flooded with volumetric orange light. A 10-meter holographic SIA geometric mark floats above the entrance. Ground-level energy veins radiate outward from the base platform like roots, connecting into the city's ground network.

### Key Architectural Elements
- Main tower body: tapered rectangular column, 100+ floors, dark glass panels
- Bronze geometric exoskeleton framework on all four facades (diagonal + horizontal members)
- Crystalline crown: faceted glass geometry emitting vertical orange beacon
- Crown junction ring: thick structural torus with 11 pipeline departure hardpoints
- Orange energy rings: horizontal glowing bands every 10 floors (10 total)
- 5-story entrance archway: angular frame, deep recess, volumetric light spill
- Holographic SIA mark: 10m floating geometric logo above entrance (holo slot)
- Ground-level energy veins: 8-12 flat tubes radiating outward from base
- Angular base platform: wide footprint, stepped geometry, darker than tower body
- Antenna/spire above crown beacon for additional height emphasis

### Silhouette Markers
Tallest structure by 2.5x minimum. The tapered body with visible exoskeleton framework, plus the crystalline crown beacon shooting light upward, makes this unmistakable at any viewport size. No other building has the vertical beacon or the visible pipeline departure arcs at the top.

### Material Assignment
| Surface | Slot | Notes |
|---------|------|-------|
| Tower glass panels | glass | Dark tinted, slight reflection, alpha 0.86 |
| Bronze exoskeleton framework | accent | Warm metallic, faint orange emission |
| Crystalline crown facets | glass | Brighter than body glass, higher emission |
| Crown beacon light | emissive | Full burnt orange emission, strength 0.06+ |
| Energy rings (every 10 floors) | energy | #FF5E00, emission strength 0.10 |
| Junction ring | detail | Structural dark metal, non-emissive |
| Entrance archway structure | base | Dark concrete/metal, roughness 0.80 |
| SIA holographic mark | holo | Semi-transparent, orange glow, alpha 0.40 |
| Base platform | base | Darker than tower, roughness 0.80 |
| Ground energy veins | energy | #FF5E00, flat tubes at ground level |

## Interior -- Neural Core Atrium

### Description
A vast cylindrical atrium spanning the full interior height, anchored by a central floating holographic 3D city model that slowly rotates at the midpoint of the space. The atrium walls are lined with holographic data panels displaying district status information. Floating platforms at varying heights create a vertical stack of observation decks connected by light bridges.

The SIA geometric mark rotates and glows at the apex of the central model. 11 color-coded corridor entrances radiate outward at ground level, each marked with its district color and leading to the corresponding pipeline. Rising particles drift upward through the space like reverse snowfall -- tiny orange and amber points of light ascending continuously. Purple AI orbs drift at various heights, pulsing with data.

### Focal Point
The central floating holographic city model -- a miniature 3D representation of the entire Balencia City, slowly rotating, with each district glowing in its signature color.

### Supporting Props (6 items)
- Holographic data panels on cylindrical walls (3-4 large curved screens)
- Floating observation platforms at 3 different heights (simple disc geometry)
- 11 color-coded corridor entrance frames at ground level (arched doorways)
- Purple AI orbs (3-4 small emissive spheres drifting at varying heights)
- Rising particle emitter zone (modeled as a vertical column of tiny spheres)
- Light bridges connecting floating platforms (thin flat geometry, emissive slot)

### Light Empties
- light_0: Center of atrium at city-model height -- warm key light illuminating the hologram
- light_1: Upper atrium near crown -- cool fill from above casting soft ambient downward
- light_2: Ground level near corridor entrances -- orange accent uplighting

### Camera Target
Center of the holographic city model, approximately 40% up the atrium height. Camera positioned to capture the vertical scale with the city model as focal center and at least 3 corridor entrances visible at the base.

## Reference Search Terms
- Sketchfab: "futuristic tower sci-fi", "cyberpunk skyscraper", "glass tower geometric framework", "sci-fi atrium interior"
- AI Generation: "dark glass skyscraper with bronze geometric exoskeleton and orange energy beacon crown, cyberpunk city, night scene"

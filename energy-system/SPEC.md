# Energy System Specification

The SIA Energy System is the visual nervous system connecting SIA Tower to all districts.

## Neural Light Pipelines (11 total)

Orange energy conduits (#FF5E00) with flowing light particles, arced through the air from SIA Tower crown to each district.

### Pipeline Types

| Type | Style | Districts | Visual |
|------|-------|-----------|--------|
| Hard Pipeline | Visible orange tube with flowing particles | Fitness, Career, Finance, Communication, Leaderboard, Knowledgebase, Analytics, Nutrition | Solid tube, bright, constant flow |
| Warm Mist | Particle cloud dispersal | Yoga & Wellbeing, Relationships | Soft cloud, gentle, diffuse |
| Faint Thread | Nearly invisible whisper line | Recovery & Sleep | Barely visible, ultra-thin |
| Waterfall (Special) | Energy cascades downward | Knowledgebase | Hard pipeline + downward cascade at endpoint |
| Lightning Bolt (Special) | Dramatic burst entry at apex | Leaderboard | Hard pipeline + dramatic flash at arena rim |

### Technical Specs
- Tube radius: 0.08 units (hard), 0.02 (faint thread)
- Arc height: 30-50 units above ground (varies by distance)
- Segments: 64 per pipeline curve
- Material: energy slot (Burnt Orange #FF5E00)
- UV layout: scrolling for particle animation effect
- Tris per pipeline: 500-1,500
- File size per pipeline: 10-40 KB

### Ground Energy Veins
At each pipeline endpoint, 8 orange veins radiate outward at ground level (Y=0.05).
- Vein radius: 3.0 units from center
- Tube radius: 0.02 units
- Material: energy slot

## AI Pulse System

Every 8 seconds, SIA Tower crown emits an expanding orange ring.

| Time | Event |
|------|-------|
| T=0.0s | Pulse origin at crown (orange intensifies) |
| T=0.5s | Ring of orange light expands outward from crown |
| T=2.0s | Ring reaches inner districts |
| T=4.0s | All districts briefly brighten, activity intensifies |
| T=6.0s | Ring dissipates at city perimeter |
| T=8.0s | Cycle repeats |

### Geometry
- Ring: Torus with small cross-section (0.1 units)
- Material: energy slot with emissive 2.0+
- Animation: scale from 0 to city diameter over 6 seconds
- Tris: 200-500

## Cross-District Gold Connections

Golden lines (#F59E0B) firing between districts when cross-pillar intelligence is active.

### Connection Examples
| From | To | Insight |
|------|----|---------|
| Fitness | Recovery | Recovery score impacts tomorrow's workout capacity |
| Nutrition | Career | Skipped meals on meeting days reduce afternoon focus 31% |
| Relationships | Wellbeing | Social connection improves recovery scores by 24% |
| Finance | Career | Spending increases 40% during high-stress work weeks |
| Sleep | Analytics | Evening meditation correlates with next-day focus scores |
| Communication | Relationships | You haven't spoken to [name] in 14 days |

### Geometry
- Thin gold lines between district orbital positions
- Midpoint anchor empty for insight card placement
- Material: gold emissive (#F59E0B, emission strength 0.8)
- Tris per connection: 100-300

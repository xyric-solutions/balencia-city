# Energy Shader Parameters

Runtime handoff notes for Balencia City energy assets.

## Cross-District Gold Connections

Session: 54  
Asset: `energy-system/cross-connections/approved/cross-district-gold.glb`  
Runtime material key: `energy`  
Display color: `#F59E0B`  
Base emission strength: `0.8`  
Inactive emission strength: `0.1`  
Active bloom target: bright gold with bloom, active for 2-3 seconds before fade  
Geometry: six arced mesh lines, 200 tris each, 1,200 tris total  
Insight anchors: `insight_anchor_*` empties, one per connection, with `connection_id`, `connection_from`, `connection_to`, and `insight` custom properties

| Connection ID | From | To | Runtime Insight |
|---------------|------|----|-----------------|
| `fitness_recovery` | Fitness | Recovery & Sleep | Recovery score impacts tomorrow's workout capacity |
| `nutrition_career` | Nutrition | Career | Skipped meals on meeting days reduce afternoon focus 31% |
| `relationships_yoga` | Relationships | Yoga & Wellbeing | Social connection improves recovery scores by 24% |
| `finance_career` | Finance | Career | Spending increases 40% during high-stress work weeks |
| `recovery_analytics` | Recovery & Sleep | AI Analytics | Evening meditation correlates with next-day focus scores |
| `chat_relationships` | Chat & Communication | Relationships | You haven't spoken to [name] in 14 days |

## AI Pulse Ring

Session: 55  
Asset: `energy-system/pulse/approved/ai-pulse.glb`  
Runtime material key: `energy`  
Display color: `#FF5E00`  
Base emission strength: `2.4`  
Inactive emission strength: `0.1`  
Active bloom target: bright orange crown heartbeat with citywide radial sweep  
Geometry: animated horizontal torus plus crown intensifier, 444 tris total  
Cycle: 8 seconds / 192 frames at 24 fps  
Origin: `[0.0, 0.0, 42.35]`, 0.35u above the SIA crown  
Perimeter radius: `75.3281` units  
City diameter: `150.6561` units

| Time | Frame | Runtime Event | Ring Radius |
|------|-------|---------------|-------------|
| `T=0.0s` | `0` | Crown origin pulse begins | `0.08u` |
| `T=0.5s` | `12` | Ring expands past crown glow | `4.5u` |
| `T=2.0s` | `48` | Inner district ring reached | `34.0149u` |
| `T=4.0s` | `96` | All district centers brighten | `59.5397u` |
| `T=6.0s` | `144` | City perimeter reached, fade begins | `75.3281u` |
| `T=8.0s` | `192` | Cycle resets | `0.08u` |

Runtime fade note: keep alpha high from T=0.5 to T=2, soften by T=4, and fade to transparent by T=6 before the T=8 reset. Reimported animation actions are `ai_pulse_crown_intensifierAction` and `ai_pulse_expanding_ringAction`.

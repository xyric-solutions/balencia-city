import type { Vec3 } from "./types";

export const AI_PULSE_TIMING = {
  assetId: "ai-pulse",
  displayColor: "#FF5E00",
  baseEmissionStrength: 2.4,
  inactiveEmissionStrength: 0.1,
  cycleSeconds: 8,
  framesAt24Fps: 192,
  origin: [0, 42.35, 0] satisfies Vec3,
  perimeterRadius: 75.3281,
  cityDiameter: 150.6561,
  keyframes: [
    { time: 0, frame: 0, event: "Crown origin pulse begins", radius: 0.08 },
    { time: 0.5, frame: 12, event: "Ring expands past crown glow", radius: 4.5 },
    { time: 2, frame: 48, event: "Inner district ring reached", radius: 34.0149 },
    { time: 4, frame: 96, event: "All district centers brighten", radius: 59.5397 },
    { time: 6, frame: 144, event: "City perimeter reached, fade begins", radius: 75.3281 },
    { time: 8, frame: 192, event: "Cycle resets", radius: 0.08 },
  ],
  animationActions: ["ai_pulse_crown_intensifierAction", "ai_pulse_expanding_ringAction"],
} as const;

export const CROSS_DISTRICT_INSIGHTS = [
  {
    id: "fitness_recovery",
    from: "Fitness",
    to: "Recovery and sleep",
    insight: "Recovery score impacts tomorrow's workout capacity",
  },
  {
    id: "nutrition_career",
    from: "Nutrition",
    to: "Career",
    insight: "Skipped meals on meeting days reduce afternoon focus 31%",
  },
  {
    id: "relationships_yoga",
    from: "Relationships",
    to: "Yoga and wellbeing",
    insight: "Social connection improves recovery scores by 24%",
  },
  {
    id: "finance_career",
    from: "Finance",
    to: "Career",
    insight: "Spending increases 40% during high-stress work weeks",
  },
  {
    id: "recovery_analytics",
    from: "Recovery and sleep",
    to: "AI analytics",
    insight: "Evening meditation correlates with next-day focus scores",
  },
  {
    id: "chat_relationships",
    from: "Chat and communication",
    to: "Relationships",
    insight: "You haven't spoken to [name] in 14 days",
  },
] as const;

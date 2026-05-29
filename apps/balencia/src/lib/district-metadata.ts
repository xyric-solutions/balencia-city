import { BRAND_COLORS } from "./materials";
import type { Vec3 } from "./types";

export type PadShape = "round" | "rect" | "oval" | "octagon";
export type DistrictMotif =
  | "civic"
  | "track"
  | "sanctuary"
  | "bank"
  | "library"
  | "signal"
  | "arena"
  | "garden"
  | "career"
  | "sleep"
  | "analytics"
  | "farm";
export type LabelTier = "primary" | "major" | "standard";
export type DistrictActivityTone = "surge" | "calm" | "focus" | "core";

export type DistrictActivityProfile = {
  tone: DistrictActivityTone;
  pulseOffset: number;
  glowScale: number;
};

export type DistrictPreview = {
  status: string;
  insight: string;
  signal: string;
};

export type ActiveLabelLayout = {
  distanceFactor?: number;
  labelHeight?: number;
  labelOffset?: number;
};

export type OverviewLabelLayout = {
  distanceFactor?: number;
  height: number;
  lateral?: number;
  maxWidth?: number;
  offset: number;
};

export type ScreenLabelLayout = {
  left: number;
  maxWidth?: number;
  top: number;
};

export type DistrictProfile = {
  label: string;
  place: string;
  padShape: PadShape;
  padSize: readonly [number, number];
  anchorHeight: number;
  labelLift: number;
  labelOffset: number;
  labelTier: LabelTier;
  motif: DistrictMotif;
  motifColor: string;
  boardLift: number;
  boardOffset: number;
  boardDistanceFactor: number;
  boardWidth: number;
  activity: DistrictActivityProfile;
  preview: DistrictPreview;
  interactionTarget: boolean;
  mobileOverview: boolean;
  boardDirection?: Vec3;
};

export const OVERVIEW_SCENES = new Set([1, 15, 17]);
export const SIA_FOCUS_SCENES = new Set([1, 2, 3, 15, 17]);

export const DISTRICT_PROFILES: Record<string, DistrictProfile> = {
  "sia-tower": {
    label: "SIA Tower",
    place: "Civic intelligence core",
    padShape: "round",
    padSize: [29, 29],
    anchorHeight: 48,
    labelLift: 4,
    labelOffset: 0,
    labelTier: "primary",
    motif: "civic",
    motifColor: BRAND_COLORS.energy,
    boardLift: 5,
    boardOffset: 5.4,
    boardDistanceFactor: 22,
    boardWidth: 5.8,
    activity: { tone: "core", pulseOffset: 0, glowScale: 1.26 },
    preview: {
      status: "Core synthesis active",
      insight: "Daily plan balances energy, mood, and commitments.",
      signal: "Sleep, nutrition, and calendar pressure shape today's priorities.",
    },
    interactionTarget: true,
    mobileOverview: true,
    boardDirection: [0, 0, 1],
  },
  fitness: {
    label: "Fitness district",
    place: "Sports and movement complex",
    padShape: "rect",
    padSize: [22, 18],
    anchorHeight: 17,
    labelLift: 4,
    labelOffset: 18,
    labelTier: "major",
    motif: "track",
    motifColor: BRAND_COLORS.forest,
    boardLift: 8,
    boardOffset: 14,
    boardDistanceFactor: 21,
    boardWidth: 5.2,
    activity: { tone: "surge", pulseOffset: 0.12, glowScale: 1.14 },
    preview: {
      status: "Training load rising",
      insight: "Recovery score sets the next workout ceiling.",
      signal: "Sleep quality and nutrition adjust effort targets.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  yoga: {
    label: "Yoga and wellbeing",
    place: "Floating sanctuary",
    padShape: "oval",
    padSize: [23, 17],
    anchorHeight: 11,
    labelLift: 4,
    labelOffset: 18,
    labelTier: "standard",
    motif: "sanctuary",
    motifColor: "#6EE7B7",
    boardLift: 8,
    boardOffset: 13,
    boardDistanceFactor: 22,
    boardWidth: 4.8,
    activity: { tone: "calm", pulseOffset: 0.34, glowScale: 0.86 },
    preview: {
      status: "Breathwork queue calm",
      insight: "Stress spikes pair with shorter reset sessions.",
      signal: "Calendar density changes calm prompts.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  finance: {
    label: "Finance district",
    place: "Premium advisory tower",
    padShape: "octagon",
    padSize: [19, 19],
    anchorHeight: 21,
    labelLift: 4,
    labelOffset: 16,
    labelTier: "major",
    motif: "bank",
    motifColor: BRAND_COLORS.gold,
    boardLift: 7,
    boardOffset: 13,
    boardDistanceFactor: 20,
    boardWidth: 5.2,
    activity: { tone: "focus", pulseOffset: 0.48, glowScale: 1.02 },
    preview: {
      status: "Spend pattern watch",
      insight: "Bills and stress peaks surface before cashflow tightens.",
      signal: "Workload and sleep trends inform advisory timing.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  knowledgebase: {
    label: "Knowledgebase district",
    place: "Archive and learning library",
    padShape: "rect",
    padSize: [22, 18],
    anchorHeight: 19,
    labelLift: 5,
    labelOffset: 18,
    labelTier: "standard",
    motif: "library",
    motifColor: BRAND_COLORS.purple,
    boardLift: 7,
    boardOffset: 13,
    boardDistanceFactor: 22,
    boardWidth: 5.4,
    activity: { tone: "focus", pulseOffset: 0.62, glowScale: 0.98 },
    preview: {
      status: "Learning queue tuned",
      insight: "Useful topics repeat when recent habits add context.",
      signal: "Career goals and chat questions steer recommendations.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  chat: {
    label: "Chat and communication",
    place: "Conversation district",
    padShape: "rect",
    padSize: [23, 18],
    anchorHeight: 17,
    labelLift: 5,
    labelOffset: 20,
    labelTier: "standard",
    motif: "signal",
    motifColor: BRAND_COLORS.energy,
    boardLift: 7,
    boardOffset: 14,
    boardDistanceFactor: 22,
    boardWidth: 4.8,
    activity: { tone: "focus", pulseOffset: 0.76, glowScale: 0.92 },
    preview: {
      status: "Conversation pulse live",
      insight: "Tone shifts flag where follow-up may help.",
      signal: "Relationships and recovery state adjust response timing.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  leaderboard: {
    label: "Leaderboard and competition",
    place: "Competition arena",
    padShape: "round",
    padSize: [23, 23],
    anchorHeight: 18,
    labelLift: 6,
    labelOffset: 18,
    labelTier: "standard",
    motif: "arena",
    motifColor: "#FB7185",
    boardLift: 7,
    boardOffset: 13,
    boardDistanceFactor: 22,
    boardWidth: 5.2,
    activity: { tone: "surge", pulseOffset: 0.9, glowScale: 1.1 },
    preview: {
      status: "Challenge window open",
      insight: "Competition ramps only when consistency is stable.",
      signal: "Fitness streaks and sleep readiness shape difficulty.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  relationships: {
    label: "Relationships district",
    place: "Connection district",
    padShape: "oval",
    padSize: [24, 18],
    anchorHeight: 10,
    labelLift: 5,
    labelOffset: 20,
    labelTier: "standard",
    motif: "garden",
    motifColor: "#F43F5E",
    boardLift: 5,
    boardOffset: 14,
    boardDistanceFactor: 22,
    boardWidth: 5.6,
    activity: { tone: "calm", pulseOffset: 0.18, glowScale: 0.9 },
    preview: {
      status: "Connection garden warm",
      insight: "Contact gaps become simple follow-up prompts.",
      signal: "Mood, recovery, and chat tone guide outreach.",
    },
    interactionTarget: true,
    mobileOverview: true,
    boardDirection: [0.55, 0, 0.84],
  },
  career: {
    label: "Career district",
    place: "Professional growth towers",
    padShape: "rect",
    padSize: [22, 19],
    anchorHeight: 23,
    labelLift: 6,
    labelOffset: 18,
    labelTier: "major",
    motif: "career",
    motifColor: "#3B82F6",
    boardLift: 8,
    boardOffset: 14,
    boardDistanceFactor: 22,
    boardWidth: 5.4,
    activity: { tone: "surge", pulseOffset: 0.4, glowScale: 1.16 },
    preview: {
      status: "Focus block forming",
      insight: "Deep work rises when recovery and stress are clear.",
      signal: "Sleep and nutrition adjust task timing.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  recovery: {
    label: "Recovery and sleep",
    place: "Restorative district",
    padShape: "oval",
    padSize: [24, 18],
    anchorHeight: 10,
    labelLift: 5,
    labelOffset: 20,
    labelTier: "standard",
    motif: "sleep",
    motifColor: "#6366F1",
    boardLift: 8,
    boardOffset: 14,
    boardDistanceFactor: 22,
    boardWidth: 5.4,
    activity: { tone: "calm", pulseOffset: 0.58, glowScale: 0.8 },
    preview: {
      status: "Reset protocol quiet",
      insight: "Bedtime shifts explain tomorrow's focus forecast.",
      signal: "Training load and stress set recovery priority.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  analytics: {
    label: "AI analytics",
    place: "Insight cathedral",
    padShape: "octagon",
    padSize: [20, 23],
    anchorHeight: 21,
    labelLift: 5,
    labelOffset: 17,
    labelTier: "standard",
    motif: "analytics",
    motifColor: "#14B8A6",
    boardLift: 7,
    boardOffset: 13,
    boardDistanceFactor: 22,
    boardWidth: 4.8,
    activity: { tone: "focus", pulseOffset: 0.72, glowScale: 1.08 },
    preview: {
      status: "Patterns consolidating",
      insight: "Outliers become recommendations when signals repeat.",
      signal: "All districts feed confidence and trend strength.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
  nutrition: {
    label: "Nutrition district",
    place: "Food and nourishment farm",
    padShape: "rect",
    padSize: [23, 18],
    anchorHeight: 14,
    labelLift: 4,
    labelOffset: 19,
    labelTier: "standard",
    motif: "farm",
    motifColor: BRAND_COLORS.forest,
    boardLift: 8,
    boardOffset: 14,
    boardDistanceFactor: 22,
    boardWidth: 5,
    activity: { tone: "focus", pulseOffset: 0.86, glowScale: 0.94 },
    preview: {
      status: "Meal rhythm syncing",
      insight: "Protein and hydration shape energy later in the day.",
      signal: "Fitness load and sleep quality adjust meal timing.",
    },
    interactionTarget: true,
    mobileOverview: true,
  },
};

export const ACTIVE_LABEL_LAYOUT_OVERRIDES: Record<number, Record<string, ActiveLabelLayout>> = {
  4: {
    fitness: { distanceFactor: 21, labelHeight: 14, labelOffset: 3.2 },
  },
  5: {
    yoga: { distanceFactor: 22, labelHeight: 10.5, labelOffset: 3.1 },
  },
  6: {
    finance: { distanceFactor: 20, labelHeight: 16, labelOffset: 3 },
  },
  7: {
    knowledgebase: { distanceFactor: 22, labelHeight: 15, labelOffset: 3.3 },
  },
  8: {
    chat: { distanceFactor: 22, labelHeight: 14, labelOffset: 3.4 },
  },
  9: {
    leaderboard: { distanceFactor: 22, labelHeight: 12, labelOffset: 3.5 },
  },
  10: {
    relationships: { distanceFactor: 22, labelHeight: 9, labelOffset: 3.2 },
  },
  11: {
    career: { distanceFactor: 22, labelHeight: 18.5, labelOffset: 3.4 },
  },
  12: {
    recovery: { distanceFactor: 22, labelHeight: 8.8, labelOffset: 3.4 },
  },
  13: {
    analytics: { distanceFactor: 22, labelHeight: 16, labelOffset: 3.2 },
  },
  14: {
    nutrition: { distanceFactor: 22, labelHeight: 11.5, labelOffset: 3.4 },
  },
};

export const OVERVIEW_LABEL_LAYOUTS: Record<number, Record<string, OverviewLabelLayout>> = {
  1: {
    "sia-tower": { distanceFactor: 120, height: 56, maxWidth: 170, offset: 8 },
    recovery: { height: 17, lateral: -5, maxWidth: 170, offset: 9 },
    analytics: { height: 26, lateral: -4, offset: 8 },
    nutrition: { height: 21, lateral: 4, offset: 9 },
    career: { height: 31, lateral: -5, offset: 10 },
    fitness: { height: 24, lateral: -4, offset: 10 },
    relationships: { height: 17, lateral: -4, maxWidth: 188, offset: 10 },
    yoga: { height: 17, lateral: 5, offset: 10 },
    leaderboard: { height: 20, lateral: -5, maxWidth: 196, offset: 9 },
    finance: { height: 27, lateral: 4, offset: 8 },
    chat: { distanceFactor: 78, height: 27, lateral: -22, maxWidth: 188, offset: 9 },
    knowledgebase: { height: 25, lateral: 3, maxWidth: 188, offset: 9 },
  },
  15: {
    "sia-tower": { distanceFactor: 124, height: 58, maxWidth: 170, offset: 8 },
    recovery: { height: 17, lateral: -7, maxWidth: 170, offset: 10 },
    analytics: { height: 27, lateral: -5, offset: 9 },
    nutrition: { height: 22, lateral: 5, offset: 10 },
    career: { height: 32, lateral: -6, offset: 11 },
    fitness: { height: 25, lateral: -5, offset: 11 },
    relationships: { height: 17, lateral: -5, maxWidth: 188, offset: 11 },
    yoga: { height: 17, lateral: 6, offset: 11 },
    leaderboard: { height: 20, lateral: -6, maxWidth: 196, offset: 10 },
    finance: { height: 28, lateral: 5, offset: 9 },
    chat: { height: 24, lateral: 1, maxWidth: 188, offset: 10 },
    knowledgebase: { height: 26, lateral: 4, maxWidth: 188, offset: 10 },
  },
  17: {
    "sia-tower": { distanceFactor: 122, height: 58, maxWidth: 170, offset: 8 },
    recovery: { height: 17, lateral: -6, maxWidth: 170, offset: 10 },
    analytics: { height: 27, lateral: -5, offset: 9 },
    nutrition: { height: 22, lateral: 5, offset: 10 },
    career: { height: 31, lateral: -6, offset: 11 },
    fitness: { height: 24, lateral: -5, offset: 11 },
    relationships: { height: 17, lateral: -5, maxWidth: 188, offset: 11 },
    yoga: { height: 17, lateral: 6, offset: 11 },
    leaderboard: { height: 42, lateral: -14, maxWidth: 196, offset: 10 },
    finance: { height: 28, lateral: 5, offset: 9 },
    chat: { height: 24, lateral: 1, maxWidth: 188, offset: 10 },
    knowledgebase: { height: 26, lateral: 4, maxWidth: 188, offset: 10 },
  },
};

export const FOCUSED_LABEL_LAYOUTS: Record<number, { id: string } & ScreenLabelLayout> = {
  4: { id: "fitness", left: 68, maxWidth: 190, top: 35 },
  6: { id: "finance", left: 68, maxWidth: 180, top: 40 },
  11: { id: "career", left: 34, maxWidth: 180, top: 34 },
};

export const INTERACTIVE_DISTRICT_IDS = Object.entries(DISTRICT_PROFILES)
  .filter(([, profile]) => profile.interactionTarget)
  .map(([id]) => id);

export const FOCUSED_SCENE_INTERACTION_IDS: Record<number, string> = {
  2: "sia-tower",
  3: "sia-tower",
  4: "fitness",
  5: "yoga",
  6: "finance",
  7: "knowledgebase",
  8: "chat",
  9: "leaderboard",
  10: "relationships",
  11: "career",
  12: "recovery",
  13: "analytics",
  14: "nutrition",
};

export function getInteractionDistrictIdsForScene(sceneIndex: number) {
  if (OVERVIEW_SCENES.has(sceneIndex)) {
    return INTERACTIVE_DISTRICT_IDS;
  }

  const activeDistrictId = FOCUSED_SCENE_INTERACTION_IDS[sceneIndex];

  if (!activeDistrictId || !INTERACTIVE_DISTRICT_IDS.includes(activeDistrictId)) {
    return [];
  }

  return [activeDistrictId];
}

export function canInteractWithDistrictInScene(districtId: string | undefined, sceneIndex: number) {
  return !!districtId && getInteractionDistrictIdsForScene(sceneIndex).includes(districtId);
}

export function getDistrictProfile(id: string) {
  return DISTRICT_PROFILES[id] ?? DISTRICT_PROFILES["sia-tower"];
}

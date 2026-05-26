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
    label: "SIA tower",
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
    label: "Fitness complex",
    place: "Sports and movement district",
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
    label: "Yoga sanctuary",
    place: "Wellbeing gardens",
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
    interactionTarget: false,
    mobileOverview: true,
  },
  finance: {
    label: "Finance bank",
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
    label: "Knowledgebase library",
    place: "Archive and learning district",
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
    interactionTarget: false,
    mobileOverview: true,
  },
  chat: {
    label: "Chat hub",
    place: "Communication district",
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
    interactionTarget: false,
    mobileOverview: true,
  },
  leaderboard: {
    label: "Competition arena",
    place: "Leaderboard district",
    padShape: "round",
    padSize: [23, 23],
    anchorHeight: 12,
    labelLift: 22,
    labelOffset: 18,
    labelTier: "standard",
    motif: "arena",
    motifColor: "#FB7185",
    boardLift: 9,
    boardOffset: 13,
    boardDistanceFactor: 22,
    boardWidth: 5.2,
    activity: { tone: "surge", pulseOffset: 0.9, glowScale: 1.1 },
    preview: {
      status: "Challenge window open",
      insight: "Competition ramps only when consistency is stable.",
      signal: "Fitness streaks and sleep readiness shape difficulty.",
    },
    interactionTarget: false,
    mobileOverview: true,
  },
  relationships: {
    label: "Relationships garden",
    place: "Connection district",
    padShape: "oval",
    padSize: [24, 18],
    anchorHeight: 10,
    labelLift: 50,
    labelOffset: 20,
    labelTier: "standard",
    motif: "garden",
    motifColor: "#F43F5E",
    boardLift: 10,
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
    label: "Career towers",
    place: "Professional growth district",
    padShape: "rect",
    padSize: [22, 19],
    anchorHeight: 23,
    labelLift: 13,
    labelOffset: 18,
    labelTier: "major",
    motif: "career",
    motifColor: "#3B82F6",
    boardLift: 11,
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
    labelLift: 15,
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
    interactionTarget: false,
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
    interactionTarget: false,
    mobileOverview: true,
  },
  nutrition: {
    label: "Nutrition farm",
    place: "Food and nourishment district",
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
    interactionTarget: false,
    mobileOverview: true,
  },
};

export const ACTIVE_LABEL_LAYOUT_OVERRIDES: Record<number, Record<string, ActiveLabelLayout>> = {
  4: {
    fitness: { distanceFactor: 21, labelHeight: 14, labelOffset: 2.8 },
  },
  6: {
    finance: { distanceFactor: 20, labelHeight: 16, labelOffset: 2.4 },
  },
  11: {
    career: { distanceFactor: 22, labelHeight: 20, labelOffset: 2.6 },
  },
};

export const OVERVIEW_LABEL_LAYOUTS: Record<number, Record<string, ScreenLabelLayout>> = {
  1: {
    "sia-tower": { left: 50, maxWidth: 170, top: 28 },
    recovery: { left: 32, maxWidth: 180, top: 34 },
    analytics: { left: 45, top: 33 },
    nutrition: { left: 58, top: 35 },
    career: { left: 25, top: 45 },
    fitness: { left: 74, top: 44 },
    relationships: { left: 45, maxWidth: 188, top: 48 },
    yoga: { left: 81, top: 54 },
    leaderboard: { left: 45, maxWidth: 180, top: 62 },
    finance: { left: 70, top: 64 },
    chat: { left: 49, top: 76 },
    knowledgebase: { left: 61, maxWidth: 188, top: 73 },
  },
  15: {
    "sia-tower": { left: 50, maxWidth: 170, top: 25 },
    recovery: { left: 27, maxWidth: 180, top: 34 },
    analytics: { left: 43, top: 30 },
    nutrition: { left: 61, top: 31 },
    career: { left: 22, top: 48 },
    fitness: { left: 78, top: 40 },
    relationships: { left: 45, maxWidth: 188, top: 57 },
    yoga: { left: 82, top: 52 },
    leaderboard: { left: 40, maxWidth: 184, top: 72 },
    finance: { left: 73, top: 66 },
    chat: { left: 50, top: 78 },
    knowledgebase: { left: 64, maxWidth: 190, top: 75 },
  },
  17: {
    "sia-tower": { left: 50, maxWidth: 170, top: 26 },
    recovery: { left: 29, maxWidth: 180, top: 36 },
    analytics: { left: 43, top: 32 },
    nutrition: { left: 61, top: 33 },
    career: { left: 25, top: 44 },
    fitness: { left: 76, top: 41 },
    relationships: { left: 45, maxWidth: 188, top: 57 },
    yoga: { left: 80, top: 53 },
    leaderboard: { left: 40, maxWidth: 184, top: 72 },
    finance: { left: 72, top: 65 },
    chat: { left: 50, top: 78 },
    knowledgebase: { left: 62, maxWidth: 190, top: 74 },
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

export function getDistrictProfile(id: string) {
  return DISTRICT_PROFILES[id] ?? DISTRICT_PROFILES["sia-tower"];
}

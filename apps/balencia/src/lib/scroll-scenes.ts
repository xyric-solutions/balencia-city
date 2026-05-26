import * as THREE from "three";
import { layoutOffset, layoutPoint } from "./city-layout-v2";
import type { ScrollCamera, ScrollScene, Vec3 } from "./types";

export const SCROLL_TIMELINE_SECONDS = 300;
export const SCROLL_STAGE_HEIGHT_VH = 1700;
export const SCROLL_VH_PER_SECOND = SCROLL_STAGE_HEIGHT_VH / SCROLL_TIMELINE_SECONDS;

export const ALL_ENERGY_IDS = [
  "hard-pipelines",
  "warm-mist",
  "faint-thread",
  "knowledgebase-waterfall",
  "leaderboard-lightning",
  "cross-district-gold",
  "ai-pulse",
] as const;

const HARD_PIPELINE_ENERGY_IDS = ["hard-pipelines", "ai-pulse"] as const;
const WARM_MIST_ENERGY_IDS = ["warm-mist", "ai-pulse"] as const;

function districtTarget(id: string, height: number): Vec3 {
  return layoutPoint(id, height);
}

function districtCamera(id: string, offset: Vec3): Vec3 {
  return layoutOffset(id, offset);
}

export const SCROLL_SCENES: ScrollScene[] = [
  {
    scene: 1,
    slug: "arrival",
    scroll: 0,
    durationSeconds: 12,
    focus: "City aerial",
    title: "The civilization revealed",
    body: "A living intelligence powering every dimension of your life.",
    activeDistrict: "city",
    mode: "city",
    activeEnergyIds: ALL_ENERGY_IDS,
    camera: {
      position: [155, 128, 185],
      target: [0, 22, 4],
      fov: 47,
      lens: 14,
      frame: 144,
    },
  },
  {
    scene: 2,
    slug: "sia-tower-reveal",
    scroll: 0.07,
    durationSeconds: 16,
    focus: "SIA tower exterior",
    title: "SIA life coach tower",
    body: "I am SIA. The intelligence core, emotional engine, and life operating system.",
    activeDistrict: "sia-tower",
    mode: "exterior",
    activeEnergyIds: HARD_PIPELINE_ENERGY_IDS,
    camera: {
      position: [18, 7.8, 25],
      target: [0, 38, 0],
      fov: 42,
      lens: 30,
      frame: 12,
    },
  },
  {
    scene: 3,
    slug: "sia-neural-core",
    scroll: 0.13,
    durationSeconds: 14,
    focus: "SIA tower interior",
    title: "Inside SIA tower",
    body: "I see what no single app can. How your sleep affects your work.",
    activeDistrict: "sia-tower",
    mode: "interior",
    interiorId: "sia-tower",
    interiorStart: 0,
    activeEnergyIds: ["ai-pulse", "cross-district-gold"],
    interiorCamera: {
      position: [0, 18, 1.2],
      target: [0, 34, 0],
      fov: 44,
      lens: 26,
      frame: 96,
    },
    camera: {
      position: [0, 7.2, 3.05],
      target: [0, 25, 0],
      fov: 46,
      lens: 24,
      frame: 48,
    },
  },
  {
    scene: 4,
    slug: "fitness-district",
    scroll: 0.2,
    durationSeconds: 20,
    focus: "Fitness district",
    title: "Fitness district",
    body: "Your body tells a story every day. I read every chapter.",
    activeDistrict: "fitness",
    mode: "exterior",
    interiorId: "fitness",
    interiorStart: 0.46,
    activeEnergyIds: HARD_PIPELINE_ENERGY_IDS,
    interiorCamera: {
      position: districtCamera("fitness", [9, 5.3, -7]),
      target: districtTarget("fitness", 4.8),
      fov: 36,
      lens: 40,
      frame: 120,
    },
    camera: {
      position: districtCamera("fitness", [33, 17, -34]),
      target: districtTarget("fitness", 8),
      fov: 41,
      lens: 34,
      frame: 96,
    },
  },
  {
    scene: 5,
    slug: "yoga-sanctuary",
    scroll: 0.27,
    durationSeconds: 18,
    focus: "Yoga and wellbeing",
    title: "Yoga and wellbeing",
    body: "Calm is not the absence of energy. It is energy perfectly directed.",
    activeDistrict: "yoga",
    mode: "exterior",
    interiorId: "yoga",
    interiorStart: 0.48,
    activeEnergyIds: WARM_MIST_ENERGY_IDS,
    interiorCamera: {
      position: districtCamera("yoga", [6, 4.8, -8]),
      target: districtTarget("yoga", 3.8),
      fov: 37,
      lens: 38,
      frame: 120,
    },
    camera: {
      position: districtCamera("yoga", [26, 14, -26]),
      target: districtTarget("yoga", 5),
      fov: 40,
      lens: 34,
      frame: 96,
    },
  },
  {
    scene: 6,
    slug: "finance-tower",
    scroll: 0.34,
    durationSeconds: 18,
    focus: "Finance district",
    title: "Finance district",
    body: "Your money tells the truth about your stress. I see the pattern before your bank does.",
    activeDistrict: "finance",
    mode: "exterior",
    interiorId: "finance",
    interiorStart: 0.48,
    activeEnergyIds: HARD_PIPELINE_ENERGY_IDS,
    interiorCamera: {
      position: districtCamera("finance", [5, 7, 5]),
      target: districtTarget("finance", 5.4),
      fov: 36,
      lens: 40,
      frame: 120,
    },
    camera: {
      position: districtCamera("finance", [32, 17, 20]),
      target: districtTarget("finance", 10),
      fov: 39,
      lens: 36,
      frame: 96,
    },
  },
  {
    scene: 7,
    slug: "knowledgebase",
    scroll: 0.41,
    durationSeconds: 18,
    focus: "Knowledgebase district",
    title: "Knowledgebase district",
    body: "I never forget what works for you. Every pattern, every insight, stored and connected.",
    activeDistrict: "knowledgebase",
    mode: "exterior",
    interiorId: "knowledgebase",
    interiorStart: 0.48,
    activeEnergyIds: ["hard-pipelines", "knowledgebase-waterfall", "ai-pulse"],
    interiorCamera: {
      position: districtCamera("knowledgebase", [4, 6.5, 5]),
      target: districtTarget("knowledgebase", 5.8),
      fov: 37,
      lens: 38,
      frame: 120,
    },
    camera: {
      position: districtCamera("knowledgebase", [24, 20, 26]),
      target: districtTarget("knowledgebase", 8),
      fov: 40,
      lens: 34,
      frame: 96,
    },
  },
  {
    scene: 8,
    slug: "communication-hub",
    scroll: 0.48,
    durationSeconds: 16,
    focus: "Chat and communication",
    title: "Chat and communication",
    body: "Every conversation teaches me something about you. I listen to understand, not just respond.",
    activeDistrict: "chat",
    mode: "exterior",
    interiorId: "chat",
    interiorStart: 0.5,
    activeEnergyIds: HARD_PIPELINE_ENERGY_IDS,
    interiorCamera: {
      position: districtCamera("chat", [5, 6.2, 5]),
      target: districtTarget("chat", 5.6),
      fov: 38,
      lens: 36,
      frame: 120,
    },
    camera: {
      position: districtCamera("chat", [25, 18, 29]),
      target: districtTarget("chat", 8),
      fov: 41,
      lens: 32,
      frame: 96,
    },
  },
  {
    scene: 9,
    slug: "leaderboard-arena",
    scroll: 0.55,
    durationSeconds: 18,
    focus: "Leaderboard and competition",
    title: "Leaderboard and competition",
    body: "Twenty one days is not a streak. It is a habit. I saw it before you did.",
    activeDistrict: "leaderboard",
    mode: "exterior",
    interiorId: "leaderboard",
    interiorStart: 0.46,
    activeEnergyIds: ["hard-pipelines", "leaderboard-lightning", "ai-pulse"],
    interiorCamera: {
      position: districtCamera("leaderboard", [-2, 5.5, 6]),
      target: districtTarget("leaderboard", 4.5),
      fov: 38,
      lens: 36,
      frame: 120,
    },
    camera: {
      position: districtCamera("leaderboard", [-24, 20, 33]),
      target: districtTarget("leaderboard", 6.4),
      fov: 41,
      lens: 32,
      frame: 96,
    },
  },
  {
    scene: 10,
    slug: "relationships-garden",
    scroll: 0.62,
    durationSeconds: 18,
    focus: "Relationships district",
    title: "Relationships district",
    body: "The people in your life shape your health more than any workout. I track those connections too.",
    activeDistrict: "relationships",
    mode: "exterior",
    interiorId: "relationships",
    interiorStart: 0.48,
    activeEnergyIds: WARM_MIST_ENERGY_IDS,
    interiorCamera: {
      position: districtCamera("relationships", [7, 4.2, 7]),
      target: districtTarget("relationships", 3.8),
      fov: 38,
      lens: 36,
      frame: 120,
    },
    camera: {
      position: districtCamera("relationships", [14, 14, 30]),
      target: districtTarget("relationships", 4.3),
      fov: 41,
      lens: 32,
      frame: 96,
    },
  },
  {
    scene: 11,
    slug: "career-towers",
    scroll: 0.69,
    durationSeconds: 18,
    focus: "Career district",
    title: "Career district",
    body: "Your career does not exist in isolation. I see how sleep, stress, and relationships power your performance.",
    activeDistrict: "career",
    mode: "exterior",
    interiorId: "career",
    interiorStart: 0.48,
    activeEnergyIds: HARD_PIPELINE_ENERGY_IDS,
    interiorCamera: {
      position: districtCamera("career", [-5, 7.5, 6]),
      target: districtTarget("career", 6.8),
      fov: 36,
      lens: 40,
      frame: 120,
    },
    camera: {
      position: districtCamera("career", [-31, 25, 32]),
      target: districtTarget("career", 11.5),
      fov: 39,
      lens: 35,
      frame: 96,
    },
  },
  {
    scene: 12,
    slug: "recovery-dreamscape",
    scroll: 0.76,
    durationSeconds: 16,
    focus: "Recovery and sleep",
    title: "Recovery and sleep",
    body: "Recovery is not downtime. It is where today's patterns become tomorrow's plan.",
    activeDistrict: "recovery",
    mode: "exterior",
    interiorId: "recovery",
    interiorStart: 0.52,
    activeEnergyIds: ["faint-thread", "ai-pulse"],
    interiorCamera: {
      position: districtCamera("recovery", [-6, 4.4, 3]),
      target: districtTarget("recovery", 3.8),
      fov: 37,
      lens: 38,
      frame: 120,
    },
    camera: {
      position: districtCamera("recovery", [-32, 14, 14]),
      target: districtTarget("recovery", 5),
      fov: 39,
      lens: 35,
      frame: 96,
    },
  },
  {
    scene: 13,
    slug: "analytics-cathedral",
    scroll: 0.83,
    durationSeconds: 20,
    focus: "AI analytics",
    title: "AI analytics",
    body: "This is where I think. Every pattern, prediction, and insight starts here.",
    activeDistrict: "analytics",
    mode: "exterior",
    interiorId: "analytics",
    interiorStart: 0.46,
    activeEnergyIds: HARD_PIPELINE_ENERGY_IDS,
    interiorCamera: {
      position: districtCamera("analytics", [-5, 7.2, -5]),
      target: districtTarget("analytics", 6.4),
      fov: 36,
      lens: 40,
      frame: 120,
    },
    camera: {
      position: districtCamera("analytics", [-33, 22, -25]),
      target: districtTarget("analytics", 10.5),
      fov: 40,
      lens: 34,
      frame: 96,
    },
  },
  {
    scene: 14,
    slug: "nutrition-farm",
    scroll: 0.88,
    durationSeconds: 14,
    focus: "Nutrition district",
    title: "Nutrition district",
    body: "What you eat connects to how you sleep, think, and perform. I track the full chain.",
    activeDistrict: "nutrition",
    mode: "exterior",
    interiorId: "nutrition",
    interiorStart: 0.48,
    activeEnergyIds: HARD_PIPELINE_ENERGY_IDS,
    interiorCamera: {
      position: districtCamera("nutrition", [-5, 5.3, -5]),
      target: districtTarget("nutrition", 4.8),
      fov: 37,
      lens: 38,
      frame: 120,
    },
    camera: {
      position: districtCamera("nutrition", [-24, 15, -29]),
      target: districtTarget("nutrition", 6),
      fov: 39,
      lens: 35,
      frame: 96,
    },
  },
  {
    scene: 15,
    slug: "cross-pillar-revelation",
    scroll: 0.93,
    durationSeconds: 34,
    focus: "Cross-pillar revelation",
    title: "Cross-pillar revelation",
    body: "Most apps see one building. I see the entire civilization.",
    bodySequence: [
      "This is the complete picture.",
      "Most apps see one building. I see the entire civilization.",
      "Your sleep affects your career. Your meals shape your mood. Your relationships drive your recovery.",
      "Every dimension of human life becomes stronger when powered by intelligent AI.",
    ],
    activeDistrict: "city",
    mode: "climax",
    activeEnergyIds: ALL_ENERGY_IDS,
    camera: {
      position: [138, 124, 172],
      target: [0, 25, 5],
      fov: 47,
      lens: 16,
      frame: 144,
    },
  },
  {
    scene: 16,
    slug: "today-screen-street",
    scroll: 0.96,
    durationSeconds: 20,
    focus: "Today screen street corridor",
    title: "The Today screen",
    body: "The city resolves back into one clear daily insight.",
    activeDistrict: "chat",
    mode: "product",
    activeEnergyIds: ["hard-pipelines", "cross-district-gold", "ai-pulse"],
    camera: {
      position: districtCamera("chat", [22, 2.9, -14]),
      target: districtTarget("chat", 8),
      fov: 41,
      lens: 32,
      frame: 96,
    },
  },
  {
    scene: 17,
    slug: "sia-tower-return",
    scroll: 1,
    durationSeconds: 10,
    focus: "SIA tower return",
    title: "The closing",
    body: "Welcome to your civilization. Let us begin.",
    activeDistrict: "city",
    mode: "closing",
    activeEnergyIds: ALL_ENERGY_IDS,
    camera: {
      position: [0, 96, 198],
      target: [0, 30, 0],
      fov: 45,
      lens: 18,
      frame: 144,
    },
  },
];

const reusableVectorA = new THREE.Vector3();
const reusableVectorB = new THREE.Vector3();

export function vec3(value: Vec3) {
  return new THREE.Vector3(value[0], value[1], value[2]);
}

export function getSceneScrollSpan(scene: ScrollScene) {
  const index = SCROLL_SCENES.findIndex((candidate) => candidate.scene === scene.scene);
  const next = SCROLL_SCENES[index + 1];

  if (!next) {
    return 0.01;
  }

  return Math.max(next.scroll - scene.scroll, 0.0001);
}

export function getScrollTargetForScene(scene: ScrollScene) {
  if (scene.scene === 1 || scene.scene === SCROLL_SCENES.length) {
    return THREE.MathUtils.clamp(scene.scroll, 0, 1);
  }

  return THREE.MathUtils.clamp(scene.scroll + 0.001, 0, 1);
}

export function resolveScrollScene(progress: number) {
  const clamped = THREE.MathUtils.clamp(progress, 0, 1);
  let current = SCROLL_SCENES[0];
  let next = SCROLL_SCENES[SCROLL_SCENES.length - 1];

  for (let index = 0; index < SCROLL_SCENES.length; index += 1) {
    const scene = SCROLL_SCENES[index];
    const maybeNext = SCROLL_SCENES[index + 1] ?? scene;
    const isLastScene = index === SCROLL_SCENES.length - 1;

    if (isLastScene || (clamped >= scene.scroll && clamped < maybeNext.scroll)) {
      current = scene;
      next = maybeNext;
      break;
    }
  }

  const span = Math.max(next.scroll - current.scroll, 0.0001);
  const localProgress = THREE.MathUtils.clamp((clamped - current.scroll) / span, 0, 1);

  return { current, next, localProgress };
}

type CameraFrame = ScrollCamera & {
  at: number;
};

function sceneCameraFrames(current: ScrollScene, next: ScrollScene): CameraFrame[] {
  const frames: CameraFrame[] = [{ ...current.camera, at: 0 }];

  if (current.interiorCamera) {
    const interiorAt = THREE.MathUtils.clamp(current.interiorStart ?? 0.5, 0, 0.78);
    frames.push({ ...current.interiorCamera, at: interiorAt });
  }

  frames.push({ ...next.camera, at: 1 });

  return frames.sort((a, b) => a.at - b.at);
}

function interpolateFrameValue(start: Vec3, end: Vec3, eased: number) {
  reusableVectorA.fromArray(start);
  reusableVectorB.fromArray(end);
  return reusableVectorA.clone().lerp(reusableVectorB, eased);
}

export function interpolateCamera(progress: number) {
  const { current, next, localProgress } = resolveScrollScene(progress);
  const frames = sceneCameraFrames(current, next);
  let from = frames[0];
  let to = frames[frames.length - 1];

  for (let index = 0; index < frames.length - 1; index += 1) {
    const candidateFrom = frames[index];
    const candidateTo = frames[index + 1];

    if (localProgress >= candidateFrom.at && localProgress <= candidateTo.at) {
      from = candidateFrom;
      to = candidateTo;
      break;
    }
  }

  const span = Math.max(to.at - from.at, 0.0001);
  const segmentProgress = THREE.MathUtils.clamp((localProgress - from.at) / span, 0, 1);
  const eased = THREE.MathUtils.smoothstep(segmentProgress, 0, 1);
  const position = interpolateFrameValue(from.position, to.position, eased);
  const target = interpolateFrameValue(from.target, to.target, eased);
  const fov = THREE.MathUtils.lerp(from.fov, to.fov, eased);

  return { position, target, fov, scene: current };
}

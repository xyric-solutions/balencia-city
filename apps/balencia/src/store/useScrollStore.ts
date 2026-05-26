import { create } from "zustand";
import { ALL_ENERGY_IDS, resolveScrollScene, SCROLL_SCENES } from "../lib/scroll-scenes";
import type { ScrollScene } from "../lib/types";

export type OverlayText = {
  scene: number;
  title: string;
  body: string;
  focus: string;
  mode: string;
};

type ScrollState = {
  sceneIndex: number;
  progress: number;
  sceneLocalProgress: number;
  activeDistrict: string;
  activeInteriorId?: string;
  activeEnergyIds: readonly string[];
  hoveredDistrictId?: string;
  focusedDistrictId?: string;
  overlay: OverlayText;
  clearFocusedDistrict: (id?: string) => void;
  clearHoveredDistrict: (id?: string) => void;
  setFocusedDistrict: (id?: string) => void;
  setHoveredDistrict: (id?: string) => void;
  setScrollProgress: (progress: number) => void;
  setScene: (scene: ScrollScene) => void;
};

function sequenceBody(scene: ScrollScene, localProgress: number) {
  if (!scene.bodySequence?.length) {
    return scene.body;
  }

  const index = Math.min(
    scene.bodySequence.length - 1,
    Math.floor(localProgress * scene.bodySequence.length),
  );

  return scene.bodySequence[index];
}

function activeInteriorForScene(scene: ScrollScene, localProgress: number) {
  if (!scene.interiorId) {
    return undefined;
  }

  return localProgress >= (scene.interiorStart ?? 0.5) ? scene.interiorId : undefined;
}

function overlayFromScene(scene: ScrollScene, localProgress = 0): OverlayText {
  return {
    scene: scene.scene,
    title: scene.title,
    body: sequenceBody(scene, localProgress),
    focus: scene.focus,
    mode: scene.mode,
  };
}

const initialScene = SCROLL_SCENES[0];

export const useScrollStore = create<ScrollState>((set) => ({
  sceneIndex: initialScene.scene,
  progress: 0,
  sceneLocalProgress: 0,
  activeDistrict: initialScene.activeDistrict,
  activeInteriorId: activeInteriorForScene(initialScene, 0),
  activeEnergyIds: initialScene.activeEnergyIds ?? ALL_ENERGY_IDS,
  hoveredDistrictId: undefined,
  focusedDistrictId: undefined,
  overlay: overlayFromScene(initialScene, 0),
  clearFocusedDistrict: (id) =>
    set((state) => (!id || state.focusedDistrictId === id ? { focusedDistrictId: undefined } : {})),
  clearHoveredDistrict: (id) =>
    set((state) => (!id || state.hoveredDistrictId === id ? { hoveredDistrictId: undefined } : {})),
  setFocusedDistrict: (id) => set({ focusedDistrictId: id }),
  setHoveredDistrict: (id) => set({ hoveredDistrictId: id }),
  setScrollProgress: (progress) => {
    const { current, localProgress } = resolveScrollScene(progress);
    set({
      sceneIndex: current.scene,
      progress,
      sceneLocalProgress: localProgress,
      activeDistrict: current.activeDistrict,
      activeInteriorId: activeInteriorForScene(current, localProgress),
      activeEnergyIds: current.activeEnergyIds ?? ALL_ENERGY_IDS,
      overlay: overlayFromScene(current, localProgress),
    });
  },
  setScene: (scene) =>
    set({
      sceneIndex: scene.scene,
      sceneLocalProgress: 0,
      activeDistrict: scene.activeDistrict,
      activeInteriorId: activeInteriorForScene(scene, 0),
      activeEnergyIds: scene.activeEnergyIds ?? ALL_ENERGY_IDS,
      overlay: overlayFromScene(scene, 0),
    }),
}));

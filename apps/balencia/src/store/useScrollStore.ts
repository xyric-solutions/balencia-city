import { create } from "zustand";
import { canInteractWithDistrictInScene } from "../lib/district-metadata";
import { ALL_ENERGY_IDS, getSceneForDistrict, resolveScrollScene, SCROLL_SCENES } from "../lib/scroll-scenes";
import type { ScrollScene, Vec3 } from "../lib/types";

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
  clickInteriorId: string | undefined;
  clickInteriorCamera: { position: Vec3; target: Vec3; fov: number } | undefined;
  isClickInteriorActive: boolean;
  clickEntryScrollProgress: number | undefined;
  enterInterior: (districtId: string) => void;
  exitInterior: () => void;
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

function sceneScopedInteractionState(sceneIndex: number, state: ScrollState) {
  return {
    focusedDistrictId: canInteractWithDistrictInScene(state.focusedDistrictId, sceneIndex)
      ? state.focusedDistrictId
      : undefined,
    hoveredDistrictId: canInteractWithDistrictInScene(state.hoveredDistrictId, sceneIndex)
      ? state.hoveredDistrictId
      : undefined,
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
  clickInteriorId: undefined,
  clickInteriorCamera: undefined,
  isClickInteriorActive: false,
  clickEntryScrollProgress: undefined,
  enterInterior: (districtId) =>
    set((state) => {
      const scene = getSceneForDistrict(districtId);
      if (!scene) return {};
      if (state.clickInteriorId === districtId) {
        return {
          clickInteriorId: undefined,
          clickInteriorCamera: undefined,
          isClickInteriorActive: false,
          clickEntryScrollProgress: undefined,
        };
      }
      return {
        clickInteriorId: districtId,
        clickInteriorCamera: {
          position: scene.interiorCamera!.position,
          target: scene.interiorCamera!.target,
          fov: scene.interiorCamera!.fov,
        },
        isClickInteriorActive: true,
        clickEntryScrollProgress: state.progress,
      };
    }),
  exitInterior: () =>
    set({
      clickInteriorId: undefined,
      clickInteriorCamera: undefined,
      isClickInteriorActive: false,
      clickEntryScrollProgress: undefined,
    }),
  clearFocusedDistrict: (id) =>
    set((state) => (!id || state.focusedDistrictId === id ? { focusedDistrictId: undefined } : {})),
  clearHoveredDistrict: (id) =>
    set((state) => (!id || state.hoveredDistrictId === id ? { hoveredDistrictId: undefined } : {})),
  setFocusedDistrict: (id) =>
    set((state) => ({
      focusedDistrictId: canInteractWithDistrictInScene(id, state.sceneIndex) ? id : undefined,
    })),
  setHoveredDistrict: (id) =>
    set((state) => ({
      hoveredDistrictId: canInteractWithDistrictInScene(id, state.sceneIndex) ? id : undefined,
    })),
  setScrollProgress: (progress) => {
    const { current, localProgress } = resolveScrollScene(progress);
    set((state) => {
      const scrolledAway =
        state.clickEntryScrollProgress !== undefined &&
        Math.abs(progress - state.clickEntryScrollProgress) > 0.02;
      return {
        sceneIndex: current.scene,
        progress,
        sceneLocalProgress: localProgress,
        activeDistrict: current.activeDistrict,
        activeInteriorId: activeInteriorForScene(current, localProgress),
        activeEnergyIds: current.activeEnergyIds ?? ALL_ENERGY_IDS,
        overlay: overlayFromScene(current, localProgress),
        ...sceneScopedInteractionState(current.scene, state),
        ...(scrolledAway
          ? {
              clickInteriorId: undefined,
              clickInteriorCamera: undefined,
              isClickInteriorActive: false,
              clickEntryScrollProgress: undefined,
            }
          : {}),
      };
    });
  },
  setScene: (scene) =>
    set((state) => ({
      sceneIndex: scene.scene,
      sceneLocalProgress: 0,
      activeDistrict: scene.activeDistrict,
      activeInteriorId: activeInteriorForScene(scene, 0),
      activeEnergyIds: scene.activeEnergyIds ?? ALL_ENERGY_IDS,
      overlay: overlayFromScene(scene, 0),
      ...sceneScopedInteractionState(scene.scene, state),
    })),
}));

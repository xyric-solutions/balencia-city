import * as THREE from "three";
import type { MaterialSlot } from "./types";

export const BRAND_COLORS = {
  ink: "#0A0A0F",
  base: "#1E1E28",
  accentIdle: "#2A2A38",
  detail: "#16161E",
  glass: "#141823",
  interiorWarmth: "#FFB066",
  energy: "#FF5E00",
  forest: "#34A853",
  purple: "#7F24FF",
  gold: "#F59E0B",
} as const;

const SLOT_PATTERNS: Record<MaterialSlot, RegExp> = {
  base: /base|wall|body|structure/i,
  accent: /accent|highlight|trim/i,
  glass: /glass|window|transparent/i,
  detail: /detail|prop|furniture/i,
  emissive: /emissive|light|glow|led/i,
  energy: /energy|pipeline|conduit|vein/i,
  holo: /holo|holographic|biolum/i,
};

type SlotAppearance = {
  color: string;
  roughness: number;
  metalness: number;
  emissive: string;
  emissiveIntensity: number;
  opacity: number;
  transparent: boolean;
  toneMapped: boolean;
  envMapIntensity: number;
};

function mixHexColors(first: string, second: string, amount: number) {
  return new THREE.Color(first).lerp(new THREE.Color(second), amount).getStyle();
}

export function normalizeMaterialSlot(materialName = ""): MaterialSlot {
  const root = materialName.split(".")[0].toLowerCase();

  if (root in SLOT_PATTERNS) {
    return root as MaterialSlot;
  }

  for (const [slot, pattern] of Object.entries(SLOT_PATTERNS) as [MaterialSlot, RegExp][]) {
    if (pattern.test(root)) {
      return slot;
    }
  }

  return "detail";
}

export function getSlotAppearance(
  slot: MaterialSlot,
  districtColor: string,
  active: boolean,
  energyColor: string = BRAND_COLORS.energy,
): SlotAppearance {
  const inactive: Record<MaterialSlot, SlotAppearance> = {
    base: {
      color: BRAND_COLORS.base,
      roughness: 0.62,
      metalness: 0.12,
      emissive: BRAND_COLORS.base,
      emissiveIntensity: active ? 0.018 : 0.03,
      opacity: 1,
      transparent: false,
      toneMapped: true,
      envMapIntensity: 0.4,
    },
    accent: {
      color: active ? districtColor : mixHexColors(BRAND_COLORS.accentIdle, districtColor, 0.18),
      roughness: 0.38,
      metalness: 0.35,
      emissive: districtColor,
      emissiveIntensity: active ? 0.34 : 0.035,
      opacity: 1,
      transparent: false,
      toneMapped: true,
      envMapIntensity: 0.6,
    },
    glass: {
      color: BRAND_COLORS.glass,
      roughness: 0.05,
      metalness: 0.92,
      emissive: BRAND_COLORS.interiorWarmth,
      emissiveIntensity: active ? 0.18 : 0.1,
      opacity: active ? 0.96 : 0.98,
      transparent: true,
      toneMapped: true,
      envMapIntensity: 1.8,
    },
    detail: {
      color: BRAND_COLORS.detail,
      roughness: 0.48,
      metalness: 0.2,
      emissive: BRAND_COLORS.detail,
      emissiveIntensity: active ? 0.012 : 0.015,
      opacity: 1,
      transparent: false,
      toneMapped: true,
      envMapIntensity: 0.3,
    },
    emissive: {
      color: districtColor,
      roughness: 0.3,
      metalness: 0,
      emissive: districtColor,
      emissiveIntensity: active ? 1.05 : 0.1,
      opacity: 1,
      transparent: false,
      toneMapped: !active,
      envMapIntensity: 0.1,
    },
    energy: {
      color: energyColor,
      roughness: 0.2,
      metalness: 0,
      emissive: energyColor,
      emissiveIntensity: active ? 1.1 : 0.05,
      opacity: 1,
      transparent: false,
      toneMapped: !active,
      envMapIntensity: 0.15,
    },
    holo: {
      color: districtColor,
      roughness: 0.1,
      metalness: 0,
      emissive: districtColor,
      emissiveIntensity: active ? 0.8 : 0.15,
      opacity: active ? 0.6 : 0.4,
      transparent: true,
      toneMapped: true,
      envMapIntensity: 0.5,
    },
  };

  return inactive[slot];
}

function applyAppearance(material: THREE.Material, appearance: SlotAppearance) {
  const standard = material as THREE.MeshStandardMaterial;

  if ("color" in standard) {
    standard.color = new THREE.Color(appearance.color);
  }
  if ("roughness" in standard) {
    standard.roughness = appearance.roughness;
  }
  if ("metalness" in standard) {
    standard.metalness = appearance.metalness;
  }
  if ("emissive" in standard) {
    standard.emissive = new THREE.Color(appearance.emissive);
  }
  if ("emissiveIntensity" in standard) {
    standard.emissiveIntensity = appearance.emissiveIntensity;
  }
  if ("envMapIntensity" in standard) {
    standard.envMapIntensity = appearance.envMapIntensity;
  }

  standard.opacity = appearance.opacity;
  standard.transparent = appearance.transparent;
  standard.depthWrite = !appearance.transparent;
  standard.toneMapped = appearance.toneMapped;
  standard.side = THREE.DoubleSide;
  standard.needsUpdate = true;
}

function forEachMeshMaterial(root: THREE.Object3D, callback: (material: THREE.Material) => void) {
  root.traverse((object) => {
    const mesh = object as THREE.Mesh;
    if (!mesh.isMesh || !mesh.material) {
      return;
    }

    if (Array.isArray(mesh.material)) {
      mesh.material.forEach(callback);
      return;
    }

    callback(mesh.material);
  });
}

export function applyBalenciaMaterialOverrides(root: THREE.Object3D, districtColor: string, active: boolean) {
  forEachMeshMaterial(root, (material) => {
    const slot = normalizeMaterialSlot(material.name);
    applyAppearance(material, getSlotAppearance(slot, districtColor, active));
  });
}

export function applyEnergyMaterialOverrides(
  root: THREE.Object3D,
  displayColor: string,
  active = true,
  emissionStrength?: number,
) {
  forEachMeshMaterial(root, (material) => {
    const appearance = getSlotAppearance("energy", displayColor, active, displayColor);
    applyAppearance(material, {
      ...appearance,
      emissiveIntensity: emissionStrength ?? appearance.emissiveIntensity,
      toneMapped: false,
    });
  });
}

let cachedQualityTier: "high" | "medium" | "low" | null = null;

export function getDeviceQualityTier(): "high" | "medium" | "low" {
  if (cachedQualityTier) return cachedQualityTier;
  if (typeof navigator === "undefined") {
    cachedQualityTier = "high";
    return cachedQualityTier;
  }
  const canvas = document.createElement("canvas");
  const gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
  if (!gl) {
    cachedQualityTier = "low";
    return cachedQualityTier;
  }
  const debugInfo = gl.getExtension("WEBGL_debug_renderer_info");
  const renderer = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "";
  if (/Mali|Adreno|PowerVR|Apple GPU/i.test(renderer)) {
    cachedQualityTier = "medium";
    return cachedQualityTier;
  }
  if (/Intel|Iris/i.test(renderer)) {
    cachedQualityTier = "medium";
    return cachedQualityTier;
  }
  cachedQualityTier = "high";
  return cachedQualityTier;
}

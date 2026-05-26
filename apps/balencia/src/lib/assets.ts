import manifestJson from "./asset-manifest.json";
import { applyCityLayoutPosition } from "./city-layout-v2";
import type { AssetManifest, EnergyAsset, StructureAsset } from "./types";

export const assetManifest = manifestJson as unknown as AssetManifest;

export const approvedStructures = assetManifest.structures.map(applyCityLayoutPosition) satisfies StructureAsset[];
export const approvedEnergyAssets = assetManifest.energyAssets satisfies EnergyAsset[];

export const structureById = new Map(approvedStructures.map((structure) => [structure.id, structure]));

export function getStructureById(id: string) {
  return structureById.get(id);
}

export function getEagerModelPaths() {
  return approvedStructures.map((structure) => structure.exterior.runtimePath);
}

export function getOnDemandInteriorPaths() {
  return approvedStructures.map((structure) => structure.interior.runtimePath);
}

export function getEnergyModelPaths() {
  return approvedEnergyAssets.map((asset) => asset.runtimePath);
}

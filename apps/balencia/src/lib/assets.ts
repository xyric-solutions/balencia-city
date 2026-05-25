import manifestJson from "./asset-manifest.json";
import type { AssetManifest, EnergyAsset, StructureAsset } from "./types";

export const assetManifest = manifestJson as unknown as AssetManifest;

export const approvedStructures = assetManifest.structures satisfies StructureAsset[];
export const approvedEnergyAssets = assetManifest.energyAssets satisfies EnergyAsset[];

export const structureById = new Map(approvedStructures.map((structure) => [structure.id, structure]));

export function getStructureById(id: string) {
  return structureById.get(id);
}

export function getEagerModelPaths() {
  return [
    ...approvedStructures.map((structure) => structure.exterior.runtimePath),
    ...approvedEnergyAssets.map((asset) => asset.runtimePath),
  ];
}

export function getOnDemandInteriorPaths() {
  return approvedStructures.map((structure) => structure.interior.runtimePath);
}

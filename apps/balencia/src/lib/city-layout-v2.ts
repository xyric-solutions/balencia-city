import layoutJson from "../../../../shared/city-layout-v2.json";
import type { StructureAsset, Vec3 } from "./types";

type LayoutDistrict = {
  runtimePosition: number[];
  blenderPosition: number[];
  ring: "core" | "outer";
};

type CityLayout = {
  version: string;
  session: number;
  minimumDistrictSpacing: number;
  island: {
    radiusX: number;
    radiusZ: number;
    innerCivicRadius: number;
    outerRoadRadius: number;
    edgeWallRadius: number;
  };
  districts: Record<string, LayoutDistrict>;
};

export const CITY_LAYOUT_V2 = layoutJson as CityLayout;
export const CITY_LAYOUT_VERSION = CITY_LAYOUT_V2.version;
export const CITY_LAYOUT_ISLAND = CITY_LAYOUT_V2.island;

function toVec3(value: number[]): Vec3 {
  return [value[0] ?? 0, value[1] ?? 0, value[2] ?? 0];
}

export function getLayoutDistrict(id: string) {
  return CITY_LAYOUT_V2.districts[id];
}

export function getRuntimePosition(id: string): Vec3 {
  return toVec3(getLayoutDistrict(id)?.runtimePosition ?? [0, 0, 0]);
}

export function getBlenderPosition(id: string): Vec3 {
  return toVec3(getLayoutDistrict(id)?.blenderPosition ?? [0, 0, 0]);
}

export function applyCityLayoutPosition<T extends StructureAsset>(structure: T): T {
  const district = getLayoutDistrict(structure.id);

  if (!district) {
    return structure;
  }

  return {
    ...structure,
    blenderPosition: toVec3(district.blenderPosition),
    position: toVec3(district.runtimePosition),
  } as T;
}

export function layoutPoint(id: string, y = 0): Vec3 {
  const [x, , z] = getRuntimePosition(id);
  return [x, y, z];
}

export function layoutOffset(id: string, [x, y, z]: Vec3): Vec3 {
  const [baseX, , baseZ] = getRuntimePosition(id);
  return [baseX + x, y, baseZ + z];
}

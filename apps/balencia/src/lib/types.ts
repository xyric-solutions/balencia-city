export type Vec3 = readonly [number, number, number];

export type ModelReference = {
  name: string;
  sourcePath: string;
  publicPath: string;
  runtimePath: string;
};

export type StructureAsset = {
  id: string;
  assemblyName: string;
  label: string;
  hex: string;
  blenderPosition: Vec3;
  position: Vec3;
  exterior: ModelReference;
  interior: ModelReference;
};

export type EnergyAsset = {
  id: string;
  label: string;
  materialKey: "energy";
  displayColor: string;
  sourcePath: string;
  publicPath: string;
  runtimePath: string;
};

export type AssetManifest = {
  session: number;
  sourceOfTruth: Record<string, string>;
  structures: StructureAsset[];
  energyAssets: EnergyAsset[];
};

export type MaterialSlot =
  | "base"
  | "accent"
  | "glass"
  | "detail"
  | "emissive"
  | "energy"
  | "holo";

export type ScrollCamera = {
  position: Vec3;
  target: Vec3;
  fov: number;
  lens: number;
  frame: number;
};

export type ScrollSceneMode = "city" | "exterior" | "interior" | "climax" | "product" | "closing";

export type ScrollScene = {
  scene: number;
  slug: string;
  scroll: number;
  durationSeconds: number;
  focus: string;
  title: string;
  body: string;
  bodySequence?: readonly string[];
  activeDistrict: string;
  mode: ScrollSceneMode;
  interiorId?: string;
  interiorStart?: number;
  interiorCamera?: ScrollCamera;
  activeEnergyIds?: readonly string[];
  camera: ScrollCamera;
};

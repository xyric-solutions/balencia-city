export type EnclosureShape = "box" | "cylinder" | "hexPrism" | "octPrism" | "tapered";

export type MotionStyle = "pulse" | "breathe" | "data-stream" | "steady";

export type FacadeStyle = "glass-curtain" | "metal-panel" | "crystalline" | "organic" | "industrial";

export type EnclosureProfile = {
  shape: EnclosureShape;
  width: number;
  depth: number;
  height: number;
  taperTop?: number;
  coreInset: number;
  shellOpacity: number;
  shellEmissive: number;
  coreOpacity: number;
  coreEmissive: number;
  floorCount: number;
  lightIntensity: number;
  yOffset: number;
  rotationY: number;
  rimPower: number;
  rimIntensity: number;
  windowRows: number;
  windowCols: number;
  motionStyle: MotionStyle;
  facadeStyle: FacadeStyle;
  panelColumns: number;
  panelRows: number;
  shellTint?: string;
  windowWarmth: number;
};

export const ENCLOSURE_PROFILES: Record<string, EnclosureProfile> = {
  "sia-tower": {
    shape: "tapered",
    width: 6.2, depth: 5.4, height: 42.5,
    taperTop: 0.55,
    coreInset: 0.8,
    shellOpacity: 0.78, shellEmissive: 0.14,
    coreOpacity: 0.92, coreEmissive: 0.14,
    floorCount: 22,
    lightIntensity: 12,
    yOffset: 0, rotationY: Math.PI / 4,
    rimPower: 2.5, rimIntensity: 1.0,
    windowRows: 32, windowCols: 14,
    motionStyle: "pulse",
    facadeStyle: "crystalline",
    panelColumns: 16, panelRows: 44,
    windowWarmth: 0.75,
  },
  fitness: {
    shape: "box",
    width: 9.4, depth: 8.4, height: 13.5,
    coreInset: 0.6,
    shellOpacity: 0.72, shellEmissive: 0.10,
    coreOpacity: 0.90, coreEmissive: 0.12,
    floorCount: 8,
    lightIntensity: 10,
    yOffset: 0, rotationY: 0,
    rimPower: 2.5, rimIntensity: 0.8,
    windowRows: 12, windowCols: 18,
    motionStyle: "steady",
    facadeStyle: "industrial",
    panelColumns: 12, panelRows: 16,
    windowWarmth: 0.9,
  },
  yoga: {
    shape: "cylinder",
    width: 12.5, depth: 9.4, height: 7.8,
    coreInset: 0.5,
    shellOpacity: 0.58, shellEmissive: 0.08,
    coreOpacity: 0.88, coreEmissive: 0.1,
    floorCount: 4,
    lightIntensity: 8,
    yOffset: 0.3, rotationY: 0,
    rimPower: 1.8, rimIntensity: 0.5,
    windowRows: 6, windowCols: 16,
    motionStyle: "breathe",
    facadeStyle: "organic",
    panelColumns: 0, panelRows: 0,
    shellTint: "#161a20",
    windowWarmth: 0.5,
  },
  finance: {
    shape: "hexPrism",
    width: 6.2, depth: 6.2, height: 16.8,
    coreInset: 0.5,
    shellOpacity: 0.82, shellEmissive: 0.12,
    coreOpacity: 0.92, coreEmissive: 0.14,
    floorCount: 10,
    lightIntensity: 10,
    yOffset: 0, rotationY: 0,
    rimPower: 2.5, rimIntensity: 0.95,
    windowRows: 16, windowCols: 18,
    motionStyle: "data-stream",
    facadeStyle: "crystalline",
    panelColumns: 18, panelRows: 20,
    shellTint: "#1a1820",
    windowWarmth: 0.75,
  },
  knowledgebase: {
    shape: "box",
    width: 8.8, depth: 7.6, height: 15.2,
    coreInset: 0.6,
    shellOpacity: 0.72, shellEmissive: 0.10,
    coreOpacity: 0.90, coreEmissive: 0.12,
    floorCount: 9,
    lightIntensity: 10,
    yOffset: 0, rotationY: 0,
    rimPower: 2.5, rimIntensity: 0.8,
    windowRows: 14, windowCols: 18,
    motionStyle: "data-stream",
    facadeStyle: "metal-panel",
    panelColumns: 14, panelRows: 18,
    windowWarmth: 0.75,
  },
  chat: {
    shape: "cylinder",
    width: 12.6, depth: 9.2, height: 13.2,
    coreInset: 0.6,
    shellOpacity: 0.68, shellEmissive: 0.10,
    coreOpacity: 0.90, coreEmissive: 0.14,
    floorCount: 8,
    lightIntensity: 11,
    yOffset: 0, rotationY: 0,
    rimPower: 2.5, rimIntensity: 0.8,
    windowRows: 12, windowCols: 16,
    motionStyle: "pulse",
    facadeStyle: "glass-curtain",
    panelColumns: 16, panelRows: 16,
    windowWarmth: 0.75,
  },
  leaderboard: {
    shape: "cylinder",
    width: 13.8, depth: 13.8, height: 7.0,
    coreInset: 0.5,
    shellOpacity: 0.62, shellEmissive: 0.09,
    coreOpacity: 0.88, coreEmissive: 0.09,
    floorCount: 4,
    lightIntensity: 8,
    yOffset: 0, rotationY: 0,
    rimPower: 3.0, rimIntensity: 0.6,
    windowRows: 8, windowCols: 14,
    motionStyle: "pulse",
    facadeStyle: "glass-curtain",
    panelColumns: 20, panelRows: 8,
    windowWarmth: 0.75,
  },
  relationships: {
    shape: "cylinder",
    width: 13.4, depth: 10.8, height: 6.7,
    coreInset: 0.5,
    shellOpacity: 0.60, shellEmissive: 0.08,
    coreOpacity: 0.88, coreEmissive: 0.1,
    floorCount: 4,
    lightIntensity: 8,
    yOffset: 0, rotationY: 0,
    rimPower: 1.8, rimIntensity: 0.55,
    windowRows: 18, windowCols: 18,
    motionStyle: "breathe",
    facadeStyle: "organic",
    panelColumns: 0, panelRows: 0,
    windowWarmth: 0.65,
  },
  career: {
    shape: "box",
    width: 11.2, depth: 8.8, height: 19.4,
    coreInset: 0.7,
    shellOpacity: 0.75, shellEmissive: 0.12,
    coreOpacity: 0.92, coreEmissive: 0.13,
    floorCount: 12,
    lightIntensity: 12,
    yOffset: 0, rotationY: 0,
    rimPower: 2.5, rimIntensity: 0.9,
    windowRows: 10, windowCols: 12,
    motionStyle: "steady",
    facadeStyle: "metal-panel",
    panelColumns: 16, panelRows: 24,
    windowWarmth: 0.75,
  },
  recovery: {
    shape: "cylinder",
    width: 14.4, depth: 11.2, height: 6.4,
    coreInset: 0.5,
    shellOpacity: 0.55, shellEmissive: 0.08,
    coreOpacity: 0.85, coreEmissive: 0.08,
    floorCount: 3,
    lightIntensity: 7,
    yOffset: 1.5, rotationY: 0,
    rimPower: 1.8, rimIntensity: 0.45,
    windowRows: 5, windowCols: 12,
    motionStyle: "breathe",
    facadeStyle: "organic",
    panelColumns: 0, panelRows: 0,
    shellTint: "#18161e",
    windowWarmth: 0.3,
  },
  analytics: {
    shape: "octPrism",
    width: 9.4, depth: 12.4, height: 17.4,
    coreInset: 0.6,
    shellOpacity: 0.74, shellEmissive: 0.10,
    coreOpacity: 0.90, coreEmissive: 0.12,
    floorCount: 11,
    lightIntensity: 10,
    yOffset: 0, rotationY: 0,
    rimPower: 2.5, rimIntensity: 0.85,
    windowRows: 16, windowCols: 24,
    motionStyle: "data-stream",
    facadeStyle: "crystalline",
    panelColumns: 24, panelRows: 22,
    windowWarmth: 0.4,
  },
  nutrition: {
    shape: "box",
    width: 13.2, depth: 11.2, height: 10.2,
    coreInset: 0.6,
    shellOpacity: 0.65, shellEmissive: 0.09,
    coreOpacity: 0.88, coreEmissive: 0.12,
    floorCount: 6,
    lightIntensity: 9,
    yOffset: 0, rotationY: 0,
    rimPower: 2.8, rimIntensity: 0.7,
    windowRows: 8, windowCols: 18,
    motionStyle: "steady",
    facadeStyle: "glass-curtain",
    panelColumns: 18, panelRows: 12,
    shellTint: "#161a18",
    windowWarmth: 0.75,
  },
};

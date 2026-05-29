import { useFrame } from "@react-three/fiber";
import { useEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import { createFresnelShellMaterial } from "../../lib/enclosure-materials";
import { ENCLOSURE_PROFILES, type EnclosureProfile, type MotionStyle } from "../../lib/enclosure-profiles";
import { AI_PULSE_TIMING } from "../../lib/energy-system";
import { BRAND_COLORS, getDeviceQualityTier } from "../../lib/materials";
import type { StructureAsset } from "../../lib/types";

type QualityTier = "high" | "medium" | "low";

const LERP_SPEED = 0.04;
const HOVER_SCALE = 1.02;
const HOVER_RIM_MULT = 1.3;
const FADE_SPEED = 0.06;
const WINDOW_GEO = new THREE.PlaneGeometry(0.30, 0.42);

function cylinderSegments(shape: string, tier: QualityTier) {
  if (shape === "hexPrism") return 6;
  if (shape === "octPrism") return 8;
  if (shape === "tapered") return 4;
  if (tier === "low") return 12;
  if (tier === "medium") return 20;
  return 32;
}

function createGeometry(profile: EnclosureProfile, inset: number, tier: QualityTier): THREE.BufferGeometry {
  const w = Math.max(0.4, profile.width - inset * 2);
  const d = Math.max(0.4, profile.depth - inset * 2);
  const h = Math.max(0.4, profile.height - inset);

  if (profile.shape === "box") {
    return new THREE.BoxGeometry(w, h, d);
  }

  const segments = cylinderSegments(profile.shape, tier);
  const baseR = Math.max(w, d) / 2;

  if (profile.shape === "tapered") {
    const topR = baseR * (profile.taperTop ?? 0.6);
    return new THREE.CylinderGeometry(topR, baseR, h, segments);
  }

  return new THREE.CylinderGeometry(baseR, baseR, h, segments);
}

function footprintScale(profile: EnclosureProfile, inset: number): [number, number, number] {
  if (profile.shape === "box") return [1, 1, 1];
  const w = Math.max(0.4, profile.width - inset * 2);
  const d = Math.max(0.4, profile.depth - inset * 2);
  const maxDim = Math.max(w, d);
  return [w / maxDim, 1, d / maxDim];
}

function FloorPlates({
  active,
  hex,
  motionStyle,
  profile,
  sceneIndex,
}: {
  active: boolean;
  hex: string;
  motionStyle: MotionStyle;
  profile: EnclosureProfile;
  sceneIndex: number;
}) {
  const meshRef = useRef<THREE.InstancedMesh | null>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const colorArray = useMemo(() => {
    const c = new THREE.Color(hex);
    const arr = new Float32Array(profile.floorCount * 3);
    for (let i = 0; i < profile.floorCount; i++) {
      arr[i * 3] = c.r;
      arr[i * 3 + 1] = c.g;
      arr[i * 3 + 2] = c.b;
    }
    return arr;
  }, [hex, profile.floorCount]);

  const tempColor = useMemo(() => new THREE.Color(hex), [hex]);

  const planeGeo = useMemo(() => {
    if (profile.shape === "box") return new THREE.PlaneGeometry(1, 1);
    const segs = profile.shape === "hexPrism" ? 6 : profile.shape === "octPrism" ? 8 : 32;
    return new THREE.CircleGeometry(0.5, segs);
  }, [profile.shape]);

  const prevSceneRef = useRef(sceneIndex);
  const cascadeProgress = useRef(1);

  useEffect(() => {
    if (prevSceneRef.current !== sceneIndex) {
      if (active) {
        cascadeProgress.current = 0;
      }
      prevSceneRef.current = sceneIndex;
    }
  }, [sceneIndex, active]);

  useEffect(() => {
    const mesh = meshRef.current;
    if (!mesh) return;

    const inset = profile.coreInset + 0.15;
    const w = Math.max(0.4, profile.width - inset * 2);
    const d = Math.max(0.4, profile.depth - inset * 2);
    const gap = profile.height / (profile.floorCount + 1);

    for (let i = 0; i < profile.floorCount; i++) {
      const t = (i + 1) / (profile.floorCount + 1);
      const taper = profile.taperTop ? THREE.MathUtils.lerp(1, profile.taperTop, t) : 1;

      dummy.position.set(0, gap * (i + 1) - profile.height / 2, 0);
      dummy.rotation.set(-Math.PI / 2, 0, 0);
      dummy.scale.set(w * taper, d * taper, 1);
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    }

    mesh.instanceMatrix.needsUpdate = true;

    mesh.instanceColor = new THREE.InstancedBufferAttribute(colorArray, 3);
    mesh.instanceColor.needsUpdate = true;
  }, [dummy, profile, colorArray]);

  useFrame(({ clock }, delta) => {
    const mesh = meshRef.current;
    if (!mesh || !mesh.instanceColor) return;

    if (cascadeProgress.current < 1) {
      cascadeProgress.current = Math.min(1, cascadeProgress.current + delta * 2.0);
    }

    const time = clock.elapsedTime;
    const fc = profile.floorCount;
    const cascadeDone = cascadeProgress.current >= 1;

    const isDataStream = motionStyle === "data-stream";
    const waveSpeed = isDataStream ? 0.8 : 0.4;
    const wavePos = isDataStream
      ? 1.0 - (time * waveSpeed) % 1.0
      : (time * waveSpeed) % 1.0;
    const waveAmp = active ? 0.3 : 0.1;
    const baseBrightness = active ? 0.18 : 0.08;

    let changed = false;

    for (let i = 0; i < fc; i++) {
      const plateNormY = (i + 0.5) / fc;

      let cascade = 1;
      if (!cascadeDone) {
        cascade = THREE.MathUtils.clamp((cascadeProgress.current - i / fc) * 4, 0, 1);
      }

      const dist = (plateNormY - wavePos) * fc;
      const wave = 1.0 + waveAmp * Math.exp(-(dist * dist) / 2);

      const brightness = baseBrightness * cascade * wave;

      const idx = i * 3;
      const nr = tempColor.r * brightness;
      const ng = tempColor.g * brightness;
      const nb = tempColor.b * brightness;

      if (Math.abs(colorArray[idx] - nr) > 0.001 ||
          Math.abs(colorArray[idx + 1] - ng) > 0.001 ||
          Math.abs(colorArray[idx + 2] - nb) > 0.001) {
        colorArray[idx] = nr;
        colorArray[idx + 1] = ng;
        colorArray[idx + 2] = nb;
        changed = true;
      }
    }

    if (changed) {
      mesh.instanceColor.needsUpdate = true;
    }
  });

  return (
    <instancedMesh ref={meshRef} args={[planeGeo, undefined, profile.floorCount]}>
      <meshBasicMaterial
        color="#FFFFFF"
        opacity={0.75}
        transparent
        side={THREE.DoubleSide}
        depthWrite={false}
        toneMapped={false}
      />
    </instancedMesh>
  );
}

const BAND_MAT = new THREE.MeshStandardMaterial({
  color: "#0E0E14",
  metalness: 0.6,
  roughness: 0.4,
  emissive: "#0E0E14",
  emissiveIntensity: 0.02,
  opacity: 0.85,
  transparent: true,
  depthWrite: false,
});

function FacadeBands({
  profile,
  tier,
}: {
  profile: EnclosureProfile;
  tier: QualityTier;
}) {
  const meshRef = useRef<THREE.InstancedMesh | null>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  if (tier === "low") return null;

  const bandCount = tier === "medium" ? Math.ceil(profile.floorCount / 2) : profile.floorCount;

  const bandGeo = useMemo(() => {
    if (profile.shape === "box") {
      return new THREE.PlaneGeometry(1, 0.08);
    }
    const segs = profile.shape === "hexPrism" ? 6 : profile.shape === "octPrism" ? 8 : 32;
    return new THREE.CylinderGeometry(1, 1, 0.08, segs, 1, true);
  }, [profile.shape]);

  const totalInstances = profile.shape === "box" ? bandCount * 4 : bandCount;

  useEffect(() => {
    const mesh = meshRef.current;
    if (!mesh) return;

    const inset = profile.coreInset + 0.05;
    const w = Math.max(0.4, profile.width - inset * 2);
    const d = Math.max(0.4, profile.depth - inset * 2);
    const gap = profile.height / (profile.floorCount + 1);
    const halfH = profile.height / 2;
    const step = tier === "medium" ? 2 : 1;

    let idx = 0;
    for (let fi = 0; fi < profile.floorCount; fi += step) {
      const y = -halfH + gap * (fi + 1);
      const t = (fi + 1) / (profile.floorCount + 1);
      const taper = profile.taperTop ? THREE.MathUtils.lerp(1, profile.taperTop, t) : 1;

      if (profile.shape === "box") {
        const faces = [
          { px: 0, pz: d / 2 * taper, ry: 0, fw: w * taper },
          { px: 0, pz: -d / 2 * taper, ry: 0, fw: w * taper },
          { px: w / 2 * taper, pz: 0, ry: Math.PI / 2, fw: d * taper },
          { px: -w / 2 * taper, pz: 0, ry: Math.PI / 2, fw: d * taper },
        ];
        for (const face of faces) {
          dummy.position.set(face.px, y, face.pz);
          dummy.rotation.set(0, face.ry, 0);
          dummy.scale.set(face.fw, 1, 1);
          dummy.updateMatrix();
          mesh.setMatrixAt(idx++, dummy.matrix);
        }
      } else {
        const rw = Math.max(w, d) / 2 * taper;
        dummy.position.set(0, y, 0);
        dummy.rotation.set(0, 0, 0);
        dummy.scale.set(rw, 1, rw);
        dummy.updateMatrix();
        mesh.setMatrixAt(idx++, dummy.matrix);
      }
    }

    mesh.instanceMatrix.needsUpdate = true;
  }, [dummy, profile, tier]);

  return (
    <instancedMesh ref={meshRef} args={[bandGeo, BAND_MAT, totalInstances]} renderOrder={1} />
  );
}

const BASE_GLOW_GEO = new THREE.CircleGeometry(1, 32);
const BASE_GLOW_OUTER_GEO = new THREE.CircleGeometry(1, 32);
const ACCENT_GEO = new THREE.SphereGeometry(0.15, 8, 8);

function EnclosureBaseGlow({
  active,
  hex,
  profile,
}: {
  active: boolean;
  hex: string;
  profile: EnclosureProfile;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const outerMeshRef = useRef<THREE.Mesh>(null);
  const outerMatRef = useRef<THREE.MeshBasicMaterial>(null);
  const opacityCurrent = useRef(active ? 0.25 : 0.12);
  const outerOpacityCurrent = useRef(active ? 0.08 : 0.03);

  useFrame(({ clock }) => {
    const mat = matRef.current;
    const mesh = meshRef.current;
    const outerMat = outerMatRef.current;
    const outerMesh = outerMeshRef.current;
    if (!mat || !mesh) return;

    const target = active ? 0.25 : 0.12;
    opacityCurrent.current = THREE.MathUtils.lerp(opacityCurrent.current, target, LERP_SPEED);
    mat.opacity = opacityCurrent.current;

    const outerTarget = active ? 0.08 : 0.03;
    outerOpacityCurrent.current = THREE.MathUtils.lerp(outerOpacityCurrent.current, outerTarget, LERP_SPEED);
    if (outerMat) outerMat.opacity = outerOpacityCurrent.current;

    const breath = 0.95 + 0.1 * Math.sin(clock.elapsedTime * 0.5);
    mesh.scale.set(breath, breath, 1);
    if (outerMesh) outerMesh.scale.set(breath, breath, 1);
  });

  const radius = Math.max(profile.width, profile.depth) * 0.55;
  const outerRadius = radius * 1.4;

  return (
    <>
      <mesh
        ref={outerMeshRef}
        geometry={BASE_GLOW_OUTER_GEO}
        position={[0, -profile.height / 2 + 0.04, 0]}
        rotation={[-Math.PI / 2, 0, 0]}
        scale={[outerRadius, outerRadius, 1]}
        renderOrder={-5}
      >
        <meshBasicMaterial
          ref={outerMatRef}
          color={hex}
          opacity={outerOpacityCurrent.current}
          transparent
          depthWrite={false}
          toneMapped={false}
        />
      </mesh>
      <mesh
        ref={meshRef}
        geometry={BASE_GLOW_GEO}
        position={[0, -profile.height / 2 + 0.05, 0]}
        rotation={[-Math.PI / 2, 0, 0]}
        scale={[radius, radius, 1]}
        renderOrder={-4}
      >
        <meshBasicMaterial
          ref={matRef}
          color={hex}
          opacity={opacityCurrent.current}
          transparent
          depthWrite={false}
          toneMapped={false}
        />
      </mesh>
    </>
  );
}

function RooftopAccent({
  active,
  hex,
  motionStyle,
  profile,
}: {
  active: boolean;
  hex: string;
  motionStyle: MotionStyle;
  profile: EnclosureProfile;
}) {
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const opacityCurrent = useRef(active ? 0.8 : 0.4);

  useFrame(({ clock }) => {
    const mat = matRef.current;
    if (!mat) return;

    const t = clock.elapsedTime;
    const baseTarget = active ? 0.8 : 0.4;
    let pulse: number;
    switch (motionStyle) {
      case "pulse":
        pulse = Math.sin(t * 3) * 0.1;
        break;
      case "breathe":
        pulse = Math.sin(t * 1.2) * 0.1;
        break;
      case "data-stream":
        pulse = (Math.sin(t * 6) > 0.3 ? 1 : 0) * 0.15 - 0.075;
        break;
      default:
        pulse = Math.sin(t * 2) * 0.1;
    }
    const target = baseTarget + pulse;
    opacityCurrent.current = THREE.MathUtils.lerp(opacityCurrent.current, target, LERP_SPEED);
    mat.opacity = opacityCurrent.current;
  });

  return (
    <mesh
      geometry={ACCENT_GEO}
      position={[0, profile.height / 2, 0]}
      renderOrder={-1}
    >
      <meshBasicMaterial
        ref={matRef}
        color={hex}
        opacity={opacityCurrent.current}
        transparent
        depthWrite={false}
        toneMapped={false}
      />
    </mesh>
  );
}

function EnclosureUplight({
  active,
  hex,
  profile,
}: {
  active: boolean;
  hex: string;
  profile: EnclosureProfile;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const opacityCurrent = useRef(active ? 0.04 : 0);

  const geo = useMemo(
    () => new THREE.CylinderGeometry(0, profile.width * 0.4, profile.height * 0.6, 16, 1, true),
    [profile.width, profile.height],
  );

  useFrame(({ clock }) => {
    const mesh = meshRef.current;
    const mat = matRef.current;
    if (!mesh || !mat) return;

    const time = clock.elapsedTime;
    mesh.rotation.y = time * 0.3;

    const target = active ? 0.03 + Math.sin(time * 0.8) * 0.015 : 0;
    opacityCurrent.current = THREE.MathUtils.lerp(opacityCurrent.current, target, LERP_SPEED);
    mat.opacity = opacityCurrent.current;
  });

  return (
    <mesh
      ref={meshRef}
      geometry={geo}
      position={[0, profile.height / 2 + profile.height * 0.1, 0]}
    >
      <meshBasicMaterial
        ref={matRef}
        color={hex}
        opacity={opacityCurrent.current}
        transparent
        blending={THREE.AdditiveBlending}
        side={THREE.DoubleSide}
        depthWrite={false}
        toneMapped={false}
      />
    </mesh>
  );
}

function EnclosureAtmosphere({
  active,
  hex,
  profile,
}: {
  active: boolean;
  hex: string;
  profile: EnclosureProfile;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const opacityCurrent = useRef(active ? 0.07 : 0.035);

  const geo = useMemo(() => {
    const r = Math.max(profile.width, profile.depth) * 0.5;
    const tube = Math.max(profile.width, profile.depth) * 0.15;
    return new THREE.TorusGeometry(r, tube, 8, 32);
  }, [profile.width, profile.depth]);

  useFrame(({ clock }) => {
    const mesh = meshRef.current;
    const mat = matRef.current;
    if (!mesh || !mat) return;

    const time = clock.elapsedTime;
    mesh.rotation.z = time * 0.15;
    const breath = 1 + Math.sin(time * 0.4) * 0.03;
    mesh.scale.set(breath, breath, breath);

    const target = active ? 0.07 : 0.035;
    opacityCurrent.current = THREE.MathUtils.lerp(opacityCurrent.current, target, LERP_SPEED);
    mat.opacity = opacityCurrent.current;
  });

  return (
    <mesh
      ref={meshRef}
      geometry={geo}
      position={[0, -profile.height / 2 + 0.3, 0]}
      rotation={[-Math.PI / 2, 0, 0]}
    >
      <meshBasicMaterial
        ref={matRef}
        color={hex}
        opacity={opacityCurrent.current}
        transparent
        blending={THREE.AdditiveBlending}
        side={THREE.DoubleSide}
        depthWrite={false}
        toneMapped={false}
      />
    </mesh>
  );
}

function seededRandom(seed: number): () => number {
  let s = Math.abs(seed) || 1;
  return () => {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

function hashStr(str: string): number {
  let h = 5381;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) + h + str.charCodeAt(i)) | 0;
  }
  return Math.abs(h) || 1;
}

type WindowPos = { x: number; y: number; z: number; ry: number };

function buildWindowPositions(
  profile: EnclosureProfile,
  rows: number,
  cols: number,
  structureId: string,
): WindowPos[] {
  const rng = seededRandom(hashStr(structureId));
  const result: WindowPos[] = [];
  const halfH = profile.height / 2;

  if (profile.shape === "box") {
    const colsPerFace = Math.max(1, Math.ceil(cols / 4));
    const faces = [
      { nx: 0, nz: 1, tx: 1, tz: 0, fw: profile.width, dist: profile.depth / 2 },
      { nx: 0, nz: -1, tx: -1, tz: 0, fw: profile.width, dist: profile.depth / 2 },
      { nx: 1, nz: 0, tx: 0, tz: -1, fw: profile.depth, dist: profile.width / 2 },
      { nx: -1, nz: 0, tx: 0, tz: 1, fw: profile.depth, dist: profile.width / 2 },
    ];

    for (let r = 0; r < rows; r++) {
      const y = -halfH + (r + 0.5) * (profile.height / rows);
      for (const face of faces) {
        for (let c = 0; c < colsPerFace; c++) {
          if (rng() < 0.03) continue;
          const u = (c + 0.5) / colsPerFace - 0.5;
          result.push({
            x: face.nx * face.dist + face.tx * u * face.fw * 0.85,
            y,
            z: face.nz * face.dist + face.tz * u * face.fw * 0.85,
            ry: Math.atan2(face.nx, face.nz),
          });
        }
      }
    }
  } else {
    const rw = profile.width / 2;
    const rd = profile.depth / 2;

    if (profile.shape === "cylinder") {
      for (let r = 0; r < rows; r++) {
        const y = -halfH + (r + 0.5) * (profile.height / rows);
        for (let c = 0; c < cols; c++) {
          if (rng() < 0.03) continue;
          const angle = (c / cols) * Math.PI * 2;
          result.push({
            x: rw * Math.cos(angle),
            y,
            z: rd * Math.sin(angle),
            ry: -angle + Math.PI / 2,
          });
        }
      }
    } else {
      const segments = profile.shape === "hexPrism" ? 6 : profile.shape === "octPrism" ? 8 : 4;
      const colsPerSeg = Math.max(1, Math.ceil(cols / segments));
      const phaseOffset = Math.PI / segments;

      for (let r = 0; r < rows; r++) {
        const rowT = (r + 0.5) / rows;
        const taper = profile.taperTop != null ? THREE.MathUtils.lerp(1, profile.taperTop, rowT) : 1;
        const y = -halfH + (r + 0.5) * (profile.height / rows);
        const rwT = rw * taper;
        const rdT = rd * taper;

        for (let s = 0; s < segments; s++) {
          const centerAngle = phaseOffset + (s / segments) * Math.PI * 2;
          for (let c = 0; c < colsPerSeg; c++) {
            if (rng() < 0.03) continue;
            const spread = ((c + 0.5) / colsPerSeg - 0.5) * (2 * Math.PI / segments) * 0.7;
            const angle = centerAngle + spread;
            result.push({
              x: rwT * Math.cos(angle),
              y,
              z: rdT * Math.sin(angle),
              ry: -centerAngle + Math.PI / 2,
            });
          }
        }
      }
    }
  }

  return result;
}

function EnclosureWindows({
  active,
  hex,
  hovered,
  isSiaTower,
  motionStyle,
  profile,
  sceneIndex,
  sceneLocalProgress,
  scrollVelocityRef,
  structureId,
  tier,
  windowWarmth,
}: {
  active: boolean;
  hex: string;
  hovered: boolean;
  isSiaTower: boolean;
  motionStyle: MotionStyle;
  profile: EnclosureProfile;
  sceneIndex: number;
  sceneLocalProgress: number;
  scrollVelocityRef: React.RefObject<number>;
  structureId: string;
  tier: QualityTier;
  windowWarmth: number;
}) {
  const meshRef = useRef<THREE.InstancedMesh>(null);

  const rows = tier === "medium" ? Math.ceil(profile.windowRows / 2) : profile.windowRows;

  const windowData = useMemo(
    () => buildWindowPositions(profile, rows, profile.windowCols, structureId),
    [profile, rows, structureId],
  );

  const count = windowData.length;

  const flickerData = useMemo(() => {
    const rng = seededRandom(hashStr(structureId + "_flk"));
    const phases = new Float32Array(count);
    const speeds = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      phases[i] = rng() * Math.PI * 2;
      speeds[i] = 0.3 + rng() * 0.9;
    }
    return { phases, speeds };
  }, [count, structureId]);

  const districtColor = useMemo(() => new THREE.Color(hex), [hex]);

  const windowBaseColor = useMemo(
    () => new THREE.Color("#FFB066").lerp(new THREE.Color(hex), 1.0 - windowWarmth),
    [hex, windowWarmth],
  );

  const colorArray = useMemo(() => {
    const arr = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      arr[i * 3] = windowBaseColor.r;
      arr[i * 3 + 1] = windowBaseColor.g;
      arr[i * 3 + 2] = windowBaseColor.b;
    }
    return arr;
  }, [count, windowBaseColor]);
  const tempColor = useMemo(() => new THREE.Color(), []);

  const prevSceneRef = useRef(sceneIndex);
  const cascadeProgress = useRef(1);

  useEffect(() => {
    const mesh = meshRef.current;
    if (!mesh || count === 0) return;

    const dummy = new THREE.Object3D();
    for (let i = 0; i < count; i++) {
      const w = windowData[i];
      dummy.position.set(w.x, w.y, w.z);
      dummy.rotation.set(0, w.ry, 0);
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;

    mesh.instanceColor = new THREE.InstancedBufferAttribute(colorArray, 3);
    mesh.instanceColor.needsUpdate = true;
  }, [windowData, count, colorArray]);

  useEffect(() => {
    if (prevSceneRef.current !== sceneIndex) {
      if (active) {
        cascadeProgress.current = 0;
      }
      prevSceneRef.current = sceneIndex;
    }
  }, [sceneIndex, active]);

  useFrame(({ clock }, delta) => {
    const mesh = meshRef.current;
    if (!mesh || count === 0 || !mesh.instanceColor) return;

    if (cascadeProgress.current < 1) {
      cascadeProgress.current = Math.min(1, cascadeProgress.current + delta * 1.5);
    }

    const time = clock.elapsedTime;
    const { phases, speeds } = flickerData;

    let flickerMin = active ? 0.92 : 0.7;
    let speedMult = 1;
    switch (motionStyle) {
      case "pulse":
        speedMult = 1.6;
        if (active) flickerMin = 0.85;
        break;
      case "breathe":
        speedMult = 0.5;
        break;
    }
    const flickerRange = motionStyle === "breathe"
      ? (1.0 - flickerMin) * 0.6
      : 1.0 - flickerMin;

    let warmthFactor = 0;
    if (active && sceneLocalProgress > 0.5) {
      warmthFactor = (sceneLocalProgress - 0.5) * 2;
    }

    let siaPulse = 1;
    if (isSiaTower && active) {
      const cycle = (time % AI_PULSE_TIMING.cycleSeconds) / AI_PULSE_TIMING.cycleSeconds;
      siaPulse = THREE.MathUtils.lerp(0.7, 1.3, 0.5 + 0.5 * Math.sin(cycle * Math.PI * 2));
    }

    let brightnessBase = active ? 1.0 : hovered ? 0.7 : 0.45;
    const absVel = Math.abs(scrollVelocityRef.current ?? 0);
    if (absVel > 0.3) {
      brightnessBase += Math.min(absVel * 0.15, 0.3);
    }
    let changed = false;
    const cascadeDone = cascadeProgress.current >= 1;

    for (let i = 0; i < count; i++) {
      const phaseOffset = motionStyle === "data-stream" && windowData[i].x < 0 ? Math.PI : 0;
      const flicker = flickerMin + flickerRange * (0.5 + 0.5 * Math.sin(time * speeds[i] * speedMult + phases[i] + phaseOffset));

      let cascade = 1;
      if (!cascadeDone) {
        const threshold = i / count;
        cascade = THREE.MathUtils.clamp((cascadeProgress.current - threshold) * 6, 0, 1);
      }

      tempColor.copy(windowBaseColor);
      if (warmthFactor > 0) {
        tempColor.lerp(districtColor, warmthFactor * 0.4);
      }

      const factor = flicker * cascade * brightnessBase * siaPulse;
      const idx = i * 3;
      const nr = tempColor.r * factor;
      const ng = tempColor.g * factor;
      const nb = tempColor.b * factor;

      if (Math.abs(colorArray[idx] - nr) > 0.001 ||
          Math.abs(colorArray[idx + 1] - ng) > 0.001 ||
          Math.abs(colorArray[idx + 2] - nb) > 0.001) {
        colorArray[idx] = nr;
        colorArray[idx + 1] = ng;
        colorArray[idx + 2] = nb;
        changed = true;
      }
    }

    if (changed) {
      mesh.instanceColor.needsUpdate = true;
    }
  });

  if (count === 0) return null;

  return (
    <instancedMesh ref={meshRef} args={[WINDOW_GEO, undefined, count]} renderOrder={2}>
      <meshBasicMaterial
        color="#FFFFFF"
        opacity={0.9}
        transparent
        depthWrite={false}
        toneMapped={false}
      />
    </instancedMesh>
  );
}

const ARRIVAL_RING_GEO = new THREE.RingGeometry(0, 1, 32, 1);

function EnclosureArrivalBurst({
  active,
  hex,
  profile,
}: {
  active: boolean;
  hex: string;
  profile: EnclosureProfile;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const wasActive = useRef(active);
  const burstProgress = useRef(1);

  useEffect(() => {
    if (active && !wasActive.current) {
      burstProgress.current = 0;
    }
    wasActive.current = active;
  }, [active]);

  useFrame((_, delta) => {
    const mesh = meshRef.current;
    const mat = matRef.current;
    if (!mesh || !mat) return;

    if (burstProgress.current >= 1) {
      mesh.visible = false;
      return;
    }

    burstProgress.current = Math.min(1, burstProgress.current + delta / 1.2);
    mesh.visible = true;

    const t = burstProgress.current;
    const scale = THREE.MathUtils.lerp(0.5, 2.5, t) * profile.width * 0.6;
    mesh.scale.set(scale, scale, 1);
    mat.opacity = 0.15 * (1 - t);
  });

  return (
    <mesh
      ref={meshRef}
      geometry={ARRIVAL_RING_GEO}
      position={[0, 0, 0]}
      rotation={[-Math.PI / 2, 0, 0]}
      visible={false}
    >
      <meshBasicMaterial
        ref={matRef}
        color={hex}
        opacity={0}
        transparent
        blending={THREE.AdditiveBlending}
        side={THREE.DoubleSide}
        depthWrite={false}
        toneMapped={false}
      />
    </mesh>
  );
}

function BuildingEnclosure({
  active,
  clickInteriorId,
  hovered,
  isClickInteriorActive,
  isSiaTower,
  sceneIndex,
  sceneLocalProgress,
  scrollVelocityRef,
  structure,
  tier,
  visible,
}: {
  active: boolean;
  clickInteriorId?: string;
  hovered: boolean;
  isClickInteriorActive: boolean;
  isSiaTower: boolean;
  sceneIndex: number;
  sceneLocalProgress: number;
  scrollVelocityRef: React.RefObject<number>;
  structure: StructureAsset;
  tier: QualityTier;
  visible: boolean;
}) {
  const profile = ENCLOSURE_PROFILES[structure.id];

  const shellGeo = useMemo(() => (profile ? createGeometry(profile, 0, tier) : null), [profile, tier]);
  const coreGeo = useMemo(() => (profile ? createGeometry(profile, profile.coreInset, tier) : null), [profile, tier]);
  const shellScale = useMemo(() => (profile ? footprintScale(profile, 0) : [1, 1, 1] as [number, number, number]), [profile]);
  const coreScale = useMemo(() => (profile ? footprintScale(profile, profile.coreInset) : [1, 1, 1] as [number, number, number]), [profile]);

  const shellMat = useMemo(() => {
    if (!profile) return null;
    if (tier === "low") {
      return new THREE.MeshStandardMaterial({
        color: BRAND_COLORS.glass,
        emissive: structure.hex,
        emissiveIntensity: profile.shellEmissive,
        roughness: 0.1,
        metalness: 0.85,
        envMapIntensity: 1.8,
        opacity: Math.min(profile.shellOpacity, 0.65),
        transparent: true,
        side: THREE.DoubleSide,
        depthWrite: false,
      });
    }
    return createFresnelShellMaterial({
      baseColor: profile.shellTint ?? BRAND_COLORS.glass,
      rimColor: structure.hex,
      rimPower: profile.rimPower,
      rimIntensity: tier === "medium" ? profile.rimIntensity * 0.5 : profile.rimIntensity,
      emissiveIntensity: profile.shellEmissive,
      opacity: profile.shellOpacity,
      facadeStyle: profile.facadeStyle,
      panelColumns: tier === "medium" ? Math.floor(profile.panelColumns / 2) : profile.panelColumns,
      panelRows: tier === "medium" ? Math.floor(profile.panelRows / 2) : profile.panelRows,
    });
  }, [profile, structure.hex, tier]);

  const coreColor = useMemo(() => {
    if (!profile) return new THREE.Color("#FFB066");
    return new THREE.Color("#FFB066").lerp(new THREE.Color(structure.hex), 0.3);
  }, [profile, structure.hex]);

  const coreColorActive = useMemo(() => {
    if (!profile) return new THREE.Color("#FFB066");
    return new THREE.Color("#FFB066").lerp(new THREE.Color(structure.hex), 0.5);
  }, [profile, structure.hex]);

  const lightColor = useMemo(() => {
    if (!profile) return new THREE.Color("#FFB066");
    return new THREE.Color("#FFB066").lerp(new THREE.Color(structure.hex), 1.0 - profile.windowWarmth);
  }, [profile, structure.hex]);

  const coreMat = useMemo(() => {
    if (!profile) return null;
    return new THREE.MeshStandardMaterial({
      color: coreColor,
      emissive: coreColor,
      emissiveIntensity: profile.coreEmissive,
      roughness: 0.6,
      metalness: 0,
      opacity: profile.coreOpacity,
      transparent: true,
      depthWrite: false,
    });
  }, [profile, coreColor]);

  const groupRef = useRef<THREE.Group>(null);
  const shellMeshRef = useRef<THREE.Mesh>(null);
  const lightRef = useRef<THREE.PointLight>(null);

  const prevActiveRef = useRef(active);
  const arrivalTimeRef = useRef(-10);

  const anim = useRef({
    shellOpacity: profile?.shellOpacity ?? 0.2,
    shellEmissive: profile?.shellEmissive ?? 0.05,
    coreEmissive: profile?.coreEmissive ?? 0.1,
    lightIntensity: profile?.lightIntensity ?? 10,
    hoverScale: 1,
    emphasis: 1,
    shellTilt: 0,
  });

  const coreColorLerped = useMemo(() => new THREE.Color(), []);

  useFrame(({ clock, camera }) => {
    if (!profile || !shellMat || !coreMat) return;

    const targetActive = active;
    const targetHover = hovered && !active;
    const time = clock.elapsedTime;

    if (active && !prevActiveRef.current) {
      arrivalTimeRef.current = time;
    }
    prevActiveRef.current = active;

    let shellOpTarget = targetActive ? profile.shellOpacity * 1.08 : profile.shellOpacity;
    let shellEmTarget = targetActive ? profile.shellEmissive * 2.2 : profile.shellEmissive;
    let coreEmTarget = targetActive ? profile.coreEmissive * 1.6 : profile.coreEmissive;
    let lightTarget = targetActive ? profile.lightIntensity * 1.8 : profile.lightIntensity;
    let scaleTarget = 1;

    if (targetHover) {
      shellEmTarget *= HOVER_RIM_MULT;
      coreEmTarget *= 1.15;
      scaleTarget = HOVER_SCALE;
    }

    if (isSiaTower && targetActive) {
      const cycle = (time % AI_PULSE_TIMING.cycleSeconds) / AI_PULSE_TIMING.cycleSeconds;
      const pulse = 0.5 + 0.5 * Math.sin(cycle * Math.PI * 2);
      shellEmTarget *= THREE.MathUtils.lerp(0.7, 1.3, pulse);
    }

    const arrivalElapsed = time - arrivalTimeRef.current;
    if (active && arrivalElapsed < 1.5) {
      shellEmTarget += 0.08 * (1 - arrivalElapsed / 1.5);
    }

    const a = anim.current;

    const dx = camera.position.x - structure.position[0];
    const dz = camera.position.z - structure.position[2];
    const camDist = Math.sqrt(dx * dx + dz * dz);
    let emphasisTarget: number;
    const CLICK_INTERIOR_LERP = 0.08;
    if (isClickInteriorActive && structure.id === clickInteriorId) {
      emphasisTarget = 0;
    } else if (isClickInteriorActive && structure.id !== clickInteriorId) {
      emphasisTarget = 0.25;
    } else if (targetActive) {
      emphasisTarget = 1.0;
    } else if (targetHover) {
      emphasisTarget = 0.85;
    } else if (camDist < 60) {
      emphasisTarget = 0.70;
    } else {
      emphasisTarget = 0.55;
    }
    let emphLerp: number;
    if (isClickInteriorActive && structure.id === clickInteriorId) {
      emphLerp = CLICK_INTERIOR_LERP;
    } else if (!isClickInteriorActive && a.emphasis < 0.3) {
      emphLerp = 0.06;
    } else {
      emphLerp = LERP_SPEED;
    }
    a.emphasis = THREE.MathUtils.lerp(a.emphasis, emphasisTarget, emphLerp);

    shellOpTarget *= a.emphasis;
    coreEmTarget *= a.emphasis;
    lightTarget *= a.emphasis;

    a.shellOpacity = THREE.MathUtils.lerp(a.shellOpacity, shellOpTarget, LERP_SPEED);
    a.shellEmissive = THREE.MathUtils.lerp(a.shellEmissive, shellEmTarget, LERP_SPEED);
    a.coreEmissive = THREE.MathUtils.lerp(a.coreEmissive, coreEmTarget, LERP_SPEED);
    a.lightIntensity = THREE.MathUtils.lerp(a.lightIntensity, lightTarget, LERP_SPEED);
    a.hoverScale = THREE.MathUtils.lerp(a.hoverScale, scaleTarget, LERP_SPEED);

    // Motion style: pulse adds to shell opacity
    if (profile.motionStyle === "pulse") {
      a.shellOpacity += Math.sin(time * 1.5) * 0.03;
    }

    shellMat.opacity = a.shellOpacity;
    shellMat.emissiveIntensity = a.shellEmissive;

    // Lerp core color between inactive (0.3 blend) and active (0.5 blend)
    coreColorLerped.copy(coreColor).lerp(coreColorActive, targetActive ? 1 : 0);
    coreMat.color.lerp(coreColorLerped, LERP_SPEED);
    coreMat.emissive.lerp(coreColorLerped, LERP_SPEED);
    coreMat.emissiveIntensity = a.coreEmissive;

    if (lightRef.current) {
      lightRef.current.intensity = a.lightIntensity;
    }

    if (shellMeshRef.current) {
      const s = a.hoverScale;
      shellMeshRef.current.scale.set(
        shellScale[0] * s,
        shellScale[1] * s,
        shellScale[2] * s,
      );

      if (profile.motionStyle === "breathe") {
        shellMeshRef.current.scale.y *= 1 + Math.sin(time * 0.8) * 0.005;
      }

      if (!isSiaTower) {
        const tiltTarget = (scrollVelocityRef.current ?? 0) * 0.008;
        a.shellTilt = THREE.MathUtils.lerp(a.shellTilt, tiltTarget, LERP_SPEED * 2);
        shellMeshRef.current.rotation.z = a.shellTilt;
      }
    }
  });

  if (!profile || !visible || !shellGeo || !coreGeo || !shellMat || !coreMat) return null;

  return (
    <group
      ref={groupRef}
      name={`${structure.id}_enclosure`}
      position={[
        structure.position[0],
        profile.height / 2 + profile.yOffset,
        structure.position[2],
      ]}
      rotation={[0, profile.rotationY, 0]}
    >
      <mesh ref={shellMeshRef} geometry={shellGeo} material={shellMat} scale={shellScale} renderOrder={1} />

      <mesh geometry={coreGeo} material={coreMat} scale={coreScale} renderOrder={0} />

      {tier !== "low" && (
        <FloorPlates active={active} hex={structure.hex} motionStyle={profile.motionStyle} profile={profile} sceneIndex={sceneIndex} />
      )}

      <FacadeBands profile={profile} tier={tier} />

      {tier !== "low" && (
        <EnclosureWindows
          active={active}
          hex={structure.hex}
          hovered={hovered}
          isSiaTower={isSiaTower}
          motionStyle={profile.motionStyle}
          profile={profile}
          sceneIndex={sceneIndex}
          sceneLocalProgress={sceneLocalProgress}
          scrollVelocityRef={scrollVelocityRef}
          structureId={structure.id}
          tier={tier}
          windowWarmth={profile.windowWarmth}
        />
      )}

      {tier !== "low" && (
        <EnclosureArrivalBurst active={active} hex={structure.hex} profile={profile} />
      )}

      <EnclosureBaseGlow active={active} hex={structure.hex} profile={profile} />

      {!isSiaTower && (
        <RooftopAccent active={active} hex={structure.hex} motionStyle={profile.motionStyle} profile={profile} />
      )}

      {active && !isSiaTower && (
        <EnclosureUplight active={active} hex={structure.hex} profile={profile} />
      )}

      {tier !== "low" && (
        <EnclosureAtmosphere active={active} hex={structure.hex} profile={profile} />
      )}

      <pointLight
        ref={lightRef}
        color={lightColor}
        intensity={anim.current.lightIntensity}
        distance={profile.height * 0.8}
        position={[0, 0, 0]}
      />
    </group>
  );
}

type BuildingEnclosureLayerProps = {
  activeDistrict: string;
  clickInteriorId?: string;
  focusedDistrictId?: string;
  hoveredDistrictId?: string;
  isClickInteriorActive?: boolean;
  sceneIndex: number;
  sceneLocalProgress: number;
  structures: StructureAsset[];
};

export function BuildingEnclosureLayer({
  activeDistrict,
  clickInteriorId,
  focusedDistrictId,
  hoveredDistrictId,
  isClickInteriorActive = false,
  sceneIndex,
  sceneLocalProgress,
  structures,
}: BuildingEnclosureLayerProps) {
  const tier = useMemo(() => getDeviceQualityTier(), []);
  const isFullCity = sceneIndex === 1 || sceneIndex === 15 || sceneIndex === 17;
  const visualActive = isFullCity ? "city" : activeDistrict;
  const revealId = focusedDistrictId ?? hoveredDistrictId;

  const groupRef = useRef<THREE.Group>(null);
  const prevSceneRef = useRef(sceneIndex);
  const fadeProgress = useRef(1);
  const prevProgressRef = useRef(sceneLocalProgress);
  const scrollVelocityRef = useRef(0);

  useEffect(() => {
    if (prevSceneRef.current !== sceneIndex) {
      fadeProgress.current = 0;
      prevSceneRef.current = sceneIndex;
    }
  }, [sceneIndex]);

  useFrame((_, delta) => {
    if (!groupRef.current) return;
    if (fadeProgress.current < 1) {
      fadeProgress.current = Math.min(1, fadeProgress.current + FADE_SPEED);
    }
    groupRef.current.visible = fadeProgress.current > 0.01;
    const f = THREE.MathUtils.smoothstep(fadeProgress.current, 0, 1);
    const s = THREE.MathUtils.lerp(0.97, 1, f);
    groupRef.current.scale.setScalar(s);

    const safeDelta = Math.max(delta, 0.001);
    const rawVelocity = THREE.MathUtils.clamp(
      (sceneLocalProgress - prevProgressRef.current) / safeDelta,
      -3,
      3,
    );
    prevProgressRef.current = sceneLocalProgress;
    scrollVelocityRef.current = THREE.MathUtils.lerp(
      scrollVelocityRef.current,
      rawVelocity,
      0.08,
    );
  });

  return (
    <group ref={groupRef} name="Building_Enclosure_Layer">
      {structures.map((structure) => {
        const isActive =
          visualActive === "city" ||
          visualActive === structure.id ||
          revealId === structure.id;

        const isVisible =
          (sceneIndex !== 3 || structure.id !== "sia-tower");
        const isHovered = hoveredDistrictId === structure.id;

        return (
          <BuildingEnclosure
            key={`${structure.id}-enclosure`}
            active={isActive}
            clickInteriorId={clickInteriorId}
            hovered={isHovered}
            isClickInteriorActive={isClickInteriorActive}
            isSiaTower={structure.id === "sia-tower"}
            sceneIndex={sceneIndex}
            sceneLocalProgress={sceneLocalProgress}
            scrollVelocityRef={scrollVelocityRef}
            structure={structure}
            tier={tier}
            visible={isVisible}
          />
        );
      })}
    </group>
  );
}

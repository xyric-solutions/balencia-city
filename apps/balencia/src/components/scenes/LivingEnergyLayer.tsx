import { Line } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import {
  getDistrictProfile,
  OVERVIEW_SCENES,
  type DistrictActivityTone,
} from "../../lib/district-metadata";
import { CITY_LAYOUT_ISLAND } from "../../lib/city-layout-v2";
import { AI_PULSE_TIMING, CROSS_DISTRICT_INSIGHTS } from "../../lib/energy-system";
import { BRAND_COLORS } from "../../lib/materials";
import type { StructureAsset, Vec3 } from "../../lib/types";
import { useScrollStore } from "../../store/useScrollStore";

type LivingEnergyLayerProps = {
  structures: StructureAsset[];
};

type EnergyRouteKind = "hub" | "cross";

type EnergyRoute = {
  id: string;
  color: string;
  curve: THREE.CatmullRomCurve3;
  intensity: number;
  kind: EnergyRouteKind;
  lineWidth: number;
  packetCount: number;
  phase: number;
  speed: number;
};

type ToneConfig = {
  color: string;
  tempo: number;
  scanOpacity: number;
};

type FloatingMote = {
  angle: number;
  center: THREE.Vector3;
  height: number;
  lift: number;
  phase: number;
  radius: number;
  speed: number;
};

const hubOrigin = new THREE.Vector3(...AI_PULSE_TIMING.origin);
const tempMatrixObject = new THREE.Object3D();

const CROSS_INSIGHT_DISTRICT_IDS: Record<string, readonly [string, string]> = {
  fitness_recovery: ["fitness", "recovery"],
  nutrition_career: ["nutrition", "career"],
  relationships_yoga: ["relationships", "yoga"],
  finance_career: ["finance", "career"],
  recovery_analytics: ["recovery", "analytics"],
  chat_relationships: ["chat", "relationships"],
};

function seeded(index: number, salt: number) {
  return Math.abs(Math.sin(index * 12.9898 + salt * 78.233) * 43758.5453 % 1);
}

function vectorFrom([x, y, z]: Vec3) {
  return new THREE.Vector3(x, y, z);
}

function districtAnchor(structure: StructureAsset, anchorScale = 0.72) {
  if (structure.id === "sia-tower") {
    return hubOrigin.clone();
  }

  const profile = getDistrictProfile(structure.id);

  return new THREE.Vector3(
    structure.position[0],
    Math.max(2.2, profile.anchorHeight * anchorScale),
    structure.position[2],
  );
}

function arcedCurve(start: THREE.Vector3, end: THREE.Vector3, liftScale = 1) {
  const distance = start.distanceTo(end);
  const midpoint = start.clone().lerp(end, 0.5);
  const lateral = new THREE.Vector3(-(end.z - start.z), 0, end.x - start.x);

  if (lateral.lengthSq() > 0.001) {
    lateral.normalize().multiplyScalar(Math.min(distance * 0.045, 4.2));
  }

  midpoint.y = Math.max(start.y, end.y) + THREE.MathUtils.clamp(distance * 0.12, 7, 16) * liftScale;
  midpoint.add(lateral);

  return new THREE.CatmullRomCurve3([start, midpoint, end]);
}

function buildRoutes({
  activeDistrict,
  focusedDistrictId,
  hoveredDistrictId,
  sceneIndex,
  structures,
}: {
  activeDistrict: string;
  focusedDistrictId?: string;
  hoveredDistrictId?: string;
  sceneIndex: number;
  structures: StructureAsset[];
}) {
  const structureMap = new Map(structures.map((structure) => [structure.id, structure]));
  const overview = OVERVIEW_SCENES.has(sceneIndex);
  const revealDistrictId = focusedDistrictId ?? hoveredDistrictId;
  const routeTargets = overview
    ? structures.filter((structure) => structure.id !== "sia-tower").map((structure) => structure.id)
    : [revealDistrictId ?? activeDistrict].filter((id) => id && id !== "city" && id !== "sia-tower");
  const routes: EnergyRoute[] = [];

  routeTargets.forEach((districtId, index) => {
    const structure = structureMap.get(districtId);

    if (!structure) {
      return;
    }

    routes.push({
      id: `sia-to-${districtId}`,
      color: BRAND_COLORS.energy,
      curve: arcedCurve(hubOrigin.clone(), districtAnchor(structure), overview ? 0.8 : 1),
      intensity: overview ? 0.48 : 0.74,
      kind: "hub",
      lineWidth: overview ? 0.78 : 1.18,
      packetCount: overview ? 2 : 3,
      phase: index * 0.137,
      speed: overview ? 0.13 : 0.18,
    });
  });

  if (sceneIndex === 15) {
    CROSS_DISTRICT_INSIGHTS.forEach((insight, index) => {
      const [fromId, toId] = CROSS_INSIGHT_DISTRICT_IDS[insight.id] ?? [];
      const from = structureMap.get(fromId);
      const to = structureMap.get(toId);

      if (!from || !to) {
        return;
      }

      routes.push({
        id: `cross-${insight.id}`,
        color: BRAND_COLORS.gold,
        curve: arcedCurve(districtAnchor(from, 0.58), districtAnchor(to, 0.58), 0.64),
        intensity: 0.7,
        kind: "cross",
        lineWidth: 1.05,
        packetCount: 3,
        phase: index * 0.171,
        speed: 0.115,
      });
    });
  }

  return routes;
}

function toneConfig(tone: DistrictActivityTone, fallbackColor: string): ToneConfig {
  if (tone === "core") {
    return { color: BRAND_COLORS.energy, scanOpacity: 0.46, tempo: 1 };
  }

  if (tone === "surge") {
    return { color: fallbackColor, scanOpacity: 0.38, tempo: 1.42 };
  }

  if (tone === "calm") {
    return { color: "#6EE7B7", scanOpacity: 0.3, tempo: 0.68 };
  }

  return { color: fallbackColor, scanOpacity: 0.34, tempo: 0.86 };
}

function routePoints(route: EnergyRoute) {
  return route.curve.getPoints(route.kind === "cross" ? 34 : 38);
}

function AnimatedDataRoute({ route }: { route: EnergyRoute }) {
  const meshRef = useRef<THREE.InstancedMesh | null>(null);
  const linePoints = useMemo(() => routePoints(route), [route]);

  useFrame(({ clock }) => {
    const mesh = meshRef.current;

    if (!mesh) {
      return;
    }

    for (let index = 0; index < route.packetCount; index += 1) {
      const t = (clock.elapsedTime * route.speed + route.phase + index / route.packetCount) % 1;
      const point = route.curve.getPointAt(t);
      const packetScale = route.kind === "cross" ? 0.34 : 0.28;
      const pulse = 0.82 + Math.sin(clock.elapsedTime * 5.4 + index) * 0.18;

      tempMatrixObject.position.copy(point);
      tempMatrixObject.scale.setScalar(packetScale * pulse);
      tempMatrixObject.updateMatrix();
      mesh.setMatrixAt(index, tempMatrixObject.matrix);
    }

    mesh.instanceMatrix.needsUpdate = true;
  });

  return (
    <group name={`${route.id}_animated_data_route`}>
      <Line
        points={linePoints}
        color={route.color}
        lineWidth={route.lineWidth}
        transparent
        opacity={route.intensity}
      />
      <instancedMesh ref={meshRef} args={[undefined, undefined, route.packetCount]}>
        <sphereGeometry args={[1, 10, 10]} />
        <meshStandardMaterial
          color={route.color}
          emissive={route.color}
          emissiveIntensity={route.kind === "cross" ? 1.45 : 1.2}
          toneMapped={false}
        />
      </instancedMesh>
    </group>
  );
}

function EnergyRouteMotes({ routes }: { routes: EnergyRoute[] }) {
  const geometryRef = useRef<THREE.BufferGeometry | null>(null);
  const moteSeeds = useMemo(() => {
    const count = Math.min(104, Math.max(28, routes.length * 7));

    return Array.from({ length: count }, (_, index) => ({
      offset: seeded(index, 2.4),
      routeIndex: index % Math.max(routes.length, 1),
      wobble: seeded(index, 5.1) * Math.PI * 2,
    }));
  }, [routes.length]);
  const positions = useMemo(() => new Float32Array(moteSeeds.length * 3), [moteSeeds.length]);

  useFrame(({ clock }) => {
    const geometry = geometryRef.current;

    if (!geometry || routes.length === 0) {
      return;
    }

    const attribute = geometry.getAttribute("position") as THREE.BufferAttribute;

    moteSeeds.forEach((mote, index) => {
      const route = routes[mote.routeIndex % routes.length];
      const t = (clock.elapsedTime * 0.036 + mote.offset) % 1;
      const point = route.curve.getPointAt(t);
      const flutter = Math.sin(clock.elapsedTime * 2.8 + mote.wobble) * 0.34;

      attribute.setXYZ(
        index,
        point.x + Math.cos(mote.wobble + clock.elapsedTime * 0.7) * 0.24,
        point.y + flutter,
        point.z + Math.sin(mote.wobble + clock.elapsedTime * 0.7) * 0.24,
      );
    });

    attribute.needsUpdate = true;
  });

  if (routes.length === 0) {
    return null;
  }

  return (
    <points name="Route_Firefly_Motes">
      <bufferGeometry ref={geometryRef}>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial
        color={BRAND_COLORS.energy}
        size={0.2}
        transparent
        opacity={0.66}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        toneMapped={false}
      />
    </points>
  );
}

function yawTowardCenter(position: Vec3) {
  return Math.atan2(position[0], position[2]);
}

function DistrictStatusGlow({
  activeDistrict,
  focusedDistrictId,
  hoveredDistrictId,
  sceneIndex,
  structure,
}: {
  activeDistrict: string;
  focusedDistrictId?: string;
  hoveredDistrictId?: string;
  sceneIndex: number;
  structure: StructureAsset;
}) {
  const groupRef = useRef<THREE.Group | null>(null);
  const groundMaterialRef = useRef<THREE.MeshStandardMaterial | null>(null);
  const crownMaterialRef = useRef<THREE.MeshStandardMaterial | null>(null);
  const scanMaterialRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const scanRingRef = useRef<THREE.Mesh | null>(null);
  const scanPlaneRef = useRef<THREE.Mesh | null>(null);
  const profile = getDistrictProfile(structure.id);
  const config = toneConfig(profile.activity.tone, profile.motifColor);
  const isOverview = OVERVIEW_SCENES.has(sceneIndex);
  const isFocused = focusedDistrictId === structure.id;
  const isHovered = hoveredDistrictId === structure.id;
  const isActive = activeDistrict === structure.id || (activeDistrict === "city" && isOverview);
  const isSia = structure.id === "sia-tower";
  const sceneBoost = sceneIndex === 15 ? 1.18 : isOverview ? 0.92 : 0.72;
  const emphasis = (isFocused ? 1.16 : isHovered ? 1.02 : isActive ? 0.86 : 0.36) * sceneBoost;
  const [padWidth, padDepth] = profile.padSize;
  const radius = isSia ? 16.8 : Math.max(padWidth, padDepth) * 0.64;
  const topHeight = isSia ? 42.4 : Math.max(3.2, profile.anchorHeight * 0.72);
  const planeHeight = isSia ? 24 : Math.max(5, topHeight * 0.72);
  const showScanPlane = isSia || isFocused || isHovered || (!isOverview && isActive) || sceneIndex === 15;

  useFrame(({ clock }) => {
    const time = clock.elapsedTime;
    const cycle = AI_PULSE_TIMING.cycleSeconds;
    const heartbeat = (Math.sin((time / cycle + profile.activity.pulseOffset) * Math.PI * 2) + 1) / 2;
    const localPulse = (Math.sin(time * config.tempo * 2.4 + profile.activity.pulseOffset * 9) + 1) / 2;
    const tonePulse = THREE.MathUtils.lerp(heartbeat, localPulse, profile.activity.tone === "core" ? 0.24 : 0.55);
    const glow = THREE.MathUtils.clamp(emphasis * profile.activity.glowScale * (0.54 + tonePulse * 0.48), 0.06, 1.18);

    if (groupRef.current) {
      groupRef.current.scale.setScalar(1 + glow * 0.018);
    }

    if (groundMaterialRef.current) {
      groundMaterialRef.current.opacity = THREE.MathUtils.clamp(0.16 + glow * 0.42, 0.12, 0.82);
      groundMaterialRef.current.emissiveIntensity = THREE.MathUtils.clamp(0.22 + glow * 0.68, 0.14, 1.1);
    }

    if (crownMaterialRef.current) {
      crownMaterialRef.current.opacity = THREE.MathUtils.clamp(0.2 + glow * 0.44, 0.18, 0.86);
      crownMaterialRef.current.emissiveIntensity = THREE.MathUtils.clamp(0.28 + glow * 0.74, 0.18, 1.25);
    }

    if (scanMaterialRef.current) {
      scanMaterialRef.current.opacity = THREE.MathUtils.clamp(config.scanOpacity * glow, 0.08, 0.62);
    }

    if (scanRingRef.current) {
      const scanTravel = (time * 0.095 * config.tempo + profile.activity.pulseOffset) % 1;

      scanRingRef.current.position.y = THREE.MathUtils.lerp(0.55, topHeight, scanTravel);
      scanRingRef.current.scale.setScalar(THREE.MathUtils.lerp(0.78, 1.06, scanTravel));
    }

    if (scanPlaneRef.current) {
      scanPlaneRef.current.rotation.y = yawTowardCenter(structure.position) + Math.sin(time * 0.32) * 0.05;
    }
  });

  return (
    <group
      ref={groupRef}
      name={`${structure.id}_status_glow`}
      position={vectorFrom(structure.position).toArray()}
    >
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.18, 0]}>
        <ringGeometry args={[radius * 0.78, radius, isSia ? 112 : 72]} />
        <meshStandardMaterial
          ref={groundMaterialRef}
          color={config.color}
          emissive={config.color}
          emissiveIntensity={0.32}
          opacity={0.24}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
          depthWrite={false}
        />
      </mesh>

      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, topHeight, 0]}>
        <torusGeometry args={[Math.max(radius * 0.28, 1.25), isSia ? 0.06 : 0.035, 8, 72]} />
        <meshStandardMaterial
          ref={crownMaterialRef}
          color={config.color}
          emissive={config.color}
          emissiveIntensity={0.46}
          opacity={0.28}
          toneMapped={false}
          transparent
        />
      </mesh>

      <mesh ref={scanRingRef} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.55, 0]}>
        <ringGeometry args={[radius * 0.42, radius * 0.48, isSia ? 96 : 56]} />
        <meshBasicMaterial
          ref={scanMaterialRef}
          color={config.color}
          opacity={0.18}
          side={THREE.DoubleSide}
          transparent
          depthWrite={false}
          blending={THREE.AdditiveBlending}
          toneMapped={false}
        />
      </mesh>

      {showScanPlane ? (
        <mesh ref={scanPlaneRef} position={[0, planeHeight * 0.52, 0]} rotation={[0, yawTowardCenter(structure.position), 0]}>
          <planeGeometry args={[Math.max(radius * 0.86, 4), planeHeight]} />
          <meshBasicMaterial
            color={config.color}
            opacity={isSia ? 0.075 : 0.052}
            side={THREE.DoubleSide}
            transparent
            depthWrite={false}
            blending={THREE.AdditiveBlending}
            toneMapped={false}
          />
        </mesh>
      ) : null}
    </group>
  );
}

function createFloatingMotes({
  countPerDistrict,
  ids,
  salt,
  structures,
}: {
  countPerDistrict: number;
  ids: string[];
  salt: number;
  structures: StructureAsset[];
}) {
  const structureMap = new Map(structures.map((structure) => [structure.id, structure]));
  const motes: FloatingMote[] = [];

  ids.forEach((id, districtIndex) => {
    const structure = structureMap.get(id);

    if (!structure) {
      return;
    }

    const profile = getDistrictProfile(id);
    const center = vectorFrom(structure.position);
    const radiusBase = Math.max(profile.padSize[0], profile.padSize[1]) * (id === "sia-tower" ? 0.32 : 0.46);

    for (let index = 0; index < countPerDistrict; index += 1) {
      const globalIndex = districtIndex * countPerDistrict + index;
      motes.push({
        angle: seeded(globalIndex, salt) * Math.PI * 2,
        center,
        height: THREE.MathUtils.lerp(1.2, Math.max(5, profile.anchorHeight * 0.82), seeded(globalIndex, salt + 2.1)),
        lift: THREE.MathUtils.lerp(0.28, 0.88, seeded(globalIndex, salt + 4.8)),
        phase: seeded(globalIndex, salt + 7.3) * Math.PI * 2,
        radius: THREE.MathUtils.lerp(radiusBase * 0.24, radiusBase, seeded(globalIndex, salt + 9.6)),
        speed: THREE.MathUtils.lerp(0.08, 0.2, seeded(globalIndex, salt + 12.2)),
      });
    }
  });

  return motes;
}

function FloatingMoteField({
  color,
  countPerDistrict,
  ids,
  name,
  salt,
  size,
  structures,
}: {
  color: string;
  countPerDistrict: number;
  ids: string[];
  name: string;
  salt: number;
  size: number;
  structures: StructureAsset[];
}) {
  const geometryRef = useRef<THREE.BufferGeometry | null>(null);
  const motes = useMemo(
    () => createFloatingMotes({ countPerDistrict, ids, salt, structures }),
    [countPerDistrict, ids, salt, structures],
  );
  const positions = useMemo(() => new Float32Array(motes.length * 3), [motes.length]);

  useFrame(({ clock }) => {
    const geometry = geometryRef.current;

    if (!geometry) {
      return;
    }

    const attribute = geometry.getAttribute("position") as THREE.BufferAttribute;

    motes.forEach((mote, index) => {
      const angle = mote.angle + clock.elapsedTime * mote.speed;
      const lift = Math.sin(clock.elapsedTime * 0.7 + mote.phase) * mote.lift;

      attribute.setXYZ(
        index,
        mote.center.x + Math.cos(angle) * mote.radius,
        mote.height + lift,
        mote.center.z + Math.sin(angle) * mote.radius,
      );
    });

    attribute.needsUpdate = true;
  });

  return (
    <points name={name}>
      <bufferGeometry ref={geometryRef}>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial
        color={color}
        size={size}
        transparent
        opacity={0.58}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        toneMapped={false}
      />
    </points>
  );
}

function IntelligenceFogVeils({ sceneIndex }: { sceneIndex: number }) {
  const groupRef = useRef<THREE.Group | null>(null);
  const isOverview = OVERVIEW_SCENES.has(sceneIndex);

  useFrame(({ clock }) => {
    const group = groupRef.current;

    if (!group) {
      return;
    }

    group.rotation.y = clock.elapsedTime * (isOverview ? 0.018 : 0.01);
    group.position.y = Math.sin(clock.elapsedTime * 0.28) * 0.18;
  });

  return (
    <group ref={groupRef} name="Holographic_Intelligence_Fog_Veils">
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.72, 0]}>
        <ringGeometry args={[34, CITY_LAYOUT_ISLAND.edgeWallRadius, 176]} />
        <meshBasicMaterial
          color={BRAND_COLORS.energy}
          opacity={isOverview ? 0.054 : 0.034}
          side={THREE.DoubleSide}
          transparent
          depthWrite={false}
          blending={THREE.AdditiveBlending}
          toneMapped={false}
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 1.28, 0]}>
        <ringGeometry args={[8, 58, 144]} />
        <meshBasicMaterial
          color={BRAND_COLORS.purple}
          opacity={isOverview ? 0.038 : 0.026}
          side={THREE.DoubleSide}
          transparent
          depthWrite={false}
          blending={THREE.AdditiveBlending}
          toneMapped={false}
        />
      </mesh>
    </group>
  );
}

function LayoutV2PulseRing({ sceneIndex }: { sceneIndex: number }) {
  const meshRef = useRef<THREE.Mesh | null>(null);
  const materialRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const isOverview = OVERVIEW_SCENES.has(sceneIndex);

  useFrame(({ clock }) => {
    const cycleProgress = (clock.elapsedTime % AI_PULSE_TIMING.cycleSeconds) / AI_PULSE_TIMING.cycleSeconds;
    const eased = THREE.MathUtils.smoothstep(cycleProgress, 0, 0.78);
    const radius = THREE.MathUtils.lerp(4.5, CITY_LAYOUT_ISLAND.edgeWallRadius + 1.5, eased);
    const fadeOut = THREE.MathUtils.smoothstep(cycleProgress, 0.55, 0.95);
    const fadeIn = THREE.MathUtils.smoothstep(cycleProgress, 0, 0.12);
    const opacity = (isOverview ? 0.38 : 0.24) * fadeIn * (1 - fadeOut);

    if (meshRef.current) {
      meshRef.current.scale.set(radius, radius, 1);
    }

    if (materialRef.current) {
      materialRef.current.opacity = opacity;
    }
  });

  return (
    <mesh
      ref={meshRef}
      name="Layout_V2_App_Layer_AI_Pulse"
      position={[AI_PULSE_TIMING.origin[0], AI_PULSE_TIMING.origin[1], AI_PULSE_TIMING.origin[2]]}
      rotation={[-Math.PI / 2, 0, 0]}
    >
      <ringGeometry args={[0.992, 1, 192]} />
      <meshBasicMaterial
        ref={materialRef}
        blending={THREE.AdditiveBlending}
        color={BRAND_COLORS.energy}
        depthWrite={false}
        opacity={0.24}
        side={THREE.DoubleSide}
        toneMapped={false}
        transparent
      />
    </mesh>
  );
}

export function LivingEnergyLayer({ structures }: LivingEnergyLayerProps) {
  const activeDistrict = useScrollStore((state) => state.activeDistrict);
  const focusedDistrictId = useScrollStore((state) => state.focusedDistrictId);
  const hoveredDistrictId = useScrollStore((state) => state.hoveredDistrictId);
  const sceneIndex = useScrollStore((state) => state.sceneIndex);
  const routes = useMemo(
    () => buildRoutes({ activeDistrict, focusedDistrictId, hoveredDistrictId, sceneIndex, structures }),
    [activeDistrict, focusedDistrictId, hoveredDistrictId, sceneIndex, structures],
  );

  return (
    <group name="Living_Energy_Layer">
      <IntelligenceFogVeils sceneIndex={sceneIndex} />
      <LayoutV2PulseRing sceneIndex={sceneIndex} />
      <group name="Animated_Data_Flow_Routes">
        {routes.map((route) => (
          <AnimatedDataRoute key={route.id} route={route} />
        ))}
        <EnergyRouteMotes routes={routes} />
      </group>
      <group name="Status_Based_District_Glow">
        {structures.map((structure) => (
          <DistrictStatusGlow
            key={`${structure.id}-status-glow`}
            activeDistrict={activeDistrict}
            focusedDistrictId={focusedDistrictId}
            hoveredDistrictId={hoveredDistrictId}
            sceneIndex={sceneIndex}
            structure={structure}
          />
        ))}
      </group>
      <FloatingMoteField
        color={BRAND_COLORS.purple}
        countPerDistrict={30}
        ids={["sia-tower", "analytics"]}
        name="Purple_AI_Scan_Motes"
        salt={16}
        size={0.24}
        structures={structures}
      />
      <FloatingMoteField
        color="#6EE7B7"
        countPerDistrict={24}
        ids={["yoga", "relationships", "nutrition"]}
        name="Green_Gentle_Lift_Motes"
        salt={24}
        size={0.22}
        structures={structures}
      />
    </group>
  );
}

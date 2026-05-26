import { Html } from "@react-three/drei";
import { useEffect, useMemo, useState, type CSSProperties } from "react";
import * as THREE from "three";
import {
  getDistrictProfile,
  OVERVIEW_LABEL_LAYOUTS,
  OVERVIEW_SCENES,
  SIA_FOCUS_SCENES,
  type DistrictProfile,
} from "../../lib/district-metadata";
import { CITY_LAYOUT_ISLAND } from "../../lib/city-layout-v2";
import { BRAND_COLORS } from "../../lib/materials";
import type { StructureAsset, Vec3 } from "../../lib/types";
import { BuildingInteractionLayer } from "./BuildingInteractionLayer";
import { DistrictLabelBoard, type DistrictLabelBoardState } from "./DistrictLabelBoard";

type CityContextProps = {
  structures: StructureAsset[];
  activeDistrict: string;
  focusedDistrictId?: string;
  hoveredDistrictId?: string;
  sceneIndex: number;
};

const ISLAND_SEGMENTS = 112;
const RETAINING_WALL_SEGMENTS = 72;
const WALL_GATE_HALF_ANGLE = 0.07;
const DISTRICT_GATE_ANGLE = -Math.PI / 2;

const SURFACE = {
  base: "#11131A",
  boundary: "#4C342A",
  canal: "#164246",
  edgeGlow: "#8B3B18",
  edgeWall: "#18141A",
  glass: "#182633",
  islandSkirt: "#090A0E",
  lamp: "#FFB066",
  outerMass: "#0B0D13",
  parapet: "#25212A",
  plaza: "#24222A",
  road: "#242632",
  roadEdge: "#4B4E60",
  roadPrimary: "#2D303E",
  shoreline: "#30251F",
  sidewalk: "#363847",
  stone: "#332D27",
};

const CROSS_DISTRICT_GROUND_CONNECTIONS = [
  ["fitness", "recovery"],
  ["nutrition", "career"],
  ["relationships", "yoga"],
  ["finance", "career"],
  ["recovery", "analytics"],
  ["chat", "relationships"],
] as const;

function planarLength([x, , z]: Vec3) {
  return Math.hypot(x, z);
}

function normalizePlanar([x, y, z]: Vec3): Vec3 {
  const length = Math.max(planarLength([x, y, z]), 0.0001);
  return [x / length, y, z / length];
}

function tangential([x, y, z]: Vec3): Vec3 {
  return [-z, y, x];
}

function yawAlong(start: Vec3, end: Vec3) {
  return -Math.atan2(end[2] - start[2], end[0] - start[0]);
}

function yawTowardCenter(position: Vec3) {
  return Math.atan2(position[0], position[2]);
}

function angularDistance(first: number, second: number) {
  return Math.abs(Math.atan2(Math.sin(first - second), Math.cos(first - second)));
}

function profileFor(structure: StructureAsset) {
  return getDistrictProfile(structure.id);
}

function useIsMobileViewport() {
  const [isMobileViewport, setIsMobileViewport] = useState(
    () => typeof window !== "undefined" && window.matchMedia("(max-width: 720px)").matches,
  );

  useEffect(() => {
    const query = window.matchMedia("(max-width: 720px)");
    const update = () => setIsMobileViewport(query.matches);

    update();
    query.addEventListener("change", update);

    return () => query.removeEventListener("change", update);
  }, []);

  return isMobileViewport;
}

function islandPoint(angle: number): Vec3 {
  const wobble =
    1 +
    Math.sin(angle * 3 + 0.35) * 0.045 +
    Math.sin(angle * 7 - 0.9) * 0.028 +
    Math.cos(angle * 11 + 0.5) * 0.016;

  return [
    Math.cos(angle) * CITY_LAYOUT_ISLAND.radiusX * wobble,
    0,
    Math.sin(angle) * CITY_LAYOUT_ISLAND.radiusZ * wobble,
  ];
}

function GroundStrip({
  color,
  emissiveIntensity = 0,
  length,
  opacity = 1,
  position = [0, 0.08, 0],
  rotationY = 0,
  width,
}: {
  color: string;
  emissiveIntensity?: number;
  length: number;
  opacity?: number;
  position?: Vec3;
  rotationY?: number;
  width: number;
}) {
  return (
    <mesh position={position} rotation={[0, rotationY, 0]}>
      <boxGeometry args={[length, 0.03, width]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={emissiveIntensity}
        metalness={0.08}
        opacity={opacity}
        roughness={0.48}
        toneMapped={emissiveIntensity === 0}
        transparent={opacity < 1}
      />
    </mesh>
  );
}

function FlatRing({
  color,
  emissiveIntensity = 0,
  inner,
  opacity = 1,
  outer,
  segments = 192,
  y = 0.055,
}: {
  color: string;
  emissiveIntensity?: number;
  inner: number;
  opacity?: number;
  outer: number;
  segments?: number;
  y?: number;
}) {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, y, 0]}>
      <ringGeometry args={[inner, outer, segments]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={emissiveIntensity}
        metalness={0.08}
        opacity={opacity}
        roughness={0.58}
        side={THREE.DoubleSide}
        toneMapped={emissiveIntensity === 0}
        transparent={opacity < 1}
      />
    </mesh>
  );
}

function IslandGround() {
  const islandShape = useMemo(() => {
    const shape = new THREE.Shape();

    for (let index = 0; index <= ISLAND_SEGMENTS; index += 1) {
      const [x, , z] = islandPoint((index / ISLAND_SEGMENTS) * Math.PI * 2);

      if (index === 0) {
        shape.moveTo(x, z);
      } else {
        shape.lineTo(x, z);
      }
    }

    shape.closePath();
    return shape;
  }, []);

  const shorelineSegments = useMemo(
    () =>
      Array.from({ length: ISLAND_SEGMENTS }, (_, index) => {
        const start = islandPoint((index / ISLAND_SEGMENTS) * Math.PI * 2);
        const end = islandPoint(((index + 1) / ISLAND_SEGMENTS) * Math.PI * 2);
        return {
          end,
          length: Math.hypot(end[0] - start[0], end[2] - start[2]),
          midpoint: [(start[0] + end[0]) / 2, 0.028, (start[2] + end[2]) / 2] satisfies Vec3,
          rotationY: yawAlong(start, end),
        };
      }),
    [],
  );

  return (
    <group name="Irregular_Urban_Island">
      <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.072, 0]}>
        <shapeGeometry args={[islandShape]} />
        <meshStandardMaterial color={SURFACE.islandSkirt} metalness={0.02} roughness={0.92} />
      </mesh>
      <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.032, 0]}>
        <shapeGeometry args={[islandShape]} />
        <meshStandardMaterial color={SURFACE.base} metalness={0.03} roughness={0.86} />
      </mesh>
      {shorelineSegments.map((segment, index) => (
        <GroundStrip
          key={`shoreline-${index}`}
          color={index % 7 === 0 ? SURFACE.edgeGlow : SURFACE.shoreline}
          emissiveIntensity={index % 7 === 0 ? 0.08 : 0}
          length={segment.length}
          opacity={0.72}
          position={segment.midpoint}
          rotationY={segment.rotationY}
          width={0.24}
        />
      ))}
    </group>
  );
}

function BoulevardToDistrict({ structure }: { structure: StructureAsset }) {
  if (structure.id === "sia-tower") {
    return null;
  }

  const profile = profileFor(structure);
  const direction = normalizePlanar(structure.position);
  const start: Vec3 = [direction[0] * 14.8, 0.07, direction[2] * 14.8];
  const end: Vec3 = [
    structure.position[0] - direction[0] * 8.3,
    0.07,
    structure.position[2] - direction[2] * 8.3,
  ];
  const midpoint: Vec3 = [(start[0] + end[0]) / 2, 0.09, (start[2] + end[2]) / 2];
  const length = Math.hypot(end[0] - start[0], end[2] - start[2]);
  const angle = yawAlong(start, end);
  const laneMarks = [-0.32, -0.12, 0.08, 0.28];

  return (
    <group name={`${structure.id}_radial_boulevard`} position={midpoint} rotation={[0, angle, 0]}>
      <mesh receiveShadow>
        <boxGeometry args={[length, 0.052, 5.8]} />
        <meshStandardMaterial color={SURFACE.roadPrimary} metalness={0.05} roughness={0.7} />
      </mesh>
      <mesh position={[0, 0.04, -3.25]}>
        <boxGeometry args={[length, 0.034, 0.72]} />
        <meshStandardMaterial color={SURFACE.sidewalk} metalness={0.08} roughness={0.62} />
      </mesh>
      <mesh position={[0, 0.04, 3.25]}>
        <boxGeometry args={[length, 0.034, 0.72]} />
        <meshStandardMaterial color={SURFACE.sidewalk} metalness={0.08} roughness={0.62} />
      </mesh>
      <mesh position={[0, 0.06, 0]}>
        <boxGeometry args={[length, 0.022, 0.18]} />
        <meshStandardMaterial
          color={BRAND_COLORS.energy}
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={0.42}
          opacity={0.82}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh position={[0, 0.065, -2.35]}>
        <boxGeometry args={[length, 0.018, 0.12]} />
        <meshStandardMaterial
          color={profile.motifColor}
          emissive={profile.motifColor}
          emissiveIntensity={0.18}
          opacity={0.76}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh position={[0, 0.065, 2.35]}>
        <boxGeometry args={[length, 0.018, 0.12]} />
        <meshStandardMaterial
          color={profile.motifColor}
          emissive={profile.motifColor}
          emissiveIntensity={0.18}
          opacity={0.76}
          toneMapped={false}
          transparent
        />
      </mesh>
      {laneMarks.map((offset, index) => (
        <mesh key={`${structure.id}-lane-${index}`} position={[length * offset, 0.072, 0]}>
          <boxGeometry args={[length * 0.08, 0.018, 0.09]} />
          <meshStandardMaterial color="#C7B9A8" opacity={0.32} transparent />
        </mesh>
      ))}
      {[-0.5, 0.5].map((offset) => (
        <mesh key={`${structure.id}-junction-${offset}`} position={[length * offset, 0.08, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[1.08, 1.26, 36]} />
          <meshStandardMaterial
            color={profile.motifColor}
            emissive={profile.motifColor}
            emissiveIntensity={0.18}
            opacity={0.56}
            side={THREE.DoubleSide}
            toneMapped={false}
            transparent
          />
        </mesh>
      ))}
    </group>
  );
}

function CentralCivicPlaza({ sceneIndex }: { sceneIndex: number }) {
  const isSiaFocus = SIA_FOCUS_SCENES.has(sceneIndex);
  const overviewBoost = OVERVIEW_SCENES.has(sceneIndex) ? 1.08 : 1;
  const glowScale = (isSiaFocus ? 1.18 : 0.76) * overviewBoost;
  const spokes = useMemo(
    () =>
      Array.from({ length: 16 }, (_, index) => {
        const angle = (index / 16) * Math.PI * 2;
        return { angle, x: Math.cos(angle) * 7.7, z: Math.sin(angle) * 7.7 };
      }),
    [],
  );

  return (
    <group name="SIA_Civic_Plaza">
      <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.076, 0]}>
        <circleGeometry args={[15.8, 128]} />
        <meshStandardMaterial color={SURFACE.plaza} metalness={0.16} roughness={0.46} />
      </mesh>
      <FlatRing color={SURFACE.sidewalk} inner={10.6} outer={11.28} y={0.095} />
      <FlatRing
        color={BRAND_COLORS.energy}
        emissiveIntensity={0.42 * glowScale}
        inner={13.2}
        opacity={0.88}
        outer={13.58}
        y={0.104}
      />
      <FlatRing color="#463429" emissiveIntensity={0.08 * glowScale} inner={5.8} opacity={0.72} outer={6.12} y={0.108} />
      <FlatRing color={BRAND_COLORS.energy} emissiveIntensity={0.2 * glowScale} inner={16.7} opacity={0.46} outer={17.05} y={0.13} />
      {spokes.map((spoke) => (
        <GroundStrip
          key={`civic-spoke-${spoke.angle}`}
          color={spoke.angle % 2 > 1 ? BRAND_COLORS.gold : BRAND_COLORS.energy}
          emissiveIntensity={0.24 * glowScale}
          length={9.8}
          opacity={0.76}
          position={[spoke.x, 0.112, spoke.z]}
          rotationY={-spoke.angle}
          width={0.16}
        />
      ))}
      {[-1, 1].map((side) => (
        <GroundStrip
          key={`civic-crosswalk-${side}`}
          color="#BFA68E"
          length={14.5}
          opacity={0.24}
          position={[0, 0.116, side * 3.8]}
          width={0.16}
        />
      ))}
    </group>
  );
}

function SiaHierarchyBeacon({ sceneIndex }: { sceneIndex: number }) {
  const isSiaFocus = SIA_FOCUS_SCENES.has(sceneIndex);
  const intensity = sceneIndex === 2 ? 1.42 : OVERVIEW_SCENES.has(sceneIndex) ? 1.08 : isSiaFocus ? 0.92 : 0.5;
  const beaconOpacity = sceneIndex === 2 ? 0.62 : OVERVIEW_SCENES.has(sceneIndex) ? 0.48 : 0.32;

  return (
    <group name="SIA_App_Layer_Hierarchy">
      <mesh position={[0, 0.18, 0]}>
        <cylinderGeometry args={[18.2, 19.4, 0.32, 96]} />
        <meshStandardMaterial color="#211C22" metalness={0.16} roughness={0.46} />
      </mesh>
      <mesh position={[0, 0.44, 0]}>
        <cylinderGeometry args={[13.4, 14.4, 0.22, 96]} />
        <meshStandardMaterial color="#2B2225" metalness={0.18} roughness={0.42} />
      </mesh>
      <mesh position={[0, 0.59, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[8.2, 8.75, 96]} />
        <meshStandardMaterial
          color={BRAND_COLORS.energy}
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={0.55 * intensity}
          opacity={0.78}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      {[0, 1, 2].map((index) => (
        <mesh
          key={`sia-crown-halo-${index}`}
          position={[0, 42.4 + index * 2.2, 0]}
          rotation={[Math.PI / 2, 0, 0]}
        >
          <torusGeometry args={[2.4 + index * 1.25, 0.035, 8, 96]} />
          <meshStandardMaterial
            color={index === 1 ? BRAND_COLORS.gold : BRAND_COLORS.energy}
            emissive={index === 1 ? BRAND_COLORS.gold : BRAND_COLORS.energy}
            emissiveIntensity={(1.1 - index * 0.18) * intensity}
            opacity={0.62 - index * 0.1}
            toneMapped={false}
            transparent
          />
        </mesh>
      ))}
      <mesh position={[0, 62, 0]}>
        <cylinderGeometry args={[0.08, 0.16, 68, 18]} />
        <meshBasicMaterial
          color={BRAND_COLORS.energy}
          opacity={beaconOpacity}
          transparent
          depthWrite={false}
          toneMapped={false}
        />
      </mesh>
      <pointLight
        color={BRAND_COLORS.energy}
        distance={90}
        intensity={sceneIndex === 2 ? 110 : OVERVIEW_SCENES.has(sceneIndex) ? 82 : 48}
        position={[0, 46, 0]}
      />
    </group>
  );
}

function DistrictPad({ structure }: { structure: StructureAsset }) {
  if (structure.id === "sia-tower") {
    return null;
  }

  const profile = profileFor(structure);
  const yaw = yawTowardCenter(structure.position);
  const [width, depth] = profile.padSize;
  const baseColor = profile.motif === "garden" || profile.motif === "farm" ? "#1D2B22" : SURFACE.stone;
  const apronWidth = width + 5.2;
  const apronDepth = depth + 4.8;

  return (
    <group
      name={`${structure.id}_urban_pad`}
      position={[structure.position[0], 0.07, structure.position[2]]}
      rotation={[0, yaw, 0]}
    >
      {profile.padShape === "rect" ? (
        <mesh receiveShadow position={[0, -0.005, 0]}>
          <boxGeometry args={[apronWidth, 0.046, apronDepth]} />
          <meshStandardMaterial color={SURFACE.sidewalk} metalness={0.06} roughness={0.68} />
        </mesh>
      ) : (
        <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.004, 0]} scale={[apronWidth / 2, apronDepth / 2, 1]}>
          <circleGeometry args={[1, profile.padShape === "octagon" ? 8 : 72]} />
          <meshStandardMaterial color={SURFACE.sidewalk} metalness={0.07} roughness={0.66} side={THREE.DoubleSide} />
        </mesh>
      )}
      {profile.padShape === "rect" ? (
        <mesh receiveShadow>
          <boxGeometry args={[width, 0.058, depth]} />
          <meshStandardMaterial color={baseColor} metalness={0.08} roughness={0.62} />
        </mesh>
      ) : (
        <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} scale={[width / 2, depth / 2, 1]}>
          <circleGeometry args={[1, profile.padShape === "octagon" ? 8 : 72]} />
          <meshStandardMaterial color={baseColor} metalness={0.08} roughness={0.58} side={THREE.DoubleSide} />
        </mesh>
      )}
      <DistrictMotif profile={profile} />
      <DistrictBoundaryRim profile={profile} />
      <mesh position={[0, 0.102, -depth * 0.54]}>
        <boxGeometry args={[Math.min(width * 0.68, 11), 0.34, 0.16]} />
        <meshStandardMaterial
          color={profile.motifColor}
          emissive={profile.motifColor}
          emissiveIntensity={0.48}
          opacity={0.88}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh position={[0, 0.112, -depth * 0.74]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.6, 2.05, 48]} />
        <meshStandardMaterial
          color={profile.motifColor}
          emissive={profile.motifColor}
          emissiveIntensity={0.34}
          opacity={0.74}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh position={[0, 0.24, -depth * 0.74]}>
        <sphereGeometry args={[0.24, 12, 12]} />
        <meshStandardMaterial
          color={profile.motifColor}
          emissive={profile.motifColor}
          emissiveIntensity={0.8}
          toneMapped={false}
        />
      </mesh>
    </group>
  );
}

function DistrictBoundaryRim({ profile }: { profile: DistrictProfile }) {
  const [width, depth] = profile.padSize;
  const apronWidth = width + 5.2;
  const apronDepth = depth + 4.8;
  const rimColor = profile.motifColor;

  if (profile.padShape === "rect") {
    const wallHeight = 0.48;
    const wallThickness = 0.28;
    const gateWidth = Math.min(width * 0.46, 8.6);
    const frontSegment = Math.max((apronWidth - gateWidth) / 2 - wallThickness, 2.2);

    return (
      <group name={`${profile.motif}_zoning_parapet`}>
        <mesh position={[0, wallHeight / 2, apronDepth / 2]}>
          <boxGeometry args={[apronWidth, wallHeight, wallThickness]} />
          <meshStandardMaterial color={SURFACE.parapet} metalness={0.08} roughness={0.58} />
        </mesh>
        <mesh position={[-apronWidth / 2, wallHeight / 2, 0]}>
          <boxGeometry args={[wallThickness, wallHeight, apronDepth]} />
          <meshStandardMaterial color={SURFACE.parapet} metalness={0.08} roughness={0.58} />
        </mesh>
        <mesh position={[apronWidth / 2, wallHeight / 2, 0]}>
          <boxGeometry args={[wallThickness, wallHeight, apronDepth]} />
          <meshStandardMaterial color={SURFACE.parapet} metalness={0.08} roughness={0.58} />
        </mesh>
        {[-1, 1].map((side) => (
          <mesh
            key={`${profile.motif}-front-parapet-${side}`}
            position={[side * (gateWidth / 2 + frontSegment / 2), wallHeight / 2, -apronDepth / 2]}
          >
            <boxGeometry args={[frontSegment, wallHeight, wallThickness]} />
            <meshStandardMaterial color={SURFACE.parapet} metalness={0.08} roughness={0.58} />
          </mesh>
        ))}
        <GroundStrip
          color={rimColor}
          emissiveIntensity={0.34}
          length={apronWidth - 1.2}
          opacity={0.78}
          position={[0, 0.59, apronDepth / 2 + 0.03]}
          width={0.1}
        />
        <GroundStrip
          color={rimColor}
          emissiveIntensity={0.22}
          length={apronDepth - 1}
          opacity={0.64}
          position={[-apronWidth / 2 - 0.03, 0.59, 0]}
          rotationY={Math.PI / 2}
          width={0.1}
        />
        <GroundStrip
          color={rimColor}
          emissiveIntensity={0.22}
          length={apronDepth - 1}
          opacity={0.64}
          position={[apronWidth / 2 + 0.03, 0.59, 0]}
          rotationY={Math.PI / 2}
          width={0.1}
        />
      </group>
    );
  }

  const posts = Array.from({ length: profile.padShape === "octagon" ? 8 : 14 }, (_, index) => {
    const angle = (index / (profile.padShape === "octagon" ? 8 : 14)) * Math.PI * 2;
    return angle;
  }).filter((angle) => angularDistance(angle, DISTRICT_GATE_ANGLE) > 0.42);

  return (
    <group name={`${profile.motif}_curved_zoning_parapet`}>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.096, 0]} scale={[apronWidth / 2, apronDepth / 2, 1]}>
        <ringGeometry args={[0.92, 1, profile.padShape === "octagon" ? 8 : 96]} />
        <meshStandardMaterial
          color={rimColor}
          emissive={rimColor}
          emissiveIntensity={0.24}
          opacity={0.54}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      {posts.map((angle) => (
        <mesh
          key={`${profile.motif}-rim-post-${angle}`}
          position={[
            Math.cos(angle) * (apronWidth / 2),
            0.3,
            Math.sin(angle) * (apronDepth / 2),
          ]}
          rotation={[0, -angle, 0]}
        >
          <boxGeometry args={[0.34, 0.6, 0.62]} />
          <meshStandardMaterial color={SURFACE.parapet} emissive={rimColor} emissiveIntensity={0.08} roughness={0.58} />
        </mesh>
      ))}
    </group>
  );
}

function DistrictMotif({ profile }: { profile: DistrictProfile }) {
  const [width, depth] = profile.padSize;
  const color = profile.motifColor;
  const lineOpacity = profile.motif === "sleep" ? 0.5 : 0.76;

  if (profile.motif === "arena" || profile.motif === "sanctuary" || profile.motif === "sleep") {
    return (
      <group name={`${profile.motif}_motif`}>
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.065, 0]} scale={[width * 0.3, depth * 0.3, 1]}>
          <ringGeometry args={[0.72, 1, 72]} />
          <meshStandardMaterial
            color={color}
            emissive={color}
            emissiveIntensity={0.3}
            opacity={lineOpacity}
            side={THREE.DoubleSide}
            toneMapped={false}
            transparent
          />
        </mesh>
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.071, 0]} scale={[width * 0.17, depth * 0.17, 1]}>
          <ringGeometry args={[0.72, 1, 64]} />
          <meshStandardMaterial
            color={profile.motif === "sleep" ? "#9AA3FF" : color}
            emissive={color}
            emissiveIntensity={0.22}
            opacity={0.62}
            side={THREE.DoubleSide}
            toneMapped={false}
            transparent
          />
        </mesh>
        {profile.motif === "sanctuary" || profile.motif === "sleep" ? (
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.052, 0]} scale={[width * 0.38, depth * 0.25, 1]}>
            <circleGeometry args={[1, 54]} />
            <meshStandardMaterial
              color={SURFACE.canal}
              metalness={0.22}
              opacity={0.58}
              roughness={0.16}
              side={THREE.DoubleSide}
              transparent
            />
          </mesh>
        ) : null}
      </group>
    );
  }

  if (profile.motif === "bank" || profile.motif === "library" || profile.motif === "analytics") {
    return (
      <group name={`${profile.motif}_motif`}>
        {[-0.3, 0, 0.3].map((offset) => (
          <GroundStrip
            key={`${profile.motif}-vertical-${offset}`}
            color={color}
            emissiveIntensity={0.22}
            length={depth * 0.76}
            opacity={0.72}
            position={[width * offset, 0.075, 0]}
            rotationY={Math.PI / 2}
            width={0.14}
          />
        ))}
        {[-0.25, 0.25].map((offset) => (
          <GroundStrip
            key={`${profile.motif}-horizontal-${offset}`}
            color={profile.motif === "analytics" ? "#14B8A6" : SURFACE.roadEdge}
            emissiveIntensity={profile.motif === "analytics" ? 0.18 : 0.02}
            length={width * 0.78}
            opacity={0.72}
            position={[0, 0.078, depth * offset]}
            width={0.14}
          />
        ))}
      </group>
    );
  }

  if (profile.motif === "garden" || profile.motif === "farm") {
    return (
      <group name={`${profile.motif}_motif`}>
        {[-0.36, -0.18, 0, 0.18, 0.36].map((offset) => (
          <GroundStrip
            key={`${profile.motif}-bed-${offset}`}
            color={profile.motif === "farm" ? "#386D36" : "#335044"}
            emissiveIntensity={0.05}
            length={width * 0.66}
            opacity={0.94}
            position={[0, 0.069, depth * offset]}
            width={0.5}
          />
        ))}
        <GroundStrip
          color={color}
          emissiveIntensity={0.2}
          length={width * 0.72}
          opacity={0.72}
          position={[0, 0.088, 0]}
          width={0.13}
        />
      </group>
    );
  }

  return (
    <group name={`${profile.motif}_motif`}>
      {[-0.34, 0, 0.34].map((offset) => (
        <GroundStrip
          key={`${profile.motif}-line-${offset}`}
          color={color}
          emissiveIntensity={0.24}
          length={width * 0.72}
          opacity={0.76}
          position={[0, 0.074, depth * offset]}
          width={0.14}
        />
      ))}
      {profile.motif === "signal" || profile.motif === "career" ? (
        <GroundStrip
          color={profile.motif === "career" ? "#7DB2FF" : BRAND_COLORS.energy}
          emissiveIntensity={0.22}
          length={depth * 0.66}
          opacity={0.72}
          position={[0, 0.082, 0]}
          rotationY={Math.PI / 2}
          width={0.12}
        />
      ) : null}
    </group>
  );
}

function ReflectiveCanalSpurs({ structures }: { structures: StructureAsset[] }) {
  return (
    <group name="Reflective_Canal_And_Park_Strips">
      {structures
        .filter((structure) => {
          const motif = profileFor(structure).motif;
          return motif === "sanctuary" || motif === "garden" || motif === "sleep" || motif === "farm";
        })
        .map((structure) => {
          const direction = normalizePlanar(structure.position);
          const tangent = tangential(direction);
          const start: Vec3 = [direction[0] * 30 + tangent[0] * 2.2, 0.048, direction[2] * 30 + tangent[2] * 2.2];
          const end: Vec3 = [
            structure.position[0] - direction[0] * 9 + tangent[0] * 2.2,
            0.048,
            structure.position[2] - direction[2] * 9 + tangent[2] * 2.2,
          ];
          const midpoint: Vec3 = [(start[0] + end[0]) / 2, 0.062, (start[2] + end[2]) / 2];
          const length = Math.hypot(end[0] - start[0], end[2] - start[2]);

          return (
            <GroundStrip
              key={`${structure.id}-canal-spur`}
              color={SURFACE.canal}
              emissiveIntensity={0.06}
              length={length}
              opacity={0.72}
              position={midpoint}
              rotationY={yawAlong(start, end)}
              width={1.18}
            />
          );
        })}
    </group>
  );
}

function CrossDistrictGroundConnections({ structures }: { structures: StructureAsset[] }) {
  const structureMap = useMemo(() => new Map(structures.map((structure) => [structure.id, structure])), [structures]);

  return (
    <group name="Ground_Level_Cross_District_Intelligence_Lanes">
      {CROSS_DISTRICT_GROUND_CONNECTIONS.map(([fromId, toId]) => {
        const from = structureMap.get(fromId);
        const to = structureMap.get(toId);

        if (!from || !to) {
          return null;
        }

        const fromDirection = normalizePlanar(from.position);
        const toDirection = normalizePlanar(to.position);
        const start: Vec3 = [
          from.position[0] - fromDirection[0] * 8,
          0.14,
          from.position[2] - fromDirection[2] * 8,
        ];
        const end: Vec3 = [to.position[0] - toDirection[0] * 8, 0.14, to.position[2] - toDirection[2] * 8];
        const midpoint: Vec3 = [(start[0] + end[0]) / 2, 0.145, (start[2] + end[2]) / 2];

        return (
          <GroundStrip
            key={`${fromId}-${toId}-ground-connection`}
            color={BRAND_COLORS.gold}
            emissiveIntensity={0.22}
            length={Math.hypot(end[0] - start[0], end[2] - start[2])}
            opacity={0.68}
            position={midpoint}
            rotationY={yawAlong(start, end)}
            width={0.16}
          />
        );
      })}
    </group>
  );
}

function CityBlockInfill({ structures }: { structures: StructureAsset[] }) {
  const blocks = useMemo(() => {
    return structures
      .filter((structure) => structure.id !== "sia-tower")
      .flatMap((structure, structureIndex) => {
        const direction = normalizePlanar(structure.position);
        const tangent = tangential(direction);
        const distance = planarLength(structure.position);

        return [0, 1, 2].flatMap((cluster) =>
          [-1, 1].map((side) => {
            const width = 2.2 + ((structureIndex + cluster) % 4) * 0.55;
            const depth = 2.4 + ((structureIndex + cluster * 2) % 5) * 0.38;
            const height = 1.2 + ((structureIndex * 1.7 + cluster) % 4) * 0.74;
            const radial = Math.max(18, distance - 11 - cluster * 3.2);
            const tangentOffset = side * (6.8 + cluster * 3.2 + (structureIndex % 2) * 0.8);
            const x = direction[0] * radial + tangent[0] * tangentOffset;
            const z = direction[2] * radial + tangent[2] * tangentOffset;

            return {
              color: structure.hex,
              depth,
              height,
              key: `${structure.id}-${cluster}-${side}`,
              position: [x, height / 2 + 0.09, z] satisfies Vec3,
              rotationY: yawTowardCenter(structure.position) + side * 0.18,
              width,
            };
          }),
        );
      });
  }, [structures]);

  return (
    <group name="Low_Rise_City_Block_Infill">
      {blocks.map((block) => (
        <group key={block.key} position={block.position} rotation={[0, block.rotationY, 0]}>
          <mesh castShadow receiveShadow>
            <boxGeometry args={[block.width, block.height, block.depth]} />
            <meshStandardMaterial color={SURFACE.glass} metalness={0.08} roughness={0.5} />
          </mesh>
          <mesh position={[0, block.height * 0.2, -block.depth / 2 - 0.018]}>
            <boxGeometry args={[block.width * 0.62, 0.09, 0.026]} />
            <meshStandardMaterial
              color={block.color}
              emissive={block.color}
              emissiveIntensity={0.22}
              opacity={0.7}
              toneMapped={false}
              transparent
            />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function OuterDepthBands({ sceneIndex }: { sceneIndex: number }) {
  const overviewOpacity = OVERVIEW_SCENES.has(sceneIndex) ? 0.72 : 0.54;

  return (
    <group name="Outer_Depth_Separation_Bands">
      <FlatRing color={SURFACE.outerMass} inner={94.4} opacity={overviewOpacity} outer={114.8} y={0.012} />
      <FlatRing color="#120D0B" emissiveIntensity={0.05} inner={91.4} opacity={0.72} outer={92.8} y={0.095} />
      <FlatRing
        color={BRAND_COLORS.energy}
        emissiveIntensity={OVERVIEW_SCENES.has(sceneIndex) ? 0.22 : 0.12}
        inner={101.8}
        opacity={0.38}
        outer={102.18}
        y={0.15}
      />
    </group>
  );
}

function ImmersiveRetainingWalls({ structures }: { structures: StructureAsset[] }) {
  const wallSegments = useMemo(() => {
    const gateAngles = structures
      .filter((structure) => structure.id !== "sia-tower")
      .map((structure) => Math.atan2(structure.position[2], structure.position[0]));

    return Array.from({ length: RETAINING_WALL_SEGMENTS }, (_, index) => {
      const startAngle = (index / RETAINING_WALL_SEGMENTS) * Math.PI * 2;
      const endAngle = ((index + 1) / RETAINING_WALL_SEGMENTS) * Math.PI * 2;
      const midpointAngle = (startAngle + endAngle) / 2;
      const isGate = gateAngles.some((angle) => angularDistance(midpointAngle, angle) < WALL_GATE_HALF_ANGLE);

      if (isGate) {
        return null;
      }

      const start = islandPoint(startAngle);
      const end = islandPoint(endAngle);
      const inward = normalizePlanar([
        -(start[0] + end[0]) / 2,
        0,
        -(start[2] + end[2]) / 2,
      ]);
      const height = 0.72 + (index % 4) * 0.08;

      return {
        height,
        key: `retaining-wall-${index}`,
        length: Math.hypot(end[0] - start[0], end[2] - start[2]) * 0.92,
        position: [
          (start[0] + end[0]) / 2 + inward[0] * 2.3,
          height / 2 + 0.05,
          (start[2] + end[2]) / 2 + inward[2] * 2.3,
        ] satisfies Vec3,
        rotationY: yawAlong(start, end),
      };
    }).filter((segment): segment is NonNullable<typeof segment> => Boolean(segment));
  }, [structures]);

  const gatePiers = useMemo(
    () =>
      structures
        .filter((structure) => structure.id !== "sia-tower")
        .flatMap((structure) => {
          const angle = Math.atan2(structure.position[2], structure.position[0]);
          const [edgeX, , edgeZ] = islandPoint(angle);
          const inward = normalizePlanar([-edgeX, 0, -edgeZ]);
          const tangent = tangential(inward);
          const profile = profileFor(structure);

          return [-1, 1].map((side) => ({
            color: profile.motifColor,
            key: `${structure.id}-gate-pier-${side}`,
            position: [
              edgeX + inward[0] * 3.1 + tangent[0] * side * 1.4,
              0.56,
              edgeZ + inward[2] * 3.1 + tangent[2] * side * 1.4,
            ] satisfies Vec3,
            rotationY: -angle,
          }));
        }),
    [structures],
  );

  return (
    <group name="Immersive_Retaining_Walls">
      {wallSegments.map((segment) => (
        <group key={segment.key} position={segment.position} rotation={[0, segment.rotationY, 0]}>
          <mesh castShadow receiveShadow>
            <boxGeometry args={[segment.length, segment.height, 0.62]} />
            <meshStandardMaterial color={SURFACE.edgeWall} metalness={0.1} roughness={0.62} />
          </mesh>
          <mesh position={[0, segment.height / 2 + 0.035, -0.08]}>
            <boxGeometry args={[segment.length * 0.82, 0.055, 0.1]} />
            <meshStandardMaterial
              color={SURFACE.edgeGlow}
              emissive={BRAND_COLORS.energy}
              emissiveIntensity={0.12}
              opacity={0.56}
              toneMapped={false}
              transparent
            />
          </mesh>
        </group>
      ))}
      {gatePiers.map((pier) => (
        <group key={pier.key} position={pier.position} rotation={[0, pier.rotationY, 0]}>
          <mesh castShadow receiveShadow>
            <boxGeometry args={[0.62, 1.12, 0.88]} />
            <meshStandardMaterial color={SURFACE.boundary} emissive={pier.color} emissiveIntensity={0.1} roughness={0.52} />
          </mesh>
          <mesh position={[0, 0.62, 0]}>
            <sphereGeometry args={[0.16, 10, 10]} />
            <meshStandardMaterial color={pier.color} emissive={pier.color} emissiveIntensity={0.74} toneMapped={false} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function PerimeterContext() {
  const edgeBlocks = useMemo(
    () =>
      Array.from({ length: 48 }, (_, index) => {
        const angle = (index / 48) * Math.PI * 2 + 0.04;
        const [edgeX, , edgeZ] = islandPoint(angle);
        const inward = normalizePlanar([-edgeX, 0, -edgeZ]);
        const height = 0.9 + (index % 6) * 0.3;
        return {
          angle,
          height,
          key: `edge-block-${index}`,
          position: [edgeX + inward[0] * 8.0, height / 2 + 0.04, edgeZ + inward[2] * 8.0] satisfies Vec3,
          width: 2.1 + (index % 4) * 0.55,
        };
      }),
    [],
  );

  return (
    <group name="Urban_Edge_Context">
      {edgeBlocks.map((block) => (
        <group key={block.key} position={block.position} rotation={[0, -block.angle, 0]}>
          <mesh castShadow receiveShadow>
            <boxGeometry args={[block.width, block.height, 1.72]} />
            <meshStandardMaterial color="#131923" metalness={0.06} roughness={0.56} />
          </mesh>
          <mesh position={[0, block.height * 0.22, -0.88]}>
            <boxGeometry args={[block.width * 0.5, 0.06, 0.025]} />
            <meshStandardMaterial
              color={BRAND_COLORS.energy}
              emissive={BRAND_COLORS.energy}
              emissiveIntensity={0.1}
              opacity={0.45}
              toneMapped={false}
              transparent
            />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function StreetLamps({ structures }: { structures: StructureAsset[] }) {
  const lamps = useMemo(() => {
    return structures
      .filter((structure) => structure.id !== "sia-tower")
      .flatMap((structure, structureIndex) => {
        const direction = normalizePlanar(structure.position);
        const tangent = tangential(direction);
        return [0.28, 0.68].flatMap((step, stepIndex) =>
          [-1, 1].map((side) => {
            const radius = THREE.MathUtils.lerp(17, planarLength(structure.position) - 7, step);
            return {
              color: structure.hex,
              key: `${structure.id}-${structureIndex}-${stepIndex}-${side}`,
              position: [
                direction[0] * radius + tangent[0] * side * 3.65,
                0.82,
                direction[2] * radius + tangent[2] * side * 3.65,
              ] satisfies Vec3,
            };
          }),
        );
      });
  }, [structures]);

  return (
    <group name="Urban_Street_Lamps">
      {lamps.map((lamp) => (
        <group key={lamp.key} position={lamp.position}>
          <mesh position={[0, -0.36, 0]}>
            <cylinderGeometry args={[0.035, 0.052, 0.76, 8]} />
            <meshStandardMaterial color="#30313A" metalness={0.25} roughness={0.5} />
          </mesh>
          <mesh>
            <sphereGeometry args={[0.12, 10, 10]} />
            <meshStandardMaterial color={SURFACE.lamp} emissive={lamp.color} emissiveIntensity={0.58} toneMapped={false} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function UrbanAtlasGround({ sceneIndex, structures }: { sceneIndex: number; structures: StructureAsset[] }) {
  return (
    <group name="Urban_Atlas_Ground">
      <IslandGround />
      <OuterDepthBands sceneIndex={sceneIndex} />
      <FlatRing color={SURFACE.roadPrimary} inner={20.8} outer={25.4} y={0.045} />
      <FlatRing color={SURFACE.roadPrimary} inner={48.0} outer={53.8} y={0.047} />
      <FlatRing color={SURFACE.road} inner={82.4} outer={88.4} y={0.049} />
      <FlatRing color={SURFACE.sidewalk} inner={25.45} outer={26.05} y={0.072} />
      <FlatRing color={SURFACE.sidewalk} inner={47.28} outer={47.82} y={0.072} />
      <FlatRing color={SURFACE.sidewalk} inner={54.0} outer={54.55} y={0.073} />
      <FlatRing color={SURFACE.roadEdge} inner={88.55} outer={88.95} y={0.074} />
      <FlatRing
        color={BRAND_COLORS.energy}
        emissiveIntensity={0.26}
        inner={90.8}
        opacity={0.78}
        outer={91.12}
        y={0.082}
      />
      <FlatRing color={SURFACE.canal} emissiveIntensity={0.04} inner={36.8} opacity={0.82} outer={37.9} y={0.052} />
      <FlatRing color={SURFACE.canal} emissiveIntensity={0.04} inner={66.8} opacity={0.78} outer={68.1} y={0.052} />
      <CentralCivicPlaza sceneIndex={sceneIndex} />
      <SiaHierarchyBeacon sceneIndex={sceneIndex} />
      {structures.map((structure) => (
        <BoulevardToDistrict key={`${structure.id}-boulevard`} structure={structure} />
      ))}
      {structures.map((structure) => (
        <DistrictPad key={`${structure.id}-pad`} structure={structure} />
      ))}
      <ReflectiveCanalSpurs structures={structures} />
      <CrossDistrictGroundConnections structures={structures} />
      <CityBlockInfill structures={structures} />
      <ImmersiveRetainingWalls structures={structures} />
      <PerimeterContext />
      <StreetLamps structures={structures} />
    </group>
  );
}

function CuratedOverviewLabels({
  sceneIndex,
  structures,
}: {
  sceneIndex: number;
  structures: StructureAsset[];
}) {
  const layout = OVERVIEW_LABEL_LAYOUTS[sceneIndex] ?? OVERVIEW_LABEL_LAYOUTS[1];

  return (
    <Html fullscreen className="city-label-map-anchor" zIndexRange={[6, 0]}>
      <div className="city-label-map" aria-label="City district labels">
        {structures.map((structure) => {
          const profile = profileFor(structure);
          const screenPosition = layout[structure.id];

          if (!screenPosition) {
            return null;
          }

          return (
            <div
              key={`${structure.id}-screen-label`}
              className="city-label-map__item"
              style={{
                left: `${screenPosition.left}%`,
                maxWidth: screenPosition.maxWidth ? `${screenPosition.maxWidth}px` : undefined,
                top: `${screenPosition.top}%`,
              }}
            >
              <div
                className={[
                  "city-label",
                  "city-label--overview",
                  "city-label--screen",
                  `city-label--${profile.labelTier}`,
                ].join(" ")}
                style={{ "--district-color": profile.motifColor } as CSSProperties}
              >
                <span>{profile.label}</span>
                <small>{profile.place}</small>
              </div>
            </div>
          );
        })}
      </div>
    </Html>
  );
}

function MobileOverviewLabels({ structures }: { structures: StructureAsset[] }) {
  return (
    <Html fullscreen className="city-label-dock-anchor" zIndexRange={[7, 0]}>
      <div className="city-label-dock" aria-label="City district labels">
        {structures.map((structure) => {
          const profile = profileFor(structure);

          return (
            <div
              key={`${structure.id}-mobile-overview-label`}
              className={[
                "city-label",
                "city-label--overview",
                "city-label--dock-item",
                `city-label--${profile.labelTier}`,
              ].join(" ")}
              style={{ "--district-color": profile.motifColor } as CSSProperties}
            >
              <span>{profile.label}</span>
              <small>{profile.place}</small>
            </div>
          );
        })}
      </div>
    </Html>
  );
}

function DistrictLabels({
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
  const isOverview = OVERVIEW_SCENES.has(sceneIndex) || activeDistrict === "city";
  const isMobileViewport = useIsMobileViewport();

  return (
    <group name="Hybrid_District_Labels">
      {isOverview && !isMobileViewport ? (
        <CuratedOverviewLabels sceneIndex={sceneIndex} structures={structures} />
      ) : null}
      {isOverview && isMobileViewport ? <MobileOverviewLabels structures={structures} /> : null}
      <DistrictLabelBoards
        activeDistrict={activeDistrict}
        focusedDistrictId={focusedDistrictId}
        hoveredDistrictId={hoveredDistrictId}
        isOverview={isOverview}
        sceneIndex={sceneIndex}
        structures={structures}
      />
    </group>
  );
}

function DistrictLabelBoards({
  activeDistrict,
  focusedDistrictId,
  hoveredDistrictId,
  isOverview,
  sceneIndex,
  structures,
}: {
  activeDistrict: string;
  focusedDistrictId?: string;
  hoveredDistrictId?: string;
  isOverview: boolean;
  sceneIndex: number;
  structures: StructureAsset[];
}) {
  const boardStates = new Map<string, DistrictLabelBoardState>();
  const shouldShowActiveBoard = !isOverview && sceneIndex !== 3 && sceneIndex !== 16 && activeDistrict !== "city";

  if (shouldShowActiveBoard) {
    boardStates.set(activeDistrict, "active");
  }

  if (hoveredDistrictId) {
    boardStates.set(hoveredDistrictId, "hovered");
  }

  if (focusedDistrictId) {
    boardStates.set(focusedDistrictId, "focused");
  }

  if (!boardStates.size) {
    return null;
  }

  return (
    <group name="District_Label_Boards">
      {Array.from(boardStates.entries()).map(([districtId, revealState]) => {
        const structure = structures.find((candidate) => candidate.id === districtId);

        if (!structure) {
          return null;
        }

        return (
          <DistrictLabelBoard
            key={`${districtId}-label-board`}
            revealState={revealState}
            sceneIndex={sceneIndex}
            structure={structure}
          />
        );
      })}
    </group>
  );
}

export function CityContext({
  activeDistrict,
  focusedDistrictId,
  hoveredDistrictId,
  sceneIndex,
  structures,
}: CityContextProps) {
  return (
    <group name="City_Context">
      <UrbanAtlasGround sceneIndex={sceneIndex} structures={structures} />
      <DistrictLabels
        activeDistrict={activeDistrict}
        focusedDistrictId={focusedDistrictId}
        hoveredDistrictId={hoveredDistrictId}
        sceneIndex={sceneIndex}
        structures={structures}
      />
      <BuildingInteractionLayer sceneIndex={sceneIndex} structures={structures} />
    </group>
  );
}

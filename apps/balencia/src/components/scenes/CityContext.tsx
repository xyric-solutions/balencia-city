import * as THREE from "three";
import { BRAND_COLORS } from "../../lib/materials";
import type { StructureAsset, Vec3 } from "../../lib/types";

type CityContextProps = {
  structures: StructureAsset[];
};

function planarLength([x, , z]: Vec3) {
  return Math.hypot(x, z);
}

function normalizePlanar([x, y, z]: Vec3): Vec3 {
  const length = Math.max(planarLength([x, y, z]), 0.0001);
  return [x / length, 0, z / length];
}

function RoadToDistrict({ structure }: { structure: StructureAsset }) {
  if (structure.id === "sia-tower") {
    return null;
  }

  const direction = normalizePlanar(structure.position);
  const start: Vec3 = [direction[0] * 15, 0.035, direction[2] * 15];
  const end: Vec3 = [
    structure.position[0] - direction[0] * 5,
    0.035,
    structure.position[2] - direction[2] * 5,
  ];
  const midpoint: Vec3 = [(start[0] + end[0]) / 2, 0.055, (start[2] + end[2]) / 2];
  const length = Math.hypot(end[0] - start[0], end[2] - start[2]);
  const angle = -Math.atan2(end[2] - start[2], end[0] - start[0]);

  return (
    <group position={midpoint} rotation={[0, angle, 0]}>
      <mesh receiveShadow>
        <boxGeometry args={[length, 0.035, 2.25]} />
        <meshStandardMaterial color="#16161E" roughness={0.7} metalness={0.08} />
      </mesh>
      <mesh position={[0, 0.035, 0]}>
        <boxGeometry args={[length, 0.025, 0.18]} />
        <meshStandardMaterial
          color={BRAND_COLORS.energy}
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={0.9}
          toneMapped={false}
        />
      </mesh>
    </group>
  );
}

function CityRing({ radius, tube }: { radius: number; tube: number }) {
  return (
    <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 0.08, 0]}>
      <torusGeometry args={[radius, tube, 8, 180]} />
      <meshStandardMaterial
        color={BRAND_COLORS.energy}
        emissive={BRAND_COLORS.energy}
        emissiveIntensity={0.75}
        roughness={0.24}
        toneMapped={false}
      />
    </mesh>
  );
}

export function CityContext({ structures }: CityContextProps) {
  return (
    <group name="City_Context">
      <mesh receiveShadow position={[0, -0.04, 0]}>
        <cylinderGeometry args={[82, 82, 0.035, 160]} />
        <meshStandardMaterial color="#101018" roughness={0.88} metalness={0.02} />
      </mesh>
      <mesh receiveShadow position={[0, 0, 0]}>
        <cylinderGeometry args={[22, 22, 0.045, 128]} />
        <meshStandardMaterial color="#16161E" roughness={0.7} metalness={0.08} />
      </mesh>
      <mesh position={[0, 0.035, 0]}>
        <cylinderGeometry args={[13.5, 13.5, 0.018, 96]} />
        <meshStandardMaterial
          color="#0F0F18"
          roughness={0.12}
          metalness={0.18}
          transparent
          opacity={0.72}
        />
      </mesh>

      <CityRing radius={24} tube={0.18} />
      <CityRing radius={46} tube={0.14} />
      <CityRing radius={71} tube={0.12} />

      {structures.map((structure) => (
        <RoadToDistrict key={structure.id} structure={structure} />
      ))}
    </group>
  );
}

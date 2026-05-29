import { useFrame } from "@react-three/fiber";
import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";
import { BRAND_COLORS } from "../../lib/materials";
import type { StructureAsset, Vec3 } from "../../lib/types";

type PresenceProfile = {
  width: number;
  depth: number;
  height: number;
  rows: number;
  columns: number;
  crownScale: number;
  seed: number;
};

type StructurePresenceProps = {
  structures: StructureAsset[];
  activeDistrict: string;
  activeInteriorId?: string;
  clickedBuildingHidden?: boolean;
  clickInteriorId?: string;
  isClickInteriorActive?: boolean;
  sceneIndex: number;
};

type WindowInstance = {
  position: Vec3;
  scale: Vec3;
  rotationY: number;
};

type AnimatedGroupRef = THREE.Group | null;

const DEFAULT_PROFILE: PresenceProfile = {
  width: 8,
  depth: 8,
  height: 11,
  rows: 7,
  columns: 3,
  crownScale: 1,
  seed: 1,
};

const PRESENCE_PROFILES: Record<string, PresenceProfile> = {
  "sia-tower": { width: 6.2, depth: 5.4, height: 42.5, rows: 22, columns: 3, crownScale: 1.5, seed: 2 },
  fitness: { width: 9.4, depth: 8.4, height: 13.5, rows: 8, columns: 4, crownScale: 0.95, seed: 3 },
  yoga: { width: 12.5, depth: 9.4, height: 7.8, rows: 4, columns: 4, crownScale: 0.85, seed: 4 },
  finance: { width: 6.2, depth: 6.2, height: 16.8, rows: 10, columns: 3, crownScale: 1, seed: 5 },
  knowledgebase: { width: 8.8, depth: 7.6, height: 15.2, rows: 9, columns: 3, crownScale: 1, seed: 6 },
  chat: { width: 12.6, depth: 9.2, height: 13.2, rows: 8, columns: 4, crownScale: 0.95, seed: 7 },
  leaderboard: { width: 13.8, depth: 13.8, height: 7.4, rows: 4, columns: 5, crownScale: 1.15, seed: 8 },
  relationships: { width: 13.4, depth: 10.8, height: 6.7, rows: 4, columns: 5, crownScale: 0.9, seed: 9 },
  career: { width: 11.2, depth: 8.8, height: 19.4, rows: 12, columns: 4, crownScale: 1.15, seed: 10 },
  recovery: { width: 14.4, depth: 11.2, height: 6.4, rows: 4, columns: 5, crownScale: 0.85, seed: 11 },
  analytics: { width: 9.4, depth: 12.4, height: 17.4, rows: 11, columns: 4, crownScale: 1.15, seed: 12 },
  nutrition: { width: 13.2, depth: 11.2, height: 10.8, rows: 6, columns: 5, crownScale: 0.95, seed: 13 },
};

const VEHICLES = [
  { radius: 42, altitude: 10.6, speed: 0.13, phase: 0.2, color: "#FFB066" },
  { radius: 61, altitude: 14.4, speed: -0.105, phase: 1.8, color: "#34A853" },
  { radius: 82, altitude: 18.2, speed: 0.082, phase: 3.1, color: "#FF5E00" },
  { radius: 96, altitude: 12.6, speed: -0.075, phase: 4.6, color: "#7F24FF" },
  { radius: 54, altitude: 21.2, speed: 0.096, phase: 5.4, color: "#F59E0B" },
];

const DRONES = [
  { radius: 27, altitude: 3.6, speed: -0.18, phase: 1.2 },
  { radius: 46, altitude: 4.6, speed: 0.16, phase: 2.7 },
  { radius: 67, altitude: 5.1, speed: -0.13, phase: 3.8 },
  { radius: 86, altitude: 4.2, speed: 0.12, phase: 5.1 },
];

function seeded(index: number, salt: number) {
  return Math.sin(index * 12.9898 + salt * 78.233) * 43758.5453 % 1;
}

function normalizedPlanar(position: Vec3) {
  const length = Math.max(Math.hypot(position[0], position[2]), 0.0001);
  return new THREE.Vector3(position[0] / length, 0, position[2] / length);
}

function towardCityCenter(position: Vec3) {
  return normalizedPlanar(position).multiplyScalar(-1);
}

function buildWindows(profile: PresenceProfile) {
  const windows: WindowInstance[] = [];
  const rowGap = profile.height / (profile.rows + 1);
  const frontStep = profile.width / (profile.columns + 1);
  const sideColumns = Math.max(2, Math.floor(profile.columns * 0.72));
  const sideStep = profile.depth / (sideColumns + 1);

  for (let row = 0; row < profile.rows; row += 1) {
    const y = Math.max(0.75, rowGap * (row + 1));
    const windowHeight = THREE.MathUtils.clamp(rowGap * 0.16, 0.055, 0.16);

    for (let column = 0; column < profile.columns; column += 1) {
      if ((row + column + profile.seed) % 5 === 0) {
        continue;
      }

      const x = -profile.width / 2 + frontStep * (column + 1);
      const width = Math.min(frontStep * 0.26, 0.34);
      windows.push({
        position: [x, y, -profile.depth / 2 - 0.045],
        scale: [width, windowHeight, 0.035],
        rotationY: 0,
      });
      windows.push({
        position: [-x * 0.94, y + windowHeight * 0.22, profile.depth / 2 + 0.045],
        scale: [width * 0.86, windowHeight, 0.035],
        rotationY: Math.PI,
      });
    }

    for (let column = 0; column < sideColumns; column += 1) {
      if ((row * 2 + column + profile.seed) % 4 === 0) {
        continue;
      }

      const z = -profile.depth / 2 + sideStep * (column + 1);
      const width = Math.min(sideStep * 0.24, 0.3);
      windows.push({
        position: [-profile.width / 2 - 0.045, y + windowHeight * 0.5, z],
        scale: [width, windowHeight * 0.88, 0.035],
        rotationY: Math.PI / 2,
      });
      windows.push({
        position: [profile.width / 2 + 0.045, y, -z],
        scale: [width * 0.82, windowHeight * 0.88, 0.035],
        rotationY: -Math.PI / 2,
      });
    }
  }

  return windows;
}

function InstancedWindowGrid({
  active,
  color,
  profile,
}: {
  active: boolean;
  color: string;
  profile: PresenceProfile;
}) {
  const meshRef = useRef<THREE.InstancedMesh | null>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const windows = useMemo(() => buildWindows(profile), [profile]);

  useEffect(() => {
    const mesh = meshRef.current;

    if (!mesh) {
      return;
    }

    windows.forEach((window, index) => {
      dummy.position.fromArray(window.position);
      dummy.rotation.set(0, window.rotationY, 0);
      dummy.scale.fromArray(window.scale);
      dummy.updateMatrix();
      mesh.setMatrixAt(index, dummy.matrix);
    });

    mesh.instanceMatrix.needsUpdate = true;
  }, [dummy, windows]);

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, windows.length]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial
        color={BRAND_COLORS.interiorWarmth}
        emissive={active ? color : BRAND_COLORS.interiorWarmth}
        emissiveIntensity={active ? 0.26 : 0.1}
        opacity={active ? 0.64 : 0.42}
        transparent
        roughness={0.28}
        metalness={0}
        toneMapped={false}
      />
    </instancedMesh>
  );
}

function HumanSilhouette({ color = BRAND_COLORS.interiorWarmth }: { color?: string }) {
  return (
    <group>
      <mesh position={[0, 0.25, 0]}>
        <sphereGeometry args={[0.055, 8, 8]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.28} toneMapped={false} />
      </mesh>
      <mesh position={[0, 0.1, 0]}>
        <cylinderGeometry args={[0.035, 0.045, 0.22, 8]} />
        <meshStandardMaterial color="#4D392E" emissive={color} emissiveIntensity={0.1} toneMapped={false} />
      </mesh>
    </group>
  );
}

function StructurePresenceItem({
  active,
  hidden,
  structure,
}: {
  active: boolean;
  hidden: boolean;
  structure: StructureAsset;
}) {
  const profile = PRESENCE_PROFILES[structure.id] ?? DEFAULT_PROFILE;
  const centerDirection = towardCityCenter(structure.position);
  const entranceOffset = Math.max(profile.width, profile.depth) * 0.52;
  const entrancePosition: Vec3 = [
    centerDirection.x * entranceOffset,
    0.26,
    centerDirection.z * entranceOffset,
  ];
  const signYaw = Math.atan2(centerDirection.x, centerDirection.z);
  const signPosition: Vec3 = [
    centerDirection.x * (entranceOffset + 0.03),
    Math.max(1.15, profile.height * 0.28),
    centerDirection.z * (entranceOffset + 0.03),
  ];
  const beaconSize = 0.16 * profile.crownScale;
  const plazaPeople = useMemo(() => {
    return [0, 1, 2].map((index) => {
      const angle = index * 2.1 + profile.seed * 0.34;
      const radius = Math.max(profile.width, profile.depth) * (0.52 + index * 0.08);

      return {
        position: [
          Math.cos(angle) * radius,
          0.05,
          Math.sin(angle) * radius,
        ] satisfies Vec3,
        rotationY: -angle + Math.PI * 0.5,
      };
    });
  }, [profile]);

  if (hidden) {
    return null;
  }

  return (
    <group name={`${structure.id}_presence`} position={structure.position}>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.028, 0]}>
        <circleGeometry args={[Math.max(profile.width, profile.depth) * 0.68, 48]} />
        <meshBasicMaterial color="#000000" opacity={active ? 0.34 : 0.22} transparent depthWrite={false} />
      </mesh>

      <InstancedWindowGrid active={active} color={structure.hex} profile={profile} />

      <mesh position={entrancePosition} rotation={[0, signYaw, 0]}>
        <boxGeometry args={[Math.max(profile.width * 0.28, 1.2), 0.42, 0.045]} />
        <meshStandardMaterial
          color={BRAND_COLORS.interiorWarmth}
          emissive={active ? structure.hex : BRAND_COLORS.interiorWarmth}
          emissiveIntensity={active ? 0.85 : 0.38}
          opacity={0.82}
          transparent
          toneMapped={false}
        />
      </mesh>

      <mesh position={signPosition} rotation={[0, signYaw, 0]}>
        <planeGeometry args={[Math.max(profile.width * 0.2, 0.9), 0.24]} />
        <meshBasicMaterial color={structure.hex} opacity={active ? 0.82 : 0.42} transparent toneMapped={false} />
      </mesh>

      <mesh position={[0, profile.height + beaconSize * 1.8, 0]}>
        <sphereGeometry args={[beaconSize, 12, 12]} />
        <meshStandardMaterial
          color={structure.hex}
          emissive={structure.hex}
          emissiveIntensity={active ? 1.1 : 0.42}
          toneMapped={false}
        />
      </mesh>

      <mesh position={[0, profile.height + beaconSize * 1.82, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[beaconSize * 2.4, beaconSize * 0.12, 8, 32]} />
        <meshStandardMaterial
          color={BRAND_COLORS.energy}
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={active ? 0.72 : 0.28}
          transparent
          opacity={0.84}
          toneMapped={false}
        />
      </mesh>

      {plazaPeople.map((person, index) => (
        <group key={`${structure.id}-person-${index}`} position={person.position} rotation={[0, person.rotationY, 0]}>
          <HumanSilhouette color={index === 0 ? structure.hex : BRAND_COLORS.interiorWarmth} />
        </group>
      ))}
    </group>
  );
}

function VehicleTraffic() {
  const vehicleRefs = useRef<AnimatedGroupRef[]>([]);
  const droneRefs = useRef<AnimatedGroupRef[]>([]);

  useFrame(({ clock }) => {
    const time = clock.elapsedTime;

    VEHICLES.forEach((vehicle, index) => {
      const group = vehicleRefs.current[index];

      if (!group) {
        return;
      }

      const angle = time * vehicle.speed + vehicle.phase;
      const nextAngle = angle + Math.sign(vehicle.speed || 1) * 0.08;
      group.position.set(
        Math.cos(angle) * vehicle.radius,
        vehicle.altitude + Math.sin(time * 0.6 + vehicle.phase) * 0.45,
        Math.sin(angle) * vehicle.radius,
      );
      group.lookAt(
        Math.cos(nextAngle) * vehicle.radius,
        vehicle.altitude,
        Math.sin(nextAngle) * vehicle.radius,
      );
    });

    DRONES.forEach((drone, index) => {
      const group = droneRefs.current[index];

      if (!group) {
        return;
      }

      const angle = time * drone.speed + drone.phase;
      const pulse = 1 + Math.sin(time * 5.2 + drone.phase) * 0.12;
      group.position.set(
        Math.cos(angle) * drone.radius,
        drone.altitude + Math.sin(time * 1.1 + drone.phase) * 0.32,
        Math.sin(angle) * drone.radius,
      );
      group.scale.setScalar(pulse);
    });
  });

  return (
    <group name="Vehicle_And_Drone_Activity">
      {VEHICLES.map((vehicle, index) => (
        <group
          key={`vehicle-${index}`}
          ref={(node) => {
            vehicleRefs.current[index] = node;
          }}
        >
          <mesh>
            <boxGeometry args={[0.72, 0.12, 0.24]} />
            <meshStandardMaterial
              color="#141823"
              emissive={vehicle.color}
              emissiveIntensity={0.38}
              metalness={0.1}
              roughness={0.4}
              toneMapped={false}
            />
          </mesh>
          <mesh position={[0.34, 0.01, 0]}>
            <sphereGeometry args={[0.055, 8, 8]} />
            <meshBasicMaterial color={vehicle.color} toneMapped={false} />
          </mesh>
        </group>
      ))}

      {DRONES.map((drone, index) => (
        <group
          key={`drone-${index}`}
          ref={(node) => {
            droneRefs.current[index] = node;
          }}
        >
          <mesh>
            <octahedronGeometry args={[0.12, 0]} />
            <meshStandardMaterial
              color={BRAND_COLORS.energy}
              emissive={BRAND_COLORS.energy}
              emissiveIntensity={0.75}
              toneMapped={false}
            />
          </mesh>
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <torusGeometry args={[0.22, 0.012, 6, 18]} />
            <meshBasicMaterial color={BRAND_COLORS.energy} opacity={0.42} transparent toneMapped={false} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function PedestrianField() {
  const people = useMemo(() => {
    return Array.from({ length: 30 }, (_, index) => {
      const radius = index % 3 === 0 ? 18 : index % 3 === 1 ? 43 : 63;
      const angle = index * 1.171 + 0.35;

      return {
        angle,
        hasOrb: index % 4 === 0,
        position: [Math.cos(angle) * radius, 0.045, Math.sin(angle) * radius] satisfies Vec3,
        rotationY: -angle + Math.PI / 2,
      };
    });
  }, []);

  return (
    <group name="Pedestrian_And_AI_Orbs">
      {people.map((person, index) => (
        <group key={`pedestrian-${index}`} position={person.position} rotation={[0, person.rotationY, 0]}>
          <HumanSilhouette color={index % 5 === 0 ? BRAND_COLORS.gold : BRAND_COLORS.interiorWarmth} />
          {person.hasOrb ? (
            <mesh position={[0.22, 0.42, -0.06]}>
              <sphereGeometry args={[0.055, 10, 10]} />
              <meshStandardMaterial
                color={BRAND_COLORS.purple}
                emissive={BRAND_COLORS.purple}
                emissiveIntensity={0.82}
                toneMapped={false}
              />
            </mesh>
          ) : null}
        </group>
      ))}
    </group>
  );
}

function createParticlePositions(count: number, radiusMin: number, radiusMax: number, heightMin: number, heightMax: number, salt: number) {
  const positions = new Float32Array(count * 3);

  for (let index = 0; index < count; index += 1) {
    const radius = THREE.MathUtils.lerp(radiusMin, radiusMax, Math.abs(seeded(index, salt)));
    const angle = seeded(index, salt + 3.7) * Math.PI * 2;
    positions[index * 3] = Math.cos(angle) * radius;
    positions[index * 3 + 1] = THREE.MathUtils.lerp(heightMin, heightMax, Math.abs(seeded(index, salt + 8.1)));
    positions[index * 3 + 2] = Math.sin(angle) * radius;
  }

  return positions;
}

function AmbientParticleField({
  color,
  count,
  heightMax,
  heightMin,
  radiusMax,
  radiusMin,
  salt,
  speed,
}: {
  color: string;
  count: number;
  heightMax: number;
  heightMin: number;
  radiusMax: number;
  radiusMin: number;
  salt: number;
  speed: number;
}) {
  const groupRef = useRef<THREE.Group | null>(null);
  const positions = useMemo(
    () => createParticlePositions(count, radiusMin, radiusMax, heightMin, heightMax, salt),
    [count, heightMax, heightMin, radiusMax, radiusMin, salt],
  );

  useFrame(({ clock }) => {
    const group = groupRef.current;

    if (!group) {
      return;
    }

    group.rotation.y = clock.elapsedTime * speed;
    group.position.y = Math.sin(clock.elapsedTime * speed * 3 + salt) * 0.16;
  });

  return (
    <group ref={groupRef}>
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[positions, 3]} />
        </bufferGeometry>
        <pointsMaterial
          color={color}
          size={0.22}
          transparent
          opacity={0.72}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
          toneMapped={false}
        />
      </points>
    </group>
  );
}

function WorldActivity({ isClickInteriorActive }: { isClickInteriorActive?: boolean }) {
  const [worldVisible, setWorldVisible] = useState(true);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    if (isClickInteriorActive) {
      timeoutRef.current = setTimeout(() => setWorldVisible(false), 250);
    } else {
      setWorldVisible(true);
    }
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [isClickInteriorActive]);

  return (
    <group name="World_Activity" visible={worldVisible}>
      <VehicleTraffic />
      <PedestrianField />
      <AmbientParticleField
        color={BRAND_COLORS.energy}
        count={84}
        heightMin={1.2}
        heightMax={21}
        radiusMin={12}
        radiusMax={72}
        salt={1}
        speed={0.018}
      />
      <AmbientParticleField
        color={BRAND_COLORS.purple}
        count={32}
        heightMin={3}
        heightMax={28}
        radiusMin={4}
        radiusMax={38}
        salt={4}
        speed={-0.012}
      />
      <AmbientParticleField
        color={BRAND_COLORS.forest}
        count={44}
        heightMin={0.7}
        heightMax={9}
        radiusMin={28}
        radiusMax={68}
        salt={9}
        speed={0.01}
      />
    </group>
  );
}

export function StructurePresence({
  activeDistrict,
  activeInteriorId,
  clickedBuildingHidden,
  clickInteriorId,
  isClickInteriorActive,
  sceneIndex,
  structures,
}: StructurePresenceProps) {
  return (
    <group name="Structure_Presence_And_World_Activity">
      {structures.map((structure) => (
        <StructurePresenceItem
          key={structure.id}
          active={activeDistrict === "city" || activeDistrict === structure.id}
          hidden={
            (sceneIndex === 3 && activeInteriorId === structure.id) ||
            (!!clickedBuildingHidden && clickInteriorId === structure.id)
          }
          structure={structure}
        />
      ))}
      <WorldActivity isClickInteriorActive={isClickInteriorActive} />
    </group>
  );
}

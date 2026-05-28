import { Html } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useMemo, useRef, type CSSProperties } from "react";
import * as THREE from "three";
import { BRAND_COLORS } from "../../lib/materials";
import type { Vec3 } from "../../lib/types";

const SIA_SESSION78_MARKERS = [
  "entrance-threshold",
  "atrium-walls",
  "neural-core",
  "holographic-city-model",
  "crown-light",
] as const;

const CITY_MODEL_NODES = [
  "#34A853",
  "#6EE7B7",
  "#F59E0B",
  "#7F24FF",
  "#FF5E00",
  "#FB7185",
  "#F43F5E",
  "#3B82F6",
  "#6366F1",
  "#14B8A6",
  "#34A853",
];

type SiaInteriorRewriteLayerProps = {
  localProgress: number;
};

function easeInScene(localProgress: number, start: number, end: number) {
  const amount = THREE.MathUtils.clamp((localProgress - start) / Math.max(end - start, 0.001), 0, 1);

  return THREE.MathUtils.smoothstep(amount, 0, 1);
}

function Beam({
  color,
  end,
  opacity = 0.76,
  radius = 0.028,
  start,
}: {
  color: string;
  end: Vec3;
  opacity?: number;
  radius?: number;
  start: Vec3;
}) {
  const transform = useMemo(() => {
    const startVector = new THREE.Vector3(...start);
    const endVector = new THREE.Vector3(...end);
    const direction = endVector.clone().sub(startVector);
    const length = Math.max(direction.length(), 0.001);
    const midpoint = startVector.clone().lerp(endVector, 0.5);
    const quaternion = new THREE.Quaternion().setFromUnitVectors(
      new THREE.Vector3(0, 1, 0),
      direction.normalize(),
    );

    return { length, midpoint, quaternion };
  }, [end, start]);

  return (
    <mesh position={transform.midpoint} quaternion={transform.quaternion}>
      <cylinderGeometry args={[radius, radius, transform.length, 8]} />
      <meshBasicMaterial color={color} opacity={opacity} transparent toneMapped={false} />
    </mesh>
  );
}

function HumanSilhouette({ color = BRAND_COLORS.interiorWarmth, position }: { color?: string; position: Vec3 }) {
  return (
    <group position={position}>
      <mesh position={[0, 0.34, 0]}>
        <sphereGeometry args={[0.06, 10, 10]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.3} toneMapped={false} />
      </mesh>
      <mesh position={[0, 0.15, 0]}>
        <cylinderGeometry args={[0.04, 0.055, 0.26, 10]} />
        <meshStandardMaterial color="#33251F" emissive={color} emissiveIntensity={0.12} toneMapped={false} />
      </mesh>
    </group>
  );
}

function EntranceThreshold({ localProgress }: { localProgress: number }) {
  const glow = 0.72 + easeInScene(localProgress, 0, 0.28) * 0.52;

  return (
    <group name="SIA_Session78_Entrance_Threshold">
      <mesh position={[0, 2.8, 8.2]}>
        <torusGeometry args={[3.12, 0.075, 12, 96]} />
        <meshStandardMaterial
          color={BRAND_COLORS.energy}
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={1.35 * glow}
          opacity={0.72}
          transparent
          toneMapped={false}
        />
      </mesh>
      <mesh position={[0, 0.18, 3.25]}>
        <boxGeometry args={[2.2, 0.08, 10.8]} />
        <meshStandardMaterial
          color="#30251F"
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={0.24 * glow}
          roughness={0.46}
          toneMapped={false}
        />
      </mesh>
      {[-0.82, -0.42, 0, 0.42, 0.82].map((x) => (
        <mesh key={`entrance-vein-${x}`} position={[x, 0.24, 3.2]}>
          <boxGeometry args={[0.045, 0.035, 9.4]} />
          <meshBasicMaterial color={BRAND_COLORS.energy} opacity={0.34 + Math.abs(x) * 0.18} transparent />
        </mesh>
      ))}
      {[-3.1, 3.1].map((x) => (
        <mesh key={`entrance-pillar-${x}`} position={[x, 2.75, 8.2]}>
          <boxGeometry args={[0.38, 5.2, 0.42]} />
          <meshStandardMaterial
            color="#3B2E27"
            emissive={BRAND_COLORS.energy}
            emissiveIntensity={0.22 * glow}
            metalness={0.24}
            roughness={0.42}
            toneMapped={false}
          />
        </mesh>
      ))}
      <mesh position={[0, 5.36, 8.2]}>
        <boxGeometry args={[6.6, 0.42, 0.42]} />
        <meshStandardMaterial
          color="#3B2E27"
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={0.28 * glow}
          metalness={0.24}
          roughness={0.42}
          toneMapped={false}
        />
      </mesh>
    </group>
  );
}

function AtriumShell({ localProgress }: { localProgress: number }) {
  const glow = 0.6 + easeInScene(localProgress, 0.12, 0.58) * 0.72;
  const ribZ = useMemo(() => [5.8, 3.8, 1.8, -0.2, -2.2, -4.2], []);
  const screenRows = useMemo(() => [2.7, 4.2, 5.7, 7.2], []);

  return (
    <group name="SIA_Session78_Atrium_Walls">
      {[-4.4, 4.4].map((x) => (
        <mesh key={`atrium-wall-${x}`} position={[x, 6.9, 0.8]}>
          <boxGeometry args={[0.24, 13.2, 12.8]} />
          <meshStandardMaterial
            color="#131721"
            emissive={x < 0 ? BRAND_COLORS.energy : BRAND_COLORS.purple}
            emissiveIntensity={0.12 * glow}
            opacity={0.44}
            roughness={0.52}
            transparent
            toneMapped={false}
          />
        </mesh>
      ))}
      <mesh position={[0, 7.2, -5.6]}>
        <boxGeometry args={[8.8, 13.8, 0.24]} />
        <meshStandardMaterial
          color="#11131A"
          emissive={BRAND_COLORS.purple}
          emissiveIntensity={0.1 * glow}
          opacity={0.5}
          roughness={0.56}
          transparent
          toneMapped={false}
        />
      </mesh>
      {ribZ.map((z, index) => (
        <mesh key={`atrium-rib-${z}`} position={[0, 4.2 + index * 0.2, z]}>
          <torusGeometry args={[3.92, 0.035, 8, 96]} />
          <meshStandardMaterial
            color={index % 2 === 0 ? BRAND_COLORS.energy : BRAND_COLORS.gold}
            emissive={index % 2 === 0 ? BRAND_COLORS.energy : BRAND_COLORS.gold}
            emissiveIntensity={0.54 * glow}
            opacity={0.48}
            transparent
            toneMapped={false}
          />
        </mesh>
      ))}
      {[3.35, 5.55, 7.75].map((y, index) => (
        <group key={`atrium-platform-${y}`} position={[0, y, -2.6 + index * 0.3]}>
          <mesh rotation={[-Math.PI / 2, 0, 0]}>
            <ringGeometry args={[2.35 + index * 0.32, 2.58 + index * 0.32, 72]} />
            <meshStandardMaterial
              color="#2C2525"
              emissive={BRAND_COLORS.energy}
              emissiveIntensity={0.12 * glow}
              opacity={0.8}
              side={THREE.DoubleSide}
              transparent
              toneMapped={false}
            />
          </mesh>
          <Beam color={BRAND_COLORS.energy} opacity={0.32} radius={0.018} start={[-2.35, 0, 0]} end={[-4.2, 0.25, 0.15]} />
          <Beam color={BRAND_COLORS.energy} opacity={0.32} radius={0.018} start={[2.35, 0, 0]} end={[4.2, 0.25, 0.15]} />
        </group>
      ))}
      {[-4.55, 4.55].map((x) => (
        <group key={`wall-screens-${x}`}>
          {screenRows.map((y, index) => (
            <mesh key={`data-screen-${x}-${y}`} position={[x * 0.985, y, 0.8 - index * 1.6]} rotation={[0, x < 0 ? Math.PI / 2 : -Math.PI / 2, 0]}>
              <planeGeometry args={[1.25, 0.58]} />
              <meshBasicMaterial
                color={index % 2 === 0 ? BRAND_COLORS.energy : BRAND_COLORS.purple}
                opacity={0.34 + index * 0.05}
                transparent
                toneMapped={false}
              />
            </mesh>
          ))}
        </group>
      ))}
      <HumanSilhouette color={BRAND_COLORS.gold} position={[-2.7, 3.42, -2.5]} />
      <HumanSilhouette color={BRAND_COLORS.energy} position={[2.3, 5.62, -2.1]} />
      <HumanSilhouette color={BRAND_COLORS.interiorWarmth} position={[0.6, 7.82, -2.7]} />
    </group>
  );
}

function HolographicCityModel({ localProgress }: { localProgress: number }) {
  const groupRef = useRef<THREE.Group | null>(null);
  const nodes = useMemo(
    () =>
      CITY_MODEL_NODES.map((color, index) => {
        const angle = (index / CITY_MODEL_NODES.length) * Math.PI * 2 + 0.28;
        const radius = 1.78 + (index % 3) * 0.16;

        return {
          color,
          position: [Math.cos(angle) * radius, 0.28 + (index % 4) * 0.08, Math.sin(angle) * radius] satisfies Vec3,
        };
      }),
    [],
  );

  useFrame(({ clock }) => {
    if (!groupRef.current) {
      return;
    }

    groupRef.current.rotation.y = clock.elapsedTime * 0.1;
  });

  const opacity = 0.44 + easeInScene(localProgress, 0.18, 0.46) * 0.42;

  return (
    <group ref={groupRef} name="SIA_Session78_Holographic_City_Model" position={[0, 3.72, -2.35]}>
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.2, 2.28, 96]} />
        <meshBasicMaterial color={BRAND_COLORS.energy} opacity={opacity * 0.28} transparent toneMapped={false} />
      </mesh>
      <mesh position={[0, 0.42, 0]}>
        <cylinderGeometry args={[0.18, 0.34, 0.88, 8]} />
        <meshStandardMaterial
          color={BRAND_COLORS.energy}
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={1.2}
          opacity={opacity}
          transparent
          toneMapped={false}
        />
      </mesh>
      {nodes.map((node, index) => (
        <group key={`city-node-${index}`} position={node.position}>
          <mesh>
            <boxGeometry args={[0.18, 0.34 + (index % 4) * 0.08, 0.18]} />
            <meshStandardMaterial color={node.color} emissive={node.color} emissiveIntensity={0.86} toneMapped={false} />
          </mesh>
          <Beam color={BRAND_COLORS.gold} opacity={0.28} radius={0.012} start={[0, 0.12, 0]} end={[-node.position[0], 0.22, -node.position[2]]} />
        </group>
      ))}
    </group>
  );
}

function NeuralCore({ localProgress }: { localProgress: number }) {
  const coreRef = useRef<THREE.Group | null>(null);
  const pulse = 0.65 + easeInScene(localProgress, 0.24, 0.62) * 0.7;

  useFrame(({ clock }) => {
    if (!coreRef.current) {
      return;
    }

    coreRef.current.rotation.y = clock.elapsedTime * 0.16;
  });

  return (
    <group ref={coreRef} name="SIA_Session78_Neural_Core" position={[0, 7.8, -2.35]}>
      <mesh position={[0, 0, 0]}>
        <icosahedronGeometry args={[0.72, 2]} />
        <meshStandardMaterial
          color={BRAND_COLORS.energy}
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={1.5 * pulse}
          opacity={0.86}
          transparent
          toneMapped={false}
        />
      </mesh>
      {[0, 1, 2].map((index) => (
        <mesh key={`neural-ring-${index}`} rotation={[Math.PI / 2 + index * 0.42, index * 0.58, 0]}>
          <torusGeometry args={[1.12 + index * 0.34, 0.035, 8, 96]} />
          <meshBasicMaterial
            color={index === 1 ? BRAND_COLORS.purple : BRAND_COLORS.energy}
            opacity={0.48 + index * 0.08}
            transparent
            toneMapped={false}
          />
        </mesh>
      ))}
      <mesh position={[0, 3.65, 0]}>
        <cylinderGeometry args={[0.08, 0.16, 9.2, 24]} />
        <meshBasicMaterial color={BRAND_COLORS.energy} opacity={0.28 + pulse * 0.22} transparent toneMapped={false} />
      </mesh>
    </group>
  );
}

function CrownLightAndOrbs() {
  const orbFieldRef = useRef<THREE.Group | null>(null);
  const positions = useMemo(() => {
    const values = new Float32Array(72 * 3);

    for (let index = 0; index < 72; index += 1) {
      const angle = index * 1.618;
      const radius = 1.6 + (index % 11) * 0.22;

      values[index * 3] = Math.cos(angle) * radius;
      values[index * 3 + 1] = 3.4 + (index % 19) * 0.42;
      values[index * 3 + 2] = -2.2 + Math.sin(angle) * radius;
    }

    return values;
  }, []);

  useFrame(({ clock }) => {
    if (!orbFieldRef.current) {
      return;
    }

    orbFieldRef.current.rotation.y = clock.elapsedTime * -0.075;
    orbFieldRef.current.position.y = Math.sin(clock.elapsedTime * 0.7) * 0.12;
  });

  return (
    <group name="SIA_Session78_Crown_Light">
      <mesh position={[0, 10.2, -2.35]}>
        <cylinderGeometry args={[1.2, 0.28, 15.4, 36, 1, true]} />
        <meshBasicMaterial
          color={BRAND_COLORS.energy}
          opacity={0.16}
          side={THREE.DoubleSide}
          transparent
          depthWrite={false}
          toneMapped={false}
        />
      </mesh>
      <group ref={orbFieldRef}>
        <points>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" args={[positions, 3]} />
          </bufferGeometry>
          <pointsMaterial
            color={BRAND_COLORS.purple}
            size={0.14}
            transparent
            opacity={0.74}
            depthWrite={false}
            blending={THREE.AdditiveBlending}
            toneMapped={false}
          />
        </points>
      </group>
    </group>
  );
}

export function SiaInteriorRewriteLayer({ localProgress }: SiaInteriorRewriteLayerProps) {
  return (
    <group
      name="SIA_Session78_Interior_Rewrite"
      userData={{ session78Markers: SIA_SESSION78_MARKERS.join(",") }}
    >
      <EntranceThreshold localProgress={localProgress} />
      <AtriumShell localProgress={localProgress} />
      <HolographicCityModel localProgress={localProgress} />
      <NeuralCore localProgress={localProgress} />
      <CrownLightAndOrbs />
      <Html
        center
        className="sia-interior-cue-anchor"
        distanceFactor={9.5}
        position={[0, 8.4, -4.85]}
        transform
        zIndexRange={[5, 0]}
      >
        <div
          className="sia-interior-cue"
          data-session78-markers={SIA_SESSION78_MARKERS.join(" ")}
          data-session78-verdict="inside-sia-tower"
          style={{ "--sia-progress": localProgress.toFixed(3) } as CSSProperties}
        >
          <span>Neural Core Atrium</span>
          <strong>Inside SIA Tower</strong>
        </div>
      </Html>
    </group>
  );
}

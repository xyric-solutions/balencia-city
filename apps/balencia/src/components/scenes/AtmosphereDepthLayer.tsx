import { useFrame } from "@react-three/fiber";
import { useLayoutEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import { CITY_LAYOUT_ISLAND } from "../../lib/city-layout-v2";
import { BRAND_COLORS } from "../../lib/materials";
import { useScrollStore } from "../../store/useScrollStore";

type AtmosphereDepthLayerProps = {
  sceneIndex: number;
  clickDim?: number;
};

type DepthConfig = {
  blockOpacity: number;
  fogOpacity: number;
  glowOpacity: number;
  rimOpacity: number;
  terrainOpacity: number;
};

type SkylineBlock = {
  angle: number;
  color: string;
  depth: number;
  glowColor: string;
  glowY: number;
  height: number;
  radius: number;
  width: number;
};

const tempMatrix = new THREE.Matrix4();
const tempPosition = new THREE.Vector3();
const tempQuaternion = new THREE.Quaternion();
const tempScale = new THREE.Vector3();
const tempColor = new THREE.Color();

function seeded(index: number, salt: number) {
  return Math.abs(Math.sin(index * 12.9898 + salt * 78.233) * 43758.5453 % 1);
}

function depthConfig(sceneIndex: number): DepthConfig {
  if (sceneIndex === 17) {
    return { blockOpacity: 0.66, fogOpacity: 0.7, glowOpacity: 0.78, rimOpacity: 0.88, terrainOpacity: 0.78 };
  }

  if (sceneIndex === 15) {
    return { blockOpacity: 0.58, fogOpacity: 0.62, glowOpacity: 0.7, rimOpacity: 0.76, terrainOpacity: 0.72 };
  }

  if (sceneIndex === 1) {
    return { blockOpacity: 0.52, fogOpacity: 0.56, glowOpacity: 0.62, rimOpacity: 0.66, terrainOpacity: 0.68 };
  }

  if (sceneIndex === 16) {
    return { blockOpacity: 0.44, fogOpacity: 0.48, glowOpacity: 0.52, rimOpacity: 0.52, terrainOpacity: 0.6 };
  }

  return { blockOpacity: 0.32, fogOpacity: 0.32, glowOpacity: 0.38, rimOpacity: 0.38, terrainOpacity: 0.44 };
}

function makeSkyGeometry(sceneIndex: number) {
  const geometry = new THREE.SphereGeometry(560, 72, 32);
  const position = geometry.getAttribute("position");
  const colors: number[] = [];
  const top = new THREE.Color(sceneIndex === 17 ? "#05060B" : "#070810");
  const upper = new THREE.Color("#0A0A0F");
  const horizon = new THREE.Color(sceneIndex === 17 ? "#3D1D12" : "#2F1A13");
  const atmosphericCool = new THREE.Color(sceneIndex === 16 ? "#172839" : "#171227");
  const color = new THREE.Color();

  for (let index = 0; index < position.count; index += 1) {
    const y = position.getY(index);
    const vertical = THREE.MathUtils.clamp((y + 92) / 430, 0, 1);
    const coolBand = Math.max(0, 1 - Math.abs(vertical - 0.36) / 0.34);

    color.lerpColors(horizon, upper, THREE.MathUtils.smoothstep(vertical, 0, 1));
    color.lerp(top, THREE.MathUtils.smoothstep(vertical, 0.66, 1) * 0.38);
    color.lerp(atmosphericCool, coolBand * 0.22);
    colors.push(color.r, color.g, color.b);
  }

  geometry.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
  geometry.computeBoundingSphere();

  return geometry;
}

function SkyGradientDome({ sceneIndex }: AtmosphereDepthLayerProps) {
  const geometry = useMemo(() => makeSkyGeometry(sceneIndex), [sceneIndex]);

  return (
    <mesh geometry={geometry} name="Premium_Sky_Gradient_Dome" position={[0, 80, 0]} renderOrder={-100}>
      <meshBasicMaterial
        depthTest={false}
        depthWrite={false}
        fog={false}
        side={THREE.BackSide}
        vertexColors
      />
    </mesh>
  );
}

function TerrainDepthField({ sceneIndex }: AtmosphereDepthLayerProps) {
  const config = depthConfig(sceneIndex);

  return (
    <group name="Distant_Terrain_Depth_Field">
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.18, 0]} renderOrder={-35}>
        <ringGeometry args={[CITY_LAYOUT_ISLAND.radiusX, 208, 192]} />
        <meshStandardMaterial
          color="#070A0D"
          metalness={0.04}
          opacity={config.terrainOpacity}
          roughness={0.94}
          side={THREE.DoubleSide}
          transparent
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.22, 0]} renderOrder={-36}>
        <ringGeometry args={[208, 340, 192]} />
        <meshStandardMaterial
          color="#040506"
          metalness={0.02}
          opacity={config.terrainOpacity * 0.8}
          roughness={0.98}
          side={THREE.DoubleSide}
          transparent
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.08, 0]} renderOrder={-20}>
        <ringGeometry args={[124, 125.4, 192]} />
        <meshBasicMaterial
          blending={THREE.AdditiveBlending}
          color={BRAND_COLORS.energy}
          depthWrite={false}
          fog={false}
          opacity={config.rimOpacity * 0.28}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.02, 0]} renderOrder={-21}>
        <ringGeometry args={[152, 155, 192]} />
        <meshBasicMaterial
          blending={THREE.AdditiveBlending}
          color="#2DD4BF"
          depthWrite={false}
          fog={false}
          opacity={config.rimOpacity * 0.08}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
    </group>
  );
}

function HorizonFogShelves({ sceneIndex, clickDim = 1 }: AtmosphereDepthLayerProps) {
  const config = depthConfig(sceneIndex);
  const nearFogRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const farFogRef = useRef<THREE.MeshBasicMaterial | null>(null);

  useFrame(({ clock }) => {
    const slowBreath = 0.9 + Math.sin(clock.elapsedTime * 0.22) * 0.1;

    if (nearFogRef.current) {
      nearFogRef.current.opacity = config.fogOpacity * 0.18 * slowBreath * clickDim;
    }

    if (farFogRef.current) {
      farFogRef.current.opacity = config.fogOpacity * 0.11 * (1.04 - slowBreath * 0.08) * clickDim;
    }
  });

  return (
    <group name="Warm_Horizon_Fog_Shelves">
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.95, 0]} renderOrder={-12}>
        <ringGeometry args={[96, 190, 192]} />
        <meshBasicMaterial
          ref={nearFogRef}
          blending={THREE.AdditiveBlending}
          color="#FF8A3D"
          depthWrite={false}
          fog={false}
          opacity={config.fogOpacity * 0.18}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 2.6, 0]} renderOrder={-13}>
        <ringGeometry args={[136, 286, 192]} />
        <meshBasicMaterial
          ref={farFogRef}
          blending={THREE.AdditiveBlending}
          color="#7F24FF"
          depthWrite={false}
          fog={false}
          opacity={config.fogOpacity * 0.11}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 4.8, 0]} renderOrder={-14}>
        <ringGeometry args={[166, 360, 192]} />
        <meshBasicMaterial
          blending={THREE.AdditiveBlending}
          color="#FFB066"
          depthWrite={false}
          fog={false}
          opacity={config.fogOpacity * 0.052}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.3, 0]} renderOrder={-11}>
        <ringGeometry args={[CITY_LAYOUT_ISLAND.radiusX, CITY_LAYOUT_ISLAND.radiusX + 30, 192]} />
        <meshBasicMaterial
          blending={THREE.AdditiveBlending}
          color="#FFB066"
          depthWrite={false}
          fog={false}
          opacity={config.fogOpacity * 0.04}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
    </group>
  );
}

function makeSkylineBlocks() {
  const glowColors = [BRAND_COLORS.energy, BRAND_COLORS.gold, BRAND_COLORS.forest, BRAND_COLORS.purple, "#2DD4BF"];

  return Array.from({ length: 86 }, (_, index): SkylineBlock => {
    const angle = (index / 86) * Math.PI * 2 + seeded(index, 3.1) * 0.034;
    const radius = THREE.MathUtils.lerp(132, 184, seeded(index, 4.8));
    const heightSeed = seeded(index, 6.2);
    const height = THREE.MathUtils.lerp(1.4, 8.8, heightSeed * heightSeed);
    const width = THREE.MathUtils.lerp(1.3, 4.8, seeded(index, 8.4));
    const depth = THREE.MathUtils.lerp(1.2, 3.9, seeded(index, 9.7));

    return {
      angle,
      color: index % 5 === 0 ? "#111827" : index % 7 === 0 ? "#121221" : "#0B1017",
      depth,
      glowColor: glowColors[index % glowColors.length],
      glowY: THREE.MathUtils.lerp(0.42, 0.84, seeded(index, 11.1)),
      height,
      radius,
      width,
    };
  });
}

function DistantUrbanEdge({ sceneIndex, clickDim = 1 }: AtmosphereDepthLayerProps) {
  const blocks = useMemo(makeSkylineBlocks, []);
  const blockRef = useRef<THREE.InstancedMesh | null>(null);
  const glowRef = useRef<THREE.InstancedMesh | null>(null);
  const blockMaterialRef = useRef<THREE.MeshStandardMaterial | null>(null);
  const glowMaterialRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const config = depthConfig(sceneIndex);

  useLayoutEffect(() => {
    const blockMesh = blockRef.current;
    const glowMesh = glowRef.current;

    if (!blockMesh || !glowMesh) {
      return;
    }

    blocks.forEach((block, index) => {
      const x = Math.cos(block.angle) * block.radius;
      const z = Math.sin(block.angle) * block.radius;
      const yaw = -block.angle;
      const inwardX = -Math.cos(block.angle);
      const inwardZ = -Math.sin(block.angle);

      tempPosition.set(x, block.height / 2 - 0.12, z);
      tempQuaternion.setFromEuler(new THREE.Euler(0, yaw, 0));
      tempScale.set(block.width, block.height, block.depth);
      tempMatrix.compose(tempPosition, tempQuaternion, tempScale);
      blockMesh.setMatrixAt(index, tempMatrix);
      blockMesh.setColorAt(index, tempColor.set(block.color));

      tempPosition.set(
        x + inwardX * (block.depth * 0.54),
        Math.max(0.32, block.height * block.glowY),
        z + inwardZ * (block.depth * 0.54),
      );
      tempScale.set(block.width * 0.52, 0.055, 0.04);
      tempMatrix.compose(tempPosition, tempQuaternion, tempScale);
      glowMesh.setMatrixAt(index, tempMatrix);
      glowMesh.setColorAt(index, tempColor.set(block.glowColor));
    });

    blockMesh.instanceMatrix.needsUpdate = true;
    glowMesh.instanceMatrix.needsUpdate = true;

    if (blockMesh.instanceColor) {
      blockMesh.instanceColor.needsUpdate = true;
    }

    if (glowMesh.instanceColor) {
      glowMesh.instanceColor.needsUpdate = true;
    }
  }, [blocks]);

  useFrame(({ clock }) => {
    const pulse = 0.86 + Math.sin(clock.elapsedTime * 0.42) * 0.1;

    if (blockMaterialRef.current) {
      blockMaterialRef.current.opacity = config.blockOpacity * clickDim;
    }

    if (glowMaterialRef.current) {
      glowMaterialRef.current.opacity = config.glowOpacity * 0.62 * pulse * clickDim;
    }
  });

  return (
    <group name="Distant_Urban_Edge_Cues">
      <instancedMesh ref={blockRef} args={[undefined, undefined, blocks.length]} renderOrder={-6}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial
          ref={blockMaterialRef}
          color="#ffffff"
          metalness={0.06}
          opacity={config.blockOpacity}
          roughness={0.74}
          transparent
          vertexColors
        />
      </instancedMesh>
      <instancedMesh ref={glowRef} args={[undefined, undefined, blocks.length]} renderOrder={-5}>
        <boxGeometry args={[1, 1, 1]} />
        <meshBasicMaterial
          ref={glowMaterialRef}
          blending={THREE.AdditiveBlending}
          color="#ffffff"
          depthWrite={false}
          opacity={config.glowOpacity * 0.62}
          toneMapped={false}
          transparent
          vertexColors
        />
      </instancedMesh>
    </group>
  );
}

function OuterRimLightLayer({ sceneIndex, clickDim = 1 }: AtmosphereDepthLayerProps) {
  const config = depthConfig(sceneIndex);
  const primaryRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const secondaryRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const scanRef = useRef<THREE.Mesh | null>(null);

  useFrame(({ clock }) => {
    const cycle = (Math.sin(clock.elapsedTime * 0.58) + 1) / 2;

    if (primaryRef.current) {
      primaryRef.current.opacity = config.rimOpacity * THREE.MathUtils.lerp(0.18, 0.3, cycle) * clickDim;
    }

    if (secondaryRef.current) {
      secondaryRef.current.opacity = config.rimOpacity * THREE.MathUtils.lerp(0.09, 0.18, 1 - cycle) * clickDim;
    }

    if (scanRef.current) {
      scanRef.current.rotation.z = clock.elapsedTime * 0.018;
    }
  });

  return (
    <group name="Premium_Outer_Rim_Lighting">
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.34, 0]} renderOrder={-3}>
        <ringGeometry args={[92.4, 94.2, 192]} />
        <meshBasicMaterial
          ref={primaryRef}
          blending={THREE.AdditiveBlending}
          color={BRAND_COLORS.energy}
          depthWrite={false}
          fog={false}
          opacity={config.rimOpacity * 0.24}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.62, 0]} renderOrder={-4}>
        <ringGeometry args={[104, 108, 192]} />
        <meshBasicMaterial
          ref={secondaryRef}
          blending={THREE.AdditiveBlending}
          color={BRAND_COLORS.gold}
          depthWrite={false}
          fog={false}
          opacity={config.rimOpacity * 0.14}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh ref={scanRef} rotation={[-Math.PI / 2, 0, 0]} position={[0, 1.04, 0]} renderOrder={-2}>
        <ringGeometry args={[116, 116.55, 192, 1, 0, Math.PI * 1.54]} />
        <meshBasicMaterial
          blending={THREE.AdditiveBlending}
          color="#6EE7B7"
          depthWrite={false}
          fog={false}
          opacity={config.rimOpacity * 0.18}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
    </group>
  );
}

function ClosingCrownProjection({ sceneIndex }: AtmosphereDepthLayerProps) {
  const materialRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const ringRef = useRef<THREE.Mesh | null>(null);
  const config = depthConfig(sceneIndex);
  const baseOpacity = sceneIndex === 17 ? 0.3 : sceneIndex === 15 ? 0.18 : 0.09;

  useFrame(({ clock }) => {
    if (materialRef.current) {
      materialRef.current.opacity = baseOpacity * (0.82 + Math.sin(clock.elapsedTime * 0.34) * 0.18);
    }

    if (ringRef.current) {
      const scale = 1 + ((clock.elapsedTime * 0.032) % 0.18);
      ringRef.current.scale.setScalar(scale);
    }
  });

  return (
    <group name="Scene_17_Crown_Horizon_Cleanup">
      <mesh position={[0, 85, 0]} renderOrder={-1}>
        <cylinderGeometry args={[0.42, 1.2, 112, 24, 1, true]} />
        <meshBasicMaterial
          ref={materialRef}
          blending={THREE.AdditiveBlending}
          color={BRAND_COLORS.energy}
          depthWrite={false}
          opacity={baseOpacity}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
      <mesh ref={ringRef} rotation={[-Math.PI / 2, 0, 0]} position={[0, 7.4, 0]} renderOrder={-1}>
        <ringGeometry args={[88, 91, 192]} />
        <meshBasicMaterial
          blending={THREE.AdditiveBlending}
          color={BRAND_COLORS.energy}
          depthWrite={false}
          fog={false}
          opacity={config.rimOpacity * 0.08}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>
    </group>
  );
}

export function AtmosphereDepthLayer({ sceneIndex }: { sceneIndex: number }) {
  const isClickInteriorActive = useScrollStore((state) => state.isClickInteriorActive);
  const fogDim = isClickInteriorActive ? 0.3 : 1;
  const ringDim = isClickInteriorActive ? 0.5 : 1;

  return (
    <group name="Atmosphere_Depth_Layer">
      <SkyGradientDome sceneIndex={sceneIndex} />
      <TerrainDepthField sceneIndex={sceneIndex} />
      <HorizonFogShelves sceneIndex={sceneIndex} clickDim={fogDim} />
      <DistantUrbanEdge sceneIndex={sceneIndex} clickDim={ringDim} />
      <OuterRimLightLayer sceneIndex={sceneIndex} clickDim={ringDim} />
      <ClosingCrownProjection sceneIndex={sceneIndex} />
    </group>
  );
}

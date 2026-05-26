import { Html, Line } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useMemo, useRef, type CSSProperties } from "react";
import * as THREE from "three";
import { ACTIVE_LABEL_LAYOUT_OVERRIDES, getDistrictProfile } from "../../lib/district-metadata";
import { BRAND_COLORS } from "../../lib/materials";
import type { StructureAsset, Vec3 } from "../../lib/types";

export type DistrictLabelBoardState = "active" | "hovered" | "focused";

type DistrictLabelBoardProps = {
  revealState: DistrictLabelBoardState;
  sceneIndex: number;
  structure: StructureAsset;
};

function planarLength([x, , z]: Vec3) {
  return Math.hypot(x, z);
}

function boardDirectionFor(structure: StructureAsset) {
  const profile = getDistrictProfile(structure.id);

  if (profile.boardDirection) {
    return new THREE.Vector3(...profile.boardDirection).normalize();
  }

  const length = Math.max(planarLength(structure.position), 0.0001);
  return new THREE.Vector3(structure.position[0] / length, 0, structure.position[2] / length);
}

function boardAnchorFor(structure: StructureAsset, sceneIndex: number) {
  const profile = getDistrictProfile(structure.id);
  const override = ACTIVE_LABEL_LAYOUT_OVERRIDES[sceneIndex]?.[structure.id];
  const direction = boardDirectionFor(structure);
  const offset = override?.labelOffset ?? profile.boardOffset;
  const height = override?.labelHeight ?? profile.anchorHeight + profile.boardLift;

  return new THREE.Vector3(
    structure.position[0] + direction.x * offset,
    height,
    structure.position[2] + direction.z * offset,
  );
}

function boardYaw(direction: THREE.Vector3) {
  return Math.atan2(direction.x, direction.z);
}

export function DistrictLabelBoard({ revealState, sceneIndex, structure }: DistrictLabelBoardProps) {
  const boardRef = useRef<THREE.Group | null>(null);
  const profile = getDistrictProfile(structure.id);
  const direction = useMemo(() => boardDirectionFor(structure), [structure]);
  const boardPosition = useMemo(() => boardAnchorFor(structure, sceneIndex), [sceneIndex, structure]);
  const tetherStart = useMemo(
    () =>
      new THREE.Vector3(
        structure.position[0],
        Math.max(1.4, profile.anchorHeight * 0.58),
        structure.position[2],
      ),
    [profile.anchorHeight, structure.position],
  );
  const baseAnchor = useMemo(
    () => new THREE.Vector3(structure.position[0], 0.24, structure.position[2]),
    [structure.position],
  );
  const isFocused = revealState === "focused";
  const isHovered = revealState === "hovered";
  const pulseScale = isFocused ? 0.026 : isHovered ? 0.022 : 0.014;
  const color = profile.motifColor;
  const distanceFactor =
    ACTIVE_LABEL_LAYOUT_OVERRIDES[sceneIndex]?.[structure.id]?.distanceFactor ?? profile.boardDistanceFactor;

  useFrame(({ clock }) => {
    const board = boardRef.current;

    if (!board) {
      return;
    }

    const pulse = 1 + Math.sin(clock.elapsedTime * 3.2 + structure.position[0] * 0.07) * pulseScale;
    board.scale.set(pulse, pulse, 1);
  });

  return (
    <group name={`${structure.id}_district_label_board`} userData={{ districtId: structure.id }}>
      <Line
        points={[tetherStart, boardPosition]}
        color={color}
        lineWidth={isFocused ? 1.75 : isHovered ? 1.45 : 1.15}
        transparent
        opacity={isFocused ? 0.92 : isHovered ? 0.84 : 0.7}
      />

      <mesh position={baseAnchor.toArray()} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[0.56, 0.78, 36]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={isFocused ? 0.56 : isHovered ? 0.44 : 0.3}
          opacity={0.78}
          side={THREE.DoubleSide}
          toneMapped={false}
          transparent
        />
      </mesh>

      <mesh position={tetherStart.toArray()}>
        <sphereGeometry args={[isFocused ? 0.34 : 0.28, 14, 14]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={isFocused ? 1.05 : isHovered ? 0.84 : 0.62}
          toneMapped={false}
        />
      </mesh>

      <group ref={boardRef} position={boardPosition.toArray()} rotation={[0, boardYaw(direction), 0]}>
        <mesh castShadow>
          <boxGeometry args={[profile.boardWidth, 1.28, 0.18]} />
          <meshStandardMaterial
            color="#10131B"
            emissive={color}
            emissiveIntensity={isFocused ? 0.72 : isHovered ? 0.58 : 0.42}
            metalness={0.18}
            opacity={0.9}
            roughness={0.36}
            toneMapped={false}
            transparent
          />
        </mesh>
        <mesh position={[0, -0.77, 0.08]}>
          <boxGeometry args={[profile.boardWidth * 0.82, 0.08, 0.08]} />
          <meshStandardMaterial
            color={BRAND_COLORS.energy}
            emissive={BRAND_COLORS.energy}
            emissiveIntensity={isFocused ? 0.82 : 0.58}
            opacity={0.82}
            toneMapped={false}
            transparent
          />
        </mesh>
        <pointLight
          color={color}
          distance={isFocused ? 10 : 7}
          intensity={isFocused ? 16 : isHovered ? 11 : 7}
          position={[0, 0, 1.2]}
        />
      </group>

      <Html
        center
        className="district-board-anchor"
        distanceFactor={distanceFactor}
        occlude={false}
        position={[boardPosition.x, boardPosition.y + 0.08, boardPosition.z]}
        zIndexRange={[10, 0]}
      >
        <div
          className={[
            "district-board",
            `district-board--${revealState}`,
            `district-board--${profile.labelTier}`,
          ].join(" ")}
          data-district-id={structure.id}
          style={{ "--district-color": color } as CSSProperties}
        >
          <span>{profile.label}</span>
          <small>{profile.place}</small>
        </div>
      </Html>
    </group>
  );
}

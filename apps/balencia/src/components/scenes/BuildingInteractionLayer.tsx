import { Html } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import * as THREE from "three";
import {
  ACTIVE_LABEL_LAYOUT_OVERRIDES,
  getDistrictProfile,
  getInteractionDistrictIdsForScene,
  OVERVIEW_SCENES,
} from "../../lib/district-metadata";
import type { StructureAsset, Vec3 } from "../../lib/types";
import { useScrollStore } from "../../store/useScrollStore";

type BuildingInteractionLayerProps = {
  sceneIndex: number;
  structures: StructureAsset[];
};

function planarLength([x, , z]: Vec3) {
  return Math.hypot(x, z);
}

function targetDirectionFor(structure: StructureAsset) {
  const profile = getDistrictProfile(structure.id);

  if (profile.boardDirection) {
    return new THREE.Vector3(...profile.boardDirection).normalize();
  }

  const length = Math.max(planarLength(structure.position), 0.0001);
  return new THREE.Vector3(structure.position[0] / length, 0, structure.position[2] / length);
}

function targetPositionFor(structure: StructureAsset, sceneIndex: number) {
  const profile = getDistrictProfile(structure.id);
  const override = ACTIVE_LABEL_LAYOUT_OVERRIDES[sceneIndex]?.[structure.id];
  const direction = targetDirectionFor(structure);
  const isOverviewScene = OVERVIEW_SCENES.has(sceneIndex);
  const baseOffset = override?.labelOffset ?? profile.boardOffset;
  const offset = Math.max(
    baseOffset * (isOverviewScene ? 0.18 : 0.2),
    structure.id === "sia-tower" ? 1.8 : 2.7,
  );
  const height = isOverviewScene
    ? Math.max(2.8, profile.anchorHeight * (structure.id === "sia-tower" ? 0.62 : 0.58))
    : Math.max(2.6, (override?.labelHeight ?? profile.anchorHeight) * 0.62);

  return new THREE.Vector3(
    structure.position[0] + direction.x * offset,
    height,
    structure.position[2] + direction.z * offset,
  );
}

function targetSizeFor(structure: StructureAsset, sceneIndex: number) {
  const profile = getDistrictProfile(structure.id);
  const padMax = Math.max(profile.padSize[0], profile.padSize[1]);

  if (OVERVIEW_SCENES.has(sceneIndex)) {
    return structure.id === "sia-tower" ? 148 : Math.round(THREE.MathUtils.clamp(padMax * 4.8, 92, 122));
  }

  if (structure.id === "sia-tower") {
    return sceneIndex === 3 ? 74 : 88;
  }

  return Math.round(THREE.MathUtils.clamp(padMax * 3.2, 64, profile.labelTier === "major" ? 82 : 76));
}

function restoreHorizontalScroll() {
  window.requestAnimationFrame(() => {
    if (window.scrollX !== 0) {
      window.scrollTo(0, window.scrollY);
    }
  });
}

function InteractionPulse({
  state,
  structure,
}: {
  state: "focused" | "hovered";
  structure: StructureAsset;
}) {
  const groupRef = useRef<THREE.Group | null>(null);
  const outerMaterialRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const innerMaterialRef = useRef<THREE.MeshBasicMaterial | null>(null);
  const profile = getDistrictProfile(structure.id);
  const radius =
    structure.id === "sia-tower"
      ? 18.8
      : Math.max(profile.padSize[0], profile.padSize[1]) * (state === "focused" ? 0.82 : 0.76);
  const color = profile.motifColor;
  const focusBoost = state === "focused" ? 1.18 : 0.88;

  useFrame(({ clock }) => {
    const time = clock.elapsedTime + profile.activity.pulseOffset * 8;
    const wave = (Math.sin(time * (state === "focused" ? 3.2 : 2.55)) + 1) / 2;
    const ringScale = 1 + wave * (state === "focused" ? 0.075 : 0.052);

    if (groupRef.current) {
      groupRef.current.scale.set(ringScale, 1, ringScale);
    }

    if (outerMaterialRef.current) {
      outerMaterialRef.current.opacity = THREE.MathUtils.lerp(0.2, 0.48, wave) * focusBoost;
    }

    if (innerMaterialRef.current) {
      innerMaterialRef.current.opacity = THREE.MathUtils.lerp(0.28, 0.62, 1 - wave) * focusBoost;
    }
  });

  return (
    <group
      ref={groupRef}
      name={`${structure.id}_interaction_${state}_pulse`}
      position={[structure.position[0], 0.46, structure.position[2]]}
    >
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[radius * 0.89, radius, structure.id === "sia-tower" ? 128 : 88]} />
        <meshBasicMaterial
          ref={outerMaterialRef}
          color={color}
          depthWrite={false}
          opacity={0.34}
          side={THREE.DoubleSide}
          transparent
          blending={THREE.AdditiveBlending}
          toneMapped={false}
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, 0]}>
        <ringGeometry args={[radius * 0.48, radius * 0.52, structure.id === "sia-tower" ? 96 : 64]} />
        <meshBasicMaterial
          ref={innerMaterialRef}
          color={color}
          depthWrite={false}
          opacity={0.42}
          side={THREE.DoubleSide}
          transparent
          blending={THREE.AdditiveBlending}
          toneMapped={false}
        />
      </mesh>
    </group>
  );
}

export function BuildingInteractionLayer({ sceneIndex, structures }: BuildingInteractionLayerProps) {
  const isClickInteriorActive = useScrollStore((state) => state.isClickInteriorActive);
  const setHoveredDistrict = useScrollStore((state) => state.setHoveredDistrict);
  const clearHoveredDistrict = useScrollStore((state) => state.clearHoveredDistrict);
  const setFocusedDistrict = useScrollStore((state) => state.setFocusedDistrict);
  const clearFocusedDistrict = useScrollStore((state) => state.clearFocusedDistrict);
  const enterInterior = useScrollStore((state) => state.enterInterior);
  const focusedDistrictId = useScrollStore((state) => state.focusedDistrictId);
  const hoveredDistrictId = useScrollStore((state) => state.hoveredDistrictId);

  const [gateInteraction, setGateInteraction] = useState(false);
  const gateTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (gateTimeoutRef.current) {
      clearTimeout(gateTimeoutRef.current);
      gateTimeoutRef.current = null;
    }

    if (isClickInteriorActive) {
      setGateInteraction(true);
    } else {
      gateTimeoutRef.current = setTimeout(() => {
        setGateInteraction(false);
      }, 1200);
    }

    return () => {
      if (gateTimeoutRef.current) {
        clearTimeout(gateTimeoutRef.current);
        gateTimeoutRef.current = null;
      }
    };
  }, [isClickInteriorActive]);

  const targets = useMemo(() => {
    const allowedDistrictIds = getInteractionDistrictIdsForScene(sceneIndex);

    return structures.filter((structure) => allowedDistrictIds.includes(structure.id));
  }, [sceneIndex, structures]);
  const activePreviewDistrictId = focusedDistrictId ?? hoveredDistrictId;

  return (
    <group name="Building_Interaction_Layer">
      {!gateInteraction && targets.map((structure) => {
        const profile = getDistrictProfile(structure.id);
        const targetPosition = targetPositionFor(structure, sceneIndex);
        const isFocused = focusedDistrictId === structure.id;
        const isHovered = hoveredDistrictId === structure.id;
        const isActivePreview = activePreviewDistrictId === structure.id;
        const tooltipId = `${structure.id}-interaction-preview`;
        const isOverviewScene = OVERVIEW_SCENES.has(sceneIndex);
        const targetSize = targetSizeFor(structure, sceneIndex);

        return (
          <group key={`${structure.id}-interaction-target`}>
            {isActivePreview ? (
              <InteractionPulse state={isFocused ? "focused" : "hovered"} structure={structure} />
            ) : null}
            <Html
              center
              className="district-interaction-anchor"
              distanceFactor={isOverviewScene ? 104 : 24}
              occlude={false}
              position={targetPosition.toArray()}
              zIndexRange={[11, 0]}
            >
              <div
                className="district-interaction-hitarea"
                style={
                  {
                    "--district-color": profile.motifColor,
                    "--target-size": `${targetSize}px`,
                  } as CSSProperties
                }
              >
                <button
                  type="button"
                  className={[
                    "district-interaction-target",
                    isHovered ? "is-hovered" : undefined,
                    isFocused ? "is-focused" : undefined,
                  ]
                    .filter(Boolean)
                    .join(" ")}
                  aria-describedby={isActivePreview ? tooltipId : undefined}
                  aria-label={`Inspect ${profile.label}`}
                  aria-pressed={isFocused}
                  data-district-id={structure.id}
                  data-district-insight={profile.preview.insight}
                  data-district-label={profile.label}
                  data-district-signal={profile.preview.signal}
                  data-district-status={profile.preview.status}
                  onBlur={() => clearFocusedDistrict(structure.id)}
                  onClick={(event) => {
                    event.currentTarget.focus({ preventScroll: true });
                    restoreHorizontalScroll();
                    setFocusedDistrict(structure.id);
                    enterInterior(structure.id);
                  }}
                  onFocus={() => {
                    restoreHorizontalScroll();
                    setFocusedDistrict(structure.id);
                  }}
                  onKeyDown={(event) => {
                    if (event.key !== "Escape") {
                      return;
                    }

                    event.preventDefault();
                    clearFocusedDistrict(structure.id);
                    event.currentTarget.blur();
                  }}
                  onMouseEnter={() => setHoveredDistrict(structure.id)}
                  onMouseLeave={() => clearHoveredDistrict(structure.id)}
                  onPointerEnter={() => setHoveredDistrict(structure.id)}
                  onPointerLeave={() => clearHoveredDistrict(structure.id)}
                />
                {isActivePreview ? (
                  <div
                    id={tooltipId}
                    className={[
                      "district-hover-card",
                      isFocused ? "district-hover-card--focused" : undefined,
                    ]
                      .filter(Boolean)
                      .join(" ")}
                  >
                    <span>{profile.preview.status}</span>
                    <strong>{profile.preview.signal}</strong>
                  </div>
                ) : null}
              </div>
            </Html>
          </group>
        );
      })}
    </group>
  );
}

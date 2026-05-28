import { useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import {
  approvedEnergyAssets,
  approvedStructures,
  getEagerModelPaths,
  getEnergyModelPaths,
  getStructureById,
} from "../../lib/assets";
import type { Vec3 } from "../../lib/types";
import { useScrollStore } from "../../store/useScrollStore";
import { AtmosphereDepthLayer } from "./AtmosphereDepthLayer";
import { BuildingEnclosureLayer } from "./BuildingEnclosureLayer";
import { CityContext } from "./CityContext";
import { DistrictInteriorRevealLayer } from "./DistrictInteriorRevealLayer";
import { LivingEnergyLayer } from "./LivingEnergyLayer";
import { ApprovedEnergyAsset, ApprovedInterior, ApprovedStructure } from "./ModelAsset";
import { SiaInteriorRewriteLayer } from "./SiaInteriorRewriteLayer";
import { StructurePresence } from "./StructurePresence";

getEagerModelPaths().forEach((path) => useGLTF.preload(path, "/draco/"));
getEnergyModelPaths().forEach((path) => useGLTF.preload(path, "/draco/"));

function ClickInteriorLighting({
  position,
  hex,
  fadeRef,
}: {
  position: Vec3;
  hex: string;
  fadeRef: React.RefObject<number>;
}) {
  const mainLightRef = useRef<THREE.PointLight>(null);
  const fillLightRef = useRef<THREE.PointLight>(null);
  const ambientRef = useRef<THREE.AmbientLight>(null);
  const fogMatRef = useRef<THREE.MeshBasicMaterial>(null);

  useFrame(() => {
    const f = fadeRef.current;
    if (mainLightRef.current) mainLightRef.current.intensity = 8 * f;
    if (fillLightRef.current) fillLightRef.current.intensity = 2 * f;
    if (ambientRef.current) ambientRef.current.intensity = 0.15 * Math.min(f * 1.5, 1);
    if (fogMatRef.current) fogMatRef.current.opacity = 0.04 * f;
  });

  return (
    <group name="Click_Interior_Lighting">
      <pointLight ref={mainLightRef} color="#FFE8D6" intensity={0} distance={25} position={position} />
      <pointLight
        ref={fillLightRef}
        color="#FFFFFF"
        intensity={0}
        distance={20}
        position={[position[0], position[1] + 5, position[2]]}
      />
      <ambientLight ref={ambientRef} intensity={0} color="#FFE0C0" />
      <mesh position={position}>
        <sphereGeometry args={[12, 16, 16]} />
        <meshBasicMaterial
          ref={fogMatRef}
          color={hex}
          transparent
          opacity={0}
          blending={THREE.AdditiveBlending}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
    </group>
  );
}

export function CityScene() {
  const activeDistrict = useScrollStore((state) => state.activeDistrict);
  const activeEnergyIds = useScrollStore((state) => state.activeEnergyIds);
  const activeInteriorId = useScrollStore((state) => state.activeInteriorId);
  const clickInteriorId = useScrollStore((state) => state.clickInteriorId);
  const isClickInteriorActive = useScrollStore((state) => state.isClickInteriorActive);
  const focusedDistrictId = useScrollStore((state) => state.focusedDistrictId);
  const hoveredDistrictId = useScrollStore((state) => state.hoveredDistrictId);
  const sceneIndex = useScrollStore((state) => state.sceneIndex);
  const sceneLocalProgress = useScrollStore((state) => state.sceneLocalProgress);
  const [clickedBuildingHidden, setClickedBuildingHidden] = useState(false);
  const [lightingInterior, setLightingInterior] = useState<ReturnType<typeof getStructureById>>(undefined);
  const [holdingInterior, setHoldingInterior] = useState<ReturnType<typeof getStructureById>>(undefined);
  const clickFadeRef = useRef(0);

  const effectiveInteriorId = clickInteriorId ?? holdingInterior?.id ?? activeInteriorId;
  const activeInterior = effectiveInteriorId ? getStructureById(effectiveInteriorId) : undefined;
  const isFullCityRead = sceneIndex === 1 || sceneIndex === 15 || sceneIndex === 17;
  const isFocusedStructureScene = sceneIndex === 2 || (sceneIndex >= 4 && sceneIndex <= 14);
  const visualActiveDistrict = isFullCityRead ? "city" : activeDistrict;
  const revealDistrictId = focusedDistrictId ?? hoveredDistrictId;
  const activeHeroStructure = isFocusedStructureScene ? getStructureById(activeDistrict) : undefined;

  useEffect(() => {
    if (!activeInterior) {
      return;
    }

    useGLTF.preload(activeInterior.interior.runtimePath, "/draco/");
  }, [activeInterior]);

  useEffect(() => {
    if (!activeHeroStructure?.exteriorHero) {
      return;
    }

    useGLTF.preload(activeHeroStructure.exteriorHero.runtimePath, "/draco/");
  }, [activeHeroStructure]);

  useEffect(() => {
    if (!hoveredDistrictId) return;
    const hovered = getStructureById(hoveredDistrictId);
    if (hovered?.interior) {
      useGLTF.preload(hovered.interior.runtimePath, "/draco/");
    }
  }, [hoveredDistrictId]);

  useEffect(() => {
    if (isClickInteriorActive && activeInterior) {
      setLightingInterior(activeInterior);
      setHoldingInterior(activeInterior);
    }
  }, [isClickInteriorActive, activeInterior]);

  useFrame((_, delta) => {
    const target = isClickInteriorActive ? 1 : 0;
    clickFadeRef.current = THREE.MathUtils.lerp(clickFadeRef.current, target, 1 - Math.pow(0.012, delta));
    if (clickFadeRef.current > 0.65 && !clickedBuildingHidden) {
      setClickedBuildingHidden(true);
    } else if (clickFadeRef.current < 0.45 && clickedBuildingHidden) {
      setClickedBuildingHidden(false);
    }
    if (!isClickInteriorActive && clickFadeRef.current < 0.10 && holdingInterior) {
      setHoldingInterior(undefined);
    }
    if (!isClickInteriorActive && clickFadeRef.current < 0.02 && lightingInterior) {
      setLightingInterior(undefined);
    }
  });

  return (
    <group name="Balencia_City">
      <AtmosphereDepthLayer sceneIndex={sceneIndex} />

      <CityContext
        activeDistrict={visualActiveDistrict}
        focusedDistrictId={focusedDistrictId}
        hoveredDistrictId={hoveredDistrictId}
        sceneIndex={sceneIndex}
        structures={approvedStructures}
      />

      <BuildingEnclosureLayer
        activeDistrict={visualActiveDistrict}
        clickInteriorId={clickInteriorId}
        focusedDistrictId={focusedDistrictId}
        hoveredDistrictId={hoveredDistrictId}
        isClickInteriorActive={isClickInteriorActive}
        sceneIndex={sceneIndex}
        sceneLocalProgress={sceneLocalProgress}
        structures={approvedStructures}
      />

      <group name="Approved_Structures">
        {approvedStructures.map((structure) => (
          <ApprovedStructure
            key={structure.id}
            structure={structure}
            exteriorLod={
              isFocusedStructureScene && structure.id === activeDistrict && structure.exteriorHero ? "hero" : "overview"
            }
            active={
              visualActiveDistrict === "city" ||
              visualActiveDistrict === structure.id ||
              revealDistrictId === structure.id
            }
            visible={
              (sceneIndex !== 3 || effectiveInteriorId !== structure.id) &&
              !(clickInteriorId === structure.id && clickedBuildingHidden)
            }
          />
        ))}
      </group>

      <StructurePresence
        activeDistrict={revealDistrictId ?? visualActiveDistrict}
        activeInteriorId={effectiveInteriorId}
        clickedBuildingHidden={clickedBuildingHidden}
        clickInteriorId={clickInteriorId}
        isClickInteriorActive={isClickInteriorActive}
        sceneIndex={sceneIndex}
        structures={approvedStructures}
      />

      <group name="On_Demand_Interiors">
        {activeInterior ? (
          <ApprovedInterior
            key={activeInterior.id}
            structure={activeInterior}
            active={
              visualActiveDistrict === "city" ||
              visualActiveDistrict === activeInterior.id ||
              revealDistrictId === activeInterior.id
            }
          />
        ) : null}
      </group>

      {lightingInterior && (
        <ClickInteriorLighting
          position={lightingInterior.position}
          hex={lightingInterior.hex}
          fadeRef={clickFadeRef}
        />
      )}

      {sceneIndex === 3 && !isClickInteriorActive ? <SiaInteriorRewriteLayer localProgress={sceneLocalProgress} /> : null}
      {sceneIndex >= 4 && sceneIndex <= 14 && !isClickInteriorActive ? (
        <DistrictInteriorRevealLayer localProgress={sceneLocalProgress} sceneIndex={sceneIndex} />
      ) : null}

      <group name="Approved_Energy_Layout_V2_Rebake">
        {approvedEnergyAssets.map((asset) => (
          <ApprovedEnergyAsset
            key={asset.id}
            asset={asset}
            active={activeEnergyIds.includes(asset.id)}
            emissionScale={sceneIndex === 15 ? 1.1 : 0.82}
          />
        ))}
      </group>

      <LivingEnergyLayer isClickInteriorActive={isClickInteriorActive} structures={approvedStructures} />
    </group>
  );
}

import { useGLTF } from "@react-three/drei";
import { useEffect } from "react";
import {
  approvedEnergyAssets,
  approvedStructures,
  getEagerModelPaths,
  getEnergyModelPaths,
  getStructureById,
} from "../../lib/assets";
import { useScrollStore } from "../../store/useScrollStore";
import { AtmosphereDepthLayer } from "./AtmosphereDepthLayer";
import { CityContext } from "./CityContext";
import { LivingEnergyLayer } from "./LivingEnergyLayer";
import { ApprovedEnergyAsset, ApprovedInterior, ApprovedStructure } from "./ModelAsset";
import { StructurePresence } from "./StructurePresence";

getEagerModelPaths().forEach((path) => useGLTF.preload(path, "/draco/"));
getEnergyModelPaths().forEach((path) => useGLTF.preload(path, "/draco/"));

export function CityScene() {
  const activeDistrict = useScrollStore((state) => state.activeDistrict);
  const activeEnergyIds = useScrollStore((state) => state.activeEnergyIds);
  const activeInteriorId = useScrollStore((state) => state.activeInteriorId);
  const focusedDistrictId = useScrollStore((state) => state.focusedDistrictId);
  const hoveredDistrictId = useScrollStore((state) => state.hoveredDistrictId);
  const sceneIndex = useScrollStore((state) => state.sceneIndex);
  const activeInterior = activeInteriorId ? getStructureById(activeInteriorId) : undefined;
  const isFullCityRead = sceneIndex === 1 || sceneIndex === 15 || sceneIndex === 17;
  const visualActiveDistrict = isFullCityRead ? "city" : activeDistrict;
  const revealDistrictId = focusedDistrictId ?? hoveredDistrictId;

  useEffect(() => {
    if (!activeInterior) {
      return;
    }

    useGLTF.preload(activeInterior.interior.runtimePath, "/draco/");
  }, [activeInterior]);

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

      <group name="Approved_Structures">
        {approvedStructures.map((structure) => (
          <ApprovedStructure
            key={structure.id}
            structure={structure}
            active={
              visualActiveDistrict === "city" ||
              visualActiveDistrict === structure.id ||
              revealDistrictId === structure.id
            }
            visible={sceneIndex !== 3 || activeInteriorId !== structure.id}
          />
        ))}
      </group>

      <StructurePresence
        activeDistrict={revealDistrictId ?? visualActiveDistrict}
        activeInteriorId={activeInteriorId}
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

      <LivingEnergyLayer structures={approvedStructures} />
    </group>
  );
}

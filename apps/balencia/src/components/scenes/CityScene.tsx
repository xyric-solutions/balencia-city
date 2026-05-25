import { useGLTF } from "@react-three/drei";
import { useEffect, useMemo } from "react";
import { approvedEnergyAssets, approvedStructures, getEagerModelPaths, getStructureById } from "../../lib/assets";
import { useScrollStore } from "../../store/useScrollStore";
import { CityContext } from "./CityContext";
import { ApprovedEnergyAsset, ApprovedInterior, ApprovedStructure } from "./ModelAsset";
import { StructurePresence } from "./StructurePresence";

getEagerModelPaths().forEach((path) => useGLTF.preload(path, "/draco/"));

export function CityScene() {
  const activeDistrict = useScrollStore((state) => state.activeDistrict);
  const activeInteriorId = useScrollStore((state) => state.activeInteriorId);
  const activeEnergyIds = useScrollStore((state) => state.activeEnergyIds);
  const sceneIndex = useScrollStore((state) => state.sceneIndex);
  const activeInterior = activeInteriorId ? getStructureById(activeInteriorId) : undefined;
  const activeEnergyIdSet = useMemo(() => new Set(activeEnergyIds), [activeEnergyIds]);
  const isFullCityRead = sceneIndex === 1 || sceneIndex === 15 || sceneIndex === 17;
  const visualActiveDistrict = isFullCityRead ? "city" : activeDistrict;
  const energyEmissionScale = sceneIndex === 1 ? 0.74 : sceneIndex === 15 ? 0.68 : sceneIndex === 17 ? 0.58 : 1;

  useEffect(() => {
    if (!activeInterior) {
      return;
    }

    useGLTF.preload(activeInterior.interior.runtimePath, "/draco/");
  }, [activeInterior]);

  return (
    <group name="Balencia_City">
      <CityContext structures={approvedStructures} />

      <group name="Approved_Structures">
        {approvedStructures.map((structure) => (
          <ApprovedStructure
            key={structure.id}
            structure={structure}
            active={visualActiveDistrict === "city" || visualActiveDistrict === structure.id}
            visible={sceneIndex !== 3 || activeInteriorId !== structure.id}
          />
        ))}
      </group>

      <StructurePresence
        activeDistrict={visualActiveDistrict}
        activeInteriorId={activeInteriorId}
        sceneIndex={sceneIndex}
        structures={approvedStructures}
      />

      <group name="On_Demand_Interiors">
        {activeInterior ? (
          <ApprovedInterior
            key={activeInterior.id}
            structure={activeInterior}
            active={visualActiveDistrict === "city" || visualActiveDistrict === activeInterior.id}
          />
        ) : null}
      </group>

      <group name="Approved_Energy">
        {approvedEnergyAssets.map((asset) => (
          <ApprovedEnergyAsset
            key={asset.id}
            asset={asset}
            active={activeEnergyIdSet.has(asset.id)}
            emissionScale={energyEmissionScale}
          />
        ))}
      </group>
    </group>
  );
}

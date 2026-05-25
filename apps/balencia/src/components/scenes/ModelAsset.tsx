import { useAnimations, useGLTF } from "@react-three/drei";
import { useEffect } from "react";
import * as THREE from "three";
import { AI_PULSE_TIMING } from "../../lib/energy-system";
import { applyBalenciaMaterialOverrides, applyEnergyMaterialOverrides } from "../../lib/materials";
import type { EnergyAsset, StructureAsset } from "../../lib/types";

type GLTFResult = {
  scene: THREE.Group;
  animations: THREE.AnimationClip[];
};

type StructureProps = {
  structure: StructureAsset;
  active: boolean;
  visible?: boolean;
};

export function ApprovedStructure({ structure, active, visible = true }: StructureProps) {
  const gltf = useGLTF(structure.exterior.runtimePath, "/draco/") as GLTFResult;

  useEffect(() => {
    applyBalenciaMaterialOverrides(gltf.scene, structure.hex, active);
  }, [active, gltf.scene, structure.hex]);

  return (
    <primitive
      object={gltf.scene}
      position={structure.position}
      visible={visible}
      userData={{ assetId: structure.id, assetType: "structure-exterior" }}
    />
  );
}

export function ApprovedInterior({ structure, active }: StructureProps) {
  const gltf = useGLTF(structure.interior.runtimePath, "/draco/") as GLTFResult;

  useEffect(() => {
    applyBalenciaMaterialOverrides(gltf.scene, structure.hex, active);
  }, [active, gltf.scene, structure.hex]);

  return (
    <primitive
      object={gltf.scene}
      position={structure.position}
      userData={{ assetId: structure.id, assetType: "structure-interior" }}
    />
  );
}

type EnergyProps = {
  asset: EnergyAsset;
  active: boolean;
  emissionScale?: number;
};

function getEnergyEmissionStrength(asset: EnergyAsset, active: boolean, emissionScale: number) {
  if (asset.id === AI_PULSE_TIMING.assetId) {
    return (
      (active ? AI_PULSE_TIMING.baseEmissionStrength : AI_PULSE_TIMING.inactiveEmissionStrength) *
      emissionScale
    );
  }

  if (!active) {
    return 0.04;
  }

  const baseStrength = asset.id === "cross-district-gold" ? 0.86 : asset.id === "faint-thread" ? 0.42 : 0.92;

  return baseStrength * emissionScale;
}

export function ApprovedEnergyAsset({ asset, active, emissionScale = 1 }: EnergyProps) {
  const gltf = useGLTF(asset.runtimePath, "/draco/") as GLTFResult;
  const { actions } = useAnimations(gltf.animations ?? [], gltf.scene);

  useEffect(() => {
    applyEnergyMaterialOverrides(
      gltf.scene,
      asset.displayColor,
      active,
      getEnergyEmissionStrength(asset, active, emissionScale),
    );
  }, [active, asset, emissionScale, gltf.scene]);

  useEffect(() => {
    if (asset.id !== AI_PULSE_TIMING.assetId) {
      return undefined;
    }

    const activeActions = Object.values(actions).filter(
      (action): action is THREE.AnimationAction => Boolean(action),
    );
    activeActions.forEach((action) => {
      action.reset();
      action.loop = THREE.LoopRepeat;
      action.timeScale = 1;
      action.play();
    });

    return () => {
      activeActions.forEach((action) => action.stop());
    };
  }, [actions, asset.id]);

  return <primitive object={gltf.scene} userData={{ assetId: asset.id, assetType: "energy" }} />;
}

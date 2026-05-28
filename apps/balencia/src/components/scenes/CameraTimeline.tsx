import { useFrame } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { getStructureById } from "../../lib/assets";
import { getDistrictProfile } from "../../lib/district-metadata";
import { interpolateCamera } from "../../lib/scroll-scenes";
import type { ScrollSceneMode } from "../../lib/types";
import { useScrollStore } from "../../store/useScrollStore";

const tempPosition = new THREE.Vector3();
const tempTarget = new THREE.Vector3();
const tempFocusAnchor = new THREE.Vector3();

function parallaxStrength(scene: number, mode: ScrollSceneMode) {
  if (scene === 1 || scene === 15 || scene === 17 || mode === "climax" || mode === "closing") {
    return { position: 2.35, target: 0.72 };
  }

  if (mode === "interior") {
    return { position: 0.26, target: 0.08 };
  }

  if (mode === "product") {
    return { position: 0.58, target: 0.18 };
  }

  return { position: 0.86, target: 0.22 };
}

function focusStrength(scene: number, mode: ScrollSceneMode, isMobileViewport: boolean) {
  if (isMobileViewport) {
    return { fov: 0.45, position: 0.014, target: 0.045 };
  }

  if (scene === 1 || scene === 15 || scene === 17 || mode === "climax" || mode === "closing") {
    return { fov: 2.2, position: 0.064, target: 0.18 };
  }

  if (mode === "interior" || mode === "product") {
    return { fov: 0.62, position: 0.018, target: 0.055 };
  }

  return { fov: 1.45, position: 0.038, target: 0.115 };
}

function focusAnchorFor(districtId: string) {
  const structure = getStructureById(districtId);

  if (!structure) {
    return undefined;
  }

  const profile = getDistrictProfile(districtId);
  const height = districtId === "sia-tower" ? 33 : Math.max(2.6, profile.anchorHeight * 0.68);

  return tempFocusAnchor.set(structure.position[0], height, structure.position[2]);
}

function useIsMobileViewport() {
  const [isMobileViewport, setIsMobileViewport] = useState(
    () => typeof window !== "undefined" && window.matchMedia("(max-width: 720px)").matches,
  );

  useEffect(() => {
    const query = window.matchMedia("(max-width: 720px)");
    const update = () => setIsMobileViewport(query.matches);

    update();
    query.addEventListener("change", update);

    return () => query.removeEventListener("change", update);
  }, []);

  return isMobileViewport;
}

export function CameraTimeline() {
  const target = useRef(new THREE.Vector3(0, 20, 8));
  const focusAnchor = useRef(new THREE.Vector3(0, 20, 8));
  const focusWeight = useRef(0);
  const parallaxPosition = useRef(new THREE.Vector3());
  const parallaxTarget = useRef(new THREE.Vector3());
  const focusedDistrictId = useScrollStore((state) => state.focusedDistrictId);
  const clickInteriorCamera = useScrollStore((state) => state.clickInteriorCamera);
  const isClickInteriorActive = useScrollStore((state) => state.isClickInteriorActive);
  const progress = useScrollStore((state) => state.progress);
  const isMobileViewport = useIsMobileViewport();
  const clickPosition = useRef(new THREE.Vector3());
  const clickTarget = useRef(new THREE.Vector3());
  const clickFov = useRef(55);
  const clickWeight = useRef(0);

  useFrame(({ camera, pointer }, delta) => {
    const cameraState = interpolateCamera(progress);
    const smoothing = 1 - Math.pow(0.001, delta);
    const parallaxSmoothing = 1 - Math.pow(0.006, delta);
    const focusSmoothing = 1 - Math.pow(0.018, delta);
    const perspectiveCamera = camera as THREE.PerspectiveCamera;
    const strength = parallaxStrength(cameraState.scene.scene, cameraState.scene.mode);
    const focus = focusStrength(cameraState.scene.scene, cameraState.scene.mode, isMobileViewport);
    const nextFocusAnchor = focusedDistrictId ? focusAnchorFor(focusedDistrictId) : undefined;

    tempPosition.set(
      pointer.x * strength.position,
      pointer.y * strength.position * 0.38,
      -pointer.x * strength.position * 0.28,
    );
    tempTarget.set(pointer.x * strength.target, pointer.y * strength.target * 0.34, 0);

    parallaxPosition.current.lerp(tempPosition, parallaxSmoothing);
    parallaxTarget.current.lerp(tempTarget, parallaxSmoothing);

    tempPosition.copy(cameraState.position).add(parallaxPosition.current);
    tempTarget.copy(cameraState.target).add(parallaxTarget.current);

    if (nextFocusAnchor) {
      focusAnchor.current.copy(nextFocusAnchor);
    }

    focusWeight.current = THREE.MathUtils.lerp(
      focusWeight.current,
      nextFocusAnchor ? (isMobileViewport ? 0.32 : 1) : 0,
      focusSmoothing,
    );

    if (focusWeight.current > 0.001) {
      tempTarget.lerp(focusAnchor.current, focus.target * focusWeight.current);
      tempPosition.lerp(focusAnchor.current, focus.position * focusWeight.current);
    }

    if (isClickInteriorActive && clickInteriorCamera) {
      clickPosition.current.set(...clickInteriorCamera.position);
      clickTarget.current.set(...clickInteriorCamera.target);
      clickFov.current = clickInteriorCamera.fov;
    }

    const clickSmoothing = 1 - Math.pow(0.008, delta);
    clickWeight.current = THREE.MathUtils.lerp(
      clickWeight.current,
      isClickInteriorActive ? 1 : 0,
      clickSmoothing,
    );

    if (clickWeight.current > 0.001) {
      parallaxPosition.current.multiplyScalar(1 - clickWeight.current);
      parallaxTarget.current.multiplyScalar(1 - clickWeight.current);
      tempPosition.lerp(clickPosition.current, clickWeight.current);
      tempTarget.lerp(clickTarget.current, clickWeight.current);
    }

    perspectiveCamera.position.lerp(tempPosition, smoothing);
    target.current.lerp(tempTarget, smoothing);
    perspectiveCamera.lookAt(target.current);

    const baseFov = cameraState.fov - focus.fov * focusWeight.current;
    const targetFov = clickWeight.current > 0.001
      ? THREE.MathUtils.lerp(baseFov, clickFov.current, clickWeight.current)
      : baseFov;
    perspectiveCamera.fov = THREE.MathUtils.lerp(
      perspectiveCamera.fov,
      targetFov,
      smoothing,
    );
    perspectiveCamera.near = 0.1;
    perspectiveCamera.far = 950;
    perspectiveCamera.updateProjectionMatrix();
  });

  return null;
}

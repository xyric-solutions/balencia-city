import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";
import { interpolateCamera } from "../../lib/scroll-scenes";
import { useScrollStore } from "../../store/useScrollStore";

export function CameraTimeline() {
  const target = useRef(new THREE.Vector3(0, 20, 8));
  const progress = useScrollStore((state) => state.progress);

  useFrame(({ camera }, delta) => {
    const cameraState = interpolateCamera(progress);
    const smoothing = 1 - Math.pow(0.001, delta);
    const perspectiveCamera = camera as THREE.PerspectiveCamera;

    perspectiveCamera.position.lerp(cameraState.position, smoothing);
    target.current.lerp(cameraState.target, smoothing);
    perspectiveCamera.lookAt(target.current);

    perspectiveCamera.fov = THREE.MathUtils.lerp(perspectiveCamera.fov, cameraState.fov, smoothing);
    perspectiveCamera.near = 0.1;
    perspectiveCamera.far = 950;
    perspectiveCamera.updateProjectionMatrix();
  });

  return null;
}

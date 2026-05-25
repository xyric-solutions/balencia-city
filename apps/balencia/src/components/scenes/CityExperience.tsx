import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import * as THREE from "three";
import { BRAND_COLORS } from "../../lib/materials";
import { SCROLL_SCENES } from "../../lib/scroll-scenes";
import { BalenciaPostProcessing } from "../effects/PostProcessing";
import { CameraTimeline } from "./CameraTimeline";
import { CityScene } from "./CityScene";

function Atmosphere() {
  return (
    <>
      <color attach="background" args={[BRAND_COLORS.ink]} />
      <fogExp2 attach="fog" args={["#24150F", 0.0054]} />
      <ambientLight intensity={0.28} color="#282335" />
      <hemisphereLight args={["#FFE4CC", "#08080D", 0.32]} />
      <directionalLight position={[-8, 22, 10]} color="#FFE4CC" intensity={1.72} />
      <spotLight
        position={[18, 24, 18]}
        angle={0.55}
        penumbra={0.9}
        color={BRAND_COLORS.energy}
        intensity={620}
        distance={170}
      />
      <pointLight position={[0, 42, 0]} color={BRAND_COLORS.energy} intensity={95} distance={130} />
      <pointLight position={[-34, 18, -12]} color={BRAND_COLORS.purple} intensity={42} distance={95} />
      <pointLight position={[34, 14, -18]} color={BRAND_COLORS.forest} intensity={36} distance={85} />
    </>
  );
}

function CanvasFallback() {
  return (
    <group name="Canvas_Loading_Fallback">
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 0.2, 0]}>
        <torusGeometry args={[24, 0.12, 8, 96]} />
        <meshStandardMaterial
          color={BRAND_COLORS.energy}
          emissive={BRAND_COLORS.energy}
          emissiveIntensity={0.85}
          toneMapped={false}
        />
      </mesh>
    </group>
  );
}

export function CityExperience() {
  const openingCamera = SCROLL_SCENES[0].camera;

  return (
    <Canvas
      className="city-canvas"
      frameloop="always"
      dpr={[1, 1.75]}
      camera={{
        position: openingCamera.position,
        fov: openingCamera.fov,
        near: 0.1,
        far: 950,
      }}
      gl={{
        antialias: true,
        alpha: false,
        powerPreference: "high-performance",
        preserveDrawingBuffer: import.meta.env.DEV,
      }}
      onCreated={({ gl }) => {
        gl.setClearColor(new THREE.Color(BRAND_COLORS.ink));
        gl.toneMapping = THREE.ACESFilmicToneMapping;
        gl.outputColorSpace = THREE.SRGBColorSpace;
      }}
    >
      <Atmosphere />
      <CameraTimeline />
      <Suspense fallback={<CanvasFallback />}>
        <CityScene />
        <BalenciaPostProcessing />
      </Suspense>
    </Canvas>
  );
}

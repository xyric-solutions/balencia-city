import { Environment } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import * as THREE from "three";
import { BRAND_COLORS, getDeviceQualityTier } from "../../lib/materials";
import { SCROLL_SCENES } from "../../lib/scroll-scenes";
import { useScrollStore } from "../../store/useScrollStore";
import { BalenciaPostProcessing } from "../effects/PostProcessing";
import { CameraTimeline } from "./CameraTimeline";
import { CityScene } from "./CityScene";

function Atmosphere() {
  const sceneIndex = useScrollStore((state) => state.sceneIndex);
  const isOverview = sceneIndex === 1 || sceneIndex === 15 || sceneIndex === 17;
  const isSiaFocus = sceneIndex === 2 || sceneIndex === 3;
  const isProductReality = sceneIndex === 16;
  const isClosing = sceneIndex === 17;
  const fogDensity = isClosing ? 0.0072 : isProductReality ? 0.0064 : isOverview ? 0.0062 : isSiaFocus ? 0.0058 : 0.0051;
  const warmKeyIntensity = isOverview ? 1.92 : isSiaFocus ? 1.84 : 1.62;
  const crownIntensity = isClosing ? 142 : isOverview ? 125 : isSiaFocus ? 118 : 88;
  const fogColor = isClosing ? "#261410" : isProductReality ? "#1E2A1E" : isOverview ? "#1E1412" : "#1A1210";

  return (
    <>
      <color attach="background" args={[BRAND_COLORS.ink]} />
      <fogExp2 attach="fog" args={[fogColor, fogDensity]} />
      <ambientLight intensity={isOverview ? 0.34 : 0.31} color="#252238" />
      <hemisphereLight args={["#FFD4B0", "#08080D", isOverview ? 0.38 : 0.35]} />
      <directionalLight
        position={[-8, 22, 10]}
        color="#FFD8B0"
        intensity={warmKeyIntensity}
        castShadow
        shadow-mapSize={1024}
        shadow-camera-near={0.5}
        shadow-camera-far={80}
        shadow-camera-left={-60}
        shadow-camera-right={60}
        shadow-camera-top={60}
        shadow-camera-bottom={-60}
        shadow-bias={-0.0004}
        shadow-normalBias={0.02}
      />
      <directionalLight position={[6, 14, -8]} color="#1E2844" intensity={0.4} />
      <spotLight
        position={[18, 24, 18]}
        angle={0.55}
        penumbra={0.9}
        color={BRAND_COLORS.energy}
        intensity={isOverview ? 710 : 620}
        distance={170}
      />
      <pointLight position={[0, 42, 0]} color={BRAND_COLORS.energy} intensity={crownIntensity} distance={130} />
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

function shouldPreserveDrawingBufferForEvidence() {
  if (import.meta.env.DEV) {
    return true;
  }

  if (typeof window === "undefined") {
    return false;
  }

  return new URLSearchParams(window.location.search).has("qa-evidence");
}

export function CityExperience() {
  const openingCamera = SCROLL_SCENES[0].camera;
  const tier = getDeviceQualityTier();
  const envIntensity = tier === "high" ? 0.55 : tier === "medium" ? 0.35 : 0.18;

  return (
    <Canvas
      className="city-canvas"
      frameloop="always"
      shadows="soft"
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
        preserveDrawingBuffer: shouldPreserveDrawingBufferForEvidence(),
      }}
      onCreated={({ gl }) => {
        gl.setClearColor(new THREE.Color(BRAND_COLORS.ink));
        gl.toneMapping = THREE.ACESFilmicToneMapping;
        gl.outputColorSpace = THREE.SRGBColorSpace;
        gl.toneMappingExposure = 1.05;
      }}
    >
      <Atmosphere />
      <Environment preset="night" environmentIntensity={envIntensity} />
      <CameraTimeline />
      <Suspense fallback={<CanvasFallback />}>
        <CityScene />
        <BalenciaPostProcessing />
      </Suspense>
    </Canvas>
  );
}

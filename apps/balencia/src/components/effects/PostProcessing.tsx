import {
  Bloom,
  BrightnessContrast,
  DepthOfField,
  EffectComposer,
  HueSaturation,
  N8AO,
  Vignette,
} from "@react-three/postprocessing";
import { useScrollStore } from "../../store/useScrollStore";

export function BalenciaPostProcessing() {
  const sceneIndex = useScrollStore((state) => state.sceneIndex);
  const isClickInteriorActive = useScrollStore((state) => state.isClickInteriorActive);
  const isOverview = sceneIndex === 1 || sceneIndex === 15 || sceneIndex === 17;
  const isFocused = sceneIndex >= 4 && sceneIndex <= 14;

  const aoRadius = isOverview ? 5.0 : 3.5;
  const aoIntensity = (isOverview ? 1.5 : 2.0) * (isClickInteriorActive ? 1.2 : 1);
  const aoQuality: "low" | "medium" = isOverview ? "low" : "medium";
  const bloomIntensity = (isOverview ? 0.50 : 0.55) * (isClickInteriorActive ? 0.6 : 1);
  const bloomThreshold = (isOverview ? 0.25 : 0.24) + (isClickInteriorActive ? 0.15 : 0);

  return (
    <EffectComposer multisampling={0}>
      <N8AO
        aoRadius={aoRadius}
        distanceFalloff={0.8}
        intensity={aoIntensity}
        quality={aoQuality}
        halfRes
        color="#0A0A0F"
      />
      <Bloom
        intensity={bloomIntensity}
        luminanceThreshold={bloomThreshold}
        luminanceSmoothing={0.65}
        mipmapBlur
      />
      <DepthOfField focusDistance={0.035} focalLength={0.05} bokehScale={isFocused ? 1.5 : 0} />
      <BrightnessContrast brightness={0.02} contrast={0.15} />
      <HueSaturation hue={0} saturation={0.08} />
      <Vignette offset={0.24} darkness={isOverview ? 0.48 : 0.54} />
    </EffectComposer>
  );
}

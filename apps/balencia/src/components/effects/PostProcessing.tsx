import { Bloom, EffectComposer, Vignette } from "@react-three/postprocessing";

export function BalenciaPostProcessing() {
  return (
    <EffectComposer multisampling={0}>
      <Bloom intensity={0.72} luminanceThreshold={0.24} luminanceSmoothing={0.68} mipmapBlur />
      <Vignette offset={0.22} darkness={0.46} />
    </EffectComposer>
  );
}

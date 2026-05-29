import { useEffect, useRef, useState } from "react";
import { CityExperience } from "./components/scenes/CityExperience";
import { ProductRealityOverlay } from "./components/ui/ProductRealityOverlay";
import { SceneOverlay } from "./components/ui/SceneOverlay";
import { useBalenciaScrollTimeline } from "./hooks/useBalenciaScrollTimeline";
import { SCROLL_SCENES, SCROLL_STAGE_HEIGHT_VH } from "./lib/scroll-scenes";
import { useScrollStore } from "./store/useScrollStore";
import "./styles.css";

function ScrollStage() {
  return (
    <main
      id="balencia-scroll-stage"
      className="scroll-stage"
      style={{ height: `${SCROLL_STAGE_HEIGHT_VH}vh` }}
      aria-hidden="true"
    >
      {SCROLL_SCENES.map((scene) => (
        <span
          key={scene.slug}
          className="scroll-stage__marker"
          style={{ top: `${scene.scroll * 100}%` }}
        />
      ))}
    </main>
  );
}

export default function App() {
  useBalenciaScrollTimeline();
  const isClickInteriorActive = useScrollStore((state) => state.isClickInteriorActive);
  const [veilActive, setVeilActive] = useState(false);
  const veilTimerRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  useEffect(() => {
    clearTimeout(veilTimerRef.current);
    if (isClickInteriorActive) {
      setVeilActive(true);
    } else {
      veilTimerRef.current = setTimeout(() => setVeilActive(false), 400);
    }
    return () => clearTimeout(veilTimerRef.current);
  }, [isClickInteriorActive]);

  return (
    <div className="app-shell">
      <div className="canvas-layer">
        <CityExperience />
      </div>
      <header className={`brand-mark${isClickInteriorActive ? " brand-mark--hidden" : ""}`} aria-label="Balencia">
        Balencia.
      </header>
      <ProductRealityOverlay />
      <div className={`click-interior-veil${veilActive ? " click-interior-veil--active" : ""}`} />
      <SceneOverlay />
      <ScrollStage />
    </div>
  );
}

import { CityExperience } from "./components/scenes/CityExperience";
import { SceneOverlay } from "./components/ui/SceneOverlay";
import { useBalenciaScrollTimeline } from "./hooks/useBalenciaScrollTimeline";
import { SCROLL_SCENES, SCROLL_STAGE_HEIGHT_VH } from "./lib/scroll-scenes";
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

  return (
    <div className="app-shell">
      <div className="canvas-layer">
        <CityExperience />
      </div>
      <header className="brand-mark" aria-label="Balencia">
        Balencia.
      </header>
      <SceneOverlay />
      <ScrollStage />
    </div>
  );
}

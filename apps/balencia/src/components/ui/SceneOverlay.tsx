import { motion } from "framer-motion";
import { getScrollTargetForScene, SCROLL_SCENES } from "../../lib/scroll-scenes";
import { useScrollStore } from "../../store/useScrollStore";

function scrollToScene(scene: (typeof SCROLL_SCENES)[number]) {
  const progress = getScrollTargetForScene(scene);

  window.dispatchEvent(new CustomEvent("balencia:scroll-to-progress", { detail: { progress } }));
}

export function SceneOverlay() {
  const overlay = useScrollStore((state) => state.overlay);
  const progress = useScrollStore((state) => state.progress);
  const sceneLocalProgress = useScrollStore((state) => state.sceneLocalProgress);
  const percent = Math.round(progress * 100);

  return (
    <aside className="scene-overlay" aria-live="polite">
      <div className="scene-overlay__meta">
        <span>
          Scene {String(overlay.scene).padStart(2, "0")} / {overlay.mode}
        </span>
        <span>{percent}%</span>
      </div>
      <motion.div
        key={`${overlay.scene}-${overlay.body}`}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35, ease: "easeOut" }}
      >
        <p className="scene-overlay__focus">{overlay.focus}</p>
        <h1>{overlay.title}</h1>
        <p className="scene-overlay__body">{overlay.body}</p>
      </motion.div>
      <div className="scene-overlay__progress" aria-hidden="true">
        <span style={{ transform: `scaleX(${progress})` }} />
      </div>
      <div className="scene-overlay__local" aria-hidden="true">
        <span style={{ transform: `scaleX(${sceneLocalProgress})` }} />
      </div>
      <nav className="scene-overlay__nav" aria-label="Scroll scenes">
        {SCROLL_SCENES.map((scene) => (
          <button
            key={scene.slug}
            type="button"
            className={scene.scene === overlay.scene ? "is-active" : undefined}
            aria-label={`Jump to scene ${scene.scene}: ${scene.focus}`}
            title={scene.focus}
            onClick={() => scrollToScene(scene)}
          />
        ))}
      </nav>
    </aside>
  );
}

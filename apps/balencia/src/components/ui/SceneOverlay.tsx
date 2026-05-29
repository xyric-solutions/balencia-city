import { motion } from "framer-motion";
import { type CSSProperties, useEffect, useRef, useState } from "react";
import { getDistrictProfile, type DistrictProfile } from "../../lib/district-metadata";
import { getScrollTargetForScene, SCROLL_SCENES } from "../../lib/scroll-scenes";
import { useScrollStore } from "../../store/useScrollStore";

function scrollToScene(scene: (typeof SCROLL_SCENES)[number]) {
  const progress = getScrollTargetForScene(scene);

  window.dispatchEvent(new CustomEvent("balencia:scroll-to-progress", { detail: { progress } }));
}

function DistrictPreviewPanel({
  interactionMode,
  profile,
}: {
  interactionMode: "Focused" | "Hovered";
  profile: DistrictProfile;
}) {
  return (
    <div className="district-preview">
      <p className="district-preview__status">{interactionMode} / {profile.preview.status}</p>
      <h1>{profile.label}</h1>
      <p className="district-preview__place">{profile.place}</p>
      <div className="district-preview__content">
        <p>
          <span>Insight</span>
          {profile.preview.insight}
        </p>
        <p>
          <span>Signal</span>
          {profile.preview.signal}
        </p>
      </div>
    </div>
  );
}

export function SceneOverlay() {
  const overlay = useScrollStore((state) => state.overlay);
  const clickInteriorId = useScrollStore((state) => state.clickInteriorId);
  const isClickInteriorActive = useScrollStore((state) => state.isClickInteriorActive);
  const focusedDistrictId = useScrollStore((state) => state.focusedDistrictId);
  const hoveredDistrictId = useScrollStore((state) => state.hoveredDistrictId);
  const progress = useScrollStore((state) => state.progress);
  const sceneLocalProgress = useScrollStore((state) => state.sceneLocalProgress);
  const percent = Math.round(progress * 100);
  const exitInterior = useScrollStore((state) => state.exitInterior);

  const [holdClickInteriorId, setHoldClickInteriorId] = useState<string | undefined>(undefined);
  const holdTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (holdTimeoutRef.current) {
      clearTimeout(holdTimeoutRef.current);
      holdTimeoutRef.current = null;
    }

    if (isClickInteriorActive && clickInteriorId) {
      setHoldClickInteriorId(clickInteriorId);
    } else if (!isClickInteriorActive) {
      holdTimeoutRef.current = setTimeout(() => {
        setHoldClickInteriorId(undefined);
      }, 1500);
    }

    return () => {
      if (holdTimeoutRef.current) {
        clearTimeout(holdTimeoutRef.current);
        holdTimeoutRef.current = null;
      }
    };
  }, [isClickInteriorActive, clickInteriorId]);

  const clickInteriorProfile = holdClickInteriorId ? getDistrictProfile(holdClickInteriorId) : undefined;
  const previewDistrictId = clickInteriorProfile ? undefined : (focusedDistrictId ?? hoveredDistrictId);

  useEffect(() => {
    if (!isClickInteriorActive) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        exitInterior();
        setHoldClickInteriorId(undefined);
        if (holdTimeoutRef.current) {
          clearTimeout(holdTimeoutRef.current);
          holdTimeoutRef.current = null;
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [isClickInteriorActive, exitInterior]);
  const previewProfile = previewDistrictId ? getDistrictProfile(previewDistrictId) : undefined;
  const interactionMode = focusedDistrictId ? "Focused" : "Hovered";

  return (
    <aside
      className={[
        "scene-overlay",
        `scene-overlay--${overlay.mode}`,
        clickInteriorProfile || previewProfile ? "scene-overlay--district" : undefined,
      ]
        .filter(Boolean)
        .join(" ")}
      aria-live="polite"
      style={
        clickInteriorProfile
          ? ({ "--district-color": clickInteriorProfile.motifColor } as CSSProperties)
          : previewProfile
            ? ({ "--district-color": previewProfile.motifColor } as CSSProperties)
            : undefined
      }
    >
      <div className="scene-overlay__meta">
        <span>
          {clickInteriorProfile
            ? `Inside / ${clickInteriorProfile.preview.status}`
            : previewProfile
              ? "District preview"
              : `Scene ${String(overlay.scene).padStart(2, "0")} / ${overlay.mode}`}
        </span>
        <span>{percent}%</span>
      </div>
      <motion.div
        key={
          clickInteriorProfile
            ? `click-interior-${holdClickInteriorId}`
            : previewProfile
              ? `${previewDistrictId}-${interactionMode}`
              : `${overlay.scene}-${overlay.body}`
        }
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35, ease: "easeOut" }}
      >
        {clickInteriorProfile ? (
          <>
            <DistrictPreviewPanel interactionMode="Focused" profile={clickInteriorProfile} />
            <button
              type="button"
              className="scene-overlay__back-btn"
              onClick={() => {
                exitInterior();
                setHoldClickInteriorId(undefined);
                if (holdTimeoutRef.current) {
                  clearTimeout(holdTimeoutRef.current);
                  holdTimeoutRef.current = null;
                }
              }}
            >
              &larr; Back to city
            </button>
          </>
        ) : previewProfile ? (
          <DistrictPreviewPanel interactionMode={interactionMode} profile={previewProfile} />
        ) : (
          <>
            <p className="scene-overlay__focus">{overlay.focus}</p>
            <h1>{overlay.title}</h1>
            <p className="scene-overlay__body">{overlay.body}</p>
          </>
        )}
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

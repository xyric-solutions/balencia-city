import { motion } from "framer-motion";
import type { CSSProperties } from "react";
import { useScrollStore } from "../../store/useScrollStore";

const actionCards = [
  { label: "Move", value: "Train at 6:20", tone: "green" },
  { label: "Focus", value: "Protect 90 min", tone: "orange" },
  { label: "Recover", value: "Wind down at 10", tone: "purple" },
  { label: "Connect", value: "Reply to Maya", tone: "gold" },
] as const;

const signalPath = ["Recovery", "Career", "Nutrition"] as const;

export function ProductRealityOverlay() {
  const sceneIndex = useScrollStore((state) => state.sceneIndex);
  const sceneLocalProgress = useScrollStore((state) => state.sceneLocalProgress);

  if (sceneIndex !== 16) {
    return null;
  }

  const exitProgress = Math.max(0, Math.min(1, (sceneLocalProgress - 0.72) / 0.24));
  const stageStyle = {
    "--product-exit": exitProgress.toFixed(3),
    "--product-progress": sceneLocalProgress.toFixed(3),
  } as CSSProperties;
  const activeSignal = Math.min(signalPath.length - 1, Math.floor(sceneLocalProgress * signalPath.length));

  return (
    <motion.section
      className="product-reality"
      aria-label="Balencia Today Screen"
      data-product-reality="true"
      data-session82-product-exit={exitProgress > 0 ? "resolving-to-closing" : "today-screen"}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 - exitProgress * 0.86 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.42, ease: "easeOut" }}
      style={stageStyle}
    >
      <motion.div
        className="product-reality__stage"
        initial={{ opacity: 0, x: 30, scale: 0.96 }}
        animate={{ opacity: 1, x: -exitProgress * 18, scale: 1 - exitProgress * 0.035 }}
        transition={{ duration: 0.62, ease: [0.19, 1, 0.22, 1] }}
      >
        <div className="product-reality__depth" aria-hidden="true" />
        <div className="product-reality__person" aria-hidden="true">
          <span className="product-reality__head" />
          <span className="product-reality__neck" />
          <span className="product-reality__torso" />
          <span className="product-reality__shoulder" />
          <span className="product-reality__arm product-reality__arm--left" />
          <span className="product-reality__arm product-reality__arm--right" />
          <span className="product-reality__hand product-reality__hand--left" />
          <span className="product-reality__hand product-reality__hand--right" />
        </div>

        <article className="today-phone">
          <div className="today-phone__hardware">
            <div className="today-phone__screen">
              <div className="today-phone__status" aria-hidden="true">
                <span>7:42</span>
                <span className="today-phone__sensor" />
                <span>82%</span>
              </div>

              <header className="today-phone__header">
                <p>Today</p>
                <h2>Good morning.</h2>
                <span>SIA found 3 connected signals for today.</span>
              </header>

              <section className="today-insight" aria-label="SIA daily insight">
                <div>
                  <p>High leverage insight</p>
                  <h3>Sleep debt plus meeting load</h3>
                </div>
                <strong>Move deep work before 2 PM.</strong>
              </section>

              <section className="today-path" aria-label="Intelligence path">
                <div className="today-path__header">
                  <span>Intelligence path</span>
                  <span>Live</span>
                </div>
                <div className="today-path__nodes">
                  {signalPath.map((signal, index) => (
                    <span
                      key={signal}
                      className={index <= activeSignal ? "is-active" : undefined}
                    >
                      {signal}
                    </span>
                  ))}
                </div>
              </section>

              <section className="today-actions" aria-label="Recommended actions">
                {actionCards.map((card) => (
                  <div key={card.label} className={`today-action today-action--${card.tone}`}>
                    <span>{card.label}</span>
                    <strong>{card.value}</strong>
                  </div>
                ))}
              </section>

              <footer className="today-phone__nav" aria-hidden="true">
                <span className="is-active">Today</span>
                <span>City</span>
                <span>SIA</span>
              </footer>
            </div>
          </div>
        </article>
      </motion.div>
    </motion.section>
  );
}

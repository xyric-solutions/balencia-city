import Lenis from "lenis";
import { useEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SCROLL_SCENES, SCROLL_TIMELINE_SECONDS } from "../lib/scroll-scenes";
import { useScrollStore } from "../store/useScrollStore";

gsap.registerPlugin(ScrollTrigger);

export function useBalenciaScrollTimeline() {
  useEffect(() => {
    const setScrollProgress = useScrollStore.getState().setScrollProgress;
    const timelineState = { progress: 0 };
    const lenis = new Lenis({
      lerp: 0.08,
      smoothWheel: true,
      wheelMultiplier: 0.82,
    });

    const updateLenis = (time: number) => {
      lenis.raf(time * 1000);
    };

    gsap.ticker.add(updateLenis);
    gsap.ticker.lagSmoothing(0);
    lenis.on("scroll", () => ScrollTrigger.update());

    const timeline = gsap.timeline({
      paused: true,
      defaults: { ease: "none" },
    });

    SCROLL_SCENES.forEach((scene) => {
      timeline.addLabel(scene.slug, scene.scroll * SCROLL_TIMELINE_SECONDS);
    });

    SCROLL_SCENES.forEach((scene, index) => {
      const next = SCROLL_SCENES[index + 1];

      if (!next) {
        return;
      }

      timeline.to(
        timelineState,
        {
          progress: next.scroll,
          duration: Math.max((next.scroll - scene.scroll) * SCROLL_TIMELINE_SECONDS, 0.001),
          onUpdate: () => setScrollProgress(timelineState.progress),
        },
        scene.scroll * SCROLL_TIMELINE_SECONDS,
      );
    });

    const trigger = ScrollTrigger.create({
      trigger: "#balencia-scroll-stage",
      start: "top top",
      end: "bottom bottom",
      scrub: true,
      onUpdate: (self) => {
        timeline.progress(self.progress);
      },
    });

    const handleTimelineJump = (event: Event) => {
      const progress = (event as CustomEvent<{ progress?: number }>).detail?.progress;

      if (typeof progress !== "number") {
        return;
      }

      const clampedProgress = gsap.utils.clamp(0, 1, progress);
      const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
      timeline.progress(clampedProgress);
      setScrollProgress(clampedProgress);
      lenis.scrollTo(clampedProgress * maxScroll, {
        duration: 1.05,
        easing: (time: number) => 1 - Math.pow(1 - time, 3),
      });
    };

    window.addEventListener("balencia:scroll-to-progress", handleTimelineJump);

    const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    const initialProgress = window.scrollY / maxScroll;
    timeline.progress(initialProgress);
    setScrollProgress(timelineState.progress);
    ScrollTrigger.refresh();

    return () => {
      window.removeEventListener("balencia:scroll-to-progress", handleTimelineJump);
      trigger.kill();
      timeline.kill();
      gsap.ticker.remove(updateLenis);
      lenis.destroy();
    };
  }, []);
}

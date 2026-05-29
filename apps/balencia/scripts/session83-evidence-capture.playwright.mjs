import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const targetUrl = process.env.BALENCIA_QA_URL ?? "http://localhost:3005/?qa-evidence=1";
const outputDir = path.resolve(repoRoot, "output/playwright/session83-evidence");
const reportPath = path.resolve(repoRoot, "output/playwright/session83-evidence-report.json");

const scenes = [
  { scene: 1, slug: "arrival", scroll: 0, focus: "City aerial" },
  { scene: 2, slug: "sia-tower-reveal", scroll: 0.07, focus: "SIA Tower" },
  { scene: 3, slug: "sia-neural-core", scroll: 0.13, focus: "Inside SIA Tower", thresholdAt: 0.28, interiorCameraAt: 0.56, exitAt: 0.76 },
  { scene: 4, slug: "fitness-district", scroll: 0.2, focus: "Fitness district", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 5, slug: "yoga-sanctuary", scroll: 0.27, focus: "Yoga and wellbeing", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 6, slug: "finance-tower", scroll: 0.34, focus: "Finance district", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 7, slug: "knowledgebase", scroll: 0.41, focus: "Knowledgebase district", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 8, slug: "communication-hub", scroll: 0.48, focus: "Chat and communication", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 9, slug: "leaderboard-arena", scroll: 0.55, focus: "Leaderboard and competition", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 10, slug: "relationships-garden", scroll: 0.62, focus: "Relationships district", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 11, slug: "career-towers", scroll: 0.69, focus: "Career district", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 12, slug: "recovery-dreamscape", scroll: 0.76, focus: "Recovery and sleep", thresholdAt: 0.56, interiorCameraAt: 0.72 },
  { scene: 13, slug: "analytics-cathedral", scroll: 0.83, focus: "AI analytics", thresholdAt: 0.56, interiorCameraAt: 0.72, exitAt: 0.84 },
  { scene: 14, slug: "nutrition-farm", scroll: 0.88, focus: "Nutrition district", thresholdAt: 0.54, interiorCameraAt: 0.68, exitAt: 0.84 },
  { scene: 15, slug: "cross-pillar-revelation", scroll: 0.93, focus: "Cross-pillar revelation", exitAt: 0.78 },
  { scene: 16, slug: "today-screen-street", scroll: 0.96, focus: "Today screen street corridor", exitAt: 0.68 },
  { scene: 17, slug: "sia-tower-return", scroll: 1, focus: "SIA tower return" },
];

function sceneSpan(scene) {
  const index = scenes.findIndex((candidate) => candidate.scene === scene.scene);
  const nextScene = scenes[index + 1];

  return Math.max((nextScene?.scroll ?? 1) - scene.scroll, 0.0001);
}

function clampProgress(progress) {
  return Math.min(Math.max(progress, 0), 1);
}

function progressAt(scene, localProgress) {
  if (scene.scene === 17) {
    return 1;
  }

  return clampProgress(scene.scroll + sceneSpan(scene) * localProgress);
}

function safeName(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function importPackageFromDir(packageDir) {
  const packageJsonPath = path.join(packageDir, "package.json");
  const packageJson = JSON.parse(await fs.readFile(packageJsonPath, "utf8"));
  const entry = packageJson.module ?? packageJson.main ?? "index.js";
  const entryPath = path.join(packageDir, entry);

  const module = await import(pathToFileURL(entryPath).href);

  return module.chromium ? module : module.default;
}

async function findCachedPlaywrightPackage() {
  const candidates = [
    path.join(appDir, "node_modules/playwright"),
    path.join(appDir, "node_modules/playwright-core"),
    path.join(repoRoot, "node_modules/playwright"),
    path.join(repoRoot, "node_modules/playwright-core"),
  ];
  const npxRoot = path.join(os.homedir(), ".npm/_npx");

  if (await pathExists(npxRoot)) {
    const cacheDirs = await fs.readdir(npxRoot, { withFileTypes: true });

    for (const cacheDir of cacheDirs) {
      if (!cacheDir.isDirectory()) {
        continue;
      }

      candidates.push(path.join(npxRoot, cacheDir.name, "node_modules/playwright"));
      candidates.push(path.join(npxRoot, cacheDir.name, "node_modules/playwright-core"));
    }
  }

  for (const packageDir of candidates) {
    if (await pathExists(path.join(packageDir, "package.json"))) {
      return packageDir;
    }
  }

  throw new Error("Could not locate playwright or playwright-core. Run the Playwright CLI once, then re-run Session 83 capture.");
}

async function importPlaywright() {
  try {
    const module = await import("playwright");

    return module.chromium ? module : module.default;
  } catch {
    try {
      const module = await import("playwright-core");

      return module.chromium ? module : module.default;
    } catch {
      return importPackageFromDir(await findCachedPlaywrightPackage());
    }
  }
}

async function findChromiumExecutable() {
  const candidates = [
    process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
  ].filter(Boolean);

  for (const executablePath of candidates) {
    if (await pathExists(executablePath)) {
      return executablePath;
    }
  }

  return undefined;
}

const desktopPoints = [
  ...scenes.map((scene) => ({
    scene: scene.scene,
    slug: scene.slug,
    focus: scene.focus,
    beat: "scene-start",
    localProgress: scene.scene === 1 || scene.scene === 17 ? 0 : 0.02,
    progress: scene.scene === 1 || scene.scene === 17 ? scene.scroll : progressAt(scene, 0.02),
  })),
  ...scenes
    .filter((scene) => typeof scene.thresholdAt === "number")
    .map((scene) => ({
      scene: scene.scene,
      slug: scene.slug,
      focus: scene.focus,
      beat: "threshold",
      localProgress: scene.thresholdAt,
      progress: progressAt(scene, scene.thresholdAt),
    })),
  ...scenes
    .filter((scene) => typeof scene.interiorCameraAt === "number")
    .map((scene) => ({
      scene: scene.scene,
      slug: scene.slug,
      focus: scene.focus,
      beat: "interior-midpoint",
      localProgress: scene.interiorCameraAt,
      progress: progressAt(scene, scene.interiorCameraAt),
    })),
  ...scenes
    .filter((scene) => typeof scene.exitAt === "number")
    .map((scene) => ({
      scene: scene.scene,
      slug: scene.slug,
      focus: scene.focus,
      beat: "exit-bridge",
      localProgress: scene.exitAt,
      progress: progressAt(scene, scene.exitAt),
    })),
];

const mobileSceneIds = new Set([1, 3, 4, 14, 16, 17]);
const mobilePoints = desktopPoints.filter(
  (point) =>
    mobileSceneIds.has(point.scene) &&
    (point.beat === "scene-start" ||
      point.beat === "interior-midpoint" ||
      (point.scene === 16 && point.beat === "exit-bridge")),
);

async function preparePage(page, viewport) {
  await page.setViewportSize(viewport);
  await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: 20000 });
  await page.waitForSelector("canvas", { timeout: 30000 });
  await page.waitForFunction(() => {
    const canvas = document.querySelector("canvas");
    const rect = canvas?.getBoundingClientRect();

    return Boolean(rect && rect.width > 200 && rect.height > 200);
  }, null, { timeout: 30000 });
  await page.waitForTimeout(2600);
}

async function jumpToProgress(page, progress, expectedScene) {
  await page.evaluate((targetProgress) => {
    window.dispatchEvent(
      new CustomEvent("balencia:scroll-to-progress", {
        detail: { progress: targetProgress },
      }),
    );
  }, progress);

  await page.waitForTimeout(1350);
  await page
    .waitForFunction(
      (scene) => {
        const navButtons = [...document.querySelectorAll(".scene-overlay__nav button")];
        const activeIndex = navButtons.findIndex((button) => button.classList.contains("is-active"));

        return activeIndex + 1 === scene;
      },
      expectedScene,
      { timeout: 3500 },
    )
    .catch(() => undefined);
  await page.waitForTimeout(180);
}

async function captureCanvasAndDom(page) {
  return page.evaluate(() => {
    function text(value) {
      return value?.textContent?.replace(/\s+/g, " ").trim() ?? "";
    }

    function rectFor(element) {
      const rect = element.getBoundingClientRect();

      return {
        x: Number(rect.x.toFixed(2)),
        y: Number(rect.y.toFixed(2)),
        width: Number(rect.width.toFixed(2)),
        height: Number(rect.height.toFixed(2)),
        right: Number(rect.right.toFixed(2)),
        bottom: Number(rect.bottom.toFixed(2)),
      };
    }

    function isVisibleElement(element) {
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();

      return (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        Number(style.opacity) > 0.01 &&
        rect.width > 1 &&
        rect.height > 1
      );
    }

    function collectTextHealth() {
      const candidates = [
        ...document.querySelectorAll(
          ".scene-overlay *, .district-preview *, [data-product-reality] *, [data-session80-verdict] *, [data-session81-verdict] *",
        ),
      ].filter((element) => {
        const isTextLeaf = element.children.length === 0 || ["H1", "P", "SPAN", "BUTTON"].includes(element.tagName);

        return isTextLeaf && isVisibleElement(element) && text(element).length > 0;
      });

      const textOverflow = candidates
        .filter((element) => element.scrollWidth > element.clientWidth + 8 || element.scrollHeight > element.clientHeight + 8)
        .slice(0, 12)
        .map((element) => ({
          selector: element.className || element.tagName.toLowerCase(),
          text: text(element).slice(0, 90),
          rect: rectFor(element),
          scrollWidth: element.scrollWidth,
          clientWidth: element.clientWidth,
          scrollHeight: element.scrollHeight,
          clientHeight: element.clientHeight,
        }));

      const overlaps = [];

      for (let index = 0; index < candidates.length; index += 1) {
        const first = candidates[index];
        const firstRect = first.getBoundingClientRect();

          for (let nextIndex = index + 1; nextIndex < candidates.length; nextIndex += 1) {
            const second = candidates[nextIndex];
            const firstRoot = first.closest(".scene-overlay, [data-product-reality], [data-session80-verdict], [data-session81-verdict]");
            const secondRoot = second.closest(".scene-overlay, [data-product-reality], [data-session80-verdict], [data-session81-verdict]");

            if (first.contains(second) || second.contains(first) || firstRoot === secondRoot) {
              continue;
            }

          const secondRect = second.getBoundingClientRect();
          const xOverlap = Math.max(0, Math.min(firstRect.right, secondRect.right) - Math.max(firstRect.left, secondRect.left));
          const yOverlap = Math.max(0, Math.min(firstRect.bottom, secondRect.bottom) - Math.max(firstRect.top, secondRect.top));

          if (xOverlap * yOverlap > 24) {
            overlaps.push({
              first: text(first).slice(0, 70),
              second: text(second).slice(0, 70),
              area: Number((xOverlap * yOverlap).toFixed(2)),
              firstRect: rectFor(first),
              secondRect: rectFor(second),
            });
          }

          if (overlaps.length >= 12) {
            break;
          }
        }

        if (overlaps.length >= 12) {
          break;
        }
      }

      return { textOverflow, overlaps };
    }

    const canvas = document.querySelector("canvas");

    if (!canvas) {
      return {
        canvas: { present: false },
        dom: {},
        textHealth: collectTextHealth(),
      };
    }

    const canvasRect = canvas.getBoundingClientRect();
    const sampleWidth = 96;
    const sampleHeight = Math.max(1, Math.round(sampleWidth * (canvasRect.height / Math.max(canvasRect.width, 1))));
    const sampler = document.createElement("canvas");
    sampler.width = sampleWidth;
    sampler.height = sampleHeight;

    const context = sampler.getContext("2d", { willReadFrequently: true });

    if (!context) {
      return {
        canvas: {
          present: true,
          rect: rectFor(canvas),
          captureError: "Could not create 2D sampling context",
        },
        dom: {},
        textHealth: collectTextHealth(),
      };
    }

    context.drawImage(canvas, 0, 0, sampleWidth, sampleHeight);

    const pixels = context.getImageData(0, 0, sampleWidth, sampleHeight).data;
    const buckets = new Set();
    let litPixels = 0;
    let minLuma = 255;
    let maxLuma = 0;
    let totalLuma = 0;

    for (let index = 0; index < pixels.length; index += 4) {
      const red = pixels[index];
      const green = pixels[index + 1];
      const blue = pixels[index + 2];
      const luma = red * 0.2126 + green * 0.7152 + blue * 0.0722;

      if (luma > 8) {
        litPixels += 1;
      }

      minLuma = Math.min(minLuma, luma);
      maxLuma = Math.max(maxLuma, luma);
      totalLuma += luma;
      buckets.add(`${red >> 4}-${green >> 4}-${blue >> 4}`);
    }

    let dataUrl = "";
    let captureError = null;

    try {
      dataUrl = canvas.toDataURL("image/png");
    } catch (error) {
      captureError = error instanceof Error ? error.message : String(error);
    }

    const overlay = document.querySelector(".scene-overlay");
    const activeNavIndex = [...document.querySelectorAll(".scene-overlay__nav button")].findIndex((button) =>
      button.classList.contains("is-active"),
    );
    const productOverlay = document.querySelector("[data-product-reality]");
    const revealCue = document.querySelector("[data-session80-verdict], [data-session81-verdict]");
    const targets = [...document.querySelectorAll("[data-district-id][data-district-label]")].map((target) => ({
      districtId: target.getAttribute("data-district-id"),
      label: target.getAttribute("data-district-label"),
      rect: rectFor(target),
    }));

    return {
      canvas: {
        present: true,
        rect: rectFor(canvas),
        methods: {
          getContext: typeof canvas.getContext,
          toDataURL: typeof canvas.toDataURL,
        },
        dataUrl,
        dataUrlLength: dataUrl.length,
        captureError,
        pixelStats: {
          sampleWidth,
          sampleHeight,
          uniqueColorBuckets: buckets.size,
          litPixelRatio: Number((litPixels / (sampleWidth * sampleHeight)).toFixed(4)),
          minLuma: Number(minLuma.toFixed(2)),
          maxLuma: Number(maxLuma.toFixed(2)),
          meanLuma: Number((totalLuma / (sampleWidth * sampleHeight)).toFixed(2)),
        },
      },
      dom: {
        activeScene: activeNavIndex + 1,
        overlayMeta: text(overlay?.querySelector(".scene-overlay__meta")),
        overlayFocus: text(overlay?.querySelector(".scene-overlay__focus")),
        overlayTitle: text(overlay?.querySelector("h1")),
        overlayBody: text(overlay?.querySelector(".scene-overlay__body")),
        productRealityState: productOverlay?.getAttribute("data-session82-product-exit") ?? null,
        revealDistrictId: revealCue?.getAttribute("data-district-id") ?? null,
        revealVerdict: revealCue?.getAttribute("data-session80-verdict") ?? revealCue?.getAttribute("data-session81-verdict") ?? null,
        targetCount: targets.length,
        targets,
      },
      textHealth: collectTextHealth(),
    };
  });
}

async function capturePoint(page, suiteName, point, index) {
  await jumpToProgress(page, point.progress, point.scene);

  const evidence = await captureCanvasAndDom(page);
  const sequence = String(index + 1).padStart(2, "0");
  const fileName = `${sequence}-s${String(point.scene).padStart(2, "0")}-${safeName(point.slug)}-${point.beat}.png`;
  const outputPath = path.join(outputDir, suiteName, fileName);

  await fs.mkdir(path.dirname(outputPath), { recursive: true });

  const dataUrlPrefix = "data:image/png;base64,";
  const canSaveCanvas =
    evidence.canvas.present &&
    evidence.canvas.dataUrl?.startsWith(dataUrlPrefix) &&
    evidence.canvas.dataUrlLength > 12000 &&
    !evidence.canvas.captureError;

  if (canSaveCanvas) {
    const imageBuffer = Buffer.from(evidence.canvas.dataUrl.slice(dataUrlPrefix.length), "base64");
    await fs.writeFile(outputPath, imageBuffer);
  }

  const pixelStats = evidence.canvas.pixelStats ?? {};
  const nonblank =
    canSaveCanvas &&
    pixelStats.uniqueColorBuckets >= 16 &&
    pixelStats.litPixelRatio >= 0.02 &&
    pixelStats.maxLuma - pixelStats.minLuma >= 8;

  return {
    ...point,
    progress: Number(point.progress.toFixed(4)),
    localProgress: Number(point.localProgress.toFixed(3)),
    suite: suiteName,
    imagePath: canSaveCanvas ? outputPath : null,
    dom: evidence.dom,
    canvas: {
      present: evidence.canvas.present,
      rect: evidence.canvas.rect,
      methods: evidence.canvas.methods,
      dataUrlLength: evidence.canvas.dataUrlLength ?? 0,
      captureError: evidence.canvas.captureError ?? null,
      pixelStats,
      nonblank,
    },
    textHealth: evidence.textHealth,
  };
}

async function captureSuite(page, suiteName, viewport, points) {
  await preparePage(page, viewport);

  const viewportShot = path.join(outputDir, suiteName, "viewport-smoke.png");
  const viewportScreenshot = { path: viewportShot, ok: false, error: null };

  try {
    await fs.mkdir(path.dirname(viewportShot), { recursive: true });
    await page.screenshot({ path: viewportShot, fullPage: false, timeout: 8000 });
    viewportScreenshot.ok = true;
  } catch (error) {
    viewportScreenshot.error = error instanceof Error ? error.message : String(error);
  }

  const captures = [];

  for (const [index, point] of points.entries()) {
    captures.push(await capturePoint(page, suiteName, point, index));
  }

  return {
    suite: suiteName,
    viewport,
    viewportScreenshot,
    captureCount: captures.length,
    captures,
  };
}

async function main() {
  const { chromium } = await importPlaywright();
  const executablePath = await findChromiumExecutable();
  const consoleMessages = [];
  const pageErrors = [];
  const startedAt = new Date().toISOString();
  const browser = await chromium.launch({
    headless: true,
    executablePath,
    args: ["--enable-unsafe-swiftshader", "--disable-dev-shm-usage", "--no-sandbox"],
  });

  try {
    await fs.rm(outputDir, { force: true, recursive: true });
    await fs.mkdir(outputDir, { recursive: true });

    const page = await browser.newPage();
    page.on("console", (message) => {
      const type = message.type();

      if (type === "warning" || type === "error") {
        consoleMessages.push({
          type,
          text: message.text(),
          location: message.location(),
        });
      }
    });
    page.on("pageerror", (error) => {
      pageErrors.push({
        message: error.message,
        stack: error.stack,
      });
    });

    const suites = [
      await captureSuite(page, "desktop", { width: 1280, height: 720 }, desktopPoints),
      await captureSuite(page, "mobile", { width: 390, height: 844 }, mobilePoints),
    ];

    const captures = suites.flatMap((suite) => suite.captures);
    const failedCanvasCaptures = captures.filter((capture) => !capture.canvas.nonblank);
    const textOverflow = captures.flatMap((capture) =>
      capture.textHealth.textOverflow.map((issue) => ({
        suite: capture.suite,
        scene: capture.scene,
        beat: capture.beat,
        ...issue,
      })),
    );
    const textOverlaps = captures.flatMap((capture) =>
      capture.textHealth.overlaps.map((issue) => ({
        suite: capture.suite,
        scene: capture.scene,
        beat: capture.beat,
        ...issue,
      })),
    );
    const blockingConsoleMessages = consoleMessages.filter((message) => message.type === "warning" || message.type === "error");

    const report = {
      session: 83,
      url: targetUrl,
      startedAt,
      completedAt: new Date().toISOString(),
      runtime: {
        playwrightSource: "node",
        executablePath: executablePath ?? "playwright-default",
      },
      summary: {
        suiteCount: suites.length,
        captureCount: captures.length,
        imageCount: captures.filter((capture) => capture.imagePath).length,
        failedCanvasCaptures: failedCanvasCaptures.length,
        textOverflow: textOverflow.length,
        textOverlaps: textOverlaps.length,
        consoleWarningsOrErrors: blockingConsoleMessages.length,
        pageErrors: pageErrors.length,
        viewportScreenshotFailures: suites.filter((suite) => !suite.viewportScreenshot.ok).length,
        passed:
          failedCanvasCaptures.length === 0 &&
          textOverflow.length === 0 &&
          textOverlaps.length === 0 &&
          blockingConsoleMessages.length === 0 &&
          pageErrors.length === 0,
      },
      suites,
      failures: {
        failedCanvasCaptures,
        textOverflow,
        textOverlaps,
        consoleMessages: blockingConsoleMessages,
        pageErrors,
      },
    };

    await fs.mkdir(path.dirname(reportPath), { recursive: true });
    await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

    if (!report.summary.passed) {
      throw new Error(`Session 83 evidence capture failed: ${JSON.stringify(report.summary)}`);
    }

    console.log(`Session 83 evidence capture passed -> ${reportPath}`);
    console.log(JSON.stringify(report.summary, null, 2));
  } finally {
    await browser.close();
  }
}

await main();

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const packagePath = path.join(appDir, "package.json");
const cityExperiencePath = path.join(appDir, "src/components/scenes/CityExperience.tsx");
const captureScriptPath = path.join(appDir, "scripts/session83-evidence-capture.playwright.mjs");
const reportPath = path.join(repoRoot, "output/playwright/session83-evidence-harness-static-qa.json");

function fail(message) {
  throw new Error(message);
}

function requireIncludes(source, marker, label) {
  if (!source.includes(marker)) {
    fail(`${label} is missing marker: ${marker}`);
  }
}

function requireRegex(source, regex, label) {
  if (!regex.test(source)) {
    fail(`${label} is missing required pattern: ${regex}`);
  }
}

const [packageSource, cityExperienceSource, captureSource] = await Promise.all([
  fs.readFile(packagePath, "utf8"),
  fs.readFile(cityExperiencePath, "utf8"),
  fs.readFile(captureScriptPath, "utf8"),
]);

const packageJson = JSON.parse(packageSource);

if (packageJson.scripts?.["qa:session83"] !== "node scripts/session83-evidence-harness-qa.mjs") {
  fail("package.json must expose npm run qa:session83");
}

requireIncludes(cityExperienceSource, "shouldPreserveDrawingBufferForEvidence", "CityExperience");
requireIncludes(cityExperienceSource, "qa-evidence", "CityExperience");
requireIncludes(cityExperienceSource, "preserveDrawingBuffer: shouldPreserveDrawingBufferForEvidence()", "CityExperience");

for (let scene = 1; scene <= 17; scene += 1) {
  requireRegex(captureSource, new RegExp(`scene:\\s*${scene}\\b`), `capture script scene ${scene}`);
}

for (const marker of [
  "canvas.toDataURL(\"image/png\")",
  "balencia:scroll-to-progress",
  "session83-evidence-report.json",
  "desktopPoints",
  "mobilePoints",
  "scene-start",
  "threshold",
  "interior-midpoint",
  "exit-bridge",
  "consoleMessages",
  "pageerror",
  "collectTextHealth",
  "textOverflow",
  "overlaps",
  "litPixelRatio",
  "uniqueColorBuckets",
  "nonblank",
  "viewport-smoke.png",
]) {
  requireIncludes(captureSource, marker, "capture script");
}

const thresholdSceneCount = (captureSource.match(/thresholdAt:/g) ?? []).length;
const interiorSceneCount = (captureSource.match(/interiorCameraAt:/g) ?? []).length;
const exitSceneCount = (captureSource.match(/exitAt:/g) ?? []).length;

if (thresholdSceneCount < 12) {
  fail(`capture script must include threshold evidence scenes; found ${thresholdSceneCount}`);
}

if (interiorSceneCount < 12) {
  fail(`capture script must include interior midpoint evidence scenes; found ${interiorSceneCount}`);
}

if (exitSceneCount < 5) {
  fail(`capture script must include Session 82 exit bridge evidence; found ${exitSceneCount}`);
}

const report = {
  session: 83,
  status: "passed",
  checks: {
    packageScript: true,
    preserveDrawingBufferEvidenceQuery: true,
    sceneStarts: 17,
    thresholdSceneCount,
    interiorSceneCount,
    exitSceneCount,
    canvasCapture: true,
    consoleCapture: true,
    textHealthCapture: true,
    desktopAndMobileSuites: true,
  },
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

console.log(`Session 83 evidence harness static QA passed -> ${reportPath}`);

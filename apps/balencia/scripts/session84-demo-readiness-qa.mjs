import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const stylesPath = path.join(appDir, "src/styles.css");
const browserReportPath = path.join(repoRoot, "output/playwright/session84-demo-readiness-browser-qa.json");
const reportPath = path.join(repoRoot, "output/playwright/session84-demo-readiness-static-qa.json");

function fail(message) {
  throw new Error(message);
}

function requireNumber(value, label) {
  if (!Number.isFinite(value)) {
    fail(`${label} must be a finite number`);
  }

  return value;
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

const styles = await fs.readFile(stylesPath, "utf8");

if (/fonts\.googleapis|@import\s+url\(\s*["']?https?:/i.test(styles)) {
  fail("Final demo CSS must not fetch external fonts or remote CSS");
}

const browserReport = await readJson(browserReportPath);
const summary = browserReport.summary ?? {};

if (summary.passed !== true) {
  fail("Session 84 browser readiness report is not passing");
}

if (requireNumber(summary.overallScore, "overallScore") < 8) {
  fail("Final demo readiness score must be at least 8.0 / 10");
}

if (summary.consoleWarningsOrErrors !== 0 || summary.pageErrors !== 0) {
  fail("Final demo readiness requires 0 runtime warnings/errors and 0 page errors");
}

if (summary.p0Blockers !== 0) {
  fail("Final demo readiness requires 0 known P0 blockers");
}

if (summary.desktopSceneFailures !== 0 || summary.mobileSpotFailures !== 0) {
  fail("Desktop and mobile runtime sweeps must have 0 failures");
}

if (summary.overviewInteractionCoverage !== "12 / 12") {
  fail("Overview interaction coverage must remain 12 / 12");
}

const staticReport = {
  session: 84,
  checkedAt: new Date().toISOString(),
  summary: {
    passed: true,
    noRemoteFontCss: true,
    browserReport: path.relative(repoRoot, browserReportPath),
    overallScore: summary.overallScore,
    overviewInteractionCoverage: summary.overviewInteractionCoverage,
    consoleWarningsOrErrors: summary.consoleWarningsOrErrors,
    p0Blockers: summary.p0Blockers,
  },
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(staticReport, null, 2)}\n`);

console.log(`Session 84 demo readiness QA passed -> ${reportPath}`);

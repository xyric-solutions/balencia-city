import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const manifestPath = path.join(appDir, "src/lib/asset-manifest.json");
const phase10QaPath = path.join(repoRoot, "output/playwright/phase10-lod-static-qa.json");
const reportPath = path.join(repoRoot, "output/playwright/session89-runtime-smoke.json");
const appUrl = process.env.BALENCIA_APP_URL ?? "http://localhost:3005/";

function fail(message) {
  throw new Error(message);
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function checkUrl(url) {
  const response = await fetch(url, { cache: "no-store" });
  const arrayBuffer = await response.arrayBuffer();
  return {
    url,
    status: response.status,
    ok: response.ok,
    contentLength: Number(response.headers.get("content-length")) || arrayBuffer.byteLength,
  };
}

const manifest = await readJson(manifestPath);
const phase10Qa = await readJson(phase10QaPath);

if (phase10Qa.status !== "passed" || phase10Qa.checks?.heroExteriorCount !== 12) {
  fail("Phase 10 LOD static QA must pass with 12 hero exteriors before runtime smoke");
}

const appRoute = await checkUrl(appUrl);
const baseUrl = appUrl.endsWith("/") ? appUrl.slice(0, -1) : appUrl;

const heroAssets = [];
const overviewAssets = [];

for (const structure of manifest.structures ?? []) {
  if (!structure.exteriorHero?.runtimePath) {
    fail(`${structure.id} is missing exteriorHero.runtimePath`);
  }

  heroAssets.push({
    id: structure.id,
    ...(await checkUrl(`${baseUrl}${structure.exteriorHero.runtimePath}`)),
  });
  overviewAssets.push({
    id: structure.id,
    ...(await checkUrl(`${baseUrl}${structure.exterior.runtimePath}`)),
  });
}

const checks = {
  appRouteHttp200: appRoute.ok,
  phase10LodStaticQaPassed: true,
  allTwelveHeroGlbsHttp200: heroAssets.length === 12 && heroAssets.every((asset) => asset.ok),
  allTwelveOverviewGlbsHttp200: overviewAssets.length === 12 && overviewAssets.every((asset) => asset.ok),
  allHeroContentNonzero: heroAssets.every((asset) => asset.contentLength > 0),
  allOverviewContentNonzero: overviewAssets.every((asset) => asset.contentLength > 0),
};

const report = {
  session: 89,
  date: new Date().toISOString(),
  status: Object.values(checks).every(Boolean) ? "passed" : "failed",
  method: "local HTTP reachability against the running Vite app plus Phase 10 LOD static QA",
  appUrl,
  checks,
  appRoute,
  heroAssets,
  overviewAssets,
  notes: [
    "This smoke verifies runtime asset reachability, not a full visual browser screenshot sweep.",
    "Final visual evidence is recorded by the Blender Session 89 app-hero and overview contact sheets.",
  ],
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

if (report.status !== "passed") {
  fail(`Session 89 runtime smoke failed -> ${reportPath}`);
}

console.log(`Session 89 runtime smoke passed -> ${reportPath}`);

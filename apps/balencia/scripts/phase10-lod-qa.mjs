import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");

const packagePath = path.join(appDir, "package.json");
const manifestPath = path.join(appDir, "src/lib/asset-manifest.json");
const typesPath = path.join(appDir, "src/lib/types.ts");
const assetsPath = path.join(appDir, "src/lib/assets.ts");
const syncAssetsPath = path.join(appDir, "scripts/sync-assets.mjs");
const modelAssetPath = path.join(appDir, "src/components/scenes/ModelAsset.tsx");
const cityScenePath = path.join(appDir, "src/components/scenes/CityScene.tsx");
const backlogPath = path.join(appDir, "PHASE-10-BACKLOG.md");
const reportPath = path.join(repoRoot, "output/playwright/phase10-lod-static-qa.json");

function fail(message) {
  throw new Error(message);
}

function requireIncludes(source, marker, label) {
  if (!source.includes(marker)) {
    fail(`${label} is missing marker: ${marker}`);
  }
}

function requireNumberArray(value, expected, label) {
  if (!Array.isArray(value) || value.length !== expected.length) {
    fail(`${label} must be [${expected.join(", ")}]`);
  }

  for (let index = 0; index < expected.length; index += 1) {
    if (value[index] !== expected[index]) {
      fail(`${label} must be [${expected.join(", ")}]`);
    }
  }
}

const [
  packageSource,
  manifestSource,
  typesSource,
  assetsSource,
  syncAssetsSource,
  modelAssetSource,
  citySceneSource,
  backlogSource,
] = await Promise.all([
  fs.readFile(packagePath, "utf8"),
  fs.readFile(manifestPath, "utf8"),
  fs.readFile(typesPath, "utf8"),
  fs.readFile(assetsPath, "utf8"),
  fs.readFile(syncAssetsPath, "utf8"),
  fs.readFile(modelAssetPath, "utf8"),
  fs.readFile(cityScenePath, "utf8"),
  fs.readFile(backlogPath, "utf8"),
]);

const packageJson = JSON.parse(packageSource);
const manifest = JSON.parse(manifestSource);

if (packageJson.scripts?.["qa:phase10-lod"] !== "node scripts/phase10-lod-qa.mjs") {
  fail("package.json must expose npm run qa:phase10-lod");
}

if (manifest.sourceOfTruth?.phase10Backlog !== "apps/balencia/PHASE-10-BACKLOG.md") {
  fail("asset manifest must reference the Phase 10 backlog");
}

requireNumberArray(manifest.lodPolicy?.overviewScenes, [1, 15, 17], "lodPolicy.overviewScenes");
requireNumberArray(
  manifest.lodPolicy?.focusedHeroScenes,
  [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
  "lodPolicy.focusedHeroScenes",
);

if (manifest.lodPolicy?.exteriorHeroField !== "exteriorHero") {
  fail("lodPolicy.exteriorHeroField must be exteriorHero");
}

let heroExteriorCount = 0;
for (const structure of manifest.structures ?? []) {
  if (!structure.exteriorHero) {
    continue;
  }

  heroExteriorCount += 1;
  for (const key of ["name", "sourcePath", "publicPath", "runtimePath"]) {
    if (typeof structure.exteriorHero[key] !== "string" || structure.exteriorHero[key].length === 0) {
      fail(`${structure.id}.exteriorHero.${key} must be a non-empty string`);
    }
  }
}

requireIncludes(typesSource, "exteriorHero?: ModelReference", "types.ts");
requireIncludes(typesSource, "lodPolicy?:", "types.ts");
requireIncludes(typesSource, 'exteriorHeroField: "exteriorHero"', "types.ts");

requireIncludes(assetsSource, "getExteriorModelReference", "assets.ts");
requireIncludes(assetsSource, "structure.exteriorHero ?? structure.exterior", "assets.ts");
requireIncludes(assetsSource, "getHeroExteriorModelPaths", "assets.ts");
requireIncludes(assetsSource, "structure.exterior.runtimePath", "assets.ts eager preload");

requireIncludes(syncAssetsSource, "structure.exteriorHero", "sync-assets.mjs");
requireIncludes(syncAssetsSource, "structure.exteriorHero.sourcePath", "sync-assets.mjs");

requireIncludes(modelAssetSource, "exteriorLod?: \"overview\" | \"hero\"", "ModelAsset");
requireIncludes(modelAssetSource, "getExteriorModelReference(structure, exteriorLod === \"hero\")", "ModelAsset");
requireIncludes(modelAssetSource, "structure-exterior-hero", "ModelAsset");

requireIncludes(citySceneSource, "isFullCityRead = sceneIndex === 1 || sceneIndex === 15 || sceneIndex === 17", "CityScene");
requireIncludes(citySceneSource, "isFocusedStructureScene = sceneIndex === 2 || (sceneIndex >= 4 && sceneIndex <= 14)", "CityScene");
requireIncludes(citySceneSource, "activeHeroStructure?.exteriorHero", "CityScene");
requireIncludes(citySceneSource, "useGLTF.preload(activeHeroStructure.exteriorHero.runtimePath", "CityScene");
requireIncludes(citySceneSource, "structure.id === activeDistrict && structure.exteriorHero ? \"hero\" : \"overview\"", "CityScene");

for (const marker of [
  "Runtime LOD Policy",
  "Scenes 1, 15, and 17",
  "`exteriorHero`",
  "Overview active city should stay at or below 250K drawn tris",
  "focused hero scenes may reach 270K drawn tris",
]) {
  requireIncludes(backlogSource, marker, "PHASE-10-BACKLOG.md");
}

const report = {
  phase: 10,
  status: "passed",
  checks: {
    packageScript: true,
    manifestPolicy: true,
    optionalHeroExteriorType: true,
    syncCopiesHeroExteriorWhenPresent: true,
    overviewEagerPreloadPreserved: true,
    focusedHeroPreloadOnDemand: true,
    focusedSceneHeroSelection: true,
    heroExteriorCount,
  },
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

console.log(`Phase 10 LOD static QA passed -> ${reportPath}`);

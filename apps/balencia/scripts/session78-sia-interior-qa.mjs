import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import ts from "typescript";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const scrollScenesPath = path.join(appDir, "src/lib/scroll-scenes.ts");
const cityScenePath = path.join(appDir, "src/components/scenes/CityScene.tsx");
const siaLayerPath = path.join(appDir, "src/components/scenes/SiaInteriorRewriteLayer.tsx");
const reportPath = path.join(repoRoot, "output/playwright/session78-sia-interior-static-qa.json");

const requiredMarkers = [
  "entrance-threshold",
  "atrium-walls",
  "neural-core",
  "holographic-city-model",
  "crown-light",
];

function fail(message) {
  throw new Error(message);
}

async function readSource(filePath, scriptKind = ts.ScriptKind.TS) {
  const sourceText = await fs.readFile(filePath, "utf8");

  return ts.createSourceFile(filePath, sourceText, ts.ScriptTarget.Latest, true, scriptKind);
}

function propertyNameText(name) {
  if (ts.isIdentifier(name) || ts.isStringLiteral(name) || ts.isNumericLiteral(name)) {
    return name.text;
  }

  return undefined;
}

function findVariableInitializer(sourceFile, variableName) {
  let initializer;

  function visit(node) {
    if (ts.isVariableDeclaration(node) && ts.isIdentifier(node.name) && node.name.text === variableName) {
      initializer = node.initializer;
    }

    ts.forEachChild(node, visit);
  }

  visit(sourceFile);

  return initializer;
}

function requireObjectLiteral(node, label) {
  if (!node || !ts.isObjectLiteralExpression(node)) {
    fail(`${label} must be an object literal`);
  }

  return node;
}

function requireArrayLiteral(node, label) {
  if (!node || !ts.isArrayLiteralExpression(node)) {
    fail(`${label} must be an array literal`);
  }

  return node;
}

function getProperty(objectLiteral, key) {
  return objectLiteral.properties.find(
    (property) => ts.isPropertyAssignment(property) && propertyNameText(property.name) === key,
  );
}

function getString(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing string property ${key}`);
  }

  const value = property.initializer;

  if (!ts.isStringLiteral(value) && !ts.isNoSubstitutionTemplateLiteral(value)) {
    fail(`${key} must be a string literal`);
  }

  return value.text;
}

function numericValue(node, label) {
  if (ts.isNumericLiteral(node)) {
    return Number(node.text);
  }

  if (
    ts.isPrefixUnaryExpression(node) &&
    node.operator === ts.SyntaxKind.MinusToken &&
    ts.isNumericLiteral(node.operand)
  ) {
    return -Number(node.operand.text);
  }

  fail(`${label} must be a numeric literal`);
}

function getNumber(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing numeric property ${key}`);
  }

  return numericValue(property.initializer, key);
}

function getObject(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing object property ${key}`);
  }

  return requireObjectLiteral(property.initializer, key);
}

function getStringArray(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing array property ${key}`);
  }

  return requireArrayLiteral(property.initializer, key).elements.map((element) => {
    if (!ts.isStringLiteral(element) && !ts.isNoSubstitutionTemplateLiteral(element)) {
      fail(`${key} must contain string literals`);
    }

    return element.text;
  });
}

function getNumberArray(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing vector property ${key}`);
  }

  return requireArrayLiteral(property.initializer, key).elements.map((element, index) =>
    numericValue(element, `${key}[${index}]`),
  );
}

function parseSceneThree(scrollScenesFile) {
  const initializer = requireArrayLiteral(findVariableInitializer(scrollScenesFile, "SCROLL_SCENES"), "SCROLL_SCENES");

  for (const element of initializer.elements) {
    const scene = requireObjectLiteral(element, "scroll scene");

    if (getNumber(scene, "scene") === 3) {
      return scene;
    }
  }

  fail("Scene 3 was not found");
}

const scrollScenesFile = await readSource(scrollScenesPath);
const sceneThree = parseSceneThree(scrollScenesFile);
const camera = getObject(sceneThree, "camera");
const interiorCamera = getObject(sceneThree, "interiorCamera");
const activeEnergyIds = getStringArray(sceneThree, "activeEnergyIds");
const citySceneSource = await fs.readFile(cityScenePath, "utf8");
const siaLayerSource = await fs.readFile(siaLayerPath, "utf8");
const sceneSummary = {
  title: getString(sceneThree, "title"),
  body: getString(sceneThree, "body"),
  activeDistrict: getString(sceneThree, "activeDistrict"),
  mode: getString(sceneThree, "mode"),
  interiorId: getString(sceneThree, "interiorId"),
  interiorStart: getNumber(sceneThree, "interiorStart"),
  activeEnergyIds,
  camera: {
    position: getNumberArray(camera, "position"),
    target: getNumberArray(camera, "target"),
    fov: getNumber(camera, "fov"),
  },
  interiorCamera: {
    position: getNumberArray(interiorCamera, "position"),
    target: getNumberArray(interiorCamera, "target"),
    fov: getNumber(interiorCamera, "fov"),
  },
};
const componentChecks = {
  mountedInCityScene:
    citySceneSource.includes("SiaInteriorRewriteLayer") && citySceneSource.includes("sceneIndex === 3"),
  markers: requiredMarkers.map((marker) => ({
    marker,
    present: siaLayerSource.includes(marker),
  })),
  hasVerdictDataAttribute: siaLayerSource.includes('data-session78-verdict="inside-sia-tower"'),
  hasReadableCue:
    siaLayerSource.includes("Neural Core Atrium") && siaLayerSource.includes("Inside SIA Tower"),
};
const failures = [];

if (sceneSummary.title !== "Inside SIA Tower") {
  failures.push("Scene 3 title must be normalized to Inside SIA Tower");
}

if (sceneSummary.mode !== "interior" || sceneSummary.activeDistrict !== "sia-tower") {
  failures.push("Scene 3 must remain an interior SIA scene");
}

if (sceneSummary.interiorId !== "sia-tower") {
  failures.push("Scene 3 must mount the SIA interior asset");
}

if (sceneSummary.interiorStart < 0.18 || sceneSummary.interiorStart > 0.35) {
  failures.push("Scene 3 must keep an entrance moment before mounting the interior");
}

if (sceneSummary.camera.position[2] < 12 || sceneSummary.camera.position[1] > 6.2) {
  failures.push("Scene 3 starting camera must read as an entrance approach");
}

if (sceneSummary.interiorCamera.position[1] < 9 || sceneSummary.interiorCamera.target[2] > -1) {
  failures.push("Scene 3 midpoint camera must look deeper into the atrium");
}

if (sceneSummary.interiorCamera.fov < 44 || sceneSummary.interiorCamera.fov > 50) {
  failures.push("Scene 3 midpoint FOV must stay wide enough for the atrium");
}

for (const energyId of ["ai-pulse", "cross-district-gold"]) {
  if (!activeEnergyIds.includes(energyId)) {
    failures.push(`Scene 3 must keep ${energyId} active`);
  }
}

if (!componentChecks.mountedInCityScene) {
  failures.push("SiaInteriorRewriteLayer must be mounted only for Scene 3");
}

for (const marker of componentChecks.markers) {
  if (!marker.present) {
    failures.push(`Missing Session 78 visual marker: ${marker.marker}`);
  }
}

if (!componentChecks.hasVerdictDataAttribute) {
  failures.push("Scene 3 must expose the inside-SIA verdict data attribute");
}

if (!componentChecks.hasReadableCue) {
  failures.push("Scene 3 must include a readable Neural Core Atrium cue");
}

const report = {
  session: 78,
  date: "2026-05-26",
  result: failures.length ? "FAIL" : "PASS",
  checks: {
    sceneSummary,
    componentChecks,
  },
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

if (failures.length) {
  console.error(`Session 78 SIA interior QA failed. Report: ${path.relative(repoRoot, reportPath)}`);
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log(`Session 78 SIA interior QA passed. Report: ${path.relative(repoRoot, reportPath)}`);

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import ts from "typescript";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const scrollScenesPath = path.join(appDir, "src/lib/scroll-scenes.ts");
const typesPath = path.join(appDir, "src/lib/types.ts");
const productOverlayPath = path.join(appDir, "src/components/ui/ProductRealityOverlay.tsx");
const metadataPath = path.join(appDir, "src/lib/district-metadata.ts");
const layoutPath = path.join(repoRoot, "shared/city-layout-v2.json");
const reportPath = path.join(repoRoot, "output/playwright/session82-flow-static-qa.json");

const requiredBridgeScenes = new Map([
  [3, { label: "SIA to Fitness", exitAt: [0.72, 0.82], targetDistrict: "fitness" }],
  [13, { label: "Analytics to Nutrition", exitAt: [0.8, 0.9], targetDistrict: "nutrition" }],
  [14, { label: "Nutrition to Climax", exitAt: [0.8, 0.9], targetCenter: true }],
  [15, { label: "Climax to Product", exitAt: [0.72, 0.84], targetDistrict: "chat" }],
  [16, { label: "Product to Closing", exitAt: [0.64, 0.72], holdProductCamera: true }],
]);

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

function unwrapExpression(node) {
  let current = node;

  while (current && (ts.isAsExpression(current) || ts.isSatisfiesExpression(current))) {
    current = current.expression;
  }

  return current;
}

function findVariableInitializer(sourceFile, variableName) {
  let initializer;

  function visit(node) {
    if (ts.isVariableDeclaration(node) && ts.isIdentifier(node.name) && node.name.text === variableName) {
      initializer = unwrapExpression(node.initializer);
    }

    ts.forEachChild(node, visit);
  }

  visit(sourceFile);

  return initializer;
}

function requireObjectLiteral(node, label) {
  const unwrapped = unwrapExpression(node);

  if (!unwrapped || !ts.isObjectLiteralExpression(unwrapped)) {
    fail(`${label} must be an object literal`);
  }

  return unwrapped;
}

function requireArrayLiteral(node, label) {
  const unwrapped = unwrapExpression(node);

  if (!unwrapped || !ts.isArrayLiteralExpression(unwrapped)) {
    fail(`${label} must be an array literal`);
  }

  return unwrapped;
}

function getProperty(objectLiteral, key) {
  return objectLiteral.properties.find(
    (property) => ts.isPropertyAssignment(property) && propertyNameText(property.name) === key,
  );
}

function getOptionalProperty(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  return property && ts.isPropertyAssignment(property) ? property.initializer : undefined;
}

function numericValue(node, label) {
  const unwrapped = unwrapExpression(node);

  if (ts.isNumericLiteral(unwrapped)) {
    return Number(unwrapped.text);
  }

  if (
    ts.isPrefixUnaryExpression(unwrapped) &&
    unwrapped.operator === ts.SyntaxKind.MinusToken &&
    ts.isNumericLiteral(unwrapped.operand)
  ) {
    return -Number(unwrapped.operand.text);
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

function getOptionalNumber(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    return undefined;
  }

  return numericValue(property.initializer, key);
}

function getString(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing string property ${key}`);
  }

  const value = unwrapExpression(property.initializer);

  if (!ts.isStringLiteral(value) && !ts.isNoSubstitutionTemplateLiteral(value)) {
    fail(`${key} must be a string literal`);
  }

  return value.text;
}

function getObject(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing object property ${key}`);
  }

  return requireObjectLiteral(property.initializer, key);
}

function getOptionalObject(objectLiteral, key) {
  const value = getOptionalProperty(objectLiteral, key);

  return value ? requireObjectLiteral(value, key) : undefined;
}

function vectorLiteral(node, label) {
  return requireArrayLiteral(node, label).elements.map((element, index) =>
    numericValue(element, `${label}[${index}]`),
  );
}

function resolveVectorExpression(node, sourceFile, cityLayout, label) {
  const value = unwrapExpression(node);

  if (ts.isArrayLiteralExpression(value)) {
    return vectorLiteral(value, label);
  }

  if (ts.isCallExpression(value) && ts.isIdentifier(value.expression)) {
    const helper = value.expression.text;
    const districtArg = unwrapExpression(value.arguments[0]);

    if (!ts.isStringLiteral(districtArg) && !ts.isNoSubstitutionTemplateLiteral(districtArg)) {
      fail(`${label} helper must use a literal district id`);
    }

    const district = cityLayout.districts[districtArg.text];

    if (!district) {
      fail(`${label} references unknown district ${districtArg.text}`);
    }

    if (helper === "districtCamera") {
      const offset = vectorLiteral(value.arguments[1], `${label}.offset`);

      return [
        district.runtimePosition[0] + offset[0],
        offset[1],
        district.runtimePosition[2] + offset[2],
      ];
    }

    if (helper === "districtTarget") {
      return [
        district.runtimePosition[0],
        numericValue(value.arguments[1], `${label}.height`),
        district.runtimePosition[2],
      ];
    }
  }

  if (ts.isIdentifier(value)) {
    return resolveVectorExpression(findVariableInitializer(sourceFile, value.text), sourceFile, cityLayout, label);
  }

  fail(`${label} must resolve to a vector`);
}

function getVector(objectLiteral, key, sourceFile, cityLayout) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing vector property ${key}`);
  }

  return resolveVectorExpression(property.initializer, sourceFile, cityLayout, key);
}

function parseFocusedSceneMap(metadataFile) {
  const initializer = requireObjectLiteral(
    findVariableInitializer(metadataFile, "FOCUSED_SCENE_INTERACTION_IDS"),
    "FOCUSED_SCENE_INTERACTION_IDS",
  );
  const sceneMap = {};

  for (const property of initializer.properties) {
    if (!ts.isPropertyAssignment(property)) {
      continue;
    }

    const scene = Number(propertyNameText(property.name));
    const value = unwrapExpression(property.initializer);

    if (!Number.isFinite(scene) || (!ts.isStringLiteral(value) && !ts.isNoSubstitutionTemplateLiteral(value))) {
      fail("Focused scene interaction map must use numeric keys and district string values");
    }

    sceneMap[scene] = value.text;
  }

  return sceneMap;
}

function parseScrollScenes(scrollScenesFile, cityLayout) {
  const initializer = requireArrayLiteral(findVariableInitializer(scrollScenesFile, "SCROLL_SCENES"), "SCROLL_SCENES");

  return initializer.elements.map((element) => {
    const scene = requireObjectLiteral(element, "scroll scene");
    const camera = getObject(scene, "camera");
    const exitCamera = getOptionalObject(scene, "exitCamera");
    const bodySequence = getOptionalProperty(scene, "bodySequence");

    return {
      activeDistrict: getString(scene, "activeDistrict"),
      bodySequenceLength: bodySequence ? requireArrayLiteral(bodySequence, "bodySequence").elements.length : 0,
      camera: {
        position: getVector(camera, "position", scrollScenesFile, cityLayout),
        target: getVector(camera, "target", scrollScenesFile, cityLayout),
      },
      exitAt: getOptionalNumber(scene, "exitAt"),
      exitCamera: exitCamera
        ? {
            position: getVector(exitCamera, "position", scrollScenesFile, cityLayout),
            target: getVector(exitCamera, "target", scrollScenesFile, cityLayout),
          }
        : undefined,
      interiorCameraAt: getOptionalNumber(scene, "interiorCameraAt"),
      interiorStart: getOptionalNumber(scene, "interiorStart"),
      mode: getString(scene, "mode"),
      scene: getNumber(scene, "scene"),
      scroll: getNumber(scene, "scroll"),
    };
  });
}

function planarDistance(left, right) {
  return Math.hypot(left[0] - right[0], left[2] - right[2]);
}

function vectorDistance(left, right) {
  return Math.hypot(left[0] - right[0], left[1] - right[1], left[2] - right[2]);
}

const scrollScenesFile = await readSource(scrollScenesPath);
const metadataFile = await readSource(metadataPath);
const cityLayout = JSON.parse(await fs.readFile(layoutPath, "utf8"));
const typesSource = await fs.readFile(typesPath, "utf8");
const scrollSource = await fs.readFile(scrollScenesPath, "utf8");
const productOverlaySource = await fs.readFile(productOverlayPath, "utf8");
const focusedSceneMap = parseFocusedSceneMap(metadataFile);
const scenes = parseScrollScenes(scrollScenesFile, cityLayout);
const failures = [];
const bridgeChecks = [];

if (scenes.length !== 17) {
  failures.push(`Expected 17 scroll scenes, found ${scenes.length}`);
}

for (let index = 1; index < scenes.length; index += 1) {
  if (scenes[index].scroll <= scenes[index - 1].scroll) {
    failures.push(`Scene ${scenes[index].scene} scroll position must be after Scene ${scenes[index - 1].scene}`);
  }
}

if (!typesSource.includes("exitAt?: number") || !typesSource.includes("exitCamera?: ScrollCamera")) {
  failures.push("ScrollScene type must expose exitAt and exitCamera");
}

if (!scrollSource.includes("current.exitCamera") || !scrollSource.includes("current.exitAt")) {
  failures.push("Camera interpolation must include exitCamera frames");
}

for (const [sceneIndex, requirement] of requiredBridgeScenes) {
  const scene = scenes.find((candidate) => candidate.scene === sceneIndex);

  if (!scene) {
    failures.push(`Missing required bridge scene ${sceneIndex}`);
    continue;
  }

  const [minAt, maxAt] = requirement.exitAt;

  if (!scene.exitCamera || typeof scene.exitAt !== "number") {
    failures.push(`Scene ${sceneIndex} must define an exit camera for ${requirement.label}`);
    continue;
  }

  if (scene.exitAt < minAt || scene.exitAt > maxAt) {
    failures.push(`Scene ${sceneIndex} exitAt ${scene.exitAt} is outside ${requirement.label} range`);
  }

  if (scene.interiorCameraAt && scene.exitAt <= scene.interiorCameraAt + 0.08) {
    failures.push(`Scene ${sceneIndex} exitAt must leave a readable interior midpoint before exiting`);
  }

  if (requirement.targetDistrict) {
    const targetDistrict = cityLayout.districts[requirement.targetDistrict].runtimePosition;
    const targetDistance = planarDistance(scene.exitCamera.target, targetDistrict);

    if (targetDistance > 1.2) {
      failures.push(`Scene ${sceneIndex} exit camera should look toward ${requirement.targetDistrict}`);
    }
  }

  if (requirement.targetCenter && planarDistance(scene.exitCamera.target, [0, 0, 0]) > 8) {
    failures.push(`Scene ${sceneIndex} exit camera should pull back toward the city center before climax`);
  }

  if (requirement.holdProductCamera) {
    const positionDistance = vectorDistance(scene.exitCamera.position, scene.camera.position);
    const targetDistance = vectorDistance(scene.exitCamera.target, scene.camera.target);

    if (positionDistance > 0.01 || targetDistance > 0.01) {
      failures.push("Scene 16 exit camera must hold the Today Screen framing before the closing pullback");
    }
  }

  bridgeChecks.push({
    scene: sceneIndex,
    label: requirement.label,
    exitAt: scene.exitAt,
    mode: scene.mode,
    targetPlanarDistance: requirement.targetDistrict
      ? Number(planarDistance(scene.exitCamera.target, cityLayout.districts[requirement.targetDistrict].runtimePosition).toFixed(2))
      : requirement.targetCenter
        ? Number(planarDistance(scene.exitCamera.target, [0, 0, 0]).toFixed(2))
        : 0,
  });
}

for (const [sceneIndex, districtId] of Object.entries({
  2: "sia-tower",
  3: "sia-tower",
  4: "fitness",
  5: "yoga",
  6: "finance",
  7: "knowledgebase",
  8: "chat",
  9: "leaderboard",
  10: "relationships",
  11: "career",
  12: "recovery",
  13: "analytics",
  14: "nutrition",
})) {
  if (focusedSceneMap[Number(sceneIndex)] !== districtId) {
    failures.push(`Focused scene ${sceneIndex} interaction gate must remain ${districtId}`);
  }
}

const climaxScene = scenes.find((scene) => scene.scene === 15);

if (!climaxScene || climaxScene.bodySequenceLength !== 4) {
  failures.push("Scene 15 must keep its four-part climax body sequence");
}

for (const requiredProductCopy of [
  "exitProgress",
  "data-session82-product-exit",
  "resolving-to-closing",
]) {
  if (!productOverlaySource.includes(requiredProductCopy)) {
    failures.push(`Product overlay is missing Session 82 exit behavior: ${requiredProductCopy}`);
  }
}

const report = {
  session: 82,
  date: "2026-05-26",
  result: failures.length ? "FAIL" : "PASS",
  checks: {
    bridgeChecks,
    interactionGatesPreserved: Object.keys(focusedSceneMap).length >= 13,
    productExitFade: {
      hasExitProgress: productOverlaySource.includes("exitProgress"),
      hasSession82Attribute: productOverlaySource.includes("data-session82-product-exit"),
    },
    sceneCount: scenes.length,
  },
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

if (failures.length) {
  console.error(`Session 82 flow QA failed. Report: ${path.relative(repoRoot, reportPath)}`);
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log(`Session 82 flow QA passed. Report: ${path.relative(repoRoot, reportPath)}`);

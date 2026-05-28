import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import ts from "typescript";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const metadataPath = path.join(appDir, "src/lib/district-metadata.ts");
const scrollScenesPath = path.join(appDir, "src/lib/scroll-scenes.ts");
const cityScenePath = path.join(appDir, "src/components/scenes/CityScene.tsx");
const revealLayerPath = path.join(appDir, "src/components/scenes/DistrictInteriorRevealLayer.tsx");
const stylesPath = path.join(appDir, "src/styles.css");
const layoutPath = path.join(repoRoot, "shared/city-layout-v2.json");
const reportPath = path.join(repoRoot, "output/playwright/session80-interior-reveal-static-qa.json");

const repairScenes = new Map([
  [4, "fitness"],
  [5, "yoga"],
  [6, "finance"],
  [7, "knowledgebase"],
  [8, "chat"],
]);

const expectedEnergyIds = {
  fitness: ["hard-pipelines", "ai-pulse"],
  yoga: ["warm-mist", "ai-pulse"],
  finance: ["hard-pipelines", "ai-pulse"],
  knowledgebase: ["hard-pipelines", "knowledgebase-waterfall", "ai-pulse"],
  chat: ["hard-pipelines", "ai-pulse"],
};

const requiredMarkers = [
  "fitness-threshold",
  "fitness-interior-midpoint",
  "yoga-threshold",
  "yoga-interior-midpoint",
  "finance-threshold",
  "finance-interior-midpoint",
  "knowledgebase-threshold",
  "knowledgebase-interior-midpoint",
  "chat-threshold",
  "chat-interior-midpoint",
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

function getBoolean(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing boolean property ${key}`);
  }

  const value = unwrapExpression(property.initializer);

  if (value.kind === ts.SyntaxKind.TrueKeyword) {
    return true;
  }

  if (value.kind === ts.SyntaxKind.FalseKeyword) {
    return false;
  }

  fail(`${key} must be a boolean literal`);
}

function getObject(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing object property ${key}`);
  }

  return requireObjectLiteral(property.initializer, key);
}

function vectorLiteral(node, label) {
  return requireArrayLiteral(node, label).elements.map((element, index) => numericValue(element, `${label}[${index}]`));
}

function parseStringArrayExpression(node, sourceFile, label) {
  const value = unwrapExpression(node);

  if (ts.isArrayLiteralExpression(value)) {
    return value.elements.map((element) => {
      const unwrapped = unwrapExpression(element);

      if (!ts.isStringLiteral(unwrapped) && !ts.isNoSubstitutionTemplateLiteral(unwrapped)) {
        fail(`${label} must contain string literals`);
      }

      return unwrapped.text;
    });
  }

  if (ts.isIdentifier(value)) {
    return parseStringArrayExpression(findVariableInitializer(sourceFile, value.text), sourceFile, value.text);
  }

  fail(`${label} must resolve to a string array`);
}

function getStringArray(objectLiteral, key, sourceFile) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing array property ${key}`);
  }

  return parseStringArrayExpression(property.initializer, sourceFile, key);
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

function parseDistrictProfiles(metadataFile) {
  const initializer = requireObjectLiteral(findVariableInitializer(metadataFile, "DISTRICT_PROFILES"), "DISTRICT_PROFILES");
  const profiles = {};

  for (const property of initializer.properties) {
    if (!ts.isPropertyAssignment(property)) {
      continue;
    }

    const id = propertyNameText(property.name);

    if (!id) {
      fail("District profile has an unsupported key");
    }

    const profile = requireObjectLiteral(property.initializer, `${id} profile`);
    const preview = getObject(profile, "preview");

    profiles[id] = {
      interactionTarget: getBoolean(profile, "interactionTarget"),
      label: getString(profile, "label"),
      preview: {
        status: getString(preview, "status"),
        insight: getString(preview, "insight"),
        signal: getString(preview, "signal"),
      },
    };
  }

  return profiles;
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

function parseRepairScenes(scrollScenesFile, cityLayout) {
  const initializer = requireArrayLiteral(findVariableInitializer(scrollScenesFile, "SCROLL_SCENES"), "SCROLL_SCENES");
  const scenes = [];

  for (const element of initializer.elements) {
    const scene = requireObjectLiteral(element, "scroll scene");
    const sceneIndex = getNumber(scene, "scene");

    if (!repairScenes.has(sceneIndex)) {
      continue;
    }

    const camera = getObject(scene, "camera");
    const approachCamera = getObject(scene, "approachCamera");
    const thresholdCamera = getObject(scene, "thresholdCamera");
    const interiorCamera = getObject(scene, "interiorCamera");

    scenes.push({
      activeDistrict: getString(scene, "activeDistrict"),
      activeEnergyIds: getStringArray(scene, "activeEnergyIds", scrollScenesFile),
      approachAt: getNumber(scene, "approachAt"),
      approachCamera: {
        fov: getNumber(approachCamera, "fov"),
        position: getVector(approachCamera, "position", scrollScenesFile, cityLayout),
        target: getVector(approachCamera, "target", scrollScenesFile, cityLayout),
      },
      camera: {
        fov: getNumber(camera, "fov"),
        position: getVector(camera, "position", scrollScenesFile, cityLayout),
        target: getVector(camera, "target", scrollScenesFile, cityLayout),
      },
      interiorCamera: {
        fov: getNumber(interiorCamera, "fov"),
        position: getVector(interiorCamera, "position", scrollScenesFile, cityLayout),
        target: getVector(interiorCamera, "target", scrollScenesFile, cityLayout),
      },
      interiorCameraAt: getNumber(scene, "interiorCameraAt"),
      interiorId: getString(scene, "interiorId"),
      interiorStart: getNumber(scene, "interiorStart"),
      mode: getString(scene, "mode"),
      scene: sceneIndex,
      thresholdAt: getNumber(scene, "thresholdAt"),
      thresholdCamera: {
        fov: getNumber(thresholdCamera, "fov"),
        position: getVector(thresholdCamera, "position", scrollScenesFile, cityLayout),
        target: getVector(thresholdCamera, "target", scrollScenesFile, cityLayout),
      },
    });
  }

  return scenes;
}

function planarDistance(position, districtPosition) {
  return Math.hypot(position[0] - districtPosition[0], position[2] - districtPosition[2]);
}

const metadataFile = await readSource(metadataPath);
const scrollScenesFile = await readSource(scrollScenesPath);
const profiles = parseDistrictProfiles(metadataFile);
const focusedSceneMap = parseFocusedSceneMap(metadataFile);
const cityLayout = JSON.parse(await fs.readFile(layoutPath, "utf8"));
const scenes = parseRepairScenes(scrollScenesFile, cityLayout);
const citySceneSource = await fs.readFile(cityScenePath, "utf8");
const revealLayerSource = await fs.readFile(revealLayerPath, "utf8");
const stylesSource = await fs.readFile(stylesPath, "utf8");
const failures = [];
const sceneChecks = [];
const interactionChecks = [];

if (scenes.length !== repairScenes.size) {
  failures.push(`Expected ${repairScenes.size} repair scenes, found ${scenes.length}`);
}

for (const scene of scenes) {
  const expectedDistrictId = repairScenes.get(scene.scene);
  const districtPosition = cityLayout.districts[expectedDistrictId].runtimePosition;
  const startDistance = planarDistance(scene.camera.position, districtPosition);
  const approachDistance = planarDistance(scene.approachCamera.position, districtPosition);
  const thresholdDistance = planarDistance(scene.thresholdCamera.position, districtPosition);
  const interiorDistance = planarDistance(scene.interiorCamera.position, districtPosition);
  const expectedEnergy = expectedEnergyIds[expectedDistrictId] ?? [];

  if (scene.activeDistrict !== expectedDistrictId || scene.interiorId !== expectedDistrictId) {
    failures.push(`Scene ${scene.scene} must target ${expectedDistrictId}`);
  }

  if (scene.mode !== "exterior") {
    failures.push(`Scene ${scene.scene} must remain an exterior-to-interior scene`);
  }

  if (scene.interiorStart < 0.52 || scene.interiorStart > 0.6) {
    failures.push(`Scene ${scene.scene} interiorStart must leave a clear exterior/threshold beat`);
  }

  if (scene.approachAt < 0.28 || scene.approachAt > 0.38) {
    failures.push(`Scene ${scene.scene} approachAt is outside the readable approach range`);
  }

  if (Math.abs(scene.thresholdAt - scene.interiorStart) > 0.001) {
    failures.push(`Scene ${scene.scene} thresholdAt must match the interior mounting threshold`);
  }

  if (scene.interiorCameraAt < 0.68 || scene.interiorCameraAt > 0.76) {
    failures.push(`Scene ${scene.scene} interior midpoint must be after the threshold and before transition out`);
  }

  if (startDistance < 52) {
    failures.push(`Scene ${scene.scene} starts too close to ${expectedDistrictId}: ${startDistance.toFixed(2)}u`);
  }

  if (approachDistance >= startDistance || approachDistance < 32) {
    failures.push(`Scene ${scene.scene} approach camera does not bridge exterior to threshold`);
  }

  if (thresholdDistance < 16 || thresholdDistance > 26) {
    failures.push(`Scene ${scene.scene} threshold camera distance is not entry-like: ${thresholdDistance.toFixed(2)}u`);
  }

  if (interiorDistance > 9) {
    failures.push(`Scene ${scene.scene} interior midpoint remains too exterior: ${interiorDistance.toFixed(2)}u`);
  }

  if (scene.camera.fov < 42 || scene.thresholdCamera.fov < 41 || scene.interiorCamera.fov < 42) {
    failures.push(`Scene ${scene.scene} FOV must stay wide enough to read the district and room`);
  }

  for (const energyId of expectedEnergy) {
    if (!scene.activeEnergyIds.includes(energyId)) {
      failures.push(`Scene ${scene.scene} must keep ${energyId} active`);
    }
  }

  if (!profiles[expectedDistrictId]?.interactionTarget || focusedSceneMap[scene.scene] !== expectedDistrictId) {
    failures.push(`Scene ${scene.scene} interaction gate must expose only ${expectedDistrictId}`);
  }

  sceneChecks.push({
    scene: scene.scene,
    districtId: expectedDistrictId,
    startDistance: Number(startDistance.toFixed(2)),
    approachDistance: Number(approachDistance.toFixed(2)),
    thresholdDistance: Number(thresholdDistance.toFixed(2)),
    interiorDistance: Number(interiorDistance.toFixed(2)),
    interiorStart: scene.interiorStart,
    interiorCameraAt: scene.interiorCameraAt,
  });

  interactionChecks.push({
    scene: scene.scene,
    expectedOnly: expectedDistrictId,
    focusedSceneMap: focusedSceneMap[scene.scene],
    interactive: profiles[expectedDistrictId]?.interactionTarget === true,
  });
}

if (!citySceneSource.includes("DistrictInteriorRevealLayer") || !citySceneSource.includes("sceneIndex >= 4 && sceneIndex <= 14")) {
  failures.push("DistrictInteriorRevealLayer must be mounted for the Phase 9 reveal scenes");
}

if (!revealLayerSource.includes("session80-interior-reveal") || !revealLayerSource.includes("data-session80-verdict")) {
  failures.push("Session 80 reveal layer must expose DOM-visible QA markers");
}

for (const marker of requiredMarkers) {
  if (!revealLayerSource.includes(marker)) {
    failures.push(`Missing Session 80 marker: ${marker}`);
  }
}

for (const copy of ["Inside Fitness Arena", "Inside Yoga Dome", "Inside Finance Advisory", "Inside Knowledgebase", "Inside Communication Nexus"]) {
  if (!revealLayerSource.includes(copy)) {
    failures.push(`Missing readable interior cue copy: ${copy}`);
  }
}

if (!stylesSource.includes(".interior-reveal-cue") || !stylesSource.includes("overflow-wrap: anywhere")) {
  failures.push("Session 80 cue CSS must keep interior text bounded and wrapping");
}

const knowledgebasePreviewValues = Object.values(profiles.knowledgebase.preview);
const financePreviewValues = Object.values(profiles.finance.preview);
const knowledgebaseRegression = {
  expectedStatus: "Learning queue tuned",
  actualStatus: profiles.knowledgebase.preview.status,
  financeCopyMatches: financePreviewValues.filter((value) => knowledgebasePreviewValues.includes(value)),
};
const chatInteraction = {
  interactionTarget: profiles.chat.interactionTarget,
  focusedScene: focusedSceneMap[8],
  previewStatus: profiles.chat.preview.status,
};

if (knowledgebaseRegression.actualStatus !== knowledgebaseRegression.expectedStatus) {
  failures.push("Knowledgebase status does not match the required regression value");
}

if (knowledgebaseRegression.financeCopyMatches.length > 0) {
  failures.push("Knowledgebase preview contains Finance preview copy");
}

if (!chatInteraction.interactionTarget || chatInteraction.focusedScene !== "chat") {
  failures.push("Chat must remain the only interaction target in Scene 8");
}

const report = {
  session: 80,
  date: "2026-05-26",
  result: failures.length ? "FAIL" : "PASS",
  checks: {
    chatInteraction,
    interactionChecks,
    knowledgebaseRegression,
    sceneChecks,
    textOverlapGuard: {
      hasInteriorCueCss: stylesSource.includes(".interior-reveal-cue"),
      wrapsCueText: stylesSource.includes("overflow-wrap: anywhere"),
    },
  },
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

if (failures.length) {
  console.error(`Session 80 interior reveal QA failed. Report: ${path.relative(repoRoot, reportPath)}`);
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log(`Session 80 interior reveal QA passed. Report: ${path.relative(repoRoot, reportPath)}`);

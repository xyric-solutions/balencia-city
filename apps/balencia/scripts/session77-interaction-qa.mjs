import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import ts from "typescript";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const metadataPath = path.join(appDir, "src/lib/district-metadata.ts");
const scrollScenesPath = path.join(appDir, "src/lib/scroll-scenes.ts");
const reportPath = path.join(repoRoot, "output/playwright/session77-interaction-static-qa.json");

function fail(message) {
  throw new Error(message);
}

async function readSource(filePath) {
  const sourceText = await fs.readFile(filePath, "utf8");

  return ts.createSourceFile(filePath, sourceText, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS);
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

function getNumber(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property) || !ts.isNumericLiteral(property.initializer)) {
    fail(`Missing numeric property ${key}`);
  }

  return Number(property.initializer.text);
}

function getBoolean(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing boolean property ${key}`);
  }

  if (property.initializer.kind === ts.SyntaxKind.TrueKeyword) {
    return true;
  }

  if (property.initializer.kind === ts.SyntaxKind.FalseKeyword) {
    return false;
  }

  fail(`${key} must be a boolean literal`);
}

function getNestedObject(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    fail(`Missing object property ${key}`);
  }

  return requireObjectLiteral(property.initializer, key);
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
    const preview = getNestedObject(profile, "preview");

    profiles[id] = {
      id,
      interactionTarget: getBoolean(profile, "interactionTarget"),
      label: getString(profile, "label"),
      place: getString(profile, "place"),
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
    const value = property.initializer;

    if (!Number.isFinite(scene) || (!ts.isStringLiteral(value) && !ts.isNoSubstitutionTemplateLiteral(value))) {
      fail("Focused scene interaction map must use numeric keys and district string values");
    }

    sceneMap[scene] = value.text;
  }

  return sceneMap;
}

function parseScrollScenes(scrollScenesFile) {
  const initializer = requireArrayLiteral(findVariableInitializer(scrollScenesFile, "SCROLL_SCENES"), "SCROLL_SCENES");

  return initializer.elements.map((element) => {
    const scene = requireObjectLiteral(element, "scroll scene");

    return {
      scene: getNumber(scene, "scene"),
      activeDistrict: getString(scene, "activeDistrict"),
      mode: getString(scene, "mode"),
    };
  });
}

function arraysMatch(left, right) {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

function expectedInteractionIdsForScene(scene, allDistrictIds) {
  if ([1, 15, 17].includes(scene.scene)) {
    return allDistrictIds;
  }

  if (scene.mode === "product" || scene.activeDistrict === "city") {
    return [];
  }

  return [scene.activeDistrict];
}

const metadataFile = await readSource(metadataPath);
const scrollScenesFile = await readSource(scrollScenesPath);
const profiles = parseDistrictProfiles(metadataFile);
const focusedSceneMap = parseFocusedSceneMap(metadataFile);
const scenes = parseScrollScenes(scrollScenesFile);
const allDistrictIds = Object.keys(profiles);
const interactiveIds = allDistrictIds.filter((id) => profiles[id].interactionTarget);
const missingInteractionTargets = allDistrictIds.filter((id) => !profiles[id].interactionTarget);
const sceneGates = scenes.map((scene) => {
  const expected = expectedInteractionIdsForScene(scene, allDistrictIds);
  const actual = [1, 15, 17].includes(scene.scene)
    ? interactiveIds
    : focusedSceneMap[scene.scene]
      ? [focusedSceneMap[scene.scene]]
      : [];

  return {
    scene: scene.scene,
    activeDistrict: scene.activeDistrict,
    mode: scene.mode,
    expected,
    actual,
    result: arraysMatch(actual, expected) ? "PASS" : "FAIL",
  };
});
const previewContentChecks = allDistrictIds.map((id) => {
  const profile = profiles[id];
  const previewValues = Object.values(profile.preview);
  const hasCompletePreview = [profile.label, profile.place, ...previewValues].every((value) => value.trim().length > 0);

  return { id, result: hasCompletePreview ? "PASS" : "FAIL" };
});
const financePreviewValues = Object.values(profiles.finance.preview);
const knowledgebasePreviewValues = Object.values(profiles.knowledgebase.preview);
const knowledgebaseRegression = {
  expectedStatus: "Learning queue tuned",
  actualStatus: profiles.knowledgebase.preview.status,
  financeCopyMatches: financePreviewValues.filter((value) => knowledgebasePreviewValues.includes(value)),
};
const failures = [
  ...missingInteractionTargets.map((id) => `${id} is not interactive`),
  ...sceneGates.filter((gate) => gate.result !== "PASS").map((gate) => `Scene ${gate.scene} interaction gate mismatch`),
  ...previewContentChecks.filter((check) => check.result !== "PASS").map((check) => `${check.id} preview copy is incomplete`),
];

if (allDistrictIds.length !== 12) {
  failures.push(`Expected 12 districts, found ${allDistrictIds.length}`);
}

if (knowledgebaseRegression.actualStatus !== knowledgebaseRegression.expectedStatus) {
  failures.push("Knowledgebase status does not match the required regression value");
}

if (knowledgebaseRegression.financeCopyMatches.length > 0) {
  failures.push("Knowledgebase preview contains Finance preview copy");
}

const report = {
  session: 77,
  date: "2026-05-26",
  result: failures.length ? "FAIL" : "PASS",
  checks: {
    interactionCoverage: `${interactiveIds.length} / ${allDistrictIds.length}`,
    missingInteractionTargets,
    sceneGates,
    previewContentChecks,
    knowledgebaseRegression,
  },
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

if (failures.length) {
  console.error(`Session 77 interaction QA failed. Report: ${path.relative(repoRoot, reportPath)}`);
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log(`Session 77 interaction QA passed. Report: ${path.relative(repoRoot, reportPath)}`);

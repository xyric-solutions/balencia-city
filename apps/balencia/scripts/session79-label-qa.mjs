import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import ts from "typescript";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(appDir, "../..");
const metadataPath = path.join(appDir, "src/lib/district-metadata.ts");
const scrollScenesPath = path.join(appDir, "src/lib/scroll-scenes.ts");
const cityContextPath = path.join(appDir, "src/components/scenes/CityContext.tsx");
const districtLabelBoardPath = path.join(appDir, "src/components/scenes/DistrictLabelBoard.tsx");
const sceneOverlayPath = path.join(appDir, "src/components/ui/SceneOverlay.tsx");
const layoutPath = path.join(repoRoot, "shared/city-layout-v2.json");
const reportPath = path.join(repoRoot, "output/playwright/session79-label-static-qa.json");

const overviewScenes = [1, 15, 17];
const focusedDistrictScenes = new Map([
  [4, "fitness"],
  [5, "yoga"],
  [6, "finance"],
  [7, "knowledgebase"],
  [8, "chat"],
  [9, "leaderboard"],
  [10, "relationships"],
  [11, "career"],
  [12, "recovery"],
  [13, "analytics"],
  [14, "nutrition"],
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

function hasProperty(objectLiteral, key) {
  return !!getProperty(objectLiteral, key);
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

  const value = property.initializer;

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

  if (property.initializer.kind === ts.SyntaxKind.TrueKeyword) {
    return true;
  }

  if (property.initializer.kind === ts.SyntaxKind.FalseKeyword) {
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

function getOptionalNumberArray(objectLiteral, key) {
  const property = getProperty(objectLiteral, key);

  if (!property || !ts.isPropertyAssignment(property)) {
    return undefined;
  }

  return requireArrayLiteral(property.initializer, key).elements.map((element, index) =>
    numericValue(element, `${key}[${index}]`),
  );
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
      id,
      anchorHeight: getNumber(profile, "anchorHeight"),
      boardDirection: getOptionalNumberArray(profile, "boardDirection"),
      boardLift: getNumber(profile, "boardLift"),
      interactionTarget: getBoolean(profile, "interactionTarget"),
      label: getString(profile, "label"),
      labelLift: getNumber(profile, "labelLift"),
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

function parseOverviewLayouts(metadataFile) {
  const initializer = requireObjectLiteral(
    findVariableInitializer(metadataFile, "OVERVIEW_LABEL_LAYOUTS"),
    "OVERVIEW_LABEL_LAYOUTS",
  );
  const layouts = {};

  for (const sceneProperty of initializer.properties) {
    if (!ts.isPropertyAssignment(sceneProperty)) {
      continue;
    }

    const scene = Number(propertyNameText(sceneProperty.name));
    const sceneLayout = requireObjectLiteral(sceneProperty.initializer, `overview scene ${scene}`);
    layouts[scene] = {};

    for (const districtProperty of sceneLayout.properties) {
      if (!ts.isPropertyAssignment(districtProperty)) {
        continue;
      }

      const id = propertyNameText(districtProperty.name);

      if (!id) {
        fail(`Overview scene ${scene} has an unsupported district key`);
      }

      const districtLayout = requireObjectLiteral(districtProperty.initializer, `${scene}.${id} layout`);
      layouts[scene][id] = {
        hasLeft: hasProperty(districtLayout, "left"),
        hasTop: hasProperty(districtLayout, "top"),
        height: getNumber(districtLayout, "height"),
        lateral: getOptionalNumber(districtLayout, "lateral") ?? 0,
        maxWidth: getOptionalNumber(districtLayout, "maxWidth"),
        offset: getNumber(districtLayout, "offset"),
      };
    }
  }

  return layouts;
}

function parseActiveLabelOverrides(metadataFile) {
  const initializer = requireObjectLiteral(
    findVariableInitializer(metadataFile, "ACTIVE_LABEL_LAYOUT_OVERRIDES"),
    "ACTIVE_LABEL_LAYOUT_OVERRIDES",
  );
  const overrides = {};

  for (const sceneProperty of initializer.properties) {
    if (!ts.isPropertyAssignment(sceneProperty)) {
      continue;
    }

    const scene = Number(propertyNameText(sceneProperty.name));
    const sceneOverrides = requireObjectLiteral(sceneProperty.initializer, `active scene ${scene}`);
    overrides[scene] = {};

    for (const districtProperty of sceneOverrides.properties) {
      if (!ts.isPropertyAssignment(districtProperty)) {
        continue;
      }

      const id = propertyNameText(districtProperty.name);
      const override = requireObjectLiteral(districtProperty.initializer, `${scene}.${id} active override`);

      overrides[scene][id] = {
        distanceFactor: getOptionalNumber(override, "distanceFactor"),
        labelHeight: getOptionalNumber(override, "labelHeight"),
        labelOffset: getOptionalNumber(override, "labelOffset"),
      };
    }
  }

  return overrides;
}

function parseScrollScenes(scrollScenesFile) {
  const initializer = requireArrayLiteral(findVariableInitializer(scrollScenesFile, "SCROLL_SCENES"), "SCROLL_SCENES");

  return initializer.elements.map((element) => {
    const scene = requireObjectLiteral(element, "scroll scene");

    return {
      activeDistrict: getString(scene, "activeDistrict"),
      focus: getString(scene, "focus"),
      mode: getString(scene, "mode"),
      scene: getNumber(scene, "scene"),
      title: getString(scene, "title"),
    };
  });
}

function normalizePlanar(position, fallback = [0, 1]) {
  const [x, , z] = position;
  const length = Math.hypot(x, z);

  if (length < 0.0001) {
    return fallback;
  }

  return [x / length, z / length];
}

function overviewAnchorFor(id, layout, profiles, cityLayout) {
  const position = cityLayout.districts[id].runtimePosition;
  const profile = profiles[id];
  const boardDirection = profile.boardDirection;
  const [directionX, directionZ] = boardDirection
    ? normalizePlanar([boardDirection[0] ?? 0, 0, boardDirection[2] ?? 0], [0, 1])
    : normalizePlanar(position);
  const tangentX = -directionZ;
  const tangentZ = directionX;

  return {
    x: position[0] + directionX * layout.offset + tangentX * layout.lateral,
    y: layout.height,
    z: position[2] + directionZ * layout.offset + tangentZ * layout.lateral,
  };
}

function planarDistance(first, second) {
  return Math.hypot(first.x - second.x, first.z - second.z);
}

const metadataFile = await readSource(metadataPath);
const scrollScenesFile = await readSource(scrollScenesPath);
const profiles = parseDistrictProfiles(metadataFile);
const overviewLayouts = parseOverviewLayouts(metadataFile);
const activeLabelOverrides = parseActiveLabelOverrides(metadataFile);
const scenes = parseScrollScenes(scrollScenesFile);
const cityLayout = JSON.parse(await fs.readFile(layoutPath, "utf8"));
const cityContextSource = await fs.readFile(cityContextPath, "utf8");
const districtLabelBoardSource = await fs.readFile(districtLabelBoardPath, "utf8");
const sceneOverlaySource = await fs.readFile(sceneOverlayPath, "utf8");
const allDistrictIds = Object.keys(profiles);
const failures = [];
const overviewChecks = [];
const activeBoardChecks = [];
const namingChecks = [];

if (allDistrictIds.length !== 12) {
  failures.push(`Expected 12 districts, found ${allDistrictIds.length}`);
}

for (const id of allDistrictIds) {
  if (!profiles[id].interactionTarget) {
    failures.push(`${id} must stay interactive after Session 79`);
  }

  if (profiles[id].labelLift > 8) {
    failures.push(`${id} labelLift is too high for model-attached overview labels`);
  }

  if (profiles[id].boardLift > 8) {
    failures.push(`${id} boardLift is too high for active district boards`);
  }
}

for (const scene of overviewScenes) {
  const layout = overviewLayouts[scene];

  if (!layout) {
    failures.push(`Scene ${scene} is missing overview label layout`);
    continue;
  }

  const missing = allDistrictIds.filter((id) => !layout[id]);
  const staleScreenSpace = Object.entries(layout)
    .filter(([, labelLayout]) => labelLayout.hasLeft || labelLayout.hasTop)
    .map(([id]) => id);
  const anchors = Object.fromEntries(
    Object.entries(layout).map(([id, labelLayout]) => [id, overviewAnchorFor(id, labelLayout, profiles, cityLayout)]),
  );
  let minAnchorDistance = Infinity;

  for (let firstIndex = 0; firstIndex < allDistrictIds.length; firstIndex += 1) {
    for (let secondIndex = firstIndex + 1; secondIndex < allDistrictIds.length; secondIndex += 1) {
      const first = allDistrictIds[firstIndex];
      const second = allDistrictIds[secondIndex];
      minAnchorDistance = Math.min(minAnchorDistance, planarDistance(anchors[first], anchors[second]));
    }
  }

  for (const [id, labelLayout] of Object.entries(layout)) {
    const profile = profiles[id];

    if (!profile) {
      failures.push(`Scene ${scene} has unknown overview label ${id}`);
      continue;
    }

    if (labelLayout.height < Math.max(6, profile.anchorHeight * 0.7)) {
      failures.push(`Scene ${scene} ${id} overview label is below its model anchor`);
    }

    if (labelLayout.height > profile.anchorHeight + 24) {
      failures.push(`Scene ${scene} ${id} overview label floats too far above its model`);
    }

    if (labelLayout.offset < 6 || labelLayout.offset > 12) {
      failures.push(`Scene ${scene} ${id} overview label offset should stay close to the model`);
    }

    if (Math.abs(labelLayout.lateral) > 36) {
      failures.push(`Scene ${scene} ${id} overview lateral nudge is too far from its model`);
    }

    if (profile.label.length > 21 && (labelLayout.maxWidth ?? 0) < 188) {
      failures.push(`Scene ${scene} ${id} needs a wider label box for its canonical name`);
    }
  }

  if (missing.length) {
    failures.push(`Scene ${scene} is missing overview labels for ${missing.join(", ")}`);
  }

  if (staleScreenSpace.length) {
    failures.push(`Scene ${scene} still has screen-space label positions for ${staleScreenSpace.join(", ")}`);
  }

  if (minAnchorDistance < 18) {
    failures.push(`Scene ${scene} overview label anchors are too close together (${minAnchorDistance.toFixed(2)}u)`);
  }

  overviewChecks.push({
    scene,
    labelCount: Object.keys(layout).length,
    minAnchorDistance: Number(minAnchorDistance.toFixed(2)),
    missing,
    staleScreenSpace,
  });
}

for (const [scene, expectedDistrictId] of focusedDistrictScenes) {
  const override = activeLabelOverrides[scene]?.[expectedDistrictId];
  const profile = profiles[expectedDistrictId];

  if (!override) {
    failures.push(`Scene ${scene} is missing active label override for ${expectedDistrictId}`);
    continue;
  }

  if (!override.labelHeight || override.labelHeight > profile.anchorHeight + 3) {
    failures.push(`Scene ${scene} ${expectedDistrictId} active board height is not anchored tightly enough`);
  }

  if (!override.labelOffset || override.labelOffset < 2.5 || override.labelOffset > 5) {
    failures.push(`Scene ${scene} ${expectedDistrictId} active board offset is outside the anchored range`);
  }

  activeBoardChecks.push({
    scene,
    districtId: expectedDistrictId,
    labelHeight: override.labelHeight,
    labelOffset: override.labelOffset,
  });
}

for (const scene of scenes) {
  if (scene.activeDistrict === "city" || scene.mode === "product") {
    continue;
  }

  const profile = profiles[scene.activeDistrict];
  const expected = scene.scene === 3 ? `Inside ${profile.label}` : profile.label;
  const titleMatches = scene.title === expected;
  const focusMatches = scene.focus === expected;

  if (!titleMatches || !focusMatches) {
    failures.push(
      `Scene ${scene.scene} naming mismatch: expected "${expected}", got title "${scene.title}" and focus "${scene.focus}"`,
    );
  }

  namingChecks.push({
    scene: scene.scene,
    districtId: scene.activeDistrict,
    expected,
    focus: scene.focus,
    title: scene.title,
    result: titleMatches && focusMatches ? "PASS" : "FAIL",
  });
}

if (!cityContextSource.includes("Overview_Anchor_Labels")) {
  failures.push("CityContext must render overview labels from a 3D anchor group");
}

if (!cityContextSource.includes('data-label-anchor="model"')) {
  failures.push("Overview labels must expose data-label-anchor=\"model\" for QA");
}

if (!cityContextSource.includes("<Line")) {
  failures.push("Overview labels must include visible tethers to model anchors");
}

if (!districtLabelBoardSource.includes("ACTIVE_LABEL_LAYOUT_OVERRIDES")) {
  failures.push("DistrictLabelBoard must preserve active scene layout overrides");
}

if (!sceneOverlaySource.includes("<h1>{profile.label}</h1>")) {
  failures.push("District preview panel must use the canonical district label");
}

const knowledgebasePreviewValues = Object.values(profiles.knowledgebase.preview);
const financePreviewValues = Object.values(profiles.finance.preview);
const knowledgebaseRegression = {
  expectedStatus: "Learning queue tuned",
  actualStatus: profiles.knowledgebase.preview.status,
  financeCopyMatches: financePreviewValues.filter((value) => knowledgebasePreviewValues.includes(value)),
};

if (knowledgebaseRegression.actualStatus !== knowledgebaseRegression.expectedStatus) {
  failures.push("Knowledgebase status does not match the required regression value");
}

if (knowledgebaseRegression.financeCopyMatches.length > 0) {
  failures.push("Knowledgebase preview contains Finance preview copy");
}

const report = {
  session: 79,
  date: "2026-05-26",
  result: failures.length ? "FAIL" : "PASS",
  checks: {
    activeBoardChecks,
    interactionCoverage: `${allDistrictIds.filter((id) => profiles[id].interactionTarget).length} / ${allDistrictIds.length}`,
    knowledgebaseRegression,
    namingChecks,
    overviewChecks,
  },
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

if (failures.length) {
  console.error(`Session 79 label QA failed. Report: ${path.relative(repoRoot, reportPath)}`);
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log(`Session 79 label QA passed. Report: ${path.relative(repoRoot, reportPath)}`);

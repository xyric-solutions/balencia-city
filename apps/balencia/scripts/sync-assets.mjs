import fs from "node:fs/promises";
import path from "node:path";

const appDir = path.resolve(import.meta.dirname, "..");
const repoRoot = path.resolve(appDir, "../..");
const publicDir = path.join(appDir, "public");
const manifestPath = path.join(appDir, "src/lib/asset-manifest.json");
const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));

async function copyFile(sourceRel, publicRel) {
  const source = path.join(repoRoot, sourceRel);
  const destination = path.join(publicDir, publicRel);

  await fs.access(source);
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.copyFile(source, destination);

  return destination;
}

const copied = [];

for (const structure of manifest.structures) {
  copied.push(await copyFile(structure.exterior.sourcePath, structure.exterior.publicPath));
  copied.push(await copyFile(structure.interior.sourcePath, structure.interior.publicPath));
}

for (const energyAsset of manifest.energyAssets) {
  copied.push(await copyFile(energyAsset.sourcePath, energyAsset.publicPath));
}

await fs.mkdir(path.join(publicDir, "models"), { recursive: true });
await fs.copyFile(manifestPath, path.join(publicDir, "models/asset-manifest.json"));

const dracoSource = path.join(appDir, "node_modules/three/examples/jsm/libs/draco");
const dracoDestination = path.join(publicDir, "draco");
try {
  await fs.rm(dracoDestination, { recursive: true, force: true });
  await fs.mkdir(dracoDestination, { recursive: true });
  await fs.cp(dracoSource, dracoDestination, { recursive: true });
  console.log(`Synced Draco decoders to ${path.relative(appDir, dracoDestination)}`);
} catch (error) {
  console.warn("Draco decoder sync skipped. Run install before dev/build if node_modules is missing.");
  console.warn(error instanceof Error ? error.message : error);
}

console.log(`Synced ${copied.length} approved GLBs into ${path.relative(appDir, path.join(publicDir, "models"))}`);

import { spawnSync } from "node:child_process";
import path from "node:path";
import process from "node:process";

const appDir = path.resolve(import.meta.dirname, "..");
const binExt = process.platform === "win32" ? ".cmd" : "";

function runBin(name, args) {
  const command = path.join(appDir, "node_modules", ".bin", `${name}${binExt}`);
  const result = spawnSync(command, args, {
    cwd: appDir,
    stdio: "inherit",
  });

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

runBin("tsc", ["--noEmit"]);
runBin("vite", ["build"]);

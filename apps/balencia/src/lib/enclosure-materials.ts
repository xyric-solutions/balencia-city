import * as THREE from "three";
import type { FacadeStyle } from "./enclosure-profiles";

export type FresnelShellOptions = {
  baseColor?: string;
  rimColor: string;
  rimPower?: number;
  rimIntensity?: number;
  emissiveIntensity?: number;
  opacity?: number;
  envMapIntensity?: number;
  panelColumns?: number;
  panelRows?: number;
  mullionColor?: string;
  facadeStyle?: FacadeStyle;
};

function facadeParams(style: FacadeStyle) {
  switch (style) {
    case "metal-panel":
      return { roughness: 0.30, metalness: 0.55, envMap: 1.5, mullionWidth: 0.06 };
    case "crystalline":
      return { roughness: 0.05, metalness: 0.90, envMap: 5.0, mullionWidth: 0.03 };
    case "organic":
      return { roughness: 0.20, metalness: 0.60, envMap: 2.5, mullionWidth: 0 };
    case "industrial":
      return { roughness: 0.45, metalness: 0.55, envMap: 1.2, mullionWidth: 0.05 };
    default:
      return { roughness: 0.12, metalness: 0.82, envMap: 3.5, mullionWidth: 0.03 };
  }
}

export function createFresnelShellMaterial(opts: FresnelShellOptions): THREE.MeshStandardMaterial {
  const rimColor = new THREE.Color(opts.rimColor);
  const style = opts.facadeStyle ?? "glass-curtain";
  const fp = facadeParams(style);
  const opacity = opts.opacity ?? 0.7;

  const mat = new THREE.MeshStandardMaterial({
    color: opts.baseColor ?? "#1a1a2e",
    emissive: opts.rimColor,
    emissiveIntensity: opts.emissiveIntensity ?? 0.05,
    roughness: fp.roughness,
    metalness: fp.metalness,
    envMapIntensity: opts.envMapIntensity ?? fp.envMap,
    opacity,
    transparent: true,
    side: THREE.DoubleSide,
    depthWrite: opacity > 0.5,
  });

  const power = opts.rimPower ?? 2.5;
  let intensity = opts.rimIntensity ?? 0.8;
  if (style === "organic") intensity *= 1.3;
  const rStr = rimColor.r.toFixed(4);
  const gStr = rimColor.g.toFixed(4);
  const bStr = rimColor.b.toFixed(4);

  const panelCols = opts.panelColumns ?? 0;
  const panelRows = opts.panelRows ?? 0;
  const hasPanels = panelCols > 0 && panelRows > 0 && style !== "organic";
  const mullionColor = opts.mullionColor ?? (style === "metal-panel" ? "#060610" : "#0a0a12");
  const mc = new THREE.Color(mullionColor);
  const mw = fp.mullionWidth;

  mat.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader.replace(
      "void main() {",
      `varying vec3 vWorldNormal;
varying vec3 vViewDir;
varying vec2 vEnclosureUv;
void main() {`,
    );

    shader.vertexShader = shader.vertexShader.replace(
      "#include <worldpos_vertex>",
      `#include <worldpos_vertex>
vWorldNormal = normalize((modelMatrix * vec4(objectNormal, 0.0)).xyz);
vViewDir = normalize(cameraPosition - (modelMatrix * vec4(position, 1.0)).xyz);
vEnclosureUv = uv;`,
    );

    shader.fragmentShader = shader.fragmentShader.replace(
      "void main() {",
      `varying vec3 vWorldNormal;
varying vec3 vViewDir;
varying vec2 vEnclosureUv;
void main() {`,
    );

    let panelGlsl = "";
    if (hasPanels) {
      if (style === "industrial") {
        panelGlsl = `
float spandrel = smoothstep(${(mw * 0.5).toFixed(4)}, ${mw.toFixed(4)}, abs(fract(vEnclosureUv.y * ${panelRows.toFixed(1)}) - 0.5));
gl_FragColor.rgb = mix(vec3(${mc.r.toFixed(4)}, ${mc.g.toFixed(4)}, ${mc.b.toFixed(4)}), gl_FragColor.rgb, spandrel);
float vStripe = smoothstep(0.02, 0.06, abs(fract(vEnclosureUv.x * ${(panelCols * 0.25).toFixed(1)}) - 0.5));
gl_FragColor.rgb = mix(vec3(${mc.r.toFixed(4)}, ${mc.g.toFixed(4)}, ${mc.b.toFixed(4)}), gl_FragColor.rgb, mix(1.0, vStripe, 0.3));`;
      } else {
        panelGlsl = `
float mullion = smoothstep(${(mw * 0.5).toFixed(4)}, ${mw.toFixed(4)}, abs(fract(vEnclosureUv.x * ${panelCols.toFixed(1)}) - 0.5));
float spandrel = smoothstep(${(mw * 0.5).toFixed(4)}, ${mw.toFixed(4)}, abs(fract(vEnclosureUv.y * ${panelRows.toFixed(1)}) - 0.5));
float panel = mullion * spandrel;
gl_FragColor.rgb = mix(vec3(${mc.r.toFixed(4)}, ${mc.g.toFixed(4)}, ${mc.b.toFixed(4)}), gl_FragColor.rgb, panel);`;
      }
    }

    let crystallineGlsl = "";
    if (style === "crystalline") {
      crystallineGlsl = `
float facetNoise = sin(vEnclosureUv.x * 47.0) * cos(vEnclosureUv.y * 43.0) * 0.03;
gl_FragColor.rgb += vec3(${rStr}, ${gStr}, ${bStr}) * abs(facetNoise) * 2.0;`;
    }

    shader.fragmentShader = shader.fragmentShader.replace(
      "#include <dithering_fragment>",
      `#include <dithering_fragment>
float fresnel = pow(1.0 - abs(dot(normalize(vViewDir), normalize(vWorldNormal))), ${power.toFixed(2)});
gl_FragColor.rgb += vec3(${rStr}, ${gStr}, ${bStr}) * fresnel * ${intensity.toFixed(2)};${panelGlsl}${crystallineGlsl}`,
    );
  };

  return mat;
}

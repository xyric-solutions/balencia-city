import { Html, Line } from "@react-three/drei";
import type { CSSProperties } from "react";
import * as THREE from "three";
import { getStructureById } from "../../lib/assets";
import { getDistrictProfile } from "../../lib/district-metadata";
import { BRAND_COLORS } from "../../lib/materials";
import type { Vec3 } from "../../lib/types";

type RevealConfig = {
  scene: number;
  districtId: string;
  thresholdMarker: string;
  interiorMarker: string;
  session: number;
  verdict: string;
  focal: string;
  cueOffsetX?: number;
  cueOffsetY?: number;
};

const PHASE9_INTERIOR_REVEALS: RevealConfig[] = [
  {
    scene: 4,
    districtId: "fitness",
    thresholdMarker: "fitness-threshold",
    interiorMarker: "fitness-interior-midpoint",
    session: 80,
    verdict: "Inside Fitness Arena",
    focal: "Pulse floor",
    cueOffsetX: 330,
    cueOffsetY: -170,
  },
  {
    scene: 5,
    districtId: "yoga",
    thresholdMarker: "yoga-threshold",
    interiorMarker: "yoga-interior-midpoint",
    session: 80,
    verdict: "Inside Yoga Dome",
    focal: "Breath rings",
  },
  {
    scene: 6,
    districtId: "finance",
    thresholdMarker: "finance-threshold",
    interiorMarker: "finance-interior-midpoint",
    session: 80,
    verdict: "Inside Finance Advisory",
    focal: "Wealth wall",
    cueOffsetX: 180,
    cueOffsetY: -118,
  },
  {
    scene: 7,
    districtId: "knowledgebase",
    thresholdMarker: "knowledgebase-threshold",
    interiorMarker: "knowledgebase-interior-midpoint",
    session: 80,
    verdict: "Inside Knowledgebase",
    focal: "Memory archive",
  },
  {
    scene: 8,
    districtId: "chat",
    thresholdMarker: "chat-threshold",
    interiorMarker: "chat-interior-midpoint",
    session: 80,
    verdict: "Inside Communication Nexus",
    focal: "Signal threads",
    cueOffsetX: 300,
    cueOffsetY: -170,
  },
  {
    scene: 9,
    districtId: "leaderboard",
    thresholdMarker: "leaderboard-threshold",
    interiorMarker: "leaderboard-interior-midpoint",
    session: 81,
    verdict: "Inside Competition Arena",
    focal: "Live challenge floor",
    cueOffsetX: 310,
    cueOffsetY: -180,
  },
  {
    scene: 10,
    districtId: "relationships",
    thresholdMarker: "relationships-threshold",
    interiorMarker: "relationships-interior-midpoint",
    session: 81,
    verdict: "Inside Connection Gardens",
    focal: "Family dome",
    cueOffsetX: 70,
    cueOffsetY: -36,
  },
  {
    scene: 11,
    districtId: "career",
    thresholdMarker: "career-threshold",
    interiorMarker: "career-interior-midpoint",
    session: 81,
    verdict: "Inside Career Command Hub",
    focal: "Growth strategy table",
    cueOffsetX: 270,
    cueOffsetY: -165,
  },
  {
    scene: 12,
    districtId: "recovery",
    thresholdMarker: "recovery-threshold",
    interiorMarker: "recovery-interior-midpoint",
    session: 81,
    verdict: "Inside Recovery Chamber",
    focal: "Sleep brain",
    cueOffsetX: 190,
    cueOffsetY: -120,
  },
  {
    scene: 13,
    districtId: "analytics",
    thresholdMarker: "analytics-threshold",
    interiorMarker: "analytics-interior-midpoint",
    session: 81,
    verdict: "Inside Data Sanctum",
    focal: "Where SIA thinks",
    cueOffsetX: 305,
    cueOffsetY: -170,
  },
  {
    scene: 14,
    districtId: "nutrition",
    thresholdMarker: "nutrition-threshold",
    interiorMarker: "nutrition-interior-midpoint",
    session: 81,
    verdict: "Inside Nourishment Hall",
    focal: "Living market",
    cueOffsetX: 260,
    cueOffsetY: -150,
  },
];

function fade(localProgress: number, start: number, end: number) {
  return THREE.MathUtils.smoothstep(THREE.MathUtils.clamp((localProgress - start) / (end - start), 0, 1), 0, 1);
}

function planarDirection([x, , z]: Vec3) {
  const length = Math.max(Math.hypot(x, z), 0.0001);
  return new THREE.Vector3(x / length, 0, z / length);
}

function ThresholdPortal({
  color,
  marker,
  opacity,
  position,
  rotationY,
}: {
  color: string;
  marker: string;
  opacity: number;
  position: THREE.Vector3;
  rotationY: number;
}) {
  return (
    <group name={marker} position={position.toArray()} rotation={[0, rotationY, 0]}>
      <mesh position={[-1.9, 1.3, 0]}>
        <boxGeometry args={[0.18, 2.6, 0.16]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.8 * opacity} opacity={0.76 * opacity} transparent toneMapped={false} />
      </mesh>
      <mesh position={[1.9, 1.3, 0]}>
        <boxGeometry args={[0.18, 2.6, 0.16]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.8 * opacity} opacity={0.76 * opacity} transparent toneMapped={false} />
      </mesh>
      <mesh position={[0, 2.62, 0]}>
        <boxGeometry args={[4.1, 0.16, 0.16]} />
        <meshStandardMaterial color={BRAND_COLORS.energy} emissive={BRAND_COLORS.energy} emissiveIntensity={0.9 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
      </mesh>
      <mesh position={[0, 0.04, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.7, 2.05, 56]} />
        <meshBasicMaterial color={color} opacity={0.42 * opacity} transparent depthWrite={false} toneMapped={false} />
      </mesh>
    </group>
  );
}

function FitnessFocal({ color, opacity }: { color: string; opacity: number }) {
  return (
    <>
      <mesh position={[0, 0.12, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.6, 2.25, 72]} />
        <meshBasicMaterial color={color} opacity={0.58 * opacity} transparent toneMapped={false} />
      </mesh>
      {[-1.25, 1.25].map((x) => (
        <mesh key={`fitness-rig-${x}`} position={[x, 1.05, -0.4]}>
          <boxGeometry args={[0.16, 2.1, 0.16]} />
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.58 * opacity} opacity={0.7 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      <mesh position={[0, 1.8, -0.4]}>
        <boxGeometry args={[2.8, 0.12, 0.16]} />
        <meshStandardMaterial color={BRAND_COLORS.energy} emissive={BRAND_COLORS.energy} emissiveIntensity={0.58 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
      </mesh>
    </>
  );
}

function YogaFocal({ color, opacity }: { color: string; opacity: number }) {
  return (
    <>
      {[1.1, 1.75, 2.35].map((radius, index) => (
        <mesh key={`yoga-ring-${radius}`} position={[0, 1 + index * 0.34, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[radius, 0.035, 8, 72]} />
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={(0.52 - index * 0.08) * opacity} opacity={(0.7 - index * 0.12) * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      {[-1.2, 0, 1.2].map((x) => (
        <mesh key={`yoga-pod-${x}`} position={[x, 0.28, -0.7]}>
          <sphereGeometry args={[0.28, 18, 10]} />
          <meshStandardMaterial color="#D9FFF0" emissive={color} emissiveIntensity={0.3 * opacity} opacity={0.62 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
    </>
  );
}

function FinanceFocal({ color, opacity }: { color: string; opacity: number }) {
  return (
    <>
      <mesh position={[0, 1.42, -0.9]}>
        <boxGeometry args={[3.4, 1.65, 0.12]} />
        <meshStandardMaterial color="#171923" emissive={color} emissiveIntensity={0.18 * opacity} opacity={0.76 * opacity} transparent toneMapped={false} />
      </mesh>
      {[-1.1, -0.36, 0.38, 1.08].map((x, index) => (
        <mesh key={`finance-bar-${x}`} position={[x, 0.72 + index * 0.22, -0.78]}>
          <boxGeometry args={[0.28, 0.7 + index * 0.24, 0.08]} />
          <meshStandardMaterial color={index % 2 === 0 ? BRAND_COLORS.gold : color} emissive={BRAND_COLORS.gold} emissiveIntensity={0.52 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
    </>
  );
}

function KnowledgebaseFocal({ color, opacity }: { color: string; opacity: number }) {
  return (
    <>
      {[-1.4, 0, 1.4].map((x) => (
        <mesh key={`knowledge-shelf-${x}`} position={[x, 1.05, -0.7]}>
          <boxGeometry args={[0.28, 1.7, 0.18]} />
          <meshStandardMaterial color="#201B2C" emissive={color} emissiveIntensity={0.3 * opacity} opacity={0.76 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      {[-0.9, -0.2, 0.55, 1.12].map((x, index) => (
        <mesh key={`knowledge-cube-${x}`} position={[x, 1.6 + Math.sin(index) * 0.25, 0.25]}>
          <boxGeometry args={[0.38, 0.38, 0.38]} />
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.62 * opacity} opacity={0.58 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
    </>
  );
}

function ChatFocal({ color, opacity }: { color: string; opacity: number }) {
  const nodes = [
    new THREE.Vector3(-1.35, 0.9, -0.4),
    new THREE.Vector3(0, 1.75, 0.25),
    new THREE.Vector3(1.35, 0.95, -0.35),
  ];

  return (
    <>
      <Line points={nodes} color={color} lineWidth={1.2} transparent opacity={0.62 * opacity} />
      {nodes.map((position, index) => (
        <mesh key={`chat-node-${index}`} position={position.toArray()}>
          <sphereGeometry args={[0.22, 18, 12]} />
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.76 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      <mesh position={[0, 0.18, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.55, 2.15, 72]} />
        <meshBasicMaterial color={BRAND_COLORS.energy} opacity={0.38 * opacity} transparent toneMapped={false} />
      </mesh>
    </>
  );
}

function LeaderboardFocal({ color, opacity }: { color: string; opacity: number }) {
  return (
    <>
      <mesh position={[0, 0.16, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.55, 2.35, 80]} />
        <meshBasicMaterial color={color} opacity={0.5 * opacity} transparent toneMapped={false} />
      </mesh>
      {[-1.35, -0.45, 0.45, 1.35].map((x, index) => (
        <mesh key={`leaderboard-rank-${x}`} position={[x, 0.52 + index * 0.22, -0.68]}>
          <boxGeometry args={[0.34, 0.72 + index * 0.34, 0.22]} />
          <meshStandardMaterial color={index === 3 ? BRAND_COLORS.gold : color} emissive={color} emissiveIntensity={0.52 * opacity} opacity={0.74 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      {[-0.8, 0, 0.8].map((x, index) => (
        <mesh key={`leaderboard-card-${x}`} position={[x, 1.95 + index * 0.12, 0.4]} rotation={[0.16, 0, 0]}>
          <boxGeometry args={[0.64, 0.38, 0.08]} />
          <meshStandardMaterial color="#241923" emissive={BRAND_COLORS.energy} emissiveIntensity={0.34 * opacity} opacity={0.68 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
    </>
  );
}

function RelationshipsFocal({ color, opacity }: { color: string; opacity: number }) {
  const nodes = [
    new THREE.Vector3(-1.5, 0.72, -0.25),
    new THREE.Vector3(-0.42, 1.28, 0.15),
    new THREE.Vector3(0.42, 1.28, 0.15),
    new THREE.Vector3(1.5, 0.72, -0.25),
  ];

  return (
    <>
      <Line points={nodes} color={color} lineWidth={1.1} transparent opacity={0.58 * opacity} />
      <mesh position={[0, 0.85, -0.2]}>
        <sphereGeometry args={[0.86, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2]} />
        <meshStandardMaterial color="#331A27" emissive={color} emissiveIntensity={0.34 * opacity} opacity={0.48 * opacity} transparent toneMapped={false} />
      </mesh>
      {nodes.map((position, index) => (
        <mesh key={`relationship-node-${index}`} position={position.toArray()}>
          <sphereGeometry args={[0.2, 18, 12]} />
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.62 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
    </>
  );
}

function CareerFocal({ color, opacity }: { color: string; opacity: number }) {
  return (
    <>
      <mesh position={[0, 0.64, 0]}>
        <boxGeometry args={[2.8, 0.16, 1.45]} />
        <meshStandardMaterial color="#111827" emissive={color} emissiveIntensity={0.24 * opacity} opacity={0.78 * opacity} transparent toneMapped={false} />
      </mesh>
      {[-1.2, -0.4, 0.4, 1.2].map((x, index) => (
        <mesh key={`career-growth-${x}`} position={[x, 1.02 + index * 0.22, -0.72]}>
          <boxGeometry args={[0.22, 0.72 + index * 0.34, 0.2]} />
          <meshStandardMaterial color={index === 3 ? BRAND_COLORS.energy : color} emissive={color} emissiveIntensity={0.54 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      <Line
        points={[
          new THREE.Vector3(-1.2, 1.4, -0.48),
          new THREE.Vector3(-0.4, 1.78, -0.48),
          new THREE.Vector3(0.4, 2.2, -0.48),
          new THREE.Vector3(1.2, 2.62, -0.48),
        ]}
        color={BRAND_COLORS.energy}
        lineWidth={1.2}
        transparent
        opacity={0.62 * opacity}
      />
    </>
  );
}

function RecoveryFocal({ color, opacity }: { color: string; opacity: number }) {
  return (
    <>
      {[-1.2, 0, 1.2].map((x, index) => (
        <mesh key={`recovery-pod-${x}`} position={[x, 0.38, -0.15]} rotation={[0, 0, index === 1 ? 0 : x * -0.08]}>
          <capsuleGeometry args={[0.26, 1.05, 8, 20]} />
          <meshStandardMaterial color="#C7D2FE" emissive={color} emissiveIntensity={0.24 * opacity} opacity={0.54 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      <mesh position={[0, 1.72, -0.32]}>
        <sphereGeometry args={[0.58, 28, 18]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.66 * opacity} opacity={0.42 * opacity} transparent toneMapped={false} />
      </mesh>
      {[1.1, 1.65, 2.15].map((radius, index) => (
        <mesh key={`recovery-breath-${radius}`} position={[0, 1.72, -0.32]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[radius, 0.025, 8, 64]} />
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={(0.38 - index * 0.07) * opacity} opacity={(0.48 - index * 0.08) * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
    </>
  );
}

function AnalyticsFocal({ color, opacity }: { color: string; opacity: number }) {
  const nodes = [
    new THREE.Vector3(-1.35, 0.82, -0.45),
    new THREE.Vector3(-0.45, 1.68, 0.05),
    new THREE.Vector3(0.36, 1.16, -0.2),
    new THREE.Vector3(1.28, 2.08, 0.26),
  ];

  return (
    <>
      <Line points={nodes} color={color} lineWidth={1.1} transparent opacity={0.62 * opacity} />
      {nodes.map((position, index) => (
        <mesh key={`analytics-node-${index}`} position={position.toArray()}>
          <sphereGeometry args={[0.2 + index * 0.02, 18, 12]} />
          <meshStandardMaterial color={index === 3 ? BRAND_COLORS.energy : color} emissive={color} emissiveIntensity={0.68 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      <mesh position={[0, 2.52, -0.1]} rotation={[Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.15, 1.62, 72]} />
        <meshBasicMaterial color={BRAND_COLORS.gold} opacity={0.38 * opacity} transparent toneMapped={false} />
      </mesh>
      {[-1.1, -0.35, 0.4, 1.12].map((x, index) => (
        <mesh key={`analytics-chart-${x}`} position={[x, 0.42 + index * 0.18, -0.9]}>
          <boxGeometry args={[0.28, 0.54 + index * 0.24, 0.08]} />
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.42 * opacity} opacity={0.66 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
    </>
  );
}

function NutritionFocal({ color, opacity }: { color: string; opacity: number }) {
  return (
    <>
      {[-1.24, -0.42, 0.42, 1.24].map((x, index) => (
        <mesh key={`nutrition-shelf-${x}`} position={[x, 0.92, -0.78]}>
          <boxGeometry args={[0.42, 1.34, 0.18]} />
          <meshStandardMaterial color={index % 2 === 0 ? "#16351F" : "#2B2414"} emissive={color} emissiveIntensity={0.32 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
      <mesh position={[0, 0.46, 0.35]}>
        <boxGeometry args={[2.6, 0.16, 1.12]} />
        <meshStandardMaterial color="#13251A" emissive={BRAND_COLORS.gold} emissiveIntensity={0.2 * opacity} opacity={0.72 * opacity} transparent toneMapped={false} />
      </mesh>
      {[0.92, 1.52, 2.12].map((height, index) => (
        <mesh key={`nutrition-grow-light-${height}`} position={[0, height, -0.18]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[1.05 + index * 0.34, 0.028, 8, 64]} />
          <meshStandardMaterial color={index === 0 ? color : BRAND_COLORS.gold} emissive={index === 0 ? color : BRAND_COLORS.gold} emissiveIntensity={0.46 * opacity} opacity={(0.56 - index * 0.08) * opacity} transparent toneMapped={false} />
        </mesh>
      ))}
    </>
  );
}

function FocalInteriorElements({ districtId, opacity, color }: { districtId: string; opacity: number; color: string }) {
  if (districtId === "fitness") {
    return <FitnessFocal color={color} opacity={opacity} />;
  }

  if (districtId === "yoga") {
    return <YogaFocal color={color} opacity={opacity} />;
  }

  if (districtId === "finance") {
    return <FinanceFocal color={color} opacity={opacity} />;
  }

  if (districtId === "knowledgebase") {
    return <KnowledgebaseFocal color={color} opacity={opacity} />;
  }

  if (districtId === "chat") {
    return <ChatFocal color={color} opacity={opacity} />;
  }

  if (districtId === "leaderboard") {
    return <LeaderboardFocal color={color} opacity={opacity} />;
  }

  if (districtId === "relationships") {
    return <RelationshipsFocal color={color} opacity={opacity} />;
  }

  if (districtId === "career") {
    return <CareerFocal color={color} opacity={opacity} />;
  }

  if (districtId === "recovery") {
    return <RecoveryFocal color={color} opacity={opacity} />;
  }

  if (districtId === "analytics") {
    return <AnalyticsFocal color={color} opacity={opacity} />;
  }

  return <NutritionFocal color={color} opacity={opacity} />;
}

export function DistrictInteriorRevealLayer({
  localProgress,
  sceneIndex,
}: {
  localProgress: number;
  sceneIndex: number;
}) {
  const reveal = PHASE9_INTERIOR_REVEALS.find((candidate) => candidate.scene === sceneIndex);
  const structure = reveal ? getStructureById(reveal.districtId) : undefined;

  if (!reveal || !structure) {
    return null;
  }

  const profile = getDistrictProfile(reveal.districtId);
  const direction = planarDirection(structure.position);
  const tangent = new THREE.Vector3(-direction.z, 0, direction.x);
  const thresholdOffset = Math.max(profile.padSize[0], profile.padSize[1]) * 0.52 + 3.2;
  const thresholdPosition = direction.clone().multiplyScalar(thresholdOffset);
  const chamberPosition = direction.clone().multiplyScalar(0.8).add(tangent.clone().multiplyScalar(0.65));
  const cuePosition = chamberPosition.clone().add(new THREE.Vector3(tangent.x * 2.2, 3.1, tangent.z * 2.2));
  const rotationY = Math.atan2(direction.x, direction.z);
  const approachOpacity = fade(localProgress, 0.12, 0.46) * (1 - fade(localProgress, 0.76, 0.94));
  const interiorOpacity = fade(localProgress, 0.52, 0.74);
  const color = profile.motifColor;

  return (
    <group
      name="session80-interior-reveal"
      position={structure.position}
      userData={{ districtId: reveal.districtId, sceneIndex, session: reveal.session }}
    >
      <Line
        points={[
          thresholdPosition.clone().setY(0.18),
          chamberPosition.clone().setY(0.32),
        ]}
        color={BRAND_COLORS.energy}
        lineWidth={1.1}
        transparent
        opacity={0.44 * approachOpacity}
      />

      <ThresholdPortal
        color={color}
        marker={reveal.thresholdMarker}
        opacity={approachOpacity}
        position={thresholdPosition}
        rotationY={rotationY}
      />

      <group name={reveal.interiorMarker} position={chamberPosition.toArray()} rotation={[0, rotationY, 0]}>
        <mesh position={[0, 0.06, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <circleGeometry args={[3.25, 80]} />
          <meshBasicMaterial color="#070A10" opacity={0.64 * interiorOpacity} transparent depthWrite={false} />
        </mesh>
        <mesh position={[0, 0.09, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[2.45, 3.25, 80]} />
          <meshBasicMaterial color={color} opacity={0.48 * interiorOpacity} transparent toneMapped={false} />
        </mesh>
        <FocalInteriorElements color={color} districtId={reveal.districtId} opacity={interiorOpacity} />
      </group>

      <pointLight color={color} distance={13} intensity={12 * interiorOpacity} position={[chamberPosition.x, 2.1, chamberPosition.z]} />

      <Html
        center
        className="interior-reveal-cue-anchor"
        distanceFactor={20}
        occlude={false}
        position={cuePosition.toArray()}
        zIndexRange={[9, 0]}
      >
        <div
          className="interior-reveal-cue"
          data-district-id={reveal.districtId}
          data-phase9-interior-session={reveal.session}
          data-session80-scene={sceneIndex}
          data-session80-verdict={`inside-${reveal.districtId}`}
          data-session81-scene={reveal.session === 81 ? sceneIndex : undefined}
          data-session81-verdict={reveal.session === 81 ? `inside-${reveal.districtId}` : undefined}
          style={
            {
              "--district-color": color,
              "--cue-offset-x": `${reveal.cueOffsetX ?? 0}px`,
              "--cue-offset-y": `${reveal.cueOffsetY ?? 0}px`,
              "--reveal-progress": interiorOpacity,
            } as CSSProperties
          }
        >
          <span>{reveal.verdict}</span>
          <strong>{reveal.focal}</strong>
        </div>
      </Html>
    </group>
  );
}

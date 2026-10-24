import type { InvestigationPayload } from "../../api";

interface Props {
  lastRun: InvestigationPayload | null;
}

const FIXTURE_ARTIFACTS = [
  { name: "logs.jsonl", note: "telemetry_log" },
  { name: "metrics.prom", note: "telemetry_metric" },
  { name: "deploys.yaml", note: "change_deployment" },
  { name: "manifest.json", note: "context" },
];

export function PlaygroundFixtureDrawer({ lastRun }: Props) {
  const evidenceCount = lastRun?.investigation.evidence?.length ?? null;
  const state = lastRun?.state;

  return (
    <div className="playground-fixture panel">
      <div className="playground-fixture__header">
        <span className="headline-sm">Fixture inspection</span>
        <span className="chip">SPEC v1</span>
      </div>
      <p className="label-md text-muted">Loaded bundle artifacts (b03)</p>
      <ul className="playground-fixture__list">
        {FIXTURE_ARTIFACTS.map((a) => (
          <li key={a.name} className="fixture-row">
            <span className="mono">{a.name}</span>
            <span className="text-muted">{a.note}</span>
          </li>
        ))}
      </ul>
      <div className="playground-fixture__meta">
        <div className="meta-row">
          <span className="text-muted">Last run state</span>
          <span className="mono">{state ?? "—"}</span>
        </div>
        <div className="meta-row">
          <span className="text-muted">Evidence items</span>
          <span className="mono">{evidenceCount ?? "—"}</span>
        </div>
        <div className="meta-row">
          <span className="text-muted">Containment</span>
          <span className="chip chip--ok">ISOLATED_REPLAY</span>
        </div>
      </div>
    </div>
  );
}

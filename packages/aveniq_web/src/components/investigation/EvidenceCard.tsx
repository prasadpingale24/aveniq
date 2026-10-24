import { formatTime } from "../../investigation/parseInvestigation";

interface Props {
  evidence: Record<string, unknown>;
  highlighted?: boolean;
  compact?: boolean;
}

export function EvidenceCard({ evidence, highlighted, compact }: Props) {
  const prov = (evidence.provenance as Record<string, unknown>) ?? {};
  const fixturePath = prov.fixture_path ? String(prov.fixture_path) : null;

  return (
    <article
      className={`evidence-card ${highlighted ? "evidence-card--highlight" : ""}`}
      id={`evidence-${String(evidence.id)}`}
    >
      <div className="evidence-card__head">
        <span className="mono evidence-card__id">{String(evidence.id)}</span>
        <span className="chip">{String(evidence.strength)}</span>
      </div>
      <p className="evidence-card__obs">{String(evidence.observation)}</p>
      {!compact && (
        <div className="evidence-card__meta label-md text-muted">
          <span>{String(evidence.source_type)}</span>
          <span>{String(evidence.entity)}</span>
          <span>{formatTime(evidence.event_time)}</span>
        </div>
      )}
      {!compact && fixturePath && (
        <p className="mono evidence-card__fixture text-muted">{fixturePath}</p>
      )}
    </article>
  );
}

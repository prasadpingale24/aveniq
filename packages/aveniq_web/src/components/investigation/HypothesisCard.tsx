interface Props {
  hypothesis: Record<string, unknown>;
  compact?: boolean;
}

export function HypothesisCard({ hypothesis, compact }: Props) {
  const status = String(hypothesis.status ?? "unknown");
  const supporting = (hypothesis.supporting_evidence_ids as string[]) ?? [];
  const contradicting = (hypothesis.contradicting_evidence_ids as string[]) ?? [];

  return (
    <article className="hypothesis-card">
      <div className="hypothesis-card__head">
        <span className={`hypothesis-card__status hypothesis-card__status--${status}`}>
          {status}
        </span>
        <span className="mono text-muted">{String(hypothesis.id)}</span>
      </div>
      <p className="hypothesis-card__statement">{String(hypothesis.statement)}</p>
      {!compact && (
        <p className="label-md text-muted">
          +{supporting.length} supporting
          {contradicting.length > 0 ? ` · ${contradicting.length} contradicting` : ""}
        </p>
      )}
    </article>
  );
}

interface Props {
  claim: Record<string, unknown>;
  onEvidenceClick?: (id: string) => void;
}

export function RcaClaimRow({ claim, onEvidenceClick }: Props) {
  const ids = (claim.evidence_ids as string[]) ?? [];

  return (
    <div className="rca-claim">
      <p className="rca-claim__text">{String(claim.text)}</p>
      <div className="rca-claim__links">
        {ids.map((id) => (
          <button
            key={id}
            type="button"
            className="evidence-link mono"
            onClick={() => onEvidenceClick?.(id)}
          >
            {id}
          </button>
        ))}
      </div>
    </div>
  );
}

import type { PresentationProfile } from "../../api";
import { RcaClaimRow } from "./RcaClaimRow";

interface Props {
  rca: Record<string, unknown>;
  profile: PresentationProfile;
  onEvidenceClick?: (id: string) => void;
}

export function RcaPanel({ rca, profile, onEvidenceClick }: Props) {
  const claims = (rca.claims as Array<Record<string, unknown>>) ?? [];
  const chain = (rca.causal_chain as string[]) ?? [];
  const showClaims = profile === "engineer";

  return (
    <section className="inv-rca panel" aria-label="Root cause analysis">
      <div className="inv-rca__head">
        <h3 className="headline-sm">Root cause analysis</h3>
        <span className="chip chip--ok">RCA {String(rca.status)}</span>
      </div>
      {profile !== "stakeholder" && rca.summary && (
        <p className="inv-rca__summary">{String(rca.summary)}</p>
      )}
      <p className="inv-rca__root">{String(rca.root_cause)}</p>
      {profile === "engineer" && chain.length > 0 && (
        <ol className="inv-rca__chain">
          {chain.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      )}
      {showClaims && claims.length > 0 && (
        <div className="inv-rca__claims">
          <h4 className="label-md">Claims</h4>
          {claims.map((c) => (
            <RcaClaimRow key={String(c.id)} claim={c} onEvidenceClick={onEvidenceClick} />
          ))}
        </div>
      )}
    </section>
  );
}

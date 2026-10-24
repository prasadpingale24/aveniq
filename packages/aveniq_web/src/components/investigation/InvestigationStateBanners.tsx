import { isBlocked, isInconclusive, type InvBody } from "../../investigation/parseInvestigation";

interface Props {
  data: InvBody;
}

export function InvestigationStateBanners({ data }: Props) {
  const blocked = isBlocked(data);
  const inconclusive = isInconclusive(data);

  if (!blocked && !inconclusive) return null;

  return (
    <div className="inv-banners">
      {blocked && (
        <div className="inv-banner inv-banner--blocked" role="alert">
          <span className="headline-sm">Investigation blocked</span>
          <p>
            The playbook could not proceed (missing evidence, policy gate, or upstream failure). Review
            events and evidence before re-running.
          </p>
        </div>
      )}
      {inconclusive && !blocked && (
        <div className="inv-banner inv-banner--inconclusive" role="alert">
          <span className="headline-sm">Inconclusive RCA</span>
          <p>
            Evidence does not support a single probable root cause. Claims and gaps are shown where
            available; do not treat output as production-ready RCA.
          </p>
        </div>
      )}
    </div>
  );
}

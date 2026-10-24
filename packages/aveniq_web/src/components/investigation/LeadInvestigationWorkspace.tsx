import type { InvBody } from "../../investigation/parseInvestigation";
import { EvidenceCard } from "./EvidenceCard";
import { HypothesisCard } from "./HypothesisCard";
import { InvestigationStateBanners } from "./InvestigationStateBanners";
import { InvestigationStateHeader } from "./InvestigationStateHeader";
import { RcaPanel } from "./RcaPanel";
import { SignalStrip } from "./SignalStrip";

interface Props {
  data: InvBody;
}

const LEAD_EVIDENCE_TOP = 3;

export function LeadInvestigationWorkspace({ data }: Props) {
  const rca = data.rca as Record<string, unknown> | null | undefined;
  const topEvidence = data.evidence.slice(0, LEAD_EVIDENCE_TOP);

  return (
    <div className="inv-workspace inv-workspace--lead">
      <InvestigationStateBanners data={data} />
      <InvestigationStateHeader data={data} />
      <SignalStrip data={data} />

      {rca && <RcaPanel rca={rca} profile="lead" />}

      <section className="panel inv-section">
        <h3 className="headline-sm">Hypothesis summary</h3>
        {data.hypotheses.map((h) => (
          <HypothesisCard key={String(h.id)} hypothesis={h as Record<string, unknown>} compact />
        ))}
      </section>

      <section className="panel inv-section">
        <h3 className="headline-sm">
          Key evidence ({topEvidence.length} of {data.evidence.length})
        </h3>
        {topEvidence.map((e) => (
          <EvidenceCard
            key={String(e.id)}
            evidence={e as Record<string, unknown>}
            compact
          />
        ))}
      </section>
    </div>
  );
}

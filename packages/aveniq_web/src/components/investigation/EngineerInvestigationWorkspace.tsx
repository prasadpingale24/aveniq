import { useCallback, useState } from "react";
import type { InvBody } from "../../investigation/parseInvestigation";
import { EvidenceCard } from "./EvidenceCard";
import { EventTimeline } from "./EventTimeline";
import { HypothesisCard } from "./HypothesisCard";
import { InvestigationStateBanners } from "./InvestigationStateBanners";
import { InvestigationStateHeader } from "./InvestigationStateHeader";
import { RcaPanel } from "./RcaPanel";
import { SignalStrip } from "./SignalStrip";

interface Props {
  data: InvBody;
}

export function EngineerInvestigationWorkspace({ data }: Props) {
  const [highlightId, setHighlightId] = useState<string | null>(null);
  const rca = data.rca as Record<string, unknown> | null | undefined;

  const onEvidenceClick = useCallback((id: string) => {
    setHighlightId(id);
    document.getElementById(`evidence-${id}`)?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, []);

  return (
    <div className="inv-workspace inv-workspace--engineer">
      <InvestigationStateBanners data={data} />
      <InvestigationStateHeader data={data} />
      <SignalStrip data={data} />

      <div className="inv-grid inv-grid--eng">
        <div className="inv-grid__main">
          <section className="panel inv-section">
            <h3 className="headline-sm">Hypotheses</h3>
            {data.hypotheses.length === 0 ? (
              <p className="text-muted">No hypotheses yet.</p>
            ) : (
              data.hypotheses.map((h) => (
                <HypothesisCard key={String(h.id)} hypothesis={h as Record<string, unknown>} />
              ))
            )}
          </section>
          <EventTimeline data={data} />
        </div>

        <div className="inv-grid__rail">
          <section className="panel inv-section">
            <h3 className="headline-sm">Evidence ({data.evidence.length})</h3>
            {data.evidence.map((e) => (
              <EvidenceCard
                key={String(e.id)}
                evidence={e as Record<string, unknown>}
                highlighted={highlightId === String(e.id)}
              />
            ))}
          </section>
          {rca && (
            <RcaPanel rca={rca} profile="engineer" onEvidenceClick={onEvidenceClick} />
          )}
        </div>
      </div>
    </div>
  );
}

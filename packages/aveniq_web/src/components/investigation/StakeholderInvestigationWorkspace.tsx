import { invSignal, invState, type InvBody } from "../../investigation/parseInvestigation";
import { InvestigationStateBanners } from "./InvestigationStateBanners";
import { SignalStrip } from "./SignalStrip";

interface Props {
  data: InvBody;
}

export function StakeholderInvestigationWorkspace({ data }: Props) {
  const rca = data.rca as Record<string, unknown> | null | undefined;
  const signal = invSignal(data);

  return (
    <div className="inv-workspace inv-workspace--stakeholder">
      <InvestigationStateBanners data={data} />
      <SignalStrip data={data} />

      <section className="panel inv-impact">
        <h3 className="headline-sm">Impact summary</h3>
        <p>
          <strong>Service affected:</strong> {String(signal.service ?? "unknown")}
        </p>
        <p>
          <strong>What happened:</strong> {String(signal.description ?? "Under investigation")}
        </p>
        <p>
          <strong>Status:</strong>{" "}
          <span className="status-pill">{invState(data)}</span>
        </p>
        {rca ? (
          <p>
            <strong>Likely cause:</strong>{" "}
            {String(rca.summary ?? rca.root_cause ?? "Analysis in progress")}
          </p>
        ) : (
          <p className="text-muted">Root cause analysis is not available yet.</p>
        )}
        <p className="text-muted inv-impact__note">
          Business impact metrics are not included in this benchmark payload.
        </p>
      </section>
    </div>
  );
}

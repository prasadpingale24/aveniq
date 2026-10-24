import { Link } from "react-router-dom";
import type { InvestigationPayload } from "../../api";

interface Props {
  payload: InvestigationPayload;
  profile: string;
  onDismiss: () => void;
}

export function PlaygroundRunComplete({ payload, profile, onDismiss }: Props) {
  const rca = payload.investigation.rca as Record<string, unknown> | null | undefined;
  const summary = rca?.root_cause ?? rca?.summary ?? "Investigation reached terminal state.";

  return (
    <div className="playground-complete panel" role="status">
      <div className="playground-complete__header">
        <span className="headline-sm">Run complete</span>
        <span className="chip chip--ok">{payload.state}</span>
      </div>
      <p className="playground-complete__summary">{String(summary)}</p>
      <p className="text-muted mono playground-complete__id">
        {payload.investigation_id} · {payload.investigation.evidence.length} evidence ·{" "}
        {payload.investigation.hypotheses.length} hypotheses
      </p>
      <div className="playground-complete__actions">
        <Link
          className="btn btn--primary"
          to={`/investigations/${payload.investigation_id}?profile=${profile}`}
        >
          Open investigation workspace
        </Link>
        <button type="button" className="btn btn--ghost" onClick={onDismiss}>
          Stay on Playground
        </button>
      </div>
      <p className="label-md text-muted playground-complete__hint">
        M5 will flesh out the workspace; Playground keeps the runner and log here.
      </p>
    </div>
  );
}

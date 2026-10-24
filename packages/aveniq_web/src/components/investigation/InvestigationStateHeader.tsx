import { formatTime, invHeader, invId, invState, type InvBody } from "../../investigation/parseInvestigation";

interface Props {
  data: InvBody;
}

function stateClass(state: string): string {
  if (state === "rca_candidate") return "inv-state--ok";
  if (state === "blocked") return "inv-state--blocked";
  if (state === "inconclusive") return "inv-state--inconclusive";
  return "";
}

export function InvestigationStateHeader({ data }: Props) {
  const header = invHeader(data);
  const state = invState(data);
  const rca = data.rca as Record<string, unknown> | null | undefined;

  return (
    <header className="inv-state-header panel">
      <div className="inv-state-header__top">
        <span className="label-md text-muted">Investigation</span>
        <span className={`inv-state-badge ${stateClass(state)}`}>{state}</span>
        {rca?.status && (
          <span className="chip">RCA {String(rca.status)}</span>
        )}
      </div>
      <p className="mono inv-state-header__id">{invId(data)}</p>
      <div className="inv-state-header__meta label-md text-muted">
        <span>Runs {String(header.run_count ?? "—")}</span>
        <span>Updated {formatTime(header.updated_at)}</span>
        {header.incident_window && (
          <span>
            Window{" "}
            {formatTime((header.incident_window as Record<string, unknown>).start)} →{" "}
            {formatTime((header.incident_window as Record<string, unknown>).end)}
          </span>
        )}
      </div>
    </header>
  );
}

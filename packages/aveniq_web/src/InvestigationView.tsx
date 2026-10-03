import type { InvestigationPayload, PresentationProfile } from "./api";

interface Props {
  profile: PresentationProfile;
  data: InvestigationPayload["investigation"];
}

export function InvestigationView({ profile, data }: Props) {
  const inv = data.investigation;
  const rca = data.rca;
  const signal = (inv.signal as Record<string, unknown>) || {};

  if (profile === "stakeholder") {
    return (
      <div className="card">
        <h2>Impact summary</h2>
        <p><strong>Service:</strong> {String(signal.service ?? "unknown")}</p>
        <p><strong>What we know:</strong> {String(signal.description ?? "No description")}</p>
        <p><strong>Status:</strong> <span className="status-pill">{String(inv.state)}</span></p>
        {rca ? (
          <p><strong>Likely cause (summary):</strong> {String(rca.summary ?? rca.root_cause ?? "Under investigation")}</p>
        ) : (
          <p className="muted">RCA not available yet.</p>
        )}
        <p className="muted">Business impact metrics are not available in this demo scenario.</p>
      </div>
    );
  }

  if (profile === "lead") {
    return (
      <div className="card">
        <h2>Incident overview</h2>
        <p><strong>Investigation:</strong> {String(inv.id)}</p>
        <p><strong>Benchmark:</strong> {String(inv.benchmark_id)} · <span className="status-pill">{String(inv.state)}</span></p>
        <p>{String(signal.description ?? "")}</p>
        {rca && (
          <>
            <h3>RCA ({String(rca.status)})</h3>
            <p>{String(rca.root_cause)}</p>
          </>
        )}
        <p className="muted">{data.evidence.length} evidence items · {data.hypotheses.length} hypotheses</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Investigation (engineer)</h2>
      <p className="muted">Id {String(inv.id)} · state {String(inv.state)}</p>
      <h3>Evidence</h3>
      {data.evidence.map((e) => (
        <div key={String(e.id)} className="evidence-item">
          <strong>{String(e.id)}</strong> — {String(e.observation)}
          <div className="muted">{String(e.source_type)} · {String(e.strength)}</div>
        </div>
      ))}
      <h3>Hypotheses</h3>
      {data.hypotheses.map((h) => (
        <div key={String(h.id)}>
          <strong>{String(h.status)}</strong>: {String(h.statement)}
        </div>
      ))}
      {rca && (
        <>
          <h3>RCA ({String(rca.status)})</h3>
          <p>{String(rca.root_cause)}</p>
          {(rca.claims as Array<Record<string, unknown>> | undefined)?.map((c) => (
            <div key={String(c.id)} className="claim">
              {String(c.text)}
              <div className="muted">evidence: {(c.evidence_ids as string[])?.join(", ")}</div>
            </div>
          ))}
        </>
      )}
    </div>
  );
}

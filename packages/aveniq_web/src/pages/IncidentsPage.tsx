import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { listInvestigations, type InvestigationListItem } from "../api";
import { usePersona } from "../context/PersonaContext";

function formatUpdated(iso: string): string {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

export function IncidentsPage() {
  const { profile } = usePersona();
  const [rows, setRows] = useState<InvestigationListItem[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [stateFilter, setStateFilter] = useState<string>("");

  useEffect(() => {
    setLoading(true);
    setLoadError(null);
    listInvestigations({
      state: stateFilter || undefined,
      limit: 50,
    })
      .then(setRows)
      .catch((e) => setLoadError(String(e)))
      .finally(() => setLoading(false));
  }, [stateFilter]);

  const states = useMemo(() => {
    const set = new Set(rows.map((r) => r.state));
    return Array.from(set).sort();
  }, [rows]);

  return (
    <div className="page incidents-page">
      <header className="incidents-page__header">
        <div>
          <h1 className="page-title">Incidents</h1>
          <p className="page-lead text-muted">
            Investigations in scope <span className="mono">local / playground</span>
          </p>
        </div>
        <span className="label-md text-muted mono">scr-incidents-inbox-05</span>
      </header>

      <div className="incidents-toolbar panel">
        <label className="incidents-filter label-md">
          State
          <select
            className="input incidents-filter__select"
            value={stateFilter}
            onChange={(e) => setStateFilter(e.target.value)}
          >
            <option value="">All</option>
            {states.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </label>
        <Link className="btn btn--ghost" to="/playground">New from Playground</Link>
      </div>

      {loadError && (
        <div className="problem-banner panel" role="alert">
          <p className="text-critical">{loadError}</p>
        </div>
      )}

      {loading && <p className="text-muted">Loading inbox…</p>}

      {!loading && !loadError && rows.length === 0 && (
        <div className="incidents-empty panel" role="status">
          <h2 className="headline-sm">No investigations yet</h2>
          <p className="text-muted">
            Run a benchmark from Playground to create an investigation, then it will appear here.
          </p>
          <Link className="btn btn--primary" to="/playground">Go to Playground</Link>
        </div>
      )}

      {!loading && rows.length > 0 && (
        <div className="incidents-table panel">
          <table className="incidents-table__grid">
            <thead>
              <tr>
                <th>Service</th>
                <th>Signal</th>
                <th>Benchmark</th>
                <th>State</th>
                <th>Updated</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id}>
                  <td className="mono">{row.service ?? "—"}</td>
                  <td>{row.signal_description ?? "—"}</td>
                  <td className="mono">{row.benchmark_id}</td>
                  <td>
                    <span className="status-pill">{row.state}</span>
                  </td>
                  <td className="mono text-muted">{formatUpdated(row.updated_at)}</td>
                  <td>
                    <Link
                      className="link mono"
                      to={`/investigations/${row.id}?profile=${profile}`}
                    >
                      Open
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

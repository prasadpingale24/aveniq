import type { PlaygroundScenario } from "../../api";

interface Props {
  active: PlaygroundScenario | null;
  all: PlaygroundScenario[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

function statusLabel(s: PlaygroundScenario): string {
  if (s.runnable) return "Ready";
  if (s.status === "draft") return "Draft";
  return "Planned";
}

function statusClass(s: PlaygroundScenario): string {
  if (s.runnable) return "chip--ok";
  if (s.status === "draft") return "chip--warn";
  return "";
}

export function PlaygroundScenarioCard({ active, all, selectedId, onSelect }: Props) {
  const scenario = active ?? all[0] ?? null;
  if (!scenario) {
    return (
      <div className="playground-card panel">
        <p className="text-muted">No scenarios registered.</p>
      </div>
    );
  }

  const queue = all.filter((s) => s.scenario_id !== scenario.scenario_id);

  return (
    <div className="playground-card panel">
      <div className="playground-card__header">
        <span className="label-md text-muted">ACTIVE BENCHMARK TARGET</span>
        <span className="label-md text-secondary">FIXTURE CONNECTOR MODE</span>
      </div>
      <h2 className="playground-card__title mono">{scenario.title}</h2>
      {scenario.subtitle && <p className="playground-card__subtitle text-muted">{scenario.subtitle}</p>}
      <div className="playground-card__tags">
        <span className="chip">benchmark: {scenario.benchmark_id}</span>
        <span className={`chip ${statusClass(scenario)}`}>{statusLabel(scenario)}</span>
      </div>
      <p className="playground-card__desc">{scenario.description}</p>
      {all.length > 1 && (
        <div className="playground-card__queue">
          <div className="label-md text-muted playground-card__queue-label">
            <span>Scenario queue</span>
            <span>{all.length} registered</span>
          </div>
          <div className="playground-card__queue-grid">
            {all.map((s) => (
              <button
                key={s.scenario_id}
                type="button"
                className={`queue-tile ${selectedId === s.scenario_id ? "queue-tile--selected" : ""} ${
                  !s.runnable ? "queue-tile--disabled" : ""
                }`}
                onClick={() => onSelect(s.scenario_id)}
              >
                <div className="queue-tile__row">
                  <span className="mono">{s.scenario_id}</span>
                  <span className={`chip chip--sm ${statusClass(s)}`}>{statusLabel(s)}</span>
                </div>
                <span className="text-muted">{s.subtitle || s.title}</span>
              </button>
            ))}
          </div>
          {queue.length > 0 && !scenario.runnable && (
            <p className="text-muted playground-card__queue-hint">
              Only runnable scenarios can be executed. Select B03 to run an end-to-end benchmark today.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

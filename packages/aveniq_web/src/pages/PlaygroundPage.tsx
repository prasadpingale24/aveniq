import { useEffect, useState } from "react";
import { listScenarios, type PlaygroundScenario } from "../api";
import { PlaygroundDisclaimer } from "../components/playground/PlaygroundDisclaimer";
import { PlaygroundExecutionLog } from "../components/playground/PlaygroundExecutionLog";
import { PlaygroundFixtureDrawer } from "../components/playground/PlaygroundFixtureDrawer";
import { PlaygroundRunnerStepper } from "../components/playground/PlaygroundRunnerStepper";
import { PlaygroundScenarioCard } from "../components/playground/PlaygroundScenarioCard";
import { PlaygroundRunComplete } from "../components/playground/PlaygroundRunComplete";
import { usePlaygroundSession } from "../context/PlaygroundSessionContext";
import { usePersona } from "../context/PersonaContext";

export function PlaygroundPage() {
  const { profile } = usePersona();
  const [scenarios, setScenarios] = useState<PlaygroundScenario[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);

  const {
    selectedScenarioId,
    setSelectedScenarioId,
    running,
    error,
    stepIndex,
    statuses,
    logs,
    lastRun,
    completedRun,
    run,
    clearLogs,
    dismissComplete,
  } = usePlaygroundSession();

  useEffect(() => {
    listScenarios()
      .then((list) => {
        setScenarios(list);
        if (!selectedScenarioId) {
          const b03 = list.find((s) => s.scenario_id === "b03") ?? list[0];
          if (b03) setSelectedScenarioId(b03.scenario_id);
        }
      })
      .catch((e) => setLoadError(String(e)));
    // selectedScenarioId intentionally read only on mount (may be restored from session)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setSelectedScenarioId]);

  const active =
    scenarios.find((s) => s.scenario_id === (selectedScenarioId ?? "b03")) ??
    scenarios[0] ??
    null;
  const canRun = Boolean(active?.runnable);

  return (
    <div className="page playground-page">
      <header className="playground-page__breadcrumb">
        <h1 className="page-title">Benchmark runner</h1>
        <span className="label-md text-muted mono">/playground · scr-playground-01</span>
      </header>

      <PlaygroundDisclaimer />

      {loadError && <p className="text-critical">{loadError}</p>}
      {error && <p className="text-critical panel">{error}</p>}

      <div className="playground-grid">
        <div className="playground-grid__main">
          <PlaygroundScenarioCard
            active={active}
            all={scenarios}
            selectedId={selectedScenarioId}
            onSelect={setSelectedScenarioId}
          />

          <div className="playground-controls panel">
            <button
              type="button"
              className="btn btn--primary btn--run"
              disabled={running || !active || !canRun}
              onClick={() => active && run(active.scenario_id)}
            >
              {running
                ? "Running…"
                : canRun
                  ? `Run scenario (${active?.scenario_id ?? "—"})`
                  : `Not runnable (${active?.status ?? "—"})`}
            </button>
            <span className="label-md text-muted">
              Mode: deterministic playbook · one runnable benchmark today (B03)
            </span>
          </div>

          {completedRun && (
            <PlaygroundRunComplete
              payload={completedRun}
              profile={profile}
              onDismiss={dismissComplete}
            />
          )}

          <PlaygroundRunnerStepper stepIndex={stepIndex} statuses={statuses} />

          <PlaygroundExecutionLog lines={logs} onClear={clearLogs} />
        </div>

        <aside className="playground-grid__side">
          <PlaygroundFixtureDrawer lastRun={lastRun} />
        </aside>
      </div>
    </div>
  );
}

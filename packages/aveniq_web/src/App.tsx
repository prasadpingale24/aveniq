import { useEffect, useState } from "react";
import {
  type InvestigationPayload,
  type PlaygroundScenario,
  type PresentationProfile,
  listScenarios,
  runScenario,
} from "./api";
import { InvestigationView } from "./InvestigationView";

const STANDIN_LOGS_URL = import.meta.env.VITE_STANDIN_URL || "http://127.0.0.1:8081";

export default function App() {
  const [scenarios, setScenarios] = useState<PlaygroundScenario[]>([]);
  const [profile, setProfile] = useState<PresentationProfile>("engineer");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<InvestigationPayload | null>(null);
  const [phase, setPhase] = useState<string>("idle");

  useEffect(() => {
    listScenarios()
      .then(setScenarios)
      .catch((e) => setError(String(e)));
  }, []);

  async function handleRun(scenarioId: string) {
    setError(null);
    setResult(null);
    setLoading(true);
    setPhase("Triggering stand-in and running investigation…");
    try {
      const payload = await runScenario(scenarioId);
      setResult(payload);
      setPhase("Complete");
    } catch (e) {
      setError(String(e));
      setPhase("Failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>AVENIQ Playground</h1>
        <p>
          Controlled B03 scenario. Investigations use benchmark fixtures; the checkout stand-in
          emits demo logs/metrics.{" "}
          <a href={`${STANDIN_LOGS_URL}/playground/logs`} target="_blank" rel="noreferrer">
            Stand-in logs
          </a>
        </p>
      </header>

      <section className="card">
        <h2>Scenarios</h2>
        {scenarios.map((s) => (
          <div key={s.scenario_id} style={{ marginBottom: "1rem" }}>
            <strong>{s.title}</strong> ({s.scenario_id})
            <p className="muted">{s.description}</p>
            <button disabled={loading} onClick={() => handleRun(s.scenario_id)}>
              Run scenario
            </button>
          </div>
        ))}
        {phase !== "idle" && <p className="muted">{phase}</p>}
        {error && <p className="error">{error}</p>}
      </section>

      <section className="card row">
        <label>
          Persona preview{" "}
          <select
            value={profile}
            onChange={(e) => setProfile(e.target.value as PresentationProfile)}
          >
            <option value="engineer">Engineer</option>
            <option value="lead">Technical lead</option>
            <option value="stakeholder">Stakeholder</option>
          </select>
        </label>
        <span className="muted">Same investigation data; presentation only.</span>
      </section>

      {result && <InvestigationView profile={profile} data={result.investigation} />}
    </div>
  );
}

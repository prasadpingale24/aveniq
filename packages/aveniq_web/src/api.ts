const API_BASE =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "";

export type PresentationProfile = "engineer" | "lead" | "stakeholder";

export interface PlaygroundScenario {
  scenario_id: string;
  benchmark_id: string;
  title: string;
  description: string;
}

export interface InvestigationPayload {
  scenario_id: string;
  investigation_id: string;
  state: string;
  investigation: {
    investigation: Record<string, unknown>;
    evidence: Array<Record<string, unknown>>;
    hypotheses: Array<Record<string, unknown>>;
    rca?: Record<string, unknown> | null;
    events: Array<Record<string, unknown>>;
  };
}

export async function listScenarios(): Promise<PlaygroundScenario[]> {
  const res = await fetch(`${API_BASE}/api/v1/playground/scenarios`);
  if (!res.ok) throw new Error(`Failed to load scenarios (${res.status})`);
  const data = await res.json();
  return data.scenarios;
}

export async function runScenario(scenarioId: string): Promise<InvestigationPayload> {
  const res = await fetch(`${API_BASE}/api/v1/playground/scenarios/${scenarioId}/runs`, {
    method: "POST",
  });
  if (!res.ok) {
    const problem = await res.json().catch(() => ({}));
    throw new Error(problem.detail || `Run failed (${res.status})`);
  }
  return res.json();
}

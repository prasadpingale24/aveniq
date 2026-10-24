import { apiFetch } from "./api/client";

export type PresentationProfile = "engineer" | "lead" | "stakeholder";

export interface PlaygroundScenario {
  scenario_id: string;
  benchmark_id: string;
  title: string;
  description: string;
  subtitle?: string;
  runnable: boolean;
  status: "ready" | "planned" | "draft" | string;
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
  const data = await apiFetch<{ scenarios: PlaygroundScenario[] }>("/api/v1/playground/scenarios");
  return data.scenarios;
}

export async function runScenario(scenarioId: string): Promise<InvestigationPayload> {
  return apiFetch<InvestigationPayload>(`/api/v1/playground/scenarios/${scenarioId}/runs`, {
    method: "POST",
  });
}

export interface InvestigationListItem {
  id: string;
  benchmark_id: string;
  state: string;
  created_at: string;
  updated_at: string;
  org_id?: string | null;
  environment_id?: string | null;
  service?: string | null;
  signal_description?: string | null;
}

export async function listInvestigations(params?: {
  state?: string;
  limit?: number;
  offset?: number;
}): Promise<InvestigationListItem[]> {
  const search = new URLSearchParams();
  if (params?.state) search.set("state", params.state);
  if (params?.limit != null) search.set("limit", String(params.limit));
  if (params?.offset != null) search.set("offset", String(params.offset));
  const qs = search.toString();
  const data = await apiFetch<{ investigations: InvestigationListItem[] }>(
    `/api/v1/investigations${qs ? `?${qs}` : ""}`,
  );
  return data.investigations;
}

export async function getInvestigation(investigationId: string): Promise<InvestigationPayload> {
  const investigation = await apiFetch<InvestigationPayload["investigation"]>(
    `/api/v1/investigations/${investigationId}`,
  );
  return {
    scenario_id: "",
    investigation_id: investigationId,
    state: (investigation.investigation as Record<string, unknown>)?.state as string ?? "",
    investigation,
  };
}

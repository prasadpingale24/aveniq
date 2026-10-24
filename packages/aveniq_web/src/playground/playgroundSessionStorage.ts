import type { InvestigationPayload } from "../api";
import type { LogLine, StepStatus } from "./runPhases";
import { initialLogLines, PLAYGROUND_PIPELINE } from "./runPhases";

const STORAGE_KEY = "aveniq.playground.session.v1";

export interface PlaygroundSessionSnapshot {
  selectedScenarioId: string | null;
  stepIndex: number;
  statuses: StepStatus[];
  logs: LogLine[];
  lastRun: InvestigationPayload | null;
  completedRun: InvestigationPayload | null;
  error: string | null;
}

function idleStatuses(): StepStatus[] {
  return PLAYGROUND_PIPELINE.map(() => "pending");
}

export function emptyPlaygroundSession(): PlaygroundSessionSnapshot {
  return {
    selectedScenarioId: null,
    stepIndex: -1,
    statuses: idleStatuses(),
    logs: initialLogLines(),
    lastRun: null,
    completedRun: null,
    error: null,
  };
}

export function loadPlaygroundSession(): PlaygroundSessionSnapshot | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as PlaygroundSessionSnapshot;
    if (!parsed || !Array.isArray(parsed.logs) || !Array.isArray(parsed.statuses)) {
      return null;
    }
    return parsed;
  } catch {
    return null;
  }
}

export function savePlaygroundSession(snapshot: PlaygroundSessionSnapshot): void {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot));
  } catch {
    // quota or private mode — context state still works for in-tab navigation
  }
}

export function clearPlaygroundSessionStorage(): void {
  sessionStorage.removeItem(STORAGE_KEY);
}

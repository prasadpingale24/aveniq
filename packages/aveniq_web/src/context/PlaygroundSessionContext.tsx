import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { runScenario, type InvestigationPayload } from "../api";
import {
  emptyPlaygroundSession,
  loadPlaygroundSession,
  savePlaygroundSession,
  type PlaygroundSessionSnapshot,
} from "../playground/playgroundSessionStorage";
import {
  initialLogLines,
  logForStep,
  logsFromInvestigationEvents,
  PLAYGROUND_PIPELINE,
  type LogLine,
  type StepStatus,
} from "../playground/runPhases";

const STEP_DWELL_MS = 550;

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function idleStatuses(): StepStatus[] {
  return PLAYGROUND_PIPELINE.map(() => "pending");
}

interface PlaygroundSessionContextValue {
  selectedScenarioId: string | null;
  setSelectedScenarioId: (id: string) => void;
  running: boolean;
  error: string | null;
  stepIndex: number;
  statuses: StepStatus[];
  logs: LogLine[];
  lastRun: InvestigationPayload | null;
  completedRun: InvestigationPayload | null;
  run: (scenarioId: string) => Promise<void>;
  clearLogs: () => void;
  dismissComplete: () => void;
}

const PlaygroundSessionContext = createContext<PlaygroundSessionContextValue | null>(null);

export function PlaygroundSessionProvider({ children }: { children: ReactNode }) {
  const hydrated = useRef(loadPlaygroundSession());
  const [selectedScenarioId, setSelectedScenarioIdState] = useState<string | null>(
    () => hydrated.current?.selectedScenarioId ?? null,
  );
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(() => hydrated.current?.error ?? null);
  const [stepIndex, setStepIndex] = useState(() => hydrated.current?.stepIndex ?? -1);
  const [statuses, setStatuses] = useState<StepStatus[]>(
    () => hydrated.current?.statuses ?? idleStatuses(),
  );
  const [logs, setLogs] = useState<LogLine[]>(() => hydrated.current?.logs ?? initialLogLines());
  const [lastRun, setLastRun] = useState<InvestigationPayload | null>(
    () => hydrated.current?.lastRun ?? null,
  );
  const [completedRun, setCompletedRun] = useState<InvestigationPayload | null>(
    () => hydrated.current?.completedRun ?? null,
  );

  const persist = useCallback(
    (patch: Partial<PlaygroundSessionSnapshot>) => {
      const snapshot: PlaygroundSessionSnapshot = {
        selectedScenarioId,
        stepIndex,
        statuses,
        logs,
        lastRun,
        completedRun,
        error,
        ...patch,
      };
      savePlaygroundSession(snapshot);
    },
    [selectedScenarioId, stepIndex, statuses, logs, lastRun, completedRun, error],
  );

  useEffect(() => {
    persist({});
  }, [selectedScenarioId, stepIndex, statuses, logs, lastRun, completedRun, error, persist]);

  const setSelectedScenarioId = useCallback((id: string) => {
    setSelectedScenarioIdState(id);
  }, []);

  const setStep = useCallback((index: number, status: StepStatus) => {
    setStepIndex(index);
    setStatuses((prev) => {
      const next = [...prev];
      for (let i = 0; i < index; i++) next[i] = "completed";
      next[index] = status;
      for (let i = index + 1; i < next.length; i++) next[i] = "pending";
      return next;
    });
  }, []);

  const appendLogs = useCallback((entries: LogLine[]) => {
    setLogs((prev) => [...prev, ...entries]);
  }, []);

  const run = useCallback(
    async (scenarioId: string) => {
      setError(null);
      setLastRun(null);
      setCompletedRun(null);
      setRunning(true);
      setLogs(initialLogLines());
      setStatuses(idleStatuses());
      setSelectedScenarioIdState(scenarioId);
      try {
        setStep(0, "active");
        appendLogs(logForStep("standin"));

        const apiPromise = runScenario(scenarioId);

        await delay(STEP_DWELL_MS);
        setStep(0, "completed");
        setStep(1, "active");
        appendLogs(logForStep("investigate"));

        const payload = await apiPromise;
        await delay(STEP_DWELL_MS);

        setStep(1, "completed");
        setStep(2, "active");
        appendLogs(logForStep("hypotheses"));
        appendLogs(logsFromInvestigationEvents(payload.investigation.events ?? []));
        await delay(STEP_DWELL_MS);

        setStep(2, "completed");
        setStep(3, "active");
        appendLogs(logForStep("rca"));
        await delay(STEP_DWELL_MS);

        appendLogs([
          {
            ts: new Date().toISOString().slice(11, 23),
            tag: "DONE",
            message: `Investigation ${payload.investigation_id} · state ${payload.state}`,
            tone: "ok",
          },
        ]);
        setStep(3, "completed");
        setLastRun(payload);
        setCompletedRun(payload);
      } catch (e) {
        setStatuses((prev) => {
          const next = [...prev];
          const failedAt = next.findIndex((s) => s === "active");
          const idx = failedAt >= 0 ? failedAt : 1;
          next[idx] = "failed";
          return next;
        });
        setError(String(e));
        appendLogs([
          {
            ts: new Date().toISOString().slice(11, 23),
            tag: "ERROR",
            message: String(e),
            tone: "warn",
          },
        ]);
      } finally {
        setRunning(false);
      }
    },
    [appendLogs, setStep],
  );

  const clearLogs = useCallback(() => {
    const fresh = emptyPlaygroundSession();
    setLogs(fresh.logs);
    setCompletedRun(null);
    setLastRun(null);
    setStepIndex(fresh.stepIndex);
    setStatuses(fresh.statuses);
    setError(null);
  }, []);

  const dismissComplete = useCallback(() => setCompletedRun(null), []);

  const value = useMemo(
    () => ({
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
    }),
    [
      selectedScenarioId,
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
      setSelectedScenarioId,
    ],
  );

  return (
    <PlaygroundSessionContext.Provider value={value}>{children}</PlaygroundSessionContext.Provider>
  );
}

export function usePlaygroundSession(): PlaygroundSessionContextValue {
  const ctx = useContext(PlaygroundSessionContext);
  if (!ctx) {
    throw new Error("usePlaygroundSession must be used within PlaygroundSessionProvider");
  }
  return ctx;
}

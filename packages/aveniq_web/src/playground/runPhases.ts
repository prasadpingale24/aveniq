export type StepStatus = "pending" | "active" | "completed" | "failed";

export interface PipelineStep {
  id: string;
  title: string;
  detailIdle: string;
  detailActive?: string;
}

export const PLAYGROUND_PIPELINE: PipelineStep[] = [
  {
    id: "standin",
    title: "Trigger stand-in telemetry",
    detailIdle: "Reset checkout stand-in and emit demo alert signal",
    detailActive: "POST stand-in /playground/reset + trigger",
  },
  {
    id: "investigate",
    title: "Run investigation playbook",
    detailIdle: "Create investigation and execute B03 deterministic playbook",
    detailActive: "Fixture connectors + investigator-b03",
  },
  {
    id: "hypotheses",
    title: "Evaluate hypotheses",
    detailIdle: "Hypothesis formation from correlated evidence",
    detailActive: "Recording hypothesis status on aggregate",
  },
  {
    id: "rca",
    title: "Synthesize evidence-backed RCA",
    detailIdle: "Publish RCA claims linked to evidence ids",
    detailActive: "Writing RCA to investigation store",
  },
];

export interface LogLine {
  ts: string;
  tag: string;
  message: string;
  tone?: "default" | "warn" | "ok" | "active";
}

function tsNow(): string {
  return new Date().toISOString().slice(11, 23);
}

export function initialLogLines(): LogLine[] {
  return [
    {
      ts: tsNow(),
      tag: "PLAYGROUND",
      message: "Awaiting scenario run. Investigation RCA uses fixture package b03.",
      tone: "default",
    },
  ];
}

export function logsFromInvestigationEvents(
  events: Array<Record<string, unknown>>,
  max = 8,
): LogLine[] {
  const ts = tsNow();
  return events.slice(-max).map((ev) => {
    const type = String(ev.type ?? "event");
    const tag = type.split(".").pop()?.toUpperCase() ?? "EVENT";
    const payload = ev.payload as Record<string, unknown> | undefined;
    const detail =
      payload && typeof payload.statement === "string"
        ? payload.statement
        : payload && typeof payload.root_cause === "string"
          ? payload.root_cause
          : type;
    return {
      ts,
      tag,
      message: String(detail).slice(0, 160),
      tone: type.includes("error") ? "warn" : type.includes("rca") ? "ok" : "default",
    };
  });
}

export function logForStep(stepId: string): LogLine[] {
  const ts = tsNow();
  switch (stepId) {
    case "standin":
      return [
        {
          ts,
          tag: "STANDIN",
          message: "Reset stand-in service and trigger B03 checkout-api alert path",
          tone: "active",
        },
      ];
    case "investigate":
      return [
        {
          ts,
          tag: "API",
          message: "POST /api/v1/playground/scenarios/b03/runs",
          tone: "active",
        },
      ];
    case "hypotheses":
      return [
        {
          ts,
          tag: "PLAYBOOK",
          message: "Playbook emitted hypothesis.created / hypothesis.updated events",
          tone: "default",
        },
      ];
    case "rca":
      return [
        {
          ts,
          tag: "PLAYBOOK",
          message: "Publishing rca.published and investigation.completed",
          tone: "default",
        },
      ];
    default:
      return [];
  }
}

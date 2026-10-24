import type { StepStatus } from "../../playground/runPhases";
import { PLAYGROUND_PIPELINE } from "../../playground/runPhases";

interface Props {
  stepIndex: number;
  statuses: StepStatus[];
}

export function PlaygroundRunnerStepper({ stepIndex, statuses }: Props) {
  const activeLabel = stepIndex >= 0 ? `STAGE ${stepIndex + 1} OF ${PLAYGROUND_PIPELINE.length}` : "IDLE";

  return (
    <div className="playground-stepper panel">
      <div className="playground-stepper__header">
        <span className="headline-sm">Causal replay pipeline</span>
        <span className="label-md text-muted">{activeLabel}</span>
      </div>
      <div className="playground-stepper__grid">
        {PLAYGROUND_PIPELINE.map((step, i) => {
          const status = statuses[i] ?? "pending";
          return (
            <div key={step.id} className={`step-card step-card--${status}`}>
              <div className="step-card__top">
                <span className="label-md text-muted">STAGE {String(i + 1).padStart(2, "0")}</span>
                <span className={`step-badge step-badge--${status}`}>{status}</span>
              </div>
              <div className="step-card__title">{step.title}</div>
              <p className="step-card__detail">
                {status === "active" ? step.detailActive ?? step.detailIdle : step.detailIdle}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

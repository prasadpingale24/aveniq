import type { LogLine } from "../../playground/runPhases";

interface Props {
  lines: LogLine[];
  onClear: () => void;
}

export function PlaygroundExecutionLog({ lines, onClear }: Props) {
  return (
    <div className="playground-log panel">
      <div className="playground-log__header">
        <span className="label-md">Execution log</span>
        <button type="button" className="btn btn--ghost" onClick={onClear}>
          Clear
        </button>
      </div>
      <div className="playground-log__well mono">
        {lines.map((line, i) => (
          <div key={i} className={`log-line log-line--${line.tone ?? "default"}`}>
            <span className="log-line__ts">{line.ts}</span>
            <span className="log-line__tag">[{line.tag}]</span>
            <span className="log-line__msg">{line.message}</span>
          </div>
        ))}
      </div>
      <div className="playground-log__footer label-md text-muted">
        {lines.length} event{lines.length === 1 ? "" : "s"} · STREAM: FIXTURE_STDOUT
      </div>
    </div>
  );
}

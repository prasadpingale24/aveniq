import { formatTime, invBenchmark, invSignal, type InvBody } from "../../investigation/parseInvestigation";

interface Props {
  data: InvBody;
}

export function SignalStrip({ data }: Props) {
  const signal = invSignal(data);
  const service = String(signal.service ?? "unknown service");
  const description = String(signal.description ?? "No signal description");
  const kind = String(signal.kind ?? "signal");
  const firedAt = formatTime(signal.fired_at);

  return (
    <section className="inv-signal panel" aria-label="Alert signal">
      <div className="inv-signal__row">
        <span className="label-md text-muted">Signal</span>
        <span className="chip">{kind}</span>
        <span className="chip">benchmark {invBenchmark(data)}</span>
      </div>
      <h2 className="inv-signal__service mono">{service}</h2>
      <p className="inv-signal__desc">{description}</p>
      <p className="label-md text-muted">Fired {firedAt}</p>
    </section>
  );
}

export function PlaygroundDisclaimer() {
  return (
    <div className="playground-disclaimer" role="note">
      <span className="playground-disclaimer__icon" aria-hidden>!</span>
      <div>
        <div className="playground-disclaimer__title">Operational boundary</div>
        <p className="playground-disclaimer__body">
          Stand-in demo telemetry is for sandbox runs. Investigation RCA uses the{" "}
          <strong>b03</strong> fixture bundle (deterministic replay). Live Prometheus/Datadog
          connectors are not used in this environment.
        </p>
      </div>
    </div>
  );
}

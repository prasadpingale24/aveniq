import { formatTime, type InvBody } from "../../investigation/parseInvestigation";

interface Props {
  data: InvBody;
  maxItems?: number;
}

export function EventTimeline({ data, maxItems }: Props) {
  const events = [...(data.events ?? [])].sort((a, b) => Number(a.seq) - Number(b.seq));
  const slice = maxItems ? events.slice(-maxItems) : events;

  return (
    <section className="inv-timeline panel" aria-label="Investigation timeline">
      <h3 className="headline-sm">Timeline</h3>
      {slice.length === 0 ? (
        <p className="text-muted">No events recorded.</p>
      ) : (
        <ol className="inv-timeline__list">
          {slice.map((ev) => (
            <li key={ev.seq} className="inv-timeline__item">
              <span className="inv-timeline__time mono">{formatTime(ev.occurred_at)}</span>
              <span className="inv-timeline__type mono">{String(ev.type)}</span>
              {ev.actor && (
                <span className="text-muted">
                  {String(ev.actor.kind)}:{String(ev.actor.id)}
                </span>
              )}
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}

export function InvestigationLoadingState() {
  return (
    <div className="inv-loading page" aria-busy="true" aria-label="Loading investigation">
      <div className="inv-skeleton inv-skeleton--header" />
      <div className="inv-skeleton inv-skeleton--signal" />
      <div className="inv-grid inv-grid--eng">
        <div className="inv-skeleton inv-skeleton--tall" />
        <div className="inv-skeleton inv-skeleton--tall" />
      </div>
      <p className="text-muted label-md">Loading investigation…</p>
    </div>
  );
}

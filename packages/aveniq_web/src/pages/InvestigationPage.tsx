import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getInvestigation, type InvestigationPayload } from "../api";
import { InvestigationLoadingState } from "../components/investigation/InvestigationLoadingState";
import { InvestigationWorkspace } from "../components/investigation/InvestigationWorkspace";
import { usePersona } from "../context/PersonaContext";

export function InvestigationPage() {
  const { id } = useParams<{ id: string }>();
  const { profile } = usePersona();
  const [data, setData] = useState<InvestigationPayload["investigation"] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    getInvestigation(id)
      .then((payload) => setData(payload.investigation))
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [id]);

  if (!id) {
    return <p className="text-muted">Missing investigation id.</p>;
  }

  if (loading) {
    return (
      <div className={`page investigation-page investigation-page--${profile}`}>
        <InvestigationLoadingState />
      </div>
    );
  }

  if (error) {
    return (
      <div className={`page investigation-page investigation-page--${profile}`}>
        <div className="problem-banner panel" role="alert">
          <span className="headline-sm">Could not load investigation</span>
          <p className="text-critical">{error}</p>
          <Link className="link" to="/playground">← Back to Playground</Link>
        </div>
      </div>
    );
  }

  if (!data) {
    return <p className="text-muted">Investigation not found.</p>;
  }

  return (
    <div className={`page investigation-page investigation-page--${profile}`}>
      <div className="investigation-page__toolbar">
        <Link className="investigation-back link label-md" to="/playground">
          ← Back to Playground
        </Link>
        <span className="label-md text-muted mono">
          scr-investigation-{profile === "stakeholder" ? "stake-04" : profile === "lead" ? "lead-03" : "eng-02"}
        </span>
      </div>
      <InvestigationWorkspace profile={profile} data={data} />
    </div>
  );
}

import type { PresentationProfile } from "../api";
import { usePersona } from "../context/PersonaContext";

const OPTIONS: { value: PresentationProfile; label: string }[] = [
  { value: "engineer", label: "ENG" },
  { value: "lead", label: "LEAD" },
  { value: "stakeholder", label: "STAKEHOLDER" },
];

export function PersonaToggle() {
  const { profile, setProfile } = usePersona();

  return (
    <div className="persona-toggle" role="group" aria-label="Presentation profile">
      {OPTIONS.map((opt) => (
        <button
          key={opt.value}
          type="button"
          className={`persona-toggle__btn ${profile === opt.value ? "persona-toggle__btn--active" : ""}`}
          onClick={() => setProfile(opt.value)}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}

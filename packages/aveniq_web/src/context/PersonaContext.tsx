import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  type ReactNode,
} from "react";
import { useSearchParams } from "react-router-dom";
import type { PresentationProfile } from "../api";

const PROFILE_PARAM = "profile";
const VALID: PresentationProfile[] = ["engineer", "lead", "stakeholder"];

function parseProfile(value: string | null): PresentationProfile {
  if (value && VALID.includes(value as PresentationProfile)) {
    return value as PresentationProfile;
  }
  return "engineer";
}

interface PersonaContextValue {
  profile: PresentationProfile;
  setProfile: (p: PresentationProfile) => void;
}

const PersonaContext = createContext<PersonaContextValue | null>(null);

export function PersonaProvider({ children }: { children: ReactNode }) {
  const [searchParams, setSearchParams] = useSearchParams();

  const profile = parseProfile(searchParams.get(PROFILE_PARAM));

  const setProfile = useCallback(
    (next: PresentationProfile) => {
      const nextParams = new URLSearchParams(searchParams);
      nextParams.set(PROFILE_PARAM, next);
      setSearchParams(nextParams, { replace: true });
    },
    [searchParams, setSearchParams],
  );

  const value = useMemo(() => ({ profile, setProfile }), [profile, setProfile]);

  return <PersonaContext.Provider value={value}>{children}</PersonaContext.Provider>;
}

export function usePersona(): PersonaContextValue {
  const ctx = useContext(PersonaContext);
  if (!ctx) {
    throw new Error("usePersona must be used within PersonaProvider");
  }
  return ctx;
}

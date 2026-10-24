import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { PersonaToggle } from "./PersonaToggle";

const ENV_LABEL = import.meta.env.VITE_AVENIQ_ENV || "local";

export function AppShell() {
  const { authRequired, user, logout } = useAuth();

  return (
    <div className="app-shell">
      <header className="app-shell__top">
        <div className="app-shell__brand">
          <span className="app-shell__logo">AVENIQ</span>
          <span className="env-badge">{ENV_LABEL}</span>
        </div>
        <div className="app-shell__top-actions">
          <PersonaToggle />
          {authRequired && user?.authenticated && (
            <span className="app-shell__user mono">
              {user.display_name || user.user_id}
              <button type="button" className="btn btn--ghost" onClick={() => logout()}>
                Sign out
              </button>
            </span>
          )}
        </div>
      </header>
      <aside className="app-shell__nav" aria-label="Primary">
        <NavLink
          to="/playground"
          className={({ isActive }) =>
            `app-shell__nav-item ${isActive ? "app-shell__nav-item--active" : ""}`
          }
          title="Playground"
        >
          <span className="app-shell__nav-icon" aria-hidden>▶</span>
          <span className="app-shell__nav-label">Play</span>
        </NavLink>
        <NavLink
          to="/incidents"
          className={({ isActive }) =>
            `app-shell__nav-item ${isActive ? "app-shell__nav-item--active" : ""}`
          }
          title="Incidents"
        >
          <span className="app-shell__nav-icon" aria-hidden>☰</span>
          <span className="app-shell__nav-label">Inc</span>
        </NavLink>
      </aside>
      <main className="app-shell__main">
        <Outlet />
      </main>
    </div>
  );
}

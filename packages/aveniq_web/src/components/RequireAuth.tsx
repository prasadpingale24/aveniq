import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function RequireAuth() {
  const { loading, authRequired, user } = useAuth();
  const location = useLocation();

  if (loading) {
    return <div className="login-page"><p className="text-muted">Loading…</p></div>;
  }

  if (authRequired && !user?.authenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <Outlet />;
}

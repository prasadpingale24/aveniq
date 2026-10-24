import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { RequireAuth } from "./components/RequireAuth";
import { AuthProvider } from "./context/AuthContext";
import { PersonaProvider } from "./context/PersonaContext";
import { PlaygroundSessionProvider } from "./context/PlaygroundSessionContext";
import { IncidentsPage } from "./pages/IncidentsPage";
import { InvestigationPage } from "./pages/InvestigationPage";
import { LoginPage } from "./pages/LoginPage";
import { PlaygroundPage } from "./pages/PlaygroundPage";

export default function App() {
  return (
    <AuthProvider>
      <PersonaProvider>
        <PlaygroundSessionProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<RequireAuth />}>
            <Route element={<AppShell />}>
              <Route path="/" element={<Navigate to="/playground" replace />} />
              <Route path="/playground" element={<PlaygroundPage />} />
              <Route path="/incidents" element={<IncidentsPage />} />
              <Route path="/investigations/:id" element={<InvestigationPage />} />
            </Route>
          </Route>
        </Routes>
        </PlaygroundSessionProvider>
      </PersonaProvider>
    </AuthProvider>
  );
}

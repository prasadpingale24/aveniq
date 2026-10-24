import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  fetchAuthConfig,
  fetchAuthMe,
  login as apiLogin,
  logout as apiLogout,
  type AuthUser,
} from "../auth/api";

interface AuthContextValue {
  loading: boolean;
  authRequired: boolean;
  user: AuthUser | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [loading, setLoading] = useState(true);
  const [authRequired, setAuthRequired] = useState(false);
  const [user, setUser] = useState<AuthUser | null>(null);

  const refresh = useCallback(async () => {
    const config = await fetchAuthConfig();
    setAuthRequired(config.enabled);
    if (!config.enabled) {
      setUser({ authenticated: false, user_id: null, display_name: null });
      return;
    }
    const me = await fetchAuthMe();
    setUser(me);
  }, []);

  useEffect(() => {
    refresh()
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, [refresh]);

  const login = useCallback(
    async (username: string, password: string) => {
      const me = await apiLogin(username, password);
      setUser(me);
    },
    [],
  );

  const logout = useCallback(async () => {
    await apiLogout();
    setUser({ authenticated: false, user_id: null, display_name: null });
  }, []);

  const value = useMemo(
    () => ({ loading, authRequired, user, login, logout, refresh }),
    [loading, authRequired, user, login, logout, refresh],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}

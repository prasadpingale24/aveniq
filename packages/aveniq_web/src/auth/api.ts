import { apiFetch } from "../api/client";

export interface AuthConfig {
  enabled: boolean;
  dev_login: boolean;
}

export interface AuthUser {
  authenticated: boolean;
  user_id: string | null;
  display_name: string | null;
}

export async function fetchAuthConfig(): Promise<AuthConfig> {
  return apiFetch<AuthConfig>("/api/v1/auth/config");
}

export async function fetchAuthMe(): Promise<AuthUser> {
  return apiFetch<AuthUser>("/api/v1/auth/me");
}

export async function login(username: string, password: string): Promise<AuthUser> {
  return apiFetch<AuthUser>("/api/v1/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
}

export async function logout(): Promise<void> {
  await apiFetch<void>("/api/v1/auth/logout", { method: "POST" });
}

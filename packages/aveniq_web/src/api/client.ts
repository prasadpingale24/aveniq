const API_BASE = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    credentials: "include",
  });
  if (!res.ok) {
    const problem = await res.json().catch(() => ({}));
    const detail = problem.detail || problem.title || `Request failed (${res.status})`;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  if (res.status === 204) {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}

import type { InvestigationPayload } from "../api";

export type InvBody = InvestigationPayload["investigation"];

export function invHeader(data: InvBody): Record<string, unknown> {
  return data.investigation as Record<string, unknown>;
}

export function invSignal(data: InvBody): Record<string, unknown> {
  return (invHeader(data).signal as Record<string, unknown>) ?? {};
}

export function invState(data: InvBody): string {
  return String(invHeader(data).state ?? "");
}

export function invBenchmark(data: InvBody): string {
  return String(invHeader(data).benchmark_id ?? "");
}

export function invId(data: InvBody): string {
  return String(invHeader(data).id ?? "");
}

export function formatTime(iso: unknown): string {
  if (!iso) return "—";
  try {
    return new Date(String(iso)).toISOString().replace("T", " ").slice(0, 19) + "Z";
  } catch {
    return String(iso);
  }
}

export function isBlocked(data: InvBody): boolean {
  return invState(data) === "blocked";
}

export function isInconclusive(data: InvBody): boolean {
  const state = invState(data);
  if (state === "inconclusive") return true;
  const rca = data.rca as Record<string, unknown> | null | undefined;
  return rca?.status === "inconclusive";
}

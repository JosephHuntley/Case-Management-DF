import type { SelectOption } from "./types"

export function formatTimestamp(iso: string): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  const date = d.toISOString().slice(0, 10)
  const time = d.toTimeString().slice(0, 5)
  return `${date} · ${time}`
}

export function shortHash(hash: string): string {
  if (hash === "genesis" || hash.length <= 8) return hash
  return hash.slice(0, 8)
}

// Normalizes whatever shape the API returns into { id, label } for the dropdowns.
export function normalizeOption(raw: Record<string, unknown>): SelectOption {
  const id = String(raw.id ?? raw.caseId ?? raw.evidenceId ?? "")
  const label = String(
    raw.label ?? raw.caseNumber ?? raw.title ?? raw.description ?? raw.name ?? id
  )
  return { id, label }
}

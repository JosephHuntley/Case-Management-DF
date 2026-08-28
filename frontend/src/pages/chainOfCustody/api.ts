import type { CustodyEntry, CustodyLogResponse, SelectOption } from "./types"
import { normalizeOption } from "./utils"

// Adjust these if your actual backend routes differ.
const CASES_ENDPOINT = "/api/cases/"
const CASE_EVIDENCE_ENDPOINT = (caseId: string) => `/api/evidence-items/case/${caseId}`
const CUSTODY_BY_CHAIN_ENDPOINT = (chainId: string) => `/api/chain-of-custody/${chainId}`
const CUSTODY_BY_EVIDENCE_ENDPOINT = (evidenceId: string) =>
  `/api/chain-of-custody/evidence/${evidenceId}`

function authHeaders(token: string | null): HeadersInit {
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function fetchJson<T>(
  url: string,
  token: string | null,
  errorLabel: string,
  notFoundMessage?: string
): Promise<T> {
  const res = await fetch(url, {
    headers: authHeaders(token),
    credentials: "include",
  })
  if (!res.ok) {
    if (res.status === 404 && notFoundMessage) throw new Error(notFoundMessage)
    throw new Error(`${errorLabel} (${res.status})`)
  }
  return res.json()
}

export async function fetchCustodyLog(
  ids: { chainId?: string; evidenceId?: string },
  token: string | null
): Promise<{ entries: CustodyEntry[]; itemLabel: string; caseLabel: string }> {
  const url = ids.chainId
    ? CUSTODY_BY_CHAIN_ENDPOINT(ids.chainId)
    : CUSTODY_BY_EVIDENCE_ENDPOINT(ids.evidenceId as string)

  const data = await fetchJson<CustodyLogResponse | CustodyEntry[]>(
    url,
    token,
    "Failed to load chain of custody",
    "This chain of custody could not be found."
  )

  return {
    entries: Array.isArray(data) ? data : data.entries ?? [],
    itemLabel: Array.isArray(data) ? "" : data.itemLabel ?? "",
    caseLabel: Array.isArray(data) ? "" : data.caseLabel ?? "",
  }
}

export async function fetchCases(token: string | null): Promise<SelectOption[]> {
  const data = await fetchJson<any>(CASES_ENDPOINT, token, "Failed to load cases")
  const list = Array.isArray(data) ? data : data.cases ?? []
  return list.map(normalizeOption)
}

export async function fetchEvidenceForCase(
  caseId: string,
  token: string | null
): Promise<SelectOption[]> {
  const data = await fetchJson<any>(
    CASE_EVIDENCE_ENDPOINT(caseId),
    token,
    "Failed to load evidence"
  )
  const list = Array.isArray(data) ? data : data.evidence ?? []
  return list.map(normalizeOption)
}

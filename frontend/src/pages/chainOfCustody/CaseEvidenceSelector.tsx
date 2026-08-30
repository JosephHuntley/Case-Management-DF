import { useEffect, useState } from "react"
import { useAuth } from "../../context/AuthContext"
import { fetchCases, fetchEvidenceForCase } from "./api"
import type { SelectOption } from "./types"

interface CaseEvidenceSelectorProps {
  onViewChain: (evidenceId: string) => void
}

function CaseEvidenceSelector({ onViewChain }: CaseEvidenceSelectorProps) {
  const { getAccessToken } = useAuth()

  const [cases, setCases] = useState<SelectOption[]>([])
  const [casesLoading, setCasesLoading] = useState<boolean>(true)
  const [casesError, setCasesError] = useState<string | null>(null)
  const [selectedCaseId, setSelectedCaseId] = useState<string>("")

  const [evidenceOptions, setEvidenceOptions] = useState<SelectOption[]>([])
  const [evidenceLoading, setEvidenceLoading] = useState<boolean>(false)
  const [evidenceError, setEvidenceError] = useState<string | null>(null)
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string>("")

  useEffect(() => {
    let cancelled = false
    async function loadCases() {
      setCasesLoading(true)
      setCasesError(null)
      try {
        const token = await getAccessToken()
        const options = await fetchCases(token)
        if (!cancelled) setCases(options)
      } catch (err) {
        if (!cancelled) {
          setCasesError(err instanceof Error ? err.message : "Failed to load cases.")
        }
      } finally {
        if (!cancelled) setCasesLoading(false)
      }
    }
    loadCases()
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (!selectedCaseId) {
      setEvidenceOptions([])
      setSelectedEvidenceId("")
      return
    }
    let cancelled = false
    async function loadEvidence() {
      setEvidenceLoading(true)
      setEvidenceError(null)
      setSelectedEvidenceId("")
      try {
        const token = await getAccessToken()
        const options = await fetchEvidenceForCase(selectedCaseId, token)
        if (!cancelled) setEvidenceOptions(options)
      } catch (err) {
        if (!cancelled) {
          setEvidenceError(err instanceof Error ? err.message : "Failed to load evidence.")
        }
      } finally {
        if (!cancelled) setEvidenceLoading(false)
      }
    }
    loadEvidence()
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCaseId])

  return (
    <div className="card selector">
      <div className="card-title">Select an evidence item</div>

      <div className="select-field">
        <label htmlFor="case-select">Case</label>
        <select
          id="coc-case-select"
          className="select"
          value={selectedCaseId}
          disabled={casesLoading || Boolean(casesError)}
          onChange={(e) => setSelectedCaseId(e.target.value)}
        >
          <option value="">{casesLoading ? "Loading cases…" : "Select a case…"}</option>
          {cases.map((c) => (
            <option key={c.id} value={c.id}>
              {c.label}
            </option>
          ))}
        </select>
        {casesError && <p className="coc-field-error">{casesError}</p>}
      </div>

      <div className="select-field">
        <label htmlFor="evidence-select">Evidence</label>
        <select
          id="coc-evidence-select"
          className="select"
          value={selectedEvidenceId}
          disabled={!selectedCaseId || evidenceLoading || Boolean(evidenceError)}
          onChange={(e) => setSelectedEvidenceId(e.target.value)}
        >
          <option value="">
            {!selectedCaseId
              ? "Select a case first…"
              : evidenceLoading
              ? "Loading evidence…"
              : "Select evidence…"}
          </option>
          {evidenceOptions.map((ev) => (
            <option key={ev.id} value={ev.id}>
              {ev.label}
            </option>
          ))}
        </select>
        {evidenceError && <p className="coc-field-error">{evidenceError}</p>}
        {!evidenceLoading && selectedCaseId && !evidenceError && evidenceOptions.length === 0 && (
          <p className="coc-field-hint">No evidence items found for this case.</p>
        )}
      </div>

      <button
        className="btn btn-sm btn-primary"
        type="button"
        disabled={!selectedEvidenceId}
        onClick={() => onViewChain(selectedEvidenceId)}
      >
        View Chain of Custody
      </button>
    </div>
  )
}

export default CaseEvidenceSelector

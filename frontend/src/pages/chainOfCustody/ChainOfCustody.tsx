import "./ChainOfCustody.css"
import { useState, useEffect, useCallback } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useAuth } from "../../context/AuthContext"
import type { ChainOfCustodyRouteParams, CustodyEntry } from "./types"
import { fetchCustodyLog } from "./api"
import CaseEvidenceSelector from "./CaseEvidenceSelector"
import CustodyTimeline from "./CustodyTimeline"

function ChainOfCustody() {
  const { chainId, evidenceId } = useParams<ChainOfCustodyRouteParams>()
  const navigate = useNavigate()
  const { getAccessToken } = useAuth()
  const hasDirectId = Boolean(chainId || evidenceId)

  const [entries, setEntries] = useState<CustodyEntry[]>([])
  const [itemLabel, setItemLabel] = useState<string>("")
  const [caseLabel, setCaseLabel] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(hasDirectId)
  const [error, setError] = useState<string | null>(null)

  const loadCustodyLog = useCallback(async () => {
    if (!chainId && !evidenceId) return
    setLoading(true)
    setError(null)
    try {
      const token = await getAccessToken()
      const result = await fetchCustodyLog({ chainId, evidenceId }, token)
      setEntries(result.entries)
      setItemLabel(result.itemLabel)
      setCaseLabel(result.caseLabel)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load chain of custody.")
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [chainId, evidenceId])

  useEffect(() => {
    if (hasDirectId) loadCustodyLog()
  }, [hasDirectId, loadCustodyLog])

  if (!hasDirectId) {
    return (
      <section id="chain-of-custody-page" className="coc-page-selector">
        <div className="coc-page-sub">Chain of Custody</div>
        <CaseEvidenceSelector
          onViewChain={(selectedEvidenceId) =>
            navigate(`/chainofcustody/evidence/${selectedEvidenceId}`)
          }
        />
      </section>
    )
  }

  return (
    <section id="chain-of-custody-page">
      <CustodyTimeline
        displayId={evidenceId ?? chainId}
        itemLabel={itemLabel}
        caseLabel={caseLabel}
        loading={loading}
        error={error}
        entries={entries}
        onRetry={loadCustodyLog}
      />
    </section>
  )
}

export default ChainOfCustody

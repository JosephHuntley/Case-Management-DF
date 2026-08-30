import { Lock, Plus, Loader2, AlertTriangle, ArrowRight } from 'lucide-react'
import type { CustodyEntry } from "./types"
import { formatTimestamp, shortHash } from "./utils"
import LogCustodyEvent from "../../components/LogCustodyEvent/LogCustodyEvent"
import { useEffect, useState } from 'react'
import type { Evidence } from '../../types'
import { useAuth } from '../../context/AuthContext'

interface CustodyTimelineProps {
  displayId?: string
  itemLabel: string
  caseLabel: string
  loading: boolean
  error: string | null
  entries: CustodyEntry[]
  onRetry: () => void
  evidenceId: string | undefined
  chainId: string | undefined
}

function CustodyTimeline({
  displayId,
  itemLabel,
  caseLabel,
  loading,
  error,
  entries,
  onRetry,
  evidenceId
}: CustodyTimelineProps) {
  const [isLogCustodyOpen, setIsLogCustodyOpen] = useState<boolean>(false)
  const [evidence, setEvidence] = useState<Evidence>(new Object as Evidence)

  const {getAccessToken} = useAuth();

  useEffect(() => {
  
      const fetchEvidenceItems = async () => {

        try {
          const token = await getAccessToken();
          const res = await fetch(`/api/evidence-items/${evidenceId}`, {
            headers: token ? { Authorization: `Bearer ${token}` } : {},
            credentials: 'include',
          })
          if (!res.ok) {
            throw new Error(`Error fetching evidence items: ${res.statusText}`)
          }
          
          const data: Evidence = await res.json()
          setEvidence(data)
        } catch (error) {
          console.error(error)
        } finally {
        }
      }
  
      fetchEvidenceItems()
    }, [])

  return (
    <>
      <div className="coc-toolbar">
        <div className="coc-page-sub">
          {caseLabel && (
            <>
              Case <span className="coc-mono">{caseLabel}</span>
              {" · "}
            </>
          )}
          Item <span className="coc-mono">{displayId}</span>
          {itemLabel && <> — {itemLabel}</>}
        </div>
        <button className="coc-btn coc-btn-sm coc-btn-primary" type="button" onClick={() => setIsLogCustodyOpen(true)}>
          <Plus size={14} />
          Log Custody Event
        </button>
      </div>

      <div className="coc-locked-banner">
        <Lock size={15} />
        Append-only log. Existing entries cannot be edited or deleted — each entry is
        chained to the previous entry's hash.
      </div>

      {loading && (
        <div className="coc-state-card">
          <Loader2 size={18} className="coc-spin" />
          Loading chain of custody…
        </div>
      )}

      {!loading && error && (
        <div className="coc-state-card coc-state-error">
          <AlertTriangle size={18} />
          <span>{error}</span>
          <button className="coc-btn coc-btn-sm" onClick={onRetry}>
            Retry
          </button>
        </div>
      )}

      {!loading && !error && entries.length === 0 && (
        <div className="coc-state-card">No custody events recorded yet.</div>
      )}

      {!loading && !error && entries.length > 0 && (
        <div className="coc-card">
          <div className="coc-chain">
            {entries.map((entry) => (
              <div className="coc-chain-entry" key={entry.id}>
                <div className="coc-chain-node" />
                <div className="coc-chain-card">
                  <div className="coc-chain-top">
                    <span className="coc-chain-action">{entry.action}</span>
                    <span className="coc-chain-when">{formatTimestamp(entry.timestamp)}</span>
                  </div>
                  <div className="coc-chain-detail">
                    <strong>{entry.actor}</strong>
                    {entry.detail ? ` — ${entry.detail}` : null}
                  </div>
                  <div className="coc-hash-row">
                    <span className="coc-hash-chip">
                      {entry.prevHash ? shortHash(entry.prevHash) : "No previous hash"}
                    </span>
                    <ArrowRight size={12} className="coc-hash-arrow" />
                    <span className="coc-hash-chip">{shortHash(entry.row_hash)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      <LogCustodyEvent isOpen={isLogCustodyOpen} onClose={() => setIsLogCustodyOpen(false)} evidence={evidence}/>
    </>
  )
}

export default CustodyTimeline

import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import './ChainOfCustody.css'

interface ChainEntry {
  id: string
  evidence_id: string
  action: string
  performed_by: string
  from_person: string | null
  to_person: string | null
  notes: string | null
  created_at: string
  previous_hash: string | null
  row_hash: string
}

interface VerifyResult {
  evidence_id: string
  is_valid: boolean
  entry_count: number
  broken_entry_ids: string[]
}

function ChainOfCustody() {
  const { getAccessToken } = useAuth()
  const [searchParams] = useSearchParams()
  // NOTE: reading evidenceId from a query param since App.tsx's current
  // route for this page ("/chainofcustody") has no :evidenceId segment.
  // A route like /evidence/:evidenceId/custody would be more RESTful and
  // bookmarkable — worth switching to once per-evidence-item pages exist.
  const evidenceId = searchParams.get('evidenceId')

  const [entries, setEntries] = useState<ChainEntry[]>([])
  const [verify, setVerify] = useState<VerifyResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!evidenceId) {
      setIsLoading(false)
      return
    }

    let cancelled = false

    ;(async () => {
      setIsLoading(true)
      setError(null)
      try {
        const token = await getAccessToken()
        const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}

        const [chainRes, verifyRes] = await Promise.all([
          fetch(`/api/chain-of-custody/evidence/${evidenceId}`, { headers, credentials: 'include' }),
          fetch(`/api/chain-of-custody/evidence/${evidenceId}/verify`, { headers, credentials: 'include' }),
        ])

        if (!chainRes.ok) throw new Error(`Failed to load chain of custody (${chainRes.status})`)
        if (!verifyRes.ok) throw new Error(`Failed to verify chain of custody (${verifyRes.status})`)

        const chainData: ChainEntry[] = await chainRes.json()
        const verifyData: VerifyResult = await verifyRes.json()

        if (!cancelled) {
          setEntries(chainData)
          setVerify(verifyData)
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        if (!cancelled) setIsLoading(false)
      }
    })()

    return () => {
      cancelled = true
    }
  }, [evidenceId, getAccessToken])

  if (!evidenceId) {
    return (
      <main id="chain-of-custody">
        <p className="coc-empty">
          No evidence item selected. Navigate here from an Evidence Item page (expects ?evidenceId=... for now).
        </p>
      </main>
    )
  }

  return (
    <main id="chain-of-custody">
      <h1 className="coc-title">Chain of Custody</h1>

      {isLoading && <p className="coc-empty">Loading…</p>}
      {error && <p className="coc-error">{error}</p>}

      {!isLoading && !error && (
        <>
          {verify && (
            <div className={`coc-integrity-banner ${verify.is_valid ? 'valid' : 'broken'}`}>
              {verify.is_valid
                ? `Chain verified — ${verify.entry_count} entries, no tampering detected.`
                : `Integrity check FAILED — ${verify.broken_entry_ids.length} of ${verify.entry_count} entries broke the hash chain.`}
            </div>
          )}

          <div className="coc-chain">
            {entries.map((entry) => {
              const isBroken = verify?.broken_entry_ids.includes(entry.id) ?? false
              return (
                <div key={entry.id} className={`coc-entry ${isBroken ? 'broken' : ''}`}>
                  <div className="coc-entry-top">
                    <span className="coc-entry-action">{entry.action}</span>
                    <span className="coc-entry-when">{new Date(entry.created_at).toLocaleString()}</span>
                  </div>
                  {entry.notes && <div className="coc-entry-notes">{entry.notes}</div>}
                  <div className="coc-entry-hashes">
                    <span className="coc-hash-chip">
                      {entry.previous_hash ? entry.previous_hash.slice(0, 8) : 'genesis'}
                    </span>
                    <span className="coc-hash-arrow">→</span>
                    <span className="coc-hash-chip">{entry.row_hash.slice(0, 8)}</span>
                  </div>
                </div>
              )
            })}
          </div>
        </>
      )}
    </main>
  )
}

export default ChainOfCustody
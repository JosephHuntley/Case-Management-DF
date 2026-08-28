import { useState, useEffect } from 'react'
import { useAuth } from '../../context/AuthContext'
import './Evidence.css'
import { useNavigate } from 'react-router-dom'

interface Case {
  id: string
  case_number: string
}

interface EvidenceItem {
  id: string
  evidence_tag: string
}

function EvidenceSearch() {

  const [cases, setCases] = useState<Case[]>([])
  const [selectedCaseId, setSelectedCaseId] = useState<string>('')
  const [casesLoading, setCasesLoading] = useState<boolean>(true)
  const [casesError, setCasesError] = useState<string | null>(null)

  const {getAccessToken} = useAuth();
  const navigate = useNavigate();

  const [evidenceItems, setEvidenceItems] = useState<EvidenceItem[]>([])
  const [evidenceLoading, setEvidenceLoading] = useState<boolean>(false)
  const [evidenceError, setEvidenceError] = useState<string | null>(null)
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string>('')

  const handleViewEvidence = () => {
    if (selectedEvidenceId) {
      navigate(`/evidence/evidenceId/${selectedEvidenceId}`)
    }
  }

  useEffect(() => {
    const fetchCases = async () => {
      setCasesLoading(true)
      setCasesError(null)
      try {
        const token = await getAccessToken();
        const res = await fetch('/api/cases/', {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
          credentials: 'include',
        })
        if (!res.ok) {
          throw new Error(`Error fetching cases: ${res.statusText}`)
        }
        
        const data: Case[] = await res.json()
        setCases(data)
      } catch (error) {
        setCasesError("Failed to fetch cases.")
        console.error(error)
      } finally {
        setCasesLoading(false)
      }
    }

    fetchCases()
  }, [])

useEffect(() => {
    if (!selectedCaseId) {
      setEvidenceItems([])
      return
    }

    const fetchEvidenceItems = async () => {
      setEvidenceLoading(true)
      setEvidenceError(null)
      try {
        const token = await getAccessToken();
        const res = await fetch(`/api/evidence-items/case/${selectedCaseId}`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
          credentials: 'include',
        })
        if (!res.ok) {
          throw new Error(`Error fetching evidence items: ${res.statusText}`)
        }
        
        const data: EvidenceItem[] = await res.json()
        setEvidenceItems(data)
      } catch (error) {
        setEvidenceError("Failed to fetch evidence items.")
        console.error(error)
      } finally {
        setEvidenceLoading(false)
      }
    }

    fetchEvidenceItems()
  }, [selectedCaseId])

  return (
    <main id="evidence">
      <div className="page-sub">Evidence</div>
        <div className="card selector">
          <div className="card-title">Select an evidence item</div>
            <div className="select-field">
                  <label htmlFor="evidence-case-select">Case</label>
                  <select
                    id="evidence-case-select"
                    className="select"
                    value={selectedCaseId}
                    disabled={casesLoading || Boolean(casesError)}
                    onChange={(e) => setSelectedCaseId(e.target.value)}
                  >
                    <option value="">
                      {casesLoading ? "Loading cases…" : "Select a case…"}
                    </option>
                    {cases.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.case_number}
                      </option>
                    ))}
                  </select>
                  {casesError && <p className="field-error">{casesError}</p>}
            </div>

            <div className="select-field">
                  <label htmlFor="evidence-case-select">Evidence</label>
                  <select
                    id="evidence-case-select"
                    className="select"
                    value={selectedEvidenceId}
                    disabled={evidenceLoading || Boolean(evidenceError)}
                    onChange={(e) => setSelectedEvidenceId(e.target.value)}
                  >
                    <option value="">
                      {evidenceLoading ? "Loading evidence…" : selectedCaseId ? "Select an evidence item…" : "Select a case first…"}
                    </option>
                    {evidenceItems.map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.evidence_tag}
                      </option>
                    ))}
                  </select>
                  {evidenceError && <p className="field-error">{evidenceError}</p>}
            </div>

            <button
            className="btn btn-sm btn-primary"
            type="button"
            disabled={!selectedEvidenceId}
            onClick={handleViewEvidence}
          >
            View Evidence
          </button>
        </div>
    </main>
  )

}

export default EvidenceSearch
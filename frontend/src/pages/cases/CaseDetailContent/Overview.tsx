import type { Case } from "../../../types"
import { formatTimestamp } from "../../chainOfCustody/utils"
import { useNavigate } from "react-router-dom"

interface OverviewProps{
    currentCase:Case | null
}

function Overview({currentCase}:OverviewProps) {
    const navigate = useNavigate()
    return (
        <>
            <span className="card-title">Summary</span>
            <p>{currentCase ? currentCase.description : "No description available"}</p>
            <span className="card-title">Linked Evidence</span>
            <table id="case-detail-linked-evidence">
                <thead>
                    <tr>
                        <th>Tag</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Acquired At</th>
                    </tr>
                </thead>
                <tbody>
                {currentCase?.evidence ? 
                currentCase.evidence.map((e, i) => (
                    <tr onClick={() => navigate(`/evidence/evidenceId/${e.id}`)} key={i} className={i == currentCase.evidence.length -1 ? 'no-border' : ''}>
                        <td>{e.evidence_tag}</td>
                        <td>{e.name}</td>
                        <td>{e.description}</td>
                        <td>{formatTimestamp(e.acquired_at)}</td>
                    </tr>
                ))
             : (
                    <tr className="no-border">
                    <td colSpan={4}>No evidence to display</td>
                    </tr>
                )}
                </tbody>
            </table>
        </>
    )
}

export default Overview
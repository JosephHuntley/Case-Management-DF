import { useNavigate, useParams } from 'react-router-dom'
import {useEffect, useState} from 'react'
import {useAuth} from '../../context/AuthContext'
import type {Case} from '../../types'
import Button from '../../components/Button/Button'
import { CaseStatusLabels } from '../../types'
import { formatTimestamp } from '../../utils/formatTimestamp'
import Overview from './CaseDetailContent/Overview'
import EvidenceDetail from '../evidence/EvidenceDetail'


interface CaseDetailParams{
    caseId: string
    [key: string]: string | undefined
}

function CaseDetail(){
    const {caseId} = useParams<CaseDetailParams>();
    const {getAccessToken} = useAuth()
    const navigate = useNavigate()
    

    const [currentCase, setCurrentCase] = useState<Case | null>(null);
    const [tab, setTab] = useState<string>('overview')

    useEffect(() => {
        const fetchCase = async () => {
            try {
                const token = await getAccessToken();
                const res = await fetch(`/api/cases/${caseId}`, {
                headers: token ? { Authorization: `Bearer ${token}` } : {},
                credentials: 'include',
                })
                if (!res.ok) {
                throw new Error(`Error fetching cases: ${res.statusText}`)
                }
                
                const data: Case = await res.json()
                setCurrentCase(data)
            } catch (error) {

                console.error(error)
            } finally {

            }}

        fetchCase()

        },[])

    return(
        <main id="case-detail"> 
            <div id="case-detail-header">
                <div id="case-detail-back" onClick={() => navigate('/cases')}>← Back to cases</div>
                <div id="case-detail-buttons">
                    <Button text="Edit" secondary/>
                    <Button text="Generate Report"/>
                </div>
            </div>
            <div className='flex-row'>
                <p className='case-detail-case_number'>
                    {currentCase?.case_number}  
                </p>
                {
                    currentCase &&
                    <span 
                    className={`badge ${currentCase.status == "open" || currentCase.status == 'closed' ? CaseStatusLabels[currentCase.status].toLowerCase() : 'pending'}`}>
                    {CaseStatusLabels[currentCase.status]}
                    </span>
                }
            </div>
            <h2 className='case-detail-title'>{currentCase?.title || "Case couldn't load"}</h2>
            <div id="case-detail-data">
                <div>
                    <span>Lead Investigator</span>
                    {
                        currentCase?.assigned_to ? 
                        `${currentCase?.assigned_to?.first_name} ${currentCase?.assigned_to?.last_name}`
                        : 'To Be Assigned'
                    }
                </div>
                <div>
                    <span>Created</span>
                    {
                        currentCase ? 
                        `${formatTimestamp(currentCase.created_at, true)}`
                        : "Error, couldn't load data"
                    }
                </div>
                <div>
                    <span>Evidence Items</span>
                    {
                        currentCase ? 
                        `${currentCase.evidence.length}`
                        : "Error, couldn't load data"
                    }
                </div>
            </div>
            <div id="case-detail-main-content">
                <div id="case-detail-tabs">
                    <div className={tab == 'overview' ? 'tab-active' : ''} onClick={() => setTab('overview')}>Overview</div>
                    <div className={tab == 'evidence' ? 'tab-active' : ''} onClick={() => setTab('evidence')}>{`Evidence (${currentCase?.evidence.length})`}</div>
                    <div className={tab == 'coc' ? 'tab-active' : ''} onClick={() => setTab('coc')}>Chain of Custody</div>
                    <div className={tab == 'reports' ? 'tab-active' : ''} onClick={() => setTab('reports')}>Reports</div>
                </div>
                <div id="case-detail-tab-content" className='card'>
                    {tab == 'overview' && <Overview currentCase={currentCase} />}
                    {tab == 'evidence' && currentCase?.evidence.map(e => (
                        <EvidenceDetail evidenceIdProp={e.id}/>
                    ))}
                </div>
            </div>
        </main>
    )
}

export default CaseDetail
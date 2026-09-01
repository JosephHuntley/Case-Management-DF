import {useState, useEffect} from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import LogCustodyEvent from "../../components/LogCustodyEvent/LogCustodyEvent";
import type { Evidence,} from "../../types";
import { EvidenceTypeLabels, AcquisitionMethodLabels, CustodyActionLabels } from "../../types";
import './Evidence.css'
import HashDisplay from "../../components/HashDisplay/HashDisplay";
import { formatTimestamp } from "../chainOfCustody/utils";
import { formatBytes } from "../../utils/formatBytes";
import { useNavigate } from 'react-router-dom'

interface EvidenceDetailProps{
    evidenceIdProp?:String | null;
}

function EvidenceDetail({evidenceIdProp = null}:EvidenceDetailProps) {
    const [evidence, SetEvidence] = useState<Evidence >(new Object() as Evidence);
    const [isLogCustodyEventOpen, setIsLogCustodyEventOpen] = useState(false);

    const { evidenceId } = useParams<{ evidenceId: string }>();
    const {getAccessToken} = useAuth();
    const navigate = useNavigate();

    const previousEntry = evidence?.chain_of_custody?.at(-2);
    const currentChain = evidence?.chain_of_custody?.at(-1);

    const handleLogCustodyEvent = () => {
        setIsLogCustodyEventOpen(true);
    }

    useEffect(() => {
        const tmpEvidenceId = evidenceIdProp || evidenceId
        const fetchEvidence = async () => {
            try {
                const token = await getAccessToken();
                const response = await fetch(`/api/evidence-items/${tmpEvidenceId}`, {
                    headers: token ? { Authorization: `Bearer ${token}` } : {},
                    credentials: 'include',
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch evidence');
                }
                const data: Evidence = await response.json();
                SetEvidence(data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchEvidence();
    }, [evidenceId]);
    return (
        <main id="evidence-detail-page">
            {
                evidenceIdProp ? <></> :
                <div className="evidence-detail-header">
                    <p className="evidence-detail-header-text"><span style={{color: 'var(--text-muted)'}}>Case</span> {evidence?.case_title} · <span style={{color: 'var(--text-muted)'}}>Item</span> {evidence?.evidence_tag}</p>
                    <button className="evidence-detail-header-btn" onClick={() => handleLogCustodyEvent()}>Log Custody Event</button>
                </div>
            }
            
            <div id="evidence-detail-grid">
                <div className="card evidence-card">
                    <h2 className="card-title low-margin">Item Details</h2>
                    <div id="evidence-detail">
                        <div className="evidence-detail-item">
                            <h3>Name</h3>
                            <p>{evidence?.name}</p>
                        </div>
                        <div className="evidence-detail-item">
                            <h3>Type</h3>
                            <p>{evidence?.evidence_type && EvidenceTypeLabels[evidence.evidence_type]}</p>
                        </div>
                        <div className="evidence-detail-item">
                            <h3>ACQUIRED At</h3>
                            <p>{formatTimestamp(evidence?.acquired_at)}</p>
                        </div>
                        <div className="evidence-detail-item">
                            <h3>Acquisition Method</h3>
                            <p>{evidence?.acquisition_method && AcquisitionMethodLabels[evidence.acquisition_method]}</p>
                        </div>
                        <div className="evidence-detail-item">
                            <h3>Hash Verified</h3>
                            <p>{evidence?.is_verified ? 'Yes' : 'No'}</p>
                        </div>
                        <div className="evidence-detail-item">
                            <h3>Size</h3>
                            <p>{formatBytes(evidence?.size_bytes)}</p>
                        </div>
                        <div className="evidence-detail-item">
                            <h3>ACQUIRED By</h3>
                            <p>{evidence?.acquired_by?.first_name} {evidence?.acquired_by?.last_name}</p>
                        </div>
                    </div>
                    <div>
                        <h2 className="card-title low-margin">Description</h2>
                        <p className="evidence-detail-description">{evidence?.description}</p>
                    </div>
                    <div id="evidence-detail-hashes">
                        <h2 className="card-title low-margin">Integrity Hashes</h2>
                        <div className="evidence-detail-hash">
                            <h3>SHA256</h3>
                            <HashDisplay value={evidence.sha256} />
                        </div>
                        <div className="evidence-detail-hash">
                            <h3>MD5</h3>
                            <HashDisplay value={evidence?.md5} />
                        </div>
                    </div>
                </div>
                <div className="card gap col">
                    <div id="evidence-detail-custody-snapshot">
                        <h2 className="card-title"> Chain of Custody Snapshot</h2>  
                        <a onClick={() => navigate(`/chainofcustody/evidence/${evidence.id}`)}>View Full Log</a>
                    </div>
                    <div className="evidence-detail-custody-snapshot-details">
                        <h3>Current Location</h3>
                        <p>TODO: Needs to be implemented on backed</p>
                    </div>
                    <div className="evidence-detail-custody-snapshot-details">
                        <h3>Current Custodian</h3>
                        <p>
                        {currentChain
                            ? `${currentChain?.to_person?.first_name} ${currentChain?.to_person?.last_name}`
                            : '-'}
                        </p>
                    </div>
                    <div className="evidence-detail-custody-snapshot-details">
                        <h3>Last Event</h3>
                        <p>
                        {previousEntry ? CustodyActionLabels[previousEntry.action] : "—"} -{" "}
                        {previousEntry ? formatTimestamp(previousEntry.created_at) : "—"}
                        </p>
                    </div>
                    <div className="evidence-detail-custody-snapshot-details">
                        <h3>Notes</h3>
                        <p>{evidence?.chain_of_custody?.at(-1)?.notes || "No Notes to Display"}</p>
                    </div>

                </div>
            </div>
            <LogCustodyEvent isOpen={isLogCustodyEventOpen} onClose={() => setIsLogCustodyEventOpen(false)} evidence={evidence} />
        </main>
    );
}

export default EvidenceDetail;
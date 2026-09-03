import type { Evidence } from "../../../types"
import { CustodyActionLabels } from "../../../types/ChainOfCustody"

function ChainOfCustody({evidence}:{evidence:Evidence[] | null}) {
    return (
    <div style={{display:'flex', flexDirection:'column', gap:'16px'}}>
        {evidence?.map(e => (
            <div id="case-detail-coc" key={e.id} >
                <h2 className="case-detail-coc-evidence-tag">{e.evidence_tag}</h2>
                {e.chain_of_custody.map((c, i) => (
                    <div className="case-detail-chain" key={c.id} id={`${i == e.chain_of_custody.length - 1 && 'case-detail-coc-last-child'}`}>
                        <div className="chain-node"/>
                        <div className="card case-detail-coc-card">
                            <div><span style={{fontWeight: 'bold'}}>{CustodyActionLabels[c.action]}</span> | {c.notes}</div>
                            <div >
                                {c.from_person ? `${c.from_person.first_name} ${c.from_person.last_name}` : c.action == 'collected' ? 'Collected' : 'No User'} {' '}
                                <span className="arrow">-&gt;</span> {' '}
                                {c.to_person ? `${c.to_person.first_name} ${c.to_person.last_name}` : 'No User'}
                            </div>
                        </div>
                        
                    </div>
                ))}
            </div>
        ))}
    </div>
)}

export default ChainOfCustody
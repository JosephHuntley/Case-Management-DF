import type { Evidence } from "../../../types"

function ChainOfCustody({evidence}:{evidence:Evidence[] | null}) {
    return (
    <div>
        {evidence?.map(e => (
            <div id="case-detail-coc" key={e.id} >
                <h2>{e.evidence_tag}</h2>
                {e.chain_of_custody.map((c, i) => (
                    <div className="case-detail-chain" key={c.id} id={`${i == e.chain_of_custody.length - 1 && 'case-detail-coc-last-child'}`}>
                        <div className="chain-node"></div>
                        <div className="card">
                            <div>{c.action} | {c.notes}</div>
                            <div >{c.from_person ? `${c.from_person.first_name} ${c.from_person.last_name}` : 'No User'} <span className="arrow">-&gt;</span> {c.to_person ? `${c.to_person.first_name} ${c.to_person.last_name}` : 'No User'}</div>
                        </div>
                        
                    </div>
                ))}
            </div>
        ))}
    </div>
)}

export default ChainOfCustody
import { useParams } from "react-router-dom";

function EvidenceDetail() {
    const { evidenceId } = useParams<{ evidenceId: string }>();
    return (
        <main>
            <h1>Evidence Detail</h1>
            <p>Evidence ID: {evidenceId}</p>
        </main>
    );
}

export default EvidenceDetail;
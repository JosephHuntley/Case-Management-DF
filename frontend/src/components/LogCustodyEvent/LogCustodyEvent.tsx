import { useState, useEffect } from 'react'
import Modal from '../Modal/Modal'
import './LogCustodyEvent.css'
import type {User, Evidence} from '../../types'
import { useAuth } from '../../context/AuthContext'

interface LogCustodyEventProps {
    isOpen: boolean
    onClose: () => void
    evidence: Evidence
}

function LogCustodyEvent({ isOpen, onClose, evidence }: LogCustodyEventProps) {
    const [selectedAction, setSelectedAction] = useState<string>("Select_an_action");
    const [toPerson, setToPerson] = useState<string>("");
    const [notes, setNotes] = useState<string>("");
    const [users, setUsers] = useState<User[]>([]);

    const {getAccessToken} = useAuth();

    const handleSubmit = async () => {
        try {
            const token = await getAccessToken();
            const response = await fetch(`/api/chain-of-custody/append`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    evidence_id: evidence.id,
                    action: selectedAction,
                    from_person: null, // TODO: remove once from_person is implemented in the backend
                    to_person: toPerson,
                    notes: notes
                }),
                credentials: 'include',
            });
            if (!response.ok) {
                throw new Error('Failed to log custody event');
            }
            onClose();
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const token = await getAccessToken();
                const response = await fetch('/api/users/', {
                    credentials: 'include',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch users');
                }
                const data: User[] = await response.json();
                setUsers(data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchUsers();
    }, []);

return(
    <Modal isOpen={isOpen} onClose={() => {onClose()}} size="sm" >
        <div id="log-custody-event-modal-content">
            <h1>Log Custody Event</h1>
            <h2>Tag: {evidence.evidence_tag}</h2>
            <div className="select-field">
                <label htmlFor="log-custody-action">Action:</label>
                <select 
                id="log-custody-action" name="log-custody-action"
                className="select"
                value={selectedAction}
                onChange={(e) => setSelectedAction(e.target.value)}>
                    <option value="Select_an_action">Select an action</option>
                    <option value="transferred">Transferred</option>
                    <option value="checked_out">Checked Out</option>
                    <option value="returned">Returned</option>
                    <option value="archived">Archived</option>
                </select>
            </div>
            <div className="select-field">
                <label htmlFor="log-custody-to-person">To Person:</label>
                <select 
                    id="log-custody-to-person" 
                    name="log-custody-to-person" 
                    className="select"
                    value={toPerson}
                    onChange={(e) => setToPerson(e.target.value)}
                >
                    <option value="">Select a person</option>
                    {users.map((user) => (
                        <option key={user.id} value={user.id}>
                            {user.username} ({user.first_name} {user.last_name})
                        </option>
                    ))}
                </select>
            </div>
            <div className="select-field">
                <label htmlFor="log-custody-notes">Notes:</label>
                <textarea
                id="log-custody-notes"
                name="log-custody-notes"
                className="form-textarea"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                />
            </div>

            <div className="log-custody-event-modal-buttons">
                <button className="btn btn-primary" onClick={() => handleSubmit()}>Submit</button>
                <button className="btn btn-secondary" onClick={() => {onClose()}}>Cancel</button>
            </div>
        </div>
    </Modal>
)
}

export default LogCustodyEvent
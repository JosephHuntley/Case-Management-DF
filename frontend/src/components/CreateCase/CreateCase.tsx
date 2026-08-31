import Modal from "../Modal/Modal"
import { useEffect, useState } from "react"
import type {User} from "../../types"
import {useAuth} from '../../context/AuthContext'
import "./CreateCase.css"


interface CreateCaseProps {
    isOpen: boolean
    onClose: () => void
}

function CreateCase({isOpen, onClose}:CreateCaseProps) {
    const [notes, setNotes] = useState<string>('')
    const [title, setTitle] = useState<string>('')
    const [selectedPriority, setSelectedPriority] = useState<string>('medium')
    const [assignedTo, setAssignedTo] = useState<string>('')
    const [users, setUsers] = useState<User[]>([])
    const [caseError, setCaseError] = useState<string | null>(null)

    const {getAccessToken} = useAuth();

    const handleSubmit = async () => {
        try {
                const token = await getAccessToken();
                const response = await fetch(`/api/cases/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        title: title,
                        description:notes,
                        status:'open',
                        priority:selectedPriority,
                        assigned_to:assignedTo,
                    }),
                    credentials: 'include',
                });
                if (!response.ok) {
                    throw new Error('Failed to create case');
                }
                onClose();
            } catch (error) {
                setCaseError('Could not submit case')
                console.error(error);
            }
    }

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
        fetchUsers()
    }, [])

    return (
        <Modal isOpen={isOpen} onClose={() => onClose()}>
            <div id="create-case-modal-content">
                <h1>Create Case</h1>
                <div className="select-field">
                    <label htmlFor="create-case-title">Title:</label>
                    <input id="create-case-title" name="create-case-title" value={title} onChange={(e => setTitle(e.target.value))}/>
                </div>
                <div className="select-field">
                    <label htmlFor="create-case-description">Description:</label>
                    <textarea
                    id="create-case-description"
                    name="create-case-description"
                    className="form-textarea"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    />
                </div>
                <div className="select-field">
                    <label htmlFor="create-case-priority">Priorirty:</label>
                    <select 
                    id="create-case-priority" 
                    name="create-case-priority"
                    className="select"
                    value={selectedPriority}
                    onChange={(e) => setSelectedPriority(e.target.value)}>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                        <option value="critical">Critical</option>
                    </select>
                </div>
                <div className="select-field">
                    <label htmlFor="create-case-assignee">Assigned To: </label>
                    <select 
                    id="create-case-assignee" 
                    name="create-case-assignee"
                    className="select"
                    value={assignedTo}
                    onChange={(e) => setAssignedTo(e.target.value)}>
                        <option value="">Select a person</option>
                        {users.map((user) => (
                            <option key={user.id} value={user.id}>
                                {user.username} ({user.first_name} {user.last_name})
                            </option>
                        ))}
                        
                    </select>
                </div>
                <div className="create-case-modal-buttons">
                    <button className="btn btn-primary" onClick={() => handleSubmit()}>Submit</button>
                    <button className="btn btn-secondary" onClick={() => {onClose()}}>Cancel</button>
                </div>
                {caseError ? <div className="error">{caseError}</div> : <></>}
            </div>
        </Modal>
    )
}

export default CreateCase
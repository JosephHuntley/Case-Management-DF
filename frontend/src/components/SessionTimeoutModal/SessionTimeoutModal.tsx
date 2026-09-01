import Modal from '../Modal/Modal'; 

interface Props {
  isOpen: boolean;
  secondsRemaining: number;
  onExtend: () => void;
  onLogout: () => void;
}

export function SessionTimeoutModal({ isOpen, secondsRemaining, onExtend, onLogout }: Props) {
  const mins = Math.floor(secondsRemaining / 60);
  const secs = secondsRemaining % 60;

  return (
    <Modal isOpen={isOpen} onClose={onExtend} size="sm">
      <h2>Are you still there?</h2>
      <p>
        You've been idle for a while and your session will expire in{' '}
        {mins}:{secs.toString().padStart(2, '0')}. Any unsaved changes in open
        forms should be saved now.
      </p>
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
        <button onClick={onExtend}>Stay signed in</button>
        <button onClick={onLogout}>Log out now</button>
      </div>
    </Modal>
  );
}

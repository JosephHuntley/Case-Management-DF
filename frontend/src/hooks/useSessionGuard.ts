import { useEffect, useRef, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useIdleTracker } from './useIdleTracker';

// Start caring once we're within this many ms of expiry.
const WARNING_WINDOW_MS = 2 * 60 * 1000; // 2 min

// "Active" means some interaction within this many ms of now.
const IDLE_THRESHOLD_MS = 5 * 60 * 1000; // 5 min

// How often to re-evaluate. Doesn't need to be precise to the second.
const POLL_INTERVAL_MS = 10 * 1000;

interface SessionGuardState {
  /** True when the user should be asked "are you still there?" */
  showWarning: boolean;
  /** Seconds until the token actually expires, for the countdown display. */
  secondsRemaining: number;
  /** Call when the user responds "yes, keep me signed in" from the modal. */
  extendSession: () => void;
  /** Call when the user chooses to log out from the modal. */
  logoutNow: () => void;
}

export function useSessionGuard(): SessionGuardState {
  const { expiresAt, refreshToken, logout } = useAuth();
  const lastActivityRef = useIdleTracker();
 
  const [showWarning, setShowWarning] = useState(false);
  const [secondsRemaining, setSecondsRemaining] = useState(0);
  const isRefreshingRef = useRef(false);
 
  useEffect(() => {
    const tick = async () => {
      if (!expiresAt) {
        // console.log('[session-guard] poll: no expiresAt yet, skipping');
        setShowWarning(false);
        return;
      }
 
      const now = Date.now();
      const msUntilExpiry = expiresAt - now;
      const idleMs = now - lastActivityRef.current;
      // console.log(
      //   `[session-guard] poll: expiresIn=${Math.round(msUntilExpiry / 1000)}s idleFor=${Math.round(idleMs / 1000)}s`,
      // );
 
      if (msUntilExpiry <= 0) {
        // Token's already dead — nothing left to silently refresh in time.
        setShowWarning(false);
        await logout();
        window.location.reload();
        return;
      }
 
      if (msUntilExpiry > WARNING_WINDOW_MS) {
        // Not close enough to expiry to care yet.
        if (showWarning) setShowWarning(false);
        return;
      }
 
      if (idleMs < IDLE_THRESHOLD_MS) {
        // User is actively working — renew quietly, never interrupt them.
        if (!isRefreshingRef.current) {
          isRefreshingRef.current = true;
          try {
            await refreshToken();
          } finally {
            isRefreshingRef.current = false;
          }
        }
        setShowWarning(false);
        return;
      }
 
      // Near expiry AND idle: ask before the session dies silently underneath them.
      setSecondsRemaining(Math.max(Math.floor(msUntilExpiry / 1000), 0));
      setShowWarning(true);
    };
 
    tick();
    const interval = setInterval(tick, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [expiresAt]);
 
  const extendSession = () => {
    isRefreshingRef.current = true;
    refreshToken().finally(() => {
      isRefreshingRef.current = false;
    });
    setShowWarning(false);
  };
 
  const logoutNow = () => {
    setShowWarning(false);
    logout().then(() => window.location.reload());
  };
 
  return { showWarning, secondsRemaining, extendSession, logoutNow };
}

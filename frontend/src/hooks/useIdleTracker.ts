import { useEffect, useRef } from 'react';

const ACTIVITY_EVENTS = ['mousedown', 'keydown', 'scroll', 'touchstart', 'wheel'] as const;

/**
 * Tracks the timestamp of the user's last interaction anywhere in the app.
 * Deliberately uses a ref, not state — activity fires constantly, and we
 * don't want every mouse move (or in this case every click/keypress) to
 * trigger a re-render. Consumers poll `lastActivityRef.current` instead.
 */
export function useIdleTracker() {
  const lastActivityRef = useRef<number>(Date.now());

  useEffect(() => {
    const markActive = () => {
      lastActivityRef.current = Date.now();
      // console.log('[idle-tracker] activity detected', new Date().toLocaleTimeString());
    };

    ACTIVITY_EVENTS.forEach(evt =>
      window.addEventListener(evt, markActive, { passive: true }),
    );

    return () => {
      ACTIVITY_EVENTS.forEach(evt => window.removeEventListener(evt, markActive));
    };
  }, []);

  return lastActivityRef;
}
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from 'react';

/**
 * AuthContext
 * -----------
 * Global auth/session state for Case-Management-DF.
 *
 * Assumptions about the backend (adjust the endpoint constants below if
 * your actual routes differ):
 *   POST /api/auth/login    -> { access_token }           sets refresh cookie (httpOnly)
 *   POST /api/auth/refresh  -> { access_token }            reads refresh cookie, rotates it
 *   POST /api/auth/logout   -> 204                         clears refresh cookie, revokes it
 *   GET  /api/auth/me       -> RawUser (snake_case)        requires Authorization: Bearer <access_token>
 *
 * The access token is kept in memory only (React state), never in
 * localStorage/sessionStorage. The refresh token lives entirely in the
 * httpOnly cookie your backend already sets, so this file never touches it
 * directly — it just calls /api/auth/refresh and lets the browser send the
 * cookie automatically (credentials: 'include').
 */

const ENDPOINTS = {
  login: `/api/auth/login`,
  refresh: `/api/auth/refresh`,
  logout: `/api/auth/logout`,
  me: `/api/auth/me`,
};

export type Role = 'admin' | 'investigator' | 'analyst' | 'viewer';

export interface User {
  id: string;
  username: string;
  firstName: string;
  lastName: string;
  role: Role;
}

/**
 * Shape returned by GET /api/auth/me — confirmed split first/last name
 * (snake_case), not a single full_name field.
 */
interface RawUser {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  role: string;
}

function normalizeUser(raw: RawUser): User {
  return {
    id: raw.id,
    username: raw.username,
    firstName: raw.first_name,
    lastName: raw.last_name,
    role: raw.role as Role,
  };
}

interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  /** Returns a valid access token, refreshing it first if needed. */
  getAccessToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

// ---- Provider -------------------------------------------------------------

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Access token lives in a ref (not state) so reads never trigger a
  // re-render and always see the latest value inside async callbacks.
  const accessTokenRef = useRef<string | null>(null);

  // Prevents a stampede of parallel refresh calls if several requests
  // hit a 401 at the same time (e.g. multiple widgets loading at once).
  const refreshPromiseRef = useRef<Promise<string | null> | null>(null);

  const setAccessToken = (token: string | null) => {
    accessTokenRef.current = token;
  };

  const fetchCurrentUser = useCallback(async (token: string): Promise<User> => {
    const res = await fetch(ENDPOINTS.me, {
      headers: { Authorization: `Bearer ${token}` },
      credentials: 'include',
    });
    if (!res.ok) throw new Error('Failed to load current user');
    const raw: RawUser = await res.json();
    return normalizeUser(raw);
  }, []);

  const refresh = useCallback(async (): Promise<string | null> => {
    if (refreshPromiseRef.current) return refreshPromiseRef.current;

    const attempt = (async () => {
      try {
        const res = await fetch(ENDPOINTS.refresh, {
          method: 'POST',
          credentials: 'include',
        });

        if (!res.ok) {
          setAccessToken(null);
          setUser(null);
          return null;
        }

        const data = await res.json();
        setAccessToken(data.access_token);
        return data.access_token as string;
      } catch {
        setAccessToken(null);
        setUser(null);
        return null;
      } finally {
        refreshPromiseRef.current = null;
      }
    })();

    refreshPromiseRef.current = attempt;
    return attempt;
  }, []);

  const getAccessToken = useCallback(async (): Promise<string | null> => {
    if (accessTokenRef.current) return accessTokenRef.current;
    return refresh();
  }, [refresh]);

  const login = useCallback(
    async (username: string, password: string) => {
      setError(null);
      // Backend route takes OAuth2PasswordRequestForm = Depends(), which
      // requires application/x-www-form-urlencoded — confirmed against
      // the actual /api/auth/login route signature.
      const res = await fetch(ENDPOINTS.login, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        credentials: 'include',
        body: new URLSearchParams({ username, password }),
      });

      if (!res.ok) {
        const message =
          res.status === 429
            ? 'Too many attempts. Try again in a few minutes.'
            : 'Invalid username or password.';
        setError(message);
        throw new Error(message);
      }

      const data = await res.json();
      setAccessToken(data.access_token);

      const currentUser = await fetchCurrentUser(data.access_token);
      setUser(currentUser);
    },
    [fetchCurrentUser],
  );

  const logout = useCallback(async () => {
    try {
      await fetch(ENDPOINTS.logout, {
        method: 'POST',
        credentials: 'include', // lets the backend revoke the refresh cookie
      });
    } finally {
      setAccessToken(null);
      setUser(null);
    }
  }, []);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      const token = await refresh();
      if (cancelled) return;

      if (token) {
        try {
          const currentUser = await fetchCurrentUser(token);
          if (!cancelled) setUser(currentUser);
        } catch {
          if (!cancelled) setUser(null);
        }
      }

      if (!cancelled) setIsLoading(false);
    })();

    return () => {
      cancelled = true;
    };
  }, [refresh, fetchCurrentUser]);

  const value: AuthContextValue = {
    user,
    isAuthenticated: user !== null,
    isLoading,
    error,
    login,
    logout,
    getAccessToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// ---- Hook -----------------------------------------------------------------

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
}

export function useHasRole(...roles: Role[]): boolean {
  const { user } = useAuth();
  return user !== null && roles.includes(user.role);
}
import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export interface DashboardStats {
  activeCases: number;
  totalCases: number;
  evidenceItemsTotal: number;
  pendingReviews: number;
  custodyIntegrityPercent: number;
}

interface RawDashboardSummary {
  active_cases: number;
  total_cases: number;
  evidence_items_total: number;
  pending_reviews: number;
  custody_integrity_percent: number;
}

function normalize(raw: RawDashboardSummary): DashboardStats {
  return {
    activeCases: raw.active_cases,
    totalCases: raw.total_cases,
    evidenceItemsTotal: raw.evidence_items_total,
    pendingReviews: raw.pending_reviews,
    custodyIntegrityPercent: raw.custody_integrity_percent,
  };
}

export function useDashboardStats() {
  const { getAccessToken } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        const token = await getAccessToken();
        const res = await fetch('/api/dashboard/summary', {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
          credentials: 'include',
        });
        if (!res.ok) throw new Error(`Failed to load dashboard stats (${res.status})`);

        const raw: RawDashboardSummary = await res.json();
        if (!cancelled) setStats(normalize(raw));
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Unknown error loading stats');
        }
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [getAccessToken]);

  return { stats, isLoading, error, setIsLoading };
}
import { useEffect, useState } from 'react'
import "./Dashboard.css"
import { useDashboardStats } from './useDashboardStats';
import { useAuth } from '../../context/AuthContext';
import { formatRelativeTime, formatAbsoluteTime } from '../../utils/formatRelativeTime';
import { useNavigate } from 'react-router-dom';

type Activity = {
  timeStamp: string // ISO 8601
  details: string
}

type Case = {
  id: string
  case_number: string
  title: string
  status: string
}

// TODO: replace with a real fetch once a recent-activity endpoint exists
// (nothing currently aggregates AuditLog/ChainOfCustody/Report into a
// feed like this — /api/dashboard/summary only returns counts). Seeded
// here as placeholder data so the section isn't permanently empty in the
// meantime. Timestamps are real ISO strings so formatRelativeTime can
// actually parse them.
const tmpActivity: Activity[] = [
  {
    timeStamp: "2026-07-07T14:32:00Z",
    details: "Evidence EV-0093 imaged — CM-2026-0142"
  },
  {
    timeStamp: "2026-07-07T11:05:00Z",
    details: "Report RPT-0021 saved as draft — CM-2026-0142"
  },
  {
    timeStamp: "2026-07-07T09:47:00Z",
    details: "Custody transfer logged for EV-0091"
  },
  {
    timeStamp: "2026-07-06T00:00:00Z",
    details: "Case CM-2026-0139 moved to In Review"
  }
]

function Dashboard() {
  const { stats, isLoading } = useDashboardStats();
  const { getAccessToken } = useAuth();

  const [recentActivities] = useState<Activity[]>(tmpActivity);
  const [openCases, setOpenCases] = useState<Case[]>([]);
  const [localLoading, setLocalLoading] = useState<boolean>(true);
  const navigate = useNavigate()

  useEffect(() => {
    let cancelled = false;

    (async () => {
      setLocalLoading(true);
      try {
        const token = await getAccessToken();
        const res = await fetch('/api/cases/', {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
          credentials: 'include',
        });
        if (!res.ok) throw new Error(`Failed to load cases (${res.status})`);

        const allCases: Case[] = await res.json();
        if (!cancelled) {
          setOpenCases(allCases.filter((c) => c.status === 'open'));
        }
      } catch (err) {
        console.log(`Error: ${err}`);
      } finally {
        if (!cancelled) setLocalLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [getAccessToken]);

  return (
    <main id="dashboard">
      <div id="dashboard-row">
        <div className="dashboard-card">
          {/* TODO: Update changes section to be dynamic and reflect real data */}
          <h2 className="dashboard-card-title">Active Cases</h2>
          <p className="dashboard-card-content">{isLoading ? '—' : stats?.activeCases ?? 0}</p>
          <p className="dashboard-card-subcontent">
            {isLoading ? '' : `of total ${stats?.totalCases ?? 0} cases`}
          </p>
          <p className="dashboard-card-change up">+1 this month</p>
        </div>
        <div className="dashboard-card">
          <h2 className="dashboard-card-title">Evidence Items</h2>
          <p className="dashboard-card-content">{isLoading ? '—' : stats?.evidenceItemsTotal ?? 0}</p>
          <p className="dashboard-card-subcontent">tracked across all cases</p>
          <p className="dashboard-card-change">no change</p>
        </div>
        <div className="dashboard-card">
          <h2 className="dashboard-card-title">Pending Reviews</h2>
          <p className="dashboard-card-content">{isLoading ? '—' : stats?.pendingReviews ?? 0}</p>
          <p className="dashboard-card-subcontent">reports awaiting sign-off</p>
          <p className="dashboard-card-change">0 due this week</p>
        </div>
        <div className="dashboard-card">
          <h2 className="dashboard-card-title">Custody Integrity</h2>
          <p className="dashboard-card-content">
            {isLoading ? '—' : `${stats?.custodyIntegrityPercent ?? 0}%`}
          </p>
          <p className="dashboard-card-subcontent">hash-chain verified</p>
        </div>
      </div>

      <div id="dashboard-grid">
        <div className="dashboard-card">
          <h2 className="dashboard-card-title">Recent Activities</h2>
          <table className="dashboard-activity-table">
            <tbody>
              {recentActivities.map((activity, index) => (
                // Using index as a fallback key since placeholder data has
                // no stable id — once this is backed by real records
                // (e.g. an AuditLog id), key off that instead.
                <tr key={index} className="dashboard-activity-row">
                  <td className='dashboard-activity-timeline'>
                    {new Date(activity.timeStamp).toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                      hour12: false,
                    })}
                  </td>
                  <td className="dashboard-activity-details">{activity.details}</td>
                  <td
                    className="dashboard-activity-time"
                    title={formatAbsoluteTime(activity.timeStamp)}
                  >
                    {formatRelativeTime(activity.timeStamp)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="dashboard-card">
          <h2 className="dashboard-card-title">Open Cases</h2>
          {localLoading && <p className="dashboard-card-subcontent">Loading…</p>}
          {!localLoading && openCases.length === 0 && (
            <p className="dashboard-card-subcontent">No open cases</p>
          )}
          {!localLoading &&
            openCases.map((c) => (
              <div key={c.id} className="dashboard-case-row" onClick={() =>  navigate(`/cases/${c.id}`)}>
                <div className='dashboard-case-information'>
                  <span className="dashboard-case-number">{c.case_number}</span>
                  <span className="dashboard-case-title">{c.title}</span>
                </div>
                <div className={`dashboard-case-status ${c.status == 'open' ? 'active' : ''}`}>{c.status}</div>
              </div>
            ))}
        </div>
      </div>
    </main>
  )
}
export default Dashboard
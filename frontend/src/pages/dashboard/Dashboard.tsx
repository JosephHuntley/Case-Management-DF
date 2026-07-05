import React from 'react'
import "./Dashboard.css"
import { useDashboardStats } from './useDashboardStats';

function Dashboard() {
  const { stats, isLoading } = useDashboardStats();

  return (
    <main id="dashboard">
      <div id="dashboard-row">

        <div className="dashboard-card">
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
    </main>
  )
}
export default Dashboard
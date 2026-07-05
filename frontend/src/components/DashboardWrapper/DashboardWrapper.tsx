import React from 'react'
import Sidebar from './Sidebar/Sidebar'
import './DashboardWrapper.css'

function DashboardWrapper({children}: {children: React.ReactNode}) {
  return (
    <div id="dashboard-wrapper">
        <Sidebar />
        <div>
            <div>Topbar</div>
            <div>{children}</div>
        </div>
    </div>
  )
}

export default DashboardWrapper
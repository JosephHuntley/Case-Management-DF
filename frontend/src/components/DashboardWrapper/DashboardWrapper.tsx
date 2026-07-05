import React from 'react'
import Sidebar from './Sidebar/Sidebar'
import './DashboardWrapper.css'

function DashboardWrapper({children}: {children: React.ReactNode}) {
  return (
    <div id="dashboard-wrapper">
        <Sidebar />
        <div>
            <div id="topbar">
              <div> 

                <div id="topbar-title">Dashboard</div>
                <div id="topbar-message">Overview across all cases</div>
              </div>
              {/* TODO: May implement search function in the future */}
              {/* <div id="search">Search case, evidence ID...</div> */}
            </div>
            <div>{children}</div>
        </div>
    </div>
  )
}

export default DashboardWrapper
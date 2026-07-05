import React from 'react'
import Sidebar from './Sidebar/Sidebar'
import './DashboardWrapper.css'
import SearchBar from './search/SearchBar'

function DashboardWrapper({children}: {children: React.ReactNode}) {
  return (
    <div id="dashboard-wrapper">
        <Sidebar />
        <div style={{"width":"85%"}}>
            <div id="topbar">
              <div> 

                <div id="topbar-title">Dashboard</div>
                <div id="topbar-message">Overview across all cases</div>
              </div>
              <SearchBar/>
            </div>
            <div>{children}</div>
        </div>
    </div>
  )
}

export default DashboardWrapper
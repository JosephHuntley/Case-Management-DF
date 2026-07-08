import React, { useEffect, useState } from 'react'
import Sidebar from './Sidebar/Sidebar'
import './DashboardWrapper.css'
import SearchBar from './search/SearchBar'
import { useLocation } from 'react-router-dom'

function DashboardWrapper({children}: {children: React.ReactNode}) {
  const location = useLocation()
  const [title, setTitle] = useState<string>()

  useEffect(() => {
    const path = location.pathname

    switch(path){
      case '/':
        setTitle("Dashboard")
        break
      case '/cases':
        setTitle("Cases")
        break
      case '/evidence':
        setTitle("Evidence")
        break
      case '/chainofcustody':
        setTitle('Chain of Custody')
        break
      case '/reports':
        setTitle('Reports')
        break
    }

  

  }, [location.pathname])
  

  return (
    <div id="dashboard-wrapper">
        <Sidebar />
        <div style={{"width":"85%"}}>
            <div id="topbar">
              <div> 
                <div id="topbar-title">{title}</div>
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
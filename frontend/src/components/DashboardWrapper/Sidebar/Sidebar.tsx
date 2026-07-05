import './Sidebar.css'
import { LayoutDashboard, Folder, Shield, Link, StickyNote, User } from 'lucide-react'
import { Link as RouterLink, useLocation } from 'react-router-dom'
import { useAuth } from '../../../context/AuthContext'

function Sidebar() {
  const { user } = useAuth()
  const location = useLocation()

  const isAdmin = user?.role === 'admin'
  const initials = user ? `${user.firstName.charAt(0)}${user.lastName.charAt(0)}`.toUpperCase() : ''

  // "/" needs an exact match (otherwise it'd match every route). Everything
  // else uses startsWith so nested routes (e.g. /cases/123 later) still
  // highlight the parent nav item.
  const isActive = (path: string) =>
    path === '/' ? location.pathname === '/' : location.pathname.startsWith(path)

  return (
    <nav id="sidebar">
        <div id="sidebar-header">
            <div id="sidebar-logo">CM</div>
            <div id="sidebar-header-text">
                <div id="title">Case-Mgmt-DF</div>
                <div className="sidebar-header-title" >case-df.local</div>
            </div>
        </div>
        <span className="sidebar-title" style={{"marginBottom": "10px"}}>WORKSPACE</span>
        <ul id="sidebar-list">
            <li>
              <RouterLink to="/" className={`sidebar-item ${isActive('/') ? 'active' : ''}`}>
                <LayoutDashboard size={13} /> Dashboard
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/cases" className={`sidebar-item ${isActive('/cases') ? 'active' : ''}`}>
                <Folder size={13}/> Cases
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/evidence" className={`sidebar-item ${isActive('/evidence') ? 'active' : ''}`}>
                <Shield size={13}/> Evidence
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/chainofcustody" className={`sidebar-item ${isActive('/chainofcustody') ? 'active' : ''}`}>
                <Link size={13}/> Chain of Custody
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/reports" className={`sidebar-item ${isActive('/reports') ? 'active' : ''}`}>
                <StickyNote size={13}/> Reports
              </RouterLink>
            </li>
        </ul>
        {isAdmin && (
          <>
            <span className="sidebar-title" style={{"marginBottom": "10px"}}>System</span>
            <ul id="sidebar-list">
                <li>
                  <RouterLink to="/users-roles" className={`sidebar-item ${isActive('/users') ? 'active' : ''}`}>
                    <User size={13} /> Users & Roles
                  </RouterLink>
                </li>
            </ul>
          </>
        )}

        <div id="sidebar-profile">
            <div id="sidebar-initials">{initials || '—'}</div>
            <div className="sidebar-profile-info">
                <div className="sidebar-user">{user ? `${user.firstName.charAt(0)}. ${user.lastName}` : 'Loading…'}</div>
                <div className="sidebar-role">{user?.role ?? ''}</div>
            </div>
        </div>

    </nav>
  )
}
export default Sidebar
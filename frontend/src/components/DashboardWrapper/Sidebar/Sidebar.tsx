import './Sidebar.css'
import { LayoutDashboard, Folder, Shield, Link, StickyNote, User } from 'lucide-react'
import { useAuth } from '../../../context/AuthContext'

function Sidebar() {
  const { user } = useAuth()
  const isAdmin = user?.role === 'admin'
  const initials = user ? `${user.firstName.charAt(0)}${user.lastName.charAt(0)}`.toUpperCase() : ''

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
        {/* TODO Add logic to determine logic of active item */}
        <ul id="sidebar-list">
            <li className="sidebar-item active"> <LayoutDashboard size={13} /> Dashboard</li>
            <li className="sidebar-item"><Folder size={13}/> Cases</li>
            <li className="sidebar-item"><Shield size={13}/> Evidence</li>
            <li className="sidebar-item"><Link size={13}/> Chain of Custody</li>
            <li className="sidebar-item"><StickyNote size={13}/> Reports</li>
        </ul>
        {isAdmin && (
          <>
            <span className="sidebar-title" style={{"marginBottom": "10px"}}>System</span>
            <ul id="sidebar-list">
                <li className="sidebar-item"> <User size={13} /> Users & Roles</li>
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
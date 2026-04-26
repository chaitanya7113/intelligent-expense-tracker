import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-layout">
      <nav className="nav">
        <span className="nav-brand">Intelligent Expense Tracker</span>
        <div className="nav-links">
          <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>Dashboard</NavLink>
          <NavLink to="/expenses" className={({ isActive }) => isActive ? 'active' : ''}>Expenses</NavLink>
          <NavLink to="/expenses/add" className={({ isActive }) => isActive ? 'active' : ''}>Add Expense</NavLink>
          <NavLink to="/analytics" className={({ isActive }) => isActive ? 'active' : ''}>Analytics</NavLink>
          <NavLink to="/ai-agent" className={({ isActive }) => isActive ? 'active' : ''}>AI Agent</NavLink>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{user?.username}</span>
          <button type="button" className="btn btn-ghost" onClick={handleLogout}>Logout</button>
        </div>
      </nav>
      <main>
        <Outlet />
      </main>
    </div>
  )
}

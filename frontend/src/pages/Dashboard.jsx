import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { analytics } from '../api/endpoints'

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    analytics.summary()
      .then(({ data }) => { if (!cancelled) setSummary(data) })
      .catch((error) => { console.error('error', error); if (!cancelled) setError('Failed to load summary') })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [])

  if (loading) return <div className="container">Loading...</div>
  if (error) return <div className="container"><p className="error-msg">{error}</p></div>

  const total = summary?.total_spending ?? 0
  const count = summary?.count_expenses ?? 0

  const income = summary?.total_income ?? 0
  const net = summary?.net ?? 0
  const incomeCount = summary?.count_incomes ?? 0

  return (
    <div className="container">
      <h1 className="page-title ">Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '1rem' }}>
        <div className="card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '0.25rem' }}>This month</div>
          <div style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--accent)' }}>
            {new Intl.NumberFormat('en-IN', {
              style: 'currency',
              currency: 'INR',
              maximumFractionDigits: 0,
            }).format(total)}
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{count} expenses</div>
        </div>
        <div className="card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '0.25rem' }}>Income (this month)</div>
          <div style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--accent)' }}>
            {new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(income)}
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{incomeCount} incomes</div>
        </div>

        <div className="card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '0.25rem' }}>Net (this month)</div>
          <div style={{ fontSize: '1.75rem', fontWeight: 700 }}>
            {new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(net)}
          </div>
        </div>
        <div className="card">
          <Link to="/expenses/add" className="btn btn-primary" style={{ display: 'inline-block' }}>Add Expense</Link>
          <p style={{ marginTop: '0.75rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>Record a new expense</p>
        </div>
        <div className="card">
          <Link to="/expenses" className="btn btn-ghost" style={{ display: 'inline-block' }}>View all expenses</Link>
          <p style={{ marginTop: '0.75rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>Filter and manage</p>
        </div>
        <div className="card">
          <Link to="/analytics" className="btn btn-ghost" style={{ display: 'inline-block' }}>Analytics</Link>
          <p style={{ marginTop: '0.75rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>Charts and breakdown</p>
        </div>
      </div>
    </div>
  )
}

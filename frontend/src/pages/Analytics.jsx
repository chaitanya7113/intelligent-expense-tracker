import { useState, useEffect } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts'
import { analytics } from '../api/endpoints'

const COLORS = ['#00d4aa', '#00a884', '#2a2a32', '#9898a6', '#ffa502', '#ff4757', '#7b68ee', '#20b2aa']

export default function Analytics() {
  const [summary, setSummary] = useState(null)
  const [byCategory, setByCategory] = useState([])
  const [monthlyComparison, setMonthlyComparison] = useState([])
  const [year, setYear] = useState(new Date().getFullYear())
  const [month, setMonth] = useState(new Date().getMonth() + 1)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    Promise.all([
      analytics.summary({ year, month }),
      analytics.byCategory({ year, month }),
      analytics.monthlyComparison({ months: 6 }),
    ])
      .then(([s, c, m]) => {
        if (cancelled) return
        setSummary(s.data)
        setByCategory(c.data)
        setMonthlyComparison(m.data)
      })
      .catch(() => {})
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [year, month])

  if (loading) return <div className="container">Loading...</div>

  const pieData = byCategory.map((item) => ({
    name: item.category_name || 'Uncategorized',
    value: item.total,
  }))

  return (
    <div className="container">
      <h1 className="page-title">Analytics</h1>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label>Year</label>
          <select value={year} onChange={(e) => setYear(Number(e.target.value))} style={{ minWidth: 100 }}>
            {[year - 2, year - 1, year, year + 1].map((y) => (
              <option key={y} value={y}>{y}</option>
            ))}
          </select>
        </div>
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label>Month</label>
          <select value={month} onChange={(e) => setMonth(Number(e.target.value))} style={{ minWidth: 120 }}>
            {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
              <option key={m} value={m}>{new Date(2000, m - 1).toLocaleString('default', { month: 'long' })}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="card">
        <h2 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Monthly summary</h2>
        <p style={{ color: 'var(--text-muted)' }}>Total: {summary?.total_spending?.toLocaleString() ?? 0} ({summary?.count ?? 0} expenses)</p>
      </div>
      <div className="card">
        <h2 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Spending by category</h2>
        {pieData.length === 0 ? (
          <p className="empty-state">No data for this period</p>
        ) : (
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {pieData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v) => v.toLocaleString()} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
      <div className="card">
        <h2 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Monthly comparison (last 6 months)</h2>
        {monthlyComparison.length === 0 ? (
          <p className="empty-state">No data</p>
        ) : (
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyComparison} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <XAxis dataKey="month_label" tick={{ fill: 'var(--text-muted)', fontSize: 12 }} />
                <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 12 }} />
                <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border)' }} formatter={(v) => v.toLocaleString()} />
                <Bar dataKey="total_spending" fill="var(--accent)" radius={[4, 4, 0, 0]} name="Spending" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}

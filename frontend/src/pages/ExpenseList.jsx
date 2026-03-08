import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { expenses, categories as catApi } from '../api/endpoints'

export default function ExpenseList() {
  const [items, setItems] = useState([])
  const [nextPage, setNextPage] = useState(null)
  const [prevPage, setPrevPage] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [category, setCategory] = useState('')
  const [categories, setCategories] = useState([])
  const [editingId, setEditingId] = useState(null)
  const [editAmount, setEditAmount] = useState('')
  const [editDate, setEditDate] = useState('')
  const [editCategoryId, setEditCategoryId] = useState('')
  const [editDesc, setEditDesc] = useState('')

  const fetchList = (params = {}) => {
    setLoading(true)
    const p = { ...params }
    if (dateFrom) p.date_from = dateFrom
    if (dateTo) p.date_to = dateTo
    if (category) p.category = category
    expenses.list(p)
      .then(({ data }) => {
        setItems(data.results || [])
        setNextPage(data.next)
        setPrevPage(data.previous)
      })
      .catch(() => setError('Failed to load expenses'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchList() }, [])
  useEffect(() => {
    catApi.list().then(({ data }) => setCategories(data)).catch(() => {})
  }, [])

  const applyFilters = () => fetchList()

  const handleDelete = (id) => {
    if (!window.confirm('Delete this expense?')) return
    expenses.delete(id).then(() => fetchList()).catch(() => setError('Delete failed'))
  }

  const startEdit = (row) => {
    setEditingId(row.id)
    setEditAmount(String(row.amount))
    setEditDate(row.date)
    setEditCategoryId(row.category ? String(row.category) : '')
    setEditDesc(row.description || '')
  }

  const saveEdit = async () => {
    if (!editingId) return
    setError('')
    try {
      await expenses.update(editingId, {
        amount: parseFloat(editAmount),
        date: editDate,
        category: editCategoryId ? parseInt(editCategoryId, 10) : null,
        description: editDesc,
      })
      setEditingId(null)
      fetchList()
    } catch (e) {
      setError('Update failed')
    }
  }

  const cancelEdit = () => setEditingId(null)

  const pageFromUrl = (url) => (url ? new URL(url).searchParams.get('page') : null)

  return (
    <div className="container">
      <h1 className="page-title">Expenses</h1>
      <div className="card" style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', alignItems: 'flex-end' }}>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>From</label>
            <input type="date" value={dateFrom} onChange={(e) => setDateFrom(e.target.value)} />
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>To</label>
            <input type="date" value={dateTo} onChange={(e) => setDateTo(e.target.value)} />
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Category</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ minWidth: 140 }}>
              <option value="">All</option>
              {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>
          <button type="button" className="btn btn-primary" onClick={applyFilters}>Filter</button>
        </div>
      </div>
      {error && <p className="error-msg">{error}</p>}
      <div className="card">
        {loading ? (
          <p className="empty-state">Loading...</p>
        ) : items.length === 0 ? (
          <p className="empty-state">No expenses. <Link to="/expenses/add">Add one</Link></p>
        ) : (
          <>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Amount</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((row) => (
                    <tr key={row.id}>
                      {editingId === row.id ? (
                        <>
                          <td><input type="date" value={editDate} onChange={(e) => setEditDate(e.target.value)} style={{ padding: '0.35rem', width: '100%', background: 'var(--bg-input)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', color: 'var(--text)' }} /></td>
                          <td><input type="number" step="0.01" value={editAmount} onChange={(e) => setEditAmount(e.target.value)} style={{ padding: '0.35rem', width: 100, background: 'var(--bg-input)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', color: 'var(--text)' }} /></td>
                          <td>
                            <select value={editCategoryId} onChange={(e) => setEditCategoryId(e.target.value)} style={{ padding: '0.35rem', minWidth: 120, background: 'var(--bg-input)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', color: 'var(--text)' }}>
                              <option value="">—</option>
                              {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                            </select>
                          </td>
                          <td><input type="text" value={editDesc} onChange={(e) => setEditDesc(e.target.value)} style={{ padding: '0.35rem', width: '100%', background: 'var(--bg-input)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', color: 'var(--text)' }} /></td>
                          <td>
                            <button type="button" className="btn btn-primary" style={{ marginRight: '0.25rem' }} onClick={saveEdit}>Save</button>
                            <button type="button" className="btn btn-ghost" onClick={cancelEdit}>Cancel</button>
                          </td>
                        </>
                      ) : (
                        <>
                          <td>{row.date}</td>
                          <td>{parseFloat(row.amount).toLocaleString()}</td>
                          <td>{row.category_name || '—'}</td>
                          <td>{row.description || '—'}</td>
                          <td>
                            <button type="button" className="btn btn-ghost" onClick={() => startEdit(row)}>Edit</button>
                            <button type="button" className="btn btn-danger" style={{ marginLeft: '0.25rem' }} onClick={() => handleDelete(row.id)}>Delete</button>
                          </td>
                        </>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="pagination">
              <button type="button" disabled={!prevPage} onClick={() => prevPage && fetchList({ page: pageFromUrl(prevPage) })}>Previous</button>
              <button type="button" disabled={!nextPage} onClick={() => nextPage && fetchList({ page: pageFromUrl(nextPage) })}>Next</button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

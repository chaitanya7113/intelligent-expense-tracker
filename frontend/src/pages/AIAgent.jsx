import { useState, useRef, useEffect } from 'react'
import { agent } from '../api/endpoints'

const SUGGESTIONS = [
  'How much did I spend this month?',
  'What are my top spending categories?',
  'Show me my spending trend',
  'Give me tips to save money',
]

export default function AIAgent() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        "Hi! I'm your AI expense assistant. Ask me anything about your spending, categories, trends, or tips to save money.",
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const msgCountRef = useRef(messages.length)

  useEffect(() => {
    if (messages.length !== msgCountRef.current) {
      msgCountRef.current = messages.length
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages])

  const sendMessage = async (text) => {
    const message = (text || input).trim()
    if (!message || loading) return

    const history = messages
      .filter((m) => m.role !== 'error')
      .map((m) => ({ role: m.role, content: m.content }))

    setMessages((prev) => [...prev, { role: 'user', content: message }])
    setInput('')
    setLoading(true)

    try {
      const { data } = await agent.chat({ message, history })
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'error', content: 'Something went wrong. Please try again.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="container" style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 64px)' }}>
      <h1 className="page-title">AI Expense Assistant</h1>

      {/* Quick suggestions */}
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            type="button"
            className="btn btn-ghost"
            style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem', border: '1px solid var(--border)' }}
            onClick={() => sendMessage(s)}
            disabled={loading}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Chat messages */}
      <div
        className="card"
        style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem', padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}
      >
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              display: 'flex',
              justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start',
            }}
          >
            <div
              style={{
                maxWidth: '75%',
                padding: '0.65rem 1rem',
                borderRadius: '12px',
                fontSize: '0.95rem',
                lineHeight: 1.5,
                background:
                  m.role === 'user'
                    ? 'var(--accent)'
                    : m.role === 'error'
                    ? 'rgba(255,71,87,0.15)'
                    : 'var(--bg-input)',
                color:
                  m.role === 'user'
                    ? 'var(--bg)'
                    : m.role === 'error'
                    ? 'var(--danger)'
                    : 'var(--text)',
                border: m.role === 'error' ? '1px solid var(--danger)' : 'none',
                whiteSpace: 'pre-wrap',
              }}
            >
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
            <div
              style={{
                padding: '0.65rem 1rem',
                borderRadius: '12px',
                background: 'var(--bg-input)',
                color: 'var(--text-muted)',
                fontSize: '0.9rem',
              }}
            >
              Thinking…
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <textarea
          className="form-group"
          style={{
            flex: 1,
            margin: 0,
            padding: '0.65rem 0.85rem',
            background: 'var(--bg-input)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius)',
            color: 'var(--text)',
            fontSize: '1rem',
            resize: 'none',
            minHeight: '46px',
            maxHeight: '120px',
          }}
          placeholder="Ask about your expenses…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          rows={1}
        />
        <button
          type="button"
          className="btn btn-primary"
          style={{ alignSelf: 'flex-end', minWidth: '80px' }}
          onClick={() => sendMessage()}
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  )
}

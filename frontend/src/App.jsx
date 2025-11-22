import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Send, Shield, ExternalLink, Globe } from 'lucide-react'
import './index.css'

const REGIONS = {
  HK: { name: 'Hong Kong', color: '#EF4444', flag: '🇭🇰' },
  JP: { name: 'Japan', color: '#3B82F6', flag: '🇯🇵' },
  NYC: { name: 'New York City', color: '#10B981', flag: '🗽' }
}

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedRegion, setSelectedRegion] = useState(null)
  const chatEndRef = useRef(null)

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const themeColor = selectedRegion ? REGIONS[selectedRegion].color : '#6B7280'

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/query', {
        query: input,
        region: selectedRegion
      })

      const botMessage = {
        role: 'bot',
        content: response.data.answer,
        sources: response.data.sources
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error querying chatbot:', error)
      const errorMessage = error.response?.data?.detail || error.message || 'Unknown error'
      setMessages(prev => [...prev, {
        role: 'bot',
        content: `Error: ${errorMessage}. Please check console/logs.`
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      <header className="header" style={{ backgroundColor: themeColor }}>
        <Shield size={28} />
        <h1>
          {selectedRegion
            ? `${REGIONS[selectedRegion].flag} ${REGIONS[selectedRegion].name} Cyber Intelligence`
            : '🌐 Global Cyber Intelligence'}
        </h1>
      </header>

      <div className="main-container">
        {/* Region Selector */}
        <div className="region-selector">
          <div className="region-label">
            <Globe size={16} />
            <span>Select Region:</span>
          </div>
          <div className="region-buttons">
            <button
              className={`region-btn ${selectedRegion === null ? 'active' : ''}`}
              onClick={() => setSelectedRegion(null)}
              style={{
                borderColor: selectedRegion === null ? '#6B7280' : '#E5E7EB',
                backgroundColor: selectedRegion === null ? '#6B7280' : 'transparent',
                color: selectedRegion === null ? 'white' : '#6B7280'
              }}
            >
              🌐 All Regions
            </button>
            {Object.entries(REGIONS).map(([code, region]) => (
              <button
                key={code}
                className={`region-btn ${selectedRegion === code ? 'active' : ''}`}
                onClick={() => setSelectedRegion(code)}
                style={{
                  borderColor: selectedRegion === code ? region.color : '#E5E7EB',
                  backgroundColor: selectedRegion === code ? region.color : 'transparent',
                  color: selectedRegion === code ? 'white' : region.color
                }}
              >
                {region.flag} {region.name}
              </button>
            ))}
          </div>
        </div>

        <div className="chat-area">
          {messages.length === 0 && (
            <div style={{
              textAlign: 'center',
              color: 'var(--text-secondary)',
              marginTop: '4rem',
              fontSize: '1.125rem'
            }}>
              <Shield size={48} style={{ margin: '0 auto 1rem', display: 'block', color: themeColor }} />
              <p>Ask me anything about cybersecurity</p>
              <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                {selectedRegion
                  ? `Information from ${REGIONS[selectedRegion].name} government sources only.`
                  : 'Information from Hong Kong, Japan, and New York City government sources.'}
              </p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div
                className={`avatar ${msg.role}`}
                style={msg.role === 'bot' ? { backgroundColor: themeColor } : {}}
              >
                {msg.role === 'bot' ? <Shield size={20} /> : 'U'}
              </div>
              <div
                className="bubble"
                style={msg.role === 'user' ? { backgroundColor: themeColor } : {}}
              >
                <div>
                  {msg.content}
                  {msg.sources && msg.sources.length > 0 && msg.role === 'bot' && (
                    <span style={{ marginLeft: '0.5rem' }}>
                      {msg.sources.map((source, i) => (
                        <a
                          key={i}
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-source"
                          style={{
                            color: themeColor,
                            textDecoration: 'none',
                            fontSize: '0.75rem',
                            verticalAlign: 'super',
                            marginLeft: '0.125rem',
                            fontWeight: '600'
                          }}
                          title={source.title}
                        >
                          [{i + 1}]
                        </a>
                      ))}
                    </span>
                  )}
                </div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="sources">
                    <div className="sources-title" style={{ color: themeColor }}>
                      <ExternalLink size={14} />
                      Sources:
                    </div>
                    {msg.sources.map((source, i) => (
                      <a
                        key={i}
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="source-link"
                        style={{ color: themeColor }}
                        title={source.title}
                      >
                        [{i + 1}] {source.region && `[${source.region}] `}{source.title}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message bot">
              <div className="avatar bot" style={{ backgroundColor: themeColor }}>
                <Shield size={20} />
              </div>
              <div className="bubble">
                <div className="loading-dots">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                </div>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        <div className="input-area">
          <input
            type="text"
            className="input-field"
            placeholder={`Ask about cybersecurity${selectedRegion ? ` in ${REGIONS[selectedRegion].name}` : ''}...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
            style={{ borderColor: loading ? '#E5E7EB' : themeColor }}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={loading || !input.trim()}
            style={{ backgroundColor: loading || !input.trim() ? '#E5E7EB' : themeColor }}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </>
  )
}

export default App

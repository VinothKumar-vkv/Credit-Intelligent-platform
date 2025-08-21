import React, { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [issuers, setIssuers] = useState([])
  const [scores, setScores] = useState([])
  const [events, setEvents] = useState([])
  const [selected, setSelected] = useState(null)
  const [loading, setLoading] = useState(true)
  const [hoveredCard, setHoveredCard] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [issuersRes, scoresRes, eventsRes] = await Promise.all([
          fetch(`${API}/v1/issuers/`),
          fetch(`${API}/v1/scores?limit=50`),
          fetch(`${API}/v1/events?limit=50`)
        ])
        
        const [issuersData, scoresData, eventsData] = await Promise.all([
          issuersRes.json(),
          scoresRes.json(),
          eventsRes.json()
        ])
        
        setIssuers(issuersData)
        setScores(scoresData)
        setEvents(eventsData)
        setLoading(false)
      } catch (error) {
        console.error('Error fetching data:', error)
        setLoading(false)
      }
    }
    
    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const getScoreColor = (score) => {
    if (score > 1000000) return '#00ff88' // Bright green for high scores
    if (score > 100000) return '#ffaa00' // Bright orange for medium scores
    return '#ff4444' // Bright red for low scores
  }

  const getSentimentColor = (sentiment) => {
    if (sentiment > 0.1) return '#00ff88' // Bright green for positive
    if (sentiment < -0.1) return '#ff4444' // Bright red for negative
    return '#8888ff' // Bright blue for neutral
  }

  const getIssuerColor = (ticker) => {
    const colors = {
      'AAPL': '#ff6b6b', // Coral red
      'MSFT': '#4ecdc4', // Turquoise
      'TSLA': '#45b7d1', // Sky blue
      'AMZN': '#96ceb4'  // Mint green
    }
    return colors[ticker] || '#a8e6cf'
  }

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57, #ff9ff3)',
        backgroundSize: '400% 400%',
        animation: 'gradientShift 3s ease infinite',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        fontSize: '24px'
      }}>
        <style>
          {`
            @keyframes gradientShift {
              0% { background-position: 0% 50%; }
              50% { background-position: 100% 50%; }
              100% { background-position: 0% 50%; }
            }
            @keyframes pulse {
              0% { transform: scale(1); }
              50% { transform: scale(1.1); }
              100% { transform: scale(1); }
            }
            @keyframes float {
              0% { transform: translateY(0px); }
              50% { transform: translateY(-10px); }
              100% { transform: translateY(0px); }
            }
            @keyframes glow {
              0% { box-shadow: 0 0 5px rgba(255,255,255,0.5); }
              50% { box-shadow: 0 0 20px rgba(255,255,255,0.8); }
              100% { box-shadow: 0 0 5px rgba(255,255,255,0.5); }
            }
          `}
        </style>
        <div style={{ textAlign: 'center', animation: 'pulse 2s ease-in-out infinite' }}>
          <div style={{ fontSize: '64px', marginBottom: '16px', animation: 'float 3s ease-in-out infinite' }}>🚀</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', textShadow: '2px 2px 4px rgba(0,0,0,0.3)' }}>
            Loading Credit Intelligence Platform...
          </div>
          <div style={{ marginTop: '16px', opacity: 0.8 }}>✨ Preparing your financial insights ✨</div>
        </div>
      </div>
    )
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)',
      backgroundSize: '400% 400%',
      animation: 'gradientShift 15s ease infinite',
      fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
      color: 'white',
      position: 'relative',
      overflow: 'hidden'
    }}>
      <style>
        {`
          @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }
          @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
          }
          @keyframes glow {
            0% { box-shadow: 0 0 5px rgba(255,255,255,0.3); }
            50% { box-shadow: 0 0 20px rgba(255,255,255,0.6); }
            100% { box-shadow: 0 0 5px rgba(255,255,255,0.3); }
          }
          @keyframes slideIn {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
          }
          @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
          }
        `}
      </style>

      {/* Floating Background Elements */}
      <div style={{
        position: 'absolute',
        top: '10%',
        left: '5%',
        fontSize: '48px',
        animation: 'float 6s ease-in-out infinite',
        opacity: 0.1
      }}>💎</div>
      <div style={{
        position: 'absolute',
        top: '20%',
        right: '10%',
        fontSize: '36px',
        animation: 'float 8s ease-in-out infinite',
        opacity: 0.1
      }}>📈</div>
      <div style={{
        position: 'absolute',
        bottom: '20%',
        left: '15%',
        fontSize: '42px',
        animation: 'float 7s ease-in-out infinite',
        opacity: 0.1
      }}>🎯</div>

      {/* Header */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.15)',
        backdropFilter: 'blur(20px)',
        borderBottom: '2px solid rgba(255, 255, 255, 0.3)',
        padding: '30px 0',
        marginBottom: '40px',
        animation: 'glow 3s ease-in-out infinite'
      }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 20px' }}>
          <h1 style={{
            margin: 0,
            fontSize: '42px',
            fontWeight: '800',
            background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            textAlign: 'center',
            textShadow: '0 0 30px rgba(255,255,255,0.5)',
            animation: 'bounce 2s ease-in-out infinite'
          }}>
            🏆 Credit Intelligence Platform 🏆
          </h1>
          <p style={{
            textAlign: 'center',
            margin: '12px 0 0 0',
            opacity: 0.9,
            fontSize: '18px',
            fontWeight: '500',
            textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
          }}>
            ✨ Real-Time Explainable Credit Risk Analysis ✨
          </p>
        </div>
      </div>

      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 20px' }}>
        {/* Stats Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '25px',
          marginBottom: '40px'
        }}>
          {[
            { icon: '📊', title: 'Active Issuers', value: issuers.length, color: '#ff6b6b' },
            { icon: '📈', title: 'Credit Scores', value: scores.length, color: '#4ecdc4' },
            { icon: '📰', title: 'News Events', value: events.length, color: '#45b7d1' },
            { icon: '⚡', title: 'Real-Time', value: 'LIVE', color: '#96ceb4' }
          ].map((stat, index) => (
            <div
              key={index}
              onMouseEnter={() => setHoveredCard(index)}
              onMouseLeave={() => setHoveredCard(null)}
              style={{
                background: `linear-gradient(135deg, ${stat.color}20, ${stat.color}40)`,
                backdropFilter: 'blur(15px)',
                borderRadius: '20px',
                padding: '30px',
                border: `2px solid ${stat.color}60`,
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                transform: hoveredCard === index ? 'scale(1.05) translateY(-5px)' : 'scale(1)',
                boxShadow: hoveredCard === index 
                  ? `0 20px 40px rgba(0,0,0,0.3), 0 0 20px ${stat.color}40`
                  : '0 10px 30px rgba(0,0,0,0.2)',
                animation: 'slideIn 0.6s ease-out'
              }}
            >
              <div style={{ 
                fontSize: '48px', 
                marginBottom: '12px',
                animation: 'float 4s ease-in-out infinite',
                filter: hoveredCard === index ? 'drop-shadow(0 0 10px rgba(255,255,255,0.5))' : 'none'
              }}>
                {stat.icon}
              </div>
              <div style={{ 
                fontSize: '32px', 
                fontWeight: '700',
                color: stat.color,
                textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
                marginBottom: '8px'
              }}>
                {stat.value}
              </div>
              <div style={{ 
                opacity: 0.9, 
                fontSize: '16px',
                fontWeight: '500',
                textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
              }}>
                {stat.title}
              </div>
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 2fr', gap: '30px', marginBottom: '40px' }}>
          {/* Issuers Panel */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(255,107,107,0.2), rgba(78,205,196,0.2))',
            backdropFilter: 'blur(15px)',
            borderRadius: '20px',
            padding: '30px',
            border: '2px solid rgba(255,255,255,0.3)',
            height: 'fit-content',
            boxShadow: '0 15px 35px rgba(0,0,0,0.2)'
          }}>
            <h3 style={{ 
              margin: '0 0 25px 0', 
              fontSize: '24px', 
              fontWeight: '700',
              textAlign: 'center',
              textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
            }}>
              🏢 Issuers
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              {issuers.map(i => (
                <button
                  key={i.id}
                  onClick={() => setSelected(i)}
                  style={{
                    background: selected?.id === i.id 
                      ? `linear-gradient(135deg, ${getIssuerColor(i.ticker)}80, ${getIssuerColor(i.ticker)}60)`
                      : `linear-gradient(135deg, ${getIssuerColor(i.ticker)}30, ${getIssuerColor(i.ticker)}20)`,
                    border: `2px solid ${getIssuerColor(i.ticker)}80`,
                    borderRadius: '15px',
                    padding: '20px',
                    color: 'white',
                    fontSize: '18px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    textAlign: 'left',
                    boxShadow: selected?.id === i.id 
                      ? `0 10px 25px rgba(0,0,0,0.3), 0 0 15px ${getIssuerColor(i.ticker)}60`
                      : '0 5px 15px rgba(0,0,0,0.2)',
                    transform: selected?.id === i.id ? 'scale(1.02)' : 'scale(1)'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.transform = 'scale(1.05) translateY(-2px)'
                    e.target.style.boxShadow = `0 15px 30px rgba(0,0,0,0.3), 0 0 20px ${getIssuerColor(i.ticker)}80`
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = selected?.id === i.id ? 'scale(1.02)' : 'scale(1)'
                    e.target.style.boxShadow = selected?.id === i.id 
                      ? `0 10px 25px rgba(0,0,0,0.3), 0 0 15px ${getIssuerColor(i.ticker)}60`
                      : '0 5px 15px rgba(0,0,0,0.2)'
                  }}
                >
                  <div style={{ 
                    fontWeight: '700', 
                    marginBottom: '6px',
                    fontSize: '20px',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
                  }}>
                    {i.ticker}
                  </div>
                  <div style={{ 
                    opacity: 0.9, 
                    fontSize: '14px',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
                  }}>
                    {i.name}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Scores Panel */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(69,183,209,0.2), rgba(150,206,180,0.2))',
            backdropFilter: 'blur(15px)',
            borderRadius: '20px',
            padding: '30px',
            border: '2px solid rgba(255,255,255,0.3)',
            maxHeight: '700px',
            overflowY: 'auto',
            boxShadow: '0 15px 35px rgba(0,0,0,0.2)'
          }}>
            <h3 style={{ 
              margin: '0 0 25px 0', 
              fontSize: '24px', 
              fontWeight: '700',
              textAlign: 'center',
              textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
            }}>
              📊 Recent Credit Scores
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              {scores.slice(0, 10).map((s, index) => (
                <div key={s.id} style={{
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1))',
                  borderRadius: '15px',
                  padding: '20px',
                  border: '2px solid rgba(255,255,255,0.2)',
                  transition: 'all 0.3s ease',
                  animation: `slideIn 0.6s ease-out ${index * 0.1}s both`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                    <span style={{ 
                      fontWeight: '700',
                      fontSize: '18px',
                      textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
                    }}>
                      Issuer {s.issuer_id}
                    </span>
                    <span style={{
                      color: getScoreColor(s.score),
                      fontWeight: '800',
                      fontSize: '22px',
                      textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
                    }}>
                      {s.score.toFixed(2)}
                    </span>
                  </div>
                  <div style={{ 
                    opacity: 0.9, 
                    fontSize: '14px',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
                  }}>
                    {new Date(s.as_of).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Events Panel */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(254,202,87,0.2), rgba(255,159,243,0.2))',
            backdropFilter: 'blur(15px)',
            borderRadius: '20px',
            padding: '30px',
            border: '2px solid rgba(255,255,255,0.3)',
            maxHeight: '700px',
            overflowY: 'auto',
            boxShadow: '0 15px 35px rgba(0,0,0,0.2)'
          }}>
            <h3 style={{ 
              margin: '0 0 25px 0', 
              fontSize: '24px', 
              fontWeight: '700',
              textAlign: 'center',
              textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
            }}>
              📰 Recent News Events
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              {events.slice(0, 10).map((e, index) => (
                <div key={e.id} style={{
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1))',
                  borderRadius: '15px',
                  padding: '20px',
                  border: '2px solid rgba(255,255,255,0.2)',
                  transition: 'all 0.3s ease',
                  animation: `slideIn 0.6s ease-out ${index * 0.1}s both`
                }}>
                  <a 
                    href={e.url} 
                    target="_blank" 
                    rel="noreferrer"
                    style={{
                      color: '#60a5fa',
                      textDecoration: 'none',
                      fontWeight: '600',
                      display: 'block',
                      marginBottom: '10px',
                      lineHeight: '1.5',
                      fontSize: '16px',
                      textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                      transition: 'all 0.3s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.target.style.color = '#ff6b6b'
                      e.target.style.textDecoration = 'underline'
                      e.target.style.transform = 'translateX(5px)'
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.color = '#60a5fa'
                      e.target.style.textDecoration = 'none'
                      e.target.style.transform = 'translateX(0)'
                    }}
                  >
                    {e.title}
                  </a>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ 
                      opacity: 0.9, 
                      fontSize: '14px',
                      textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
                    }}>
                      {new Date(e.published_at).toLocaleString()}
                    </span>
                    <span style={{
                      color: getSentimentColor(e.sentiment),
                      fontWeight: '700',
                      fontSize: '16px',
                      textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
                      padding: '4px 12px',
                      borderRadius: '20px',
                      background: 'rgba(255,255,255,0.1)',
                      border: '1px solid rgba(255,255,255,0.2)'
                    }}>
                      Sentiment: {e.sentiment?.toFixed(2)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Issuer Detail */}
        {selected && <IssuerDetail issuer={selected} />}
      </div>
    </div>
  )
}

function IssuerDetail({ issuer }) {
  const [trend, setTrend] = useState(null)
  const [latest, setLatest] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    setTrend(null)
    setLatest(null)
    
    const fetchData = async () => {
      try {
        const [latestRes, trendRes] = await Promise.all([
          fetch(`${API}/v1/scores?issuer_id=${issuer.id}&limit=1`),
          fetch(`${API}/v1/scores/trend?issuer_id=${issuer.id}&limit=200`)
        ])
        
        const [latestData, trendData] = await Promise.all([
          latestRes.json(),
          trendRes.json()
        ])
        
        setLatest(latestData[0])
        setTrend(trendData)
        setLoading(false)
      } catch (error) {
        console.error('Error fetching issuer data:', error)
        setLoading(false)
      }
    }
    
    fetchData()
  }, [issuer])

  const getContributionColor = (value) => {
    if (value > 0) return '#00ff88'
    if (value < 0) return '#ff4444'
    return '#8888ff'
  }

  const getIssuerColor = (ticker) => {
    const colors = {
      'AAPL': '#ff6b6b',
      'MSFT': '#4ecdc4',
      'TSLA': '#45b7d1',
      'AMZN': '#96ceb4'
    }
    return colors[ticker] || '#a8e6cf'
  }

  return (
    <div style={{
      background: `linear-gradient(135deg, ${getIssuerColor(issuer.ticker)}20, rgba(255,255,255,0.1))`,
      backdropFilter: 'blur(15px)',
      borderRadius: '20px',
      padding: '30px',
      border: `2px solid ${getIssuerColor(issuer.ticker)}60`,
      marginTop: '30px',
      boxShadow: '0 20px 40px rgba(0,0,0,0.3)',
      animation: 'slideIn 0.8s ease-out'
    }}>
      <h3 style={{ 
        margin: '0 0 25px 0', 
        fontSize: '28px', 
        fontWeight: '700',
        textAlign: 'center',
        textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
        color: getIssuerColor(issuer.ticker)
      }}>
        📊 {issuer.ticker} — Detailed Analysis
      </h3>
      
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px' }}>
          <div style={{ 
            fontSize: '48px', 
            marginBottom: '20px',
            animation: 'float 2s ease-in-out infinite'
          }}>⏳</div>
          <div style={{ fontSize: '20px', fontWeight: '600' }}>Loading detailed analysis...</div>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
          {/* Latest Score */}
          {latest && (
            <div style={{
              background: 'linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1))',
              borderRadius: '20px',
              padding: '25px',
              border: '2px solid rgba(255,255,255,0.3)',
              boxShadow: '0 15px 30px rgba(0,0,0,0.2)'
            }}>
              <h4 style={{ 
                margin: '0 0 20px 0', 
                fontSize: '22px', 
                fontWeight: '700',
                textAlign: 'center',
                textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
              }}>
                🎯 Latest Credit Score
              </h4>
              <div style={{ 
                fontSize: '48px', 
                fontWeight: '800', 
                marginBottom: '12px', 
                color: '#00ff88',
                textAlign: 'center',
                textShadow: '3px 3px 6px rgba(0,0,0,0.3)',
                animation: 'glow 2s ease-in-out infinite'
              }}>
                {latest.score.toFixed(2)}
              </div>
              <div style={{ 
                opacity: 0.9, 
                fontSize: '16px',
                textAlign: 'center',
                textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
              }}>
                Updated: {new Date(latest.as_of).toLocaleString()}
              </div>
              
              {latest.contributions && (
                <div style={{ marginTop: '25px' }}>
                  <h5 style={{ 
                    margin: '0 0 15px 0', 
                    fontSize: '18px', 
                    fontWeight: '700',
                    textAlign: 'center',
                    textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
                  }}>
                    📈 Feature Contributions
                  </h5>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {Object.entries(latest.contributions).map(([k, v]) => (
                      <div key={k} style={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        padding: '8px 12px',
                        background: 'rgba(255,255,255,0.1)',
                        borderRadius: '10px',
                        border: '1px solid rgba(255,255,255,0.2)'
                      }}>
                        <span style={{ 
                          fontSize: '14px', 
                          opacity: 0.9,
                          fontWeight: '600',
                          textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
                        }}>
                          {k.replace(/_/g, ' ').toUpperCase()}
                        </span>
                        <span style={{
                          color: getContributionColor(v),
                          fontWeight: '700',
                          fontSize: '16px',
                          textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
                        }}>
                          {Number(v).toFixed(4)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
          
          {/* Trend Chart */}
          {trend && (
            <div style={{
              background: 'linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1))',
              borderRadius: '20px',
              padding: '25px',
              border: '2px solid rgba(255,255,255,0.3)',
              boxShadow: '0 15px 30px rgba(0,0,0,0.2)'
            }}>
              <h4 style={{ 
                margin: '0 0 20px 0', 
                fontSize: '22px', 
                fontWeight: '700',
                textAlign: 'center',
                textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
              }}>
                📊 Score Trend
              </h4>
              <div style={{
                display: 'flex',
                gap: '3px',
                alignItems: 'flex-end',
                height: '150px',
                border: '2px solid rgba(255,255,255,0.3)',
                borderRadius: '15px',
                padding: '15px',
                background: 'linear-gradient(135deg, rgba(0,0,0,0.2), rgba(0,0,0,0.1))',
                boxShadow: 'inset 0 5px 15px rgba(0,0,0,0.2)'
              }}>
                {trend.scores.map((v, i) => (
                  <div
                    key={i}
                    style={{
                      width: '6px',
                      background: 'linear-gradient(to top, #00ff88, #4ecdc4, #45b7d1)',
                      height: Math.max(6, Math.min(120, (v + 1) * 60)),
                      borderRadius: '3px',
                      transition: 'all 0.3s ease',
                      boxShadow: '0 2px 8px rgba(0,255,136,0.3)'
                    }}
                    title={`Score: ${v.toFixed(2)}`}
                    onMouseEnter={(e) => {
                      e.target.style.transform = 'scale(1.2)'
                      e.target.style.boxShadow = '0 4px 12px rgba(0,255,136,0.6)'
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.transform = 'scale(1)'
                      e.target.style.boxShadow = '0 2px 8px rgba(0,255,136,0.3)'
                    }}
                  />
                ))}
              </div>
              <div style={{ 
                marginTop: '15px', 
                textAlign: 'center', 
                opacity: 0.9, 
                fontSize: '16px',
                fontWeight: '600',
                textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
              }}>
                Last {trend.timestamps.length} data points
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}


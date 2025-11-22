import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useTheme } from '../contexts/ThemeContext'
import { getHistory, getSummary, downloadPDF } from '../services/api'
import './History.css'

const History = ({ onLogout }) => {
  const { isDark, toggleTheme } = useTheme()
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const data = await getHistory()
      setHistory(data)
    } catch (err) {
      setError('Failed to load history')
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = async () => {
    if (history.length === 0) {
      setError('No data available to generate PDF')
      return
    }
    
    try {
      await downloadPDF()
      alert('PDF downloaded successfully!')
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to download PDF'
      setError(errorMsg)
      alert(errorMsg)
    }
  }

  return (
    <div className="app">
      <nav className="nav">
        <div>
          <h2>Chemical Equipment Visualizer</h2>
        </div>
        <div className="nav-links">
          <Link to="/upload">Upload</Link>
          <Link to="/history">History</Link>
          <button onClick={handleDownloadPDF} className="btn btn-secondary" style={{ marginLeft: '10px' }}>
            Download PDF
          </button>
          <button onClick={toggleTheme} className="btn btn-secondary" style={{ marginLeft: '10px' }}>
            {isDark ? '☀️' : '🌙'}
          </button>
          <button onClick={onLogout} className="btn btn-secondary" style={{ marginLeft: '10px' }}>
            Logout
          </button>
        </div>
      </nav>

      <div className="container">
        <div className="card">
          <h2>Upload History</h2>
          {loading && <p>Loading...</p>}
          {error && <div className="error">{error}</div>}
          
          {!loading && history.length === 0 && (
            <p>No upload history available</p>
          )}

          {!loading && history.length > 0 && (
            <div className="history-list">
              {history.map((item) => (
                <div key={item.id} className="history-item">
                  <div className="history-header">
                    <h3>Dataset #{item.id}</h3>
                    <span className="history-date">
                      {new Date(item.uploaded_at).toLocaleString()}
                    </span>
                  </div>
                  <div className="history-summary">
                    <div className="summary-item">
                      <strong>Total Equipment:</strong> {item.summary.total_count}
                    </div>
                    <div className="summary-item">
                      <strong>Avg Flowrate:</strong> {item.summary.avg_flowrate.toFixed(2)}
                    </div>
                    <div className="summary-item">
                      <strong>Avg Pressure:</strong> {item.summary.avg_pressure.toFixed(2)}
                    </div>
                    <div className="summary-item">
                      <strong>Avg Temperature:</strong> {item.summary.avg_temperature.toFixed(2)}
                    </div>
                    <div className="summary-item">
                      <strong>Types:</strong> {Object.keys(item.summary.type_distribution).join(', ')}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default History


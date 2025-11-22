import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { uploadCSV, getSummary, downloadPDF } from '../services/api'
import { useTheme } from '../contexts/ThemeContext'
import EquipmentTable from '../components/EquipmentTable'
import SummaryCards from '../components/SummaryCards'
import Charts from '../components/Charts'
import './Upload.css'

const Upload = ({ onLogout }) => {
  const { isDark, toggleTheme } = useTheme()
  const [file, setFile] = useState(null)
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [uploaded, setUploaded] = useState(false)

  useEffect(() => {
    loadSummary()
  }, [])

  const loadSummary = async () => {
    try {
      const data = await getSummary()
      setSummary(data.summary)
      setUploaded(true)
    } catch (err) {
      console.log('No existing data')
    }
  }

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setError('')
  }

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError('')

    try {
      const result = await uploadCSV(file)
      setSummary(result.summary)
      setUploaded(true)
      setFile(null)
      document.getElementById('file-input').value = ''
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = async () => {
    if (!summary) {
      setError('Please upload a CSV file first')
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
          <button onClick={onLogout} className="btn btn-secondary" style={{ marginLeft: '10px' }}>
            Logout
          </button>
        </div>
      </nav>

      <div className="container">
        <div className="card">
          <h2>Upload CSV File</h2>
          <form onSubmit={handleUpload}>
            <input
              id="file-input"
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="input"
            />
            {error && <div className="error">{error}</div>}
            <button type="submit" className="btn btn-primary" disabled={loading || !file}>
              {loading ? 'Uploading...' : 'Upload CSV'}
            </button>
          </form>
        </div>

        {summary && (
          <>
            <SummaryCards summary={summary} />
            <div style={{ marginBottom: '32px' }}>
              <Charts summary={summary} />
            </div>
            <EquipmentTable data={summary.equipment_data} />
          </>
        )}

        {!uploaded && !summary && (
          <div className="card">
            <p>Upload a CSV file to view equipment data and statistics.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Upload


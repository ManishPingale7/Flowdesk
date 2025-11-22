import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import Landing from './pages/Landing'
import Auth from './pages/Auth'
import Upload from './pages/Upload'
import History from './pages/History'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const auth = localStorage.getItem('auth')
    setIsAuthenticated(!!auth)
    setLoading(false)
  }, [])

  const handleLogin = (auth) => {
    localStorage.setItem('auth', auth)
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('auth')
    setIsAuthenticated(false)
  }

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <ThemeProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route 
            path="/auth" 
            element={!isAuthenticated ? <Auth onLogin={handleLogin} /> : <Navigate to="/upload" />} 
          />
          <Route 
            path="/upload" 
            element={isAuthenticated ? <Upload onLogout={handleLogout} /> : <Navigate to="/auth" />} 
          />
          <Route 
            path="/history" 
            element={isAuthenticated ? <History onLogout={handleLogout} /> : <Navigate to="/auth" />} 
          />
          <Route path="/" element={<Navigate to={isAuthenticated ? "/upload" : "/auth"} />} />
        </Routes>
      </Router>
    </ThemeProvider>
  )
}

export default App


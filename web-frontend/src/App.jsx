import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
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
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={!isAuthenticated ? <Login onLogin={handleLogin} /> : <Navigate to="/upload" />} 
        />
        <Route 
          path="/upload" 
          element={isAuthenticated ? <Upload onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/history" 
          element={isAuthenticated ? <History onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route path="/" element={<Navigate to={isAuthenticated ? "/upload" : "/login"} />} />
      </Routes>
    </Router>
  )
}

export default App


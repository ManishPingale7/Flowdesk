import { useState } from 'react'
import { useTheme } from '../contexts/ThemeContext'
import { login, register } from '../services/api'
import './Auth.css'

const Auth = ({ onLogin }) => {
  const { isDark } = useTheme()
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    passwordConfirm: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (isLogin) {
        await login(formData.username, formData.password)
        const auth = btoa(`${formData.username}:${formData.password}`)
        onLogin(auth)
      } else {
        if (formData.password !== formData.passwordConfirm) {
          setError('Passwords do not match')
          setLoading(false)
          return
        }
        if (formData.password.length < 8) {
          setError('Password must be at least 8 characters')
          setLoading(false)
          return
        }
        await register(formData.username, formData.email, formData.password)
        const auth = btoa(`${formData.username}:${formData.password}`)
        onLogin(auth)
      }
    } catch (err) {
      if (err.response) {
        const errorMsg = err.response.data?.error || 
                        err.response.data?.message ||
                        (typeof err.response.data === 'object' ? 
                          Object.values(err.response.data).flat().join(', ') : 
                          'An error occurred')
        setError(errorMsg)
      } else {
        setError(isLogin ? 'Login failed. Please try again.' : 'Registration failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const switchMode = () => {
    setIsLogin(!isLogin)
    setError('')
    setFormData({
      username: '',
      email: '',
      password: '',
      passwordConfirm: ''
    })
  }

  return (
    <div className={`auth-container ${isDark ? 'dark' : ''}`}>
      <div className="auth-card">
        <div className="auth-header">
          <h1>Chemical Equipment Visualizer</h1>
          <p>{isLogin ? 'Welcome back!' : 'Create your account'}</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              name="username"
              type="text"
              placeholder="Enter your username"
              value={formData.username}
              onChange={handleChange}
              required
              className="form-input"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder={isLogin ? "Enter your password" : "Create a password (min 8 characters)"}
              value={formData.password}
              onChange={handleChange}
              required
              minLength={isLogin ? undefined : 8}
              className="form-input"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="passwordConfirm">Confirm Password</label>
              <input
                id="passwordConfirm"
                name="passwordConfirm"
                type="password"
                placeholder="Confirm your password"
                value={formData.passwordConfirm}
                onChange={handleChange}
                required
                minLength={8}
                className="form-input"
              />
            </div>
          )}

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="auth-submit-btn" disabled={loading}>
            {loading ? (
              <span className="loading">
                <span className="spinner"></span>
                {isLogin ? 'Logging in...' : 'Creating account...'}
              </span>
            ) : (
              isLogin ? 'Login' : 'Sign Up'
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button type="button" onClick={switchMode} className="switch-mode-btn">
              {isLogin ? 'Sign Up' : 'Login'}
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Auth


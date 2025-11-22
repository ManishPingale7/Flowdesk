import React from 'react'
import { useNavigate } from 'react-router-dom'
import GlassFeatureGrid from '../components/GlassFeatureGrid'
import './Landing.css'

const Landing = () => {
  const navigate = useNavigate()

  return (
    <div className="landing-page">
      <nav className="landing-nav">
        <div className="logo">Flowdesk</div>
        <div className="nav-links">
          <button onClick={() => navigate('/auth')} className="btn-login">Login</button>
        </div>
      </nav>
      
      <header className="hero-section">
        <h1>Data Processing Simplified</h1>
        <p>Build powerful data pipelines with ease.</p>
      </header>

      <section className="features-section">
        <GlassFeatureGrid />
      </section>
    </div>
  )
}

export default Landing

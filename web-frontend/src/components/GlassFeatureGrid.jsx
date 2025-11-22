import React from 'react'
import './GlassFeatureGrid.css'

const GlassFeatureGrid = () => {
  return (
    <div className="glass-container">
      <div className="glass-header">
        <h2>Features built for industrial precision</h2>
      </div>

      <div className="glass-grid">
        {/* Card 1: Ingestion */}
        <div className="glass-card span-2">
          <div className="glass-card-content">
            <h3>Instant Data Ingestion.</h3>
            <p>Upload your equipment logs instantly. Our system automatically parses standard CSV formats, validating headers and data types for immediate analysis.</p>
          </div>
          <div className="visual-element visual-ingest">
            <div className="grid-mockup">
              {[...Array(12)].map((_, i) => (
                <div key={i} className="grid-cell"></div>
              ))}
            </div>
            <div className="ingest-arrow">↓</div>
            <div className="database-icon">🛢️</div>
          </div>
        </div>

        {/* Card 2: History */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>Historical Tracking.</h3>
            <p>Keep a record of all your uploads. Compare datasets over time with our persistent history log.</p>
          </div>
          <div className="visual-element">
            <div className="circle-glow">
              <div className="clock-hand"></div>
            </div>
          </div>
        </div>

        {/* Card 3: Visualization */}
        <div className="glass-card span-2">
          <div className="glass-card-content">
            <h3>Interactive Visualization.</h3>
            <p>Visualize flowrates, pressures, and temperatures with interactive dashboards. Spot anomalies and trends at a glance.</p>
          </div>
          <div className="visual-element">
            {/* Abstract visual for charts */}
            <div style={{ display: 'flex', gap: '10px', padding: '20px', alignItems: 'end', height: '100%' }}>
               <div style={{ width: '30px', height: '40%', background: 'rgba(249, 115, 22, 0.5)', borderRadius: '4px' }}></div>
               <div style={{ width: '30px', height: '70%', background: 'rgba(139, 92, 246, 0.5)', borderRadius: '4px' }}></div>
               <div style={{ width: '30px', height: '50%', background: 'rgba(255, 255, 255, 0.2)', borderRadius: '4px' }}></div>
               <div style={{ width: '30px', height: '80%', background: 'rgba(249, 115, 22, 0.5)', borderRadius: '4px' }}></div>
            </div>
          </div>
        </div>

        {/* Card 4: Distribution (Moved) */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>Equipment Distribution.</h3>
            <p>Automatically categorize and visualize your equipment types (Pumps, Valves, Reactors) with dynamic charts.</p>
          </div>
          <div className="visual-element">
             <div style={{ padding: '20px', display: 'flex', justifyContent: 'center' }}>
               <div style={{ 
                 width: '60px', 
                 height: '60px', 
                 borderRadius: '50%', 
                 border: '4px solid rgba(249, 115, 22, 0.6)',
                 borderRightColor: 'rgba(139, 92, 246, 0.6)',
                 borderBottomColor: 'rgba(255, 255, 255, 0.2)'
               }}></div>
             </div>
          </div>
        </div>

        {/* Card 5: Reporting (Moved & Resized) */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>Comprehensive Reporting.</h3>
            <p>Generate professional PDF reports for stakeholders. Share insights with a single click.</p>
          </div>
          <div className="visual-element" style={{ position: 'relative' }}>
             <div className="gradient-orb"></div>
             <div style={{ 
               position: 'absolute', 
               top: '50%', 
               left: '50%', 
               width: '60px', 
               height: '80px', 
               borderRadius: '4px', 
               border: '1px solid rgba(255,255,255,0.2)',
               background: 'rgba(255,255,255,0.05)',
               transform: 'translate(-50%, -50%)',
               display: 'flex',
               alignItems: 'center',
               justifyContent: 'center'
             }}>
                <span style={{ fontSize: '24px' }}>📄</span>
             </div>
          </div>
        </div>

        {/* Card 6: Analytics */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>Real-time Analytics.</h3>
            <p>Calculate average flowrates, pressures, and temperatures instantly. Get a snapshot of your plant's health.</p>
          </div>
          <div className="visual-element" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
             <div style={{ width: '40px', height: '40px', borderRadius: '50%', border: '1px solid rgba(255,255,255,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
               <span style={{ fontSize: '20px' }}>⚡</span>
             </div>
          </div>
        </div>

        {/* Card 7: Performance */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>Performance Metrics.</h3>
            <p>Track key performance indicators across all your equipment to ensure optimal operation efficiency.</p>
          </div>
          <div className="visual-element">
            <div className="bar-chart">
              <div className="bar" style={{ height: '30%' }}></div>
              <div className="bar" style={{ height: '50%' }}></div>
              <div className="bar active" style={{ height: '80%' }}></div>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}

export default GlassFeatureGrid

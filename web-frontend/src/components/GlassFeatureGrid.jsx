import React from 'react'
import './GlassFeatureGrid.css'

const GlassFeatureGrid = () => {
  return (
    <div className="glass-container">
      <div className="glass-header">
        <h2>Features built for ease of use</h2>
      </div>

      <div className="glass-grid">
        {/* Card 1: Deduplication */}
        <div className="glass-card span-2">
          <div className="glass-card-content">
            <h3>Deduplication with one click.</h3>
            <p>Select the columns as primary keys and enjoy a fully managed processing without the need to tune memory or state management.</p>
          </div>
          <div className="visual-element visual-deduplicate">
            <button className="btn-glass">Deduplicate</button>
            <div className="grid-mockup">
              {[...Array(9)].map((_, i) => (
                <div key={i} className="grid-cell"></div>
              ))}
            </div>
          </div>
        </div>

        {/* Card 2: 7 days checks */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>7 days deduplication checks.</h3>
            <p>Auto detection of duplicates within 7 days after setup to ensure your data is always clean and storage is not exhausted.</p>
          </div>
          <div className="visual-element">
            <div className="circle-glow">
              <div className="clock-hand"></div>
            </div>
          </div>
        </div>

        {/* Card 3: Batch Ingestions */}
        <div className="glass-card span-2">
          <div className="glass-card-content">
            <h3>Batch Ingestions built for ClickHouse.</h3>
            <p>Select from ingestion logics like auto, size based or time window based.</p>
          </div>
          <div className="visual-element">
            {/* Abstract visual for batch ingestion */}
            <div style={{ display: 'flex', gap: '10px', padding: '20px', alignItems: 'center' }}>
               <div style={{ width: '40px', height: '40px', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px' }}></div>
               <div style={{ width: '40px', height: '40px', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px' }}></div>
               <div style={{ height: '1px', flex: 1, background: 'linear-gradient(90deg, rgba(255,255,255,0.2), transparent)' }}></div>
            </div>
          </div>
        </div>

        {/* Card 4: Joins */}
        <div className="glass-card span-2">
          <div className="glass-card-content">
            <h3>Joins, simplified.</h3>
            <p>Define the fields of the streams that you would like to join and GlassFlow handles execution and state management automatically.</p>
          </div>
          <div className="visual-element" style={{ position: 'relative' }}>
             <div className="gradient-orb"></div>
             <div style={{ 
               position: 'absolute', 
               top: '50%', 
               left: '40%', 
               width: '80px', 
               height: '80px', 
               borderRadius: '50%', 
               border: '1px solid rgba(255,255,255,0.1)',
               background: 'linear-gradient(135deg, rgba(249, 115, 22, 0.1), transparent)',
               transform: 'translate(-50%, -50%)'
             }}></div>
             <div style={{ 
               position: 'absolute', 
               top: '50%', 
               left: '60%', 
               width: '80px', 
               height: '80px', 
               borderRadius: '50%', 
               border: '1px solid rgba(168, 85, 247, 0.1)',
               background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.1), transparent)',
               transform: 'translate(-50%, -50%)',
               mixBlendMode: 'screen'
             }}></div>
          </div>
        </div>

        {/* Card 5: Stateful Processing */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>Stateful Processing.</h3>
            <p>Built-in lightweight state store enables low-latency, in-memory deduplication and joins with context retention.</p>
          </div>
          <div className="visual-element">
             <div style={{ padding: '20px' }}>
               <div style={{ height: '8px', width: '100%', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', marginBottom: '8px' }}></div>
               <div style={{ height: '8px', width: '70%', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', marginBottom: '8px' }}></div>
               <div style={{ height: '8px', width: '40%', background: 'rgba(255,255,255,0.1)', borderRadius: '4px' }}></div>
             </div>
          </div>
        </div>

        {/* Card 6: Managed Kafka */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>Managed Kafka and ClickHouse Connector.</h3>
            <p>Built and updated by GlassFlow team. Data inserts with a declared schema and schemaless.</p>
          </div>
          <div className="visual-element" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
             <div style={{ width: '40px', height: '40px', borderRadius: '50%', border: '1px solid rgba(255,255,255,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
               <span style={{ fontSize: '20px' }}>⚡</span>
             </div>
          </div>
        </div>

        {/* Card 7: Auto Scaling */}
        <div className="glass-card">
          <div className="glass-card-content">
            <h3>Auto Scaling of Workers.</h3>
            <p>Our Kafka connector will trigger based on partitions new workers and make sure that execution runs efficient.</p>
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

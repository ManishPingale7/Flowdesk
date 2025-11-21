const SummaryCards = ({ summary }) => {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '20px' }}>
      <div className="card" style={{ textAlign: 'center' }}>
        <h3 style={{ color: '#666', marginBottom: '10px' }}>Total Equipment</h3>
        <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#007bff' }}>{summary.total_count}</p>
      </div>
      <div className="card" style={{ textAlign: 'center' }}>
        <h3 style={{ color: '#666', marginBottom: '10px' }}>Avg Flowrate</h3>
        <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#28a745' }}>{summary.avg_flowrate.toFixed(2)}</p>
      </div>
      <div className="card" style={{ textAlign: 'center' }}>
        <h3 style={{ color: '#666', marginBottom: '10px' }}>Avg Pressure</h3>
        <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#ffc107' }}>{summary.avg_pressure.toFixed(2)}</p>
      </div>
      <div className="card" style={{ textAlign: 'center' }}>
        <h3 style={{ color: '#666', marginBottom: '10px' }}>Avg Temperature</h3>
        <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#dc3545' }}>{summary.avg_temperature.toFixed(2)}</p>
      </div>
    </div>
  )
}

export default SummaryCards


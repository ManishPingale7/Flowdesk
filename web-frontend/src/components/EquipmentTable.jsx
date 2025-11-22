import './EquipmentTable.css'

const EquipmentTable = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="glass-table-container">
        <div className="glass-table-header">
          <h2>Equipment Data</h2>
        </div>
        <p style={{ color: '#94a3b8', padding: '20px' }}>No equipment data available</p>
      </div>
    )
  }

  return (
    <div className="glass-table-container">
      <div className="glass-table-header">
        <h2>Equipment Data</h2>
      </div>
      <table className="glass-table">
        <thead>
          <tr>
            <th>Equipment Name</th>
            <th>Type</th>
            <th>Flowrate</th>
            <th>Pressure</th>
            <th>Temperature</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item['Equipment Name']}</td>
              <td>{item.Type}</td>
              <td>{item.Flowrate}</td>
              <td>{item.Pressure}</td>
              <td>{item.Temperature}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default EquipmentTable


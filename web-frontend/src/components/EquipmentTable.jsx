const EquipmentTable = ({ data }) => {
  if (!data || data.length === 0) {
    return <p>No equipment data available</p>
  }

  return (
    <table className="table">
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
  )
}

export default EquipmentTable


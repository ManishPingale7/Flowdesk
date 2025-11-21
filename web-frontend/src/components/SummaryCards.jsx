import './SummaryCards.css'

const SummaryCards = ({ summary }) => {
  const cards = [
    {
      label: 'Total Equipment',
      value: summary.total_count,
      color: 'var(--primary)',
      icon: '📊'
    },
    {
      label: 'Avg Flowrate',
      value: summary.avg_flowrate.toFixed(2),
      color: 'var(--accent)',
      icon: '💧'
    },
    {
      label: 'Avg Pressure',
      value: summary.avg_pressure.toFixed(2),
      color: 'var(--warning)',
      icon: '⚡'
    },
    {
      label: 'Avg Temperature',
      value: summary.avg_temperature.toFixed(2),
      color: 'var(--danger)',
      icon: '🌡️'
    }
  ]

  return (
    <div className="summary-cards">
      {cards.map((card, index) => (
        <div key={index} className="summary-card" style={{ '--card-color': card.color }}>
          <div className="summary-card-icon">{card.icon}</div>
          <div className="summary-card-content">
            <div className="summary-card-label">{card.label}</div>
            <div className="summary-card-value" style={{ color: card.color }}>
              {card.value}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default SummaryCards

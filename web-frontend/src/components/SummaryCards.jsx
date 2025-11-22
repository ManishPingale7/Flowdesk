import { BarChart3, Droplets, Zap, Thermometer } from 'lucide-react'
import './SummaryCards.css'

const SummaryCards = ({ summary }) => {
  const cards = [
    {
      label: 'Total Equipment',
      value: summary.total_count,
      color: 'var(--accent-primary)',
      icon: <BarChart3 size={24} />
    },
    {
      label: 'Avg Flowrate',
      value: summary.avg_flowrate.toFixed(2),
      color: '#3b82f6', // Blue
      icon: <Droplets size={24} />
    },
    {
      label: 'Avg Pressure',
      value: summary.avg_pressure.toFixed(2),
      color: '#eab308', // Yellow
      icon: <Zap size={24} />
    },
    {
      label: 'Avg Temperature',
      value: summary.avg_temperature.toFixed(2),
      color: '#ef4444', // Red
      icon: <Thermometer size={24} />
    }
  ]

  return (
    <div className="summary-cards">
      {cards.map((card, index) => (
        <div key={index} className="summary-card" style={{ '--card-accent': card.color }}>
          <div className="summary-card-icon-wrapper">
            {card.icon}
          </div>
          <div className="summary-card-content">
            <div className="summary-card-label">{card.label}</div>
            <div className="summary-card-value">
              {card.value}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default SummaryCards

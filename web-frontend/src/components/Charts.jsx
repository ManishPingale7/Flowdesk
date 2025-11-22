import { Pie, Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
} from 'chart.js'
import './Charts.css'

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
)

const Charts = ({ summary }) => {
  const typeDistributionData = {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(summary.type_distribution),
        backgroundColor: [
          'rgba(249, 115, 22, 0.6)',  // Orange
          'rgba(168, 85, 247, 0.6)',  // Purple
          'rgba(59, 130, 246, 0.6)',  // Blue
          'rgba(16, 185, 129, 0.6)',  // Emerald
          'rgba(244, 63, 94, 0.6)',   // Rose
        ],
        borderColor: [
          'rgba(249, 115, 22, 1)',
          'rgba(168, 85, 247, 1)',
          'rgba(59, 130, 246, 1)',
          'rgba(16, 185, 129, 1)',
          'rgba(244, 63, 94, 1)',
        ],
        borderWidth: 1,
      },
    ],
  }

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    color: '#a1a1aa',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#a1a1aa',
          padding: 20,
          usePointStyle: true,
          pointStyle: 'circle',
          font: {
            family: "'Inter', sans-serif",
            size: 12,
            weight: 500
          }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(24, 24, 27, 0.9)',
        titleColor: '#fafafa',
        bodyColor: '#a1a1aa',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
        displayColors: true,
        titleFont: {
          family: "'Inter', sans-serif",
          size: 13,
          weight: 600
        },
        bodyFont: {
          family: "'Inter', sans-serif",
          size: 12
        }
      }
    }
  }

  const pieOptions = {
    ...commonOptions,
    layout: {
      padding: 20
    }
  }

  const statisticsData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          summary.avg_flowrate,
          summary.avg_pressure,
          summary.avg_temperature
        ],
        backgroundColor: 'rgba(168, 85, 247, 0.6)', // Purple
        borderColor: 'rgba(168, 85, 247, 1)',
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  }

  const barOptions = {
    ...commonOptions,
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(255, 255, 255, 0.05)',
          drawBorder: false,
        },
        ticks: {
          color: '#a1a1aa',
          padding: 10,
          font: {
            family: "'Inter', sans-serif",
            size: 11
          }
        }
      },
      x: {
        grid: {
          display: false,
          drawBorder: false,
        },
        ticks: {
          color: '#a1a1aa',
          padding: 10,
          font: {
            family: "'Inter', sans-serif",
            size: 11
          }
        }
      }
    },
    plugins: {
      ...commonOptions.plugins,
      legend: {
        display: false // Hide legend for bar chart as it's redundant
      }
    }
  }

  return (
    <div className="charts-grid">
      <div className="chart-wrapper">
        <h3>Equipment Type Distribution</h3>
        <div className="chart-container">
          <Pie data={typeDistributionData} options={pieOptions} />
        </div>
      </div>
      <div className="chart-wrapper">
        <h3>Average Statistics</h3>
        <div className="chart-container">
          <Bar data={statisticsData} options={barOptions} />
        </div>
      </div>
    </div>
  )
}

export default Charts


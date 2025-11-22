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
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 1,
      },
    ],
  }

  const pieOptions = {
    plugins: {
      legend: {
        labels: {
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      },
      tooltip: {
        titleFont: {
          size: 16,
          weight: 'bold'
        },
        bodyFont: {
          size: 14,
          weight: 'bold'
        }
      }
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
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  }

  const barOptions = {
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          font: {
            size: 14,
            weight: 'bold'
          }
        }
      },
      x: {
        ticks: {
          font: {
            size: 14,
            weight: 'bold'
          }
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      },
      tooltip: {
        titleFont: {
          size: 16,
          weight: 'bold'
        },
        bodyFont: {
          size: 14,
          weight: 'bold'
        }
      }
    }
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px' }}>
      <div>
        <h3>Equipment Type Distribution</h3>
        <Pie data={typeDistributionData} options={pieOptions} />
      </div>
      <div>
        <h3>Average Statistics</h3>
        <Bar 
          data={statisticsData}
          options={barOptions}
        />
      </div>
    </div>
  )
}

export default Charts


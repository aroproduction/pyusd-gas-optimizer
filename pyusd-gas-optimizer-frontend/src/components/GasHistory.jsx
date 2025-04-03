import React, { useState, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend);

const API_BASE_URL = '/api';

function GasHistory() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const chartRef = useRef(null);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/gas/history?limit=50`);
      const data = await response.json();
      const history = data.history.reverse(); // Ascending order
      
      const labels = history.map(entry => {
        // Parse ISO date string with timezone information
        const timestamp = new Date(entry.timestamp);
        return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      });
      
      const gasPrices = history.map(entry => entry.gas_price);

      setChartData({
        labels,
        datasets: [{
          label: 'Gas Price (Gwei)',
          data: gasPrices,
          borderColor: '#007bff',
          backgroundColor: 'rgba(0, 123, 255, 0.1)',
          fill: true,
          tension: 0.4, // Smooth curve
          pointRadius: 3,
          pointHoverRadius: 5,
        }],
      });
    } catch (error) {
      console.error('Error fetching gas history:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
    const interval = setInterval(fetchHistory, 30000); // Update every 30s
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, []);

  const options = {
    responsive: true,
    animation: {
      duration: 1000, // Smooth transition for updates
      easing: 'easeInOutQuad',
    },
    scales: {
      x: {
        type: 'category',
        title: { display: true, text: 'Time (Local)' },
      },
      y: {
        title: { display: true, text: 'Gas Price (Gwei)' },
        beginAtZero: true,
      },
    },
    plugins: {
      tooltip: { mode: 'index', intersect: false },
      legend: { position: 'top' },
    },
  };

  return (
    <section id="history">
      <h2>Historical Gas Prices</h2>
      {loading ? (
        <p>Loading chart...</p>
      ) : chartData ? (
        <Line ref={chartRef} data={chartData} options={options} />
      ) : (
        <p>No data available</p>
      )}
    </section>
  );
}

export default GasHistory;
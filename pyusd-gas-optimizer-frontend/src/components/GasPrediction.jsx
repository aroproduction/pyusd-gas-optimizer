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

function GasPrediction() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const chartRef = useRef(null);

  const fetchPredictionData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${API_BASE_URL}/gas/predict`);
      
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      if (!data.predicted_gas_prices || data.predicted_gas_prices.length === 0) {
        throw new Error("No prediction data available");
      }

      // Get current time for display
      const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      
      const labels = [
        now, 
        ...data.predicted_gas_prices.map(p => {
          // Parse ISO date string with timezone information
          const timestamp = new Date(p.timestamp);
          return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        })
      ];
      
      const gasPrices = [data.current_gas_price_gwei, ...data.predicted_gas_prices.map(p => p.gas_price)];

      setChartData({
        labels,
        datasets: [
          {
            label: 'Gas Price (Gwei)',
            data: gasPrices,
            borderColor: '#28a745',
            backgroundColor: 'rgba(40, 167, 69, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointHoverRadius: 5,
          },
        ],
      });
    } catch (error) {
      console.error('Error fetching prediction:', error);
      setError(error.message || "Failed to load prediction data");
      setChartData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPredictionData();
    const interval = setInterval(fetchPredictionData, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    return () => {
      if (chartRef.current) chartRef.current.destroy();
    };
  }, []);

  const options = {
    responsive: true,
    animation: { duration: 1000, easing: 'easeInOutQuad' },
    scales: {
      x: { title: { display: true, text: 'Time (Local)' } },
      y: { title: { display: true, text: 'Gas Price (Gwei)' }, beginAtZero: true },
    },
    plugins: { tooltip: { mode: 'index', intersect: false }, legend: { position: 'top' } },
  };

  return (
    <section id="prediction">
      <h2>Predicted Gas Price (Next 3 Hours)</h2>
      {loading ? (
        <p>Loading prediction...</p>
      ) : error ? (
        <div className="error-container">
          <p className="error">{error}</p>
          <button onClick={fetchPredictionData} className="refresh-button">Try Again</button>
        </div>
      ) : chartData ? (
        <Line ref={chartRef} data={chartData} options={options} />
      ) : (
        <p>No prediction available</p>
      )}
      <div className="prediction-info">
        <p>Predictions are based on machine learning analysis of historical gas prices</p>
        <p><small>Updated every minute. Last update: {new Date().toLocaleTimeString()}</small></p>
      </div>
    </section>
  );
}

export default GasPrediction;
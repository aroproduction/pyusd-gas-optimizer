import React, { useState, useEffect } from 'react';

const API_BASE_URL = '/api';

function CurrentGas() {
  const [gasPrice, setGasPrice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [animate, setAnimate] = useState(false);
  const [error, setError] = useState(null);

  const fetchGasPrice = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${API_BASE_URL}/gas/current`);
      
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setGasPrice(`${data.gas_price_gwei} Gwei`);
      setAnimate(true); // Trigger animation
      setTimeout(() => setAnimate(false), 500); // Reset after animation
    } catch (error) {
      console.error('Error fetching gas price:', error);
      setError('Failed to load gas price');
      setGasPrice(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGasPrice();
    const interval = setInterval(fetchGasPrice, 10000); // Update every 10s
    return () => clearInterval(interval);
  }, []);

  return (
    <section id="current-gas">
      <h2>Current Gas Price (Ethereum)</h2>
      <div className="gas-display">
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="error">{error}</p>
        ) : (
          <p className={animate ? 'fade-in' : ''}>{gasPrice}</p>
        )}
        <button 
          onClick={fetchGasPrice} 
          disabled={loading}
          className="refresh-button"
        >
          Refresh
        </button>
      </div>
    </section>
  );
}

export default CurrentGas;
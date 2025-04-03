import React, { useState, useEffect } from 'react';

const API_BASE_URL = '/api';

function CurrentGas() {
  const [gasPrice, setGasPrice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [animate, setAnimate] = useState(false);

  const fetchGasPrice = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/gas/current`);
      const data = await response.json();
      setGasPrice(`${data.gas_price_gwei} Gwei`);
      setAnimate(true); // Trigger animation
      setTimeout(() => setAnimate(false), 500); // Reset after animation
    } catch (error) {
      console.error('Error fetching gas price:', error);
      setGasPrice('Error loading gas price');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGasPrice();
    const interval = setInterval(fetchGasPrice, 30000); // Update every 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <section id="current-gas">
      <h2>Current Gas Price (Ethereum)</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <p className={animate ? 'fade-in' : ''}>{gasPrice}</p>
      )}
    </section>
  );
}

export default CurrentGas;
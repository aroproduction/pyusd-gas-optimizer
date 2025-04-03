import React, { useState } from 'react';

const API_BASE_URL = '/api';

function GasEstimate() {
  const [amount, setAmount] = useState(100);
  const [result, setResult] = useState('Enter an amount to estimate cost.');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/gas/estimate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: parseFloat(amount) }),
      });
      const data = await response.json();
      setResult(`Estimated Cost: ${data.estimated_cost_eth.toFixed(6)} ETH for ${data.pyusd_amount} PYUSD`);
    } catch (error) {
      console.error('Error estimating gas cost:', error);
      setResult('Error estimating cost');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="estimate">
      <h2>Estimate Transaction Cost</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="amount">PYUSD Amount:</label>
        <input
          type="number"
          id="amount"
          step="0.01"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          min="0"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Estimating...' : 'Estimate'}
        </button>
      </form>
      <p>{result}</p>
    </section>
  );
}

export default GasEstimate;
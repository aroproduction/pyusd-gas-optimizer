import React, { useState } from 'react';

const API_BASE_URL = '/api';

function GasEstimate() {
  const [amount, setAmount] = useState(100);
  const [fromAddress, setFromAddress] = useState("0x0000000000000000000000000000000000000000");
  const [toAddress, setToAddress] = useState("0x0000000000000000000000000000000000000001");
  const [result, setResult] = useState('Enter an amount to estimate cost.');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Build query string for GET request
      const queryParams = new URLSearchParams({
        amount: parseFloat(amount),
        from: fromAddress,
        to: toAddress
      });
      
      const response = await fetch(`${API_BASE_URL}/gas/estimate?${queryParams.toString()}`);
      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setResult(
        `Estimated Cost: ${data.gas_cost_eth.toFixed(6)} ETH ($${data.gas_cost_usd.toFixed(2)}) 
         for ${amount} PYUSD | Gas: ${data.gas_price_gwei} Gwei | Gas Limit: ${data.gas_limit} units`
      );
    } catch (error) {
      console.error('Error estimating gas cost:', error);
      setResult('Error estimating cost: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="estimate">
      <h2>Estimate PYUSD Transaction Cost</h2>
      <form onSubmit={handleSubmit}>
        <div>
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
        </div>
        <div>
          <label htmlFor="from">From Address:</label>
          <input
            type="text" 
            id="from"
            value={fromAddress}
            onChange={(e) => setFromAddress(e.target.value)}
            placeholder="0x..."
            required
          />
        </div>
        <div>
          <label htmlFor="to">To Address:</label>
          <input
            type="text"
            id="to"
            value={toAddress}
            onChange={(e) => setToAddress(e.target.value)}
            placeholder="0x..."
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Estimating...' : 'Estimate'}
        </button>
      </form>
      <p>{result}</p>
    </section>
  );
}

export default GasEstimate;
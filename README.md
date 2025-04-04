# PYUSD Gas Optimizer

A comprehensive tool for tracking, predicting, and optimizing gas costs for PYUSD transactions on Ethereum.

## Project Overview

PYUSD Gas Optimizer is a web application that helps users track, predict, and optimize gas costs when transacting with PYUSD tokens on the Ethereum network. The application provides real-time gas price information, historical data visualization, gas cost estimates for PYUSD transactions, and predictive analytics for future gas prices.

## Key Features

- **Real-time Gas Price Monitoring**: Track current Ethereum gas prices
- **Historical Gas Price Visualization**: View historical gas price trends with proper timezone handling
- **Transaction Cost Estimation**: Calculate the estimated cost in ETH and USD for PYUSD transfers
- **Gas Price Prediction**: Forecast gas prices for the next 3 hours using machine learning
- **Direct GCP RPC Integration**: Uses Google Cloud Platform's blockchain RPC endpoints for all Ethereum interactions

## System Architecture

The project consists of two main components:

### Backend

Python Flask application that interacts with Ethereum via direct GCP RPC calls and provides API endpoints for the frontend to consume.

[See Backend Documentation](./backend/README.md)

### Frontend

React application that provides a user-friendly interface for interacting with the gas optimization features.

[See Frontend Documentation](./pyusd-gas-optimizer-frontend/README.md)

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- GCP RPC endpoint for Ethereum

### Running the Application

1. Start the backend server:
   ```
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   python app.py
   ```

2. Start the frontend development server:
   ```
   cd pyusd-gas-optimizer-frontend
   npm install
   npm run dev
   ```

3. Open http://localhost:5173 in your browser

## Screenshots

(Coming soon)

## License

[MIT](LICENSE)
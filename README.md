# PYUSD Gas Optimizer

## Project Overview

PYUSD Gas Optimizer is a web application that helps users track, predict, and optimize gas costs when transacting with PYUSD tokens on the Ethereum network. The application provides real-time gas price information, historical data visualization, gas cost estimates for PYUSD transactions, and predictive analytics for future gas prices.

## Features

- **Real-time Gas Price Monitoring**: Track current Ethereum gas prices
- **Historical Gas Price Visualization**: View historical gas price trends
- **Transaction Cost Estimation**: Calculate the estimated cost in ETH for PYUSD transfers
- **Gas Price Prediction**: Forecast gas prices for the next 3 minutes using machine learning
- **Timezone-aware Display**: Consistent timestamp handling between backend and frontend

## Architecture

The project consists of two main components:

### Backend (Python Flask)

- **API Endpoints**:
  - `/api/gas/current`: Returns current gas price on Ethereum
  - `/api/gas/history`: Returns historical gas price data
  - `/api/gas/estimate`: Estimates gas cost for PYUSD transactions
  - `/api/gas/predict`: Returns predicted gas prices for the next 3 minutes

- **Key Components**:
  - app.py: Flask server with API endpoints
  - gas_fetcher.py: Handles blockchain interactions and ML prediction
  - db.py: Manages SQLite database operations for gas price history

- **Technology Stack**:
  - Flask for the web server
  - Web3.py for Ethereum blockchain interaction
  - scikit-learn for ML-based gas price prediction
  - SQLite for storage
  - Pandas for data processing

### Frontend (React)

- **Key Components**:
  - CurrentGas.jsx: Displays real-time gas price
  - GasHistory.jsx: Visualizes historical gas price data
  - GasEstimate.jsx: Allows users to estimate transaction costs
  - GasPrediction.jsx: Shows predicted gas prices for the next 3 minutes

- **Technology Stack**:
  - React 19
  - Chart.js for data visualization
  - React Router for navigation

## Setup

### Backend

1. Navigate to the backend directory
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a .env file with your GCP RPC URL
6. Run the application: `python app.py`

### Frontend

1. Navigate to the pyusd-gas-optimizer-frontend directory
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

## Data Flow

1. The backend collects gas prices from the Ethereum blockchain via GCP RPC
2. Data is saved in a SQLite database with UTC timestamps
3. A machine learning model (RandomForest) is trained on historical data
4. The frontend fetches current prices, history, and predictions via API calls
5. All timestamps are properly converted from UTC to the user's local timezone for display

## Usage

- Visit the home page to see current gas prices, historical trends, and estimate transaction costs
- Navigate to the prediction page to view forecasted gas prices for the next 3 minutes
- Enter a PYUSD amount in the estimator to calculate the approximate gas cost for your transaction

## Future Improvements

- User authentication system for personalized recommendations
- Transaction scheduling based on predicted gas prices
- Support for additional ERC-20 tokens beyond PYUSD
- Mobile-responsive design optimizations
- Enhanced machine learning models for more accurate predictions

## Technical Notes

- All timestamps are stored in UTC format in the backend database
- Frontend components handle timezone conversion to the user's local time
- The prediction model is trained whenever the application starts, using available historical data
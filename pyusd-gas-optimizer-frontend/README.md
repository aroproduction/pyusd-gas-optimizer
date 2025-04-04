# PYUSD Gas Optimizer Frontend

The frontend application for PYUSD Gas Optimizer, providing an intuitive user interface for monitoring and optimizing gas costs for PYUSD transactions on Ethereum.

## Architecture

The frontend is built with React 19 and provides:

- Real-time gas price monitoring
- Historical gas price charts
- Gas cost estimation for PYUSD transfers
- Gas price prediction visualization

## Key Components

- **CurrentGas.jsx**: Displays and updates the current Ethereum gas price
- **GasHistory.jsx**: Visualizes historical gas price data using Chart.js
- **GasEstimate.jsx**: Form for estimating PYUSD transaction costs
- **GasPrediction.jsx**: Visualizes predicted gas prices for the next few hours

## Technology Stack

- **React 19**: Core UI framework
- **Chart.js / React-Chartjs-2**: For data visualization
- **React Router**: For navigation
- **Vite**: Build tool and development server

## Features

### Current Gas Price Display

- Shows real-time gas price in Gwei
- Auto-refreshes every 10 seconds
- Manual refresh button
- Visual animation on price change

### Historical Gas Price Chart

- Displays the last 50 gas price readings
- Time series visualization with proper time formatting
- Auto-updates every 30 seconds
- Error handling with retry functionality

### Transaction Cost Estimator

- Calculate gas costs for PYUSD transfers
- Input fields for amount, source and destination addresses
- Shows cost in both ETH and USD
- Displays estimated gas limit

### Gas Price Prediction

- Visualizes predicted gas prices for the next 3 hours
- Machine learning-based forecasting
- Updates every minute
- Clear error handling and retry mechanisms

## Timezone Handling

All timestamps from the backend are in UTC format with explicit timezone information. The frontend automatically converts these to the user's local timezone for display using JavaScript's built-in Date methods.

## API Integration

The frontend communicates with the backend through RESTful API calls:

- `/api/gas/current`: Fetches current gas price
- `/api/gas/history`: Retrieves historical gas price data
- `/api/gas/predict`: Gets gas price predictions
- `/api/gas/estimate`: Calculates transaction costs

## Responsive Design

The user interface is designed to be responsive and works well on:
- Desktop computers
- Tablets
- Mobile devices (with optimized layout)

## Setup Instructions

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm run dev
   ```

3. Build for production:
   ```
   npm run build
   ```

4. Preview production build:
   ```
   npm run preview
   ```

## Development

The project uses Vite's proxy configuration to route API requests to the backend during development. This is configured in `vite.config.js`.

## Error Handling

All components include comprehensive error handling to provide a robust user experience:

- Connection failures
- API errors
- Data processing issues
- Empty datasets

Each error state includes user-friendly messages and retry functionality.
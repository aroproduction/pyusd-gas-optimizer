# PYUSD Gas Optimizer Backend

The backend component of the PYUSD Gas Optimizer, responsible for interacting with the Ethereum blockchain, collecting gas prices, and providing prediction services.

## Architecture

The backend is built with Flask and provides RESTful API endpoints for:
- Current gas price retrieval
- Historical gas price data
- Gas price prediction
- PYUSD transaction cost estimation

## Key Components

- **app.py**: Main Flask application with API endpoints
- **gas_fetcher.py**: Core functionality for blockchain interaction and ML prediction
- **db.py**: Database operations for storing and retrieving gas price data
- **config.py**: Configuration management

## Technology Stack

- **Flask**: Web framework
- **Requests**: For direct GCP RPC calls to Ethereum nodes
- **SQLite**: Database for gas price history
- **Pandas/NumPy**: Data processing and analysis
- **scikit-learn**: Machine learning for gas price prediction

## API Endpoints

### GET `/api/gas/current`
Returns the current gas price on Ethereum.

**Response:**
```json
{
  "gas_price_gwei": 25.42
}
```

### GET `/api/gas/history?limit=50`
Returns historical gas price data.

**Parameters:**
- `limit` (optional): Maximum number of records to return (default: 50)

**Response:**
```json
{
  "history": [
    {
      "timestamp": "2025-04-04T01:30:00.123456+00:00",
      "gas_price": 25.42
    },
    ...
  ]
}
```

### GET `/api/gas/predict`
Returns predicted gas prices for the next few hours.

**Response:**
```json
{
  "current_gas_price_gwei": 25.42,
  "predicted_gas_prices": [
    {
      "timestamp": "2025-04-04T02:00:00.000000+00:00",
      "gas_price": 26.12
    },
    ...
  ],
  "timestamp": "2025-04-04T01:30:00.123456+00:00"
}
```

### GET `/api/gas/estimate`
Estimates the gas cost for PYUSD transactions.

**Parameters:**
- `amount`: PYUSD amount to transfer (e.g., 100)
- `from`: Source Ethereum address
- `to`: Destination Ethereum address

**Response:**
```json
{
  "gas_limit": 65000,
  "gas_price_gwei": 25.42,
  "gas_cost_eth": 0.001653,
  "gas_cost_usd": 2.81,
  "eth_price_usd": 1700.0
}
```

## Direct GCP RPC Integration

Instead of using Web3.py or other abstractions, this backend directly interfaces with Google Cloud Platform's RPC endpoints for Ethereum using the JSON-RPC protocol. This approach offers:

1. Better control over RPC calls
2. Fewer dependencies
3. Optimization for GCP's blockchain services
4. Direct access to Ethereum node data

Key RPC methods used:
- `eth_gasPrice`: For getting current gas prices
- `eth_estimateGas`: For estimating PYUSD transfer gas costs

## Machine Learning Model

The system uses a RandomForest model to predict future gas prices based on:
- Time of day
- Day of week
- Recent gas price trends (lag features)

Model accuracy is evaluated using Mean Absolute Error (MAE).

## UTC Timestamp Handling

All timestamps are stored in UTC format in the database and API responses include timezone information to ensure consistent display across different user locations.

## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```
   # Windows
   .venv\Scripts\activate
   
   # Unix/Linux/MacOS
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your GCP RPC URL:
   ```
   GCP_RPC_URL=https://blockchain.googleapis.com/v1/projects/your-project/locations/region/endpoints/ethereum-network/rpc?key=your-api-key
   ```

5. Run the application:
   ```
   python app.py
   ```

## Database

The application uses SQLite to store historical gas prices. On first run, it will create `gas_data.db` in the current directory.
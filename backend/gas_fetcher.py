import os
import json
import time
import requests
import numpy as np
import pandas as pd
import pickle
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from db import GasDatabase
from config import DB_FILE

load_dotenv()

class GasFetcher:
    def __init__(self, db_path=DB_FILE):
        self.db = GasDatabase(db_path)
        self.rpc_url = os.getenv('GCP_RPC_URL')
        if not self.rpc_url:
            raise ValueError("GCP_RPC_URL environment variable is not set")
        
        self.model = None
        self.train_model()
    
    def make_rpc_call(self, method, params=None):
        """Make a direct RPC call to the Ethereum node via GCP."""
        if params is None:
            params = []
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': int(time.time() * 1000),  # Use timestamp as ID
        }
        
        try:
            response = requests.post(self.rpc_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if 'error' in result:
                raise ValueError(f"RPC Error: {result['error']}")
            
            return result.get('result')
        except Exception as e:
            print(f"RPC call failed: {str(e)}")
            return None
    
    def get_current_gas_price(self):
        """Get current gas price directly with eth_gasPrice RPC method."""
        result = self.make_rpc_call('eth_gasPrice')
        if result:
            # Convert hex result to Gwei
            wei_gas_price = int(result, 16)
            gwei_gas_price = wei_gas_price / 1e9
            return round(gwei_gas_price, 4)
        return None

    def get_pyusd_transfer_gas(self, from_address, to_address, amount):
        """Estimate gas for PYUSD transfer with eth_estimateGas."""
        # PYUSD contract address on mainnet
        pyusd_contract = "0xCaC524BcA292aaade2DF8A05cC58F0a65B1B3bB9"
        
        # Create the transfer function data
        # transfer(address,uint256)
        function_selector = "0xa9059cbb"
        
        # Format to_address - remove 0x prefix and pad to 32 bytes
        to_param = to_address[2:].zfill(64)
        
        # Convert amount to wei (assuming 6 decimals for PYUSD) and format to 32 bytes
        amount_in_smallest_unit = int(amount * 10**6)
        amount_param = hex(amount_in_smallest_unit)[2:].zfill(64)
        
        # Combine function selector and parameters
        data = function_selector + to_param + amount_param
        
        # Prepare transaction parameters for gas estimation
        tx_params = {
            "from": from_address,
            "to": pyusd_contract,
            "data": "0x" + data
        }
        
        result = self.make_rpc_call('eth_estimateGas', [tx_params])
        if result:
            return int(result, 16)
        
        # Default gas limit if estimation fails
        return 100000

    def fetch_and_save_gas_price(self):
        """Fetch current gas price and save to database."""
        gas_price = self.get_current_gas_price()
        if gas_price:
            self.db.save_gas_price(gas_price)
            return gas_price
        return None
    
    def get_historical_data(self, limit=50):
        """Get historical gas prices from database."""
        return self.db.get_historical_data(limit)
    
    def train_model(self):
        """Train a machine learning model for gas price prediction."""
        history = self.db.get_historical_data(limit=1000)  # Get substantial history
        if len(history) < 50:  # Need enough data to train
            print("Insufficient data for model training")
            return
        
        df = pd.DataFrame(history)
        df.columns = ['timestamp', 'gas_price']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Feature engineering
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # Create lag features - gas prices from previous times
        for i in range(1, 6):  # 5 previous prices
            df[f'lag_{i}'] = df['gas_price'].shift(i)
        
        # Drop rows with NaN values (first 5 rows with lag features)
        df = df.dropna()
        
        # Prepare features and target
        features = ['hour', 'day_of_week', 'lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
        X = df[features]
        y = df['gas_price']
        
        # Train model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f"Model trained with MAE: {mae:.2f} Gwei")
    
    def predict_next_gas_prices(self, steps=6):
        """Predict gas prices for the next few periods (30 min increments)."""
        if not self.model:
            return None

        history = self.db.get_historical_data(limit=5)  # We only need the last 5 prices for lag features
        if len(history) < 5:
            return None

        df = pd.DataFrame(history)
        df.columns = ['timestamp', 'gas_price']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        predictions = []
        current_lags = list(df['gas_price'].values[:5][::-1])  # Last 5 prices in reverse order
        
        # Use current time as starting point for predictions
        current_time = pd.Timestamp.now(tz='UTC')
        
        for step in range(steps):
            next_hour = (current_time.hour + (step * 0.5)) % 24  # Half hour increments
            next_day = (current_time.dayofweek + (current_time.hour + (step * 0.5)) // 24) % 7
            features = np.array([[next_hour, next_day, *current_lags]])
            prediction = self.model.predict(features)[0]
            
            # Create future timestamp based on current time
            next_timestamp = current_time + pd.Timedelta(minutes=30 * step)
            utc_timestamp = next_timestamp.isoformat()
            
            predictions.append({
                'timestamp': utc_timestamp,
                'gas_price': float(prediction)
            })
            
            # Update lags for next prediction (drop oldest, add newest)
            current_lags.pop(0)
            current_lags.append(prediction)
        
        return predictions

    def get_eth_price_usd(self):
        """Get the current ETH price in USD using a public API."""
        try:
            response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
            data = response.json()
            return data['ethereum']['usd']
        except Exception as e:
            print(f"Failed to fetch ETH price: {e}")
            return 3000  # Fallback price if API call fails

if __name__ == "__main__":
    fetcher = GasFetcher()
    print(f"Current Gas Price: {fetcher.get_current_gas_price()} Gwei")
    predictions = fetcher.predict_next_gas_prices()
    if predictions:
        for pred in predictions:
            print(f"Predicted Gas Price at {pred['timestamp']}: {pred['gas_price']} Gwei")
from web3 import Web3
from config import RPC_URL
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from db import GasDatabase
from config import DB_FILE

# Minimal ERC-20 ABI for PYUSD
PYUSD_ABI = [
    {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
]
PYUSD_ADDRESS = "0x6c3ea9036406852006290770BEdFcAbA0e23A0e8"

class GasFetcher:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not self.w3.is_connected():
            raise Exception("Failed to connect to Ethereum Mainnet")
        self.pyusd_contract = self.w3.eth.contract(address=PYUSD_ADDRESS, abi=PYUSD_ABI)
        self.db = GasDatabase(DB_FILE)
        self.model = None
        self.train_model()

    def get_current_gas_price(self):
        gas_price_wei = self.w3.eth.gas_price
        return float(self.w3.from_wei(gas_price_wei, 'gwei'))

    def estimate_transaction_cost(self, pyusd_amount, sender_address=None):
        amount_wei = int(pyusd_amount * 10**6)
        if sender_address is None:
            sender_address = "0x264bd8291fAE1D75DB2c5F573b07faA6715997B5"
        tx = {
            "from": sender_address,
            "to": PYUSD_ADDRESS,
            "data": self.pyusd_contract.encodeABI(fn_name="transfer", args=[sender_address, amount_wei]),
            "chainId": 1,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(sender_address),
        }
        try:
            gas_estimate = self.w3.eth.estimate_gas(tx)
        except Exception as e:
            gas_estimate = 50000
            print(f"Gas estimation failed: {e}. Using fallback: {gas_estimate}")
        gas_price_wei = self.w3.eth.gas_price
        cost_wei = gas_estimate * gas_price_wei
        return float(self.w3.from_wei(cost_wei, 'ether'))

    def train_model(self):
        history = self.db.get_historical_data(limit=1000)
        if len(history) < 6:
            print(f"Not enough data to train model: {len(history)} entries found")
            self.model = None
            return

        df = pd.DataFrame(history)
        if len(df.columns) != 2:
            print(f"Unexpected data format: {df.columns}")
            self.model = None
            return
        
        df.columns = ['timestamp', 'gas_price']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
    
        for i in range(1, 6):
            df[f'lag_{i}'] = df['gas_price'].shift(i)
    
        df = df.dropna()
        if len(df) == 0:
            print("No valid training data after preprocessing")
            self.model = None
            return
    
        X = df[['hour', 'day_of_week', 'lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']]
        y = df['gas_price']
    
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        print(f"Gas price prediction model trained with {len(df)} samples")

    def predict_next_gas_prices(self, steps=6):
        if not self.model:
            return None
    
        history = self.db.get_historical_data(limit=5 + steps - 1)  # Enough data for lags
        if len(history) < 5:
            return None
    
        df = pd.DataFrame(history)
        df.columns = ['timestamp', 'gas_price']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        predictions = []
        current_lags = list(df['gas_price'].values[-5:][::-1])  # Last 5 prices in reverse order
        latest = df.iloc[-1]
        
        for step in range(steps):
            next_hour = (latest['timestamp'].hour + (step + 1)) % 24
            next_day = (latest['timestamp'].dayofweek + (latest['timestamp'].hour + step + 1) // 24) % 7
            features = np.array([[next_hour, next_day, *current_lags]])
            prediction = self.model.predict(features)[0]
            
            # Create timestamp with proper UTC handling
            next_timestamp = latest['timestamp'] + pd.Timedelta(minutes=30 * (step + 1))
            
            # Check if timestamp already has timezone info
            if next_timestamp.tzinfo is None:
                utc_timestamp = next_timestamp.tz_localize('UTC').isoformat()
            else:
                utc_timestamp = next_timestamp.isoformat()
            
            predictions.append({
                'timestamp': utc_timestamp,
                'gas_price': float(prediction)
            })
            # Update lags for next prediction
            current_lags.pop(0)  # Remove oldest
            current_lags.append(prediction)  # Add new prediction
        
        return predictions

if __name__ == "__main__":
    fetcher = GasFetcher()
    print(f"Current Gas Price: {fetcher.get_current_gas_price()} Gwei")
    predictions = fetcher.predict_next_gas_prices()
    if predictions:
        for pred in predictions:
            print(f"Predicted Gas Price at {pred['timestamp']}: {pred['gas_price']} Gwei")
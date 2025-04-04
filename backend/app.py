from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import time
from gas_fetcher import GasFetcher
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the gas fetcher
fetcher = GasFetcher()

@app.route('/api/gas/current', methods=['GET'])
def get_current_gas():
    gas_price = fetcher.get_current_gas_price()
    if gas_price is None:
        return jsonify({"error": "Failed to fetch gas price"}), 500
    
    # Also save the gas price to the database
    fetcher.db.save_gas_price(gas_price)
    
    return jsonify({"gas_price_gwei": gas_price})

@app.route('/api/gas/history', methods=['GET'])
def get_gas_history():
    limit = request.args.get('limit', default=50, type=int)
    history = fetcher.get_historical_data(limit)
    return jsonify({"history": history})

@app.route('/api/gas/predict', methods=['GET'])
def predict_gas():
    predicted_prices = fetcher.predict_next_gas_prices()
    if predicted_prices is None:
        return jsonify({"error": "Prediction not available due to insufficient data"}), 503
    current_price = fetcher.get_current_gas_price()
    
    # Use current time for response
    now = pd.Timestamp.now(tz='UTC')
    
    return jsonify({
        "current_gas_price_gwei": current_price,
        "predicted_gas_prices": predicted_prices,
        "timestamp": now.isoformat()
    })

@app.route('/api/gas/estimate', methods=['GET'])
def estimate_gas():
    amount = request.args.get('amount', default=1.0, type=float)
    from_address = request.args.get('from', default="0x0000000000000000000000000000000000000000")
    to_address = request.args.get('to', default="0x0000000000000000000000000000000000000001")
    
    if not from_address.startswith('0x') or not to_address.startswith('0x'):
        return jsonify({"error": "Invalid Ethereum addresses"}), 400
    
    gas_limit = fetcher.get_pyusd_transfer_gas(from_address, to_address, amount)
    gas_price_wei = fetcher.get_current_gas_price() * 1e9  # Convert Gwei to Wei
    
    # Calculate total gas cost
    gas_cost_eth = (gas_limit * gas_price_wei) / 1e18
    
    # Get ETH price in USD
    eth_price_usd = fetcher.get_eth_price_usd()
    
    # Calculate USD equivalent
    gas_cost_usd = gas_cost_eth * eth_price_usd
    
    return jsonify({
        "gas_limit": gas_limit,
        "gas_price_gwei": fetcher.get_current_gas_price(),
        "gas_cost_eth": gas_cost_eth,
        "gas_cost_usd": gas_cost_usd,
        "eth_price_usd": eth_price_usd
    })

@app.route('/healthcheck', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    # Schedule background task to periodically fetch and save gas prices
    import threading
    
    def background_fetch():
        while True:
            fetcher.fetch_and_save_gas_price()
            time.sleep(30)  # Fetch every 30 seconds
    
    # Start the background thread
    thread = threading.Thread(target=background_fetch)
    thread.daemon = True
    thread.start()
    
    # Run the Flask app
    app.run(debug=True)
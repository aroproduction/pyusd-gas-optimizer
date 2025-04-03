from flask import Flask, jsonify, request
from flask_cors import CORS
from gas_fetcher import GasFetcher
from db import GasDatabase
from config import DB_FILE
import pandas as pd

app = Flask(__name__)
CORS(app)
fetcher = GasFetcher()
db = GasDatabase(DB_FILE)

@app.route('/api/gas/current', methods=['GET'])
def get_current_gas():
    gas_price = fetcher.get_current_gas_price()
    db.save_gas_price(gas_price)
    return jsonify({"gas_price_gwei": gas_price, "network": "Ethereum"})

@app.route('/api/gas/history', methods=['GET'])
def get_gas_history():
    limit = request.args.get('limit', default=100, type=int)
    history = db.get_historical_data(limit)
    return jsonify({"history": history})

@app.route('/api/gas/estimate', methods=['POST'])
def estimate_cost():
    data = request.get_json()
    pyusd_amount = data.get('amount', 100.0)
    sender_address = data.get('sender', None)
    cost_eth = fetcher.estimate_transaction_cost(pyusd_amount, sender_address)
    return jsonify({"estimated_cost_eth": cost_eth, "pyusd_amount": pyusd_amount})

@app.route('/api/gas/predict', methods=['GET'])
def predict_gas():
    predicted_prices = fetcher.predict_next_gas_prices()
    if predicted_prices is None:
        return jsonify({"error": "Prediction not available due to insufficient data"}), 503
    current_price = fetcher.get_current_gas_price()
    
    # Get current time with proper UTC timezone
    now = pd.Timestamp.utcnow().tz_convert('UTC')
    print(f"Current UTC time: {now}")
    
    return jsonify({
        "current_gas_price_gwei": current_price,
        "predicted_gas_prices": predicted_prices,
        "timestamp": now.isoformat()
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# GCP Blockchain RPC URL for Ethereum Mainnet
RPC_URL = os.getenv("GCP_RPC_URL", "https://your-gcp-rpc-url-here")

# Database file
DB_FILE = "gas_data.db"
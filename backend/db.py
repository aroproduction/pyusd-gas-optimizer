import sqlite3
from datetime import datetime, timezone

class GasDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def _get_connection(self):
        """Create a new connection for each operation."""
        return sqlite3.connect(self.db_file)

    def create_table(self):
        """Create gas_prices table if it doesn't exist."""
        conn = self._get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gas_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                gas_price REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_gas_price(self, gas_price):
        """Save a gas price entry with explicit UTC timezone."""
        timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        conn = self._get_connection()
        conn.execute("INSERT INTO gas_prices (timestamp, gas_price) VALUES (?, ?)",
                     (timestamp, gas_price))
        conn.commit()
        conn.close()

    def get_historical_data(self, limit=100):
        """Fetch last N gas price entries."""
        conn = self._get_connection()
        cursor = conn.execute("SELECT timestamp, gas_price FROM gas_prices ORDER BY id DESC LIMIT ?", (limit,))
        data = [{"timestamp": row[0], "gas_price": row[1]} for row in cursor.fetchall()]
        conn.close()
        return data
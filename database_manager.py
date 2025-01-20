import sqlite3

class DatabaseManager:
    def __init__(self, db_name='stocks.db'):
        self.db_name = db_name

    def connect(self):
        """Establish a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Allows access to columns by name
        return conn

    def create_table(self):
        """Create the stock_prices table if it doesn't exist."""
        conn = self.connect()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS stock_prices (
                stock TEXT,
                date DATE,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                PRIMARY KEY (stock, date)
            )
        ''')
        conn.commit()
        conn.close()

    def insert_stock_data(self, stock_data):
        """Insert or replace stock data into the database."""
        conn = self.connect()
        c = conn.cursor()
        
        for date, row in stock_data.iterrows():
            c.execute('''
                INSERT OR REPLACE INTO stock_prices (stock, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (stock_data.name, date.date(), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

        conn.commit()
        conn.close()

    def get_top_stocks(self, limit=10):
        """Retrieve the top stocks by average closing price."""
        conn = self.connect()
        query = f"""
            SELECT stock, AVG(close) AS avg_close 
            FROM stock_prices 
            GROUP BY stock 
            ORDER BY avg_close DESC 
            LIMIT {limit}
        """
        top_stocks = conn.execute(query).fetchall()
        conn.close()
        return top_stocks

    def get_stock_data(self, stock_name):
        """Retrieve historical data for a specific stock."""
        conn = self.connect()
        query = "SELECT * FROM stock_prices WHERE stock = ?"
        stock_data = conn.execute(query, (stock_name,)).fetchall()
        conn.close()
        
        return stock_data

# Example usage (commented out for modular use)
# if __name__ == '__main__':
#     db_manager = DatabaseManager()
#     db_manager.create_table()

import yfinance as yf
import sqlite3
import pandas as pd

# List of popular stocks
stocks = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'FB', 'BRK.B', 'NVDA', 'JPM', 'V',
    'JNJ', 'WMT', 'PG', 'DIS', 'MA',
    'NFLX', 'VZ', 'INTC', 'CMCSA', 'PEP'
]

# Function to fetch stock data
def fetch_stock_data(stock):
    print(f"Fetching data for {stock}...")
    # Fetch historical data for one year
    data = yf.download(stock, period='1y')
    return data

# Function to save data to the SQLite database
def save_to_database(stock_data):
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
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

    # Insert data into the database
    for date, row in stock_data.iterrows():
        c.execute('''
            INSERT OR REPLACE INTO stock_prices (stock, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (stock_data.name, date.date(), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

    conn.commit()
    conn.close()

# Main function to orchestrate the scraping and saving process
def main():
    for stock in stocks:
        stock_data = fetch_stock_data(stock)
        save_to_database(stock_data)

if __name__ == '__main__':
    main()

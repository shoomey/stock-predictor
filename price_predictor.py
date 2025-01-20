import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sqlite3
import matplotlib.pyplot as plt

class PricePredictor:
    def __init__(self, db_name='stocks.db'):
        self.db_name = db_name
        self.model = LinearRegression()

    def connect(self):
        """Establish a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_name)
        return conn

    def fetch_stock_data(self, stock_name):
        """Fetch historical stock data from the database."""
        conn = self.connect()
        query = "SELECT date, close FROM stock_prices WHERE stock = ? ORDER BY date"
        stock_data = pd.read_sql_query(query, conn, params=(stock_name,))
        conn.close()
        return stock_data

    def prepare_data(self, stock_data):
        """Prepare data for training the model."""
        # Convert date to ordinal for regression analysis
        stock_data['date'] = pd.to_datetime(stock_data['date']).map(pd.Timestamp.toordinal)
        
        X = stock_data[['date']]  # Features (date)
        y = stock_data['close']    # Target variable (closing price)
        
        return X, y

    def train_model(self, X, y):
        """Train the linear regression model."""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Print model performance metrics
        score = self.model.score(X_test, y_test)
        print(f'Model R^2 Score: {score:.4f}')

    def predict_future_prices(self, stock_name, days=30):
        """Predict future prices for the specified number of days."""
        stock_data = self.fetch_stock_data(stock_name)
        
        # Prepare data for prediction
        X, y = self.prepare_data(stock_data)

        # Train the model on all available data
        self.train_model(X, y)

        # Predict future dates
        last_date = stock_data['date'].max()
        future_dates = np.array([last_date + i for i in range(1, days + 1)]).reshape(-1, 1)

        # Predict future prices
        future_prices = self.model.predict(future_dates)

        # Convert back to datetime format for plotting
        future_dates_dt = [pd.Timestamp.fromordinal(int(date)) for date in future_dates.flatten()]

        return future_dates_dt, future_prices

    def plot_predictions(self, stock_name, future_dates, future_prices):
        """Plot historical and predicted prices."""
        stock_data = self.fetch_stock_data(stock_name)

        plt.figure(figsize=(12, 6))
        
        # Plot historical prices
        plt.plot(pd.to_datetime(stock_data['date']), stock_data['close'], label='Historical Prices', color='blue')
        
        # Plot predicted prices
        plt.plot(future_dates, future_prices, label='Predicted Prices', color='orange', linestyle='--')
        
        plt.title(f'Stock Price Prediction for {stock_name}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        
        plt.show()

# Example usage (commented out for modular use)
# if __name__ == '__main__':
#     predictor = PricePredictor()
#     future_dates, future_prices = predictor.predict_future_prices('AAPL', days=30)
#     predictor.plot_predictions('AAPL', future_dates, future_prices)

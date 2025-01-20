import pandas as pd
import matplotlib.pyplot as plt

def format_dates(dates):
    """Convert ordinal dates to datetime format."""
    return [pd.Timestamp.fromordinal(int(date)) for date in dates]

def plot_stock_prices(historical_data, future_dates, future_prices, stock_name):
    """Plot historical and predicted stock prices."""
    plt.figure(figsize=(12, 6))
    
    # Plot historical prices
    plt.plot(pd.to_datetime(historical_data['date']), historical_data['close'], label='Historical Prices', color='blue')
    
    # Plot predicted prices
    plt.plot(future_dates, future_prices, label='Predicted Prices', color='orange', linestyle='--')
    
    plt.title(f'Stock Price Prediction for {stock_name}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    
    plt.grid()
    plt.tight_layout()
    plt.show()

def calculate_return(prices):
    """Calculate the return based on historical closing prices."""
    if len(prices) < 2:
        return 0.0
    return (prices[-1] - prices[0]) / prices[0] * 100  # Return as a percentage

def get_stock_summary(stock_data):
    """Generate a summary of stock data including average price and return."""
    avg_price = stock_data['close'].mean()
    total_return = calculate_return(stock_data['close'].values)
    
    return {
        'average_price': avg_price,
        'total_return': total_return
    }

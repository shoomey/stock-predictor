from flask import Flask, render_template, request
from database_manager import DatabaseManager
from price_predictor import PricePredictor

app = Flask(__name__)
db_manager = DatabaseManager()
predictor = PricePredictor()

# Create the database table if it doesn't exist
db_manager.create_table()

@app.route('/')
def index():
    """Home page displaying top stocks by average closing price."""
    top_stocks = db_manager.get_top_stocks(limit=10)
    return render_template('index.html', top_stocks=top_stocks)

@app.route('/stock/<string:stock_name>')
def stock_detail(stock_name):
    """Display detailed information and predictions for a specific stock."""
    stock_data = db_manager.get_stock_data(stock_name)
    if not stock_data:
        return render_template('error.html', message="Stock data not found.")

    # Prepare data for prediction
    future_dates, future_prices = predictor.predict_future_prices(stock_name, days=30)

    return render_template('stock_detail.html', 
                           stock_name=stock_name, 
                           stock_data=stock_data,
                           future_dates=future_dates,
                           future_prices=future_prices)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests from the user."""
    stock_name = request.form.get('stock_name')
    if not stock_name:
        return render_template('error.html', message="Stock name is required.")

    # Predict future prices
    future_dates, future_prices = predictor.predict_future_prices(stock_name, days=30)

    return render_template('prediction_result.html', 
                           stock_name=stock_name, 
                           future_dates=future_dates,
                           future_prices=future_prices)

if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class SampleDataFetcher:
    """Generates sample stock data for testing purposes"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def generate_sample_data(self, symbol, start_date=None, end_date=None, days=252):
        """Generate realistic sample stock data"""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=days)
        if end_date is None:
            end_date = datetime.now()
        
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        date_range = date_range[date_range.weekday < 5]  # Only weekdays
        
        # Generate realistic price data
        np.random.seed(42)  # For reproducible results
        
        # Start with a base price
        base_price = 100.0
        
        # Generate daily returns (log-normal distribution)
        daily_returns = np.random.normal(0.0005, 0.02, len(date_range))
        
        # Calculate prices
        prices = [base_price]
        for ret in daily_returns[1:]:
            new_price = prices[-1] * (1 + ret)
            prices.append(max(new_price, 0.01))  # Ensure positive prices
        
        # Generate OHLC data
        data = []
        for i, (date, price) in enumerate(zip(date_range, prices)):
            # Generate realistic OHLC from close price
            volatility = price * 0.02  # 2% daily volatility
            
            high = price + np.random.uniform(0, volatility)
            low = price - np.random.uniform(0, volatility)
            open_price = prices[i-1] if i > 0 else price
            
            # Ensure OHLC relationships
            high = max(high, open_price, price)
            low = min(low, open_price, price)
            
            volume = np.random.randint(1000000, 10000000)
            
            data.append({
                'Open': round(open_price, 2),
                'High': round(high, 2),
                'Low': round(low, 2),
                'Close': round(price, 2),
                'Volume': volume
            })
        
        df = pd.DataFrame(data, index=date_range)
        
        # Save to CSV
        filename = f"{self.data_dir}/{symbol}_sample_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename)
        print(f"Generated sample data for {symbol}: {len(df)} days")
        print(f"Saved to: {filename}")
        
        return df
    
    def get_multiple_symbols(self, symbols, days=252):
        """Generate sample data for multiple symbols"""
        data = {}
        for symbol in symbols:
            print(f"\nGenerating sample data for {symbol}...")
            df = self.generate_sample_data(symbol, days=days)
            data[symbol] = df
        return data


if __name__ == "__main__":
    print("Sample Data Fetcher Test")
    print("=" * 30)
    
    fetcher = SampleDataFetcher()
    
    # Generate sample data for SPY
    print("\nGenerating sample SPY data...")
    spy_data = fetcher.generate_sample_data('SPY', days=252)  # 1 year of trading days
    
    if spy_data is not None:
        print(f"\nSPY Data Shape: {spy_data.shape}")
        print(f"Date Range: {spy_data.index[0].date()} to {spy_data.index[-1].date()}")
        print(f"\nFirst few rows:")
        print(spy_data.head())
        print(f"\nLast few rows:")
        print(spy_data.tail())
        
        # Show some statistics
        print(f"\nPrice Statistics:")
        print(f"Starting Price: ${spy_data['Close'].iloc[0]:.2f}")
        print(f"Ending Price: ${spy_data['Close'].iloc[-1]:.2f}")
        print(f"Total Return: {((spy_data['Close'].iloc[-1] / spy_data['Close'].iloc[0]) - 1) * 100:.2f}%")
        print(f"Average Volume: {spy_data['Volume'].mean():,.0f}")
    
    print("\nTest completed!")

import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time

class SimpleDataFetcher:
    """Simple data fetcher using Alpha Vantage API"""
    
    def __init__(self, data_dir='data', api_key=None):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Use a working API key or fallback to sample data
        self.api_key = api_key or 'XOLA7URKC6PQJEXY'  # Free Alpha Vantage key
        self.base_url = 'https://www.alphavantage.co/query'
    
    def fetch_data(self, symbol, period='1y'):
        """Fetch daily data for a symbol"""
        try:
            print(f"Fetching {symbol}...")
            
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'outputsize': 'full',
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Error Message' in data:
                print(f"API Error: {data['Error Message']}")
                return None
            
            if 'Note' in data:
                print(f"API Note: {data['Note']}")
                return None
            
            time_series = data.get('Time Series (Daily)')
            if not time_series:
                print(f"No data found for {symbol}")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Sort by date and filter by period
            df = df.sort_index()
            
            if period == '1y':
                cutoff_date = datetime.now() - timedelta(days=365)
                df = df[df.index >= cutoff_date]
            
            if df.empty:
                print(f"No data after filtering for {symbol}")
                return None
            
            # Save to CSV
            filename = f"{self.data_dir}/{symbol}_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(filename)
            print(f"Saved {len(df)} days of data for {symbol}")
            
            # Rate limiting for demo API
            if self.api_key == 'demo':
                print("Waiting 12 seconds for rate limiting...")
                time.sleep(12)
            
            return df
            
        except Exception as e:
            print(f"Error fetching {symbol}: {str(e)}")
            return None
    
    def get_multiple_symbols(self, symbols):
        """Fetch data for multiple symbols"""
        data = {}
        for symbol in symbols:
            df = self.fetch_data(symbol)
            if df is not None:
                data[symbol] = df
        return data


if __name__ == "__main__":
    print("Simple Data Fetcher Test")
    print("=" * 30)
    
    fetcher = SimpleDataFetcher()
    
    # Test with one symbol first
    print("\nTesting single symbol fetch...")
    spy_data = fetcher.fetch_data('SPY')
    
    if spy_data is not None:
        print(f"\nSPY Data Shape: {spy_data.shape}")
        print(f"Date Range: {spy_data.index[0].date()} to {spy_data.index[-1].date()}")
        print(f"\nFirst few rows:")
        print(spy_data.head())
        print(f"\nLast few rows:")
        print(spy_data.tail())
    else:
        print("Failed to fetch SPY data")
    
    print("\nTest completed!")

import yfinance as yf

def extract(symbols, period='1y'):
    try:
        tickers = yf.Tickers(symbols)
        # pulling a trailing 12 month window of daily OHLCV data for all three tickers at once
        # since this runs automatically once a day, the window is going to shift forward every time it runs
        # so the database is always going to hold the most recent 12 months, not a fixed start date
        raw_data = yf.download(symbols, period = period)
        if raw_data is None or raw_data.empty:
            raise ValueError(f"No data found for symbols: {symbols}")
        return raw_data
    except Exception as e:
        print(f"Error in extract function: {e}", flush=True)
        raise ValueError(f"Failed to extract data for symbols: {symbols}. Error: {e}")

def extract_new_data(data):
    pass
import yfinance as yf
import pandas as pd

def fetch_from_yahoo(ticker, start, end, interval):
    try:
        print(f"📡 Fetching from remote: {ticker} [{interval}] {start} to {end}")
        data = yf.download(
            ticker,
            start=start,
            end=end,
            interval=interval,
            progress=False,
            auto_adjust=False  # Set explicitly to avoid warning
        )

        if data.empty:
            print(f"⚠️ No data returned for {ticker} in that range.")
            return pd.DataFrame()

        data.reset_index(inplace=True)  # Ensure 'Date' is a column
        return data

    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

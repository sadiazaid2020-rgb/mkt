import os
import json
import pandas as pd

BASE_DIR = "csv"

def get_csv_path(ticker, interval):
    folder = os.path.join(BASE_DIR, ticker.upper())
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{interval}.csv")

def get_meta_path(ticker, interval):
    folder = os.path.join(BASE_DIR, ticker.upper())
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{interval}_meta.json")

def save_data(ticker, interval, df):
    path = get_csv_path(ticker, interval)
    print(f"💾 Saving data locally: {path}")
    df.to_csv(path, index=False)

def load_data(ticker, interval):
    path = get_csv_path(ticker, interval)
    if os.path.exists(path):
        print(f"📁 Loading from local cache: {path}")
        return pd.read_csv(path, parse_dates=['Date'])
    print(f"📁 No local data found for {ticker} [{interval}]")
    return None

def save_metadata(ticker, interval, metadata):
    path = get_meta_path(ticker, interval)
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2)

def load_metadata(ticker, interval):
    path = get_meta_path(ticker, interval)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

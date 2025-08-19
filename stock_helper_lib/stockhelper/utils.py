import os
import pandas as pd
import json

def get_data_path(ticker, interval, base_dir="csv"):
    folder = os.path.join(base_dir, ticker)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{interval}.csv")

def save_to_csv(ticker, interval, data, base_dir="csv"):
    path = get_data_path(ticker, interval, base_dir)
    print(f"💾 Saving data locally: {path}")
    data.to_csv(path, index=False)

def load_from_csv(ticker, interval, base_dir="csv"):
    path = get_data_path(ticker, interval, base_dir)
    return pd.read_csv(path)

def save_metadata(ticker, interval, metadata, base_dir="csv"):
    folder = os.path.join(base_dir, ticker)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{interval}_meta.json")
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2)

def load_metadata(ticker, interval, base_dir="csv"):
    path = os.path.join(base_dir, ticker, f"{interval}_meta.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

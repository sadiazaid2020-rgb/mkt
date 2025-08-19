import os
import pandas as pd
from datetime import datetime
from stockhelper.utils import (
    get_data_path,
    save_to_csv,
    load_from_csv,
    save_metadata,
    load_metadata,
)
from stockhelper.fetchers import fetch_from_yahoo

def get_stock_data(ticker, start, end, interval="1d"):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    local_data = load_local_data(ticker, interval)
    metadata = load_metadata(ticker, interval)

    if local_data is not None and not local_data.empty:
        print(f"📁 Loading from local cache: csv/{ticker}/{interval}.csv")
        local_data['Date'] = pd.to_datetime(local_data['Date'])
        local_data = local_data.drop_duplicates(subset=['Date'])
        local_data = local_data.sort_values(by='Date')

        last_local_date = local_data['Date'].max()
        if last_local_date >= end:
            print("✅ Using cached data.")
            return local_data[(local_data['Date'] >= start) & (local_data['Date'] <= end)]

        fetch_start = last_local_date + pd.Timedelta(days=1)
        if fetch_start > end:
            print("✅ No new data needed (all dates already cached).")
            return local_data[(local_data['Date'] >= start) & (local_data['Date'] <= end)]

        remote_data = fetch_from_yahoo(
            ticker,
            fetch_start.strftime("%Y-%m-%d"),
            end.strftime("%Y-%m-%d"),
            interval
        )
        if isinstance(remote_data.columns, pd.MultiIndex):
            remote_data.columns = remote_data.columns.get_level_values(0)


        if not remote_data.empty:
            if 'Date' not in remote_data.columns:
                remote_data.reset_index(inplace=True)
                print("ℹ️ 'Date' column was missing — index reset applied.")

            remote_data['Date'] = pd.to_datetime(remote_data['Date'])
            remote_data = remote_data.drop_duplicates(subset=['Date'])
            combined_data = pd.concat([local_data, remote_data])
            combined_data = combined_data.drop_duplicates(subset=['Date'])
            combined_data = combined_data.sort_values(by='Date')
            print("🔄 Merging remote data with local cache")
            save_to_csv(ticker, interval, combined_data)
            save_metadata(ticker, interval, {'last_updated': datetime.today().strftime('%Y-%m-%d')})
            return combined_data[(combined_data['Date'] >= start) & (combined_data['Date'] <= end)]
        else:
            print("⚠️ No new data fetched from remote. Returning available local data.")
            return local_data[(local_data['Date'] >= start) & (local_data['Date'] <= end)]
    else:
        print("🚨 No valid local data. Fetching all data from remote.")
        remote_data = fetch_from_yahoo(
            ticker,
            start.strftime("%Y-%m-%d"),
            end.strftime("%Y-%m-%d"),
            interval
        )

        if isinstance(remote_data.columns, pd.MultiIndex):
            remote_data.columns = remote_data.columns.get_level_values(0)

        if not remote_data.empty:
            if 'Date' not in remote_data.columns:
                remote_data.reset_index(inplace=True)
                print("ℹ️ 'Date' column was missing — index reset applied.")
            remote_data['Date'] = pd.to_datetime(remote_data['Date'])
            print(remote_data.columns)
            remote_data = remote_data.drop_duplicates(subset=['Date'])
            remote_data = remote_data.sort_values(by='Date')
            save_to_csv(ticker, interval, remote_data)
            save_metadata(ticker, interval, {'last_updated': datetime.today().strftime('%Y-%m-%d')})
            return remote_data[(remote_data['Date'] >= start) & (remote_data['Date'] <= end)]
        else:
            print("❌ Failed to fetch any data from remote.")
            return pd.DataFrame()

def load_local_data(ticker, interval):
    path = get_data_path(ticker, interval)
    if os.path.exists(path):
        return load_from_csv(ticker, interval)
    return None

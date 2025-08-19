from stockhelper.core import get_stock_data

if __name__ == "__main__":
    df = get_stock_data("AAPL", "2023-01-01", "2023-01-10", interval="5m")
    print(df.head())

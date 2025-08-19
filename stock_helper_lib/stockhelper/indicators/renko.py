# renko.py
import pandas as pd
import numpy as np

def get_renko_data(df, brick_size=None, brick_pct=None):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    closes = df['Close'].values
    dates = df['Date'].values

    if brick_pct is not None:
        brick_size = closes[-1] * brick_pct
    elif brick_size is None:
        raise ValueError("Specify either brick_size or brick_pct")

    renko_dates, renko_prices, renko_dirs = [], [], []

    last_price = closes[0]

    for price, date in zip(closes[1:], dates[1:]):
        diff = price - last_price
        while abs(diff) >= brick_size:
            direction = np.sign(diff)
            last_price += direction * brick_size
            renko_dates.append(date)
            renko_prices.append(last_price)
            renko_dirs.append(direction)
            diff = price - last_price

    return pd.DataFrame({
        'Date': renko_dates,
        'Price': renko_prices,
        'Direction': renko_dirs
    })

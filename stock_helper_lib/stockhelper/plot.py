# plot.py
import finplot as fplt
import pandas as pd

def plot_ohlc_and_renko(ohlc_df, renko_df):
    ohlc_df = ohlc_df.set_index('Date')
    renko_df = renko_df.set_index('Date')

    # Create new window
    ax1, ax2 = fplt.create_plot('OHLC + Renko', rows=2)

    # Plot OHLC candles
    fplt.candlestick_ochl(ohlc_df[['Open', 'Close', 'High', 'Low']], ax=ax1)

    # Plot Renko as vertical line markers (up/down)
    up = renko_df[renko_df['Direction'] == 1]
    down = renko_df[renko_df['Direction'] == -1]

    up_dup_count = up.index.duplicated().sum()
    down_dup_count = down.index.duplicated().sum()
    if up_dup_count > 0:
        print(f"Found {up_dup_count} duplicate indices in up DataFrame. Removing duplicates.")
        up = up[~up.index.duplicated(keep='first')]
    if down_dup_count > 0:
        print(f"Found {down_dup_count} duplicate indices in down DataFrame. Removing duplicates.")
        down = down[~down.index.duplicated(keep='first')]

    # Reset index and use Date column for plotting to avoid index comparison issues in finplot
    up = up.reset_index()
    down = down.reset_index()
    if 'Date' in up.columns:
        up_dates = pd.to_datetime(up['Date'])
    else:
        up_dates = up.index
    if 'Date' in down.columns:
        down_dates = pd.to_datetime(down['Date'])
    else:
        down_dates = down.index

    fplt.plot(up_dates, up['Price'], style='^', color='green', ax=ax2, legend='Renko Up')
    fplt.plot(down_dates, down['Price'], style='v', color='red', ax=ax2, legend='Renko Down')

    fplt.show()

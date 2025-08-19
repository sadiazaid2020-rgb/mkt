
from stockhelper.core import get_stock_data
from stockhelper.indicators.renko import get_renko_data
from stockhelper.plot import plot_ohlc_and_renko

df = get_stock_data("AAPL", "2023-01-01", "2023-07-01", interval="1d")

if not df.empty:
	dup_count = df.index.duplicated().sum()
	if dup_count > 0:
		print(f"Found {dup_count} duplicate indices in df. Removing duplicates.")
		df = df[~df.index.duplicated(keep='first')]
	else:
		print("No duplicate indices in df.")

	renko_df = get_renko_data(df, brick_pct=0.01)
	if not renko_df.empty:
		renko_dup_count = renko_df.index.duplicated().sum()
		if renko_dup_count > 0:
			print(f"Found {renko_dup_count} duplicate indices in renko_df. Removing duplicates.")
			renko_df = renko_df[~renko_df.index.duplicated(keep='first')]
		else:
			print("No duplicate indices in renko_df.")
		plot_ohlc_and_renko(df, renko_df)
	else:
		print("Renko data is empty. Cannot plot.")
else:
	print("No stock data available for the given range. Please check the ticker and date range.")
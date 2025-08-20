
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../stock_helper_lib')))

from stockhelper.core import get_stock_data
from stockhelper.indicators.renko import get_renko_data
from stockhelper.plot import plot_renko_only, plot_renko_matplotlib, plot_renko_equal_time_finplot


import datetime
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)
df = get_stock_data("RELIANCE.NS", str(start_date), str(end_date), interval="1d")


if not df.empty:
	dup_count = df.index.duplicated().sum()
	if dup_count > 0:
		print(f"Found {dup_count} duplicate indices in df. Removing duplicates.")
		df = df[~df.index.duplicated(keep='first')]
	else:
		print("No duplicate indices in df.")

	renko_df = get_renko_data(df, brick_pct=0.005)
	if not renko_df.empty:
		renko_dup_count = renko_df.index.duplicated().sum()
		if renko_dup_count > 0:
			print(f"Found {renko_dup_count} duplicate indices in renko_df. Removing duplicates.")
			renko_df = renko_df[~renko_df.index.duplicated(keep='first')]
		else:
			print("No duplicate indices in renko_df.")
	# plot_renko_only(df, renko_df)
		plot_renko_matplotlib(renko_df)
		plot_renko_equal_time_finplot(renko_df)
	else:
		print("Renko data is empty. Cannot plot.")
else:
	print("No stock data available for the given range. Please check the ticker and date range.")
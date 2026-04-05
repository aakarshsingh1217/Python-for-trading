import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Get Apple stock data
df = yf.download("XOM", period="5y", auto_adjust=False)
df.columns = df.columns.get_level_values(0)
monthly = df.resample("MS").agg({
    "High": "max",
    "Volume": "sum"
})
monthly = monthly.reset_index()
monthly["Month"] = monthly["Date"].dt.strftime("%b")
monthly = monthly[["Date", "High", "Volume", "Month"]]
monthly = monthly.sort_values(by="Date", ascending=True).reset_index(drop=True)
print(monthly.head())
monthly.plot(x="Month",
             y="Volume",
             kind="bar",
             title="Exxon Stock Price")

plt.show()
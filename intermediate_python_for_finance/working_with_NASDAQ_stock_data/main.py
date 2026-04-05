import yfinance as yf
import pandas as pd

# Get Apple stock data
df = yf.download("AAPL", start="2020-02-28", end="2020-03-28", auto_adjust=False)
df.columns = df.columns.get_level_values(0)
df = df.rename(columns={'Close': 'Price'})
df['Trend'] = df['Price'].diff().apply(lambda x: 'Up' if x > 0 else 'Down')
df = df.reset_index()
df = df[['Date', 'Price', 'Volume', 'Trend']]
df.columns.name = None
df = df.sort_values(by="Date", ascending=False).reset_index(drop=True)

print(df.Price > 60)
print("###############")
mask_symbol = df.Trend == "Up"
aapl = df.loc[mask_symbol]
print(aapl.head())
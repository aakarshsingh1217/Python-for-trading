import talib

"""
RSI implemented using talib.RSI and passing price col.
Uses 14 period lookback window.
The longer the lookback window, the less sensitive the RSI is to price fluctuations.
In code, we calc. RSI and save it in new DataFrame col.
"""

# Calculate RSI
stock_data = None
stock_data['RSI'] = talib.RSI(stock_data['Close'], timeperiod=14)
# Print last 5 rows
print(stock_data.tail())

"""
Similar to ADX, helpful to plot the price and RSI one above another.
In code, we create two subplots, top plot shows price and bottom plot shows RSI.
Notice when RSI is falling near 30 in chart, the price bottoms out and gradually 
recovers, and when the RSI is approaching 70, the price reaches new highs and is 
more likely to pull back.
"""

import matplotlib.pyplot as plt

# Create subplots
fig, (ax1, ax2) = plt.subplots(2)

# Plot RSI with the price
ax1.set_ylabel('Price')
ax1.plot(stock_data['Close'])
ax2.set_ylabel('RSI')
ax2.plot(stock_data['RSI'])

ax1.set_title('Price and RSI')
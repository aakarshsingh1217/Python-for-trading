import talib

"""
Implemented by calling talib.ADX and passing 3 types price data as input, high, low and 
close price.

Originally 14-period lookback window was used for ADX calcs., which became industry 
standard.

Can change default period with timeperiod param, keep in mind, the longer the lookback 
window, the less sensitive the ADX is to price fluctuations.
In other words, 14 day ADX more sensitive to daily price changes than 21 day ADX.
Sometimes traders change lookback period to suit their trading time horizons.
E.g., position trader who holds a trading position for several months would likely use a 
longer lookback period.
In code, we calc. ADX and save it in new DataFrame col.
"""

# Calculate ADX
stock_data = None
stock_data['ADX'] = talib.ADX(stock_data['High'], stock_data['Low'], stock_data['Close'],
                              timeperiod=14)
# Print last 5 rows
print(stock_data.tail())

"""
Usually an ADX plot is placed horizontally under price plot, so we can observe price and 
indicator changes together along same timeline.
Accomplished by using matplotlib subplots func.
in Code, we crfeate a set of subplots, ax1 and ax2, to plot the price and ADX seperately.
Can use set_ylabel to label y axis of each subplot for more clarity.
In chart, we can see ADX starts to rice when price is steadily trending up.
ADX starts to decline when uptrend in price is stalling and price is moving sideways.
"""

import matplotlib as plt

# Create subplots
fig, (ax1, ax2) = plt.subplots(2)

# Plot ADX with price
ax1.set_ylabel('Price')
ax1.plot(stock_data['Close'])
ax2.set_ylabel('ADX')
ax2.plot(stock_data['ADX'])

ax1.set_title('Price and ADX')
plt.show()
import talib

"""
TA-Lib: Technical Analysis Library
- Includes 150+ technical indicator implementations

Most commonly used trend indicators:

SMA: simple moving average
EMA: exponential moving avg.
Called moving averages because every avg val. calc. using data 
points of most recent n periods, and hence moves along with the price.
Calc. avg. creates smoothing effect which helps to give indication 
of which direction price is moving - upward, downward or sideways.
Moving avgs. calc. based on longer lookback period have more 
smoothing affects than a shorter one.

Arithmetic mean of past n prices (SMA = (p1 + p2 + ... + pn) / n)
N/s chosen num. of periods for calc. mean
Can call talib.SMA and pass DataFrame col., e.g. Close price
Use time period param. to specify avging. period
Note since n-period SMA needs at least n data points to calc. 
the first avg. val., we will get NA vals. for the first n - 1 rows.
Instead, we can use tail method to check last 5 rows.
"""

# Calc. 2 SMAs
stock_data = None
stock_data['SMA_short'] = talib.SMA(stock_data['Close'], timeperiod=10)
stock_data['SMA_long'] = talib.SMA(stock_data['Close'], timeperiod=50)

# Print last 5 rows
print(stock_data.tail())

"""
Can plot SMAs together with the price with matplotlib.
Label is added to indicate each data series.
"""

import matplotlib as plt

# Plot SMA w/ price
plt.plot(stock_data['SMA_short'], label='SMA_short')
plt.plot(stock_data['SMA_long'], label='SMA_long')
plt.plot(stock_data['Close'], label='Close')

# Customize and show the plot
plt.legend()
plt.title('SMAs')
plt.show()

"""
Exponential Moving Average (EMA) is an exponentially weighted avg. of the last n prices, 
where the weight decreases exponentially with each previous price.
EM A subscript n = P subscript n * multiplier + previous EMA * (1 - multiplier)
To implement an EMA with talib, call talib.EMA and pass DataFrame col. as input, in 
this case the close price.
Similarly, specify the averaging period with the timeperiod parameter.
"""

# Calculate two EMAs
stock_data['EMA_short'] = talib.EMA(stock_data['Close'], timeperiod=10)
stock_data['EMA_long'] = talib.EMA(stock_data['Close'], timeperiod=50)
# Print last 5 rows
print(stock_data.tail())

"""
We see when plotting EMAs and price data (as with SMAs), the shorter EMA in blue is 
more reactive to the price movement compared to the longer EMA in red.

Main diff. between SMAs and EMAs is that EMAs give higher weight to more recent data, 
while SMAs assign equal weight to all data points.
In plots containg SMA and EMA (calc. with same lookback window), whenever the price 
makes a big change, the EMA in the orange line is more sensitive to the price move 
compared to the SMA in the blue line.
"""
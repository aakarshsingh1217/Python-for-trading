import matplotlib as plt

eurusd_h = None
eurusd_daily = eurusd_h.resample('D').mean()
eurusd_weekly = eurusd_h.resample('W').mean()

stock_data = None
# Calc daily returns
stock_data['daily_return'] = stock_data['Close'].pct_change() * 100
# Plot data
plt.plot(stock_data['daily_return'])
plt.show()

stock_data['daily_return'].hist(bins=100)
plt.show()

# Simple moving avg. (SMA)
stock_data['sma_50'] = stock_data['Close'].rolling(window=50).mean()

# Plotting rolling avg

plt.plot(stock_data['Close'], label='Close')
plt.plot(stock_data['sma_50'], label='sma_50')
plt.legend()
plt.show()

"""
As a trader, it's important to analyze an asset's return profile, such as ranges of 
price changes, return distributions etc. Over the years, Tesla fans and short sellers 
have either been betting on or against Tesla stocks aggresively, leading to volatile 
stock prices. You have some Tesla historical daily price data and want to verify this 
phenomenon.

Can calc. daily percentage change using Close price and save it in new col. named daily 
return.

Then can plot a histogram of daily return, setting bin size to 100.

The histogram shows the majority of daily returns are between -4% and +4%, but 
occasionally the prices had big negative or positive 15% changes, so the stock is 
indeed very volatile.
"""

tsla_data = None
# Calculate daily returns
tsla_data['daily_return'] = tsla_data['Close'].pct_change() * 100

# Plot the histogram
tsla_data['daily_return'].hist(bins=100, color='red')
plt.ylabel('Frequency')
plt.xlabel('Daily return')
plt.title('Daily return histogram')
plt.show()

"""
Daily price data inherently messy and noisy.
Need to analyze Apple stock daily price data, and plan to add a 
simple moving avg. (SMA) indicator to smooth out data, specifically 
50-day SMA.
"""
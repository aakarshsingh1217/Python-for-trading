import numpy as np

prices = np.array([170.12, 93.29, 55.28, 145.30, 171.81, 59.50, 100.50])

# Find the mean
price_mean = np.mean(prices)

# Create boolean array
boolean_array = (prices > price_mean)
print(boolean_array)

# Select prices that are greater than average
above_avg = prices[boolean_array]
print(above_avg)
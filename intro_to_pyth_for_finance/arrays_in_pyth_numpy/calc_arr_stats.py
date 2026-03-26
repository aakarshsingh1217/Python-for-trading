import numpy as np

stock_array = np.array([
    [170.12, 93.29, 55.28, 145.30, 171.81, 59.50, 100.50],
    [9.2,    5.31,  2.41,  5.91,   15.42,  2.51,  6.79]
])
stock_array_transposed = np.transpose(stock_array)
prices = stock_array_transposed[:, 0]
prices_mean = np.mean(prices)

print(prices_mean)

prices_std = np.std(prices)

print(prices_std)
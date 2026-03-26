import numpy as np

stock_array = np.array([
    [170.12, 93.29, 55.28, 145.30, 171.81, 59.50, 100.50],
    [9.2,    5.31,  2.41,  5.91,   15.42,  2.51,  6.79]
])

print(stock_array)
print(stock_array.shape)
print(stock_array.size)

print("\n##############\n")

stock_array_transposed = np.transpose(stock_array)

print(stock_array_transposed)
print(stock_array_transposed.shape)
print(stock_array_transposed.size)

print("\n##############\n")

prices = stock_array_transposed[:, 0]

print(prices)

earnings = stock_array_transposed[:, 1]

print(earnings)

company_1 = stock_array_transposed[0]

print(company_1)
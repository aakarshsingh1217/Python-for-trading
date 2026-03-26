import matplotlib.pyplot as plt

prices = [170.12, 93.29, 55.28, 145.30, 171.81, 59.50, 100.50]
months = [1, 2, 3, 4, 5, 6, 7]
prices_new = [price * 2 for price in prices]

# plt.plot(months, prices, color = 'red', linestyle = '--')
# plt.plot(months, prices_new, color = 'green', linestyle = '--')
# plt.xlabel('Months')
# plt.ylabel('Consumer Price Indexes, $')
# plt.title('Some data')
# plt.show()
# plt.scatter(x = months, y = prices, color = 'red')
# plt.show()

plt.hist(x=prices, bins=6, density=True, alpha=0.5, label="Prices 1")
plt.hist(x=prices_new, bins=6, density=True, alpha=0.5, label="Prices New")
plt.legend()
plt.show()
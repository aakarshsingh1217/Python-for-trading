import bt
import matplotlib.pyplot as plt

"""
With bt, we can use its get func. to fetch data online directly (bt.get).

By default, downloads adjusted close prices from Yahoo Finance by 
tickers.

A ticker is an abbreviated identifier for a public-traded stock, and 
"Adjusted Close" price is adjusted for events like corporate actions 
such as stock splits, dividends, etc.

Prices of multiple securities can be downloaded at once by specifying
multiple tickers within single str. seper. by commas.

Use start and end to specify start and end date.
"""
bt_data = bt.get('goog, amzn, tsla',
                 start = '2020-6-1', end='2020-12-1')
print(bt_data.head())

"""
Next we def. our strat. with bt.strategy.

The strategy contains trading logics by combining various "algos".
This unique feature of bt allows us to easily create strategies
by mixing and matching different algos, each of which acts like a small
task force that performs a specific operation.

Within strat. we first assign a name. Then we define a list of algos in the square
brackets. First algo specifies when to exect. trades. Second algo specifies what
data the strategy will apply to, for simplicity apply to all data using select all.
The third algo specifies, in the case of multiple assets, what weights apply to
each asset. Here WeighEqually means, for e.g., if we have 2 stocks, we will always
alloc. equal amounts of capital to each stock. Last algo specifies that it will
rebalance the asset weights according to what we've specified in the previous step.

Now have strat that will exect. trades weekly on a portfolio that holds several
stocks. It'll sell stock that's risen in price and redistribute profit to buy a
stock that's fallen in price, maintaining an equal amount of holdings in each
stock.
"""

bt_strategy = bt.Strategy('Trade_Weekly',
                          [bt.algos.RunWeekly(),    # Run weekly
                           bt.algos.SelectAll(),    # Use all data
                           bt.algos.WeighEqually(), # Maintain equal weights,
                           bt.algos.Rebalance()])   # Rebalance

"""
Now we can perform backtesting. Use bt.Backtest to combine the data and previously
defined strategy, and create a "backtest". Call bt.run to run the backtest and save the
res.
"""

# Create a backtest
bt_test = bt.Backtest(bt_strategy, bt_data)
# Run the backtest
bt_res = bt.run(bt_test)

"""
Can use dot plot to plot and review the result. Line chart shows if we apply the strat.
to trade Google, Amazon, Tesla stocks weekly, buy and sell them to maintain an equal
weighted stock portfolio, in the 6 months during 2020 our portfolio would incr. from
100 to 180.

Can also use .get_transactions() to print out transaction details.

What this plot represents:
- X-axis → time (June → Dec 2020)
- Y-axis → portfolio value (starting at 100)
- Line (“Trade_Weekly”) → how your strategy performed over time
What strat actually did:
- You told bt:
  - Run weekly
  - Use GOOG, AMZN, TSLA
  - Keep equal weights
  - Rebalance every week
- So effectively you simulated a portfolio that:
  - Invests equally in those 3 stocks
  - Every week:
    - Sells winners
    - Buys losers
    - Rebalances back to equal weights.
How to interpret result:
- Starting val. = 100 (normalized starting capital)
- Ending val. approx. = 180 - 185
  - Portfolio grew 80% in 6 months (probs. due to 2020 massive tech. rally)
Important insight:
- Strat basically: Equal-weighted tech portfolio with periodic rebalancing.
Don't overinterpret:
- Strat not amazing yet
- Why?:
  - Short time window (6 months)
  - Strong bull market
  - No transaction costs
  - No risk metrics yet
"""

# Plot the result
bt_res.plot(title="Backtest result")
plt.show()

# Get trade details
print("##############################################")
print(bt_res.get_transactions())

"""
1. Get the historical price data, either using bt.get() or loading data from existing 
CSV files.

2. Define the strategy with bt.Strategy() and pass in the strategy name and the algos 
needed.

3. Create a backtest with bt.Backtest(), pass in the strategy and data, and run the 
backtest.

4. Plot and evaluate the backtest result to assess the strategy’s viability.
"""
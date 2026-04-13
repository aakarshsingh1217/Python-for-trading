from binance.client import Client
import pandas as pd

api = "Ua0nz7FZ9RJSD003RvLH7ujsOdlD7p7XuA9a8BE5nM76PKhocDP0ZhXfYQx1voFl"
api_secret = "ozRfNa5lLCPVAjFNU8ugYZTydKl51fqoBCSskR4NnOvCHKqHBYLiBz0E65VPzsRl"

client = Client(api, api_secret, tld="com", testnet=True)

def get_balance():
    x = client.futures_account()
    df = pd.DataFrame(x['assets'])
    print(df)

"""
To place orders we have to use futures create order method
Within parantheses, we specify symbol, side (either buy or sell), type (limit order, 
which is an instruction to buy or sell a security at a specific price or better, 
ensuring price control over execution speed, it restricts the max price paid (buy) or 
min price received (sell)), then quantity and price.
Since this is a buy limit order, price is below current price level
"""
"""
Buy Limit Order:
client.futures_create_order(
    symbol="BTCUSDT",
    side=Client.SIDE_BUY,
    type=Client.FUTURE_ORDER_TYPE_LIMIT,
    timeInForce=Client.TIME_IN_FORCE_GTC,
    quantity=0.01,
    price=70000
)
"""
"""
Now we place sell limit order, where we have to specify price above current price level

Sell Limit order:
client.futures_create_order(
    symbol="BTCUSDT",
    side=Client.SIDE_SELL,
    type=Client.FUTURE_ORDER_TYPE_LIMIT,
    timeInForce=Client.TIME_IN_FORCE_GTC,
    quantity=0.01,
    price=74000
)
"""

"""
Now we create functions to place buy limit orders and sell limit orders.
"""

def sell_limit(symbol, volume, price):
    output = client.futures_create_order(
        symbol=symbol,
        side=Client.SIDE_SELL,
        type=Client.FUTURE_ORDER_TYPE_LIMIT,
        timeInForce=Client.TIME_IN_FORCE_GTC,
        quantity=volume,
        price=price
    )

    print(output)

def buy_limit(symbol, volume, price):
    output = client.futures_create_order(
        symbol=symbol,
        side=Client.SIDE_BUY,
        type=Client.FUTURE_ORDER_TYPE_LIMIT,
        timeInForce=Client.TIME_IN_FORCE_GTC,
        quantity=volume,
        price=price
    )

    print(output)

"""
buy_limit("BTCUSDT", 0.02, 71000)
sell_limit("BTCUSDT", 0.02, 73000)
"""

"""
Need to create a func. to close all pending orders.
"""

def close_orders(symbol):
    x = client.futures_get_open_orders(symbol=symbol)
    df = pd.DataFrame(x)

    for index in df.index:
        client.futures_cancel_order(
            symbol=symbol, 
            orderId=df["orderId"][index]
        )

"""
close_orders("BTCUSDT")
"""

"""
Now create seperate function to close buy and sell orders seperately
"""

def close_buy_orders(symbol):
    x = client.futures_get_open_orders(symbol=symbol)
    df = pd.DataFrame(x)
    df = df[df["side"] == "BUY"]
    for index in df.index:
        client.futures_cancel_order(
            symbol=symbol, 
            orderId=df["orderId"][index]
        )

def close_sell_orders(symbol):
    x = client.futures_get_open_orders(symbol=symbol)
    df = pd.DataFrame(x)
    df = df[df["side"] == "SELL"]
    for index in df.index:
        client.futures_cancel_order(
            symbol=symbol, 
            orderId=df["orderId"][index]
        )

"""
close_sell_orders("BTCUSDT")
"""

"""
Get direction of current positions

Need to check the sum of these positions, if the sum is greater than zero, direction
will be long, if the sum is less than 0, direction will be short, other direction is
flat.

Because we placed a buy market order, direction will be long.
Because we placed a sell market order and amt < 0, direction will be short.

What code does:
Ask Binance:
What is my current pos. in BTCUSDT?
Look at:
positionAmt
Sum it up and decide:
> 0 -> you hold BTC -> LONG
< 0 -> you're short BTC -> SHORT
= 0 -> no position -> FLAT

Strategy in one sentence:
Your direction = whatever position you currently hold

Interpretation:
If you bought (market order filled) -> you're LONG
If you sold (market order filled) -> you're SHORT
If nothing filled -> you're FLAT

This isn't the trading strategy itself, it's just:
Read my current exposure
It doesn't decide:
When to buy
When to sell
Only tells you:
What you already did

How it fits into a real strategy:
Usually used for:
RIsk management:
Am I too long or short?
Market making logic:
If LONG -> bias towards selling
If SHORT -> bias towards buying

LONG (> 0) → you own the asset → you profit if price goes up 📈
SHORT (< 0) → you owe/sold the asset → you profit if price goes down 📉
FLAT (= 0) → no position → you’re not exposed to price movement ↔️
"""

def get_direction(symbol):
    x = client.futures_position_information(symbol=symbol)
    df = pd.DataFrame(x)

    if float(df["positionAmt"].sum()) > 0:
        return "LONG"
    elif float(df["positionAmt"].sum()) < 0:
        return "SHORT"
    else:
        return "FLAT"

"""
print(get_direction("BTCUSDT"))
"""

"""
Now create func. to get curr. market price
"""

import requests

symbol = "BTCUSDT"

def get_current_price(symbol):
    response = requests.get(
        f"https://testnet.binancefuture.com/fapi/v1/ticker/price?symbol={symbol}"
    )

    # Get price from Binance Testnet
    price = float(response.json()['price'])

    return price

"""
print(get_current_price(symbol))
"""

"""
Create a function to place orders like a grid

After creating sell prices, we need to increase gap between these levels
with var. adj_sell initially equal to 1.2, multiply (pct_change / 100) * current_price
by adj_sell, and with each iteration increase the value of adj_sell by 0.2.

Then place sell limit order after calculation of sale price.

Now lets change the gap between these orders, create var. called proportion.

Write similar code for buy limit orders, this time pct_change = -1, adj_sell changed
to adj_buy, sell_price changed to buy_price, pct_change -= 1, adj_buy changed from
adj_sell, and sell_limit changed to buy_limit.

Explanation:

n plain english:
Find the current price, place several small sell orders above it, and several small 
buy orders below it.
So instead of just placing one buy and one sell, places a ladder of orders.


Imagine BTC is currently at 72,000.
Func. tries to place something like:
sell orders above current price:
72,034
72,065
72,104
...

current price:
72,000

buy orders below current price:
71,965
71,931
71,896
...
So if price moves up, some sell orders may fill.
If price moves down, some buy orders may fill.
This's the grid strategy.

What each var. means
num_decimal_places = 1
Round the final order to 1 decimal place
E.g.:
72123.456 becomes 72123.5, format the price

volume = 0.01
This means: every order will be 0.01 BTC
So each buy or sell order same sized.

proportion = 0.04
This's scaling factor that makes distance from curr price smaller.
Without it, percentages would create much bigger graps
With 0.04, gap reduced alot.
So var says: Only move a small fraction of the calc. perc. dist.

draw_grid(n)
Means: 
Create n sell orders above price, and n buy orders below price

First half: sell orders
pct_change = 1
Starts the first sell order at positive 1%
Means:
First sell order starts above curr. price
Since it's positive, pushes price upward from curr. market price.

adj_sell = 1.2
Extra multiplier that widens spacing
Starts at 1.2, then grows each loop, 1.4, 1.6, ...
As you go further out, each sell order gets placed a bit farther away.
Means: Don't keep all sell orders equally placed, spread them out more
and more.

current_price = get_currrent_price(symbol)
This fetches live price from Binance testnet
So if BTCUSDT is around 72689, becomes center point

Sell price formula
Is just: take the current price, calc. a small amount above it, then add that amount 
to curr. price.

Break into pieces:
pct_change / 100 turns percent into decimal
1 becomes 0.01, 2 becomes 0.02, ...
Gives percentage distance

times by (*) current_price
Now we're taking that percentage of the current BTC price.
If BTC is 72000:
1% of 72,000 = 720

times by (*) adj_sell
Stretches the gap
So if gap was 720, multiplying by 1.2 makes it 864

times by (*) proportion
Shrinks gap back down a lot
If 864 * 0.04 = 34.56
So now order is placed about 34.56 above curr price.

+ current_price
Now add that small gap onto curr. price
If curr. price is 72,000, then:
72,000 + 34.56 = 72,034.56
Then it gets rounded
So first sell order is around: 72,034.6

sell_limit(symbol, volume, sell_price)
Actually places the sell order on Binance
Once price calculated, bot says:
Place a sell limit order at this level.

Then vars change:
pct_change += 1
adj_sell += 0.2
So after first sell order:
pct_change goes from 1 to 2
adj_sell goes from 1.2 to 1.4
Means next sell order placed farther above market than first one.
So each new sell order is:
Based on a larger percentage
With a larger spacing multiplier
Makes sell ladder expand upward.

Second half: buy orders
After sell loop finishes, code resets vars.
pct_change = -1
adj_buy = 1.2
curr_price = ...
Now we're doing same thing, but below curr price

Why pct_change = -1?
Because neg perc. means:
Move below curr. price
So buy orders placed under market.
Makes sense because buy limit order usually placed lower, hoping price drops into it.

adj_buy = 1.2
Same idea as sell side:
first buy order is a bit below price
later buy orders are farther below price
This should widen the buy ladder downward.

Same structure as sell side, except now pct_change is negative.
So instead of adding a positive gap above price, it adds a negative gap, which 
effectively subtracts from current price.
So it says: “Take the current price and place a buy order a bit below it.”

Then: pct_change -= 1
This makes: -1, -2, ...
So each buy order goes further down, creating staircase of buy orders below market


Strategy idea
Code's trying to say:
Place several sell orders above curr. price
Place several buy orders below curr. price
Wait for price to move into them
This's grid strategy:
If price rises, upper sell orders may fill
If price falls, lower buy orders may fill
It's trying to capture movement in a range by scattering small orders around curr. 
market.
"""

num_decimal_places = 1
volume = 0.01
proportion = 0.04

# n: number of orders
def draw_grid(n):
    # Place sell limit orders
    pct_change = 1
    adj_sell = 1.2
    current_price = get_mark_price(symbol)

    for _ in range(n):
        # Calculate sell limit price
        sell_price = float(
            round(
                (((pct_change / 100) * current_price * adj_sell * proportion) 
                 + current_price
                ),
                num_decimal_places
            )
        )

        sell_limit(symbol, volume, sell_price)
        """
        First order will place 1% above current price, then second order will
        place 2% above current price, and so on.
        """
        pct_change += 1
        adj_sell += 0.2

    pct_change = -1
    adj_buy = 1.2
    current_price = get_mark_price(symbol)

    for _ in range(n):
        # Calculate buy limit price
        buy_price = float(
            round(
                (((pct_change / 100) * current_price * adj_buy * proportion) 
                 + current_price
                ),
                num_decimal_places
            )
        )

        buy_limit(symbol, volume, buy_price)

        pct_change -= 1
        adj_buy += 0.2

draw_grid(5)

"""
Create func. to calc. take profit level.

Purspoe of this code is:
Figure out a price where you want to exit your current trade in profit
So if your bot is already in a position, this func. tries to answer:
At what price should I close?
How big's my current position?
That's why it returns:
Price: the take profit exit price
t_pos_amt: the total amount of the position to close

Big picture
Imagine you bought BTC and now you want to sell it later for profit.
This func. tries to:
Look at your current trade
Figure out how much money is tied up in it
Calculate a target profit
Convert that target profit into an exit price
Return both the exit price and the size of the position

tp = 5
This means:
Target take-profit % = 5%
So bot is saying:
I want to make 5%  profit on the margin used for this trade.

Start of the function
def calc_take_profit_level(symbol, tp):
This means:
Calc. the take-profit level for a given symbol, using a chosen take-profit percent.
E.g.:
calc_take_profit_level("BTCUSDT", 5)
means:
For BTCUSDT, calc. exit price that would give me 5% profit.

Step 1: get your current position

x = client.futures_position_information(symbol=symbol)
df = pd.DataFrame(x)
This asks Binance:
“What is my current futures position in this symbol?”
Then it turns the answer into a table so it is easier to work with.

Step 2: keep only real positions
df = df.loc[df["positionAmt"] != "0.000"]
This means:
ignore rows where the position size is zero
So if you are not actually in a trade, those rows are removed.
if positionAmt = 0, you are not in a position
if positionAmt != 0, you do have a position

t_margin
t_margin = (
    float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0]))
) / float(df["leverage"][0])

Trying to calc:
How much margin is being used for this trade
Margin means: the amount of your own money you put up to hold a leveraged trade.
E.g.: 
You wan to control $1000
You use 10x leverage
Leverage means:
Using borrowed money to control a bigger position.
E.g.:
You have $100
With 10x  leverage, you can trade $1000
Leverage = amplify your position size using less of your own money
Then you only need:
$100 of your own money
That $100 is the margin
So in this context, how much margin is being used for the trade means:
How much of your capital is tied up backing that position

What each piece means
df["entryPrice"][0]
This is:
The price where you entered the trade
E.g.:
You entered BTC at 70,000

abs(float(df["positionAmt"][0]))
This is:
How big your position is, ignoring whether it's long or short
E.g.:
If position is 0.01, size of 0.01
If position is -0.01, size still 0.01
Abs used bc. size should be positive when calc. money involved

entryPrice * positionAmt
This gives:
Notional val. of trade
E.g.:
BTC entry price = 70000
Position size = 0.01
Then: 70000 * 0.01 = 700
So trade controls about $700 worth of BTC

/ leverage
This adjusts for leverage
If leverage is 10x, you don't need full 700 yourself.
You only need abt: 700 / 10 = 70
So:
t_margin = how much of your own money is tied up in trade

Meaning of t_margin
So t_margin means:
Margin used in position
In plain English:
How much of my own capital is backing this leveraged trade?

profit
profit = float(t_margin * tp * 0.01)
This means:
Calc dollar profit target

Break it down
tp (this's take profit percentage, like 5%, times by 0.01 turns into 0.05)
t_margin * 0.05 gives:
Amt of money you want to make

E.g.:
If t_margin = 100 and tp = 5, then:
profit = 100 * 5 * 0.01 = 5
So bot says: I want to make $5 profit
So profit means: the money profit target, based on the margin and the chosen take-profit %

price
This's trying to calc.:
Market price at which your total profit = target profit
Idea is:
Work out how much price must move per unit
Add that move to your entry price
That gives the take-profit exit price

Break logic down
profit / positionAmt
Trying to answer:
How much does price need to move to make this profit?
E.g.:
Target profit = $5
Position size = 0.01 BTC
Then:
5 / 0.01 = 500
So BTC needs to move about $500 in your favour

+ entryPrice
If entry price was 7000, then: 70000 + 500 = 70500
So take profit level would be: 70500
That's idea behind price

Meaning of price
So price means:
the target exit price where the bot wants to take profit
In plain English:
“If BTC reaches this price, my trade should make the profit I wanted.”

Why return price and t_pos_amt
Because later, bot needs both pieces of info.
Price tells bot where to place take profit order, e.g. place a sell order at 70500
t_pos_amt tells bot how much to close when taking profit, e.g. close 0.03 BTC, if you only returned price, bot would know where to exit but not how much to exit, If you only returned the amount, the bot would know how much to close but not at what price, so both needed.

t_pos_amt
This means:
add up the size of all open positions
So if there are multiple position rows, the code totals them.
Example:
0.01 + 0.02 = 0.03 = t_pos_amt

In one sentence
Func is trying to say:
Look at my current trade, work out how much margin I used, decide how much profit I want, convert that into a price target, and tell me both target price and total position size.

Clean layman summary of each variable
tp → desired profit percentage
t_margin → how much of your money is tied up in the leveraged trade
profit → how many dollars of profit you want
price → the BTC price that would give that profit
t_pos_amt → total size of the position to close

Simple analogy
Imagine:
you bought 1 item for $100
you want 5% profit
you invested $100
so you want $5 profit
that means you want to sell at $105
This function is doing the leveraged trading version of that same idea.
"""

tp = 5 # take profit = tp = 5 percent

def calc_take_profit_level(symbol, tp):
    try:
        # Get position info.
        x = client.futures_position_information(symbol=symbol)
        # Convert pos. to DataFrame
        df = pd.DataFrame(x)
        # Select positions which're greater than 0
        df = df.loc[df["positionAmt"] != "0.000"]
        # Calculate the margin
        # margin = entry price * % amount, then divide by leverage
        t_margin = (
            float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0]))
        ) / float(df["leverage"][0])
        # profit = total margin * take profit, since it's a percentage,
        # multiply by 0.01 and convert to float
        profit = float(t_margin * tp * 0.01)
        # Imagine margin is $10, take profit is $5, then profit'll be $0.5
        # Calc price level corresp. to this profit
        # Going to divide profit by position amount, then we're going to add
        # entry price. By using round function, we're going to round it
        # according to the number of decimal places
        price = (
            round((profit / float(df["positionAmt"][0])) + float(df["entryPrice"][0]),
                  num_decimal_places
            )
        )
        # Now, calc total position amount
        t_pos_amt = 0
        # Use for loop to iterate dataframe
        for index in df.index:
            t_pos_amt += abs(float(df["positionAmt"][index]))
        # return price and total position amt
        return price, t_pos_amt
    except:
        pass

def place_take_profit_order(symbol, price, t_pos_amt, dir):
    try:
        if dir == "LONG":
            sell_limit(symbol, t_pos_amt, price)
        elif dir == "SHORT":
            buy_limit(symbol, t_pos_amt, price)
    except:
        place_take_profit_order(symbol, price, t_pos_amt, dir)

"""
Because current price is highly variable, use mark price instead
"""
def get_mark_price(symbol):
    x = client.get_symbol_ticker(symbol)
    price = float(x["price"])

    return price

n = 5

"""
What get_mark_price doing
Func is getting reference price bot uses as its current market level
Says: ask binance for latest price of this symbol, pull num and give it back.

Draw grid needs a center price to build ladder of buy and sell orders around.
So instead of saying:
Sell above some old random number
Buy below some old random number

Code is getting ticker price, idea is use a steadier reference price e.g. latest ticker 
price.
Plain current price can jump around alot, stable anchor helps place cleaner buy/sell
levels.

Final while True loop

Main brain loop, keeps running forever and asks:
Do I have any open orders?
Do I have a position?
Do I need to place a grid?
Do I need to place or update a take-profit order?
Is the trade finished?

Big picture purpose of loop
Loop is triyng to do:
If no open orders, create a fresh grid
if one of those orders gets filled and becomes a real position:
Figure out if you're long or short
Remove opposite side orders
Place take profit order
Keep watching the position
If position changes, update take-profit order
If position disappears, clean everything up and go back to step 1
Whole loop's basically:
Build grid, detect when a trade happens, manage open trade, then reset.
"""
while True:
    x = client.futures_get_open_orders(symbol)
    df1 = pd.DataFrame(x)

    if len(df1) == 0:
        draw_grid(n)

    y = client.futures_position_information(symbol)
    df2 = pd.DataFrame(y)
    df2 = df2.loc[df2["positionAmt"] != "0.000"]

    if len(df2) > 0:
        direction = get_direction(symbol)

        try:
            if direction == "LONG":
                close_sell_orders(symbol)
            elif direction == "SHORT":
                close_buy_orders(symbol)
        except:
            pass

        price0, amt0 = calc_take_profit_level(symbol, tp)
        is_ok = True

        place_take_profit_order(symbol, price0, amt0, direction)

        while is_ok:
            try:
                price1, amt1 = calc_take_profit_level(symbol, tp)
                print(f"price: {price1} amt: {amt1}")

                if price1 != price0 or amt1 != amt0:
                    if direction == "LONG":
                        close_sell_orders(symbol)
                    elif direction == "SHORT":
                        close_buy_orders(symbol)

                    place_take_profit_order(symbol, price1, amt1, direction)
                    price0, amt0 = price1, amt1

            except:
                pass

            y = client.futures_position_information(symbol)
            df2 = pd.DataFrame(y)
            df2 = df2.loc[df2["positionAmt"] != "0.000"]

            if len(df2) == 0:
                try:
                    close_orders(symbol)
                    is_ok = False
                except:
                    pass
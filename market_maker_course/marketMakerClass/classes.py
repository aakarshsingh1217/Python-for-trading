from binance.client import Client
import pandas as pd
import requests

api = "Ua0nz7FZ9RJSD003RvLH7ujsOdlD7p7XuA9a8BE5nM76PKhocDP0ZhXfYQx1voFl"
api_secret = "ozRfNa5lLCPVAjFNU8ugYZTydKl51fqoBCSskR4NnOvCHKqHBYLiBz0E65VPzsRl"
client = Client(api, api_secret, tld="com", testnet=True)

class Bot:
    def __init__(
            self, 
            symbol, 
            num_decimals, 
            volume, 
            proportion, 
            take_profit, 
            num_orders
        ):
        self.symbol = symbol
        self.num_decimals = num_decimals
        self.volume = volume
        self.proportion = proportion
        self.take_profit = take_profit
        self.num_orders = num_orders

    def sell_limit(self, price):
        output = client.futures_create_order(
            symbol=self.symbol,
            side=Client.SIDE_SELL,
            type=Client.FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=self.volume,
            price=price
        )

        print(output)

    def buy_limit(self, price):
        output = client.futures_create_order(
            symbol=self.symbol,
            side=Client.SIDE_BUY,
            type=Client.FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=self.volume,
            price=price
        )

        print(output)

    def close_orders(self):
        x = client.futures_get_open_orders(symbol=self.symbol)
        df = pd.DataFrame(x)

        for index in df.index:
            client.futures_cancel_order(
                symbol=self.symbol, 
                orderId=df["orderId"][index]
            )

    def close_buy_orders(self):
        x = client.futures_get_open_orders(symbol=self.symbol)
        df = pd.DataFrame(x)
        df = df[df["side"] == "BUY"]
        for index in df.index:
            client.futures_cancel_order(
                symbol=self.symbol, 
                orderId=df["orderId"][index]
            )

    def close_sell_orders(self):
        x = client.futures_get_open_orders(symbol=self.symbol)
        df = pd.DataFrame(x)
        df = df[df["side"] == "SELL"]
        for index in df.index:
            client.futures_cancel_order(
                symbol=self.symbol, 
                orderId=df["orderId"][index]
            )

    def get_direction(self):
        x = client.futures_position_information(symbol=self.symbol)
        df = pd.DataFrame(x)

        if float(df["positionAmt"].sum()) > 0:
            return "LONG"
        elif float(df["positionAmt"].sum()) < 0:
            return "SHORT"
        else:
            return "FLAT"
        
    def draw_grid(self):
        # Place sell limit orders
        pct_change = 1
        adj_sell = 1.2
        current_price = self.get_mark_price()

        for _ in range(self.num_orders):
            # Calculate sell limit price
            sell_price = float(
                round(
                    (((pct_change / 100) * current_price * adj_sell * self.proportion) 
                    + current_price
                    ),
                    self.num_decimal_places
                )
            )

            self.sell_limit(sell_price)
            """
            First order will place 1% above current price, then second order will
            place 2% above current price, and so on.
            """
            pct_change += 1
            adj_sell += 0.2

        pct_change = -1
        adj_buy = 1.2
        current_price = self.get_mark_price()

        for _ in range(self.num_orders):
            # Calculate buy limit price
            buy_price = float(
                round(
                    (((pct_change / 100) * current_price * adj_buy * self.proportion) 
                    + current_price
                    ),
                    self.num_decimal_places
                )
            )

            self.buy_limit(buy_price)

            pct_change -= 1
            adj_buy += 0.2

    def get_mark_price(self):
        x = client.get_symbol_ticker(self.symbol)
        price = float(x["price"])

        return price
    
    def run(self):
        while True:
            x = client.futures_get_open_orders(self.symbol)
            df1 = pd.DataFrame(x)

            if len(df1) == 0:
                self.draw_grid()

            y = client.futures_position_information(self.symbol)
            df2 = pd.DataFrame(y)
            df2 = df2.loc[df2["positionAmt"] != "0.000"]

            if len(df2) > 0:
                direction = self.get_direction()

                try:
                    if direction == "LONG":
                        self.close_sell_orders()
                    elif direction == "SHORT":
                        self.close_buy_orders()
                except:
                    pass

                price0, amt0 = self.calc_take_profit_level(self.symbol, self.take_profit)
                is_ok = True

                self.place_take_profit_order(self.symbol, price0, amt0, direction)

                while is_ok:
                    try:
                        price1, amt1 = self.calc_take_profit_level(self.symbol, self.take_profit)
                        print(f"price: {price1} amt: {amt1}")

                        if price1 != price0 or amt1 != amt0:
                            if direction == "LONG":
                                self.close_sell_orders()
                            elif direction == "SHORT":
                                self.close_buy_orders()

                            self.place_take_profit_order(self.symbol, price1, amt1, direction)
                            price0, amt0 = price1, amt1

                    except:
                        pass

                    y = client.futures_position_information(self.symbol)
                    df2 = pd.DataFrame(y)
                    df2 = df2.loc[df2["positionAmt"] != "0.000"]

                    if len(df2) == 0:
                        try:
                            self.close_orders()
                            is_ok = False
                        except:
                            pass

bot = Bot("BTCUSDT", 1, 0.01, 0.04, 5, 5)
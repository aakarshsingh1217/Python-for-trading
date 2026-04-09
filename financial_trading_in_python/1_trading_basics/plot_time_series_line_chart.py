import plotly.graph_objects as go

some_data_eg_bitcoin = None

# Define the candlestick
candlestick = go.Candlestick(
    x = some_data_eg_bitcoin.index,
    open = some_data_eg_bitcoin["Open"],
    high = some_data_eg_bitcoin["High"],
    low = some_data_eg_bitcoin["Low"],
    close = some_data_eg_bitcoin["Close"]
)

# Call figure to create a plot, passing in data as list
fig = go.Figure(data=[candlestick])
# Show plot
fig.show()
import pandas as pd

"""
Pandas series is a 1D data structure, similar to a column in a table.
First we import pandas into Python, create list called x with vals., then 
create pandas series and pass in list using .Series and print
"""

x = ['a', 'b', 'c']
# Custom indexes using index = []
data_series = pd.Series(x, index=['letter1', 'letter2', 'letter3'])
print(data_series)

print(data_series.iloc[2]) # Selects specific element
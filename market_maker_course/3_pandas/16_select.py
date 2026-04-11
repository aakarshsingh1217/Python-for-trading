import pandas as pd

"""
Rets. pandas series:
x = df.Grade
print(x)
x = df["Grade"]
print(x)

Rets. pandas dataframe:
x = df[["Grade"]]
print(x)
"""

record = {
    'Name': ['Ankit'],
    'Age': [21],
    'Stream': ['Math'],
    'Percentage': [88]
}

df = pd.DataFrame(record)
print(df) # Returns dataframe (col names, indices, values)

print("################")

# Returns pandas series (indices and values)
x = df.Name
print(x)
x = df['Name']
print(x)
# Returns dataframe (col names, indices, values) of that val. and col
x = df[['Name']]
print(x)

"""
Selecting specific row of data frame:
x = df.loc[0]
print(x) (returns row 0 in pandas series)
x = df.loc[0]
print(x) (returns row 0 in pandas dataframe)
"""
print("################")

x = df.loc[0]
print(x)

print("################")

x = df.loc[[0]]
print(x)
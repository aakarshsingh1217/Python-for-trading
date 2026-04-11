import pandas as pd

"""
Pandas Data Frame is a 2D data structure, similar to a table with columns and rows
Each row has an index
You can specify a dict and pass it into a dataframe.
To index a dataframe, specify column and row
"""

hashmap = {
    "name": ["john", "alan"],
    "marks": [50, 70]
}
df = pd.DataFrame(hashmap)
print(df["marks"][1])
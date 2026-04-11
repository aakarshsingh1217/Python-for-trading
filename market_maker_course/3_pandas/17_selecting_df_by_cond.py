"""
Select rows by col. vals.
x = df.loc[df.age > 20]
print(x) # Returns rows > 20

x = df.loc[df.Marks > 85]
print(x) # Returns rows where marks are > 85

x = df.loc[df.Marks > 85]["Name"]
print(x) # Returns rows where marks are > 85 and print name vals.
         # of each col
"""
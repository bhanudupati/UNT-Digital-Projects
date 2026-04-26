import pandas as pd

df = pd.read_csv('K7kUaRU4 - projects-in-progress(K7kUaRU4 - projects-in-progress).csv', low_memory=False)
print('Shape:', df.shape)
print('Columns:', df.columns.tolist())